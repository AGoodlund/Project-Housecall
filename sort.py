import json
from typing import List, Dict, Any

def match_providers(providers: List[Dict], user_tags: List[str]) -> List[Dict]:
    """
    Match providers based on specialty tags and calculate match scores.
    """
    user_tags_set = set(tag.lower() for tag in user_tags)
    matched_providers = []
    
    for provider in providers:
        provider_tags = provider.get('specialty_tags', provider.get('tags', []))
        provider_tags_set = set(tag.lower() for tag in provider_tags)
        
        matching_tags = user_tags_set.intersection(provider_tags_set)
        match_count = len(matching_tags)
        
        if match_count > 0:
            provider_copy = provider.copy()
            provider_copy['match_count'] = match_count
            provider_copy['matching_tags'] = list(matching_tags)
            matched_providers.append(provider_copy)
    
    matched_providers.sort(key=lambda x: x['match_count'], reverse=True)
    return matched_providers


def save_sorted_results(matched_providers: List[Dict], output_file: str = 'matched_providers.json'):
    """Save matched providers to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(matched_providers, f, indent=4)
    print(f"✅ Saved sorted providers to {output_file}")


if __name__ == "__main__":
    """
    This section runs only if you execute the script directly.
    You can dynamically provide data here or integrate this file
    into another script or backend service.
    """
    # Get input from external source (e.g., frontend, API, or file)
    try:
        # Example: read JSON input from stdin or a file path argument
        import sys
        if len(sys.argv) > 1:
            input_file = sys.argv[1]
            with open(input_file, "r") as f:
                data = json.load(f)
        else:
            print("Waiting for JSON input (with 'user_tags' and 'providers')...")
            data = json.loads(sys.stdin.read())
        
        user_tags = data.get("user_tags", [])
        providers = data.get("providers", [])
        
        if not user_tags or not providers:
            print("❌ Error: JSON must include both 'user_tags' and 'providers'.")
            sys.exit(1)
        
        matched = match_providers(providers, user_tags)
        save_sorted_results(matched)

    except Exception as e:
        print(f"❌ Error processing data: {e}")
        sys.exit(1)
