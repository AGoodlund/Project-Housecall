
import requests
def get_data_from_website(search_query):
    base_url = "https://mapper.dpcfrontier.com"
    params = {"q": search_query}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() #raise exception for http errors
        return response.text #or response.json() if its an API
    except requests.exceptions.RequestException as e:
        print(f"error fetching data: {e}")
        return None
    
#example usage
second_input = "95747"
website_data = get_data_from_website(second_input)
if website_data:
    print(f"data from website: {website_data[:200]}...")
