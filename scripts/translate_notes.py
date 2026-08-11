import os
import re
import json
import urllib.request


API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-3.5-flash-lite"
SOURCE_FILE = "Libft/Part 1- Libc functions/strlen().md"


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


def translate(text, language):
    prompt = f"""Translate the following Markdown text into {language}.

Important rules:
- Return only the translated Markdown.
- Preserve all Markdown structure.
- Do not add explanations.
- Do not translate placeholders such as ___PROTECTED_0___.
- Keep the original meaning accurate.
- This is a technical programming note.

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


def main():
    with open(SOURCE_FILE, "r", encoding="utf-8") as file:
        original = file.read()

    protected_text, protected = protect_markdown(original)

    english = translate(protected_text, "English")
    french = translate(protected_text, "French")

    english = restore_markdown(english, protected)
    french = restore_markdown(french, protected)

    english_file = "translations/en/" + os.path.basename(SOURCE_FILE)
    french_file = "translations/fr/" + os.path.basename(SOURCE_FILE)

    os.makedirs(os.path.dirname(english_file), exist_ok=True)
    os.makedirs(os.path.dirname(french_file), exist_ok=True)

    with open(english_file, "w", encoding="utf-8") as file:
        file.write(english)

    with open(french_file, "w", encoding="utf-8") as file:
        file.write(french)

    print("English:", english_file)
    print("French:", french_file)


if __name__ == "__main__":
    main()
