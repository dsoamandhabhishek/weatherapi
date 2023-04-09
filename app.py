from flask import Flask, render_template, request
import requests
from datetime import datetime
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
cnx = mysql.connector.connect(user='root', password='12345',
                              host='localhost', database='your_database')
cursor = cnx.cursor()

# Define route for index page
@app.route('/')
def index():
    return render_template('index.html')

# Define route for weather page
@app.route('/get-weather')
def get_weather():
    # Get city name from form input
    city = request.args.get('city')

    # Call OpenWeatherMap API to get weather data
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=9660d420ec5c6c3bc136e365a8462418&units=metric'
    response = requests.get(url).json()

    # Parse weather data
    temperature = response['main']['temp']
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']

    # Save weather data to MySQL database
    timestamp = datetime.now()
    sql = "INSERT INTO weather_data (city_name, temperature, humidity, description, timestamp) VALUES (%s, %s, %s, %s, %s)"
    val = (city, temperature, humidity, description, timestamp)
    cursor.execute(sql, val)
    cnx.commit()

    # Define weather dictionary
    weather = {
        'city': city,
        'temperature': temperature,
        'humidity': humidity,
        'description': description
    }

    # Render weather data on HTML page
    return render_template('weather.html', weather=weather)

if __name__ == '__main__':
    app.run(debug=True)
