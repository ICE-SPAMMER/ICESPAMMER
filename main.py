import random
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import string
from faker import Faker
# Add these imports at the top
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

# Replace the browser creation line:
#browser = webdriver.Chrome()

# With this Firefox + Tor setup:
firefox_options = Options()
firefox_options.set_preference('network.proxy.type', 1)
firefox_options.set_preference('network.proxy.socks', '127.0.0.1')
firefox_options.set_preference('network.proxy.socks_port', 9050)
firefox_options.set_preference('network.proxy.socks_version', 5)
firefox_options.set_preference('network.proxy.socks_remote_dns', True)


def wait_for_captcha_completion(browser, timeout=60):
    """
    Enhanced CAPTCHA detection and completion verification
    """
    try:
        # Wait for the CAPTCHA iframe to be present
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title^='reCAPTCHA']"))
        )
        print("CAPTCHA detected! Please complete it manually.")
        
        # Wait for CAPTCHA completion
        success = False
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Switch to default content to check for response
                browser.switch_to.default_content()
                token = browser.execute_script(
                    "return document.getElementById('g-recaptcha-response').value"
                )
                if token and len(token) > 0:
                    success = True
                    break
            except:
                pass
            time.sleep(1)
            
        if success:
            print("CAPTCHA completed successfully!")
            return True
        else:
            print("CAPTCHA completion timeout!")
            return False
            
    except Exception as e:
        print(f"Error during CAPTCHA detection: {str(e)}")
        return False

def random_word():
    word = ""
    for i in range(random.randint(1, 10)):
        word += random.choice(string.ascii_letters)
    return word
def generate_sentence(min, max):
    sentence = ""
    for i in range(random.randint(min, max)):
        newword = random_word()
        sentence += newword
        sentence += " "
    print(sentence)
    return sentence
def randomify(input, often = 3):
    tempinput = list(input)
    for i in range(int(len(tempinput)/often)):
        tempinput.insert(random.randint(0, len(tempinput)), random.choice(string.ascii_letters))
        
    output = ""
    for i in tempinput:
        output += i
    return output
def randomify_sentence(input):
    tempinput = input.split(" ")
    for i in range(int(len(tempinput))):
        tempinput.insert(random.randint(0, len(tempinput)), random.choice(string.ascii_letters))
        currword = tempinput[i]
        currword = randomify(currword, 5)
        
    output = ""
    for i in tempinput:
        output += i + " "
    return output
providers = ["gmail.com", "yahoo.com", "hotmail.com", "aol.com", "msn.com", "comcast.net"]
company_names = ["SpaceX", "X Holdings Corp.", "X Corp.", "X Payments LLC", "The Boring Company", "X.AI Corp.", "Neuralink Corp.", "Tesla, Inc.", ]
company_line1 = ["54298 Boca Chica Blvd", "865 FM 1209", "865 FM 1209", "865 FM 1209", "12200 Crenshaw Blvd", "865 FM 1209", "Unknown", "1 Tesla Road", ]
company_cities = ["Brownsville", "Bastrop", "Bastrop", "Bastrop", "Hawthorne", "Bastrop", "Austin", "Austin"]
company_states = ["TX", "TX", "TX", "TX", "CA", "TX", "TX", "TX"]
while True:
    browser = webdriver.Firefox(options=firefox_options)
    browser.get("https://check.torproject.org/")  
    try:
        browser.find_element(By.CLASS_NAME, "on")  
    except:
        print("YOU ARE NOT ON TOR, FIX THAT, NOW! YOU DON'T WANT ICE OR THE FBI KNOCKING ON YOUR DOOR.")
        browser.quit()
        exit()
    fake = Faker("en_US")

    firstname = fake.first_name()
    lastname = fake.last_name()
    if random.randrange(0, 5) == 5:
        number = ""
        
    else:
        number = str(random.randint(0,10000))
    if random.getrandbits(1) == True:
        email = f"{firstname.lower()}.{lastname.lower()}{number}@{random.choice(providers)}"
    else:
        email = f"{lastname.lower()}.{firstname.lower()}{number}@{random.choice(providers)}"
    print(email)
    phone=""
    for i in range(10):
        phone+= str(random.randint(0,9))
    print(phone)
    browser.get("https://www.ice.gov/webform/ice-tip-form")
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "usa-input")))
    print("loaded")
    browser.find_element(By.ID, "edit-first-name").send_keys(firstname)
    browser.find_element(By.ID, "edit-last-name").send_keys(lastname)
    browser.find_element(By.ID, "edit-email").send_keys(email)
    browser.find_element(By.ID, "edit-phone-number").send_keys(phone)
    radio = browser.find_element(By.ID, "edit-where-are-you-reporting-from-radios-inside")
    browser.execute_script("arguments[0].click();", radio)
    wait = WebDriverWait(browser, 10)
    street_address = wait.until(EC.visibility_of_element_located((By.ID, "edit-line-1")))
    street_address.send_keys(fake.street_address())
    browser.find_element(By.ID, "edit-city").send_keys(fake.city())
    dropdown = Select(browser.find_element("id", "edit-state"))
    options = []
    for option in dropdown.options:
        if option.get_attribute("value") != "":
            options.append(option.get_attribute("value"))
    print(options)
    dropdown.select_by_value(random.choice(options)) 
    browser.find_element(By.ID, "edit-zip-code").send_keys(fake.zipcode())
    radio2 = browser.find_element(By.ID, "edit-please-check-all-that-apply-other")
    browser.execute_script("arguments[0].click();", radio2)
    wait = WebDriverWait(browser, 10)
    reason = wait.until(EC.visibility_of_element_located((By.ID, "edit-other")))
    reason.send_keys(generate_sentence(3, 20))
    Select(browser.find_element("id", "edit-state-location")).select_by_value(random.choice(options)) #
    radio3 = browser.find_element(By.ID, "edit-the-complaint-involves-a-2-both")
    browser.execute_script("arguments[0].click();", radio3)
    company = random.randint(0, len(company_names))
    wait = WebDriverWait(browser, 10)
    reason = wait.until(EC.visibility_of_element_located((By.ID, "edit-business-company-name")))
    reason.send_keys(randomify(company_names[company]) )
    browser.find_element(By.ID, "edit-line-1-busniess").send_keys(randomify(company_line1[company]) )
    browser.find_element(By.ID, "edit-city-business").send_keys(randomify(company_cities[company]) )
    Select(browser.find_element("id", "edit-state-business")).select_by_value(company_states[company]) 
    browser.find_element(By.ID, "edit-first-name-individual").send_keys(randomify("Elon"))
    browser.find_element(By.ID, "edit-last-name-individual").send_keys(randomify("Musk"))
    radio4 = browser.find_element(By.ID, "edit-date-of-birth-or-approximate-age-dob")
    browser.execute_script("arguments[0].click();", radio4)
    wait = WebDriverWait(browser, 10)
    date = wait.until(EC.visibility_of_element_located((By.ID, "edit-date-of-birth")))
    date.send_keys("06-28-1971")
    browser.find_element(By.ID, "edit-line-1-individual").send_keys(randomify("PO Box 341886"))
    browser.find_element(By.ID, "edit-city-individual").send_keys(randomify("Lakeway, TX 78734"))
    Select(browser.find_element("id", "edit-state-individual")).select_by_value("TX") 
    radio5 = browser.find_element(By.ID, "edit-have-you-previously-submitted-this-information-to-any-law-radios-false")
    browser.execute_script("arguments[0].click();", radio5) 
    browser.find_element(By.ID, "edit-please-provide-a-summary-of-the-criminal-activity-limit-2500-cha").send_keys(randomify_sentence("YOU CANNOT DEFEAT US. WE WILL FIGHT BACK. WE WILL NOT LET OUR BROTHERS AND SISTERS BE TAKEN AWAY. WE WILL NOT LET YOU TAKE OUR RIGHTS AWAY. GO AWAY, FASCISTS \n")+generate_sentence(30,100)) 
    radio6 = browser.find_element(By.ID, "edit-did-you-have-additional-businesses-individuals-to-report-on-yes")
    browser.execute_script("arguments[0].click();", radio6)
    element = browser.find_element(By.ID, 'edit-actions')
    browser.execute_script("arguments[0].scrollIntoView();", element)
    WebDriverWait(browser, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
)

    # Wait for the reCAPTCHA checkbox to be clickable and click it
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
    ).click()

    # Switch back to the main content
    browser.switch_to.default_content()
    if wait_for_captcha_completion(browser):
        try:
            # Find and click the submit button after CAPTCHA is completed
            """submit_button = browser.find_element(By.ID, "edit-submit")
            browser.execute_script("arguments[0].click();", submit_button)"""
            print("Form submitted successfully!")
        except Exception as e:
            print(f"Error submitting form: {str(e)}")
    else:
        print("Could not verify CAPTCHA completion")

    browser.quit()