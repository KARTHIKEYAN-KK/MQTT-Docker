from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    petrol_url = 'https://www.ndtv.com/fuel-prices/petrol-price-in-india'
    diesel_url = 'https://www.ndtv.com/fuel-prices/diesel-price-in-india'
    petrol_response = requests.get(petrol_url)
    diesel_response = requests.get(diesel_url)

    petrol_soup = BeautifulSoup(petrol_response.content, 'html.parser')
    diesel_soup = BeautifulSoup(diesel_response.content, 'html.parser')
    data = {}

    petrol_table = petrol_soup.find('table', {'class': 'font-16 color-blue short-nm'})
    diesel_table = diesel_soup.find('table', {'class': 'font-16 color-blue short-nm'})
    petrol_rows = petrol_table.find_all('tr')[1:]
    diesel_rows = diesel_table.find_all('tr')[1:]
    for p_row, d_row in zip(petrol_rows, diesel_rows):
        p_cols = p_row.find_all('td')
        d_cols = d_row.find_all("td")
        city = p_cols[0].text.strip()
        petrol_price = re.sub(r'[^\d.]+', '', (p_cols[1].text.strip()))
        diesel_price = d_cols[1].text.strip()
        data[city] = {'petrol': petrol_price, 'diesel': diesel_price}
    
    response_data = []
    for city, prices in data.items():
        response_data.append({'city': city, 'petrol': prices['petrol'], 'diesel': prices['diesel']})
    return jsonify(response_data)
    
    # return jsonify(data)