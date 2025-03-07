import unittest
import testdata
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class TestStartPage(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Starts webdriver and opens start page"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Headless mode for automated tests without GUI
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.get("http://localhost:3000/wetterstation.html")

    def test_page_loads(self):
        """Tests if the page is loaded"""
        self.assertIn("ZEUS-Wetterstationen", self.driver.title)

    def test_input_fields_exist(self):
        """Tests if input fields exist"""
        fields = ["latitude", "longitude", "radius", "maxStations", "startYear", "endYear"]
        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(self.driver.find_element(By.ID, field).is_displayed())

    def test_buttons_exist(self):
        """Tests if search and reset buttons exist"""
        search_button = self.driver.find_element(By.CLASS_NAME, "search")
        reset_button = self.driver.find_element(By.CLASS_NAME, "reset")
        self.assertTrue(search_button.is_displayed())
        self.assertTrue(reset_button.is_displayed())

    def test_fill_input_fields(self):
        """Fills the input fields with test values"""
        for field, value in testdata.testdata_fill_input_fields.items():
            input_element = self.driver.find_element(By.ID, field)
            input_element.clear()
            input_element.send_keys(value)
            self.assertEqual(input_element.get_attribute("value"), value)

    def test_search_button_click(self):
        """Clicks on the search button and tests if markers are displayed on the map"""
        search_button = self.driver.find_element(By.CLASS_NAME, "search")
        search_button.click()
        self.assertTrue(len(self.driver.find_elements(By.CLASS_NAME, "leaflet-marker-icon")) > 0)

    @classmethod
    def tearDownClass(cls):
        """Quits webdriver."""
        cls.driver.quit()

class TestStationPage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Starts webdriver and opens sample station page"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.get("http://localhost:3000/station.html?station=VILLINGEN-SCHWENNINGEN&id=GME00129634&latitude=48.0458&longitude=8.4617&startYear=2010&endYear=2020")

    def test_page_loads(self):
        """Tests if the page is loaded"""
        self.assertIn("ZEUS-Wetterstation", self.driver.title)

    def test_headers_exist(self):
        """Tests if Header und SubHeader exist"""
        header = self.driver.find_element(By.ID, "stationHeader")
        sub_header = self.driver.find_element(By.ID, "stationSubHeader")
        self.assertEqual(header.text, "VILLINGEN-SCHWENNINGEN")
        self.assertIn("Breitengrad: 48.0458", sub_header.text)
        self.assertIn("Längengrad: 8.4617", sub_header.text)

    def test_charts_exist(self):
        """Tests if annual and seasonal charts exist"""
        annual_chart = self.driver.find_element(By.ID, "annualChartContainer")
        seasonal_chart = self.driver.find_element(By.ID, "seasonalChartContainer")
        self.assertTrue(annual_chart.is_displayed())  # Shown by default
        self.assertFalse(seasonal_chart.is_displayed())  # Hidden by default

    @classmethod
    def tearDownClass(cls):
        """Quits webdriver"""
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
