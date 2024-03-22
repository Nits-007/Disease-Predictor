import requests
from bs4 import BeautifulSoup

def scrape_doctors(location):
    url = f'https://www.practo.com/{location}/doctors'
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        doctors = []
        doctor_cards = soup.find_all('div', class_='info-section')
        for card in doctor_cards:
            name = card.find('h2', class_='doctor-name').text.strip()
            specialty = card.find('div', class_='u-d-flex').find('span').text.strip()
            address = card.find_all('a')[1].text.strip()
            doctors.append({
                'name': name,
                'address': address,
            })
        return doctors
    else:
        print('Failed to fetch data')
        return None