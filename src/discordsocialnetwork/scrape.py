from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

# Set up Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Open in fullscreen
driver = webdriver.Chrome(options=options)

# Open Discord login page
driver.get("https://discord.com/login")

# Allow time for the page to load
time.sleep(3)

# get user credentials via environment variables
EMAIL = str(os.getenv("DISCORD_EMAIL"))
PASSWORD = str(os.getenv("DISCORD_PASSWORD"))

# Find and fill in email field
email_field = driver.find_element(By.NAME, "email")
email_field.send_keys(EMAIL)

# Find and fill in password field
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys(PASSWORD)

# Submit login form
password_field.send_keys(Keys.RETURN)

# Wait for the home page to load
time.sleep(10)  # Adjust this based on your internet speed
