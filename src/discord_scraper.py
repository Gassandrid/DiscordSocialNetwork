from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import json

# check if user has environment variables set, and if not, prompt them to set them
if not os.getenv("DISCORD_EMAIL") or not os.getenv("DISCORD_PASSWORD"):
    print("Please set your Discord email and password as environment variables.")
    email = str(input("Enter your Discord email: "))
    password = str(input("Enter your Discord password: "))
else:
    email = str(os.getenv("DISCORD_EMAIL"))
    password = str(os.getenv("DISCORD_PASSWORD"))

# Set up Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Open in fullscreen
driver = webdriver.Chrome(options=options)

# Open Discord login page
driver.get("https://discord.com/login")

# Allow time for the page to load
time.sleep(2)

# get user credentials via environment variables
EMAIL = str(os.getenv("DISCORD_EMAIL"))
PASSWORD = str(os.getenv("DISCORD_PASSWORD"))

# Find and fill in email field
email_field = driver.find_element(By.NAME, "email")
email_field.send_keys(email)

# Find and fill in password field
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys(password)

# Submit login form
password_field.send_keys(Keys.RETURN)

# Wait for the home page to load
time.sleep(5)  # Adjust this based on your internet speed

# Click on "All" friends tab
all_friends_tab = driver.find_element(By.XPATH, "//div[contains(text(), 'All')]")
all_friends_tab.click()
time.sleep(1)  # Wait for the friend list to load

running = True
friend_data = {}

# because not al lthe friends are loaded at once, we need to scroll down and get more friends.
# aka we load the friends, scroll, load friends and remove duplicates, and continue until we have all the friends.
# returns a dictionary --> Key: friend name, Value: {"mutual_friends": [list of mutual friends], "mutual_servers": [list of mutual servers]}
def load_existing_data():
    try:
        with open("friends.json", "r") as infile:
            return json.load(infile)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_json(data):
    json_object = json.dumps(data, indent=4)
    with open("friends.json", "w") as outfile:
        outfile.write(json_object)

def parse_friends():
    running = True
    output = load_existing_data()  # Load existing data if any
    TotalFriends = []
    scroller = driver.find_element(By.CLASS_NAME, "peopleList__5ec2f")

    # Scroll in smaller increments
    current_height = 0
    scroll_increment = 400  # Scroll 200 pixels at a time
    max_height = driver.execute_script("return arguments[0].scrollHeight", scroller)

    while running:
        friends = driver.find_elements(By.CLASS_NAME, "peopleListItem_cc6179") 
        friends_to_check = []
        # if not in TotalFriends, add to TotalFriends
        for friend in friends:
            if friend not in TotalFriends:
                TotalFriends.append(friend)
                # add to friends to check
                friends_to_check.append(friend)

        
        # for each friend, get the name, right click, open profile, get mutual friends, get mutual servers, store data, close profile
        for friend in friends_to_check:

            # Extract friend's name - using the correct Discord username class
            #username__0a06e
            friend_name_elem = friend.find_element(By.CLASS_NAME, "username__0a06e")
            time.sleep(.2)

            # right click and open profile
            ActionChains(driver).context_click(friend).perform()
            time.sleep(.2)

            # now context is open, click profile button item_c1e9c4
            profile_option = driver.find_element(By.XPATH, "//div[contains(text(), 'Profile')]")
            ActionChains(driver).click(profile_option).perform()
            time.sleep(.3)

            # click mutual Friends
            mutual_friends_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Mutual Friend')]")
            ActionChains(driver).click(mutual_friends_button).perform()
            time.sleep(.2)

            # Find the profile modal first
            profile_modal = driver.find_element(By.XPATH, "//div[@aria-label='User Profile Modal']")
            
            # Get mutual friends within the modal context
            info_elems = profile_modal.find_elements(By.CLASS_NAME, "info_f4bc97")
            names = [elem.text for elem in info_elems]
            print(names)
            time.sleep(.2)

            # click the mutual servers button
            servers_button = profile_modal.find_element(By.XPATH, ".//div[contains(text(), 'Mutual Server')]")
            ActionChains(driver).click(servers_button).perform()
            time.sleep(.2)

            # values are in the same format as mutual friends, but search within modal
            server_elems = profile_modal.find_elements(By.CLASS_NAME, "listName__9d78f")
            servers = [elem.text for elem in server_elems]
            print(servers)
            time.sleep(.2)

            # the first output of the names and server mutals are the actual users name, so we remove them
            names.pop(0)
            # add all the data to the output
            # output = {friend_name: {"mutual_friends": names, "mutual_servers": servers}}
            output[friend_name_elem.text] = {"mutual_friends": names, "mutual_servers": servers}
            # clear the names and servers
            names = []
            servers = []

            # press escape to close the profile
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(.2)

        time.sleep(.2)

        # Save the current progress after processing each batch of friends
        save_json(output)
        print(f"Saved progress... Current friend count: {len(output)}")

        if current_height < max_height:
            current_height += scroll_increment
            driver.execute_script(f"arguments[0].scrollTo(0, {current_height});", scroller)
            time.sleep(1)  # Wait a bit between each scroll
        else:
            running = False

    return output

# Run the scraper and get the final list
final_list = parse_friends()
print("Scraping completed!")
print(f"Total friends processed: {len(final_list)}")
