from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests  # For checking website status

# Function to check if the official college website is reachable
def check_website_status(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException:
        return False

def home(request):
    return render(request, 'index.html')

def main(request):
    return render(request, 'main.html')

def calculate_attendance(request):
    if request.method == 'POST':
        reg_no = request.POST['reg_no']
        password = request.POST['password']

        # Configure Chrome options for headless mode
        options = Options()
        options.add_argument('--headless')  # Run Chrome in headless mode
        options.add_argument('--disable-gpu')  # Disable GPU acceleration
        options.add_argument('--no-sandbox')  # Bypass OS security model
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
        options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
        options.add_argument('--allow-insecure-localhost')  # Allow insecure localhost connections
        options.add_argument('--log-level=3')  # Set logging level to fatal

        driver = None
        college_url = "http://mitsims.in/"

        try:
            # Check if the college website is reachable
            if not check_website_status(college_url):
                result = "The official college website is currently down. You cannot calculate your attendance until it is back online."
                return render(request, 'index.html', {'result': result})

            # Proceed with attendance scraping if the website is reachable
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            # Open the website
            driver.get(college_url)

            # Wait until the page is fully loaded
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "studentLink"))).click()

            # Wait for the login form to appear
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "studentForm")))

            # Fill in the form
            form = driver.find_element(By.ID, "studentForm")
            form.find_element(By.ID, "inputStuId").send_keys(reg_no)
            form.find_element(By.ID, "inputPassword").send_keys(password)
            form.find_element(By.ID, "studentSubmitButton").click()

            # Wait for the attendance data to load (adjust if necessary)
            time.sleep(10)

            # Extract name and attendance percentages using JavaScript
            script = """
                var name = '';
                var percentages = [];
                var elements = document.getElementsByClassName('x-form-display-field');
                
                for (var i = 0; i < elements.length; i++) {
                    var text = elements[i].innerText.trim();
                    
                    // Check if this element contains the student's name
                    if (i == 0) {  // Assuming the name is the first element
                        name = text;
                    }
                    
                    // Extract attendance percentages (those containing floating points)
                    if (text && text.includes('.')) {
                        percentages.push(parseFloat(text));
                    }
                }
                return { 'name': name, 'percentages': percentages };
            """
            data = driver.execute_script(script)
            student_name = data['name']
            percentage_values = data['percentages']
            percentage_values = [p for p in percentage_values if p is not None]

            if percentage_values:
                total_percentage = sum(percentage_values) / len(percentage_values)
                result = f"Hey {student_name}, your total attendance percentage is: {total_percentage:.2f}%"
            else:
                result = "Please enter correct username and password."

        except Exception as e:
            result = f"An error occurred: {e}"

        finally:
            if driver:
                driver.quit()

        return render(request, 'index.html', {'result': result})
    else:
        return render(request, 'index.html')
