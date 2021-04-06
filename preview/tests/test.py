import unittest
from selenium import webdriver
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep

class Testing(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_homepage(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000")
        sleep(5)

        self.assertIn("RECSYS", driver.title)
        driver.find_element_by_xpath("//p[contains(text(), 'Enjoy')]")
        assert "No results found." not in driver.page_source

    def test_navigation(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000")
        sleep(5)

        self.assertIn("RECSYS", driver.title)
        home_btn = driver.find_element_by_xpath("//ul/li/a[contains(text(), 'Homepage')]")
        home_btn.click()
        sleep(5)

        data_btn = driver.find_element_by_xpath("//ul/li/a[contains(text(), 'Data')]")
        data_btn.click()
        sleep(5)

        recom_btn = driver.find_element_by_xpath("//ul/li/a[contains(text(), 'Recommendation')]")
        recom_btn.click()
        sleep(5)

        graph_btn = driver.find_element_by_xpath("//ul/li/a[contains(text(), 'Graph')]")
        graph_btn.click()
        sleep(5)

        assert "No results found." not in driver.page_source

    def test_datapage(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/data")
        sleep(5)

        driver.execute_script("window.scrollTo(0,1000)")
        sleep(3)
        driver.execute_script("window.scrollTo(1000,0)")
        sleep(3)    
              
        for i in range(5):
            sleep(5)
            select_elm = Select(driver.find_element_by_name('keyword'))
            select_elm.select_by_index(i)

            price_input = driver.find_element_by_xpath("//input[contains(@name, 'price')]")
            if i == 0 and i == 3:
                price_input.send_keys("2000000")
            elif i == 1:
                price_input.send_keys("250000")
            elif i == 2:
                price_input.send_keys("100000")
            else:
                price_input.send_keys("300000")
            
            top_input = driver.find_element_by_xpath("//input[contains(@name, 'topk')]")
            top_input.send_keys("5")
            
            submit_btn = driver.find_element_by_xpath("//button[contains(text(), 'Submit')]")
            submit_btn.click()
            sleep(5) 
        
        assert "No results found." not in driver.page_source
            

    def test_recommendationpage(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/recommendation")

        sleep(5)

        driver.execute_script("window.scrollTo(0,1500)")
        sleep(3)
        driver.execute_script("window.scrollTo(1500,0)")
        sleep(3) 

        click_count = 0

        for i in range(5):
            sleep(5)

            if click_count > 0:
                driver.execute_script("window.scrollTo(0,1000)")
                sleep(5)
                driver.execute_script("window.scrollTo(1000,0)")
                sleep(5)
            
            select_elm = Select(driver.find_element_by_name('keyword'))
            select_elm.select_by_index(i)

            price_input = driver.find_element_by_xpath("//input[contains(@name, 'price')]")
            if i == 0 and i == 3:
                price_input.send_keys("2000000")
            elif i == 1:
                price_input.send_keys("250000")
            elif i == 2:
                price_input.send_keys("100000")
            else:
                price_input.send_keys("300000")
            
            top_input = driver.find_element_by_xpath("//input[contains(@name, 'topk')]")
            top_input.send_keys("5")
            
            submit_btn = driver.find_element_by_xpath("//button[contains(text(), 'Submit')]")
            submit_btn.click()
            click_count += 1
            sleep(5)
        
        assert "No results found." not in driver.page_source


    def test_graphpage(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/graph")

        sleep(5)

        driver.execute_script("window.scrollTo(0,1000)")
        sleep(3)
        driver.execute_script("window.scrollTo(1000,0)")
        sleep(3) 

        for i in range(5):
            sleep(5)
            driver.execute_script("window.scrollTo(0,1000)")
            sleep(5)
            select_elm = Select(driver.find_element_by_name('keyword'))
            select_elm.select_by_index(i)
            
            submit_btn = driver.find_element_by_xpath("//button[contains(text(), 'Submit')]")
            submit_btn.click()
            sleep(5)
        
        assert "No results found." not in driver.page_source

    def test_detailpage(self):
        driver = self.driver
        for i in range(5):
            driver.get("http://127.0.0.1:5000/recommendation")
            sleep(5)

            select_elm = Select(driver.find_element_by_name('keyword'))
            select_elm.select_by_index(i)

            sleep(5)
                                    
            submit_btn = driver.find_element_by_xpath("//button[contains(text(), 'Submit')]")
            submit_btn.click()

            driver.execute_script("window.scrollTo(0,250)")
            sleep(3)

            item = driver.find_element_by_xpath("//a[contains(@id, 'postData')]").get_attribute('href')   
            driver.get(item) 
            sleep(10)
            
            driver.execute_script("window.scrollTo(0,1000)")

            sleep(5)
            
        assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.close()
        # pass


if __name__ == '__main__':
    unittest.main()