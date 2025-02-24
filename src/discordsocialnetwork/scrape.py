from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import json

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


# at this point we are logged in and on the main page
#
# we need to go to the "all" friends page, click through each friend, and scrape their profile for mutual servers, friends, and other relevant information
# element looks like <div class="item__133bf item_b3f026 themed_b3f026" role="tab" aria-selected="false" aria-disabled="false" tabindex="-1">All</div>

# click on the "all" friends tab

# we now iterate over all people in this list

# look for element <div class="peopleList__5ec2f auto__99f8c scrollerBase__99f8c" role="list" tabindex="0" data-list-id="people-list" ...
#
# inside this is other element <div class="content__99f8c" style="height: 8482px;"><div aria-hidden="true" style="height: 0px;"> ...
# and inside this is a list of friends we can click.
# friend elemnts are in the form of:
# <div class="peopleListItem_cc6179" role="listitem" data-list-item-id="people-list___248600454013911040" tabindex="-1" ....

# we want to right click on a person element, choose the "Profile Option"
# the profile is now on the screen, we want to go to the "mutual friends" by clicking a button of the form:
#<div class="tabBarItem_d1d9f3 item_b3f026 themed_b3f026" role="tab" aria-selected="false" aria-disabled="false" ...

# which will change the following list scroller div to show a list of frineds:
# <div class="listScroller__9d78f thin_d125d2 scrollerBase_d125d2 fade_d125d2" dir="ltr" ...
# within each listscroller element, there are some list row elements:
# <div class="listRow__9d78f" role="button" tabindex="0"><div class="wrapper__44b0c listAvatar__9d78f" role="img" ...
# and in each of those listrow elements, there is a info element <div class="info_f4bc97 listName__9d78f"><span class="">Calvin</span></div> with the name of the friend.

# once we have all the friends names, we do the same for the mutual servers.
# profile will still be open, we just click a button of the form:
# <div class="defaultColor__4bd52 text-sm/normal_cf4812" data-text-variant="text-sm/normal">1 Mutual Server</div>
# this will change the same list elements to showcase list row elements with the server names.

# all this info should be stored as the following:
# name of user: string, list of mutual friends: list(string), list of mutual servers: list(string)

# ---

# Click on "All" friends tab
all_friends_tab = driver.find_element(By.XPATH, "//div[contains(text(), 'All')]")
all_friends_tab.click()
time.sleep(3)  # Wait for the friend list to load

running = True
TotalFriends = friends = driver.find_elements(By.CLASS_NAME, "peopleListItem_cc6179")

while running:

# Get all friend elements

    print("got here")
    print(friends)

    friend_data = {}

# Iterate through each friend
    for friend in friends:
        # Extract friend's name
        friend_name_elem = friend.find_element(By.CLASS_NAME, "username-class")  # Update class name
        friend_name = friend_name_elem.text

        # Right-click and open profile
        action = ActionChains(driver)
        action.context_click(friend).perform()
        time.sleep(1)

        # Click "Profile" from context menu
        profile_option = driver.find_element(By.XPATH, "//div[contains(text(), 'Profile')]")
        profile_option.click()
        time.sleep(3)

        # Scrape mutual friends
        mutual_friends_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Mutual Friends')]")
        mutual_friends_button.click()
        time.sleep(2)

        mutual_friends = []
        mutual_friends_list = driver.find_elements(By.CLASS_NAME, "listRow__9d78f")
        for mutual in mutual_friends_list:
            name_elem = mutual.find_element(By.CLASS_NAME, "info_f4bc97")
            mutual_friends.append(name_elem.text)

        # Scrape mutual servers
        mutual_servers_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Mutual Server')]")
        mutual_servers_button.click()
        time.sleep(2)

        mutual_servers = []
        mutual_servers_list = driver.find_elements(By.CLASS_NAME, "listRow__9d78f")
        for server in mutual_servers_list:
            name_elem = server.find_element(By.CLASS_NAME, "info_f4bc97")
            mutual_servers.append(name_elem.text)

        # Store the data
        friend_data[friend_name] = {
            "mutual_friends": mutual_friends,
            "mutual_servers": mutual_servers,
        }

        # Close profile (Escape key)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)

    # now we scroll down to get more friends, rerun the friends element extractor and remove duplicates
    # scroll
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for new content to load
    friends = driver.find_elements(By.CLASS_NAME, "peopleListItem_cc6179")
    for friend in friends:
        if friend in TotalFriends:
            friends.remove(friend)
        if len(friends) == 0:
            running = False



# Save data to JSON file
with open("discord_friends_data.json", "w") as f:
    json.dump(friend_data, f, indent=4)

print("Scraping complete! Data saved.")


