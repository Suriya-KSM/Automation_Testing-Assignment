from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import pytest
from Test_Data import data

class Test_Gmaps():

    @pytest.fixture
    def boot_function(self):
        options = Options()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) #
        self.driver.implicitly_wait(10)
        yield
        self.driver.quit()


    def test_google_maps(self, boot_function):
        # a. Load Google Maps
        self.driver.get(data.Data().URL)
        self.driver.maximize_window()
        assert "Google Maps" in self.driver.title, "Google Maps did not load"

        # b. Zoom controls
        zoom_in = self.driver.find_element(By.XPATH, "//button[@aria-label='Zoom in']")
        zoom_out = self.driver.find_element(By.XPATH, "//button[@aria-label='Zoom out']")
        zoom_in.click()
        sleep(1)
        zoom_out.click()
        sleep(1)

        # c. Search for Chennai
        search_box = self.driver.find_element(By.ID, "searchboxinput")
        search_box.clear()
        search_box.send_keys(data.Data().find_location)
        search_box.send_keys(Keys.ENTER)
        sleep(4)

    # d. Validate marker location
        try:
            location_title = self.driver.find_element(By.XPATH, "//h1[@class='DUwDvf lfPIob']").text
            assert data.Data().find_location == location_title, f"Expected 'Chennai' in location marker, got: {location_title}"
        except:
            pytest.fail("Location marker for Chennai not found")

        cancel_button = self.driver.find_element(By.XPATH, "//button[@class='yAuNSb vF7Cdb']")
        cancel_button.click()
        sleep(2)

        # e. Directions from Pondicherry to Chennai
        directions_btn = self.driver.find_element(By.XPATH, "//span[@class='google-symbols NhBTye G47vBd']")
        directions_btn.click()
        sleep(2)

        start_input = self.driver.find_element(By.XPATH, "//input[@aria-label='Choose starting point, or click on the map...']")
        start_input.send_keys(data.Data().start_location)
        start_input.send_keys(Keys.ENTER)
        sleep(2)

        end_input = self.driver.find_element(By.XPATH, "//input[@aria-label='Choose destination, or click on the map...']")
        end_input.clear()
        end_input.send_keys(data.Data().Destination)
        end_input.send_keys(Keys.ENTER)
        sleep(5)

        # f. Validate the distance between Pondicherry to Chennai (~151 km)
        # Car_route = self.driver.find_element(By.XPATH, "//span[@aria-label='Driving']")
        # Car_route.click()
        # sleep(1)
        # Details = self.driver.find_element(By.XPATH, "//*[text()='Details']")
        # Details.click()
        # sleep(2)
        try:
            distance_elem = self.driver.find_element(By.XPATH, "//div[@class='ivN21e tUEI8e fontBodyMedium']")
            distance_text = distance_elem.text
            print("Fetched distance:", distance_text)
        except:
            pytest.fail("Could not find distance info for directions")

        match = re.search(r"(\d+\.?\d*)\s*km", distance_text)
        assert match, f"Distance not in expected format: {distance_text}"
        distance_km = float(match.group(1))
        assert 150 <= distance_km <= 170, f"Expected ~151 km, but got {distance_km} km"
