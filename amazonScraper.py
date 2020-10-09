# required installs:
# numpy, pandas, selenium, chromedriver-py

# all installs can be installed with pip 
#  pip install [package]

# if chromedriver-py doesn't work, dl from here (https://sites.google.com/a/chromium.org/chromedriver/home)

import numpy as np
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from chromedriver_py import binary_path
import time

# start up automated browser
driver = webdriver.Chrome(executable_path=binary_path)

try:
	driver.get("https://www.amazon.com/gp/css/order-history?ref_=nav_AccountFlyout_orders")

	# enter email
    email = driver.find_element_by_name("email")
    email.clear()
    email.send_keys("") # ENTER AMAZON EMAIL HERE
    email.send_keys(Keys.RETURN)

    # enter password
    pwd = driver.find_element_by_name("password")
    pwd.clear()
    pwd.send_keys("") # ENTER AMAZON PASSWORD HERE
    pwd.send_keys(Keys.RETURN)

    # start scraping
    prices = []
    order_names = []
    order_qtys = []
    next_button_flag = 1
    while(next_button_flag):
        next_button_flag -= 1

        # getting list of orders on page
        orders_box = driver.find_element_by_id('ordersContainer') 
        orders = orders_box.find_elements_by_class_name('shipment') 

        # store price, name, quantity for each order in a list
        for i in orders:
            shipment_prices = i.find_elements_by_class_name('a-color-price')
            shipment_order_names = i.find_elements_by_class_name('a-link-normal')
            shipment_order_names = [j for j in shipment_order_names if j.text != '']
            shipment_order_qtys = i.find_elements_by_class_name('item-view-qty')
            for j in range(len(shipment_prices)):
                prices.append(shipment_prices[j].text)
                order_names.append(shipment_order_names[j].text)
                if(j < len(shipment_order_qtys)):
                    order_qtys.append(shipment_order_qtys[j].text)
                else:
                    order_qtys.append('1')
        
        # check for and move to next page 
        next_button_list = orders_box.find_elements_by_partial_link_text('Next')
        if (len(next_button_list) > 0):
            next_button = next_button_list[0]
            driver.get(next_button.get_attribute("href"))
            next_button_flag += 1
    
    # optional; remove to close window faster
    time.sleep(5)

# close automated browser
finally:
    driver.quit()
driver.quit()

# put all data in a pandas dataframe to easily make it a csv
info_d = {'Item': order_names, 'Price': prices, 'Quantity':order_qtys}
df = pd.DataFrame(info_d)
df

# convert dataframe to csv
df.to_csv('amazonOrders.csv')