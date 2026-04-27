import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_CSV = BASE_DIR / "examples" / "raw_leads_sample.csv"
OUTPUT_DIR = BASE_DIR / "artifacts"
OUTPUT_CSV = OUTPUT_DIR / "cleaned_leads.csv"


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def normalize_phone(value: str) -> str:
    digits = "".join(ch for ch in value if ch.isdigit())
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"+1-{digits[0:3]}-{digits[3:6]}-{digits[6:10]}"
    return value.strip()


def normalize_email(value: str) -> str:
    return value.strip().lower()


def dedupe_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        normalize_text(row["agent_name"]).lower(),
        normalize_email(row["email"]),
        normalize_phone(row["mobile_phone"]),
    )


def crm_status(row: dict[str, str]) -> str:
    required_fields = ("agent_name", "mobile_phone", "city", "state", "source_platform", "source_url")
    if any(not row[field] for field in required_fields):
        return "needs_review"
    if not row["email"]:
        return "needs_review"
    return "ready_for_crm"


def clean_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str, str]] = set()
    cleaned: list[dict[str, str]] = []
    for row in rows:
        normalized = {
            "agent_name": normalize_text(row["agent_name"]),
            "brokerage": normalize_text(row["brokerage"]),
            "email": normalize_email(row["email"]),
            "mobile_phone": normalize_phone(row["mobile_phone"]),
            "city": normalize_text(row["city"]).title(),
            "state": row["state"].strip().upper(),
            "source_platform": normalize_text(row["source_platform"]),
            "source_url": row["source_url"].strip(),
        }
        key = dedupe_key(normalized)
        if key in seen:
            continue
        seen.add(key)
        normalized["crm_status"] = crm_status(normalized)
        cleaned.append(normalized)
    return cleaned


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    with INPUT_CSV.open("r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        cleaned = clean_rows(list(reader))

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=cleaned[0].keys())
        writer.writeheader()
        writer.writerows(cleaned)

    print(f"Cleaned {len(cleaned)} unique lead records -> {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
