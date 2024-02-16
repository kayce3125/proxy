import random
import time
import platform
import socket
import requests
import pycountry
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Define the maximum number of clicks/taps per page
MAX_CLICKS_PER_PAGE = 3
# Define session duration (in seconds)
SESSION_DURATION = random.randint(180, 300)

def generate_screen_resolutions(num_resolutions):
    resolutions = set()
    while len(resolutions) < num_resolutions:
        width = random.randint(800, 3840)  # Random width between 800 and 3840 pixels
        height = random.randint(600, 2160)  # Random height between 600 and 2160 pixels
        resolutions.add((width, height))
    return resolutions

def get_random_user_agent():
    # Generate a random user agent using the fake-useragent library
    return UserAgent().random

def get_random_connection_type():
    # Sample connection types
    connection_types = ["WiFi", "Ethernet", "4G", "3G", "2G"]
    return random.choice(connection_types)

def get_random_ip_address():
    # Generate a random IP address (IPv4) for simulating different users
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

def visit_website(proxy, website_url):
    device_info = get_device_info()
    user_agent = device_info["user_agent"]
    ip_address = device_info["ip_address"]
    screen_resolution = device_info["screen_resolution"]
    browser_type = device_info["browser_type"]

    # Simulate visiting the website with the given proxy and device information
    print(f"Visiting website {website_url} using proxy: {proxy} and device info: {device_info}")

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument(f"--window-size={screen_resolution[0]}x{screen_resolution[1]}")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation features to avoid detection

    # Change the path below to your chromedriver path
    driver = webdriver.Chrome(executable_path='C:\\Users\\HP\\Desktop\\chrome', options=options)


    # Simulate scrolling up and down on the page
    def scroll():
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        scroll_amount = random.randint(200, 400)
        for _ in range(scroll_height // scroll_amount):
            driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
            time.sleep(random.uniform(0.5, 1.5))

    # Simulate clicking or tapping on links/buttons
    try:
        driver.get(website_url)  # Visit the provided website URL
        time.sleep(random.uniform(5, 10))  # Simulate initial wait time

        # Start session timer
        start_time = time.time()
        while time.time() - start_time < SESSION_DURATION:
            scroll()  # Simulate scrolling up and down
            time.sleep(random.uniform(3, 5))  # Simulate waiting time between scrolls

            # Find all clickable elements on the page
            clickable_elements = driver.find_elements(By.XPATH, "//a | //button")

            if clickable_elements:
                # Randomly click or tap on an element
                random.choice(clickable_elements).click()
                time.sleep(random.uniform(3, 5))  # Simulate waiting time after click
            else:
                break  # Break if no clickable elements found

    finally:
        driver.quit()  # Make sure to quit the browser session to release resources

def get_device_info():
    # Get device information
    device_type = "Desktop" if platform.system() == "Windows" else "Mobile"
    operating_system = platform.system() + " " + platform.release()
    device_model = platform.machine()
    screen_resolution = get_screen_resolution(device_type)

    # Get browser information
    user_agent = get_random_user_agent()
    browser_info = user_agent.split("(")[1].split(")")[0]
    browser_type, browser_version = browser_info.split(";")

    # Get language settings
    language_settings = pycountry.languages.get(alpha_2='en').name

    # Get connection type
    connection_type = get_random_connection_type()

    # Get IP address
    ip_address = get_random_ip_address()

    return {
        "device_type": device_type,
        "operating_system": operating_system,
        "device_model": device_model,
        "screen_resolution": screen_resolution,
        "browser_type": browser_type.strip(),
        "browser_version": browser_version.strip(),
        "language_settings": language_settings,
        "connection_type": connection_type,
        "ip_address": ip_address,
        "user_agent": user_agent
    }

def get_screen_resolution(device_type):
    # Generate millions of unique screen resolutions
    resolutions = generate_screen_resolutions(10000000)

    # Randomly select a resolution from the generated resolutions based on device type
    if device_type == "Desktop":
        return random.choice(list(resolutions))
    else:
        return random.choice(list(resolutions))

def main():
    website_url = input("Enter the website URL: ")
    num_visits = int(input("Enter the number of visits: "))

    try:
        with open("proxies.txt", "r") as file:
            proxies = file.readlines()
            total_proxies = len(proxies)
            visited_proxies = set()

            while len(visited_proxies) < total_proxies:
                proxies_to_visit = random.sample(proxies, min(num_visits, total_proxies - len(visited_proxies)))

                for proxy in proxies_to_visit:
                    visit_website(proxy.strip(), website_url)
                    visited_proxies.add(proxy.strip())
                    print(f"Visited proxies: {visited_proxies}")

    except FileNotFoundError:
        print("Error: File 'proxies.txt' not found.")

if __name__ == "__main__":
    main()
