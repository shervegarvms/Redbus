from datetime import datetime
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="MDE92"
)
cursor = con.cursor()

# Function to scrape data
def scrape_data(source, destination, date):
    formatted_date = date.strftime("%d-%b-%Y")
    url = f"https://www.redbus.in/bus-tickets/{source.lower()}-to-{destination.lower()}?fromCityName={source}&toCityName={destination}&onward={formatted_date}&opId=0&busType=Any"
    driver.get(url)
    data = []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bus-item"))
        )
        
        buses = driver.find_elements(By.CLASS_NAME, "bus-item")
        
        for bus in buses:
            bus_name = bus.find_element(By.CLASS_NAME, "travels").text
            bus_type = bus.find_element(By.CLASS_NAME, "bus-type").text
            departure_time = bus.find_element(By.CLASS_NAME, "dp-time").text
            arrival_time = bus.find_element(By.CLASS_NAME, "bp-time").text
            price = bus.find_element(By.CLASS_NAME, "seat-fare").text

            # Filter by corporation name (optional, depending on actual bus name structure)
            if bus_name!= '':
                dict1 = {
                        "bus_name": bus_name,
                        "bus_type": bus_type,
                        "departure_time": departure_time,
                        "arrival_time": arrival_time,
                        "price": price
                    }
                data.append(dict1)
        return data
    
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return []
    finally:
        driver.quit()

# Streamlit UI
st.title("Redbus Data Scraping with Selenium and Dynamic Filtering")
source = st.text_input("Source")
destination = st.text_input("Destination")
date = st.date_input("Date")

if st.button("Scrape Data"):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome()#options=chrome_options)
    
    with st.spinner(f"Scraping data from {source} to {destination} on {date}..."):
        data = scrape_data(source, destination, date)
    
    if data:
        st.success("Data scraped successfully!")
        for route in data:
            st.write(f"Bus Name: {route['bus_name']}, Type: {route['bus_type']}, Departure: {route['departure_time']}, Arrival: {route['arrival_time']}, Fare: {route['price']}")
    else:
        st.error("No data found or an error occurred.")

