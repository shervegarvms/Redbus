import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import time
import mysql.connector

st.title("Bus Route Data Scraper")

# Dropdown list for state selection
state_options = ['Kerala (KSRTC)', 'Kadamba (KTCL)', 'Rajasthan (RSRTC)', 'Himachal Pradesh (HRTC)',
                 'Punjab (PEPSU)', 'Bihar (BSRTC)', 'South Bengal (SBSTC)', 'West Bengal', 
                 'Chandigarh (CTU)', 'Assam (ASTC)']
selected_state = st.selectbox("Select State", state_options)

# Function to scrape data
def scrape_data(state):
    driver = webdriver.Chrome()
    state_urls = {
        'Kerala (KSRTC)': 'https://www.redbus.in/online-booking/ksrtc-kerala',
        'Kadamba (KTCL)': 'https://www.redbus.in/online-booking/ktcl-kadamba',
        'Rajasthan (RSRTC)': 'https://www.redbus.in/online-booking/rsrtc-rajasthan',
        'Himachal Pradesh (HRTC)': 'https://www.redbus.in/online-booking/hrtc-himachal-pradesh',
        'Punjab (PEPSU)': 'https://www.redbus.in/online-booking/pepsu-punjab',
        'Bihar (BSRTC)': 'https://www.redbus.in/online-booking/bsrtc-bihar',
        'South Bengal (SBSTC)': 'https://www.redbus.in/online-booking/sbstc-south-bengal',
        'West Bengal': 'https://www.redbus.in/online-booking/wbtc-west-bengal',
        'Chandigarh (CTU)': 'https://www.redbus.in/online-booking/ctu-chandigarh',
        'Assam (ASTC)': 'https://www.redbus.in/online-booking/astc-assam'
    }
    
    driver.get(state_urls[state])
    driver.maximize_window()

    time.sleep(3)
    driver.execute_script("window.scrollBy(0, window.innerHeight);")
    driver.execute_script("window.scrollBy(0, window.innerHeight);")
    driver.execute_script("window.scrollBy(0, window.innerHeight);")

    route_names = []
    route_links = []

    def get_route_data():
        route_elements = driver.find_elements(By.CLASS_NAME, "route")
        for route_element in route_elements:
            route_names.append(route_element.text)
            route_links.append(route_element.get_attribute('href'))

    page_tabs = driver.find_elements(By.CLASS_NAME, "DC_117_pageTabs ")
    for i in range(len(page_tabs)):
        if i > 0:
            page_tab = page_tabs[i]
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(page_tab)
                )
                driver.execute_script("arguments[0].click();", page_tab)
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", page_tab)
            time.sleep(4)
        get_route_data()

    df = pd.DataFrame(columns=['route_name', 'route_link', 'busname', 'bustype', 'departing_time', 
                               'duration', 'reaching_time', 'star_rating', 'price', 'seats_available'])
    count = 0
    for link in route_links:
        driver.get(link)
        driver.maximize_window()

        try:
            wait = WebDriverWait(driver, 3)
            wait_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
            driver.execute_script("arguments[0].click();", wait_button)
        except (NoSuchElementException, TimeoutException):
            pass    

        for t in range(22):  # scrolling 20 times so that the whole website loads
            driver.execute_script("window.scrollBy(0, 650);")
            time.sleep(0.3)

        bus_name = []
        bus_type = []
        departing = []
        duration = []
        reaching = []
        rating = []
        price = []
        availability = []
        route_name = []
        route_link = []

        names = driver.find_elements(By.CLASS_NAME, "travels")
        types = driver.find_elements(By.CLASS_NAME, "bus-type")
        depart_timings = driver.find_elements(By.CLASS_NAME, "dp-time")
        travel_durations = driver.find_elements(By.CLASS_NAME, "dur")
        arrivals = driver.find_elements(By.CLASS_NAME, "bp-time")
        star_ratings = driver.find_elements(By.CLASS_NAME, "column-six")
        fares = driver.find_elements(By.CLASS_NAME, "fare")
        seats_available = driver.find_elements(By.CLASS_NAME, "seat-left")

        for name in names:
            bus_name.append(name.text)

        for type in types:
            bus_type.append(type.text)

        for depart_timing in depart_timings:
            departing.append(depart_timing.text)

        for travel_duration in travel_durations:
            duration.append(travel_duration.text)

        for arrival in arrivals:
            reaching.append(arrival.text)

        for star_rating in star_ratings:
            rating.append(star_rating.text[:3])

        for fare in fares:
            if fare.text.isdigit():
                price.append(fare.text)
            else:
                price.append(fare.text.replace('INR', '').strip())

        for seat_available in seats_available:
            availability.append(seat_available.text[:2].strip())
        
        for i in range(len(bus_name)):
            route_name.append(route_names[count])
            route_link.append(link)

        count += 1

        for i in range(len(rating)):
            if rating[i] == 'New' or rating[i] == ' ':
                rating[i] = '0.0'

        data = {
            'route_name': route_name,
            'route_link': route_link,
            'busname': bus_name,
            'bustype': bus_type,
            'departing_time': departing,
            'duration': duration,
            'reaching_time': reaching,
            'star_rating': rating,
            'price': price,
            'seats_available': availability
        }

        df1 = pd.DataFrame(data)
        df = pd.concat([df, df1], ignore_index=True)

    driver.quit()
    return df

# Function to insert data into MySQL
def insert_data_into_mysql(df):
    connection = mysql.connector.connect(
        host='localhost',  # Change as per your MySQL server settings
        user='root',  # Change to your MySQL username
        password='12345678',  # Change to your MySQL password
        database='Redbus'  # Change to your MySQL database name
    )
    cursor = connection.cursor()

    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO bus_routes (route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['route_name'], row['route_link'], row['busname'], row['bustype'], row['departing_time'],
            row['duration'], row['reaching_time'], row['star_rating'], row['price'], row['seats_available']
        ))
    
    connection.commit()
    cursor.close()
    connection.close()

if st.button('Scrape Data'):
    with st.spinner('Scraping data...'):
        df = scrape_data(selected_state)
        st.write('Scraping complete!')
        
        # Insert data into MySQL
        insert_data_into_mysql(df)
        st.write('Data inserted into MySQL database!')

    st.dataframe(df)
