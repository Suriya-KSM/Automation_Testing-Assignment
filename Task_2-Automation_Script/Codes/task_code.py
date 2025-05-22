from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

class TaskCodes:
    def __init__(self, driver):
        self.driver = driver

    def add_task(self, task_name):
        sleep(2)
        input_box = self.driver.find_element(By.CLASS_NAME, "new-todo")
        input_box.send_keys(task_name + Keys.RETURN)
        

    def get_all_tasks(self):
        sleep(2)
        return self.driver.find_elements(By.CSS_SELECTOR, ".todo-list li")

    def get_task_texts(self):
        sleep(2)
        return [task.find_element(By.CSS_SELECTOR, "label").text for task in self.get_all_tasks()]

    def complete_task(self, index):
        sleep(2)
        task = self.get_all_tasks()[index]
        checkbox = task.find_element(By.CSS_SELECTOR, "input.toggle")
        checkbox.click()
        

    def delete_task(self, index):
        sleep(2)
        task = self.get_all_tasks()[index]
        self.driver.execute_script("arguments[0].scrollIntoView();", task)
        self.driver.execute_script("arguments[0].querySelector('button.destroy').click();", task)
        

    def is_task_completed(self, index):
        sleep(2)
        task = self.get_all_tasks()[index]
        return "completed" in task.get_attribute("class")
