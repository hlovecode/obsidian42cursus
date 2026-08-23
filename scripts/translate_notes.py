import hashlib
import json
import os
import random
import re
import time
import urllib.error
import urllib.request


API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-3.5-flash-lite"

TRANSLATION_DIR = "translations"
HASH_FILE = os.path.join(
    TRANSLATION_DIR,
    ".translation_hashes.json"
)

MAX_RETRIES = 5
BASE_DELAY = 2
REQUEST_DELAY = 2


def protect_markdown(text):
    protected = []

    def replace(match):
        protected.append(match.group(0))
        return f"PROTECTEDTOKEN{len(protected) - 1}END"

    pattern = (
        r"```[\s\S]*?```"
        r"|`[^`\n]+`"
        r"|https?://[^\s)]+"
    )

    text = re.sub(
        pattern,
        replace,
        text
    )

    return text, protected


def restore_markdown(text, protected):
    for i, value in enumerate(protected):
        placeholder = (
            f"PROTECTEDTOKEN{i}END"
        )

        if placeholder not in text:
            raise RuntimeError(
                f"Protected token missing: "
                f"{placeholder}"
            )

        text = text.replace(
            placeholder,
            value
        )

    return text


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


def contains_chinese(text):
    return bool(
        re.search(
            r"[\u4e00-\u9fff]",
            text
        )
    )


def chinese_character_count(text):
    return len(
        re.findall(
            r"[\u4e00-\u9fff]",
            text
        )
    )


def non_space_character_count(text):
    return len(
        re.findall(
            r"\S",
            text
        )
    )


def translation_is_valid(
    source,
    translation,
    language
):
    if not translation:
        return False

    if not translation.strip():
        return False

    if source.strip() == translation.strip():
        return False

    source_has_chinese = contains_chinese(
        source
    )

    if not source_has_chinese:
        return True

    chinese_count = chinese_character_count(
        translation
    )

    total_count = non_space_character_count(
        translation
    )

    if total_count == 0:
        return False

    chinese_ratio = (
        chinese_count / total_count
    )

    if language == "English":
        if chinese_ratio > 0.15:
            return False

    if language == "French":
        if chinese_ratio > 0.15:
            return False

    return True


def is_valid_translation(path):
    if not os.path.exists(path):
        return False

    try:
        if os.path.getsize(path) == 0:
            return False

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:
            content = file.read()

        return bool(content.strip())

    except OSError:
        return False


def validate_translation_file(
    source,
    translation,
    language
):
    if not translation_is_valid(
        source,
        translation,
        language
    ):
        return False

    if "PROTECTEDTOKEN" in translation:
        return False

    return True


def translate(
    text,
    language
):
    prompt = f"""Translate the following Markdown text into {language}.

Important rules:

- Return only the translated Markdown.
- Do not add explanations.
- Preserve the Markdown structure exactly.
- Preserve headings.
- Preserve lists.
- Preserve tables.
- Preserve emphasis.
- Preserve links.
- Preserve Markdown formatting.
- Preserve all numbers exactly.
- Preserve all punctuation that is part of Markdown structure.
- Do not translate URLs.
- Do not translate inline code.
- Do not translate fenced code blocks.
- Do not translate C source code.
- Do not translate C function names.
- Do not translate variable names.
- Do not translate programming keywords.
- Do not translate filenames.
- Do not translate technical identifiers.
- Keep all PROTECTEDTOKEN placeholders EXACTLY unchanged.
- Do not add, remove, rename, split or modify any PROTECTEDTOKEN.
- Every PROTECTEDTOKEN must appear exactly as provided.
- Do not interpret PROTECTEDTOKEN as Markdown.
- This is a technical programming note.
- Use accurate C programming terminology.
- Translate Chinese explanatory text completely.
- Do not leave Chinese explanatory sentences untranslated.

Text:

{text}
"""

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{MODEL}:generateContent?key={API_KEY}"
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

    for attempt in range(MAX_RETRIES):
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
                print(
                    "  Gemini API error:"
                )
                print(
                    json.dumps(
                        result["error"],
                        ensure_ascii=False,
                        indent=2
                    )
                )

                raise RuntimeError(
                    "Gemini API returned an error."
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

            translation = translation.strip()

            if not translation:
                raise RuntimeError(
                    "Gemini returned an empty translation."
                )

            return translation

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

            if attempt == MAX_RETRIES - 1:
                raise

            delay = (
                BASE_DELAY * (2 ** attempt)
                + random.uniform(0, 1)
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
            if attempt == MAX_RETRIES - 1:
                raise

            delay = (
                BASE_DELAY * (2 ** attempt)
                + random.uniform(0, 1)
            )

            print(
                f"  API response error: {error}"
            )
            print(
                f"  Retrying in {delay:.1f}s..."
            )

            time.sleep(delay)


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

        source_set.add(
            relative_path
        )

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

        if os.path.exists(
            english_file
        ):
            os.remove(
                english_file
            )

            print(
                f"DELETE: {english_file}"
            )

        if os.path.exists(
            french_file
        ):
            os.remove(
                french_file
            )

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

    if not has_real_content(
        original
    ):
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

    english_valid = False
    french_valid = False

    if (
        old_hash == current_hash
        and is_valid_translation(
            english_file
        )
    ):
        with open(
            english_file,
            "r",
            encoding="utf-8"
        ) as file:
            english_content = file.read()

        english_valid = translation_is_valid(
            original,
            english_content,
            "English"
        )

    if (
        old_hash == current_hash
        and is_valid_translation(
            french_file
        )
    ):
        with open(
            french_file,
            "r",
            encoding="utf-8"
        ) as file:
            french_content = file.read()

        french_valid = translation_is_valid(
            original,
            french_content,
            "French"
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
        f"\nPROCESS: {source_file}"
    )

    protected_text, protected = (
        protect_markdown(original)
    )

    success = True

    if not english_valid:
        try:
            print(
                "  Translating -> English"
            )

            english = translate(
                protected_text,
                "English"
            )

            if not validate_translation_file(
                original,
                english,
                "English"
            ):
                raise RuntimeError(
                    "English translation "
                    "failed validation."
                )

            english = restore_markdown(
                english,
                protected
            )

            if not translation_is_valid(
                original,
                english,
                "English"
            ):
                raise RuntimeError(
                    "English translation "
                    "failed final validation."
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

            time.sleep(
                REQUEST_DELAY
            )

        except Exception as error:
            print(
                "  ERROR: English "
                "translation failed."
            )
            print(
                f"  {error}"
            )
            success = False

    else:
        print(
            "  English already valid"
        )

    if not french_valid:
        try:
            print(
                "  Translating -> French"
            )

            french = translate(
                protected_text,
                "French"
            )

            if not validate_translation_file(
                original,
                french,
                "French"
            ):
                raise RuntimeError(
                    "French translation "
                    "failed validation."
                )

            french = restore_markdown(
                french,
                protected
            )

            if not translation_is_valid(
                original,
                french,
                "French"
            ):
                raise RuntimeError(
                    "French translation "
                    "failed final validation."
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
                "  ERROR: French "
                "translation failed."
            )
            print(
                f"  {error}"
            )
            success = False

    english_final = (
        is_valid_translation(
            english_file
        )
        and translation_file_matches_language(
            original,
            english_file,
            "English"
        )
    )

    french_final = (
        is_valid_translation(
            french_file
        )
        and translation_file_matches_language(
            original,
            french_file,
            "French"
        )
    )

    if (
        english_final
        and french_final
    ):
        hashes[relative_path] = current_hash
    else:
        success = False

    return success


def translation_file_matches_language(
    source,
    path,
    language
):
    try:
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:
            content = file.read()

    except OSError:
        return False

    return translation_is_valid(
        source,
        content,
        language
    )


def verify_all_translations(
    source_files
):
    missing_english = []
    missing_french = []

    invalid_english = []
    invalid_french = []

    for source_file in source_files:
        with open(
            source_file,
            "r",
            encoding="utf-8"
        ) as file:
            original = file.read()

        if not has_real_content(
            original
        ):
            continue

        english_file = get_translation_path(
            source_file,
            "English"
        )

        french_file = get_translation_path(
            source_file,
            "French"
        )

        if not is_valid_translation(
            english_file
        ):
            missing_english.append(
                english_file
            )
        elif not translation_file_matches_language(
            original,
            english_file,
            "English"
        ):
            invalid_english.append(
                english_file
            )

        if not is_valid_translation(
            french_file
        ):
            missing_french.append(
                french_file
            )
        elif not translation_file_matches_language(
            original,
            french_file,
            "French"
        ):
            invalid_french.append(
                french_file
            )

    if (
        not missing_english
        and not missing_french
        and not invalid_english
        and not invalid_french
    ):
        print(
            "\nPASS: All English and French "
            "translations are valid."
        )
        return True

    print(
        "\nERROR: Translation verification failed."
    )

    if missing_english:
        print(
            "\nMissing English translations:"
        )

        for path in missing_english:
            print(
                f"  {path}"
            )

    if invalid_english:
        print(
            "\nInvalid English translations:"
        )

        for path in invalid_english:
            print(
                f"  {path}"
            )

    if missing_french:
        print(
            "\nMissing French translations:"
        )

        for path in missing_french:
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

    return False


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

    failed_files = []

    for source_file in files:
        try:
            success = translate_file(
                source_file,
                hashes
            )

            if not success:
                failed_files.append(
                    source_file
                )

        except Exception as error:
            print(
                f"\nERROR: {source_file}"
            )
            print(
                f"  {error}"
            )

            failed_files.append(
                source_file
            )

    save_hashes(hashes)

    verification_passed = (
        verify_all_translations(files)
    )

    if failed_files:
        print(
            "\nTranslation failures:"
        )

        for source_file in failed_files:
            print(
                f"  {source_file}"
            )

    if (
        failed_files
        or not verification_passed
    ):
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
