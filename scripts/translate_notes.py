import os
import re
import json
import urllib.request


API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-3.5-flash-lite"
SOURCE_DIR = "Libft"
TRANSLATION_DIR = "translations"


def protect_markdown(text):
    protected = []

    def replace(match):
        protected.append(match.group(0))
        return f"___PROTECTED_{len(protected) - 1}___"

    pattern = r"```[\s\S]*?```|`[^`\n]+`|https?://[^\s)]+"
    text = re.sub(pattern, replace, text)

    return text, protected


def restore_markdown(text, protected):
    for i, value in enumerate(protected):
        text = text.replace(f"___PROTECTED_{i}___", value)

    return text


def find_markdown_files():
    files = []

    for root, dirs, filenames in os.walk(SOURCE_DIR):
        for filename in filenames:
            if filename.endswith(".md"):
                files.append(os.path.join(root, filename))

    return sorted(files)


def translate(text, language):
    prompt = f"""Translate the following Markdown text into {language}.

Important rules:
- Return only the translated Markdown.
- Preserve all Markdown structure.
- Do not add explanations.
- Do not translate placeholders such as ___PROTECTED_0___.
- Keep the original meaning accurate.
- This is a technical programming note.
- Preserve C programming terminology accurately.

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

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["candidates"][0]["content"]["parts"][0]["text"]


def get_translation_path(source_file, language):
    relative_path = os.path.relpath(source_file, SOURCE_DIR)

    if language == "English":
        language_dir = "en"
    else:
        language_dir = "fr"

    return os.path.join(
        TRANSLATION_DIR,
        language_dir,
        relative_path
    )


def translate_file(source_file):
    print(f"\nTranslating: {source_file}")

    with open(source_file, "r", encoding="utf-8") as file:
        original = file.read()

    protected_text, protected = protect_markdown(original)

    english = translate(protected_text, "English")
    french = translate(protected_text, "French")

    english = restore_markdown(english, protected)
    french = restore_markdown(french, protected)

    english_file = get_translation_path(source_file, "English")
    french_file = get_translation_path(source_file, "French")

    os.makedirs(os.path.dirname(english_file), exist_ok=True)
    os.makedirs(os.path.dirname(french_file), exist_ok=True)

    with open(english_file, "w", encoding="utf-8") as file:
        file.write(english)

    with open(french_file, "w", encoding="utf-8") as file:
        file.write(french)

    print(f"  English -> {english_file}")
    print(f"  French  -> {french_file}")


def main():
    files = find_markdown_files()

    print(f"Found {len(files)} Markdown files.")

    for source_file in files:
        translate_file(source_file)

    print("\nTranslation completed.")


if __name__ == "__main__":
    main()
