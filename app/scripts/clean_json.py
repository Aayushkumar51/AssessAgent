import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "app" / "data" / "shl_product_catalog.json"

OUTPUT_FILE = BASE_DIR / "app" / "data" / "cleaned_shl_catalog.json"


def clean_json_text(text):

    # Remove invalid control characters
    text = re.sub(r'[\x00-\x1F\x7F]', ' ', text)

    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    return text


def main():

    print("Reading broken JSON file...\n")

    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    print("Cleaning invalid characters...\n")

    cleaned = clean_json_text(raw)

    print("Saving cleaned file...\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"Cleaned file saved at:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()