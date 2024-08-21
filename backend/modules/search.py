import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InternetSearch():
    ENDPOINT = 3000
    API_ENDPOINT = 3001
    
    def __init__(self, query: str):
        self.query = query
        
    def format_query(self, query):
        formatted_query = query.replace(" ", "+")
        return formatted_query

    def search(self):
        # Set up the Chrome WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode (optional)
        driver = webdriver.Chrome(options=options)

        try:
            # Format the URL with the query
            url = f"http://localhost:{self.ENDPOINT}/?q={self.format_query(self.query)}&format=json"
            
            # Navigate to the formatted URL
            print(f"Navigating to: {url}")
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".response-content"))
            )
            
            print("Search completed successfully")

        except Exception as e:
            print(f"An error occurred during the search: {e}")

        finally:
            # Close the browser
            driver.quit()

    def fetch_id(self):
        api = f"http://localhost:{self.API_ENDPOINT}/api/chats/"        
        response = requests.get(api)
        
        recent_chat = response.json()["chats"][0]
        chat_id = recent_chat["id"]
        chat_query = recent_chat["title"]
        
        return chat_id, chat_query

    def check(self):
        chat_id, chat_query = self.fetch_id()
        if chat_query == self.query:
            return chat_id
        else:
            time.sleep(10)
            self.check()
            
    def process(self):
        chat_id = self.check()
        url = f"http://localhost:3001/api/chats/{chat_id}"
        raw_response = requests.get(url)
        response = raw_response.json()["messages"][1]["content"]
        
        return response
    
def SEARCH(query):
    search = InternetSearch(query)
    search.search()
    result = search.process()
    
    if result:
        return result
    else:
        return "Mission failed to search"