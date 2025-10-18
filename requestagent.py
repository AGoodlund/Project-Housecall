
import requests
def get_data_from_website(search_query):
    base_url = ""
    params = {"q": search_query}
    try:
        response = response.get(base_url,params=params)
        response.raise_for_status() #raise exception for http errors
        directProvider= response.text #or response.json() if its an API
        content_div = directProvider.find('div',id="ProviderData")
        if content_div:
            return content_div.get_text(separator = "\n", stip=True)
        else:
            return
    except requests.exceptions.RequestException as e:
        print(f"error fetching data: {e}")
        return None
    
#example usage
second_input = "cloud computing benefits"
website_data = get_data_from_website(second_input)
if website_data:
    print(f"data from website: {website_data[:200]}...")
