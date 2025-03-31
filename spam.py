# """i have a thougth that company or org name and posted by 
# edxample cards in this we can see right 
# Full Stack Developer 

# Leading Client
# Posted by Rudr Consultancy Services
# 1-3 Yrs
# Not disclosed
# Jaipur
# Full Stack Developer . Job Name: Full StackDeveloper . Job Role: Developer Industry:Sof...
# csswebsocketxmlapinode.jsfullstack developmentserver sideapi integration
# 1 Day Ago
# save
# Angular Developer

# Leading Client
# Posted by Rudr Consultancy Services"""
# """i have an idea that store the data for company ,position, role, posted by, url of tab to apply  and all from the card it self without going in to the other tab to open 
# example stoping to nav in tab by this content stage 
# <div class="srp-jobtuple-wrapper" data-job-id="260325921629"><div class="cust-job-tuple layout-wrapper lay-2 sjw__tuple "><div class=" row1"><h2><a class="title " title="Full Stack Developer" href="https://www.naukri.com/job-listings-full-stack-developer-rudr-consultancy-services-jaipur-1-to-3-years-260325921629" target="_blank" rel="noopener noreferrer">Full Stack Developer</a></h2><span class="imagewrap "><img src="https://img.naukimg.com/logo_images/groups/v1/2413086.gif" class="logoImage" loading="lazy"></span></div><div class=" row2"><span class="rm-cursor-pointer comp-dtls-wrap"><a class=" comp-name " title="Leading Client" target="_blank">Leading Client</a></span> <div class="client-company-name"><a target="_blank" title="Posted by Rudr Consultancy Services" href="https://www.naukri.com/rudr-consultancy-services-jobs-careers-2523810">Posted by Rudr Consultancy Services</a></div> </div><div class=" row3"><div class="job-details "><span class="exp-wrap"><span class="ni-job-tuple-icon ni-job-tuple-icon-srp-experience exp"><span title="1-3 Yrs " class="expwdth">1-3 Yrs</span></span></span><span class="sal-wrap ver-line"><span class="ni-job-tuple-icon ni-job-tuple-icon-srp-rupee sal"><span title="Not disclosed " class="">Not disclosed</span></span></span><span class="loc-wrap ver-line"><span class="ni-job-tuple-icon ni-job-tuple-icon-srp-location loc"><span title="Jaipur " class="locWdth">Jaipur</span></span></span></div></div><div class=" row4"><span class="job-desc ni-job-tuple-icon ni-job-tuple-icon-srp-description">Full Stack Developer . Job Name: Full StackDeveloper . Job Role: Developer Industry:Sof...</span></div><div class=" row5"><ul class="tags-gt "><li class="dot-gt tag-li ">css</li><li class="dot-gt tag-li ">websocket</li><li class="dot-gt tag-li ">xml</li><li class="dot-gt tag-li ">api</li><li class="dot-gt tag-li ">node.js</li><li class="dot-gt tag-li ">fullstack development</li><li class="dot-gt tag-li ">server side</li><li class="dot-gt tag-li ">api integration</li></ul></div><div class=" row6">  <span class="job-post-day ">1 Day Ago</span><span class="ni-job-tuple-icon ni-job-tuple-icon-srpSaveUnfilled un-saved save-job-tag">save</span></div></div></div>
# we can save time and get all the data from the card it self
# i need a final complete code not showing the code"""

# import os
# import time
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from urllib.parse import quote
# from webdriver_manager.chrome import ChromeDriverManager
# from dotenv import load_dotenv

# # ===== CONFIGURATION =====
# load_dotenv('auth.env')

# EMAIL = os.getenv('NAUKRI_EMAIL_now')
# PASSWORD = os.getenv('NAUKRI_PASSWORD_now')

# KEYWORDS = ['Angular Developer', 'Full Stack Developer']
# JOB_AGES = [1, 3]
# EXPERIENCES = [1]
# MAX_PAGES = 5

# # ===== DRIVER SETUP =====
# options = Options()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--incognito")
# options.add_argument("--disable-popup-blocking")
# options.add_argument("--disable-extensions")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # ===== LOGIN FUNCTION =====
# def login():
#     print("🔐 Logging into Naukri...")
#     driver.get('https://login.naukri.com/')
#     time.sleep(3)
#     driver.find_element(By.ID, 'usernameField').send_keys(EMAIL)
#     driver.find_element(By.ID, 'passwordField').send_keys(PASSWORD + Keys.RETURN)
#     time.sleep(5)
#     if "naukri.com" in driver.current_url:
#         print("✅ Logged in successfully")
#     else:
#         print("❌ Login failed")

# # ===== SCROLL TO LOAD JOBS =====
# def scroll_to_load_jobs():
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height

# # ===== EXTRACT JOB DATA =====
# def extract_jobs():
#     job_data = []
#     for keyword in KEYWORDS:
#         for job_age in JOB_AGES:
#             for experience in EXPERIENCES:
#                 print(f"\n🔎 Searching for '{keyword}' | Job Age: {job_age} days | Experience: {experience} years")

#                 search_url = f"https://www.naukri.com/{quote(keyword)}-jobs?k={quote(keyword)}&experience={experience}&jobAge={job_age}"
#                 driver.get(search_url)
#                 time.sleep(2)

#                 for page in range(1, MAX_PAGES + 1):
#                     print(f"📄 Fetching Page {page} for '{keyword}'")

#                     if page > 1:
                        
#                          print(f"\n🔎 Searching for '{keyword}' with job age '{job_age}' days and experience '{experience}' years...page{page}")
#                          driver.get(f"https://www.naukri.com/{quote(keyword)}-jobs-{page}?k={quote(keyword)}&experience={experience}&jobAge={job_age}")
#                          time.sleep(2)
                    
#                     scroll_to_load_jobs()
#                     soup = BeautifulSoup(driver.page_source, 'html.parser')
#                     job_cards = soup.find_all('div', class_='srp-jobtuple-wrapper')

#                     if not job_cards:
#                         print("⚠️ No job cards found on this page.")
#                         break

#                     for card in job_cards:
#                         try:
#                             job_title = card.find('a', class_='title').text.strip()
#                             job_url = card.find('a', class_='title')['href']
#                             company_name = card.find('a', class_='comp-name').text.strip()
#                             posted_by = card.find('div', class_='client-company-name').text.strip() if card.find('div', class_='client-company-name') else 'Not mentioned'
#                             experience = card.find('span', title=True, class_='expwdth').text.strip() if card.find('span', title=True, class_='expwdth') else 'Not specified'
#                             salary = card.find('span', class_='sal').text.strip() if card.find('span', class_='sal') else 'Not disclosed'
#                             location = card.find('span', class_='locWdth').text.strip() if card.find('span', class_='locWdth') else 'Not specified'
#                             skills = ', '.join([skill.text.strip() for skill in card.find_all('li', class_='tag-li')]) if card.find_all('li', class_='tag-li') else 'Not specified'
#                             job_desc = card.find('span', class_='job-desc').text.strip() if card.find('span', class_='job-desc') else 'Not provided'
#                             post_date = card.find('span', class_='job-post-day').text.strip() if card.find('span', class_='job-post-day') else 'Unknown'

#                             job_data.append({
#                                 'Company': company_name,
#                                 'Role': job_title,
#                                 'Posted By': posted_by,
#                                 'Skills': skills,
#                                 'Link to Apply': job_url,
#                                 'Page Number': page,
#                                 'Experience': experience,
#                                 'Job Age': f"{job_age} days"
#                             })
#                         except Exception as e:
#                             print(f"❌ Error extracting job data: {e}")
#     return job_data

# # ===== DATA CLEANING FUNCTION =====
# def clean_data(data):
#     df = pd.DataFrame(data)

#     # Remove duplicates based on 'Role', 'Company', 'Link to Apply'
#     df.drop_duplicates(subset=['Role', 'Company', 'Link to Apply'], keep='first', inplace=True)

#     # Strip whitespace and clean text fields
#     for col in ['Role', 'Company', 'Posted By', 'Skills', 'Location']:
#         df[col] = df[col].str.strip().str.replace(r'\s+', ' ', regex=True).str.title()

#     # Handle missing values
#     df['Posted By'].fillna('Not Mentioned', inplace=True)
#     df['Skills'].fillna('Not Specified', inplace=True)
#     df['Experience'].fillna('Not Mentioned', inplace=True)
#     df['Location'].fillna('Not Specified', inplace=True)

#     # Convert experience format
#     df['Experience'] = df['Experience'].str.replace('Yrs', '').str.strip()

#     # Remove duplicate skills (if any)
#     df['Skills'] = df['Skills'].apply(lambda x: ', '.join(sorted(set(x.split(', ')))))

#     # === Mark as spam if company, role, posted by, and location appear more than twice ===
#     df['Spam'] = df.duplicated(subset=['Company', 'Role', 'Posted By', 'Location'], keep=False).groupby(df['Company']).transform('sum').gt(2).replace({True: 'Yes', False: 'No'})

#     return df
# from playwright.sync_api import sync_playwright
# # checking the application type
# def check_application_type(df):
#     def get_application_type(url):
#         with sync_playwright() as p:
#             browser = p.chromium.launch(headless=True)  # Use headless=True for background execution
#             page = browser.new_page()
#             try:
#                 page.goto(url, timeout=10000)

#                 # Check for "Apply" button
#                 apply_button = page.locator('text="Apply"').first
#                 apply_on_company_button = page.locator('text="Apply on Company Site"').first

#                 if apply_on_company_button.is_visible():
#                     return "Apply on Company Site"
#                 elif apply_button.is_visible():
#                     return "Apply"
#                 else:
#                     return "Not Found"
#             except Exception as e:
#                 print(f"Error processing {url}: {e}")
#                 return "Error"
#             finally:
#                 browser.close()

#     # Create a new column based on the extracted application type
#     df['Application Type'] = df['Link to Apply'].apply(get_application_type)

#     return df

# # ===== SAVE TO CSV =====
# def save_to_csv(data):
#     df = clean_data(data)
#     file_path = 'data/naukri_jobs_cleaned.csv'
#     df.to_csv(file_path, index=False)
#     print(f"✅ Cleaned data saved to '{file_path}' with {len(df)} rows")

# # ===== MAIN FUNCTION =====
# def main():
#     try:
#         login()
#         time.sleep(2)
#         job_data = extract_jobs()
#         if job_data:
#             save_to_csv(job_data)
#         else:
#             print("⚠️ No data to save.")
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     main()


import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from webdriver_manager.chrome import ChromeDriverManager

# ===== CONFIGURATION =====
load_dotenv('auth.env')

EMAIL = os.getenv('NAUKRI_EMAIL')
PASSWORD = os.getenv('NAUKRI_PASSWORD')

KEYWORDS = ['Angular Developer', 'Full Stack Developer']
JOB_AGES = [1, 3]
EXPERIENCES = [1]
MAX_PAGES = 5

# ===== DRIVER SETUP =====
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-extensions")
options.add_argument("--headless=new")  # Headless mode for faster execution

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ===== LOGIN FUNCTION =====
def login():
    print("🔐 Logging into Naukri...")
    driver.get('https://www.naukri.com/nlogin/login')

    time.sleep(5)  # Ensure page is fully loaded

    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        email_input.send_keys(EMAIL)

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        password_input.send_keys(PASSWORD + Keys.RETURN)

        time.sleep(5)

        # Handle CAPTCHA manually if needed
        if "captcha" in driver.page_source.lower():
            input("⚠️ Complete the CAPTCHA manually and press Enter to continue...")

        if "naukri.com" in driver.current_url:
            print("✅ Logged in successfully")
        else:
            raise Exception("❌ Login failed")
    except Exception as e:
        print(f"❌ Error during login: {e}")

# ===== SCROLL TO LOAD JOBS =====
def scroll_to_load_jobs():
    last_height = driver.execute_script("return document.body.scrollHeight")
    retries = 0
    while retries < 3:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            retries += 1
        else:
            retries = 0
        last_height = new_height

# ===== EXTRACT JOB DATA =====
def extract_jobs():
    job_data = []
    for keyword in KEYWORDS:
        for job_age in JOB_AGES:
            for experience in EXPERIENCES:
                print(f"\n🔎 Searching for '{keyword}' | Job Age: {job_age} days | Experience: {experience} years")
                
                search_url = f"https://www.naukri.com/{quote(keyword)}-jobs?k={quote(keyword)}&experience={experience}&jobAge={job_age}"
                driver.get(search_url)
                time.sleep(3)

                for page in range(1, MAX_PAGES + 1):
                    print(f"📄 Fetching Page {page} for '{keyword}'")

                    if page > 1:
                        driver.get(f"https://www.naukri.com/{quote(keyword)}-jobs-{page}?k={quote(keyword)}&experience={experience}&jobAge={job_age}")
                        time.sleep(3)

                    scroll_to_load_jobs()
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    job_cards = soup.find_all('div', class_='srp-jobtuple-wrapper')

                    if not job_cards:
                        print("🚫 No job cards found on this page.")
                        break

                    for card in job_cards:
                        try:
                            job = extract_card_data(card)
                            if job:
                                job_data.append(job)
                        except Exception as e:
                            print(f"❌ Error extracting job data: {e}")

                    # Check for "Next" button
                    next_button = driver.find_elements(By.CSS_SELECTOR, 'a[title="Next"]')
                    if not next_button:
                        print("🚫 No more pages.")
                        break

    return job_data

# ===== EXTRACT DATA FROM CARD =====
def extract_card_data(card):
    try:
        job_title = card.find('a', class_='title').text.strip()
        job_url = card.find('a', class_='title')['href']
        company_name = card.find('a', class_='comp-name').text.strip()
        posted_by = card.find('a', class_='client-name').text.strip() if card.find('a', class_='client-name') else 'Not mentioned'
        experience = card.find('span', class_='expwdth').text.strip() if card.find('span', class_='expwdth') else 'Not specified'
        salary = card.find('span', class_='sal').text.strip() if card.find('span', class_='sal') else 'Not disclosed'
        location = card.find('span', class_='locWdth').text.strip() if card.find('span', class_='locWdth') else 'Not specified'
        skills = ', '.join([skill.text.strip() for skill in card.find_all('li', class_='tag-li')])
        post_date = card.find('span', class_='job-post-day').text.strip() if card.find('span', class_='job-post-day') else 'Unknown'

        return {
            'Company': company_name,
            'Role': job_title,
            'Posted By': posted_by,
            'Skills': skills,
            'Link to Apply': job_url,
            'Experience': experience,
            'Location': location,
            'Post Date': post_date
        }
    except Exception as e:
        print(f"❌ Error extracting card data: {e}")
        return None

# ===== CHECK APPLICATION TYPE =====
def get_application_type(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=10000)
            if page.locator('text="Apply on Company Site"').first.is_visible():
                return "Apply on Company Site"
            if page.locator('text="Apply"').first.is_visible():
                return "Direct Apply"
            return "Not Found"
        except Exception:
            return "Error"
        finally:
            browser.close()

# ===== SAVE TO CSV =====
def save_to_csv(data):
    df = pd.DataFrame(data).drop_duplicates(subset=['Role', 'Company', 'Link to Apply'])
    df['Application Type'] = df['Link to Apply'].apply(get_application_type)
    file_path = 'data/naukri_jobs.csv'
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f"📁 Data saved to '{file_path}'")

# ===== MAIN FUNCTION =====
def main():
    login()
    data = extract_jobs()
    save_to_csv(data)
    driver.quit()

if __name__ == "__main__":
    main()
