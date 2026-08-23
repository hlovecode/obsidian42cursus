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
TRANSLATION_ATTEMPTS = 3


def protect_markdown(text):
    protected = []

    def replace(match):
        protected.append(match.group(0))
        return (
            f"PROTECTEDTOKEN{len(protected) - 1}END"
        )

    pattern = (
        r"```[\s\S]*?```"
        r"|`[^`\n]+`"
        r"|https?://[^\s)]+"
    )

    protected_text = re.sub(
        pattern,
        replace,
        text
    )

    return protected_text, protected


def validate_protected_tokens(
    translation,
    protected
):
    for i in range(len(protected)):
        token = (
            f"PROTECTEDTOKEN{i}END"
        )

        count = translation.count(token)

        if count != 1:
            print(
                f"  Invalid protected token: "
                f"{token} "
                f"(found {count} times)"
            )
            return False

    return True


def restore_markdown(
    text,
    protected
):
    if not validate_protected_tokens(
        text,
        protected
    ):
        raise RuntimeError(
            "Protected tokens are missing "
            "or duplicated."
        )

    for i, value in enumerate(protected):
        placeholder = (
            f"PROTECTEDTOKEN{i}END"
        )

        text = text.replace(
            placeholder,
            value
        )

    return text


def validate_restored_markdown(
    original,
    translation,
    protected
):
    if not translation.strip():
        return False

    if len(original.strip()) > 0:
        if len(translation.strip()) == 0:
            return False

    for value in protected:
        if translation.count(value) != 1:
            print(
                "  Protected Markdown content "
                "was changed or lost."
            )
            print(
                f"  Protected content: {value[:80]!r}"
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


def remove_protected_tokens(
    text,
    protected_count
):
    result = text

    for i in range(protected_count):
        token = (
            f"PROTECTEDTOKEN{i}END"
        )

        result = result.replace(
            token,
            ""
        )

    return result


def validate_translation_language(
    source,
    translated_protected_text,
    protected
):
    if not translated_protected_text.strip():
        return False

    if not validate_protected_tokens(
        translated_protected_text,
        protected
    ):
        return False

    source_has_chinese = contains_chinese(
        source
    )

    if not source_has_chinese:
        return True

    explanatory_text = (
        remove_protected_tokens(
            translated_protected_text,
            len(protected)
        )
    )

    chinese_count = chinese_character_count(
        explanatory_text
    )

    total_count = non_space_character_count(
        explanatory_text
    )

    if total_count == 0:
        return True

    chinese_ratio = (
        chinese_count / total_count
    )

    if chinese_ratio > 0.15:
        print(
            "  Translation still contains "
            f"too much Chinese "
            f"({chinese_ratio:.1%})."
        )
        return False

    return True


def clean_gemini_output(text):
    text = text.strip()

    markdown_wrapper = re.match(
        r"^```(?:markdown|md)\s*\n"
        r"([\s\S]*?)"
        r"\n```\s*$",
        text,
        re.IGNORECASE
    )

    if markdown_wrapper:
        text = markdown_wrapper.group(1)

    return text.strip()


def build_translation_prompt(
    text,
    language
):
    return f"""Translate the following Markdown text into {language}.

This is a technical programming note.

IMPORTANT RULES:

1. Return ONLY the translated Markdown.
2. Do not add explanations before or after the Markdown.
3. Preserve the Markdown structure exactly.
4. Preserve headings.
5. Preserve lists.
6. Preserve tables.
7. Preserve bold and italic formatting.
8. Preserve Markdown links.
9. Preserve all numbers.
10. Preserve punctuation that belongs to Markdown structure.
11. Keep URLs unchanged.
12. Keep inline code unchanged.
13. Keep fenced code blocks unchanged.
14. Keep C source code unchanged.
15. Keep C function names unchanged.
16. Keep variable names unchanged.
17. Keep filenames unchanged.
18. Keep programming keywords unchanged.
19. Keep technical identifiers unchanged.
20. Translate all Chinese explanatory text completely.
21. Use accurate C programming terminology.
22. Do not leave Chinese explanatory sentences untranslated.
23. The strings PROTECTEDTOKEN0END, PROTECTEDTOKEN1END,
    PROTECTEDTOKEN2END, etc. are protected placeholders.
24. NEVER translate a PROTECTEDTOKEN.
25. NEVER modify a PROTECTEDTOKEN.
26. NEVER remove a PROTECTEDTOKEN.
27. NEVER add a PROTECTEDTOKEN.
28. NEVER split a PROTECTEDTOKEN.
29. Every existing PROTECTEDTOKEN must appear exactly once
    in your response.
30. Treat PROTECTEDTOKEN strings as opaque identifiers,
    not as Markdown.
31. Do not wrap the entire response in a Markdown code block.

Text to translate:

{text}
"""


def request_gemini(
    text,
    language
):
    prompt = build_translation_prompt(
        text,
        language
    )

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/"
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

            return clean_gemini_output(
                translation
            )

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


def translate_with_validation(
    original,
    protected_text,
    protected,
    language
):
    for attempt in range(
        1,
        TRANSLATION_ATTEMPTS + 1
    ):
        print(
            f"  Translation attempt "
            f"{attempt}/{TRANSLATION_ATTEMPTS}"
        )

        try:
            translation = request_gemini(
                protected_text,
                language
            )

            if not validate_translation_language(
                original,
                translation,
                protected
            ):
                print(
                    "  Translation validation failed."
                )

                if attempt < TRANSLATION_ATTEMPTS:
                    print(
                        "  Requesting a new "
                        "translation..."
                    )
                    time.sleep(
                        REQUEST_DELAY
                    )
                    continue

                raise RuntimeError(
                    f"{language} translation "
                    "failed validation."
                )

            restored = restore_markdown(
                translation,
                protected
            )

            if not validate_restored_markdown(
                original,
                restored,
                protected
            ):
                print(
                    "  Restored Markdown "
                    "validation failed."
                )

                if attempt < TRANSLATION_ATTEMPTS:
                    print(
                        "  Requesting a new "
                        "translation..."
                    )
                    time.sleep(
                        REQUEST_DELAY
                    )
                    continue

                raise RuntimeError(
                    f"{language} translation "
                    "failed Markdown validation."
                )

            return restored

        except RuntimeError as error:
            if attempt >= TRANSLATION_ATTEMPTS:
                raise

            print(
                f"  {error}"
            )
            print(
                "  Retrying translation..."
            )

            time.sleep(
                REQUEST_DELAY
            )

    raise RuntimeError(
        f"{language} translation failed."
    )


def is_valid_translation_file(
    source,
    translation_file,
    language
):
    if not os.path.exists(
        translation_file
    ):
        return False

    try:
        with open(
            translation_file,
            "r",
            encoding="utf-8"
        ) as file:
            translation = file.read()

    except OSError:
        return False

    if not translation.strip():
        return False

    if source.strip() == translation.strip():
        if contains_chinese(source):
            return False

    source_protected_text, protected = (
        protect_markdown(source)
    )

    translated_protected_text, _ = (
        protect_markdown(translation)
    )

    if not validate_protected_tokens(
        translated_protected_text,
        protected
    ):
        return False

    for value in protected:
        if translation.count(value) != 1:
            return False

    if not validate_translation_language(
        source,
        translated_protected_text,
        protected
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
        and os.path.exists(english_file)
    ):
        english_valid = (
            is_valid_translation_file(
                original,
                english_file,
                "English"
            )
        )

    if (
        old_hash == current_hash
        and os.path.exists(french_file)
    ):
        french_valid = (
            is_valid_translation_file(
                original,
                french_file,
                "French"
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
        f"\nPROCESS: {source_file}"
    )

    protected_text, protected = (
        protect_markdown(original)
    )

    success = True

    if not english_valid:
        print(
            "  Translating -> English"
        )

        try:
            english = translate_with_validation(
                original,
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
                "  ERROR: English "
                "translation failed."
            )
            print(
                f"  {error}"
            )
            success = False

        time.sleep(
            REQUEST_DELAY
        )

    else:
        print(
            "  English already valid"
        )

    if not french_valid:
        print(
            "  Translating -> French"
        )

        try:
            french = translate_with_validation(
                original,
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
                "  ERROR: French "
                "translation failed."
            )
            print(
                f"  {error}"
            )
            success = False

    if success:
        english_valid = (
            is_valid_translation_file(
                original,
                english_file,
                "English"
            )
        )

        french_valid = (
            is_valid_translation_file(
                original,
                french_file,
                "French"
            )
        )

        if (
            english_valid
            and french_valid
        ):
            hashes[relative_path] = (
                current_hash
            )
        else:
            success = False

    return success


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

        if not os.path.exists(
            english_file
        ):
            missing_english.append(
                english_file
            )

        elif not is_valid_translation_file(
            original,
            english_file,
            "English"
        ):
            invalid_english.append(
                english_file
            )

        if not os.path.exists(
            french_file
        ):
            missing_french.append(
                french_file
            )

        elif not is_valid_translation_file(
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

    verification_passed = (
        verify_all_translations(
            files
        )
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

        save_hashes(hashes)

        raise SystemExit(1)

    save_hashes(hashes)

    print(
        "\nTranslation process completed "
        "successfully."
    )


if __name__ == "__main__":
    main()
