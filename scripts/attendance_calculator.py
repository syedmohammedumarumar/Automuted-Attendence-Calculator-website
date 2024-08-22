# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# def calculate_attendance(reg_no, password):
#     try:
#         # Set Chrome options (non-headless mode for debugging)
#         options = Options()
#         options.add_argument('--ignore-certificate-errors')
#         options.add_argument('--disable-web-security')
#         options.add_argument('--disable-extensions')
#         options.add_argument('--log-level=3')
#         # Comment out the headless option for debugging
#         # options.add_argument('--headless')  # Enable headless mode
#         options.add_argument('--disable-gpu')  # Disable GPU usage
#         options.add_argument('--window-size=1920,1080')  # Set window size

#         # Install ChromeDriver and set up the service
#         service = Service(ChromeDriverManager().install())

#         # Initialize WebDriver with options
#         driver = webdriver.Chrome(service=service, options=options)

#         # Open the college website and log in
#         driver.get("http://www.mitsims.in/home.jsp")
#         WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "studentLink"))).click()
#         WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "studentForm")))
#         form = driver.find_element(By.ID, "studentForm")
#         form.find_element(By.ID, "inputStuId").send_keys(reg_no)
#         form.find_element(By.ID, "inputPassword").send_keys(password)
#         form.find_element(By.ID, "studentSubmitButton").click()

#         # Wait for attendance page to load
#         WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'x-form-display-field')))

#         # Use JavaScript to extract percentages
#         script = """
#             var percentages = [];
#             var elements = document.getElementsByClassName('x-form-display-field');
#             for (var i = 0; i < elements.length; i++) {
#                 var text = elements[i].innerText.trim();
#                 if (text && text.includes('.')) {  // Check if the text is a percentage
#                     percentages.push(parseFloat(text));
#                 }
#             }
#             return percentages;
#         """

#         # Execute JavaScript in the browser context
#         percentage_values = driver.execute_script(script)

#         # Filter out None values
#         percentage_values = [p for p in percentage_values if p is not None]

#         # Calculate and print the average attendance percentage
#         if percentage_values:
#             total_percentage = sum(percentage_values) / len(percentage_values)
#             return f"Your total attendance percentage is: {total_percentage:.2f}%"
#         else:
#             return "No valid attendance percentages found."

#     except Exception as e:
#         return f"An error occurred: {e}"

#     finally:
#         # Automatically close the browser after displaying the result
#         driver.quit()
