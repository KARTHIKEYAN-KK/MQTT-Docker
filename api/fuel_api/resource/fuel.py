from flask import Flask, request, Response, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CityFuelPricesSchema, AllCityFuelPricesSchema
import requests
from bs4 import BeautifulSoup
import re

blp = Blueprint("Fuel Price details", __name__, description="Fuel prices of every cities in India")

@blp.route('/fuel/data/<string:city>')
class CityFuelData(MethodView):
    @blp.response(200, CityFuelPricesSchema())
    def get(self, city):
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
            cities = p_cols[0].text.strip()
            petrol_price = re.sub(r'[^\d.]+', '', (p_cols[1].text.strip()))
            diesel_price = re.sub(r'[^\d.]+', '', (d_cols[1].text.strip()))
            if cities.lower() == city.lower():
                data = {'city': cities, 'petrol': petrol_price, 'diesel': diesel_price}
                break
            else:
                data = {'message':'City not found or check the spelling of the city'}

        return jsonify(data)


@blp.route('/fuel/data')
class AllCityFuelData(MethodView):
    @blp.response(200, AllCityFuelPricesSchema())
    def get(self):
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
            cities = p_cols[0].text.strip()
            petrol_price = re.sub(r'[^\d.]+', '', (p_cols[1].text.strip()))
            diesel_price = re.sub(r'[^\d.]+', '', (d_cols[1].text.strip()))
            data[cities] = {'petrol': petrol_price, 'diesel': diesel_price}

        # return jsonify(data)

        response_data = []
        for city, prices in data.items():
            response_data.append({'city': city, 'petrol': prices['petrol'], 'diesel': prices['diesel']})
        return jsonify(response_data)
