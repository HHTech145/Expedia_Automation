from time import sleep
# from .base import Base
# from .scroller import Scroller
# import threading
import undetected_chromedriver as uc
# import undetected_chromedriver.v2 as uc
import json
# from pyvirtualdisplay import Display
import traceback
import pandas as pd
# from .settings import DRIVER_EXECUTABLE_PATH
# from .communicator import Communicator
import re
from urllib.parse import urlencode, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.common.exceptions import JavascriptException
from common import Common
from selenium.common.exceptions import NoSuchElementException,TimeoutException,InvalidSelectorException,StaleElementReferenceException,ElementClickInterceptedException
from data import JsonDataHandler

#Database
from Database.connector import Database
from Database.image_downloader import HotelImageDownloader
##########

class ExpediaUrlGenerator:
    def __init__(self, destination, check_in, check_out, adults, rooms, sort="RECOMMENDED"):
        # Initialize instance variables
        self.destination = destination
        self.check_in = check_in
        self.check_out = check_out
        self.adults = adults
        self.rooms = rooms
        self.sort = sort

    def generate_url(self):
        # Generate the Expedia URL using instance variables
        base_url = "https://www.expedia.com/Hotel-Search"
        url = (
            f"{base_url}?adults={self.adults}&rooms={self.rooms}&destination={self.destination},"
            f"&startDate={self.check_in}&endDate={self.check_out}&regionId=1079"
            f"&theme=&userIntent=&semdtl=&useRewards=true&sort={self.sort}"
        )
        return url




class WebDriverManager():
    

    def __init__(self,healdessmode):
        """
        params:

        search query: it is the value that user will enter in search query entry 
        outputformat: output format of file , selected by user
        outputpath: directory path where file will be stored after scraping
        headlessmode: it's value can be 0 and 1, 0 means unchecked box and 1 means checked

        """
        # self.output_file_name=output_file_name

        # self.searchquery = searchquery  # search query that user will enter
        
        # it is a function used as api for transfering message form this backend to frontend

        self.headlessMode = healdessmode
        self.__allResultsLinks=[]
        self.init_driver()
        # self.scroller = Scroller(driver=self.driver,output_file_name=self.output_file_name)



    def init_driver(self):
        options = uc.ChromeOptions()
        if self.headlessMode:
                options.headless = True
        options = uc.ChromeOptions()
        # options.add_argument("--headless=new")  # Enable headless mode
        options.add_argument("--disable-gpu")  # Disable GPU (optional)
        options.add_argument("--no-sandbox")  # Avoid sandboxing issues
        options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues
        # options.add_argument("--start-maximized")  # Open browser in maximized mode
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--window-size=1920,1080")
        # options.add_argument("--headless")  # Run headless to avoid UI display
        # options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent automation detection
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        # adding argument to disable the AutomationControlled flag 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        
        # exclude the collection of enable-automation switches 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        
        # turn-off userAutomationExtension 
        options.add_experimental_option("useAutomationExtension", False) 

        # Optional: Specify Chrome executable path if needed
        # browser_executable_path = "chromedriver.exe"
        browser_executable_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

        # Initialize undetected-chromedriver
        self.driver = uc.Chrome(options=options, browser_executable_path=browser_executable_path)
        # driver = uc.Chrome(options=options, use_subprocess=False)  # Disable patching
        # DRIVER_EXECUTABLE_PATH="chromedriver.exe"
        # try:
        #     if DRIVER_EXECUTABLE_PATH is not None:
        #         self.driver = uc.Chrome(
        #             driver_executable_path=DRIVER_EXECUTABLE_PATH, options=options)
        #     else:
        #         self.driver = uc.Chrome(options=options)

        # except NameError:
        #     self.driver = uc.Chrome(options=options)

        # print("version --------------",uc.get_chrome_version())
        # Communicator.show_message("Opening browser...")
        self.driver.maximize_window()
        # self.driver.implicitly_wait(self.timeout)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    def open_site(self,url):
        # url="https://www.expedia.com/" 
        print("url --------------------------",url)
        self.driver.get(url)
        # self.driver.execute_script("document.body.style.zoom='50%'")
        sleep(10)

    def click_send_destination(self):
                # Wait until the element is clickable
        # Check if the element is inside an iframe and switch to it
        sleep(5)
        # element = self.driver.find_element(By.XPATH,'//button[@data-stid="destination_form_field-dialog-trigger"]')
        # self.driver.execute_script("arguments[0].scrollIntoView();", element)


        location_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-stid="destination_form_field-dialog-trigger"]'))
        )
        location_button.click()
        print("Button clicked successfully!")
                    # Wait until the button is visible
        # Explicitly wait for the button to be clickable
        # button = WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-stid="destination_form_field-dialog-trigger"]'))
        # )

        # button.click()
        # sleep(3000)
        # If the element is inside an iframe, switch to the iframe first

                # Click on the "Where to?" button (location field)
        # Wait until the "Where to?" button is clickable
        # location_button = WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-stid="destination_form_field-dialog-trigger"]'))
        # )
        

        # Wait for any actions to complete, you can adjust the sleep time based on your page load times
        # sleep(2000)


    def sign_in(self):
        try:
            # Wait until the button is available (optional but recommended)
            self.driver.implicitly_wait(10)

            # Locate the button by its class and text
            button = self.driver.find_element(By.XPATH, "//a[contains(@class, 'uitk-button-primary') and contains(text(), 'Sign in, it')]")
            
            # Scroll to the button if it's not in view
            ActionChains(self.driver).move_to_element(button).perform()

            # Click the button
            button.click()
                # Wait for the element to load (optional but useful for dynamic pages)
            self.driver.implicitly_wait(10)
            print("Button clicked successfully!")
            # Locate the email input field by its ID
            email_input = self.driver.find_element(By.ID, "loginFormEmailInput")
            # Send email into the input field
            email_input.send_keys("aihtech508@gmail.com")  # Replace with your email
            print("Email entered successfuly !!!!!!!!!!!!!!!!!!!!!!!")
            
                        # Locate the 'Continue' button by ID and click it
            continue_button = self.driver.find_element(By.ID, "loginFormSubmitButton")
            continue_button.click()
            print("Continue button clicked successfully!")
            # Locate the 'Enter password instead' button by ID and click it
            password_button = self.driver.find_element(By.ID, "passwordButton")
            password_button.click()
            print("use password button clicked successfully!")

                        # Wait for the page to load (if necessary)
            self.driver.implicitly_wait(10)

            # Locate the password input field by ID
            password_field = self.driver.find_element(By.ID, "enterPasswordFormPasswordInput")

            # Enter the password
            password = "Htech786#"  # Replace with the actual password
            password_field.send_keys(password)
            print("enter password sucessfully !!!")

                        # Locate the "Sign in" button by ID and click it
            # sign_in_button = self.driver.find_element(By.ID, "enterPasswordFormSubmitButton")
            # sign_in_button.click()
            # sign_in_button = self.driver.find_element(By.ID, "enterPasswordFormSubmitButton")
            # self.driver.execute_script("arguments[0].click();", sign_in_button)

            self.click_on_Sign_in_button()

            print("Clicked the Sign in button successfully!")
        except Exception as e:
            print("An error occurred:", e)

    def click_on_Sign_in_button(self):
        # Max retries
        MAX_RETRIES = 5

        for attempt in range(MAX_RETRIES):
            try:
                # Find the "Sign in" button
                sign_in_button = self.driver.find_element(By.ID, "enterPasswordFormSubmitButton")
                
                # Click the button using JavaScript
                self.driver.execute_script("arguments[0].click();", sign_in_button)
                
                # Wait for the "Skip for now" button to appear
                skip_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[text()='Skip for now']"))
                )
                
                # Click the "Skip for now" button
                self.driver.execute_script("arguments[0].click();", skip_button)
                print("Sign-in successful and 'Skip for now' button clicked!")
                break  # Exit the loop if successful
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                
                # Check if it's the last attempt
                if attempt == MAX_RETRIES - 1:
                    print("Max retries reached. Unable to sign in.")
                    raise
                
                # Wait before retrying
                sleep(2)

    def get_hote_details(self):
        sleep(5)
                # Locate the div and get its outer HTML
        div_element = self.driver.find_element(By.CSS_SELECTOR, ".uitk-layout-grid")  # Target the div using the class
        outer_html = div_element.get_attribute('outerHTML')

        # Parse the outer HTML using BeautifulSoup
        soup = BeautifulSoup(outer_html, 'html.parser')

        # Extract the link (assuming it's the anchor tag you mentioned)
        link = soup.find('a', {'class': 'uitk-card-link'})  # Adjust based on your HTML structure
        if link:
            url = link.get('href')
            full_url = "https://www.expedia.com" + url  # Prepend the base URL
            print("Extracted URL:", full_url)

    def extract_hotel_links(self):
        """Extract hotel links from the Expedia search results page."""
        # Wait for the page to load completely (adjust timeout as needed)
        sleep(5)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the hotel links to be present
        wait = WebDriverWait(self.driver, 20)  # Adjust timeout as needed
        # Find all hotel result cards
        hotel_cards = self.driver.find_elements(By.CSS_SELECTOR, ".uitk-card[data-stid='lodging-card-responsive']")
        # hotel_cards = wait.until(
        #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".uitk-card[data-stid='lodging-card-responsive']"))
        # )
        all_links = []
        for card in hotel_cards:
            # Get the outer HTML of each card
            outer_html = card.get_attribute('outerHTML')

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(outer_html, 'html.parser')

            # Find the anchor tag within the card
            link_tag = soup.find('a', {'class': 'uitk-card-link'})

            if link_tag:
                # Extract the href attribute
                href = link_tag.get('href')
                if href:
                    # Form the full URL by prepending the base URL
                    full_url = "https://www.expedia.com" + href
                    all_links.append(full_url)

        # Print all extracted links (for debugging)
        print(f"Extracted {len(all_links)} hotel links:")
        # for link in all_links:
        #     print(link)

        return all_links

    def scroll(self):
        """Scroll through the page to collect all hotel result URLs from Expedia."""
        # Find the scrollable area on Expedia's search result page
        scrollAbleElement = self.driver.execute_script(
            """return document.querySelector(".main-region")"""
        )
        
        if scrollAbleElement is None:
            print("We are sorry but, No results found for your search query on Expedia.")
            return []

        last_height = 0

        while True:
            # Check if the thread is closed (used to safely exit the scroll loop)
            if Common.close_thread_is_set():
                self.driver.quit()
                return []

            # Refind the scrollable element to avoid StaleElementReferenceException
            scrollAbleElement = self.driver.execute_script(
                """return document.querySelector(".main-region")"""
            )

            # Perform the scroll action
            self.driver.execute_script(
                "arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollAbleElement
            )
            sleep(2)  # Wait for the page to load new content

            # Check the new scroll height to see if the page has finished loading
            new_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", scrollAbleElement
            )

            if new_height == last_height:
                # If the height hasn't changed, we've reached the end of the list
                script = """
                const endingElement = document.querySelector(".uitk-button .uitk-button-secondary");
                return endingElement;
                """
                endAlertElement = self.driver.execute_script(script)  # Check if we're at the end

                if endAlertElement is None:
                    # If not at the end, try clicking a result to trigger further loading
                    try:
                        self.driver.execute_script(
                            "array = document.getElementsByClassName('uitk-card-link'); array[array.length-1].click();"
                        )
                    except JavascriptException:
                        pass
                else:
                    # We've reached the end of the list
                    break
            else:
                # Update the last height for the next iteration
                last_height = new_height

                # Parse the new content loaded by scrolling
                allResultsListSoup = BeautifulSoup(
                    scrollAbleElement.get_attribute('outerHTML'), 'html.parser'
                )

                # Extract all hotel result div elements (adjusting the selector)
                div_elements = allResultsListSoup.find_all('div', class_='uitk-layout-grid')  # Adjust class if needed
                print("length of elements----",len(div_elements))
                # Collect all the URLs from anchor tags inside each div element
                # self.__allResultsLinks = []
                for div_element in div_elements:
                    link = div_element.find('a', class_='uitk-card-link')  # Adjust based on your HTML structure
                    if link:
                        url = link.get('href')
                        full_url = "https://www.expedia.com" + url  # Prepend the base URL
                        self.__allResultsLinks.append(url)

                # Optionally print how many locations have been scrolled
                print(f"Total locations scrolled: {len(self.__allResultsLinks)}")
                print("Hotels ________________________________________", self.__allResultsLinks)

        return self.__allResultsLinks

    def room_amenities(self):
        amenities={}
        try:
            # Locate the parent container dynamically
            parent_xpath = '//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div'
            parent_elements = self.driver.find_elements(By.XPATH, parent_xpath)
            print(f"Found {len(parent_elements)} parent containers")
            
            for index, parent in enumerate(parent_elements):
                try:
                    # Locate child divs with the specific class under the current parent
                    amenities_elements = parent.find_elements(By.XPATH, './/div[contains(@class, "uitk-layout-grid-item")]')
                    print("len of grids --------:", len(amenities_elements))
                    if amenities_elements:
                        for element in amenities_elements:
                            # Split the text into lines
                            text_lines = element.text.split('\n')
                            if len(text_lines) > 1:
                                heading = text_lines[0]  # The first line is the heading
                                details = text_lines[1:]  # The rest are the amenities
                                amenities[heading] = details
                        print(amenities)
                        break  # Stop searching after finding the first valid set of amenities
                except Exception as e:
                    print(f"Error processing parent index {index} - {e}")
            return amenities
        except Exception as e:
            print(f"Failed to locate parent containers - {e}")

        # sleep(10000)

        # amenities_xpath='//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[4]/div/div'
                        
        # amenities_heading_xpath= '//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[4]/div/h3'
        # try:
        #     check_amenities= self.driver.find_element(By.XPATH, amenities_heading_xpath)
        #     # print("heading---------------------------",check_amenities.text)
        #     # if check_amenities.text != "Room amenities":
        #     #     amenities_xpath='//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[5]/div/div'
        # except Exception as e:
        #     print("no room amenities ")
        #     amenities_xpath='//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[5]/div/div'
        #     # continue

        # global amenities_elements  # Declare amenities_elements as global

        # xpaths = [
        #     '//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[4]/div/div',
        #     '//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[5]/div/div',
        #     '//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div/div[4]/div/div'
        #     # //*[@id="app-layer-room-info-201193233-3"]/section/div[3]/div/div[2]/div[5]/div/div
        #     # //*[@id="app-layer-room-info-323642409-3"]/section/div[3]/div/div[2]/div[5]/div/div
        # ]
        
        # for xpath in xpaths:
        #     try:
        #         amenities_elements = self.driver.find_element(By.XPATH, xpath)
        #         print("______________________________amenities ________________",amenities_elements)
        #         if amenities_elements:
        #             # for element in amenities_elements:
        #             #     print("Amenity:", element.text)
        #             break
        #     except Exception as e:
        #         print(f"XPath failed: {xpath} - {e}")

        # amenities_section=amenities_elements
        # # parent_xpath = '//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div'
        # # amenities_elements = self.driver.find_elements(By.XPATH, './/div[contains(@class, "uitk-layout-grid-item")]')




        # # amenities_xpath='//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div'
        # # amenities_section = self.driver.find_element(By.XPATH, amenities_xpath)
        # # uitk-heading uitk-heading-5 uitk-spacing uitk-spacing-margin-blockend-six
        # # print(amenities_section)
        # outer_html = amenities_section.get_attribute('outerHTML')


        # amenities_soup = BeautifulSoup(outer_html, 'html.parser') 

        # # print(amenities_soup.prettify())
        # # Find the grid that contains the list of amenities
        # # grid = amenities_soup.find('div', class_='uitk-layout-grid')

        # # Extract all the grid items
        # grid_items = amenities_soup.find_all('div', class_='uitk-layout-grid-item')

        # print("-------------------- grid items",len(grid_items),)
        # # Loop through each grid item to extract the headings and the amenities list
        
        # for item in grid_items:
        #     # uitk-heading uitk-heading-6 uitk-layout-flex-item
        #     heading = item.find('h4', class_='uitk-heading uitk-heading-6 uitk-layout-flex-item') #uitk-heading uitk-heading-6 uitk-layout-flex-item
        #     if heading:
        #         heading_text = heading.get_text(strip=True)
        #         # Find the list of amenities under this heading
        #         ul = item.find('ul')
        #         if ul:
        #             amenities_list = [li.get_text(strip=True) for li in ul.find_all('li')]
        #             amenities[heading_text] = amenities_list

        # return amenities

    def extract_features(self):
        # XPath to check for "Highlights"
        xpath_highlights = '//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div/div[2]/div/div/div/div'
        # XPath to get the features if "Highlights" text is found
        xpath_features = '//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div/div[2]/div/div/div/div'
        # '//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[2]/div/div/div[2]'
        # '//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div/div[2]/div/div/div/div'
        # //*[contains(@id, "app-layer-room-info")]
        try:
            # Find the element containing the text "Highlights"
            highlight_element = self.driver.find_element(By.XPATH, xpath_highlights)
            # Get the text content of the element
            highlight_text = highlight_element.text
            if "Highlights" in highlight_text:
                print("Highlights found. Now fetching features...")
                # Now find the second XPath to get the features
                feature_element = self.driver.find_element(By.XPATH, xpath_features)
                # Get the text content of the feature element and split into individual features
                features = feature_element.text.split()  # Adjust split method if necessary
                
                if features:
                    print("Found the following features:")
                    for feature in features:
                        print(feature)
                    return features
                else:
                    print("No features found.")
            else:
                print("No 'Highlights' text found.")
                # Use the fallback XPath to get the features
                feature_element_fallback = self.driver.find_element(By.XPATH, xpath_highlights)
                # Get the text content of the feature element and split into individual features
                features_fallback = feature_element_fallback.text.split()  # Adjust split method if necessary
                if features_fallback:
                    print("Found the following features (Highlights absent):")
                    for feature in features_fallback:
                        print(feature)
                    return features_fallback
                else:
                    print("No features found in fallback XPath.")
        except NoSuchElementException:
            print("Element NOT found.")

    def get_room_details(self):            
        try:
            # Find the element using its data-stid attribute
                # Wait for the element to be visible
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-stid="rooms-rates"]'))
            )
                    # data-stid="section-room-list"
            # Scroll to the element
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            sleep(2)
            action = ActionChains(self.driver)
            ################################## ROOMS ############################################
            # Step 1: Extract all room names from the page
            outer_html = element.get_attribute('outerHTML')
            soup = BeautifulSoup(outer_html, 'html.parser')  
            # print(soup.prettify())
            room_headings = soup.find_all('h3', class_='uitk-heading uitk-heading-6')
            print(room_headings)
            # Extract and strip the text from each heading and put it into room_names
            room_names = [heading.get_text(strip=True) for heading in room_headings]
            # room_names_elements = self.driver.find_elements(By.XPATH, "//h3[contains(@class, 'uitk-heading-6')]")
            # room_names = [room.text for room in room_names_elements]

            print("Room names ---------------------------------",room_names,type(room_names))
            # Step 2: Loop through room names and click "More details" for each room
            rooms = {}

            for room_name in room_names:
                print("Room name -----------------------------------------",room_name)
                # Construct dynamic XPath for the "More details" button based on the room name
                # button_xpath = f"//button[.//span[contains(text(), 'More details for {room_name}')]]"
                button_xpath = f"//div[h3[contains(text(), '{room_name}')]]//button[span[text()='More details']]"
                try:
                    # Find and click the "More details" button
                    # button = self.driver.find_element(By.XPATH, button_xpath)
                    # button.click()
                    print("button_xpath---------------------------------------------------------",button_xpath)
                    button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                    # self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    button.click()
                    print(f"Clicked 'More details' for {room_name}")
                    ########################################
                    wait = WebDriverWait(self.driver, 10)
                    # popup_section = self.driver.find_element(By.XPATH, "//section[contains(@class, 'uitk-centered-sheet')]")
                    popup_section = wait.until(EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'uitk-centered-sheet')]")))
                    print("Element found:", popup_section)

                    # div_element = self.driver.find_element(By.CSS_SELECTOR, "uitk-spacing uitk-spacing-padding-large-inlineend-three")  # Target the div using the class
                    outer_html = popup_section.get_attribute('outerHTML')


                    room_soup = BeautifulSoup(outer_html, 'html.parser')                    

                    # Extract the room name from the popup
                    popup_room_name = room_soup.find('h3', class_='uitk-heading-5').text

                    print("popup_room_name------------------------------",popup_room_name)

                    # Assuming you have already navigated to the correct page and the elements are present
                    # features_container = self.driver.find_element(By.XPATH, "//div[contains(@class, 'uitk-layout-flex uitk-layout-flex-gap-two uitk-layout-flex-flex-wrap-wrap')]")

                    # Find all child div elements with class 'uitk-text' within this container
                    # feature_container = self.driver.find_element(By.XPATH, '//*[@id="app-layer-room-info-230733352-1"]/section/div[3]/div/div[2]/div[2]/div/div/div/div')
                    # print(features_container,feature_elements)
                    # Create an empty list to store feature names
                    features = self.extract_features()
                    print("features ----------------------------------------------------", features)                    
                    # element = self.driver.find_element(By.CSS_SELECTOR,"uitk-spacing uitk-spacing-margin-block-four")
                    # room_Detail_div= room_soup.find('div',class_='//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[3]/ul')
                    # xpath_room_detail='//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[3]/ul'
                    # xpath_room_detail='//*[contains(@id, "app-layer-room-info")]//ul'
                    xpath_room_detail = '//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div/div[3]//ul[@role="list" and contains(@class, "uitk-typelist")]'

                    # //*[@id="app-layer-room-info-323642411-6"]/section/div[3]/div/div/div[3]/ul
                    # room_Detail_div=self.driver.find_element(By.XPATH, xpath_room_detail)
                    # Find all the list items in the provided HTML
                    # list_items = room_Detail_div.text.split()

                    li_texts=[]
                    # print(room_detail_soup.prettify())
                    # Get all <li> elements inside the <ul>
                    # Wait for the elements to be present and interactable before proceeding
                    wait = WebDriverWait(self.driver, 10)

                    # Retry logic to handle StaleElementReferenceException
                    for attempt in range(3):  # Retry up to 3 times
                        try:
                            # Wait until all <li> elements are present
                            li_elements = wait.until(
                                EC.presence_of_all_elements_located((By.XPATH, xpath_room_detail + '/li'))
                            )
                            
                            # Extract the text from each <li> element and store it in a list
                            li_texts = [li.text for li in li_elements]
                            print("Room details:", li_texts)
                            break  # If successful, break the loop
                            
                        except StaleElementReferenceException:
                            # Handle the exception by retrying
                            print(f"Stale element exception occurred. Retrying {attempt + 1} of 3.")
                            continue  # Retry if an element is stale
                    # list_items= 
                    # print("list_items ------------------------------------------------------",list_items)
                    # Find the div containing the heading 'Room amenities'
                    # amenities_xpath='//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[4]/div/div'
                    # amenities_heading_xpath= '//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[4]/div/h3'
                    # try:
                    #     check_amenities= self.driver.find_element(By.XPATH, amenities_heading_xpath)
                    #     print("heading---------------------------",check_amenities.text)
                    #     if check_amenities.text != "Room amenities":
                    #         amenities_xpath='//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[5]/div/div'
                    # except Exception as e:
                    #     print("no room amenities ")
                    #     amenities_xpath='//*[contains(@id, "app-layer-room-info")]/section/div[3]/div/div[2]/div[5]/div/div'
                    #     # continue

                    # amenities_section = self.driver.find_element(By.XPATH, amenities_xpath)
                    # # uitk-heading uitk-heading-5 uitk-spacing uitk-spacing-margin-blockend-six
                    # # print(amenities_section)
                    # outer_html = amenities_section.get_attribute('outerHTML')


                    # amenities_soup = BeautifulSoup(outer_html, 'html.parser') 
                    # # print(amenities_soup.prettify())
                    # # Find the grid that contains the list of amenities
                    # # grid = amenities_soup.find('div', class_='uitk-layout-grid')

                    # # Extract all the grid items
                    # grid_items = amenities_soup.find_all('div', class_='uitk-layout-grid-item')

                    # # Loop through each grid item to extract the headings and the amenities list
                    # amenities = {}
                    # for item in grid_items:
                    #     heading = item.find('h4', class_='uitk-heading uitk-heading-6 uitk-layout-flex-item') #uitk-heading uitk-heading-6 uitk-layout-flex-item
                    #     if heading:
                    #         heading_text = heading.get_text(strip=True)
                    #         # Find the list of amenities under this heading
                    #         ul = item.find('ul')
                    #         if ul:
                    #             amenities_list = [li.get_text(strip=True) for li in ul.find_all('li')]
                    #             amenities[heading_text] = amenities_list

                    # # Print the extracted amenities
                    # for heading, items in amenities.items():
                    #     print(f"{heading}:")
                    #     for item in items:
                    #         print(f"  - {item}")
                    amenities = self.room_amenities()
                    print("amenities_--------------------",room_name,'-------------------------------',amenities)
                    # Extract the text from each list item and store in a dictionary
                    # room_details = {
                    #     "room_details": [item.get_text(strip=True) for item in list_items]
                    # }

                                    # Locate the main price summary div
                    price_summary_div = room_soup.find('div', {'data-stid': 'price-summary'})

                    # Extract data
                    price_detail = {}

                    if price_summary_div:
                        # Current price
                        current_price = price_summary_div.find('div', class_='uitk-text uitk-type-500 uitk-type-medium uitk-text-emphasis-theme')
                        price_detail['current_price'] = current_price.text if current_price else None
                        
                        # Original price
                        original_price = price_summary_div.find('div', class_='uitk-text uitk-type-300 uitk-text-default-theme')
                        price_detail['original_price'] = original_price.text.strip('$') if original_price else None

                        # Total price
                        total_price = price_summary_div.find('div', class_='uitk-text uitk-type-start uitk-type-200 uitk-text-default-theme', text=lambda t: '$' in t)
                        price_detail['total_price'] = total_price.text if total_price else None

                        # Additional info
                        includes_text = price_summary_div.find('div', text='includes taxes & fees')
                        price_detail['includes_taxes_and_fees'] = True if includes_text else False

                    print("Price details -----------------------------------------------------",price_detail)
                    # sleep(4000)

                    # images = room_soup.find_all('img', class_='uitk-image-media')

                    # print(" images of room ", len(images),images[0])
                    # sleep(4000)

                    # Store in a dictionary
                    rooms[popup_room_name] = {
                        'highlights': features,
                        'room_details': li_texts,
                        'amenities_list': amenities,
                        'price_detail':price_detail
                    }
                    # room_details = {
                    #     'room_name': popup_room_name,
                    #     'highlights': features,
                    #     "room_details": li_texts,
                    #     "amenities_list":amenities
                    # }
                    
                    # print(f"Room Details for {room_name}: {room_details}")
                    # Wait for the page to update after clicking the button
                    sleep(2)
                    
                
                except TimeoutException:
                    # print(f"TimeoutException: Could not find or click the button using XPath: {button_xpath}")
                    print(traceback.format_exc())
                    self.driver.save_screenshot("timeout_debug.png")
                    continue
                    # sleep(100000)
                
                except Exception as e:
                    print(f"Error clicking 'More details' for {room_name}: {e}")
                    print(traceback.format_exc())
                    action.send_keys(Keys.ESCAPE).perform()
                    # sleep(1000)
                    continue
                
                action.send_keys(Keys.ESCAPE).perform()
                sleep(2)

            # # Locate the parent element with data-stid="section-room-list"
            # parent_element = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, 
            #         'div[data-stid="section-room-list"].uitk-spacing.uitk-spacing-margin-block-three'))
            # )
            # # print("Parent element found:", parent_element)

            # # Get the outerHTML of the parent element
            # outer_html = parent_element.get_attribute('outerHTML')

            # # Parse the outerHTML with BeautifulSoup
            # soup = BeautifulSoup(outer_html, 'html.parser')

            # # Find all child divs with the specified class and a data-stid that starts with 'property-offer-'
            # offer_divs = soup.find_all('div', class_='uitk-layout-flex uitk-layout-flex-block-size-full-size uitk-layout-flex-flex-direction-column uitk-layout-flex-justify-content-space-between uitk-card uitk-card-roundcorner-all uitk-card-has-border uitk-card-has-overflow uitk-card-has-primary-theme',
            #                         attrs={'data-stid': lambda x: x and x.startswith('property-offer-')})

            # print(f"Found {len(offer_divs)} divs with data-stid starting with 'property-offer-'.")
            # for index, room_div in enumerate(offer_divs):
            #     # print(f"Div {index + 1}:")
            #     # print(div.prettify())
            #     # Extract room name and details
            #     room_name = room_div.find('h3', class_='is-visually-hidden').get_text(strip=True)  # Room name from the <h3> tag
            #     room_details = room_div.find('button', {'aria-label': True})['aria-label']  # Room details from the button's aria-label

            #     # Find all image elements with the class 'uitk-image-media'
            #     images = room_div.find_all('img', class_='uitk-image-media')

            #     # Extract the 'src' attribute from each image tag
            #     image_sources = [img['src'] for img in images]

            #     # Print room name, details, and image sources
            #     print(f"Room Name: {room_name}")
            #     print(f"Room Details: {room_details}")
            #     print("Image Sources:")
            #     for src in image_sources:
            #         print(src)

            return rooms
        except Exception as e:
            print("Error:", str(e))

    # Define a function for slow scrolling
    # Define a function for slow scrolling within the modal
    def slow_scroll_modal(self,modal_element, scroll_pause=0.05, step=100):
        """
        Slowly scrolls within a modal element.

        :param modal_element: The modal element to scroll
        :param scroll_pause: Time to pause between scrolls in seconds (smaller for faster scrolling)
        :param step: Pixels to scroll in each step (larger for faster scrolling)
        """
        # Get the current and total scroll height of the modal
        current_scroll = 0
        total_scroll_height = self.driver.execute_script("return arguments[0].scrollHeight", modal_element)

        while current_scroll < total_scroll_height:
            # Scroll down by step pixels
            self.driver.execute_script(f"arguments[0].scrollTop += {step}", modal_element)
            sleep(scroll_pause)  # Pause to create smooth scrolling
            current_scroll += step


    def get_hotel_photos(self):
        try:
            
            # Click to open the gallery
            x_path = "//*[@id='Overview']//div//figure//button"
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, x_path))
            )
            button.click()

            sleep(5)

            # Locate the pop-up or modal section
            modal_xpath = "//section[@class='uitk-centered-sheet uitk-centered-sheet-xxxlarge uitk-sheet uitk-centered-sheet-medium']"



            modal_content = self.driver.find_element(By.CLASS_NAME, "uitk-sheet-content")
            # Scroll slowly to the bottom of the modal
            self.slow_scroll_modal(modal_content, scroll_pause=0.05, step=100)

            print("Scrolling completed ##########$$$$$$$------------------------------------------------------------------------")


            # # Scroll to the bottom
            # self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_content)

            # # Pause to allow lazy-loaded images to load
            # sleep(5)

            # # Optional: Scroll up and down to trigger more loading if required
            # for _ in range(3):
            #     self.driver.execute_script("arguments[0].scrollTop -= 50", modal_content)
            #     sleep(1)
            #     self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_content)
            #     sleep(1)

            # print("Scrolling complete.")

            # sleep(40000)

            #######################
            # Wait for the gallery element to load
            element_xpath = '//*[@id="app-layer-thumbnail-gallery"]//ul'
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, element_xpath))
            )

            # Get the HTML content of the element
            element_html = element.get_attribute('outerHTML')

            # Parse with BeautifulSoup
            soup = BeautifulSoup(element_html, 'html.parser')

            # # Find the desired div using its attribute
            # div = soup.find_all('div', {'data-stid': 'image-thumbnail-view-with-label'})

            # for i in div:
            #     # Locate the img tag inside the div
            #     mg_tag = i.find('img', class_='uitk-image-media')

            #     print(mg_tag)
            images = soup.find_all('img', class_='uitk-image-media')
            
            print("Extracted images -----------------------------------------------------------------------)",len(images))

            # Extract image data
            images_data = {}
            for img in images:
                alt_text = img.get('alt', 'No description')  # Default alt text
                src_url = img.get('src', None)  # Default src as None
                if src_url:  # Only process valid src
                    images_data[alt_text] = {'src_url': src_url}

            print(images_data)

            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            # print(f"Extracted {len(images_data)} images.")
            return images_data

        except Exception as e:
            print(f"Error while fetching hotel photos: {e}")
            return {}


    def get_hotel_amenities(self):
        action = ActionChains(self.driver)
        # action = ActionChains(self.driver)
        
        # # # Wait for the div element to be present
        # div_element = WebDriverWait(self.driver, 20).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, ".uitk-spacing.uitk-spacing-padding-large-inlineend-three"))
        # )

        # # div_element = self.driver.find_element(By.CSS_SELECTOR, "uitk-spacing uitk-spacing-padding-large-inlineend-three")  # Target the div using the class
        # outer_html = div_element.get_attribute('outerHTML')


        # hotel_div = BeautifulSoup(outer_html, 'html.parser')
        # # print(hotel_div.prettify())
        # #     # Find the target div by its class
        # # # hotel_div = soup.find('div', class_='uitk-spacing uitk-spacing-padding-large-inlineend-three')

        # # Extract hotel details
        # if hotel_div:
        #     hotel_name = hotel_div.find('h1', class_='uitk-heading uitk-heading-3').text.strip() if hotel_div.find('h1', class_='uitk-heading uitk-heading-3') else None

        #     # Extract hotel rating
        #     hotel_rating_meta = hotel_div.find('meta', itemprop='ratingValue')
        #     hotel_rating = hotel_rating_meta['content'] if hotel_rating_meta else None

        #     # Extract hotel description or other attributes
        #     hotel_description_meta = hotel_div.find('meta', itemprop='description')
        #     hotel_description = hotel_description_meta['content'] if hotel_description_meta else None

        #     # Extract latitude and longitude
        #     latitude_meta = hotel_div.find('meta', itemprop='latitude')
        #     latitude = latitude_meta['content'] if latitude_meta else None

        #     longitude_meta = hotel_div.find('meta', itemprop='longitude')
        #     longitude = longitude_meta['content'] if longitude_meta else None
        #     # Extract additional rating (out of 10)
        #     additional_rating = hotel_div.find('span', class_='uitk-badge-base-text').text.strip() if hotel_div.find('span', class_='uitk-badge-base-text') else None

        #     # Display the details
        #     # print(f"Hotel Name: {hotel_name}")
        #     # print(f"Hotel Rating (from meta): {hotel_rating}")
        #     # print(f"Additional Rating (out of 10): {additional_rating}")
        #     # print(f"Hotel Description: {hotel_description}")
        #     # print(f"Latitude: {latitude}")
        #     # print(f"Longitude: {longitude}")
        # else:
        #     print("Hotel details not found.")

        try:
            # sleep(2)
            #         # Find the button using the aria-label attribute
            # button = self.driver.find_element(By.XPATH, "//button[@aria-label='See all property amenities']")
            ####################################
            button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'See all') and (contains(@aria-label, 'property amenities') or contains(@aria-label, 'about this property'))]")))
            
            # button.click()
            #####################################


            # Attempt to locate the button with either aria-label "See all property amenities" or "See all about this property"
            # button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'See all') and (contains(@aria-label, 'property amenities') or contains(@aria-label, 'about this property'))]")
            # Extract the 'aria-label' attribute
            aria_label = button.get_attribute("aria-label")
            print("Aria label -----------------------------------",aria_label)
            # Now you can click the button or perform other actions
            # button.click()
            # Click the button
            button.click()

            sleep(5)
            amenities={}
            if aria_label=="See all about this property":
                sleep(1)


                # div_element = self.driver.find_element(By.CSS_SELECTOR, "uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-columns uitk-layout-grid-display-grid")
                # Wait until the element is present
        
                div_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 
                        ".uitk-spacing.uitk-spacing-padding-inlinestart-six.uitk-spacing-padding-inlineend-six"))
                )
                print("Element found:", div_element)

                            
                # sleep(50000)
                # Get the outerHTML of the div
                outer_html = div_element.get_attribute('outerHTML')
                amenities_div = BeautifulSoup(outer_html, 'html.parser')
                print(amenities_div.prettify())
                # amenities={}
                # Find all the divs with the specified classes
                # Find all the divs with the specified class
                divs = amenities_div.find_all('div', class_='uitk-spacing uitk-spacing-padding-blockend-four')
                print("Number of divs found:", len(divs))

                # print("length of divs" ,len(divs))   
                sleep(5) 
                # Loop through each div to extract the heading and list items
                for div in divs:
                    # Try to get the heading element (either <h3> or <h4>)
                    heading = div.find('h4', class_='uitk-heading uitk-heading-6 uitk-layout-flex-item')
                    if heading:
                        heading_text = heading.text.strip()
                        print(f"Heading: {heading_text}")
                        
                        # Initialize an empty list to hold the items for this heading
                        list_items_text = []

                        # Get the ul element
                        ul = div.find('ul', class_='uitk-typelist uitk-typelist-orientation-stacked uitk-typelist-size-2')
                        if ul:
                            # Find all list items within the ul
                            list_items = ul.find_all('li', class_='uitk-spacing uitk-spacing-padding-blockstart-two uitk-spacing-padding-inline-eight')
                            for item in list_items:
                                # Find the <div> with the text inside the <li>
                                div_text = item.find('div', class_='uitk-text uitk-type-300 uitk-text-default-theme')
                                if div_text:
                                    item_text = div_text.text.strip()
                                    list_items_text.append(item_text)
                                    print(f"List item: {item_text}")
                                else:
                                    print("No div found with the specified class in list item.")

                        # Store the heading and list items in the dictionary
                        amenities[heading_text] = list_items_text

                        print("-" * 40)                
            else:
                sleep(1)
                    # Locate the div using its class name
                div_element = self.driver.find_element(By.CSS_SELECTOR, "div.uitk-sheet-content.uitk-spacing.uitk-spacing-padding-blockend-.uitk-sheet-content-padded")

                # Get the outerHTML of the div
                outer_html = div_element.get_attribute('outerHTML')
                amenities_div = BeautifulSoup(outer_html, 'html.parser')
                # print(amenities_div.prettify())
                # Print the outerHTML
                # print(outer_html)
                # Parse the HTML content
                # soup = BeautifulSoup(html_data, 'html.parser')
                # amenities={}
                # Find all the divs with the specified classes
                divs = amenities_div.find_all('div', class_='uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-columns-by-medium uitk-layout-grid-has-columns-by-large uitk-layout-grid-has-space uitk-layout-grid-display-grid uitk-spacing uitk-spacing-padding-blockend-three')
                # divs = amenities_div.find_all('div', class_=lambda class_list: all(c in class_list for c in ['uitk-layout-grid', 'uitk-layout-grid-has-auto-columns', 'uitk-layout-grid-has-columns-by-medium', 'uitk-layout-grid-has-columns-by-large']))

                print("length of divs" ,len(divs))
                # Loop through each div to extract the heading and list items
                for div in divs:
                    # Get the heading (h3 tag)
                    heading = div.find('h3', class_='uitk-heading')
                    if heading:
                        heading_text = heading.text.strip()
                        print(f"Heading: {heading_text}")
                        
                        # Initialize an empty list to hold the items for this heading
                        list_items_text = []

                        # Get the list items (li tags within the ul)
                        ul = div.find('ul', class_='uitk-typelist')
                        if ul:
                            list_items = ul.find_all('li', class_='uitk-typelist-item')
                            for item in list_items:
                                # Find the span with the specified classes inside the li
                                span = item.find('span', class_='uitk-text uitk-type-300 uitk-text-default-theme uitk-layout-flex-item')
                                if span:
                                    item_text = span.text.strip()
                                    list_items_text.append(item_text)
                                    print(f"List item: {item_text}")
                                else:
                                    print("No span found with the specified class.")
                        
                        # Store the heading and list items in the dictionary
                        amenities[heading_text] = list_items_text
                        
                        print("-" * 40)

            # Print the dictionary to verify the result
            print("Amenities Dictionary:", amenities)
            # close the amenities button
            action.send_keys(Keys.ESCAPE).perform()   

            return amenities
        except Exception as e:
            print(e)                 
    # Function to split place names and times
    def split_place_time(place_time_str):
        # Split by ' - ' and remove extra spaces
        name, time = place_time_str.split(' - ')
        return {"name": name.strip(), "time": time.strip()}

    def get_hotel_neighbourhood_data(self):
        # Locate the button using its attributes
        try:
            # neighbourhood= {}
            # Using aria-label
            button = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="See all about this area"]')
            # Click the button
            button.click()
            print("Button clicked successfully!")

            ############################ fetch data ####################################
            
            # Locate the specific div using its unique attribute
            poi_modal = self.driver.find_element(By.XPATH, "//div[@data-stid='poi-images-modal']")

            # Get the outer HTML of the located div
            outer_html = poi_modal.get_attribute('outerHTML')

            # Parse with BeautifulSoup
            soup = BeautifulSoup(outer_html, 'html.parser')
            print("##################################################")
            # print(soup.prettify())
            print("#####################################################")
            # Extract data
            poi_items = soup.find_all('div', class_='uitk-layout-grid-item')
            # print(poi_items[0].prettify())
            poi={}
            for item in poi_items:
                # Find the name and time by targeting the correct classes
                # Extract the name and time using more flexible searches based on their contents
                # Find the name and time by targeting the correct classes
                name_element = item.find('div', class_='uitk-text uitk-type-300 uitk-type-medium uitk-text-default-theme uitk-spacing uitk-spacing-padding-blockstart-two')
                time_element = item.find('div', class_='uitk-text uitk-type-200 uitk-text-default-theme uitk-spacing uitk-spacing-padding-blockstart-one')

                # Extract the name and time if found
                name = name_element.get_text(strip=True) if name_element else 'No name found'
                time = time_element.get_text(strip=True) if time_element else 'No time found'

                image = item.find('img')['src']
                print(f"Name: {name}, Time: {time}, Image: {image}")

                poi[name]={"name":name,"time":time,"image_url":image}

            # print()

            # Locate the specific section using its unique attribute
            location_section = self.driver.find_element(By.XPATH, "//section[@data-stid='location-modal-editorial']")

            # Get the outer HTML of the located section
            outer_html = location_section.get_attribute('outerHTML')

            # Parse with BeautifulSoup
            soup = BeautifulSoup(outer_html, 'html.parser')

            # Extract data
            geo_meta = soup.find('meta', itemprop='description')
            description = geo_meta['content'] if geo_meta else "No description available."

            print(f"Location Description: {description}")

            ###################################################################################
            div_element= self.driver.find_element(By.XPATH, '//*[@id="app-layer-PlacesSectionDialog"]/section/div[3]')
            # div_element
            
                    # Get the outer HTML of the located section
            outer_html = div_element.get_attribute('outerHTML')

            # Parse with BeautifulSoup
            soup = BeautifulSoup(outer_html, 'html.parser')


            # uitk-layout-flex uitk-layout-flex-gap-three uitk-spacing uitk-spacing-padding-blockstart-three uitk-spacing-padding-blockend-three

            # Find all divs with the specified class
            # divs = soup.find_all("div", class_="uitk-layout-flex uitk-layout-flex-gap-three uitk-spacing uitk-spacing-padding-block-three")
            divs = soup.find_all('div', class_=re.compile(r'uitk-layout-flex.*uitk-spacing.*'))

            print("##################",len(divs))
            # Loop through each div and extract its content
            neighbouthood_data={}

            

            for div in divs:
                # print("DIV CONTENT:")
                # print(div.get_text(separator="\n").strip())  # Extract text and clean up spacing
                # print("\n" + "-" * 50 + "\n")
                key=div.get_text(separator="\n").strip()
                # Split by newline and get the first line
                key = key.split('\n')[0]

                div_content = div.get_text(separator="\n").strip()
                # Split the text into individual restaurant names and walks
                restaurant_list = div_content.split('\n')[1:]  # Skip the first line (heading)
                
                if restaurant_list:
                    # Use the first restaurant name as the key
                    first_restaurant = restaurant_list[0].split(' - ')[0]

                    neighbouthood_data[key] = restaurant_list


            # Function to split place names and times
            def split_place_time(place_time_str):
                # Split by ' - ' and remove extra spaces
                name, time = place_time_str.split(' - ')
                return {"name": name.strip(), "time": time.strip()}

            # Iterate over the dictionary and apply the function
            for category, places in neighbouthood_data.items():
                neighbouthood_data[category] = [split_place_time(place) for place in places]

            # print("neighbourhood  data ",neighbouthood_data)


            neighbourhood={'poi':poi,'location_description':description,"places":neighbouthood_data}
            print("neighbourhood  data ",neighbourhood)
            sleep(2)
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            return neighbourhood
        except Exception as e:
            print(f"Error: {e}")
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    # Define a function to scroll and click the "Show more" button
    def scroll_and_click_show_more(self):
        while True:
            try:
                # Scroll to the bottom of the page
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait for the button to become clickable
                show_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Show more']"))
                )
                
                # Click the button
                show_more_button.click()
                print("Clicked 'Show more' button")
                
                # Wait briefly to allow new content to load
                sleep(5)
            
            except Exception as e:
                # If the button is not found or no longer clickable, exit the loop
                print("No 'Show more' button found or clickable.")
                break


    def get_hotel_name_from_web(self):
        try:            
            # # Wait for the div element to be present
            div_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".uitk-spacing.uitk-spacing-padding-large-inlineend-three"))
            )

            # div_element = self.driver.find_element(By.CSS_SELECTOR, "uitk-spacing uitk-spacing-padding-large-inlineend-three")  # Target the div using the class
            outer_html = div_element.get_attribute('outerHTML')


            hotel_div = BeautifulSoup(outer_html, 'html.parser')
            # print(hotel_div.prettify())
            #     # Find the target div by its class
            # # hotel_div = soup.find('div', class_='uitk-spacing uitk-spacing-padding-large-inlineend-three')

            # Extract hotel details
            if hotel_div:
                hotel_name = hotel_div.find('h1', class_='uitk-heading uitk-heading-3').text.strip() if hotel_div.find('h1', class_='uitk-heading uitk-heading-3') else None
                return hotel_name
        except Exception as e:
            return None        

    def main(self,url,db,image_downloader):
        # print(url)
        self.driver.get(url)
        # Some websites use meta tags to restrict zoom behavior (like preventing zooming on mobile devices). Check the HTML <head> for something like:
        # <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        # If the page has such settings, JavaScript zooming might be restricted. You can try to remove or modify these restrictions by interacting with the DOM:

        self.driver.execute_script("var meta = document.querySelector('meta[name=viewport]'); meta.parentNode.removeChild(meta);")

        # sleep(40000)
        self.driver.execute_script("document.body.style.zoom='20%'")
        sleep(4)
        json_handler=JsonDataHandler(file_path="oxford.json")
        # json_handler.hotel_exists("White Fort Hotel")

        hotel_name= self.get_hotel_name_from_web()
        print("-----------------------------------hotel name:", hotel_name)
        check_hotel=False
        if hotel_name is not None:
            check_hotel=json_handler.hotel_exists(hotel_name)

        if check_hotel is False:
        # hotel_name,hotel_details,hotel_amenities=self.hotel_details(url)

            neighbourhood=self.get_hotel_neighbourhood_data()
            # sleep(4000)
            images_data=self.get_hotel_photos()
            # sleep(4000)
            # self.get_room_details()
            
            # sleep(20000)
            hotel_name,hotel_details,hotel_amenities=self.hotel_details(url)
            room_details=self.get_room_details()

            # Fetch hotel details and room details
            # hotel_name, hotel_details, hotel_amenities = self.hotel_details(url)
            # room_details = self.get_room_details()
            # json_handler=JsonDataHandler()
            # Save data to JSON using JsonDataHandler
            # sleep(10000)
            json_handler.save_to_json(hotel_name, hotel_details, hotel_amenities, room_details,images_data,neighbourhood)

            hotel_json_data=json_handler.get_hotel_data(hotel_name=hotel_name)
            print("insertign hotel into database -------------------------")

            db.process_and_insert_single_hotel(hotel_json_data)
            print("###############################################################################\n")
            image_downloader.process_single_hotel(hotel_name)    
            # sleep(10000)
        if check_hotel is True:
            # json_handler.save_to_json(hotel_name, hotel_details, hotel_amenities, room_details,images_data,neighbourhood)

            hotel_json_data=json_handler.get_hotel_data(hotel_name=hotel_name)
            print("inserting hotel into database -------------------------")

            db.process_and_insert_single_hotel(hotel_json_data)
            image_downloader.process_single_hotel(hotel_name)    
            return 
        # # Load data from JSON
        # data = self.json_handler.load_from_json()
        # print(f"Loaded data: {data}")

        # # Get hotel specific data from JSON
        # hotel_data = self.json_handler.get_hotel_data(hotel_name)
        # print(f"Hotel data for {hotel_name}: {hotel_data}")


    def hotel_details(self,url):


        # sleep(1)
        # action = ActionChains(self.driver)
        hotel_name=""
        hotel_rating=""
        additional_rating=""
        hotel_description=""
        hotel_address=""
        # sleep(2000)
        try:            
            # # Wait for the div element to be present
            div_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".uitk-spacing.uitk-spacing-padding-large-inlineend-three"))
            )

            # div_element = self.driver.find_element(By.CSS_SELECTOR, "uitk-spacing uitk-spacing-padding-large-inlineend-three")  # Target the div using the class
            outer_html = div_element.get_attribute('outerHTML')


            hotel_div = BeautifulSoup(outer_html, 'html.parser')
            # print(hotel_div.prettify())
            #     # Find the target div by its class
            # # hotel_div = soup.find('div', class_='uitk-spacing uitk-spacing-padding-large-inlineend-three')

            # Extract hotel details
            if hotel_div:
                hotel_name = hotel_div.find('h1', class_='uitk-heading uitk-heading-3').text.strip() if hotel_div.find('h1', class_='uitk-heading uitk-heading-3') else None

                # Extract hotel rating
                hotel_rating_meta = hotel_div.find('meta', itemprop='ratingValue')
                hotel_rating = hotel_rating_meta['content'] if hotel_rating_meta else None

                # Extract hotel description or other attributes
                hotel_description_meta = hotel_div.find('meta', itemprop='description')
                # hotel_description = hotel_description_meta['content'] if hotel_description_meta else None

                # Safely access the 'content' attribute
                hotel_description = (
                    hotel_description_meta.get('content') if hotel_description_meta and hotel_description_meta.has_attr('content') else None
                )

                # Extract latitude and longitude
                latitude_meta = hotel_div.find('meta', itemprop='latitude')
                latitude = latitude_meta['content'] if latitude_meta else None

                longitude_meta = hotel_div.find('meta', itemprop='longitude')
                longitude = longitude_meta['content'] if longitude_meta else None
                # Extract additional rating (out of 10)
                additional_rating = hotel_div.find('span', class_='uitk-badge-base-text').text.strip() if hotel_div.find('span', class_='uitk-badge-base-text') else None

                                # Locate the element using XPath
                hotel_address_element = self.driver.find_element(By.XPATH, "//div[@class='uitk-text uitk-type-300 uitk-text-default-theme uitk-layout-flex-item uitk-layout-flex-item-flex-basis-full_width' or @data-stid='content-hotel-address']")

                # Extract the text
                hotel_address = hotel_address_element.text

                # Display the details
                print(f"Hotel Name: {hotel_name}")
                print(f"Hotel Rating (from meta): {hotel_rating}")
                print(f"Additional Rating (out of 10): {additional_rating}")
                print(f"Hotel Description: {hotel_description}")
                print(f"Latitude: {latitude}")
                print(f"Longitude: {longitude}")
            else:
                print("Hotel details not found.")
            
        except Exception as e:
            div_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app-layer-base"]/div/main/div/div/section/div[1]/div/div[1]/div/div[3]/div[1]/div'))
            )

            # div_element = self.driver.find_element(By.CSS_SELECTOR, "uitk-spacing uitk-spacing-padding-large-inlineend-three")  # Target the div using the class
            outer_html = div_element.get_attribute('outerHTML')


            hotel_div = BeautifulSoup(outer_html, 'html.parser')

            # print(hotel_div.prettify())


                        # Find the heading using the class
            # hotel_name = hotel_div.find('h1', class_='uitk-heading uitk-heading-4')
            # Find the h1 tag with a class containing "uitk-heading"
            hotel_name = hotel_div.find('h1', class_=re.compile(r'uitk-heading-\d'))
            hotel_name = hotel_name.text
                        # Extract hotel rating
            hotel_rating_meta = hotel_div.find('meta', itemprop='ratingValue')
            hotel_rating = hotel_rating_meta['content'] if hotel_rating_meta else None

            try:
                # Extract hotel description or other attributes
                hotel_description_meta = hotel_div.find('meta', itemprop='description')
                hotel_description = hotel_description_meta['content'] if hotel_description_meta else None
                    

                            # Find the <meta> tag with the itemprop="description"
                meta_tag = hotel_div.find('meta', attrs={'itemprop': 'description'})
                # Get the content attribute
                if meta_tag and 'content' in meta_tag.attrs:
                    hotel_description = meta_tag['content']
            except Exception as e:
                hotel_description=""

            additional_rating = hotel_div.find('span', class_='uitk-badge-base-text').text.strip() if hotel_div.find('span', class_='uitk-badge-base-text') else None
        
            # print()

        hotel_details={"hotel_name":hotel_name,
                       "hotel_address":hotel_address,
                        "hotel_rating":hotel_rating,
                        "additional_rating":additional_rating,
                        "hotel_description":hotel_description,
                        "url":url
                    }

        print(hotel_details)

        hotel_amenities=self.get_hotel_amenities()

        return hotel_name,hotel_details,hotel_amenities
        


        # # sleep(2)
        # #         # Find the button using the aria-label attribute
        # # button = self.driver.find_element(By.XPATH, "//button[@aria-label='See all property amenities']")
        # # Attempt to locate the button with either aria-label "See all property amenities" or "See all about this property"
        # button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'See all') and (contains(@aria-label, 'property amenities') or contains(@aria-label, 'about this property'))]")
        # # Extract the 'aria-label' attribute
        # aria_label = button.get_attribute("aria-label")
        # print("Aria label -----------------------------------",aria_label)
        # # Now you can click the button or perform other actions
        # # button.click()
        # # Click the button
        # button.click()

        # sleep(5)
        # amenities={}
        # if aria_label=="See all about this property":
        #     sleep(1)


        #     # div_element = self.driver.find_element(By.CSS_SELECTOR, "uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-columns uitk-layout-grid-display-grid")
        #     # Wait until the element is present
       
        #     div_element = WebDriverWait(self.driver, 10).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, 
        #             ".uitk-spacing.uitk-spacing-padding-inlinestart-six.uitk-spacing-padding-inlineend-six"))
        #     )
        #     print("Element found:", div_element)

                        
        #     # sleep(50000)
        #     # Get the outerHTML of the div
        #     outer_html = div_element.get_attribute('outerHTML')
        #     amenities_div = BeautifulSoup(outer_html, 'html.parser')
        #     print(amenities_div.prettify())
        #     # amenities={}
        #     # Find all the divs with the specified classes
        #     # Find all the divs with the specified class
        #     divs = amenities_div.find_all('div', class_='uitk-spacing uitk-spacing-padding-blockend-four')
        #     print("Number of divs found:", len(divs))

        #     # print("length of divs" ,len(divs))   
        #     sleep(5) 
        #     # Loop through each div to extract the heading and list items
        #     for div in divs:
        #         # Try to get the heading element (either <h3> or <h4>)
        #         heading = div.find('h4', class_='uitk-heading uitk-heading-6 uitk-layout-flex-item')
        #         if heading:
        #             heading_text = heading.text.strip()
        #             print(f"Heading: {heading_text}")
                    
        #             # Initialize an empty list to hold the items for this heading
        #             list_items_text = []

        #             # Get the ul element
        #             ul = div.find('ul', class_='uitk-typelist uitk-typelist-orientation-stacked uitk-typelist-size-2')
        #             if ul:
        #                 # Find all list items within the ul
        #                 list_items = ul.find_all('li', class_='uitk-spacing uitk-spacing-padding-blockstart-two uitk-spacing-padding-inline-eight')
        #                 for item in list_items:
        #                     # Find the <div> with the text inside the <li>
        #                     div_text = item.find('div', class_='uitk-text uitk-type-300 uitk-text-default-theme')
        #                     if div_text:
        #                         item_text = div_text.text.strip()
        #                         list_items_text.append(item_text)
        #                         print(f"List item: {item_text}")
        #                     else:
        #                         print("No div found with the specified class in list item.")

        #             # Store the heading and list items in the dictionary
        #             amenities[heading_text] = list_items_text

        #             print("-" * 40)                
        # else:
        #     sleep(1)
        #         # Locate the div using its class name
        #     div_element = self.driver.find_element(By.CSS_SELECTOR, "div.uitk-sheet-content.uitk-spacing.uitk-spacing-padding-blockend-.uitk-sheet-content-padded")

        #     # Get the outerHTML of the div
        #     outer_html = div_element.get_attribute('outerHTML')
        #     amenities_div = BeautifulSoup(outer_html, 'html.parser')
        #     # print(amenities_div.prettify())
        #     # Print the outerHTML
        #     # print(outer_html)
        #     # Parse the HTML content
        #     # soup = BeautifulSoup(html_data, 'html.parser')
        #     # amenities={}
        #     # Find all the divs with the specified classes
        #     divs = amenities_div.find_all('div', class_='uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-columns-by-medium uitk-layout-grid-has-columns-by-large uitk-layout-grid-has-space uitk-layout-grid-display-grid uitk-spacing uitk-spacing-padding-blockend-three')
        #     # divs = amenities_div.find_all('div', class_=lambda class_list: all(c in class_list for c in ['uitk-layout-grid', 'uitk-layout-grid-has-auto-columns', 'uitk-layout-grid-has-columns-by-medium', 'uitk-layout-grid-has-columns-by-large']))

        #     print("length of divs" ,len(divs))
        #     # Loop through each div to extract the heading and list items
        #     for div in divs:
        #         # Get the heading (h3 tag)
        #         heading = div.find('h3', class_='uitk-heading')
        #         if heading:
        #             heading_text = heading.text.strip()
        #             print(f"Heading: {heading_text}")
                    
        #             # Initialize an empty list to hold the items for this heading
        #             list_items_text = []

        #             # Get the list items (li tags within the ul)
        #             ul = div.find('ul', class_='uitk-typelist')
        #             if ul:
        #                 list_items = ul.find_all('li', class_='uitk-typelist-item')
        #                 for item in list_items:
        #                     # Find the span with the specified classes inside the li
        #                     span = item.find('span', class_='uitk-text uitk-type-300 uitk-text-default-theme uitk-layout-flex-item')
        #                     if span:
        #                         item_text = span.text.strip()
        #                         list_items_text.append(item_text)
        #                         print(f"List item: {item_text}")
        #                     else:
        #                         print("No span found with the specified class.")
                    
        #             # Store the heading and list items in the dictionary
        #             amenities[heading_text] = list_items_text
                    
        #             print("-" * 40)

        # # Print the dictionary to verify the result
        # print("Amenities Dictionary:", amenities)
        # # close the amenities button
        # action.send_keys(Keys.ESCAPE).perform()

        # ################################## ROOMS ############################################
        # # Find the element using its data-stid attribute
        # element = self.driver.find_element(By.CSS_SELECTOR,'div[data-stid="rooms-rates"]')

        # # Scroll to the element
        # self.driver.execute_script("arguments[0].scrollIntoView();", element)
        # sleep(2)

    def get_hotel_links(self,url):
        
        self.driver.get(url)
        # self.driver.execute_script("document.body.style.zoom='30%'")
        try:
            # Open the target page
            # driver.get("URL_of_your_page")  # Replace with the actual URL
            
            all_links = []  # List to store all collected links

            while True:  # Loop until the "Next" button is no longer clickable
                try:
                    sleep(3)
                    self.driver.execute_script("document.body.style.zoom='30%'")
                    # Wait for the <ul> element to be present
                    wait = WebDriverWait(self.driver, 10)
                    ul_element = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="links-1"]/div/div[2]/div/div[1]/ul'))
                    )

                    # Find all <li> elements inside the targeted <ul>
                    li_elements = ul_element.find_elements(By.TAG_NAME, "li")

                    # Extract links from <li> elements
                    for li in li_elements:
                        try:
                            a_tag = li.find_element(By.TAG_NAME, "a")
                            link = a_tag.get_attribute("href")
                            if link and link not in all_links:  # Avoid duplicates
                                all_links.append(link)
                        except NoSuchElementException:
                            print(f"No <a> tag found in <li>: {li}")

                    print(f"Collected {len(all_links)} links so far.")

                    # Locate and click the "Next" button
                    try:
                        next_button = self.driver.find_element(By.XPATH, '//a[@data-testid="linksPagination-link-next"]')
                        if "disabled" in next_button.get_attribute("class"):
                            print("Next button is disabled. Exiting loop.")
                            break
                        else:
                            next_button.click()
                    except (NoSuchElementException, ElementClickInterceptedException):
                        print("Next button not found or not clickable. Exiting loop.")
                        break

                except TimeoutException:
                    print("Timed out waiting for elements on the page. Exiting loop.")
                    break

            # Print all collected links
            print(f"Total links collected: {len(all_links)}")
            # print(all_links)
            return all_links
        except Exception as e:
            print(f"An error occurred: {e}")

    def expedia_link_creator(self,base_url):
                # Original URL
        # base_url = "https://www.expedia.co.uk/London-Hotels-Great-Cumberland-Place.h21659.Hotel-Information"

        # Parse the URL to get the path
        parsed_url = urlparse(base_url)

        # Extract the property name from the URL path (second-to-last part before `.hXXXXX`)
        path_parts = parsed_url.path.split('/')
        property_name = path_parts[-2].replace('-', ' ')  # Replace hyphens with spaces

        # Define the query parameters as a dictionary with f-string for dynamic property name
        params = {
            "chkin": "2025-2-20",
            "chkout": "2025-2-21",
            "x_pwa": "1",
            "rfrr": "HSR",
            "pwa_ts": "1734959065478",
            "referrerUrl": "aHR0cHM6Ly93d3cuZXhwZWRpYS5jby51ay9Ib3RlbC1TZWFyY2g%3D",
            "useRewards": "false",
            "rm1": "a2",
            "regionId": "553248621538637513",
            "destination": f"{property_name.replace(' ', '+')}",  # Dynamically set destination
            "destType": "MARKET",
            "selected": "7763320",
            "latLong": "53.421071,-2.998314",
            "sort": "RECOMMENDED",
            "top_dp": "323",
            "top_cur": "GBP",
            "userIntent": "",
            "selectedRoomType": "200714388",
            "selectedRatePlan": "203654355",
            "searchId": "6bd23021-5d37-4613-8940-64d0ec3160e7",
            "propertyName": f"{property_name.replace(' ', '+')}"  # Dynamically set propertyName
        }

        # Create the full URL with query parameters
        full_url = f"{base_url}?{urlencode(params)}"
        return full_url

def generate_url():
        # Example usage
    destination = "Lahore, Punjab, Pakistan"
    check_in_date = "2024-12-28"
    check_out_date = "2024-12-30"
    adults = 2
    rooms = 1
    sort = "PRICE_LOW_TO_HIGH"  # Can be changed to other options like 'PRICE_LOW_TO_HIGH', etc.

    # RECOMMENDED
    # PRICE_LOW_TO_HIGH
    # PRICE_HIGH_TO_LOW
    # REVIEW_RELEVANT
    # PROPERTY_CLASS


    # Create an object of ExpediaUrlGenerator
    expedia_url_generator = ExpediaUrlGenerator(destination, check_in_date, check_out_date, adults, rooms, sort)

    # Generate the URLj
    url = expedia_url_generator.generate_url()
    print(url)
    return url


if __name__ == "__main__":
    # display.start()
    obj=WebDriverManager(healdessmode=False)
    db = Database(host="localhost", user="htech_ai", password="Htech786#")
    # db.create_database("expedia_db")
    # Initialize the database (connect to it)
    db.initialize_database("expedia_db")

        # Database connection details
    db_config = {
        "host": "localhost",
        "user": "htech_ai",
        "password": "Htech786#"
    }

    image_downloader = HotelImageDownloader(db_config)

    # db.process_and_insert_single_hotel()
    # url=generate_url()

    # print("Url ------------------------------",url)
    url="https://www.expedia.com/Hotel-Search?adults=2&children=&d1=2025-01-21&d2=2025-01-22&destination=Oxford%2C%20England%2C%20United%20Kingdom&endDate=2025-01-22&latLong=51.752026%2C-1.257731&mapBounds=&regionId=9272&rooms=1&semdtl=&sort=RECOMMENDED&startDate=2025-01-21&theme=&useRewards=true&userIntent=&isInvalidatedDate=false&pwaDialog="
    # sleep(4000)
    obj.open_site(url)
    obj.scroll_and_click_show_more()                                                                  
    # sleep(2000)
    print("out of show more click !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    hotels=obj.extract_hotel_links()
    # url="https://www.expedia.co.uk/All-London-Hotels.d178279.Travel-Guide-City-All-Hotels"
    # hotels=obj.get_hotel_links(url)    
    #     # Create a DataFrame from the list of links
    # df = pd.DataFrame(hotels, columns=["Links"])

    # # Define the output CSV file name
    # output_file = "london_links.csv"

    # # Write the DataFrame to a CSV file
    # df.to_csv(output_file, index=False)

    # print(f"CSV file '{output_file}' has been created with the links.")
    # Load the CSV file into a DataFrame
    # df = pd.read_csv("london_links.csv")
    # # Convert the "Links" column into a list
    # links_list = df["Links"].tolist()

    # hotels= links_list
    # print(len(hotels))

    # # sleep(20000)
    # print("---------------------------------------------------------------------------------number of hotels",len(hotels))
    # print(hotels[0])
    # print("---------------------------------------------------------------------------------------------------------------------------------------------")
    for url in hotels:
        print(url)
        # url="https://www.expedia.com/Atherstone-Hotels-The-Atherstone-Red-Lion-Hotel.h11541319.Hotel-Information?chkin=2025-01-21&chkout=2025-01-22&x_pwa=1&rfrr=HSR&pwa_ts=1734519892027&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5jb20vSG90ZWwtU2VhcmNo&useRewards=true&rm1=a2&regionId=6196039&destination=Birmingham+City+Centre%2C+Birmingham%2C+England%2C+United+Kingdom&destType=MARKET&latLong=52.479366%2C-1.899091&lodging=HOTEL&stay_options_group=hotels_option&sort=RECOMMENDED&top_dp=69&top_cur=USD&userIntent=&selectedRoomType=315757282&selectedRatePlan=384522508&searchId=f507d7fb-c5d4-48a4-812a-41e54a311ac2&propertyName=The+Atherstone+Red+Lion+Hotel"
        # url="https://www.expedia.com/Dubai-Hotels-MOUNT-SINA-HOTEL.h69555306.Hotel-Information?chkin=2024-12-07&chkout=2024-12-11&x_pwa=1&rfrr=HSR&pwa_ts=1733564591585&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5jb20vSG90ZWwtU2VhcmNo&useRewards=true&rm1=a2&regionId=1079&destination=Dubai%2C+United+Arab+Emirates&destType=MARKET&neighborhoodId=553248635976007325&latLong=25.110714%2C55.394882&sort=PRICE_LOW_TO_HIGH&top_dp=44&top_cur=USD&userIntent=&selectedRoomType=314421365&selectedRatePlan=383592209&searchId=aae1409b-df6f-4eee-ac69-b38a64aad3c3&propertyName=MOUNT+SINA+HOTEL+BY+AURA"
    # url="https://www.expedia.com/Dubai-Hotels-Rb-Hostel-Jbr.h106538927.Hotel-Information?chkin=2024-12-28&chkout=2024-12-30&x_pwa=1&rfrr=HSR&pwa_ts=1733831249649&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5jb20vSG90ZWwtU2VhcmNo&useRewards=true&rm1=a2&regionId=1079&destination=Dubai%2C%20United%20Arab%20Emirates&destType=MARKET&neighborhoodId=6258785&latLong=25.110714%2C55.394882&sort=PRICE_LOW_TO_HIGH&top_dp=59&top_cur=USD&userIntent=&selectedRoomType=325092572&selectedRatePlan=396784403&searchId=96c9d7c8-f5cd-4fdf-92b4-dea627d823f2&propertyName=Rb%20Hostel%20Jbr"
        # final_url=obj.expedia_link_creator("https://www.expedia.co.uk/Derby-Hotels-The-Continental-Hotel-Derby.h1381209.Hotel-Information?ai_search_query=&bed_count_ge=&bedroom_count_gt=&chain=&chkin=7%2F2%2F2025&chkout=8%2F2%2F2025&daysInFuture=&destType=MARKET&destination=Derby%2C%20England%2C%20United%20Kingdom&endDate=8%2F2%2F2025&expediaPropertyId=&group=&guestRating=&highlightedPropertyId=&hotelName=&latLong=52.921722%2C-1.47688&misId=&neighborhood=&pdpImageUrls=https%3A%2F%2Fimages.trvl-media.com%2Flodging%2F2000000%2F1390000%2F1381300%2F1381209%2F6a1fd1f0.jpg%3Fimpolicy%3Dresizecrop%26rw%3D598%26ra%3Dfit%2Chttps%3A%2F%2Fimages.trvl-media.com%2Flodging%2F2000000%2F1390000%2F1381300%2F1381209%2F12c3df8f.jpg%3Fimpolicy%3Dresizecrop%26rw%3D297%26ra%3Dfit%2Chttps%3A%2F%2Fimages.trvl-media.com%2Flodging%2F2000000%2F1390000%2F1381300%2F1381209%2F0baa7f53.jpg%3Fimpolicy%3Dresizecrop%26rw%3D297%26ra%3Dfit%2Chttps%3A%2F%2Fimages.trvl-media.com%2Flodging%2F2000000%2F1390000%2F1381300%2F1381209%2F2652b06a.jpg%3Fimpolicy%3Dresizecrop%26rw%3D297%26ra%3Dfit&petsIncluded=false&poi=&pricing_group=&propertyName=The%20Continental%20Hotel%20Derby&pwa_ts=1735295619771&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5jby51ay9Ib3RlbC1TZWFyY2g%3D&regionId=7573&rm1=a2&roomIndex=&searchId=7a033cc9-7360-45e9-9b2a-b4218d992f0e&selected=&selectedRatePlan=385123049&selectedRoomType=315942841&showFilterNotification=false&sort=RECOMMENDED&startDate=7%2F2%2F2025&stayLength=&theme=&us_bathroom_count_gt=&useRewards=false&userIntent=&vacationRentalsOnly=false&x_pwa=1")
        obj.main(url,db,image_downloader)


    # display.stop()            
        # break
    # obj.get_hote_details()
    # obj.sign_in()
    # print("sign in #######################################################")
    # obj.click_send_destination()
    # sleep(4000)
    # obj.click_send_destination()

