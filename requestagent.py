# requestagent.py
import csv
from typing import List, Dict
from provider import Provider

class ProviderAgent:
    """
    Load Provider objects from a CSV file.
    Supported header variants (case-insensitive):
      - name: name, provider_name
      - specialty: specialty, specialism
      - address: address, street, location
      - phone_number: phone_number, phone, tel
      - accepting_new_clients: accepting_new_clients, accepting, new_patients
    """

    def __init__(self):
        pass

    def load_providers_from_csv(self, csv_path: str) -> List[Provider]:
        """
        Read providers from a CSV file and return a list of Provider objects.

        If a column is missing, falls back to Provider._default (if available) or ''.
        """
        # Map CSV headers (lowercased) -> Provider attribute
        header_map: Dict[str, str] = {
            "name": "name",
            "provider_name": "name",
            "specialty": "specialty",
            "specialism": "specialty",
            "address": "address",
            "street": "address",
            "location": "address",
            "zip": "zip_code",
            "zipcode": "zip_code",
            "postal_code": "zip_code",
            "phone_number": "phone_number",
            "phone": "phone_number",
            "tel": "phone_number",
            "accepting_new_clients": "accepting_new_clients",
            "accepting": "accepting_new_clients",
            "new_patients": "accepting_new_clients",
        }

        providers: List[Provider] = []

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, restkey="_extra", restval="")

            # Normalize header names defensively
            raw_fields = reader.fieldnames or []
            normalized_fields: Dict[object, str] = {}
            for fn in raw_fields:
                if not isinstance(fn, str):
                    # skip non-string header cells
                    continue
                key = fn.lstrip("\ufeff").strip()
                normalized_fields[fn] = key.lower()
                
            for row in reader:
                p = Provider()

                # Helper to set attribute with a safe default
                def set_attr(attr: str, value):
                    default_val = getattr(Provider, "_default", "")
                    setattr(p, attr, (value if value not in (None, "") else default_val))

                # Map recognized columns onto Provider
                for original_key, value in row.items():
                     # Skip invalid keys and the aggregated extras
                    if original_key in (None, "_extra") or not isinstance(original_key, str):
                        continue

                    mapped = normalized_fields.get(original_key, original_key)
                    key_lc = mapped.lower() if isinstance(mapped, str) else ""
                    attr = header_map.get(key_lc)
                    if not attr:
                        continue

                    if isinstance(value, str):
                        value = value.strip()

                    # Normalize accepting_new_clients to bool
                    if attr == "accepting_new_clients":
                        v = (value or "").strip().lower() if isinstance(value, str) else ""
                        if v in {"true", "yes", "y", "1"}:
                            value = True
                        elif v in {"false", "no", "n", "0"}:
                            value = False
                        else:
                            value = False

                    set_attr(attr, value)

                # Ensure all expected attributes exist
                for attr in ("name", "specialty", "address","zip-code" "phone_number", "accepting_new_clients"):
                    if not hasattr(p, attr):
                        set_attr(attr, "" if attr != "accepting_new_clients" else False)

                providers.append(p)

        return providers


def pretty_print_provider(p: Provider, index: int | None = None) -> None:
    prefix = f"[{index}] " if index is not None else ""
    print(
        f"{prefix}name={getattr(p,'name','')} | "
        f"specialty={getattr(p,'specialty','')} | "
        f"address={getattr(p,'address','')} | "
        f"phone={getattr(p,'phone_number','')} | "
        f"accepting={getattr(p,'accepting_new_clients',False)}"
    )


def normalize_search_field(raw: str) -> str | None:
    """Map user-entered field name to an attribute on Provider."""
    key = (raw or "").strip().lower()
    if key in {"name", "provider", "provider_name"}:
        return "name"
    if key in {"specialty", "specialism"}:
        return "specialty"
    if key in {"address", "street", "location"}:
        return "address"
    if key in {"zip", "zipcode", "postal", "postal_code"}:
        return "zip_code"
    if key in {"phone", "phone_number", "tel"}:
        return "phone_number"
    if key in {"accepting", "accepting_new_clients", "new_patients"}:
        return "accepting_new_clients"
    if key in {"", "any", "all"}:
        return ""  # search across common text fields
    return None


def parse_bool(text: str) -> bool | None:
    t = (text or "").strip().lower()
    if t in {"true", "yes", "y", "1"}:
        return True
    if t in {"false", "no", "n", "0"}:
        return False
    return None


def provider_matches(p: Provider, field: str, query: str) -> bool:
    """Return True if provider p matches query for given field ('' means multi-field)."""
    if field == "accepting_new_clients":
        desired = parse_bool(query)
        if desired is None:
            return False
        return bool(getattr(p, "accepting_new_clients", False)) == desired

    # Text search: case-insensitive "contains"
    haystacks = []
    if field:
        haystacks = [str(getattr(p, field, "") or "")]
    else:
        # multi-field search across common text attributes
        haystacks = [
            str(getattr(p, "name", "") or ""),
            str(getattr(p, "specialty", "") or ""),
            str(getattr(p, "address", "") or ""),
            str(getattr(p, "zip_code", "") or ""),
            str(getattr(p, "phone_number", "") or ""),
        ]
    needle = (query or "").strip().lower()
    if not needle:
        return False
    return any(needle in h.lower() for h in haystacks)


if __name__ == "__main__":
    agent = ProviderAgent()

    # Look for a CSV in common locations
    import os
    candidate_paths = [
        "output.csv",
        "outout.csv",             # earlier misspelling fallback
        "/mnt/data/output.csv",
        "/mnt/data/outout.csv",
    ]
    csv_path = next((p for p in candidate_paths if os.path.exists(p)), None)
    if not csv_path:
        raise SystemExit(
            "CSV not found. Place 'output.csv' (or 'outout.csv') next to this file "
            "or in /mnt/data/, then run again."
        )

    providers = agent.load_providers_from_csv(csv_path)
    print(f"Loaded {len(providers)} providers from {csv_path}\n")

    # --- Interactive filter ---
    print("Search fields: name, specialty, zip-code, address, phone, accepting")
    field_input = input("Choose a field (or press Enter to search all text fields): ")
    field = normalize_search_field(field_input)
    if field is None:
        raise SystemExit(f"Unrecognized field: '{field_input}'. Valid: zip-code, name, specialty, address, phone, accepting.")

    query = input(
        "Enter your search query "
        + ("(true/false/yes/no for 'accepting'): " if field == "accepting_new_clients" else ": ")
    )

    matches = [p for p in providers if provider_matches(p, field, query)]

    if not matches:
        print("\nNo matching providers found.")
    elif len(matches) == 1:
        print("\nSelected provider:")
        pretty_print_provider(matches[0])
    else:
        print(f"\nFound {len(matches)} matching providers:")
        for i, p in enumerate(matches, 1):
            pretty_print_provider(p, i)
        # Optional: allow user to pick one for exact "instance"
        pick = input("\nEnter the number of the provider to view details (or press Enter to skip): ").strip()
        if pick.isdigit():
            idx = int(pick)
            if 1 <= idx <= len(matches):
                print("\nSelected provider:")
                pretty_print_provider(matches[idx - 1])
            else:
                print("Index out of range; showing all matches above.")