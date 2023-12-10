# Python Assignment - Individual (MSDA/CDA104 PYTHON FOR DATA SCIENCE)
#!/usr/bin/env python
# coding: utf-8
# Scraping Light in The Box Website - Using BeautifulSoup
# Import Libraries

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

title = [] # List to store names of the products
price = [] # List to store prices of the products
review = [] # List to store ratings of the products
data = [] # Extract information for all products
links_list = [] # Initialize the links_list

# Website URL for video games Category
URL = "https://www.lightinthebox.com/c/video-games_113331?prm=1.1.51.0"

# Headers for request
HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

# HTTP Request
webpage = requests.get(URL, headers=HEADERS)

# Type of webpage.content
type(webpage.content)


# Request connection status: [200] means successful while [503] means temporarily unavailable or unsuccessful
webpage

# Create a BeautifulSoup object
soup = BeautifulSoup(webpage.content, "html.parser")

# Fetch links as List of Tag Objects
links = soup.find_all("a", attrs={'class':'prod_item-2020'})
    
# Loop for extracting links from Tag Objects
for link in links:
    links_list.append(link.get('href'))
        
# Print or further process the links
for link in links_list:
    print(link)


# Find all div elements with class "prod-name"
all_prod_names = soup.find_all('div', class_='prod-name')

# Find all div elements with class "price"
all_prices = soup.find_all('div', class_='price')

# Find all span elements with class "review-score"
all_review_scores = soup.find_all('span', class_='review-score')

# Extract information for all products
for prod_name, price, review_score in zip(all_prod_names, all_prices, all_review_scores):
    title = prod_name['title']
    price_text = price.text.strip()
    review_score_text = review_score.text.strip()
    
    data.append({'Title': title, 'Price': price_text, 'Review Score': review_score_text})
    
# Create a Pandas DataFrame
df = pd.DataFrame(data)

# Create CSV file
df.to_csv("litb_data.csv", header=True, index=False)

# Print the DataFrame
print(df)

# Assuming 'Title' is the column containing product titles
df2 = pd.read_csv("litb_data.csv")

# Extract numeric values from 'Price' column and convert to integer
df2['Price'] = df2['Price'].replace('[^\d.]', '', regex=True).astype(float).astype(int)

# Convert 'Review Score' column to numeric values
df2['Review Score'] = pd.to_numeric(df2['Review Score'])

# Plotting
fig, ax = plt.subplots(figsize=(15, 6))

# Bar plot for Prices
ax.bar(df2['Title'], df2['Price'], color='blue', label='Price')

# Rotate x-axis labels for better readability
ax.set_xticks(range(len(df2['Title'])))
ax.set_xticklabels(df2['Title'], rotation=45, ha='right', fontsize=8)

# Line plot for Review Scores
ax2 = ax.twinx()
ax2.plot(df2['Title'], df2['Review Score'], color='red', marker='o', label='Review Score')

# Set labels and title
ax.set_ylabel('Price ($)')
ax2.set_ylabel('Review Score')
ax.set_xlabel('Game Consoles')
plt.title('Video Games Category Information')

# Show legend
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

# Show the plot
plt.show()

