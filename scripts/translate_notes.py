import json
import os
import random
import re
import sys
import time
import hashlib
import urllib.error
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TRANSLATIONS_DIR = ROOT_DIR / "translations"
EN_DIR = TRANSLATIONS_DIR / "en"
FR_DIR = TRANSLATIONS_DIR / "fr"
CACHE_FILE = TRANSLATIONS_DIR / "translation_cache.json"

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
MAX_RETRIES = 7
BATCH_SIZE = 24
MAX_REQUEST_CHARS = 14000
INITIAL_RETRY_DELAY = 8.0

EXCLUDED_DIRS = {
    ".git", ".github", ".obsidian", ".venv-pages",
    "docs", "site", "scripts", "translations",
}

ORIGINAL_SECTION_MARKER = "\n---\n\n## 中文原文\n\n"

# Markdown constructs which must never be sent to Gemini.
INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
WIKILINK_RE = re.compile(r"!?\[\[[^\]\n]+\]\]")
AUTOLINK_RE = re.compile(r"<(?:https?://|mailto:)[^>\n]+>", re.I)
URL_RE = re.compile(r"(?:https?://|ftp://|www\.)[^\s<>()]+", re.I)
HTML_TAG_RE = re.compile(r"</?[A-Za-z][^>\n]*>")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]\n]*\]\([^) \n]+(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def info(message):
    print(message, flush=True)


def warning(message):
    print(f"  WARNING: {message}", flush=True)


def error(message):
    print(f"  ERROR: {message}", flush=True)


def read_text(path):
    return path.read_text(encoding="utf-8")


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def get_file_md5(text_content):
    # 强制将可能混入的 \r\n 统一替换为 \n，防止不同操作系统下 MD5 误判
    normalized_text = text_content.replace("\r\n", "\n")
    return hashlib.md5(normalized_text.encode("utf-8")).hexdigest()


def load_cache():
    if CACHE_FILE.exists():
        try:
            return json.loads(read_text(CACHE_FILE))
        except Exception as e:
            warning(f"Failed to load cache: {e}. Starting fresh.")
    return {}


def save_cache(cache_dict):
    write_text(CACHE_FILE, json.dumps(cache_dict, indent=2))


def is_source_markdown_file(path):
    if path.suffix.lower() != ".md" or not path.is_file():
        return False
    try:
        relative = path.relative_to(ROOT_DIR)
    except ValueError:
        return False
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if any(part.startswith(".") for part in relative.parts):
        return False
    return True


def find_markdown_files():
    return sorted(
        path for path in ROOT_DIR.rglob("*.md")
        if is_source_markdown_file(path)
    )


def markdown_files_from_list(list_path):
    result = []
    for line in read_text(list_path).splitlines():
        value = line.strip()
        if not value:
            continue
        path = (ROOT_DIR / value).resolve()
        if is_source_markdown_file(path):
            result.append(path)
    return sorted(set(result))


def selected_markdown_files():
    args = sys.argv[1:]
    if not args:
        return find_markdown_files()
    if len(args) == 2 and args[0] == "--files-from":
        return markdown_files_from_list((ROOT_DIR / args[1]).resolve())
    raise RuntimeError("Usage: translate_notes.py [--files-from PATH]")


def split_protected_text(line):
    newline = "\n" if line.endswith("\n") else ""
    content = line[:-1] if newline else line

    if not content.strip():
        return [("protected", line)]

    prefix = ""
    body = content

    m = re.match(r"^(\s{0,3}#{1,6}\s+)(.*)$", body)
    if m:
        prefix, body = m.group(1), m.group(2)
    else:
        m = re.match(
            r"^(\s{0,3}(?:[-+*]|\d+[.)])\s+)(.*)$", body
        )
        if m:
            prefix, body = m.group(1), m.group(2)
        else:
            m = re.match(r"^(\s{0,3}>\s?)(.*)$", body)
            if m:
                prefix, body = m.group(1), m.group(2)

    parts = [("protected", prefix)] if prefix else []

    patterns = [
        INLINE_CODE_RE,
        WIKILINK_RE,
        MARKDOWN_LINK_RE,
        AUTOLINK_RE,
        URL_RE,
        HTML_TAG_RE,
    ]
    combined = re.compile(
        "|".join(f"(?:{p.pattern})" for p in patterns),
        re.I | re.X,
    )

    pos = 0
    for match in combined.finditer(body):
        if match.start() > pos:
            parts.append(("text", body[pos:match.start()]))
        parts.append(("protected", match.group(0)))
        pos = match.end()

    if pos < len(body):
        parts.append(("text", body[pos:]))

    if newline:
        parts.append(("protected", newline))
    return parts


def parse_markdown(text):
    lines = text.splitlines(keepends=True)
    result = []
    in_fence = False
    fence_char = None

    for line in lines:
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            char = marker[0]
            if not in_fence:
                in_fence = True
                fence_char = char
                result.append(("code", line))
                continue
            if char == fence_char:
                result.append(("code", line))
                in_fence = False
                fence_char = None
                continue

        if in_fence:
            result.append(("code", line))
        else:
            result.append(("text", split_protected_text(line)))
    return result


def has_chinese(text):
    return bool(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", text))


def contains_translatable_text(text):
    if not text.strip():
        return False
    return bool(re.search(r"[A-Za-zÀ-ÖØ-öø-ÿ\u3400-\u9fff]", text))


def build_items(parsed):
    items = []
    locations = []
    item_id = 0

    for line_index, (kind, value) in enumerate(parsed):
        if kind == "code":
            continue
        for part_index, (part_kind, content) in enumerate(value):
            if part_kind == "text" and contains_translatable_text(content):
                items.append((item_id, content))
                locations.append((line_index, part_index, item_id))
                item_id += 1
    return items, locations


def build_batches(items):
    batches = []
    current = []
    size = 0

    for item in items:
        item_size = len(item[1])
        if current and (
            len(current) >= BATCH_SIZE
            or size + item_size > MAX_REQUEST_CHARS
        ):
            batches.append(current)
            current = []
            size = 0
        current.append(item)
        size += item_size

    if current:
        batches.append(current)
    return batches


def translation_prompt(target, items):
    language = "English" if target == "en" else "French"
    payload = [{"id": i, "text": text} for i, text in items]

    return f"""
You are translating technical documentation from Chinese into {language}.

The documentation is about C programming, Libft, Unix, pointers,
memory, strings, compilation, Makefiles, Git, GitHub, Markdown and
42 School.

Translate EVERY Chinese natural-language passage completely and
faithfully into {language}. Do not leave Chinese prose untranslated.

Important:
- The input contains ONLY natural-language text fragments.
- Markdown syntax, code, URLs, function names and identifiers have
  already been removed by the Python program.
- Do not invent information.
- Do not summarize.
- Do not omit sentences.
- Keep technical identifiers such as strlen, memchr, memmove, strdup,
  calloc, malloc, NULL, size_t, char, int, src, dst, s1, s2 unchanged
  when they occur in prose.
- Keep numbers and technical expressions accurate.
- For French, use natural technical French.
- For English, use natural technical English.
- If a fragment is already English/French and contains no Chinese,
  preserve its meaning and wording.
- Return ONLY a JSON array.
- Every input id must appear exactly once.
- Each object must have integer "id" and string "translation".
- Preserve whitespace at the beginning/end of each fragment when
  practical.

INPUT:
{json.dumps(payload, ensure_ascii=False, indent=2)}
""".strip()


def api_url(model):
    return (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{model}:generateContent"
    )


def api_request(prompt):
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1,
        },
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    request = urllib.request.Request(
        api_url(MODEL),
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": API_KEY,
        },
    )

    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.loads(response.read().decode("utf-8"))

    candidates = result.get("candidates") or []
    if not candidates:
        raise RuntimeError("Gemini returned no candidates.")

    parts = candidates[0].get("content", {}).get("parts", [])
    output = "".join(
        part.get("text", "") for part in parts if "text" in part
    )
    if not output:
        raise RuntimeError("Gemini returned an empty response.")
    return output


def parse_json_response(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        if len(lines) >= 2:
            raw = "\n".join(lines[1:-1]).strip()

    data = json.loads(raw)
    if not isinstance(data, list):
        raise RuntimeError("Gemini response is not a JSON array.")

    result = {}
    for item in data:
        if not isinstance(item, dict):
            raise RuntimeError("Invalid translation item.")
        item_id = item.get("id")
        translation = item.get("translation")
        if not isinstance(item_id, int) or not isinstance(translation, str):
            raise RuntimeError("Invalid translation id/value.")
        if item_id in result:
            raise RuntimeError(f"Duplicate translation id: {item_id}")
        result[item_id] = translation
    return result


def translate_batch(target, items):
    prompt = translation_prompt(target, items)
    expected = {i for i, _ in items}
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            info(
                f"  Translation request {attempt}/{MAX_RETRIES} "
                f"({len(items)} fragments)"
            )
            result = parse_json_response(api_request(prompt))
            if set(result) != expected:
                missing = sorted(expected - set(result))
                extra = sorted(set(result) - expected)
                raise RuntimeError(
                    f"Translation item mismatch. Missing={missing}, Extra={extra}"
                )

            if target in ("en", "fr"):
                bad = [
                    (i, result[i])
                    for i, _ in items
                    if has_chinese(result[i])
                ]
                if bad:
                    sample = bad[0][1][:120].replace("\n", " ")
                    raise RuntimeError(
                        f"Chinese text remains in translated fragment {bad[0][0]}: "
                        f"{sample}"
                    )

            return result

        except urllib.error.HTTPError as exc:
            last_error = exc
            try:
                body = exc.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""

            # 处理 429 和 5xx 服务端错误进行退避重试
            if exc.code in (429, 500, 502, 503, 504) and attempt < MAX_RETRIES:
                retry_after = exc.headers.get("Retry-After")
                try:
                    delay = float(retry_after) if retry_after else 0.0
                except ValueError:
                    delay = 0.0
                if delay <= 0:
                    delay = INITIAL_RETRY_DELAY * (2 ** (attempt - 1))
                delay += random.uniform(0.0, 1.5)
                warning(f"HTTP {exc.code}. Retrying in {delay:.1f}s...")
                time.sleep(delay)
                continue

            raise RuntimeError(
                f"Gemini HTTP {exc.code}: {body[:500]}"
            ) from exc

        except (urllib.error.URLError, TimeoutError, ValueError, RuntimeError) as exc:
            last_error = exc
            if attempt >= MAX_RETRIES:
                break
            delay = INITIAL_RETRY_DELAY * (2 ** (attempt - 1))
            delay += random.uniform(0.0, 1.0)
            warning(f"{exc}. Retrying in {delay:.1f}s...")
            time.sleep(delay)

    raise RuntimeError(
        f"Translation request failed after {MAX_RETRIES} attempts: {last_error}"
    )


def translate_markdown(source, target):
    parsed = parse_markdown(source)
    items, locations = build_items(parsed)

    if not items:
        return source

    translated = {}
    batches = build_batches(items)

    info(
        f"  {len(items)} translatable fragments, "
        f"{len(batches)} API request(s)"
    )

    for number, batch in enumerate(batches, 1):
        translated.update(translate_batch(target, batch))
        if number < len(batches):
            time.sleep(1.0)

    for line_index, part_index, item_id in locations:
        parts = parsed[line_index][1]
        parts[part_index] = ("text", translated[item_id])

    output = []
    for kind, value in parsed:
        if kind == "code":
            output.append(value)
        else:
            output.append("".join(content for _, content in value))
    return "".join(output)


def translation_body(text):
    if ORIGINAL_SECTION_MARKER in text:
        return text.split(ORIGINAL_SECTION_MARKER, 1)[0]
    return text


def compose_translation_page(translated, original):
    translated = translated.rstrip("\n") + "\n"
    original = original.rstrip("\n") + "\n"
    return translated + ORIGINAL_SECTION_MARKER + original


def translation_path(source_path, language):
    relative = source_path.relative_to(ROOT_DIR)
    return (EN_DIR if language == "en" else FR_DIR) / relative


def natural_text_without_code(text):
    parsed = parse_markdown(translation_body(text))
    result = []
    for kind, value in parsed:
        if kind == "code":
            continue
        for part_kind, content in value:
            if part_kind == "text":
                result.append(content)
    return "\n".join(result)


def validate_translation(source, translated, target):
    body = translation_body(translated)
    if not body.strip():
        return False

    src_parsed = parse_markdown(source)
    out_parsed = parse_markdown(body)

    src_code = [v for k, v in src_parsed if k == "code"]
    out_code = [v for k, v in out_parsed if k == "code"]
    if src_code != out_code:
        warning("Fenced code blocks were changed.")
        return False

    def protected_values(parsed):
        values = []
        for kind, value in parsed:
            if kind == "code":
                values.append(value)
                continue
            for part_kind, content in value:
                if part_kind == "protected":
                    values.append(content)
        return values

    if protected_values(src_parsed) != protected_values(out_parsed):
        warning("Protected Markdown syntax was changed.")
        return False

    if has_chinese(natural_text_without_code(body)):
        warning("Chinese natural-language text remains untranslated.")
        return False

    return True


def existing_translation_is_valid(source, path, target):
    if not path.exists():
        return False
    try:
        text = read_text(path)
    except OSError:
        return False
    if ORIGINAL_SECTION_MARKER not in text:
        return False
    return validate_translation(source, text, target)


def translate_file(source_path, file_cache):
    relative = str(source_path.relative_to(ROOT_DIR))
    info("")
    info(f"PROCESS: {relative}")

    source = read_text(source_path)
    if not source.strip():
        info(f"SKIP EMPTY: {relative}")
        return True, file_cache

    current_md5 = get_file_md5(source)

    if file_cache.get(relative) == current_md5:
        en_path = translation_path(source_path, "en")
        fr_path = translation_path(source_path, "fr")

        if existing_translation_is_valid(source, en_path, "en") and \
           existing_translation_is_valid(source, fr_path, "fr"):
            info(f"  UNCHANGED (Cached): Skipping API call.")
            return True, file_cache

    success = True
    translation_passed = {"en": False, "fr": False}

    for target in ("en", "fr"):
        output_path = translation_path(source_path, target)

        if existing_translation_is_valid(source, output_path, target):
            info(f"  {target.upper()} already valid (will reuse local copy)")
            translation_passed[target] = True
            continue

        language = "English" if target == "en" else "French"
        info(f"  Translating -> {language}")

        try:
            translated = translate_markdown(source, target)
            if not validate_translation(source, translated, target):
                raise RuntimeError(
                    f"{language} translation failed validation."
                )

            page = compose_translation_page(translated, source)
            if not validate_translation(source, page, target):
                raise RuntimeError(
                    f"{language} generated page failed validation."
                )

            write_text(output_path, page)
            info(f"  Saved: {output_path.relative_to(ROOT_DIR)}")
            translation_passed[target] = True

        except Exception as exc:
            error(f"{target.upper()} translation failed: {exc}")
            success = False

    # 每翻译完一篇，只要合法就立刻存入硬盘，防止因后续 API 错误导致进度丢失
    if translation_passed["en"] and translation_passed["fr"]:
        file_cache[relative] = current_md5
        save_cache(file_cache)
        info(f"  Cache updated and saved to disk for {relative}")

    return success, file_cache


def verify_all_translations(files):
    info("")
    info("Verifying all translations...")

    invalid_en = []
    invalid_fr = []

    for source_path in files:
        source = read_text(source_path)
        if not source.strip():
            continue

        for target, invalid in (("en", invalid_en), ("fr", invalid_fr)):
            path = translation_path(source_path, target)
            if not existing_translation_is_valid(source, path, target):
                invalid.append(str(path.relative_to(ROOT_DIR)))

    if invalid_en:
        info("")
        info("Invalid English translations:")
        for path in invalid_en:
            info(f"  {path}")

    if invalid_fr:
        info("")
        info("Invalid French translations:")
        for path in invalid_fr:
            info(f"  {path}")

    if invalid_en or invalid_fr:
        return False

    info("All translations are valid.")
    return True


def main():
    if not API_KEY:
        error("GEMINI_API_KEY environment variable is not set.")
        return 1

    try:
        files = selected_markdown_files()
    except Exception as exc:
        error(str(exc))
        return 1

    info(f"Found {len(files)} Markdown files.")

    if not files:
        warning("No Markdown files found.")
        return 0

    success = True
    file_cache = load_cache()

    for path in files:
        file_success, file_cache = translate_file(path, file_cache)
        if not file_success:
            success = False

    # 执行到这里说明全部循环正常结束，进行最后一次保险保存
    save_cache(file_cache)

    if not verify_all_translations(files):
        success = False

    if not success:
        error("Translation process FAILED.")
        return 1

    info("")
    info("Translation process completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
