from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_attendance():
    reg_no = request.form['reg_no']
    password = request.form['password']

    # Set Chrome options
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-extensions')
    options.add_argument('--log-level=3')
    options.add_argument('--headless')  # Enable headless mode
    options.add_argument('--disable-gpu')  # Disable GPU usage
    options.add_argument('--window-size=1920,1080')  # Set window size

    # Initialize WebDriver with ChromeDriver
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Log in to the website
        driver.get("http://www.mitsims.in/home.jsp")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "studentLink"))).click()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "studentForm")))
        form = driver.find_element(By.ID, "studentForm")
        form.find_element(By.ID, "inputStuId").send_keys(reg_no)
        form.find_element(By.ID, "inputPassword").send_keys(password)
        form.find_element(By.ID, "studentSubmitButton").click()

        # Add a delay to ensure the attendance page is fully loaded
        time.sleep(10)

        # Use JavaScript to extract percentages
        script = """
            var percentages = [];
            var elements = document.getElementsByClassName('x-form-display-field');
            for (var i = 0; i < elements.length; i++) {
                var text = elements[i].innerText.trim();
                if (text && text.includes('.')) {
                    percentages.push(parseFloat(text));
                }
            }
            return percentages;
        """
        percentage_values = driver.execute_script(script)
        percentage_values = [p for p in percentage_values if p is not None]

        if percentage_values:
            total_percentage = sum(percentage_values) / len(percentage_values)
            result = f"Your total attendance percentage is: {total_percentage:.2f}%"
        else:
            result = "No valid attendance percentages found."

    except Exception as e:
        result = f"An error occurred: {e}"

    finally:
        driver.quit()

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
