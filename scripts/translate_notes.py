#!/usr/bin/env python3

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
    "gemini-2.5-flash",
)

API_URL = (
    "https://generativelanguage.googleapis.com/"
    f"v1beta/models/{MODEL}:generateContent"
)

MAX_RETRIES = 3

# Number of natural-language fragments sent in one request.
BATCH_SIZE = 20

# Gemini API can temporarily return 429.
INITIAL_RETRY_DELAY = 5.0

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

def find_markdown_files():
    files = []

    for path in ROOT_DIR.rglob("*.md"):
        relative = path.relative_to(ROOT_DIR)

        if not relative.parts:
            continue

        # Only source notes should be translated. Generated docs,
        # translations, workflows, scripts, and hidden directories
        # must not become translation sources.
        if any(
            part in SOURCE_EXCLUDED_DIRS
            for part in relative.parts
        ):
            continue

        # Never process .git or other hidden directories.
        if any(part.startswith(".") for part in relative.parts):
            continue

        if len(relative.parts) == 1:
            continue

        files.append(path)

    files.sort()

    return files


# ============================================================
# Markdown protection
# ============================================================
#
# IMPORTANT:
#
# The previous implementation protected Markdown by replacing
# pieces such as:
#
#     `src`
#     `dst`
#     ```c ... ```
#
# with artificial tokens and then asking Gemini to return them.
#
# That is exactly what caused errors such as:
#
#     Original: `src`
#     Translated: `n`
#
# and:
#
#     Protected token order changed.
#
# This implementation does NOT do that.
#
# Protected content is never sent to Gemini at all.
#
# We split each line into:
#
#     translatable text
#     protected Markdown/code
#     translatable text
#
# and translate only the natural-language fragments.
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
    """
    Return a list of fragments.

    Each fragment is:

        ("text", content)
        ("protected", content)

    Protected content is never sent to Gemini.
    """

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


# ============================================================
# Markdown line handling
# ============================================================

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
    """
    Separate Markdown syntax from natural language.

    Markdown syntax itself is never translated.
    """

    newline = ""

    if line.endswith("\n"):
        newline = "\n"
        content = line[:-1]
    else:
        content = line

    if not content.strip():
        return [
            ("protected", content + newline)
        ]

    # Markdown table separator must remain untouched.
    if TABLE_SEPARATOR_RE.match(content):
        return [
            ("protected", content + newline)
        ]

    # Fenced code is handled by the whole-document parser.
    if FENCE_RE.match(content):
        return [
            ("protected", content + newline)
        ]

    match = HEADING_RE.match(content)

    if match:
        prefix = match.group(1)
        body = match.group(2)

        result = [
            ("protected", prefix)
        ]

        result.extend(
            protect_inline_markdown(body)
        )

        if newline:
            result.append(("protected", newline))

        return result

    match = BLOCKQUOTE_RE.match(content)

    if match:
        prefix = match.group(1)
        body = match.group(2)

        result = [
            ("protected", prefix)
        ]

        result.extend(
            protect_inline_markdown(body)
        )

        if newline:
            result.append(("protected", newline))

        return result

    match = LIST_RE.match(content)

    if match:
        prefix = match.group(1)
        body = match.group(2)

        result = [
            ("protected", prefix)
        ]

        result.extend(
            protect_inline_markdown(body)
        )

        if newline:
            result.append(("protected", newline))

        return result

    result = protect_inline_markdown(content)

    if newline:
        result.append(("protected", newline))

    return result


def parse_markdown(text):
    """
    Parse Markdown while keeping fenced code blocks completely
    untouched.

    Returns a list of blocks.

    Each block is:

        {
            "type": "code" or "text",
            "content": ...
        }
    """

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


# ============================================================
# Translatable fragment extraction
# ============================================================

def extract_translatable_fragments(text):
    """
    Convert Markdown text into fragments.

    Returns:

        [
            ("protected", "..."),
            ("text", "..."),
            ("protected", "..."),
            ...
        ]

    No placeholder tokens are generated.
    """

    fragments = []

    lines = text.splitlines(keepends=True)

    for line in lines:
        fragments.extend(
            split_markdown_line(line)
        )

    return fragments


def merge_fragments(fragments, translations):
    """
    Reconstruct Markdown from translated fragments.

    `translations` maps the index of a text fragment to its
    translated value.
    """

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


# ============================================================
# Language / translation helpers
# ============================================================

def contains_translatable_text(text):
    """
    Return True if the fragment contains enough natural language
    to justify an API request.
    """

    if not text.strip():
        return False

    # Ignore fragments consisting almost entirely of punctuation.
    letters = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ\u4e00-\u9fff]", text)

    return len(letters) >= 2


def clean_model_output(text):
    """
    Remove accidental Markdown code fences around a response.

    The model is instructed not to produce them, but this makes
    the script more robust.
    """

    text = text.strip()

    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()

        if len(lines) >= 2:
            lines = lines[1:-1]
            text = "\n".join(lines)

    return text


# ============================================================
# Gemini API
# ============================================================

def build_translation_prompt(target_language, items):
    """
    Build a structured JSON translation request.

    Each item has an ID that exists only inside the API request.
    It is NOT inserted into the Markdown.

    Therefore token order is irrelevant.
    """

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


def api_request(prompt):
    """
    Send one request to Gemini using the official REST
    generateContent endpoint.
    """

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
        API_URL,
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
    """
    Translate one batch.

    Retry only API failures or malformed responses.

    There is deliberately NO Protected Token validation here.
    """

    prompt = build_translation_prompt(
        target_language,
        items,
    )

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            info(
                f"  Translation request "
                f"{attempt}/{MAX_RETRIES} "
                f"({len(items)} fragments)"
            )

            raw = api_request(prompt)

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

                # Small random jitter avoids synchronized retries.
                delay += random.uniform(0.0, 1.5)

                warning(
                    f"HTTP 429. "
                    f"Retrying in {delay:.1f}s..."
                )

                time.sleep(delay)
                continue

            try:
                response_body = exc.read().decode(
                    "utf-8",
                    errors="replace",
                )
            except Exception:
                response_body = ""

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


# ============================================================
# Translation engine
# ============================================================

def build_batches(items):
    """
    Group fragments into reasonably sized API requests.
    """

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
    """
    Translate natural-language fragments while preserving all
    Markdown/code content exactly.
    """

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

        # Small pause between successful requests.
        # This helps reduce accidental rate-limit bursts.
        if len(batches) > 1:
            time.sleep(0.5)

    # Replace translated fragments.
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

            # Find global ID.
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


# ============================================================
# Translation validity
# ============================================================

def extract_protected_content(text):
    """
    Extract content that must remain byte-for-byte identical.

    This is ONLY used for final verification.

    Unlike the previous implementation, we do not ask Gemini
    to preserve these values. They never enter the translation
    request.
    """

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
    """
    Verify that protected Markdown/code content has not changed.

    We intentionally compare exact content in sequence here because
    Python itself preserved it. This is NOT a Gemini token-order
    validation mechanism.
    """

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
    """
    Calculate the ratio of Chinese/Japanese/Korean characters
    in natural-language text.

    Used only as a sanity check for French/English output.
    """

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
    """
    Remove code and protected Markdown before language checks.
    """

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
    """
    Return only the translated part of a generated translation page.

    The Chinese source is appended for readers, but it must not
    participate in translation validation.
    """

    if ORIGINAL_SECTION_MARKER not in text:
        return text

    return text.split(
        ORIGINAL_SECTION_MARKER,
        1,
    )[0].rstrip() + "\n"


def has_original_section(text):
    return ORIGINAL_SECTION_MARKER in text


def compose_translation_page(
    translated,
    original,
):
    translated = translated.strip()
    original = original.strip()

    return (
        f"{translated}"
        f"{ORIGINAL_SECTION_MARKER}"
        f"{original}\n"
    )


def validate_translation(
    original,
    translated,
    target_language,
):
    """
    Validate the resulting Markdown.

    We check:
      - output is not empty
      - protected content is unchanged
      - fenced code is unchanged
      - basic language sanity

    We do NOT check token order generated by Gemini.
    """

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

        # A tiny amount of Chinese can legitimately remain in
        # technical documentation, names, or quoted material.
        #
        # We use a deliberately conservative threshold so that
        # this check does not reject otherwise correct translations.
        if ratio > 0.40:
            warning(
                "Translation still contains too much "
                f"Chinese ({ratio * 100:.1f}%)."
            )
            return False

    return True


# ============================================================
# Existing translation handling
# ============================================================

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


# ============================================================
# Single file processing
# ============================================================

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


# ============================================================
# Final verification
# ============================================================

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


# ============================================================
# Main
# ============================================================

def main():
    if not API_KEY:
        error(
            "GEMINI_API_KEY environment variable is not set."
        )
        return 1

    markdown_files = find_markdown_files()

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
