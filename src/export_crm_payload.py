import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_CSV = BASE_DIR / "artifacts" / "cleaned_leads.csv"
OUTPUT_DIR = BASE_DIR / "artifacts"
OUTPUT_JSON = OUTPUT_DIR / "crm_payloads.json"


def split_name(full_name: str) -> tuple[str, str]:
    parts = full_name.strip().split()
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


def build_payload(row: dict[str, str]) -> dict[str, object]:
    first_name, last_name = split_name(row["agent_name"])
    return {
        "firstName": first_name,
        "lastName": last_name,
        "email": row["email"],
        "phone": row["mobile_phone"],
        "city": row["city"],
        "state": row["state"],
        "source": row["source_platform"],
        "tags": [
            f'{row["state"].lower()}-agent',
            "off-market-outreach",
            row["crm_status"].replace("_", "-"),
        ],
        "customFields": {
            "brokerage": row["brokerage"],
            "source_url": row["source_url"],
            "crm_status": row["crm_status"],
        },
    }


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    with INPUT_CSV.open("r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        payloads = [build_payload(row) for row in reader if row["crm_status"] == "ready_for_crm"]

    with OUTPUT_JSON.open("w", encoding="utf-8") as outfile:
        json.dump(payloads, outfile, indent=2)

    print(f"Exported {len(payloads)} CRM-ready payloads -> {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
