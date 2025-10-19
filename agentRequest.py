# requestagent.py
import csv
from typing import List, Dict
from provider import Provider

class ProviderAgent:
    """
    Load Provider objects either from a CSV file or (optionally) from a web search.
    This version focuses on CSV ingestion.
    """

    def __init__(self):
        pass

    # ---------- CSV INGESTION PATH ----------
    def load_providers_from_csv(self, csv_path: str) -> List[Provider]:
        """
        Read providers from a CSV file and return a list of Provider objects.

        Supports common header variants:
          - name: name, provider_name
          - specialty: specialty, specialism
          - address: address, street, location
          - phone_number: phone_number, phone, tel
          - accepting_new_clients: accepting_new_clients, accepting, new_patients
        If a column is missing, falls back to Provider._default (if available) or ''.
        """
        # Known header -> Provider attribute mapping (lowercased headers)
        header_map: Dict[str, str] = {
            "name": "name",
            "provider_name": "name",

            "specialty": "specialty",
            "specialism": "specialty",

            "address": "address",
            "street": "address",
            "location": "address",

            "phone_number": "phone_number",
            "phone": "phone_number",
            "tel": "phone_number",

            "accepting_new_clients": "accepting_new_clients",
            "accepting": "accepting_new_clients",
            "new_patients": "accepting_new_clients",
        }

        providers: List[Provider] = []

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Normalize fieldnames once
            normalized_fields = {fn: fn.lower().strip() for fn in reader.fieldnames or []}

            for row in reader:
                p = Provider()

                # Helper to set an attribute with fallback to Provider._default or empty string
                def set_attr(attr: str, value):
                    default_val = getattr(Provider, "_default", "")
                    setattr(p, attr, (value if value not in (None, "") else default_val))

                # For each CSV column, map to Provider attribute if we recognize it
                for original_key, value in row.items():
                    key_lc = normalized_fields.get(original_key, original_key).lower()
                    attr = header_map.get(key_lc)
                    if not attr:
                        continue  # unrecognized column, skip

                    # Clean value
                    if isinstance(value, str):
                        value = value.strip()

                    # Convert accepting_new_clients to bool if present
                    if attr == "accepting_new_clients":
                        if isinstance(value, str):
                            v = value.lower()
                            if v in {"true", "yes", "y", "1"}:
                                value = True
                            elif v in {"false", "no", "n", "0"}:
                                value = False
                            else:
                                value = False  # default if unclear
                        elif isinstance(value, (int, float)):
                            value = bool(value)
                        else:
                            value = False

                    set_attr(attr, value)

                # Ensure all expected attributes exist even if columns were missing
                for attr in ("name", "specialty", "address", "phone_number", "accepting_new_clients"):
                    if not hasattr(p, attr):
                        set_attr(attr, "" if attr != "accepting_new_clients" else False)

                providers.append(p)

        return providers


if __name__ == "__main__":
    agent = ProviderAgent()
    # Try the expected filename, then the earlier typo as a fallback
    import os
    candidate_paths = ["output.csv", "outout.csv", "/mnt/data/output.csv", "/mnt/data/outout.csv"]

    csv_path = next((p for p in candidate_paths if os.path.exists(p)), None)
    if not csv_path:
        raise SystemExit(
            "CSV not found. Place 'output.csv' or 'outout.csv' next to this file "
            "or in /mnt/data/, then run again."
        )

    providers = agent.load_providers_from_csv(csv_path)
    print(f"Loaded {len(providers)} providers from {csv_path}")
    # Show a quick preview
    for i, p in enumerate(providers[:5], start=1):
        print(f"[{i}] name={getattr(p,'name',None)} | specialty={getattr(p,'specialty',None)} "
              f"| phone={getattr(p,'phone_number',None)} | accepting={getattr(p,'accepting_new_clients',None)}")




