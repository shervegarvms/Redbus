Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit

This repository contains a comprehensive solution for scraping, storing, and visualizing bus travel data from the Red Bus website. The project utilizes Selenium for web scraping, SQL for data storage, and Streamlit for data visualization.

Table of Contents
Introduction
Skills Acquired
Problem Statement
Approach
Project Structure
Prerequisites
Installation
Usage
Contributing
Introduction
This project aims to provide a robust solution for collecting, analyzing, and visualizing bus travel data from the Red Bus platform. It is divided into three primary components:

Web Scraping Script: Extracts data from the Red Bus website.
SQL Script: Inserts the extracted data into a SQL database.
Streamlit App: Visualizes the data stored in the SQL database.
Skills Acquired
Web Scraping using Selenium
Python Programming
Data Visualization with Streamlit
SQL Database Management
Problem Statement
The "Redbus Data Scraping and Filtering with Streamlit Application" project seeks to revolutionize the transportation industry by offering a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By automating the extraction of detailed information from Redbus—such as bus routes, schedules, prices, and seat availability—this project enhances data collection processes and empowers data-driven decision-making. This can significantly improve operational efficiency and strategic planning within the transportation sector.

Approach
Data Scraping
Utilize Selenium to automate the extraction of data from the Redbus website, including routes, schedules, prices, and seat availability.
Data Storage
Store the scraped data in a SQL database.
Streamlit Application
Develop a Streamlit application to display and filter the scraped data.
Implement filters such as bus type, route, price range, star rating, and availability.
Data Analysis/Filtering using Streamlit
Execute SQL queries to retrieve and filter data based on user inputs.
Leverage Streamlit to allow users to interact with and filter the data through the application.
Project Structure
red_bus_scraping.ipynb: Jupyter notebook containing the Selenium script for scraping data from the Red Bus website.
sql_script.ipynb: Jupyter notebook containing the SQL script for inserting the scraped data into a SQL database.
streamlit_app.py: Streamlit application script for displaying the scraped data.
Prerequisites
Ensure you have the following installed before starting:

Python 3.x
Jupyter Notebook
Selenium
Streamlit
SQL Database (e.g., SQLite, MySQL)
Installation
Clone the repository:

git clone https://github.com/arunachaladevaraj/red_bus_scraping.git
cd red_bus_scraping
Install the required Python packages:

pip install -r requirements.txt
Set up your SQL database and update the connection details in sql_script.ipynb and streamlit_app.py.

Usage
Run the web scraping script: Open red_bus_scraping.ipynb in Jupyter Notebook and execute the cells to scrape data from the Red Bus website.

Insert data into the SQL database: Open sql_script.ipynb in Jupyter Notebook and execute the cells to insert the scraped data into your SQL database.

Run the Streamlit app:

streamlit run streamlit_app.py
This will start the Streamlit server and open the app in your default web browser.
