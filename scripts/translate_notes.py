import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

TRANSLATIONS_DIR = ROOT_DIR / "translations"

EN_DIR = TRANSLATIONS_DIR / "en"
FR_DIR = TRANSLATIONS_DIR / "fr"

API_KEY = os.environ.get("GEMINI_API_KEY")

MODEL = os.environ.get(
    "GEMINI_MODEL",
    "gemini-3.6-flash",
)

FALLBACK_MODEL = "gemini-3.6-flash"

MODEL_CANDIDATES = []

for model in (MODEL, FALLBACK_MODEL):
    if model not in MODEL_CANDIDATES:
        MODEL_CANDIDATES.append(model)

MAX_RETRIES = 6

# Number of natural-language fragments sent in one request.
BATCH_SIZE = 40

# Gemini API can temporarily return 429.
INITIAL_RETRY_DELAY = 10.0

# Maximum size of one translation request.
MAX_REQUEST_CHARS = 18000

SOURCE_EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".obsidian",
    ".venv-pages",
    "docs",
    "site",
    "scripts",
    "translations",
}

ORIGINAL_SECTION_HEADING = "## 中文原文"
ORIGINAL_SECTION_MARKER = f"\n---\n\n{ORIGINAL_SECTION_HEADING}\n\n"


# ============================================================
# Console helpers
# ============================================================

def info(message):
    print(message, flush=True)


def warning(message):
    print(f"  WARNING: {message}", flush=True)


def error(message):
    print(f"  ERROR: {message}", flush=True)


# ============================================================
# File discovery
# ============================================================

def is_source_markdown_file(path):
    if path.suffix != ".md":
        return False

    try:
        relative = path.relative_to(ROOT_DIR)
    except ValueError:
        return False

    if not relative.parts:
        return False

    # Only source notes should be translated. Generated docs,
    # translations, workflows, scripts, and hidden directories
    # must not become translation sources.
    if any(
        part in SOURCE_EXCLUDED_DIRS
        for part in relative.parts
    ):
        return False

    # Never process .git or other hidden directories.
    if any(part.startswith(".") for part in relative.parts):
        return False

    if len(relative.parts) == 1:
        return False

    return path.exists()


def find_markdown_files():
    files = []

    for path in ROOT_DIR.rglob("*.md"):
        if is_source_markdown_file(path):
            files.append(path)

    files.sort()

    return files


def markdown_files_from_list(list_path):
    files = []

    for line in read_text(list_path).splitlines():
        value = line.strip()

        if not value:
            continue

        path = (ROOT_DIR / value).resolve()

        if is_source_markdown_file(path):
            files.append(path)

    files = sorted(set(files))

    return files


def selected_markdown_files():
    args = sys.argv[1:]

    if not args:
        return find_markdown_files()

    if len(args) == 2 and args[0] == "--files-from":
        return markdown_files_from_list(
            (ROOT_DIR / args[1]).resolve()
        )

    raise RuntimeError(
        "Usage: translate_notes.py [--files-from PATH]"
    )


# ============================================================
# Markdown protection
# ============================================================

INLINE_CODE_RE = re.compile(
    r"`+[^`\n]*`+"
)

URL_RE = re.compile(
    r"""
    (?:
        https?://[^\s<>()]+
        |
        ftp://[^\s<>()]+
        |
        www\.[^\s<>()]+
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

HTML_TAG_RE = re.compile(
    r"</?[A-Za-z][^>\n]*>"
)

AUTOLINK_RE = re.compile(
    r"<(?:https?://|mailto:)[^>\n]+>",
    re.IGNORECASE,
)

OBSIDIAN_LINK_RE = re.compile(
    r"!\[\[[^\]\n]+\]\]|\[\[[^\]\n]+\]\]"
)

MARKDOWN_LINK_RE = re.compile(
    r"!?\[[^\]\n]*\]\([^) \n]+(?:\s+\"[^\"]*\")?\)"
)


def protect_inline_markdown(text):
    patterns = [
        INLINE_CODE_RE,
        OBSIDIAN_LINK_RE,
        MARKDOWN_LINK_RE,
        AUTOLINK_RE,
        URL_RE,
        HTML_TAG_RE,
    ]

    combined = re.compile(
        "|".join(
            f"({pattern.pattern})"
            for pattern in patterns
        ),
        re.IGNORECASE | re.VERBOSE,
    )

    fragments = []
    position = 0

    for match in combined.finditer(text):
        if match.start() > position:
            fragments.append(
                ("text", text[position:match.start()])
            )

        fragments.append(
            ("protected", match.group(0))
        )

        position = match.end()

    if position < len(text):
        fragments.append(
            ("text", text[position:])
        )

    if not fragments:
        fragments.append(("text", text))

    return fragments


FENCE_RE = re.compile(
    r"^\s*(```+|~~~+)"
)

HEADING_RE = re.compile(
    r"^(\s{0,3}#{1,6}\s+)(.*)$"
)

BLOCKQUOTE_RE = re.compile(
    r"^(\s{0,3}>\s?)(.*)$"
)

LIST_RE = re.compile(
    r"""
    ^
    (
        \s{0,3}
        (?:
            [-+*]
            |
            \d+[.)]
        )
        \s+
    )
    (.*)
    $
    """,
    re.VERBOSE,
)

TABLE_SEPARATOR_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$"
)


def split_markdown_line(line):
    newline = ""

    if line.endswith("\n"):
        newline = "\n"
        content = line[:-1]
    else:
        content = line

    if not content.strip():
        return [("protected", content + newline)]

    if TABLE_SEPARATOR_RE.match(content):
        return [("protected", content + newline)]

    if FENCE_RE.match(content):
        return [("protected", content + newline)]

    match = HEADING_RE.match(content)

    if match:
        prefix = match.group(1)
        body = match.group(2)

        result = [("protected", prefix)]
        result.extend(protect_inline_markdown(body))

        if newline:
            result.append(("protected", newline))

        return result

    match = BLOCKQUOTE_RE.match(content)

    if match:
        prefix = match.group(1)
        body = match.group(2)

        result = [("protected", prefix)]
        result.extend(protect_inline_markdown(body))

        if newline:
            result.append(("protected", newline))

        return result

    match = LIST_RE.match(content)

    if match:
        prefix = match.group(1)
        body = match.group(2)

        result = [("protected", prefix)]
        result.extend(protect_inline_markdown(body))

        if newline:
            result.append(("protected", newline))

        return result

    result = protect_inline_markdown(content)

    if newline:
        result.append(("protected", newline))

    return result


def parse_markdown(text):
    lines = text.splitlines(keepends=True)

    blocks = []
    in_fence = False
    fence_marker = None
    current_text = []

    def flush_text():
        if current_text:
            blocks.append(
                {
                    "type": "text",
                    "content": "".join(current_text),
                }
            )
            current_text.clear()

    for line in lines:
        fence_match = FENCE_RE.match(line)

        if fence_match:
            marker = fence_match.group(1)

            if not in_fence:
                flush_text()

                in_fence = True
                fence_marker = marker[0]

                blocks.append(
                    {
                        "type": "code",
                        "content": line,
                    }
                )

                continue

            if marker.startswith(fence_marker):
                blocks.append(
                    {
                        "type": "code",
                        "content": line,
                    }
                )

                in_fence = False
                fence_marker = None

                continue

        if in_fence:
            blocks.append(
                {
                    "type": "code",
                    "content": line,
                }
            )
        else:
            current_text.append(line)

    flush_text()

    return blocks


def extract_translatable_fragments(text):
    fragments = []

    lines = text.splitlines(keepends=True)

    for line in lines:
        fragments.extend(
            split_markdown_line(line)
        )

    return fragments


def merge_fragments(fragments, translations):
    output = []

    for index, fragment in enumerate(fragments):
        kind, content = fragment

        if kind == "protected":
            output.append(content)
        else:
            output.append(
                translations.get(index, content)
            )

    return "".join(output)


def contains_translatable_text(text):
    if not text.strip():
        return False

    letters = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ\u4e00-\u9fff]", text)

    return len(letters) >= 2


def clean_model_output(text):
    text = text.strip()

    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()

        if len(lines) >= 2:
            lines = lines[1:-1]
            text = "\n".join(lines)

    return text


def build_translation_prompt(target_language, items):
    language_name = {
        "en": "English",
        "fr": "French",
    }[target_language]

    payload = []

    for item_id, text in items:
        payload.append(
            {
                "id": item_id,
                "text": text,
            }
        )

    payload_text = json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
    )

    return f"""
You are translating technical Markdown documentation.

Translate ONLY the natural-language text values in the JSON input
into {language_name}.

This documentation is about C programming, Libft, Unix, memory,
strings, pointers, compilation, Makefiles, and 42 School.

Rules:

1. Return ONLY valid JSON.
2. Return an array of objects.
3. Each object MUST contain:
   - "id": the original integer ID
   - "translation": the translated text
4. Do not remove any item.
5. Do not invent any item.
6. IDs may be returned in any order.
7. Do not translate programming identifiers.
8. Keep function names such as:
   strlen, memset, memcpy, memmove, memchr, memcmp,
   strlcpy, strlcat, strchr, strrchr, strncmp, strnstr,
   strdup, calloc, malloc, free
   unchanged.
9. Keep C keywords unchanged.
10. Keep technical identifiers unchanged.
11. Preserve numbers, operators, punctuation, and mathematical
    expressions whenever they are part of the technical meaning.
12. Do not add Markdown formatting.
13. Do not add code fences.
14. Do not add explanations.
15. Do not summarize.
16. Translate the text faithfully and completely.
17. Preserve the meaning of the original documentation.
18. For English, use natural technical English.
19. For French, use natural technical French suitable for
    programming documentation.
20. If the input is already in the requested language, return it
    unchanged.
21. Do not translate Chinese technical identifiers or code syntax
    unless they are ordinary natural-language prose.

JSON input:

{payload_text}
""".strip()


def gemini_api_url(model):
    return (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{model}:generateContent"
    )


def api_request(prompt, model):
    if not API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not set."
        )

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
        },
    }

    data = json.dumps(
        body,
        ensure_ascii=False,
    ).encode("utf-8")

    request = urllib.request.Request(
        gemini_api_url(model),
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": API_KEY,
        },
    )

    with urllib.request.urlopen(
        request,
        timeout=120,
    ) as response:
        raw = response.read().decode("utf-8")

    result = json.loads(raw)

    candidates = result.get("candidates")

    if not candidates:
        raise RuntimeError(
            "Gemini returned no candidates."
        )

    content = candidates[0].get("content", {})
    parts = content.get("parts", [])

    output = []

    for part in parts:
        if "text" in part:
            output.append(part["text"])

    if not output:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return "".join(output)


def translate_batch(target_language, items):
    prompt = build_translation_prompt(
        target_language,
        items,
    )

    last_error = None

    for model in MODEL_CANDIDATES:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                info(
                    f"  Translation request "
                    f"{attempt}/{MAX_RETRIES} "
                    f"with {model} "
                    f"({len(items)} fragments)"
                )

                raw = api_request(prompt, model)
                raw = clean_model_output(raw)
                data = json.loads(raw)

                if not isinstance(data, list):
                    raise RuntimeError(
                        "Gemini response is not a JSON array."
                    )

                translations = {}

                for item in data:
                    if not isinstance(item, dict):
                        raise RuntimeError(
                            "Invalid translation item."
                        )

                    if "id" not in item:
                        raise RuntimeError(
                            "Translation item has no id."
                        )

                    if "translation" not in item:
                        raise RuntimeError(
                            "Translation item has no translation."
                        )

                    item_id = item["id"]
                    translation = item["translation"]

                    if not isinstance(item_id, int):
                        raise RuntimeError(
                            "Translation id is not an integer."
                        )

                    if not isinstance(translation, str):
                        raise RuntimeError(
                            "Translation value is not a string."
                        )

                    translations[item_id] = translation

                expected_ids = {
                    item_id
                    for item_id, _ in items
                }

                returned_ids = set(translations.keys())

                if expected_ids != returned_ids:
                    missing = sorted(
                        expected_ids - returned_ids
                    )

                    extra = sorted(
                        returned_ids - expected_ids
                    )

                    raise RuntimeError(
                        "Translation item mismatch. "
                        f"Missing={missing}, Extra={extra}"
                    )

                return translations

            except urllib.error.HTTPError as exc:
                last_error = exc

                try:
                    response_body = exc.read().decode(
                        "utf-8",
                        errors="replace",
                    )
                except Exception:
                    response_body = ""

                if exc.code == 404 and model != MODEL_CANDIDATES[-1]:
                    warning(
                        f"Model {model} is unavailable. "
                        f"Trying {MODEL_CANDIDATES[-1]}..."
                    )
                    break

                if exc.code == 429:
                    if attempt >= MAX_RETRIES:
                        break

                    retry_after = exc.headers.get(
                        "Retry-After"
                    )

                    if retry_after:
                        try:
                            delay = float(retry_after)
                        except ValueError:
                            delay = (
                                INITIAL_RETRY_DELAY
                                * (2 ** (attempt - 1))
                            )
                    else:
                        delay = (
                            INITIAL_RETRY_DELAY
                            * (2 ** (attempt - 1))
                        )

                    delay += random.uniform(0.0, 1.5)

                    warning(
                        f"HTTP 429. "
                        f"Retrying in {delay:.1f}s..."
                    )

                    time.sleep(delay)
                    continue

                raise RuntimeError(
                    f"Gemini HTTP {exc.code}: "
                    f"{response_body[:500]}"
                ) from exc

            except (
                urllib.error.URLError,
                TimeoutError,
                json.JSONDecodeError,
                RuntimeError,
            ) as exc:
                last_error = exc

                if attempt >= MAX_RETRIES:
                    break

                delay = (
                    INITIAL_RETRY_DELAY
                    * (2 ** (attempt - 1))
                )

                delay += random.uniform(0.0, 1.0)

                warning(
                    f"{exc}. "
                    f"Retrying in {delay:.1f}s..."
                )

                time.sleep(delay)

    raise RuntimeError(
        f"Translation request failed after "
        f"{MAX_RETRIES} attempts: {last_error}"
    )


def build_batches(items):
    batches = []
    current = []
    current_size = 0

    for item in items:
        item_id, text = item
        item_size = len(text)

        if current and (
            len(current) >= BATCH_SIZE
            or current_size + item_size > MAX_REQUEST_CHARS
        ):
            batches.append(current)
            current = []
            current_size = 0

        current.append(item)
        current_size += item_size

    if current:
        batches.append(current)

    return batches


def translate_markdown(text, target_language):
    blocks = parse_markdown(text)

    all_fragments = []
    fragment_locations = []
    global_id = 0

    for block_index, block in enumerate(blocks):
        if block["type"] == "code":
            fragment_locations.append(
                (
                    block_index,
                    None,
                    block["content"],
                )
            )
            continue

        fragments = extract_translatable_fragments(
            block["content"]
        )

        blocks[block_index]["fragments"] = fragments

        for fragment_index, fragment in enumerate(
            fragments
        ):
            kind, content = fragment

            if kind != "text":
                continue

            if not contains_translatable_text(content):
                continue

            all_fragments.append(
                (
                    global_id,
                    content,
                )
            )

            fragment_locations.append(
                (
                    block_index,
                    fragment_index,
                    global_id,
                )
            )

            global_id += 1

    if not all_fragments:
        return text

    translated = {}
    batches = build_batches(all_fragments)

    info(
        f"  {len(all_fragments)} text fragments, "
        f"{len(batches)} API request(s)"
    )

    for batch in batches:
        result = translate_batch(
            target_language,
            batch,
        )

        translated.update(result)

        if len(batches) > 1:
            time.sleep(0.5)

    for block_index, block in enumerate(blocks):
        if block["type"] != "text":
            continue

        fragments = block.get("fragments", [])

        for index, fragment in enumerate(fragments):
            kind, content = fragment

            if kind != "text":
                continue

            if not contains_translatable_text(content):
                continue

            global_id = None

            for (
                location_block,
                location_fragment,
                location_id,
            ) in fragment_locations:
                if (
                    location_block == block_index
                    and location_fragment == index
                ):
                    global_id = location_id
                    break

            if global_id is not None:
                fragments[index] = (
                    "text",
                    translated[global_id],
                )

        block["fragments"] = fragments

    output = []

    for block in blocks:
        if block["type"] == "code":
            output.append(block["content"])
            continue

        fragments = block.get("fragments", [])

        if not fragments:
            output.append(block["content"])
            continue

        output.append(
            merge_fragments(
                fragments,
                {
                    index: content
                    for index, (kind, content)
                    in enumerate(fragments)
                    if kind == "text"
                },
            )
        )

    return "".join(output)


def extract_protected_content(text):
    protected = []

    blocks = parse_markdown(text)

    for block in blocks:
        if block["type"] == "code":
            protected.append(
                block["content"]
            )
            continue

        fragments = extract_translatable_fragments(
            block["content"]
        )

        for kind, content in fragments:
            if kind == "protected":
                protected.append(content)

    return protected


def validate_protected_content(original, translated):
    original_protected = extract_protected_content(
        original
    )

    translated_protected = extract_protected_content(
        translated
    )

    if original_protected != translated_protected:
        return False

    return True


def cjk_ratio(text):
    if not text:
        return 0.0

    cjk = len(
        re.findall(
            r"[\u3400-\u4dbf\u4e00-\u9fff]",
            text,
        )
    )

    letters = len(
        re.findall(
            r"[A-Za-zÀ-ÖØ-öø-ÿ\u3400-\u9fff]",
            text,
        )
    )

    if letters == 0:
        return 0.0

    return cjk / letters


def natural_language_content(text):
    blocks = parse_markdown(text)

    output = []

    for block in blocks:
        if block["type"] == "code":
            continue

        fragments = extract_translatable_fragments(
            block["content"]
        )

        for kind, content in fragments:
            if kind == "text":
                output.append(content)

    return "\n".join(output)


def translation_body(text):
    if ORIGINAL_SECTION_MARKER not in text:
        return text

    return text.split(
        ORIGINAL_SECTION_MARKER,
        1,
    )[0]


def has_original_section(text):
    return ORIGINAL_SECTION_MARKER in text


def compose_translation_page(
    translated,
    original,
):
    if not translated.endswith("\n"):
        translated += "\n"

    if not original.endswith("\n"):
        original += "\n"

    return (
        f"{translated}"
        f"{ORIGINAL_SECTION_MARKER}"
        f"{original}"
    )


def validate_translation(
    original,
    translated,
    target_language,
):
    if not translated.strip():
        warning("Translation is empty.")
        return False

    translated = translation_body(translated)

    if not validate_protected_content(
        original,
        translated,
    ):
        warning(
            "Protected Markdown/code content changed."
        )
        return False

    original_blocks = parse_markdown(original)
    translated_blocks = parse_markdown(translated)

    original_code = [
        block["content"]
        for block in original_blocks
        if block["type"] == "code"
    ]

    translated_code = [
        block["content"]
        for block in translated_blocks
        if block["type"] == "code"
    ]

    if original_code != translated_code:
        warning(
            "Fenced code blocks were changed."
        )
        return False

    language_text = natural_language_content(
        translated
    )

    if target_language in ("en", "fr"):
        ratio = cjk_ratio(language_text)

        if ratio > 0.40:
            warning(
                "Translation still contains too much "
                f"Chinese ({ratio * 100:.1f}%)."
            )
            return False

    return True


def read_text(path):
    return path.read_text(
        encoding="utf-8"
    )


def write_text(path, content):
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        content,
        encoding="utf-8",
    )


def translation_path(source_path, language):
    relative = source_path.relative_to(ROOT_DIR)

    if language == "en":
        return EN_DIR / relative

    if language == "fr":
        return FR_DIR / relative

    raise ValueError(
        f"Unsupported language: {language}"
    )


def existing_translation_is_valid(
    source,
    translation_path_value,
    language,
):
    if not translation_path_value.exists():
        return False

    try:
        translated = read_text(
            translation_path_value
        )
    except OSError:
        return False

    if not has_original_section(translated):
        return False

    return validate_translation(
        source,
        translated,
        language,
    )


def upgrade_existing_translation_if_possible(
    source,
    translation_path_value,
    language,
):
    if not translation_path_value.exists():
        return False

    try:
        translated = read_text(
            translation_path_value
        )
    except OSError:
        return False

    if has_original_section(translated):
        return False

    if not validate_translation(
        source,
        translated,
        language,
    ):
        return False

    write_text(
        translation_path_value,
        compose_translation_page(
            translated,
            source,
        ),
    )

    return True


def translate_file(source_path):
    relative = source_path.relative_to(ROOT_DIR)

    info("")
    info(f"PROCESS: {relative}")

    source = read_text(source_path)

    if not source.strip():
        info("SKIP EMPTY: " + str(relative))
        return True

    success = True

    for language in ("en", "fr"):
        output_path = translation_path(
            source_path,
            language,
        )

        if existing_translation_is_valid(
            source,
            output_path,
            language,
        ):
            info(
                f"  {language.upper()} already valid"
            )
            continue

        if upgrade_existing_translation_if_possible(
            source,
            output_path,
            language,
        ):
            info(
                f"  {language.upper()} added Chinese original"
            )
            continue

        info(
            f"  Translating -> "
            f"{'English' if language == 'en' else 'French'}"
        )

        try:
            translated = translate_markdown(
                source,
                language,
            )

            if not validate_translation(
                source,
                translated,
                language,
            ):
                error(
                    f"{language.upper()} translation "
                    f"failed validation."
                )

                success = False
                continue

            page = compose_translation_page(
                translated,
                source,
            )

            if not validate_translation(
                source,
                page,
                language,
            ):
                error(
                    f"{language.upper()} generated page "
                    f"failed validation."
                )

                success = False
                continue

            write_text(
                output_path,
                page,
            )

            info(
                f"  Saved: {output_path.relative_to(ROOT_DIR)}"
            )

        except Exception as exc:
            error(
                f"{language.upper()} translation failed: "
                f"{exc}"
            )
            success = False

    return success


def verify_all_translations(markdown_files):
    info("")
    info("Verifying all translations...")

    invalid_en = []
    invalid_fr = []

    for source_path in markdown_files:
        source = read_text(source_path)

        if not source.strip():
            continue

        en_path = translation_path(
            source_path,
            "en",
        )

        fr_path = translation_path(
            source_path,
            "fr",
        )

        if not en_path.exists():
            invalid_en.append(
                str(en_path.relative_to(ROOT_DIR))
            )
        else:
            try:
                english = read_text(en_path)

                if (
                    not has_original_section(english)
                    or not validate_translation(
                        source,
                        english,
                        "en",
                    )
                ):
                    invalid_en.append(
                        str(en_path.relative_to(ROOT_DIR))
                    )

            except Exception:
                invalid_en.append(
                    str(en_path.relative_to(ROOT_DIR))
                )

        if not fr_path.exists():
            invalid_fr.append(
                str(fr_path.relative_to(ROOT_DIR))
            )
        else:
            try:
                french = read_text(fr_path)

                if (
                    not has_original_section(french)
                    or not validate_translation(
                        source,
                        french,
                        "fr",
                    )
                ):
                    invalid_fr.append(
                        str(fr_path.relative_to(ROOT_DIR))
                    )

            except Exception:
                invalid_fr.append(
                    str(fr_path.relative_to(ROOT_DIR))
                )

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
        error(
            "GEMINI_API_KEY environment variable is not set."
        )
        return 1

    try:
        markdown_files = selected_markdown_files()
    except Exception as exc:
        error(str(exc))
        return 1

    info(
        f"Found {len(markdown_files)} Markdown files."
    )

    if not markdown_files:
        warning("No Markdown files found.")
        return 0

    translation_failures = []

    for source_path in markdown_files:
        try:
            success = translate_file(
                source_path
            )

            if not success:
                translation_failures.append(
                    str(
                        source_path.relative_to(
                            ROOT_DIR
                        )
                    )
                )

        except Exception as exc:
            relative = source_path.relative_to(
                ROOT_DIR
            )

            error(
                f"Unexpected failure while processing "
                f"{relative}: {exc}"
            )

            translation_failures.append(
                str(relative)
            )

    verification_ok = verify_all_translations(
        markdown_files
    )

    if translation_failures:
        info("")
        info("Translation failures:")

        for path in translation_failures:
            info(f"  {path}")

    if not verification_ok:
        info("")
        error(
            "Translation verification failed."
        )
        info("Translation process FAILED.")
        return 1

    if translation_failures:
        info("")
        error(
            "One or more files failed translation."
        )
        info("Translation process FAILED.")
        return 1

    info("")
    info("Translation process completed successfully.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
