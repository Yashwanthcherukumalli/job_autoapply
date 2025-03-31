import os
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===== CONFIGURATION =====
load_dotenv('auth.env')

EMAIL = os.getenv('NAUKRI_EMAIL_now')
PASSWORD = os.getenv('NAUKRI_PASSWORD_now')
FIRST_NAME = os.getenv('FIRST_NAME')
LAST_NAME = os.getenv('LAST_NAME')
LOCATION = os.getenv('LOCATION')

KEYWORDS = ['Frontend Developer', 'Angular Developer', 'React Developer']
MAX_SCROLLS = 20
JOB_AGES = [3, 7, 15, 30]
EXPERIENCES = [0, 1, 2]

# ===== VARIABLES =====
direct_apply_urls = []
company_site_apply_urls = []
results = []

# ===== DRIVER SETUP =====
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--enable-unsafe-webgl")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ===== LOGIN FUNCTION =====
def login():
    print("🚀 Logging into Naukri...")
    driver.get('https://login.naukri.com/')
    time.sleep(random.uniform(2, 4))

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'usernameField'))).send_keys(EMAIL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'passwordField'))).send_keys(PASSWORD)
        driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

        WebDriverWait(driver, 15).until(EC.url_contains('naukri.com'))
        print("✅ Logged in successfully!")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        driver.quit()
        exit()

# ===== SEARCH FUNCTION =====
def search_jobs():
    for keyword in KEYWORDS:
        for job_age in JOB_AGES:
            for experience in EXPERIENCES:
                print(f"\n🔎 Searching for '{keyword}' in '{LOCATION}' with job age '{job_age}' days and experience '{experience}' years...")
                
                search_url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs?k={keyword.replace(' ', '+')}&nignbevent_src=jobsearchDeskGNB&jobAge={job_age}&experience={experience}"
                driver.get(search_url)
                time.sleep(random.uniform(3, 5))

                # Scroll to load more jobs
                for _ in range(MAX_SCROLLS):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(random.uniform(1, 2))

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                job_cards = soup.find_all('div', class_='cust-job-tuple')

                if not job_cards:
                    print("❌ No job cards found!")
                    continue

                print(f"✅ Found {len(job_cards)} job cards.")
                
                for card in job_cards:
                    try:
                        link = card.find('a', class_='title')['href']
                        if link.startswith('/'):
                            link = f"https://www.naukri.com{link}"

                        driver.execute_script(f"window.open('{link}', '_blank');")
                        time.sleep(random.uniform(2, 4))
                        driver.switch_to.window(driver.window_handles[-1])

                        apply_type = None
                        if handle_apply():
                            direct_apply_urls.append(link)
                            apply_type = 'Direct Apply'
                        elif handle_company_site():
                            company_site_apply_urls.append(link)
                            apply_type = 'Company Site'

                        if apply_type:
                            results.append({
                                'Keyword': keyword,
                                'Experience': experience,
                                'Job Age': job_age,
                                'URL': link,
                                'Apply Type': apply_type
                            })

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    except Exception as e:
                        print(f"❌ Failed to open job card: {e}")

                # ✅ Save progress after completing each keyword, job age, and experience combination
                save_results_to_csv()
                print(f"✅ Successfully completed '{keyword}' with job age '{job_age}' days and experience '{experience}' years")

# ===== HANDLE APPLY BUTTON =====
def handle_apply():
    try:
        apply_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'apply-button'))
        )
        if apply_button.is_displayed():
            apply_button.click()
            print("✅ Direct Apply button clicked!")
            time.sleep(random.uniform(2, 4))
            return True
        return False
    except Exception:
        return False

# ===== HANDLE COMPANY SITE BUTTON =====
def handle_company_site():
    try:
        company_site_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'company-site-button'))
        )
        if company_site_button.is_displayed():
            print("🌐 Redirecting to company site...")
            company_site_button.click()
            time.sleep(random.uniform(2, 4))
            return True
        return False
    except Exception:
        return False

# ===== PAGINATION HANDLER =====
def handle_pagination():
    try:
        while True:
            next_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'styles_btn-secondary__2AsIP'))
            )
            if next_button and next_button.is_displayed():
                print("➡️ Navigating to next page...")
                next_button.click()
                time.sleep(random.uniform(2, 4))
            else:
                break
    except Exception:
        pass

# ===== SAVE TO CSV FUNCTION =====
def save_results_to_csv():
    pd.DataFrame(results).to_csv('data/job_results.csv', index=False)

# ===== SAVE URLS TO CSV FUNCTION =====
def save_urls_to_csv():
    pd.DataFrame(direct_apply_urls, columns=['Direct Apply URL']).to_csv('data/direct_apply_urls.csv', index=False)
    pd.DataFrame(company_site_apply_urls, columns=['Company Site Apply URL']).to_csv('data/company_site_apply_urls.csv', index=False)

# ===== MAIN FUNCTION =====
def main():
    login()
    search_jobs()
    handle_pagination()
    save_urls_to_csv()

    print("\n===== ✅ Summary ✅ =====")
    print(f"Direct Apply URLs: {len(direct_apply_urls)}")
    print(f"Company Site Apply URLs: {len(company_site_apply_urls)}")

    driver.quit()

# ===== EXECUTE SCRIPT =====
if __name__ == "__main__":
    main()


"""final code with saving all columsn and rows """
"""----------------------------------------------m-------a--------i-----------n--------------------------------"""
"""----------------------------------------------m-------a--------i-----------n--------------------------------"""
"""----------------------------------------------m-------a--------i-----------n--------------------------------"""
"""----------------------------------------------m-------a--------i-----------n--------------------------------"""
"""----------------------------------------------m-------a--------i-----------n--------------------------------"""
"""----------------------------------------------m-------a--------i-----------n--------------------------------"""
"""----------------------------------------------m-------a--------i-----------n--------------------------------"""
"""----------------------------------------------m-------a--------i-----------n--------------------------------"""
"""----------------------------------------------m-------a--------i-----------n--------------------------------"""
"""----------------------------------------------m-------a--------i-----------n--------------------------------"""
"""----------------------------------------------m-------a--------i-----------n--------------------------------"""
# import os
# import time
# import random
# import pandas as pd
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# from urllib.parse import quote
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException

# # ===== CONFIGURATION =====
# load_dotenv('auth.env')

# EMAIL = os.getenv('NAUKRI_EMAIL_now')
# PASSWORD = os.getenv('NAUKRI_PASSWORD_now')
# LOCATION = os.getenv('LOCATION')

# KEYWORDS = ['Angular Developer', 'Html,css', "frontend developer"]
# JOB_AGES = [1, 3]
# EXPERIENCES = [1]
# MAX_SCROLLS = 7
# MAX_PAGES = 10

# # ===== DRIVER SETUP =====
# options = Options()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--incognito")
# options.add_argument("--disable-popup-blocking")
# options.add_argument("--disable-extensions")

# # Start the driver
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

# # # ===== SEARCH JOBS =====
# def search_jobs():
#     for keyword in KEYWORDS:
#         for job_age in JOB_AGES:
#             for experience in EXPERIENCES:
#                 print(f"\n🔎 Searching for '{keyword}' with job age '{job_age}' days and experience '{experience}' years...")
#                 search_url = f"https://www.naukri.com/{quote(keyword)}-jobs?k={quote(keyword)}&experience={experience}&jobAge={job_age}"
                
#                 driver.get(search_url)
#                 time.sleep(2)

#                 for page in range(1, MAX_PAGES + 1):
#                     if page > 1:
#                         print(f"\n🔎 Searching for '{keyword}' with job age '{job_age}' days and experience '{experience}' years...page{page}")
#                         driver.get(f"https://www.naukri.com/{quote(keyword)}-jobs-{page}?k={quote(keyword)}&experience={experience}&jobAge={job_age}")
#                         time.sleep(2)
                    
#                     scroll_to_load_jobs()
#                     process_job_cards(keyword, job_age)

# # ===== SCROLL TO LOAD JOBS =====
# def scroll_to_load_jobs():
#     try:
#         for _ in range(MAX_SCROLLS):
#             driver.execute_script("window.scrollBy(0, 800);")
#             time.sleep(random.uniform(1, 2))
#     except Exception as e:
#         print(f"❌ Error while scrolling: {e}")

# # ===== PROCESS JOB CARDS =====
# def process_job_cards(keyword, job_age):
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     job_cards = soup.find_all('div', class_='cust-job-tuple')

#     if not job_cards:
#         print("⚠️ No jobs found on this page.")
#         return

#     for card in job_cards:
#         try:
#             link = card.find('a', class_='title')['href']
#             company = card.find('a', class_='comp-name').text.strip() if card.find('a', class_='comp-name') else "Unknown"

#             if link.startswith('/'):
#                 link = f"https://www.naukri.com{link}"

#             # Open job in new tab
#             driver.execute_script(f"window.open('{link}', '_blank');")
#             time.sleep(3)
#             driver.switch_to.window(driver.window_handles[-1])

#             applied = False

#             if handle_company_site(keyword, link, job_age, company):
#                 applied = True

#             if not applied and handle_apply(keyword, link, job_age, company):
#                 applied = True

#             # Close job tab
#             driver.close()
#             driver.switch_to.window(driver.window_handles[0])

#         except Exception as e:
#             print(f"❌ Error processing job card: {e}")

# # ===== HANDLE APPLY (Direct) =====
# def handle_apply(keyword, link, job_age, company):
#     try:
#         apply_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Apply')]")
#         for button in apply_buttons:
#             try:
#                 if button.is_displayed() and "Apply on company site" not in button.text:
#                     print(f"▶ Clicking direct apply button: {button.text}")
#                     button.click()
#                     time.sleep(3)

#                     # Success check based on URL or success message
#                     if driver.current_url != "about:blank":
#                         print("✅ Direct apply successful")
#                         save_to_csv(keyword, link, job_age, company, "Direct")
#                         return True
#             except StaleElementReferenceException:
#                 continue
#     except Exception as e:
#         print(f"❌ Error clicking direct apply: {e}")
#     return False

# # ===== HANDLE COMPANY SITE APPLY =====
# def handle_company_site(keyword, link, job_age, company):
#     try:
#         company_site_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Apply on company site')]")
#         for button in company_site_buttons:
#             try:
#                 if button.is_displayed():
#                     print(f"▶ Clicking company site apply button: {button.text}")
#                     button.click()
#                     time.sleep(3)
                    
#                     # Handle new window
#                     if len(driver.window_handles) > 2:
#                         print("✅ Company site apply successful")
#                         save_to_csv(keyword, link, job_age, company, "Company Site")
#                         driver.switch_to.window(driver.window_handles[-1])
#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])
#                         return True
#             except StaleElementReferenceException:
#                 continue
#     except Exception as e:
#         print(f"❌ Error clicking company site apply: {e}")
#     return False

# # ===== SAVE TO CSV =====
# def save_to_csv(keyword, url, job_age, company, apply_type):
#     try:
#         # Create a DataFrame with the data
#         data = {
#             'Keyword': [keyword],
#             'Company': [company],
#             'URL': [url],
#             'Job Age (Days)': [job_age],
#             'Apply Type': [apply_type]
#         }
#         df = pd.DataFrame(data)

#         filename = "data/jobs_apply_urls.csv"

#         # Write to CSV, append without writing headers if file exists
#         if not os.path.isfile(filename):
#             df.to_csv(filename, index=False)
#         else:
#             df.to_csv(filename, mode='a', header=False, index=False)

#         print(f"✅ Saved URL to {filename}")
#     except Exception as e:
#         print(f"❌ Error saving to CSV: {e}")

# # ===== RUN SCRIPT =====
# if __name__ == "__main__":
#     try:
#         login()
#         search_jobs()
#     except KeyboardInterrupt:
#         print("\n🛑 Stopping script...")
#     except Exception as e:
#         print(f"❌ Error running script: {e}")
#     finally:
#         driver.quit()
#         print("🚪 Driver closed.")


"""----------------------main--------------------colsed-----------------------------------"""
"""----------------------main--------------------colsed-----------------------------------"""
"""----------------------main--------------------colsed-----------------------------------"""
"""----------------------main--------------------colsed-----------------------------------"""
"""----------------------main--------------------colsed-----------------------------------"""
