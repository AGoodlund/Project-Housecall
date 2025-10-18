import requests
from bs4 import BeautifulSoup
    url = ""  # Replace with your target URL
    response = requests.get(url)
    html_content = response.text
    directProvider = BeautifulSoup(html_content, 'html.parser') # or 'lxml' for faster parsing

    # Example: Assuming specialties are in <span> tags with class 'specialty'
    specialty_elements = directProvider.find_all('span', class_='specialty')
    specialties = [element.get_text(strip=True) for element in specialty_elements]

    # If specialties are comma-separated in a single string
    all_specialties_raw = "Cardiology, Pediatrics, Dermatology"
    tags = [s.strip() for s in all_specialties_raw.split(',')]

    # Or directly from the extracted list
    doctor_tags = specialties

