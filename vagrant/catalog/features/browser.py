from selenium import webdriver


class Browser(object):

    base_url = 'http://localhost:5000'
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    def close(self):
        """
        close the webdriver instance
        """
        self.driver.quit()

    def visit(self, location=''):
        """
        navigate webdriver to different pages
        """
        url = self.base_url + location
        self.driver.get(url)

    def find_by_id(self, selector):
        """
        find a page element in the DOM
        """
        return self.driver.find_element_by_id(selector)

    def find_by_link(self, selector):
        """
        find an element with link text in the DOM
        """
        return self.driver.find_element_by_link_text(selector)

    def find_elements_by_id(self, selector):
        """
        find all element with link text in the DOM
        """
        return self.driver.find_elements_by_id(selector)
