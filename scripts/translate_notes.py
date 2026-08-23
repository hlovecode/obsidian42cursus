import os
import re
import json
import time
import random
import hashlib
import urllib.request
import urllib.error


API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-3.5-flash-lite"

TRANSLATION_DIR = "translations"
HASH_FILE = os.path.join(
    TRANSLATION_DIR,
    ".translation_hashes.json"
)

MAX_TRANSLATION_ATTEMPTS = 3
MAX_HTTP_RETRIES = 5

BASE_RETRY_DELAY = 5
REQUEST_DELAY = 5

CHINESE_RATIO_LIMIT = 0.15


def protect_markdown(text):
    protected = []

    def replace(match):
        index = len(protected)
        value = match.group(0)
        protected.append(value)
        return f"PROTECTEDTOKEN{index}END"

    pattern = (
        r"```[\s\S]*?```"
        r"|`[^`\n]+`"
        r"|https?://[^\s<>\])]+"
    )

    protected_text = re.sub(
        pattern,
        replace,
        text
    )

    return protected_text, protected


def extract_protected_tokens(text):
    pattern = r"PROTECTEDTOKEN(\d+)END"

    tokens = re.findall(
        pattern,
        text
    )

    return [
        int(index)
        for index in tokens
    ]


def validate_protected_tokens(
    translated,
    protected
):
    expected_indexes = list(
        range(len(protected))
    )

    actual_indexes = extract_protected_tokens(
        translated
    )

    if actual_indexes != expected_indexes:
        if len(actual_indexes) != len(
            expected_indexes
        ):
            print(
                "  Protected token count mismatch."
            )
            print(
                f"  Expected: {len(expected_indexes)}"
            )
            print(
                f"  Found: {len(actual_indexes)}"
            )
        else:
            print(
                "  Protected token order changed."
            )
            print(
                f"  Expected: {expected_indexes}"
            )
            print(
                f"  Found: {actual_indexes}"
            )

        return False

    for index in expected_indexes:
        token = f"PROTECTEDTOKEN{index}END"

        if translated.count(token) != 1:
            print(
                f"  Invalid protected token: {token}"
            )
            print(
                f"  Found {translated.count(token)} times"
            )
            return False

    return True


def restore_markdown(
    text,
    protected
):
    for index, value in enumerate(protected):
        placeholder = (
            f"PROTECTEDTOKEN{index}END"
        )

        text = text.replace(
            placeholder,
            value
        )

    return text


def extract_markdown_protected(text):
    protected = []

    def replace(match):
        protected.append(match.group(0))
        return ""

    pattern = (
        r"```[\s\S]*?```"
        r"|`[^`\n]+`"
        r"|https?://[^\s<>\])]+"
    )

    re.sub(
        pattern,
        replace,
        text
    )

    return protected


def validate_restored_markdown(
    original,
    translated
):
    original_protected = (
        extract_markdown_protected(original)
    )

    translated_protected = (
        extract_markdown_protected(translated)
    )

    if original_protected != translated_protected:
        print(
            "  Protected Markdown content was "
            "changed or lost."
        )

        max_items = max(
            len(original_protected),
            len(translated_protected)
        )

        for index in range(max_items):
            original_value = (
                original_protected[index]
                if index < len(original_protected)
                else "<MISSING>"
            )

            translated_value = (
                translated_protected[index]
                if index < len(translated_protected)
                else "<MISSING>"
            )

            if original_value != translated_value:
                print(
                    f"  Protected content mismatch "
                    f"at index {index}:"
                )
                print(
                    f"    Original: {original_value!r}"
                )
                print(
                    f"    Translated: "
                    f"{translated_value!r}"
                )

                break

        return False

    return True


def calculate_chinese_ratio(text):
    chinese_characters = re.findall(
        r"[\u4e00-\u9fff]",
        text
    )

    meaningful_characters = re.findall(
        r"[A-Za-z\u4e00-\u9fff]",
        text
    )

    if not meaningful_characters:
        return 0.0

    return (
        len(chinese_characters)
        / len(meaningful_characters)
    )


def validate_language(
    text,
    language
):
    ratio = calculate_chinese_ratio(text)

    if ratio > CHINESE_RATIO_LIMIT:
        print(
            f"  Translation still contains too "
            f"much Chinese ({ratio * 100:.1f}%)."
        )
        return False

    return True


def find_markdown_files():
    files = []

    excluded_dirs = {
        ".git",
        ".github",
        ".obsidian",
        "translations",
        "scripts",
        "docs",
        "site",
        ".venv-pages",
        ".venv",
        "__pycache__"
    }

    for root, dirs, filenames in os.walk("."):
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in excluded_dirs
        ]

        for filename in filenames:
            if not filename.endswith(".md"):
                continue

            source_file = os.path.join(
                root,
                filename
            )

            source_file = os.path.normpath(
                source_file
            )

            if source_file.startswith(
                f"{TRANSLATION_DIR}{os.sep}"
            ):
                continue

            files.append(source_file)

    return sorted(files)


def get_translation_path(
    source_file,
    language
):
    relative_path = os.path.relpath(
        source_file,
        "."
    )

    if language == "English":
        language_dir = "en"
    else:
        language_dir = "fr"

    return os.path.join(
        TRANSLATION_DIR,
        language_dir,
        relative_path
    )


def calculate_hash(text):
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}

    try:
        with open(
            HASH_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

    except (
        json.JSONDecodeError,
        OSError
    ):
        print(
            "WARNING: Could not read hash file."
        )

    return {}


def save_hashes(hashes):
    os.makedirs(
        TRANSLATION_DIR,
        exist_ok=True
    )

    temporary_file = HASH_FILE + ".tmp"

    with open(
        temporary_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            hashes,
            file,
            ensure_ascii=False,
            indent=2
        )
        file.write("\n")

    os.replace(
        temporary_file,
        HASH_FILE
    )


def has_real_content(text):
    lines = text.splitlines()

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#"):
            continue

        return True

    return False


def build_prompt(
    protected_text,
    language
):
    return f"""Translate the following Markdown text into {language}.

This is a technical programming note about the C programming language.

STRICT RULES:

1. Return ONLY the translated Markdown.
2. Do not add explanations before or after the translation.
3. Preserve the Markdown structure exactly.
4. Preserve headings.
5. Preserve lists.
6. Preserve tables.
7. Preserve emphasis.
8. Preserve Markdown links.
9. Preserve URLs.
10. Preserve inline code.
11. Preserve fenced code blocks.
12. Preserve C source code exactly.
13. Do not translate code.
14. Do not translate URLs.
15. Do not translate protected tokens.
16. Every PROTECTEDTOKEN<number>END token must appear exactly once.
17. Do not create new PROTECTEDTOKEN tokens.
18. Do not remove any PROTECTEDTOKEN tokens.
19. Do not change the number of PROTECTEDTOKEN tokens.
20. Preserve the order of all PROTECTEDTOKEN tokens.
21. Preserve the original meaning accurately.
22. Use correct technical terminology.
23. Translate all natural-language Chinese text.
24. Do not leave large portions of Chinese untranslated.

Protected tokens look like:

PROTECTEDTOKEN0END
PROTECTEDTOKEN1END
PROTECTEDTOKEN2END

They are placeholders and MUST remain exactly unchanged.

Text to translate:

{protected_text}
"""


def request_gemini(prompt):
    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/"
        f"{MODEL}:generateContent"
        f"?key={API_KEY}"
    )

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    request_data = json.dumps(
        data
    ).encode("utf-8")

    for attempt in range(MAX_HTTP_RETRIES):
        try:
            request = urllib.request.Request(
                url,
                data=request_data,
                headers={
                    "Content-Type": "application/json"
                },
                method="POST"
            )

            with urllib.request.urlopen(
                request,
                timeout=120
            ) as response:
                response_text = (
                    response
                    .read()
                    .decode("utf-8")
                )

            result = json.loads(
                response_text
            )

            if "error" in result:
                error = result["error"]

                code = error.get(
                    "code"
                )

                if code in (
                    408,
                    429,
                    500,
                    502,
                    503,
                    504
                ):
                    raise urllib.error.HTTPError(
                        url,
                        code,
                        error.get(
                            "message",
                            "Gemini API error"
                        ),
                        None,
                        None
                    )

                raise RuntimeError(
                    "Gemini API returned an error: "
                    + json.dumps(
                        error,
                        ensure_ascii=False
                    )
                )

            candidates = result.get(
                "candidates",
                []
            )

            if not candidates:
                raise RuntimeError(
                    "Gemini returned no candidates."
                )

            content = candidates[0].get(
                "content",
                {}
            )

            parts = content.get(
                "parts",
                []
            )

            if not parts:
                raise RuntimeError(
                    "Gemini response contains no parts."
                )

            translation = parts[0].get(
                "text"
            )

            if not translation:
                raise RuntimeError(
                    "Gemini response contains no text."
                )

            return translation.strip()

        except urllib.error.HTTPError as error:
            if error.code not in (
                408,
                429,
                500,
                502,
                503,
                504
            ):
                raise

            if attempt == MAX_HTTP_RETRIES - 1:
                raise

            delay = (
                BASE_RETRY_DELAY
                * (2 ** attempt)
                + random.uniform(0, 2)
            )

            print(
                f"  HTTP {error.code}. "
                f"Retrying in {delay:.1f}s..."
            )

            time.sleep(delay)

        except (
            urllib.error.URLError,
            RuntimeError
        ) as error:
            if attempt == MAX_HTTP_RETRIES - 1:
                raise

            delay = (
                BASE_RETRY_DELAY
                * (2 ** attempt)
                + random.uniform(0, 2)
            )

            print(
                f"  API response error: {error}"
            )

            print(
                f"  Retrying in {delay:.1f}s..."
            )

            time.sleep(delay)


def translate(
    protected_text,
    protected,
    language
):
    prompt = build_prompt(
        protected_text,
        language
    )

    for attempt in range(
        MAX_TRANSLATION_ATTEMPTS
    ):
        print(
            f"  Translation attempt "
            f"{attempt + 1}/"
            f"{MAX_TRANSLATION_ATTEMPTS}"
        )

        try:
            translation = request_gemini(
                prompt
            )

            if not validate_protected_tokens(
                translation,
                protected
            ):
                print(
                    "  Translation validation failed."
                )
                print(
                    "  Requesting a new translation..."
                )
                continue

            restored = restore_markdown(
                translation,
                protected
            )

            if not validate_restored_markdown(
                protected_text,
                translation
            ):
                print(
                    "  Restored Markdown validation "
                    "failed."
                )
                print(
                    "  Requesting a new translation..."
                )
                continue

            if not validate_language(
                restored,
                language
            ):
                print(
                    "  Translation validation failed."
                )
                print(
                    "  Requesting a new translation..."
                )
                continue

            return restored

        except Exception as error:
            print(
                f"  Translation error: {error}"
            )

            if attempt == (
                MAX_TRANSLATION_ATTEMPTS - 1
            ):
                raise

            print(
                "  Requesting a new translation..."
            )

    raise RuntimeError(
        f"{language} translation failed "
        "validation."
    )


def validate_existing_translation(
    original,
    translated
):
    if not os.path.exists(translated):
        return False

    try:
        with open(
            translated,
            "r",
            encoding="utf-8"
        ) as file:
            translated_text = file.read()

    except OSError:
        return False

    if not validate_restored_markdown(
        original,
        translated_text
    ):
        return False

    if not validate_language(
        translated_text,
        "English"
    ):
        return False

    return True


def cleanup_deleted_files(
    source_files,
    hashes
):
    source_set = set()

    for source_file in source_files:
        relative_path = os.path.relpath(
            source_file,
            "."
        )

        source_set.add(relative_path)

    deleted_paths = []

    for relative_path in list(hashes):
        if relative_path not in source_set:
            deleted_paths.append(
                relative_path
            )

    for relative_path in deleted_paths:
        english_file = os.path.join(
            TRANSLATION_DIR,
            "en",
            relative_path
        )

        french_file = os.path.join(
            TRANSLATION_DIR,
            "fr",
            relative_path
        )

        if os.path.exists(english_file):
            os.remove(english_file)

            print(
                f"DELETE: {english_file}"
            )

        if os.path.exists(french_file):
            os.remove(french_file)

            print(
                f"DELETE: {french_file}"
            )

        del hashes[relative_path]


def translate_file(
    source_file,
    hashes
):
    english_file = get_translation_path(
        source_file,
        "English"
    )

    french_file = get_translation_path(
        source_file,
        "French"
    )

    with open(
        source_file,
        "r",
        encoding="utf-8"
    ) as file:
        original = file.read()

    if not has_real_content(original):
        print(
            f"SKIP EMPTY: {source_file}"
        )
        return True

    relative_path = os.path.relpath(
        source_file,
        "."
    )

    current_hash = calculate_hash(
        original
    )

    old_hash = hashes.get(
        relative_path
    )

    english_exists = os.path.exists(
        english_file
    )

    french_exists = os.path.exists(
        french_file
    )

    english_valid = False
    french_valid = False

    if english_exists:
        english_valid = (
            validate_existing_translation(
                original,
                english_file
            )
        )

    if french_exists:
        french_valid = (
            validate_existing_translation(
                original,
                french_file
            )
        )

    if (
        old_hash == current_hash
        and english_valid
        and french_valid
    ):
        print(
            f"SKIP: {source_file}"
        )
        return True

    print(
        f"PROCESS: {source_file}"
    )

    protected_text, protected = (
        protect_markdown(original)
    )

    success = True

    if english_valid:
        print(
            "  English already valid"
        )

    else:
        print(
            "  Translating -> English"
        )

        try:
            english = translate(
                protected_text,
                protected,
                "English"
            )

            os.makedirs(
                os.path.dirname(
                    english_file
                ),
                exist_ok=True
            )

            with open(
                english_file,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(english)

            print(
                f"  Saved: {english_file}"
            )

        except Exception as error:
            print(
                f"  ERROR: English translation "
                f"failed."
            )
            print(
                f"  {error}"
            )
            success = False

        time.sleep(
            REQUEST_DELAY
        )

    if french_valid:
        print(
            "  French already valid"
        )

    else:
        print(
            "  Translating -> French"
        )

        try:
            french = translate(
                protected_text,
                protected,
                "French"
            )

            os.makedirs(
                os.path.dirname(
                    french_file
                ),
                exist_ok=True
            )

            with open(
                french_file,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(french)

            print(
                f"  Saved: {french_file}"
            )

        except Exception as error:
            print(
                f"  ERROR: French translation "
                f"failed."
            )
            print(
                f"  {error}"
            )
            success = False

    if success:
        hashes[relative_path] = current_hash

    return success


def verify_all_translations(
    source_files
):
    invalid_english = []
    invalid_french = []

    for source_file in source_files:
        with open(
            source_file,
            "r",
            encoding="utf-8"
        ) as file:
            original = file.read()

        if not has_real_content(original):
            continue

        english_file = get_translation_path(
            source_file,
            "English"
        )

        french_file = get_translation_path(
            source_file,
            "French"
        )

        if not validate_existing_translation(
            original,
            english_file
        ):
            invalid_english.append(
                english_file
            )

        if not validate_existing_translation(
            original,
            french_file
        ):
            invalid_french.append(
                french_file
            )

    if invalid_english:
        print(
            "\nInvalid English translations:"
        )

        for path in invalid_english:
            print(
                f"  {path}"
            )

    if invalid_french:
        print(
            "\nInvalid French translations:"
        )

        for path in invalid_french:
            print(
                f"  {path}"
            )

    return (
        not invalid_english
        and not invalid_french
    )


def main():
    hashes = load_hashes()

    files = find_markdown_files()

    print(
        f"Found {len(files)} Markdown files."
    )

    cleanup_deleted_files(
        files,
        hashes
    )

    failures = []

    for source_file in files:
        try:
            success = translate_file(
                source_file,
                hashes
            )

            if not success:
                failures.append(
                    source_file
                )

        except Exception as error:
            print(
                f"\nERROR: {source_file}"
            )

            print(
                f"  {error}"
            )

            failures.append(
                source_file
            )

    save_hashes(hashes)

    print(
        "\nVerifying all translations..."
    )

    translations_valid = (
        verify_all_translations(files)
    )

    if failures:
        print(
            "\nTranslation failures:"
        )

        for source_file in failures:
            print(
                f"  {source_file}"
            )

    if not translations_valid:
        print(
            "\nERROR: Translation verification "
            "failed."
        )

        print(
            "\nTranslation process FAILED."
        )

        raise SystemExit(1)

    if failures:
        print(
            "\nTranslation process FAILED."
        )

        raise SystemExit(1)

    print(
        "\nTranslation process completed "
        "successfully."
    )


if __name__ == "__main__":
    main()
