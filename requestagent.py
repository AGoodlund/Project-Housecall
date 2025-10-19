# requestagent.py
import csv
from typing import List, Dict
from provider import Provider

def read_queries_from_txt(txt_path: str) -> tuple[str, str]:
    """
    Read the first two lines from a text file:
      line 1 -> zip (string, supports partial match)
      line 2 -> free-text (searched across name/specialty/address/zip/phone)
    """
    zip_query = ""
    free_query = ""
    with open(txt_path, "r", encoding="utf-8-sig") as f:
        lines = [ln.strip() for ln in f.readlines()]
    if lines:
        zip_query = lines[0]
    if len(lines) > 1:
        free_query = lines[1]
    return zip_query, free_query


def pick_first_distinct(
    pool: list, 
    already_picked: set
):
    """Return the first item in pool not in already_picked; fallback to pool[0] if needed."""
    if not pool:
        return None
    for p in pool:
        if id(p) not in already_picked:
            return p
    return pool[0]  # all were picked; allow repeat




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
                for attr in ("name", "specialty", "address","zip_code" "phone_number", "accepting_new_clients"):
                    if not hasattr(p, attr):
                        set_attr(attr, "" if attr != "accepting_new_clients" else False)

                providers.append(p)

        return providers


def pretty_print_provider(p: Provider, index: int | None = None, fields_to_show: list[str] | None = None) -> None:
    prefix = f"[{index}] " if index is not None else ""
    if not fields_to_show:
        fields_to_show = ["name", "specialty", "address", "zip_code", "phone_number", "accepting_new_clients"]

    label_map = {
        "name": "name",
        "specialty": "specialty",
        "address": "address",
        "zip_code": "zip",
        "phone_number": "phone",
        "accepting_new_clients": "accepting",
        "tags": "tags",
    }

    parts = []
    for f in fields_to_show:
        lab = label_map.get(f, f)
        val = getattr(p, f, "")
        if f == "tags" and isinstance(val, list):
            val = ", ".join(val)
        parts.append(f"{lab}={val}")
    print(prefix + " | ".join(parts))



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

    import os
    # CSV candidates
    candidate_csv_paths = [
        "output.csv",
        "outout.csv",
        "/mnt/data/output.csv",
        "/mnt/data/outout.csv",
        "sac_mhp_output.csv",
        "/mnt/data/sac_mhp_output.csv",
    ]
    csv_path = next((p for p in candidate_csv_paths if os.path.exists(p)), None)
    if not csv_path:
        raise SystemExit(
            "CSV not found. Place 'output.csv' (or 'outout.csv' / 'sac_mhp_output.csv') "
            "next to this file or in /mnt/data/, then run again."
        )

    # Query file (line 1 = ZIP, line 2 = free-text)
    candidate_txt_paths = ["query.txt", "/mnt/data/query.txt"]
    txt_path = next((p for p in candidate_txt_paths if os.path.exists(p)), None)
    if not txt_path:
        raise SystemExit(
            "Query file not found. Create 'query.txt' with:\n"
            "  line 1 = zip (e.g., 85001)\n"
            "  line 2 = free text (e.g., family medicine)\n"
        )

    zip_query, free_query = read_queries_from_txt(txt_path)

    providers = agent.load_providers_from_csv(csv_path)

    # Prepare match pools
    zip_matches = []
    text_matches = []
    both_matches = []

    if zip_query.strip():
        zip_matches = [p for p in providers if provider_matches(p, "zip_code", zip_query)]

    if free_query.strip():
        # empty field => search across all common text fields
        text_matches = [p for p in providers if provider_matches(p, "", free_query)]

    if zip_query.strip() and free_query.strip():
        both_matches = [
            p for p in providers
            if provider_matches(p, "zip_code", zip_query) and provider_matches(p, "", free_query)
        ]

    # Pick one for each bucket (aim for distinct providers where possible)
    picked_ids = set()
    one_zip = pick_first_distinct(zip_matches, picked_ids)
    if one_zip:
        picked_ids.add(id(one_zip))

    one_text = pick_first_distinct(text_matches, picked_ids)
    if one_text:
        picked_ids.add(id(one_text))

    one_both = pick_first_distinct(both_matches, picked_ids)
    # (don't add to picked_ids; nothing else to pick after this)

    # Decide which columns to show:
    #   Always show name and the field(s) you asked about (zip and whatever your free text is targeting).
    fields_to_show = ["name"]
    if zip_query.strip():
        fields_to_show.append("zip_code")
    # Show core fields to make results useful
    for f in ["specialty", "address", "phone_number", "accepting_new_clients"]:
        if f not in fields_to_show:
            fields_to_show.append(f)

    print(f"Loaded {len(providers)} providers from {csv_path}")
    print(f"Query file: {txt_path}")

    # --- Output: one provider for ZIP ---
    if one_zip:
        pretty_print_provider(one_zip, fields_to_show=fields_to_show)
    else:
        print("No provider matched the ZIP query.")

    # --- Output: one provider for TEXT ---
    if one_text:
        pretty_print_provider(one_text, fields_to_show=fields_to_show)
    else:
        print("No provider matched the TEXT query.")
    # --- Output: one provider for BOTH ---
    if one_both:
        pretty_print_provider(one_both, fields_to_show=fields_to_show)
    else:
        print("No provider matched BOTH ZIP and TEXT.")
