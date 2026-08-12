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

MAX_RETRIES = 5
BASE_DELAY = 2
REQUEST_DELAY = 2


def protect_markdown(text):
    protected = []

    def replace(match):
        protected.append(match.group(0))
        return f"___PROTECTED_{len(protected) - 1}___"

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
        placeholder = f"___PROTECTED_{i}___"
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
        "translations",
        "scripts",
        ".obsidian"
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

            files.append(source_file)

    return sorted(files)


def get_translation_path(source_file, language):
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


def translate(text, language):
    prompt = f"""Translate the following Markdown text into {language}.

Important rules:

- Return only the translated Markdown.
- Preserve all Markdown structure exactly.
- Do not add explanations.
- Do not translate placeholders such as ___PROTECTED_0___.
- Keep all placeholders unchanged.
- Keep URLs unchanged.
- Keep inline code unchanged.
- Keep fenced code blocks unchanged.
- Keep C source code unchanged.
- Keep Markdown links unchanged.
- Keep headings, lists, tables and emphasis.
- Preserve the original meaning accurately.
- This is a technical programming note.
- Use accurate C programming terminology.

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
        return

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

    if (
        old_hash == current_hash
        and english_exists
        and french_exists
    ):
        print(
            f"SKIP: {source_file}"
        )
        return

    print(
        f"\nPROCESS: {source_file}"
    )

    protected_text, protected = (
        protect_markdown(original)
    )

    if (
        old_hash != current_hash
        or not english_exists
    ):
        print(
            "  Translating -> English"
        )

        english = translate(
            protected_text,
            "English"
        )

        english = restore_markdown(
            english,
            protected
        )

        os.makedirs(
            os.path.dirname(english_file),
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

        time.sleep(REQUEST_DELAY)

    else:
        print(
            "  English already exists"
        )

    if (
        old_hash != current_hash
        or not french_exists
    ):
        print(
            "  Translating -> French"
        )

        french = translate(
            protected_text,
            "French"
        )

        french = restore_markdown(
            french,
            protected
        )

        os.makedirs(
            os.path.dirname(french_file),
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

    else:
        print(
            "  French already exists"
        )

    hashes[relative_path] = current_hash


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

    for source_file in files:
        try:
            translate_file(
                source_file,
                hashes
            )

        except Exception as error:
            print(
                f"\nERROR: {source_file}"
            )

            print(
                f"  {error}"
            )

            continue

    save_hashes(hashes)

    print(
        "\nTranslation process completed."
    )


if __name__ == "__main__":
    main()
