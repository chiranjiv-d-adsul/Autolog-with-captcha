import time
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import requests

# Path to your Tesseract executable (install pytesseract and Tesseract OCR)
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def solve_captcha(captcha_element):
    captcha_image_url = captcha_element.get_attribute('src')
    response = requests.get(captcha_image_url)
    if response.status_code == 200:
        with open("captcha_image.jpg", "wb") as f:
            f.write(response.content)
        captcha_text = pytesseract.image_to_string(Image.open("captcha_image.jpg"))
        return captcha_text
    else:
        print("Failed to fetch captcha image. Status code:", response.status_code)
        return None





def enter_data(driver, second_url,data):

    driver.get(second_url)

    name_field = driver.find_element(By.NAME, "name")
    password_field = driver.find_element(By.NAME, "pass")

    name_field.send_keys(data[0])
    password_field.send_keys(data[1])
        # Locate and fill data fields (adapt based on website structure)
        # data_fields = driver.find_elements(By.CLASS_NAME, "data-field")
        # for field, value in zip(data_fields, data):
        #     field.send_keys(value)
        # Solve the Captcha
    captcha_element = driver.find_element(By.ID, "captcha_image")
    captcha_text = solve_captcha(captcha_element)

    captcha_input = driver.find_element(By.ID, "edit-captcha-response")
    captcha_input.send_keys(captcha_text)

    submit_button = driver.find_element(By.ID, "edit-submit")

    submit_button.click()


def login(driver, url, username, password):
    while True:
        driver.get(url)
        username_field = driver.find_element(By.NAME, "username_email")
        # password_field = driver.find_element(By.NAME, "registerPassword")
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys(username)
        password_field.send_keys(password)  # Replace with your actual password


        login_button = driver.find_element(By.CSS_SELECTOR, "form button")
        login_button.click()
        time.sleep(5)




def main():
    driver = webdriver.Chrome()  # Replace with your preferred browser's WebDriver
    second_url = "https://www.india.gov.in/user/login"
    data = ["chiranjiv", "123"]

    url = "https://coopasspm.000webhostapp.com/loginregister.php"  # Replace with the actual login URL
    # DATA OF FIRST URL
    username = "chiranjiv"
    password = "12345678"


    # Loop for 1 hour
    enter_data(driver, second_url, data)

    print("hi")
    time.sleep(5)
    start_time = time.time()
    while time.time() - start_time < 10:  # Loop for 1 hour

        login(driver, url, username, password)
        print("2")
        time.sleep(5)  # Adjust delay as needed
        print("3")
    p1 = multiprocessing.Process(target=enter_data(driver, second_url, data))
    p2 = multiprocessing.Process(target=login(driver, url, username, password))


    p1.start()
    p2.start()

    # Wait for a short while to ensure p1 is running before starting p2
    time.sleep(2)

    p2.join()





    p1.terminate()
    print("p1")
    p1.join()  # Wait for p1 to terminate

    print("Both processes finished")


if __name__ == "__main__":
    main()
