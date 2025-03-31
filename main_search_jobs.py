# import os
# import time
# import random
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from dotenv import load_dotenv
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # ===== CONFIGURATION =====
# load_dotenv('auth.env')

# EMAIL = os.getenv('NAUKRI_EMAIL')
# PASSWORD = os.getenv('NAUKRI_PASSWORD')
# FIRST_NAME = os.getenv('FIRST_NAME')
# LAST_NAME = os.getenv('LAST_NAME')
# LOCATION = os.getenv('LOCATION')

# # ===== UPDATED FRONTEND KEYWORDS =====
# # KEYWORDS = [
# #     'Frontend Developer', 'Angular Developer', 'React Developer', 'Vue.js Developer',
# #     'JavaScript Developer', 'HTML CSS Developer', 'Web Developer', 'UI Developer',
# #     'UX Developer', 'Frontend Engineer', 'Web Engineer', 'Frontend Architect',
# #     'Next.js Developer', 'TypeScript Developer', 'Tailwind CSS Developer',
# #     'Bootstrap Developer', 'jQuery Developer', 'CSS Specialist', 'Frontend Consultant',
# #     'Frontend Designer', 'Full Stack Developer', 'React Native Developer']

# KEYWORDS = [
#     'Frontend Developer', 'Angular Developer','JavaScript Developer',
#       'Web Developer', 'UI Developer', 'Frontend Engineer',
#         'TypeScript Developer', 'Bootstrap Developer',"HTML Developer"
# ]
# MAX_SCROLLS = 50   # Increased for more search depth

# # ===== VARIABLES =====
# direct_apply_urls = []
# company_site_apply_urls = []

# # ===== DRIVER SETUP =====
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#                      "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")

# # Start Driver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # ===== LOGIN FUNCTION =====
# def login():
#     print("🚀 Logging into Naukri...")
#     driver.get('https://login.naukri.com/')
#     time.sleep(random.uniform(2, 4))

#     try:
#         WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'usernameField'))).send_keys(EMAIL)
#         WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'passwordField'))).send_keys(PASSWORD)
#         driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

#         # Confirm successful login
#         WebDriverWait(driver, 15).until(EC.url_contains('naukri.com'))
#         print("✅ Logged in successfully!")
#     except Exception as e:
#         print(f"❌ Login failed: {e}")
#         driver.quit()
#         exit()

# # ===== SEARCH FUNCTION =====
# def search_jobs():
#     for keyword in KEYWORDS:
#         print(f"\n🔎 Searching for '{keyword}' in '{LOCATION}'...")
#         search_url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{LOCATION.replace(' ', '-')}"
#         driver.get(search_url)
#         time.sleep(random.uniform(3, 5))

#         # Scroll to load more job cards
#         for _ in range(MAX_SCROLLS):
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#             time.sleep(random.uniform(1, 2))

#         # Extract job cards using BeautifulSoup
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         job_cards = soup.find_all('div', class_='cust-job-tuple')

#         if not job_cards:
#             print("❌ No job cards found!")
#             continue

#         print(f"✅ Found {len(job_cards)} job cards.")

#         for card in job_cards:
#             try:
#                 link = card.find('a', class_='title')['href']
                
#                 if link.startswith('/'):
#                     link = f"https://www.naukri.com{link}"

#                 # Open link in a new tab
#                 driver.execute_script(f"window.open('{link}', '_blank');")
#                 time.sleep(random.uniform(2, 4))
#                 driver.switch_to.window(driver.window_handles[-1])

#                 if handle_apply():
#                     direct_apply_urls.append(link)
#                 elif handle_company_site():
#                     company_site_apply_urls.append(link)

#                 # Close tab and switch back
#                 driver.close()
#                 driver.switch_to.window(driver.window_handles[0])

#             except Exception as e:
#                 print(f"❌ Failed to open job card: {e}")

# # ===== HANDLE APPLY BUTTON =====
# def handle_apply():
#     try:
#         apply_button = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.ID, 'apply-button'))
#         )
#         if apply_button.is_displayed():
#             apply_button.click()
#             print("✅ Direct Apply button clicked!")
#             time.sleep(random.uniform(2, 4))
#             return True
#         return False
#     except Exception:
#         return False

# # ===== HANDLE COMPANY SITE BUTTON =====
# def handle_company_site():
#     try:
#         company_site_button = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.ID, 'company-site-button'))
#         )
#         if company_site_button.is_displayed():
#             print("🌐 Redirecting to company site...")
#             company_site_button.click()
#             time.sleep(random.uniform(2, 4))
#             return True
#         return False
#     except Exception:
#         return False

# # ===== PAGINATION HANDLER =====
# def handle_pagination():
#     try:
#         while True:
#             next_button = WebDriverWait(driver, 3).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, 'styles_btn-secondary__2AsIP'))
#             )
#             if next_button and next_button.is_displayed():
#                 print("➡️ Navigating to next page...")
#                 next_button.click()
#                 time.sleep(random.uniform(2, 4))
#             else:
#                 break
#     except Exception:
#         pass

# # ===== SAVE TO CSV FUNCTION =====
# def save_urls_to_csv():
#     pd.DataFrame(direct_apply_urls, columns=['Direct Apply URL']).to_csv('data/direct_apply_urls.csv', index=False)
#     pd.DataFrame(company_site_apply_urls, columns=['Company Site Apply URL']).to_csv('data/company_site_apply_urls.csv', index=False)

#     print("\n✅ URLs saved to CSV files.")

# # ===== MAIN FUNCTION =====
# def main():
#     login()
#     search_jobs()
#     handle_pagination()
#     save_urls_to_csv()

#     print("\n===== ✅ Summary ✅ =====")
#     print(f"Direct Apply URLs: {len(direct_apply_urls)}")
#     print(f"Company Site Apply URLs: {len(company_site_apply_urls)}")

#     driver.quit()

# # ===== EXECUTE SCRIPT =====
# if __name__ == "__main__":
#     main()




"""updating the code in exp and job age 
---------------------------------
--------------------------------
---------------------------------------------"""
# import os
# import time
# import random
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from dotenv import load_dotenv
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # ===== CONFIGURATION =====
# load_dotenv('auth.env')

# EMAIL = os.getenv('NAUKRI_EMAIL_now')
# PASSWORD = os.getenv('NAUKRI_PASSWORD_now')
# FIRST_NAME = os.getenv('FIRST_NAME')
# LAST_NAME = os.getenv('LAST_NAME')
# LOCATION = os.getenv('LOCATION')

# KEYWORDS = ['Frontend Developer', 'Angular Developer', 'HTML/CSS Developer']
# MAX_SCROLLS = 30
# JOB_AGES = [3, 7]
# EXPERIENCES = [0, 1]

# # ===== VARIABLES =====
# direct_apply_urls = []
# company_site_apply_urls = []

# # ===== DRIVER SETUP =====
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-software-rasterizer")
# options.add_argument("--enable-unsafe-webgl")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # ===== LOGIN FUNCTION =====
# def login():
#     print("🚀 Logging into Naukri...")
#     driver.get('https://login.naukri.com/')
#     time.sleep(random.uniform(2, 4))

#     try:
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'usernameField'))).send_keys(EMAIL)
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'passwordField'))).send_keys(PASSWORD)
#         driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

#         WebDriverWait(driver, 15).until(EC.url_contains('naukri.com'))
#         print("✅ Logged in successfully!")
#     except Exception as e:
#         print(f"❌ Login failed: {e}")
#         driver.quit()
#         exit()

# # ===== SEARCH FUNCTION =====
# def search_jobs():
#     for keyword in KEYWORDS:
#         for job_age in JOB_AGES:
#             for experience in EXPERIENCES:
#                 print(f"\n🔎 Searching for '{keyword}' in '{LOCATION}' with job age '{job_age}' days and experience '{experience}' years...")
                
#                 search_url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs?k={keyword.replace(' ', '+')}&nignbevent_src=jobsearchDeskGNB&jobAge={job_age}&experience={experience}"
#                 driver.get(search_url)
#                 time.sleep(random.uniform(3, 5))

#                 # Scroll to load more jobs
#                 for _ in range(MAX_SCROLLS):
#                     driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#                     time.sleep(random.uniform(1, 2))

#                 soup = BeautifulSoup(driver.page_source, 'html.parser')
#                 job_cards = soup.find_all('div', class_='cust-job-tuple')

#                 if not job_cards:
#                     print("❌ No job cards found!")
#                     continue

#                 print(f"✅ Found {len(job_cards)} job cards.")
                
#                 for card in job_cards:
#                     try:
#                         link = card.find('a', class_='title')['href']
#                         if link.startswith('/'):
#                             link = f"https://www.naukri.com{link}"

#                         driver.execute_script(f"window.open('{link}', '_blank');")
#                         time.sleep(random.uniform(2, 4))
#                         driver.switch_to.window(driver.window_handles[-1])

#                         if handle_apply():
#                             direct_apply_urls.append(link)
#                         elif handle_company_site():
#                             company_site_apply_urls.append(link)

#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])
#                     except Exception as e:
#                         print(f"❌ Failed to open job card: {e}")

# # ===== HANDLE APPLY BUTTON =====
# def handle_apply():
#     try:
#         apply_button = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.ID, 'apply-button'))
#         )
#         if apply_button.is_displayed():
#             apply_button.click()
#             print("✅ Direct Apply button clicked!")
#             time.sleep(random.uniform(2, 4))
#             return True
#         return False
#     except Exception:
#         return False

# # ===== HANDLE COMPANY SITE BUTTON =====
# def handle_company_site():
#     try:
#         company_site_button = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.ID, 'company-site-button'))
#         )
#         if company_site_button.is_displayed():
#             print("🌐 Redirecting to company site...")
#             company_site_button.click()
#             time.sleep(random.uniform(2, 4))
#             return True
#         return False
#     except Exception:
#         return False

# # ===== PAGINATION HANDLER =====
# def handle_pagination():
#     try:
#         while True:
#             next_button = WebDriverWait(driver, 3).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, 'styles_btn-secondary__2AsIP'))
#             )
#             if next_button and next_button.is_displayed():
#                 print("➡️ Navigating to next page...")
#                 next_button.click()
#                 time.sleep(random.uniform(2, 4))
#             else:
#                 break
#     except Exception:
#         pass

# # ===== SAVE TO CSV FUNCTION =====
# def save_urls_to_csv():
#     pd.DataFrame(direct_apply_urls, columns=['Direct Apply URL']).to_csv('data/direct_apply_urls.csv', index=False)
#     pd.DataFrame(company_site_apply_urls, columns=['Company Site Apply URL']).to_csv('data/company_site_apply_urls.csv', index=False)

#     print("\n✅ URLs saved to CSV files.")

# # ===== MAIN FUNCTION =====
# def main():
#     login()
#     search_jobs()
#     handle_pagination()
#     save_urls_to_csv()

#     print("\n===== ✅ Summary ✅ =====")
#     print(f"Direct Apply URLs: {len(direct_apply_urls)}")
#     print(f"Company Site Apply URLs: {len(company_site_apply_urls)}")

#     driver.quit()

# # ===== EXECUTE SCRIPT =====
# if __name__ == "__main__":
#     main()



"""auto saving next after the job url opened
-------------------------------------------------------------

--------------------------------------------------

--------------------------------------------------------"""

# import os
# import time
# import random
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from dotenv import load_dotenv
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # ===== CONFIGURATION =====
# load_dotenv('auth.env')

# EMAIL = os.getenv('NAUKRI_EMAIL_now')
# PASSWORD = os.getenv('NAUKRI_PASSWORD_now')
# FIRST_NAME = os.getenv('FIRST_NAME')
# LAST_NAME = os.getenv('LAST_NAME')
# LOCATION = os.getenv('LOCATION')

# KEYWORDS = ['Frontend Developer', 'Angular Developer', 'HTML/CSS Developer']
# MAX_SCROLLS = 30
# JOB_AGES = [3, 7]
# EXPERIENCES = [0, 1]

# # ===== VARIABLES =====
# direct_apply_urls = []
# company_site_apply_urls = []

# # ===== DRIVER SETUP =====
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-software-rasterizer")
# options.add_argument("--enable-unsafe-webgl")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # ===== LOGIN FUNCTION =====
# def login():
#     print("🚀 Logging into Naukri...")
#     driver.get('https://login.naukri.com/')
#     time.sleep(random.uniform(2, 4))

#     try:
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'usernameField'))).send_keys(EMAIL)
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'passwordField'))).send_keys(PASSWORD)
#         driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

#         WebDriverWait(driver, 15).until(EC.url_contains('naukri.com'))
#         print("✅ Logged in successfully!")
#     except Exception as e:
#         print(f"❌ Login failed: {e}")
#         driver.quit()
#         exit()

# # ===== SEARCH FUNCTION =====
# def search_jobs():
#     for keyword in KEYWORDS:
#         for job_age in JOB_AGES:
#             for experience in EXPERIENCES:
#                 print(f"\n🔎 Searching for '{keyword}' in '{LOCATION}' with job age '{job_age}' days and experience '{experience}' years...")
                
#                 search_url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs?k={keyword.replace(' ', '+')}&nignbevent_src=jobsearchDeskGNB&jobAge={job_age}&experience={experience}"
#                 driver.get(search_url)
#                 time.sleep(random.uniform(3, 5))

#                 # Scroll to load more jobs
#                 for _ in range(MAX_SCROLLS):
#                     driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#                     time.sleep(random.uniform(1, 2))

#                 soup = BeautifulSoup(driver.page_source, 'html.parser')
#                 job_cards = soup.find_all('div', class_='cust-job-tuple')

#                 if not job_cards:
#                     print("❌ No job cards found!")
#                     continue

#                 print(f"✅ Found {len(job_cards)} job cards.")
                
#                 for card in job_cards:
#                     try:
#                         link = card.find('a', class_='title')['href']
#                         if link.startswith('/'):
#                             link = f"https://www.naukri.com{link}"

#                         driver.execute_script(f"window.open('{link}', '_blank');")
#                         time.sleep(random.uniform(2, 4))
#                         driver.switch_to.window(driver.window_handles[-1])

#                         if handle_apply():
#                             direct_apply_urls.append(link)
#                             save_single_url_to_csv(link, "direct_apply_urls.csv")
#                         elif handle_company_site():
#                             company_site_apply_urls.append(link)
#                             save_single_url_to_csv(link, "company_site_apply_urls.csv")

#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])
#                     except Exception as e:
#                         print(f"❌ Failed to open job card: {e}")

# # ===== HANDLE APPLY BUTTON =====
# def handle_apply():
#     try:
#         apply_button = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.ID, 'apply-button'))
#         )
#         if apply_button.is_displayed():
#             apply_button.click()
#             print("✅ Direct Apply button clicked!")
#             time.sleep(random.uniform(2, 4))
#             return True
#         return False
#     except Exception:
#         return False

# # ===== HANDLE COMPANY SITE BUTTON =====
# def handle_company_site():
#     try:
#         company_site_button = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.ID, 'company-site-button'))
#         )
#         if company_site_button.is_displayed():
#             print("🌐 Redirecting to company site...")
#             company_site_button.click()
#             time.sleep(random.uniform(2, 4))
#             return True
#         return False
#     except Exception:
#         return False

# # ===== PAGINATION HANDLER =====
# def handle_pagination():
#     try:
#         while True:
#             next_button = WebDriverWait(driver, 3).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, 'styles_btn-secondary__2AsIP'))
#             )
#             if next_button and next_button.is_displayed():
#                 print("➡️ Navigating to next page...")
#                 next_button.click()
#                 time.sleep(random.uniform(2, 4))
#             else:
#                 break
#     except Exception:
#         pass

# # ===== SAVE SINGLE URL TO CSV FUNCTION =====
# def save_single_url_to_csv(url, file_name):
#     try:
#         # Append data instead of overwriting
#         with open(f'data/{file_name}', 'a') as f:
#             f.write(url + '\n')
#         print(f"✅ Saved URL to '{file_name}': {url}")
#     except Exception as e:
#         print(f"❌ Failed to save URL: {e}")

# # ===== SAVE TO CSV FUNCTION =====
# def save_urls_to_csv():
#     pd.DataFrame(direct_apply_urls, columns=['Direct Apply URL']).to_csv('data/direct_apply_urls.csv', index=False)
#     pd.DataFrame(company_site_apply_urls, columns=['Company Site Apply URL']).to_csv('data/company_site_apply_urls.csv', index=False)

#     print("\n✅ URLs saved to CSV files.")

# # ===== MAIN FUNCTION =====
# def main():
#     login()
#     search_jobs()
#     handle_pagination()
#     save_urls_to_csv()

#     print("\n===== ✅ Summary ✅ =====")
#     print(f"Direct Apply URLs: {len(direct_apply_urls)}")
#     print(f"Company Site Apply URLs: {len(company_site_apply_urls)}")

#     driver.quit()

# # ===== EXECUTE SCRIPT =====
# if __name__ == "__main__":
#     main()


"""----------------------------
------------------------
------------------

nav to 10 pages and finding

----------------------
---------------------
-------------------"""


# import os
# import time
# import random
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from dotenv import load_dotenv
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # ===== CONFIGURATION =====
# load_dotenv('auth.env')

# EMAIL = os.getenv('NAUKRI_EMAIL_now')
# PASSWORD = os.getenv('NAUKRI_PASSWORD_now')
# FIRST_NAME = os.getenv('FIRST_NAME')
# LAST_NAME = os.getenv('LAST_NAME')
# LOCATION = os.getenv('LOCATION')

# KEYWORDS = ['Frontend Developer', 'Angular Developer', 'HTML/CSS Developer']
# MAX_SCROLLS = 30
# JOB_AGES = [3, 7]
# EXPERIENCES = [0, 1]
# MAX_PAGES = 10

# # ===== VARIABLES =====
# direct_apply_urls = []
# company_site_apply_urls = []

# # ===== DRIVER SETUP =====
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-software-rasterizer")
# options.add_argument("--enable-unsafe-webgl")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # ===== LOGIN FUNCTION =====
# # def login():
# #     print("🚀 Logging into Naukri...")
# #     driver.get('https://login.naukri.com/')
# #     time.sleep(random.uniform(2, 4))

# #     try:
# #         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'usernameField'))).send_keys(EMAIL)
# #         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'passwordField'))).send_keys(PASSWORD)
# #         driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

# #         WebDriverWait(driver, 15).until(EC.url_contains('naukri.com'))
# #         print("✅ Logged in successfully!")
# #     except Exception as e:
# #         print(f"❌ Login failed: {e}")
# #         driver.quit()
# #         exit()
# def login():
#     print("🚀 Logging into Naukri...")
#     driver.get('https://login.naukri.com/')
#     time.sleep(random.uniform(2, 4))

#     try:
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'usernameField'))).send_keys(EMAIL)
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'passwordField'))).send_keys(PASSWORD)
#         driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

#         WebDriverWait(driver, 15).until(EC.url_contains('naukri.com'))
#         print("✅ Logged in successfully!")
#     except Exception as e:
#         print(f"❌ Login failed: {e}")
#         driver.quit()
#         exit()
# # ===== SEARCH FUNCTION =====
# """def search_jobs():
#     for keyword in KEYWORDS:
#         for job_age in JOB_AGES:
#             for experience in EXPERIENCES:
#                 for page in range(1, MAX_PAGES + 1):
#                     print(f"\n🔎 Searching for '{keyword}' in '{LOCATION}' with job age '{job_age}' days, experience '{experience}' years on page '{page}'...")
                    
#                     if page == 1:
#                         search_url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs?k={keyword.replace(' ', '+')}&nignbevent_src=jobsearchDeskGNB&experience={experience}&jobAge={job_age}"
#                     else:
#                         search_url = f"https://www.naukri.com/{keyword.replace(' ','-')}-jobs-{page}?k={keyword.replace(' ', '+')}&nignbevent_src=jobsearchDeskGNB&experience={experience}&jobAge={job_age}"
#                     driver.get(search_url)
#                     time.sleep(random.uniform(3, 5))

#                     # Scroll to load more jobs
#                     for _ in range(MAX_SCROLLS):
#                         driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#                         time.sleep(random.uniform(1, 2))

#                     soup = BeautifulSoup(driver.page_source, 'html.parser')
#                     job_cards = soup.find_all('div', class_='cust-job-tuple')

#                     if not job_cards:
#                         print("❌ No job cards found!")
#                         continue

#                     print(f"✅ Found {len(job_cards)} job cards.")

#                     for card in job_cards:
#                         try:
#                             link = card.find('a', class_='title')['href']
#                             if link.startswith('/'):
#                                 link = f"https://www.naukri.com{link}"

#                             driver.execute_script(f"window.open('{link}', '_blank');")
#                             time.sleep(random.uniform(2, 4))
#                             driver.switch_to.window(driver.window_handles[-1])

#                             if handle_apply():
#                                 direct_apply_urls.append(link)
#                                 save_single_url_to_csv(link, "direct_apply_urls.csv")
#                             elif handle_company_site():
#                                 company_site_apply_urls.append(link)
#                                 save_single_url_to_csv(link, "company_site_apply_urls.csv")

#                             driver.close()
#                             driver.switch_to.window(driver.window_handles[0])
#                         except Exception as e:
#                             print(f"❌ Failed to open job card: {e}")
# """
# def search_jobs():
#     visited_urls = set()  # ✅ Track visited URLs to avoid duplicates

#     for keyword in KEYWORDS:
#         for job_age in JOB_AGES:
#             for experience in EXPERIENCES:
#                 print(f"\n🔎 Searching for '{keyword}' with job age '{job_age}' days and experience '{experience}' years...")

#                 for page in range(1, MAX_PAGES + 1):
#                     print(f"➡️ Loading Page {page}...")

#                     # ✅ Clean and consistent URL handling
#                     if page == 1 and experience == 0:
#                         search_url = f"https://www.naukri.com/{'-'.join(keyword.split())}-jobs?k={'+'.join(keyword.split())}&nignbevent_src=jobsearchDeskGNB&experience={experience}&jobAge={job_age}"
#                     else:
#                         search_url = f"https://www.naukri.com/{'-'.join(keyword.split())}-jobs-{page}?k={'+'.join(keyword.split())}&nignbevent_src=jobsearchDeskGNB&experience={experience}&jobAge={job_age}"

#                     # ✅ Load the page
#                     driver.get(search_url)
#                     time.sleep(random.uniform(3, 5))

#                     # ✅ Scroll to load more jobs
#                     for _ in range(MAX_SCROLLS):
#                         driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#                         time.sleep(random.uniform(1, 2))

#                     soup = BeautifulSoup(driver.page_source, 'html.parser')
#                     job_cards = soup.find_all('div', class_='cust-job-tuple')

#                     if not job_cards:
#                         print("❌ No job cards found!")
#                         break

#                     print(f"✅ Found {len(job_cards)} job cards.")

#                     for card in job_cards:
#                         try:
#                             # ✅ Extract job link
#                             link = card.find('a', class_='title')['href']
#                             if link.startswith('/'):
#                                 link = f"https://www.naukri.com{link}"

#                             # ✅ Skip if already visited
#                             if link in visited_urls:
#                                 print(f"⚠️ Skipping duplicate URL: {link}")
#                                 continue

#                             visited_urls.add(link)  # ✅ Mark as visited

#                             # ✅ Open job link in a new tab
#                             driver.execute_script(f"window.open('{link}', '_blank');")
#                             time.sleep(random.uniform(2, 4))
#                             driver.switch_to.window(driver.window_handles[-1])

#                             if handle_apply():
#                                 direct_apply_urls.append(link)
#                                 save_single_url_to_csv(link, "direct_apply_urls.csv")
#                             elif handle_company_site():
#                                 company_site_apply_urls.append(link)
#                                 save_single_url_to_csv(link, "company_site_apply_urls.csv")

#                             # ✅ Close tab and switch back to main window
#                             driver.close()
#                             driver.switch_to.window(driver.window_handles[0])

#                         except Exception as e:
#                             print(f"❌ Failed to open job card: {e}")

#                     # ✅ Stop if no more jobs are available
#                     if len(job_cards) == 0:
#                         break
# # ===== HANDLE APPLY BUTTON =====
# def handle_apply():
#     try:
#         apply_button = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.ID, 'apply-button'))
#         )
#         if apply_button.is_displayed():
#             apply_button.click()
#             print("✅ Direct Apply button clicked!")
#             time.sleep(random.uniform(2, 4))
#             return True
#         return False
#     except Exception:
#         return False

# # ===== HANDLE COMPANY SITE BUTTON =====
# def handle_company_site():
#     try:
#         company_site_button = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.ID, 'company-site-button'))
#         )
#         if company_site_button.is_displayed():
#             print("🌐 Redirecting to company site...")
#             company_site_button.click()
#             time.sleep(random.uniform(2, 4))
#             return True
#         return False
#     except Exception:
#         return False

# # ===== SAVE SINGLE URL TO CSV FUNCTION =====
# def save_single_url_to_csv(url, file_name):
#     try:
#         with open(f'data/{file_name}', 'a') as f:
#             f.write(url + '\n')
#         print(f"✅ Saved URL to '{file_name}': {url}")
#     except Exception as e:
#         print(f"❌ Failed to save URL: {e}")

# # ===== SAVE TO CSV FUNCTION =====
# def save_urls_to_csv():
#     pd.DataFrame(direct_apply_urls, columns=['Direct Apply URL']).to_csv('data/direct_apply_urls.csv', index=False)
#     pd.DataFrame(company_site_apply_urls, columns=['Company Site Apply URL']).to_csv('data/company_site_apply_urls.csv', index=False)

#     print("\n✅ URLs saved to CSV files.")

# # ===== MAIN FUNCTION =====
# def main():
#     login()
#     search_jobs()
#     save_urls_to_csv()

#     print("\n===== ✅ Summary ✅ =====")
#     print(f"Direct Apply URLs: {len(direct_apply_urls)}")
#     print(f"Company Site Apply URLs: {len(company_site_apply_urls)}")

#     driver.quit()

# # ===== EXECUTE SCRIPT =====
# if __name__ == "__main__":
#     main()



"""auto loop to pages """

# import os
# import time
# import random
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from dotenv import load_dotenv
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # ===== CONFIGURATION =====
# load_dotenv('auth.env')

# EMAIL = os.getenv('NAUKRI_EMAIL_now')
# PASSWORD = os.getenv('NAUKRI_PASSWORD_now')
# FIRST_NAME = os.getenv('FIRST_NAME')
# LAST_NAME = os.getenv('LAST_NAME')
# LOCATION = os.getenv('LOCATION')

# KEYWORDS = ['Frontend Developer', 'Angular Developer', 'HTML/CSS Developer']
# MAX_SCROLLS = 30
# JOB_AGES = [3]   # ✅ Only 3 days
# EXPERIENCES = [0, 1]

# # ===== VARIABLES =====
# direct_apply_urls = []
# company_site_apply_urls = []

# # ===== DRIVER SETUP =====
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-software-rasterizer")
# options.add_argument("--enable-unsafe-webgl")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # ===== LOGIN FUNCTION =====
# def login():
#     print("🚀 Logging into Naukri...")
#     driver.get('https://login.naukri.com/')
#     time.sleep(random.uniform(2, 4))

#     try:
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'usernameField'))).send_keys(EMAIL)
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'passwordField'))).send_keys(PASSWORD)
#         driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

#         WebDriverWait(driver, 15).until(EC.url_contains('naukri.com'))
#         print("✅ Logged in successfully!")
#     except Exception as e:
#         print(f"❌ Login failed: {e}")
#         driver.quit()
#         exit()

# # ===== SEARCH FUNCTION =====
# def search_jobs():
#     for keyword in KEYWORDS:
#         for job_age in JOB_AGES:
#             for experience in EXPERIENCES:
#                 print(f"\n🔎 Searching for '{keyword}' in '{LOCATION}' with job age '{job_age}' days and experience '{experience}' years...")

#                 # First page URL
#                 search_url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs?k={keyword.replace(' ', '+')}&nignbevent_src=jobsearchDeskGNB&jobAge={job_age}&experience={experience}"
#                 driver.get(search_url)
#                 time.sleep(random.uniform(3, 5))

#                 # Get total number of pages dynamically
#                 total_pages = get_total_pages()
#                 print(f"📄 Total Pages Found: {total_pages}")

#                 for page in range(1, total_pages + 1):
#                     print(f"\n➡️ Loading Page {page} of {total_pages}...")
                    
#                     if page == 1:
#                         driver.get(search_url)
#                     else:
#                         search_url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-{page}?k={keyword.replace(' ', '+')}&nignbevent_src=jobsearchDeskGNB&jobAge={job_age}&experience={experience}"
#                         driver.get(search_url)
                    
#                     time.sleep(random.uniform(3, 5))

#                     # Scroll to load more jobs
#                     for _ in range(MAX_SCROLLS):
#                         driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#                         time.sleep(random.uniform(1, 2))

#                     soup = BeautifulSoup(driver.page_source, 'html.parser')
#                     job_cards = soup.find_all('div', class_='cust-job-tuple')

#                     if not job_cards:
#                         print("❌ No job cards found!")
#                         continue

#                     print(f"✅ Found {len(job_cards)} job cards.")

#                     for card in job_cards:
#                         try:
#                             link = card.find('a', class_='title')['href']
#                             if link.startswith('/'):
#                                 link = f"https://www.naukri.com{link}"

#                             driver.execute_script(f"window.open('{link}', '_blank');")
#                             time.sleep(random.uniform(2, 4))
#                             driver.switch_to.window(driver.window_handles[-1])

#                             if handle_apply():
#                                 direct_apply_urls.append(link)
#                                 save_single_url_to_csv(link, "direct_apply_urls.csv")
#                             elif handle_company_site():
#                                 company_site_apply_urls.append(link)
#                                 save_single_url_to_csv(link, "company_site_apply_urls.csv")

#                             driver.close()
#                             driver.switch_to.window(driver.window_handles[0])
#                         except Exception as e:
#                             print(f"❌ Failed to open job card: {e}")

# # ===== GET TOTAL PAGES =====
# # def get_total_pages():
# #     try:
# #         soup = BeautifulSoup(driver.page_source, 'html.parser')
# #         pagination = soup.find('div', class_='styles_pages__v1rAK')
# #         if pagination:
# #             pages = pagination.find_all('a')
# #             last_page = int(pages[-1].text.strip()) if pages else 1
# #             return last_page
# #         return 1
# #     except Exception:
# #         return 1
# def get_total_pages():
#     try:
#         # Wait for pagination to load
#         WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.CLASS_NAME, 'styles_pages__v1rAK'))
#         )
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         pagination = soup.find('div', class_='styles_pages__v1rAK')
#         if pagination:
#             # Extract numeric pages only
#             pages = [a.text.strip() for a in pagination.find_all('a')]
#             numeric_pages = [int(p) for p in pages if p.isdigit()]
#             if numeric_pages:
#                 last_page = max(numeric_pages)
#                 return last_page
#         return 1
#     except Exception as e:
#         print(f"❌ Failed to detect pagination: {e}")
#         return 1


# # ===== HANDLE APPLY BUTTON =====
# def handle_apply():
#     try:
#         apply_button = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.ID, 'apply-button'))
#         )
#         if apply_button.is_displayed():
#             apply_button.click()
#             print("✅ Direct Apply button clicked!")
#             time.sleep(random.uniform(2, 4))
#             return True
#         return False
#     except Exception:
#         return False

# # ===== HANDLE COMPANY SITE BUTTON =====
# def handle_company_site():
#     try:
#         company_site_button = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.ID, 'company-site-button'))
#         )
#         if company_site_button.is_displayed():
#             print("🌐 Redirecting to company site...")
#             company_site_button.click()
#             time.sleep(random.uniform(2, 4))
#             return True
#         return False
#     except Exception:
#         return False

# # ===== SAVE SINGLE URL TO CSV FUNCTION =====
# def save_single_url_to_csv(url, file_name):
#     try:
#         with open(f'data/{file_name}', 'a') as f:
#             f.write(url + '\n')
#         print(f"✅ Saved URL to '{file_name}': {url}")
#     except Exception as e:
#         print(f"❌ Failed to save URL: {e}")

# # ===== SAVE TO CSV FUNCTION =====
# def save_urls_to_csv():
#     pd.DataFrame(direct_apply_urls, columns=['Direct Apply URL']).to_csv('data/direct_apply_urls.csv', index=False)
#     pd.DataFrame(company_site_apply_urls, columns=['Company Site Apply URL']).to_csv('data/company_site_apply_urls.csv', index=False)
#     print("\n✅ URLs saved to CSV files.")

# # ===== MAIN FUNCTION =====
# def main():
#     login()
#     search_jobs()
#     save_urls_to_csv()

#     print("\n===== ✅ Summary ✅ =====")
#     print(f"Direct Apply URLs: {len(direct_apply_urls)}")
#     print(f"Company Site Apply URLs: {len(company_site_apply_urls)}")

#     driver.quit()

# # ===== EXECUTE SCRIPT =====
# if __name__ == "__main__":
#     main()




'''
----------------
-----------------
cleaning the code 
-----------------
-----------------
'''
# import os
# import time
# import random
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from dotenv import load_dotenv
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # ===== CONFIGURATION =====
# load_dotenv('auth.env')

# EMAIL = os.getenv('NAUKRI_EMAIL_now')
# PASSWORD = os.getenv('NAUKRI_PASSWORD_now')
# LOCATION = os.getenv('LOCATION')

# KEYWORDS = ['Angular Developer', 'Html,css', "frontend developer"]
# MAX_SCROLLS = 10
# JOB_AGES = [3]
# EXPERIENCES = [1]
# MAX_PAGES = 10

# # ===== VARIABLES =====
# direct_apply_urls = set()  # ✅ Use set to avoid duplicates
# company_site_apply_urls = set()

# # ===== DRIVER SETUP =====
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-software-rasterizer")
# options.add_argument("--enable-unsafe-webgl")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # ===== LOGIN FUNCTION =====
# # def login():
# #     print("🚀 Logging into Naukri...")
# #     driver.get('https://login.naukri.com/')
# #     time.sleep(random.uniform(2, 4))

# #     try:
# #         WebDriverWait(driver, 10).until(
# #             EC.presence_of_element_located((By.ID, 'usernameField'))
# #         ).send_keys(EMAIL)
# #         WebDriverWait(driver, 10).until(
# #             EC.presence_of_element_located((By.ID, 'passwordField'))
# #         ).send_keys(PASSWORD)
# #         driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

# #         WebDriverWait(driver, 15).until(EC.url_contains('naukri.com'))
# #         print("✅ Logged in successfully!")
# #     except Exception as e:
# #         print(f"❌ Login failed: {e}")
# #         driver.quit()
# #         exit()
# def login():
#     print("🚀 Logging into Naukri...")
#     driver.get('https://login.naukri.com/')
#     time.sleep(random.uniform(2, 4))

#     try:
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'usernameField'))).send_keys(EMAIL)
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'passwordField'))).send_keys(PASSWORD)
#         driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

#         WebDriverWait(driver, 15).until(EC.url_contains('naukri.com'))
#         print("✅ Logged in successfully!")
#     except Exception as e:
#         print(f"❌ Login failed: {e}")
#         driver.quit()
#         exit()

# # ===== SEARCH FUNCTION =====
# def search_jobs():
#     for keyword in KEYWORDS:
#         for job_age in JOB_AGES:
#             for experience in EXPERIENCES:
#                 print(f"\n🔎 Searching for '{keyword}' with job age '{job_age}' days and experience '{experience}' years...")

#                 # ✅ First page URL
#                 search_url = f"https://www.naukri.com/{'-'.join(keyword.split())}-jobs?k={'+'.join(keyword.split())}&nignbevent_src=jobsearchDeskGNB&experience={experience}&jobAge={job_age}"
#                 driver.get(search_url)
#                 time.sleep(random.uniform(3, 5))

#                 # ✅ Get total pages dynamically
#                 total_pages = get_total_pages()
#                 print(f"📄 Total Pages Found: {total_pages}")

#                 for page in range(1, total_pages + 1):
#                     print(f"\n➡️ Loading Page {page} of {total_pages}...")

#                     if page > 1:
#                         search_url = f"https://www.naukri.com/{'-'.join(keyword.split())}-jobs-{page}?k={'+'.join(keyword.split())}&nignbevent_src=jobsearchDeskGNB&experience={experience}&jobAge={job_age}"
#                         driver.get(search_url)

#                     time.sleep(random.uniform(3, 5))

#                     # ✅ Scroll to load more jobs
#                     for _ in range(MAX_SCROLLS):
#                         driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#                         time.sleep(random.uniform(1, 2))

#                     soup = BeautifulSoup(driver.page_source, 'html.parser')
#                     job_cards = soup.find_all('div', class_='cust-job-tuple')

#                     if not job_cards:
#                         print("❌ No job cards found!")
#                         continue

#                     print(f"✅ Found {len(job_cards)} job cards.")

#                     for card in job_cards:
#                         try:
#                             link = card.find('a', class_='title')['href']
#                             if link.startswith('/'):
#                                 link = f"https://www.naukri.com{link}"

#                             # ✅ Skip duplicate URLs
#                             if link in direct_apply_urls or link in company_site_apply_urls:
#                                 continue

#                             driver.execute_script(f"window.open('{link}', '_blank');")
#                             time.sleep(random.uniform(2, 4))
#                             driver.switch_to.window(driver.window_handles[-1])

#                             if handle_apply():
#                                 direct_apply_urls.add(link)
#                                 save_single_url_to_csv(link, "direct_apply_urls.csv")
#                             elif handle_company_site():
#                                 company_site_apply_urls.add(link)
#                                 save_single_url_to_csv(link, "company_site_apply_urls.csv")

#                             driver.close()
#                             driver.switch_to.window(driver.window_handles[0])
#                         except Exception as e:
#                             print(f"❌ Failed to open job card: {e}")

# # ===== GET TOTAL PAGES =====
# def get_total_pages():
#     try:
#         WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.CLASS_NAME, 'styles_pages__v1rAK'))
#         )
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         pagination = soup.find('div', class_='styles_pages__v1rAK')

#         if pagination:
#             pages = pagination.find_all('a')
#             numeric_pages = [int(a.text.strip()) for a in pages if a.text.strip().isdigit()]
#             if numeric_pages:
#                 return max(numeric_pages)

#         return 1
#     except Exception as e:
#         print(f"❌ Failed to detect pagination: {e}")
#         return 1

# # ===== HANDLE APPLY BUTTON =====
# def handle_apply():
#     try:
#         apply_button = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.ID, 'apply-button'))
#         )
#         if apply_button.is_displayed():
#             apply_button.click()
#             time.sleep(random.uniform(2, 4))
#             return True
#         return False
#     except Exception:
#         return False

# # ===== HANDLE COMPANY SITE BUTTON =====
# def handle_company_site():
#     try:
#         company_site_button = WebDriverWait(driver, 3).until(
#             EC.presence_of_element_located((By.ID, 'company-site-button'))
#         )
#         if company_site_button.is_displayed():
#             company_site_button.click()
#             time.sleep(random.uniform(2, 4))
#             return True
#         return False
#     except Exception:
#         return False

# # ===== SAVE TO CSV FUNCTION =====
# # # def save_single_url_to_csv(url, file_name):
# # #     with open(f'data/{file_name}', 'a') as f:
# # #         f.write(url + '\n')
# # #     print(f"✅ Saved URL to '{file_name}': {url}")

# # def save_single_url_to_csv(url, file_name):
# #     file_path = f'data/{file_name}'
    
# #     # Ensure the directory exists
# #     os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
# #     existing_urls = set()

# #     # ✅ Read from all CSV files in the 'data' directory
# #     if os.path.exists('data'):
# #         for csv_file in os.listdir('data'):
# #             if csv_file.endswith('.csv'):
# #                 file_path = os.path.join('data', csv_file)
# #                 try:
# #                     df = pd.read_csv(file_path)
# #                     if 'URL' in df.columns:
# #                         existing_urls.update(df['URL'].tolist())
# #                 except Exception as e:
# #                     print(f"❌ Error reading {csv_file}: {e}")
    
# #     # ✅ Skip if URL already exists in any CSV file
# #     if url in existing_urls:
# #         print(f"🔁 URL already added: {url}")
# #     else:
# #         with open(file_path, 'a') as f:
# #             f.write(url + '\n')
# #         print(f"✅ Saved URL to '{file_name}': {url}")


# # # def save_urls_to_csv():
# # #     pd.DataFrame(list(direct_apply_urls), columns=['Direct Apply URL']).to_csv('data/direct_apply_urls.csv', index=False)
# # #     pd.DataFrame(list(company_site_apply_urls), columns=['Company Site Apply URL']).to_csv('data/company_site_apply_urls.csv', index=False)
# # def save_urls_to_csv():
# #     all_existing_urls = set()

# #     # ✅ Read from all CSV files in the 'data' directory
# #     if os.path.exists('data'):
# #         for csv_file in os.listdir('data'):
# #             if csv_file.endswith('.csv'):
# #                 file_path = os.path.join('data', csv_file)
# #                 try:
# #                     df = pd.read_csv(file_path)
# #                     if 'URL' in df.columns:
# #                         all_existing_urls.update(df['URL'].tolist())
# #                 except Exception as e:
# #                     print(f"❌ Error reading {csv_file}: {e}")

# #     # ✅ Save Direct Apply URLs (skip duplicates)
# #     new_direct_apply_urls = [url for url in direct_apply_urls if url not in all_existing_urls]
# #     if new_direct_apply_urls:
# #         df = pd.DataFrame(new_direct_apply_urls, columns=['URL'])
# #         df.to_csv('data/direct_apply_urls.csv', mode='a', header=not os.path.exists('data/direct_apply_urls.csv'), index=False)
# #         print(f"✅ Added {len(new_direct_apply_urls)} new direct apply URLs.")
# #     else:
# #         print("🔁 No new direct apply URLs to add.")

# #     # ✅ Save Company Site Apply URLs (skip duplicates)
# #     new_company_site_apply_urls = [url for url in company_site_apply_urls if url not in all_existing_urls]
# #     if new_company_site_apply_urls:
# #         df = pd.DataFrame(new_company_site_apply_urls, columns=['URL'])
# #         df.to_csv('data/company_site_apply_urls.csv', mode='a', header=not os.path.exists('data/company_site_apply_urls.csv'), index=False)
# #         print(f"✅ Added {len(new_company_site_apply_urls)} new company site apply URLs.")
# #     else:
# #         print("🔁 No new company site apply URLs to add.")
# # ===== SAVE SINGLE URL TO CSV =====
# def save_single_url_to_csv(url, file_name):
#     file_path = f'data/{file_name}'
    
#     # Ensure the directory exists
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
#     existing_urls = set()

#     # ✅ Read from all CSV files in the 'data' directory
#     if os.path.exists('data'):
#         for csv_file in os.listdir('data'):
#             if csv_file.endswith('.csv'):
#                 try:
#                     df = pd.read_csv(os.path.join('data', csv_file))
#                     if 'URL' in df.columns:
#                         existing_urls.update(df['URL'].tolist())
#                 except Exception as e:
#                     print(f"❌ Error reading '{csv_file}': {e}")
    
#     # ✅ Skip if URL already exists in any CSV file
#     if url in existing_urls:
#         print(f"🔁 URL already exists: {url}")
#     else:
#         with open(file_path, 'a') as f:
#             f.write(url + '\n')
#         print(f"✅ Saved URL to '{file_name}': {url}")


# # ===== SAVE MULTIPLE URLS TO CSV =====
# def save_urls_to_csv():
#     all_existing_urls = set()

#     # ✅ Read from all CSV files in the 'data' directory
#     if os.path.exists('data'):
#         for csv_file in os.listdir('data'):
#             if csv_file.endswith('.csv'):
#                 file_path = os.path.join('data', csv_file)
#                 try:
#                     df = pd.read_csv(file_path)
#                     if 'URL' in df.columns:
#                         all_existing_urls.update(df['URL'].tolist())
#                 except Exception as e:
#                     print(f"❌ Error reading '{csv_file}': {e}")

#     # ✅ Save Direct Apply URLs (skip duplicates)
#     new_direct_apply_urls = [url for url in direct_apply_urls if url not in all_existing_urls]
#     if new_direct_apply_urls:
#         df = pd.DataFrame(new_direct_apply_urls, columns=['URL'])
#         df.to_csv('data/direct_apply_urls.csv', mode='a', header=not os.path.exists('data/direct_apply_urls.csv'), index=False)
#         print(f"✅ Added {len(new_direct_apply_urls)} new direct apply URLs.")
#     else:
#         print("🔁 No new direct apply URLs to add.")

#     # ✅ Save Company Site Apply URLs (skip duplicates)
#     new_company_site_apply_urls = [url for url in company_site_apply_urls if url not in all_existing_urls]
#     if new_company_site_apply_urls:
#         df = pd.DataFrame(new_company_site_apply_urls, columns=['URL'])
#         df.to_csv('data/company_site_apply_urls.csv', mode='a', header=not os.path.exists('data/company_site_apply_urls.csv'), index=False)
#         print(f"✅ Added {len(new_company_site_apply_urls)} new company site apply URLs.")
#     else:
#         print("🔁 No new company site apply URLs to add.")

# # ===== MAIN FUNCTION =====
# def main():
#     login()
#     search_jobs()
#     save_urls_to_csv()

#     print("\n===== ✅ Summary ✅ =====")
#     print(f"Direct Apply URLs: {len(direct_apply_urls)}")
#     print(f"Company Site Apply URLs: {len(company_site_apply_urls)}")

#     driver.quit()

# # ===== EXECUTE SCRIPT =====
# if __name__ == "__main__":
#     main()


"""
----------------
-----------------
final cleaning the code
-----------------
-----------------
"""
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

# # ===== SEARCH JOBS =====
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
#                         driver.get(f"{search_url}-{page}")
#                         time.sleep(2)
                    
#                     scroll_to_load_jobs()
#                     process_job_cards()

# # ===== SCROLL TO LOAD JOBS =====
# def scroll_to_load_jobs():
#     try:
#         for _ in range(MAX_SCROLLS):
#             driver.execute_script("window.scrollBy(0, 800);")
#             time.sleep(random.uniform(1, 2))
#     except Exception as e:
#         print(f"❌ Error while scrolling: {e}")

# # ===== PROCESS JOB CARDS =====
# def process_job_cards():
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

#             if handle_company_site():
#                 save_to_csv(company, link, "company_site_apply_urls.csv")
#                 applied = True

#             if not applied and handle_apply():
#                 save_to_csv(company, link, "direct_apply_urls.csv")

#             # Close job tab
#             driver.close()
#             driver.switch_to.window(driver.window_handles[0])

#         except Exception as e:
#             print(f"❌ Error processing job card: {e}")

# # ===== HANDLE APPLY =====
# def handle_apply():
#     try:
#         apply_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Apply')]")
#         for button in apply_buttons:
#             try:
#                 if button.is_displayed():
#                     print(f"▶ Clicking direct apply button: {button.text}")
#                     button.click()
#                     time.sleep(3)

#                     # Success check based on URL or success message
#                     if driver.current_url != "about:blank":
#                         print("✅ Direct apply successful")
#                         return True
#             except StaleElementReferenceException:
#                 continue
#     except Exception as e:
#         print(f"❌ Error clicking apply: {e}")
#     return False

# # ===== HANDLE COMPANY SITE APPLY =====
# def handle_company_site():
#     try:
#         company_site_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Apply on company site')]")
#         for button in company_site_buttons:
#             try:
#                 if button.is_displayed():
#                     print(f"▶ Clicking company site apply button: {button.text}")
#                     button.click()
#                     time.sleep(3)
                    
#                     # Handle new window
#                     if len(driver.window_handles) > 2:
#                         print("✅ Company site apply successful")
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
# def save_to_csv(company, url, filename):
#     try:
#         # Create a DataFrame with the data
#         data = {'Company': [company], 'URL': [url]}
#         df = pd.DataFrame(data)

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
import os
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import quote
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException

# ===== CONFIGURATION =====
load_dotenv('auth.env')

EMAIL = os.getenv('NAUKRI_EMAIL_now')
PASSWORD = os.getenv('NAUKRI_PASSWORD_now')
LOCATION = os.getenv('LOCATION')

KEYWORDS = [
    "angular developer",
    "angular frontend developer",
    "html5 css3 javascript",
    "angular angular-cli",
    "angular angular-material bootstrap",
    "nodejs developer",
    "rest api developer",
    "database developer",
    "data science",
    "python developer",
    "machine learning engineer",
    "data analysis",
    "data visualization",
    "statistical modeling",
]

JOB_AGES = [1]
EXPERIENCES = [0, 1, 2]
MAX_SCROLLS = 7
MAX_PAGES = 5

# ===== DRIVER SETUP =====
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-extensions")

# Start the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ===== LOGIN FUNCTION =====
def login():
    print("🔐 Logging into Naukri...")
    driver.get('https://login.naukri.com/')
    time.sleep(3)
    driver.find_element(By.ID, 'usernameField').send_keys(EMAIL)
    driver.find_element(By.ID, 'passwordField').send_keys(PASSWORD + Keys.RETURN)
    time.sleep(5)
    if "naukri.com" in driver.current_url:
        print("✅ Logged in successfully")
    else:
        print("❌ Login failed")

# # # ===== SEARCH JOBS =====
# def search_jobs():
#     for keyword in KEYWORDS:
#         for job_age in JOB_AGES:
#             for experience in EXPERIENCES:
#                 # print(f"\n🔎 Searching for '{keyword}' with job age '{job_age}' days and experience '{experience}' years...")
#                 # search_url = f"https://www.naukri.com/{quote(keyword)}-jobs?k={quote(keyword)}&experience={experience}&jobAge={job_age}"
                
#                 # driver.get(search_url)
#                 # time.sleep(2)

#                 for page in range(2, MAX_PAGES + 1):
#                     if page > 1:
#                         print(f"\n🔎 Searching for '{keyword}' with job age '{job_age}' days and experience '{experience}' years...page{page}")
#                         driver.get(f"https://www.naukri.com/{quote(keyword)}-jobs-{page}?k={quote(keyword)}&nignbevent_src=jobsearchDeskGNB&experience={experience}&jobAge={job_age}")
#                         print(f"https://www.naukri.com/{quote(keyword)}-jobs-{page}?k={quote(keyword)}&nignbevent_src=jobsearchDeskGNB&experience={experience}&jobAge={job_age}")
#                         time.sleep(2)
                    
#                     scroll_to_load_jobs()
#                     process_job_cards(keyword, job_age)
# ===== pages are loading but age and exp not loading SEARCH JOBS =====
# def search_jobs():
#     for keyword in KEYWORDS:
#         for job_age in JOB_AGES:
#             for experience in EXPERIENCES:
#                 for page in range(2, MAX_PAGES + 1):
#                     if page > 1:
#                         formatted_keyword = keyword.replace(" ", "-")  # ✅ Fix spaces in keyword
#                         search_url = (
#                             f"https://www.naukri.com/{formatted_keyword}-jobs-{page}?k={formatted_keyword}&nignbevent_src=jobsearchDeskGNB&experience={experience}&jobAge={job_age}"
#                         )
#                         print(f"\n🔎 Searching for '{keyword}' with job age '{job_age}' days and experience '{experience}' years... page {page}")
#                         print(search_url)

#                         driver.get(search_url)
#                         time.sleep(2)
                    
#                     scroll_to_load_jobs()
#                     process_job_cards(keyword, job_age)
# ===== loading all pages, exp, job age SEARCH JOBS =====
def search_jobs():
    for keyword in KEYWORDS:
        for job_age in JOB_AGES:
            for experience in EXPERIENCES:
                 # ✅ Handle Page 1 separately (without -page in URL)
                formatted_keyword_path = keyword.replace(" ", "-").lower()
                formatted_keyword_query = keyword.replace(" ", "+").lower()

                search_url = (
                    f"https://www.naukri.com/{formatted_keyword_path}-jobs"
                    f"?k={formatted_keyword_query}&nignbevent_src=jobsearchDeskGNB"
                    f"&experience={experience}&jobAge={job_age}"
                )

                print(f"\n🔎 Searching for '{keyword}' with job age '{job_age}' days and experience '{experience}' years... page 1")
                print(search_url)

                driver.get(search_url)
                time.sleep(2)
                
                scroll_to_load_jobs()
                process_job_cards(keyword, job_age)
                for page in range(2, MAX_PAGES + 1):
                    if page > 1:
                        # Use '-' for URL path and '+' for query parameters
                        formatted_keyword_path = keyword.replace(" ", "-").lower()  # ✅ Use hyphen and lowercase in path
                        formatted_keyword_query = keyword.replace(" ", "+").lower()  # ✅ Use plus sign and lowercase in query

                        search_url = (
                            f"https://www.naukri.com/{formatted_keyword_path}-jobs-{page}"
                            f"?k={formatted_keyword_query}&nignbevent_src=jobsearchDeskGNB"
                            f"&experience={experience}&jobAge={job_age}"
                        )

                        print(f"\n🔎 Searching for '{keyword}' with job age '{job_age}' days and experience '{experience}' years... page {page}")
                        print(search_url)

                        driver.get(search_url)
                        time.sleep(2)
                    
                    scroll_to_load_jobs()
                    process_job_cards(keyword, job_age)


# ===== SCROLL TO LOAD JOBS =====
def scroll_to_load_jobs():
    try:
        for _ in range(MAX_SCROLLS):
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(random.uniform(1, 2))
    except Exception as e:
        print(f"❌ Error while scrolling: {e}")

# ===== PROCESS JOB CARDS =====
def process_job_cards(keyword, job_age):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_cards = soup.find_all('div', class_='cust-job-tuple')

    if not job_cards:
        print("⚠️ No jobs found on this page.")
        return

    for card in job_cards:
        try:
            link = card.find('a', class_='title')['href']
            company = card.find('a', class_='comp-name').text.strip() if card.find('a', class_='comp-name') else "Unknown"

            if link.startswith('/'):
                link = f"https://www.naukri.com{link}"

            # Open job in new tab
            driver.execute_script(f"window.open('{link}', '_blank');")
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[-1])


            # Parse job details
            job_soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Extract job title
            job_title = job_soup.find('h1', class_='styles_jd-header-title__rZwM1').text.strip() if job_soup.find('h1', class_='styles_jd-header-title__rZwM1') else "Unknown"

            # Extract posted by
            posted_by = job_soup.find('div', class_='styles_consultant-posted-by__Vb6Hq')
            if posted_by:
                posted_by = posted_by.find('a').text.strip() if posted_by.find('a') else "Unknown"
            else:
                posted_by = "Unknown"
            
            #log job details
            print(f"Job Title: {job_title}")
            print(f"Company: {company}")
            print(f"Posted By: {posted_by}")

            applied = False

            if handle_company_site(keyword, link, job_age, company, posted_by, job_title):
                applied = True

            if not applied and handle_apply(keyword, link, job_age, company, posted_by, job_title):
                applied = True

            # Close job tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"❌ Error processing job card: {e}")

# ===== HANDLE APPLY (Direct) =====
def handle_apply(keyword, link, job_age, company, posted_by, job_title):
    try:
        apply_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Apply')]")
        for button in apply_buttons:
            try:
                if button.is_displayed() and "Apply on company site" not in button.text:
                    print(f"▶ Clicking direct apply button: {button.text}")
                    button.click()
                    time.sleep(3)

                    # Success check based on URL or success message
                    if driver.current_url != "about:blank":
                        print("✅ Direct apply successful")
                        save_to_csv(keyword, link, job_age, company, "Direct",  posted_by, job_title)
                        return True
            except StaleElementReferenceException:
                continue
    except Exception as e:
        print(f"❌ Error clicking direct apply: {e}")
    return False

# ===== HANDLE COMPANY SITE APPLY =====
def handle_company_site(keyword, link, job_age, company, posted_by, job_title):
    try:
        company_site_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Apply on company site')]")
        for button in company_site_buttons:
            try:
                if button.is_displayed():
                    print(f"▶ Clicking company site apply button: {button.text}")
                    button.click()
                    time.sleep(3)
                    
                    # Handle new window
                    if len(driver.window_handles) > 2:
                        print("✅ Company site apply successful")
                        save_to_csv(keyword, link, job_age, company, "Company Site", posted_by, job_title)
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        return True
            except StaleElementReferenceException:
                continue
    except Exception as e:
        print(f"❌ Error clicking company site apply: {e}")
    return False

# ===== SAVE TO CSV =====
def save_to_csv(keyword, url, job_age, company, apply_type, posted_by, job_title):
    try:
        # Create a DataFrame with the data
        data = {
            'Keyword': [keyword],
            'Company': [company],
            'Job Title': [job_title],
            'Posted By': [posted_by],
            'URL': [url],
            'Job Age (Days)': [job_age],
            'Apply Type': [apply_type]
        }
        df = pd.DataFrame(data)

        filename = "data/jobs_apply_urls.csv"

        # Write to CSV, append without writing headers if file exists
        if not os.path.isfile(filename):
            df.to_csv(filename, index=False)
        else:
            df.to_csv(filename, mode='a', header=False, index=False)

        print(f"✅ Saved URL to {filename}")
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")

# ===== RUN SCRIPT =====
if __name__ == "__main__":
    try:
        login()
        search_jobs()
    except KeyboardInterrupt:
        print("\n🛑 Stopping script...")
    except Exception as e:
        print(f"❌ Error running script: {e}")
    finally:
        driver.quit()
        print("🚪 Driver closed.")


"""----------------------main--------------------colsed-----------------------------------"""
"""----------------------main--------------------colsed-----------------------------------"""
"""----------------------main--------------------colsed-----------------------------------"""
"""----------------------main--------------------colsed-----------------------------------"""
"""----------------------main--------------------colsed-----------------------------------"""
"""i have a thougth that company or org name and posted by 
edxample cards in this we can see right 
Full Stack Developer 

Leading Client
Posted by Rudr Consultancy Services
1-3 Yrs
Not disclosed
Jaipur
Full Stack Developer . Job Name: Full StackDeveloper . Job Role: Developer Industry:Sof...
csswebsocketxmlapinode.jsfullstack developmentserver sideapi integration
1 Day Ago
save
Angular Developer

Leading Client
Posted by Rudr Consultancy Services"""
"""i have an idea that store the data for company ,position, role, posted by, url of tab to apply  and all from the card it self without going in to the other tab to open 
example stoping to nav in tab by this content stage 
<div class="srp-jobtuple-wrapper" data-job-id="260325921629"><div class="cust-job-tuple layout-wrapper lay-2 sjw__tuple "><div class=" row1"><h2><a class="title " title="Full Stack Developer" href="https://www.naukri.com/job-listings-full-stack-developer-rudr-consultancy-services-jaipur-1-to-3-years-260325921629" target="_blank" rel="noopener noreferrer">Full Stack Developer</a></h2><span class="imagewrap "><img src="https://img.naukimg.com/logo_images/groups/v1/2413086.gif" class="logoImage" loading="lazy"></span></div><div class=" row2"><span class="rm-cursor-pointer comp-dtls-wrap"><a class=" comp-name " title="Leading Client" target="_blank">Leading Client</a></span> <div class="client-company-name"><a target="_blank" title="Posted by Rudr Consultancy Services" href="https://www.naukri.com/rudr-consultancy-services-jobs-careers-2523810">Posted by Rudr Consultancy Services</a></div> </div><div class=" row3"><div class="job-details "><span class="exp-wrap"><span class="ni-job-tuple-icon ni-job-tuple-icon-srp-experience exp"><span title="1-3 Yrs " class="expwdth">1-3 Yrs</span></span></span><span class="sal-wrap ver-line"><span class="ni-job-tuple-icon ni-job-tuple-icon-srp-rupee sal"><span title="Not disclosed " class="">Not disclosed</span></span></span><span class="loc-wrap ver-line"><span class="ni-job-tuple-icon ni-job-tuple-icon-srp-location loc"><span title="Jaipur " class="locWdth">Jaipur</span></span></span></div></div><div class=" row4"><span class="job-desc ni-job-tuple-icon ni-job-tuple-icon-srp-description">Full Stack Developer . Job Name: Full StackDeveloper . Job Role: Developer Industry:Sof...</span></div><div class=" row5"><ul class="tags-gt "><li class="dot-gt tag-li ">css</li><li class="dot-gt tag-li ">websocket</li><li class="dot-gt tag-li ">xml</li><li class="dot-gt tag-li ">api</li><li class="dot-gt tag-li ">node.js</li><li class="dot-gt tag-li ">fullstack development</li><li class="dot-gt tag-li ">server side</li><li class="dot-gt tag-li ">api integration</li></ul></div><div class=" row6">  <span class="job-post-day ">1 Day Ago</span><span class="ni-job-tuple-icon ni-job-tuple-icon-srpSaveUnfilled un-saved save-job-tag">save</span></div></div></div>
we can save time and get all the data from the card it self
i need a final complete code not showing the code"""

