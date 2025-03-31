# import os
# import time
# import pandas as pd
# from dotenv import load_dotenv
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

# # ===== CONFIGURATION =====
# load_dotenv('auth.env')

# EMAIL = os.getenv('NAUKRI_EMAIL_now')
# PASSWORD = os.getenv('NAUKRI_PASSWORD_now')
# FIRST_NAME = os.getenv('FIRST_NAME')
# LAST_NAME = os.getenv('LAST_NAME')

# MAX_APPLY_COUNT = 100

# # ===== VARIABLES =====
# applied = 0
# failed = 0
# application_status = []

# # ===== DRIVER SETUP =====
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-blink-features=AutomationControlled")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # ===== LOGIN FUNCTION =====
# def login():
#     print("🚀 Logging into Naukri...")
#     driver.get('https://login.naukri.com/')
#     time.sleep(5)

#     driver.find_element(By.ID, 'usernameField').send_keys(EMAIL)
#     driver.find_element(By.ID, 'passwordField').send_keys(PASSWORD)
#     driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

#     print("✅ Logged in successfully!")
#     time.sleep(5)

# # ===== APPLY FROM CSV =====
# def apply_from_csv():
#     global applied, failed
#     urls = pd.read_csv('data/cleaned_direct_apply_urls.csv')['Direct Apply URL'].tolist()

#     for url in urls:
#         if applied >= MAX_APPLY_COUNT:
#             break
#         print(f"🌐 Opening job URL: {url}")
#         driver.get(url)

# # ✅ Wait 30 seconds before attempting to apply
#         print("🕒 Waiting 30 seconds to ensure full page load...")
#         time.sleep(30)

# #  # ✅ Scroll to bottom to load all dynamic elements
# #     print("📜 Scrolling to the bottom of the page...")
# #     scroll_pause_time = 1  # Adjust based on page load speed
# #     last_height = driver.execute_script("return document.body.scrollHeight")

# #     while True:
# #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# #         time.sleep(scroll_pause_time)
        
# #         new_height = driver.execute_script("return document.body.scrollHeight")
# #         if new_height == last_height:
# #             break
# #         last_height = new_height

#         try:
#             # Check if apply button exists
#             if driver.find_elements(By.ID, 'apply-button'):
#                 driver.find_element(By.ID, 'apply-button').click()
#                 time.sleep(3)

#                 # Check for error message after clicking apply
#                 error_message = driver.find_elements(By.CSS_SELECTOR, 'section.styles_user-msg__YLRsE.styles_error__PZ5op span')
#                 if error_message:
#                     print(f"❌ Error while applying to {url}: {error_message[0].text}")
#                     failed += 1
#                     break
                    

#                 print(f"✅ Applied successfully to {url}")
#                 application_status.append({'URL': url, 'Status': 'Applied'})
#                 applied += 1
#             else:
#                 print(f"❌ No apply button found for {url}")
#                 failed += 1
#                 application_status.append({'URL': url, 'Status': 'Failed'})
#         except Exception as e:
#             print(f"❌ Failed to apply: {e}")
#             failed += 1
#             break

# # ===== SAVE STATUS =====
# def save_status():
#     pd.DataFrame(application_status).to_csv('data/application_status.csv', index=False)
#     print("✅ Application status saved.")

# # ===== MAIN FUNCTION =====
# def main():
#     login()
#     apply_from_csv()
#     save_status()

#     print(f"Direct Applies: {applied}")
#     print(f"Failed Attempts: {failed}")

#     driver.quit()

# if __name__ == "__main__":
#     main()

"""apply button notifier """

# import os 
# import time
# import pandas as pd
# from dotenv import load_dotenv
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

# # ===== CONFIGURATION =====
# load_dotenv('auth.env')

# EMAIL = os.getenv('NAUKRI_EMAIL_now')
# PASSWORD = os.getenv('NAUKRI_PASSWORD_now')
# FIRST_NAME = os.getenv('FIRST_NAME')
# LAST_NAME = os.getenv('LAST_NAME')

# MAX_APPLY_COUNT = 100

# # ===== VARIABLES =====
# applied = 0
# failed = 0
# application_status = []

# # ===== DRIVER SETUP =====
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-blink-features=AutomationControlled")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # ===== LOGIN FUNCTION =====
# def login():
#     print("🚀 Logging into Naukri...")
#     driver.get('https://login.naukri.com/')
#     time.sleep(5)

#     driver.find_element(By.ID, 'usernameField').send_keys(EMAIL)
#     driver.find_element(By.ID, 'passwordField').send_keys(PASSWORD)
#     driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

#     print("✅ Logged in successfully!")
#     time.sleep(5)

# # ===== APPLY FROM CSV =====
# def apply_from_csv():
#     global applied, failed
#     urls = pd.read_csv('data/cleaned_direct_apply_urls.csv')['Direct Apply URL'].tolist()

#     for url in urls:
#         if applied >= MAX_APPLY_COUNT:
#             break
        
#         print(f"🌐 Opening job URL: {url}")
#         driver.get(url)

#         # ✅ Wait 30 seconds to ensure full page load
#         print("🕒 Waiting 120 seconds to ensure full page load...")
#         time.sleep(3)

#         try:
#             # ✅ Check if "Already Applied" button exists
#             already_applied = driver.find_elements(By.ID, 'already-applied')
#             if already_applied:
#                 print(f"⚠️ Already applied for {url}. Skipping to next URL...")
#                 application_status.append({'URL': url, 'Status': 'Already Applied'})
#                 continue
            
#             # ✅ Check if apply button exists
#             apply_button = driver.find_elements(By.ID, 'apply-button')
#             if apply_button:
#                 apply_button[0].click()
#                 application_status.append({'URL': url, 'Status': 'Already Applied'})
#                 time.sleep(3)

#                 # ✅ Check for error message after clicking apply
#                 error_message = driver.find_elements(By.CSS_SELECTOR, 'section.styles_user-msg__YLRsE.styles_error__PZ5op span')
#                 if error_message:
#                     print(f"❌ Error while applying to {url}: {error_message[0].text}")
#                     failed += 1
#                     application_status.append({'URL': url, 'Status': 'Failed'})
#                     continue

#                 print(f"✅ Applied successfully to {url}")
#                 application_status.append({'URL': url, 'Status': 'Applied'})
#                 applied += 1
#             else:
#                 print(f"❌ No apply button found for {url}")
#                 failed += 1
#                 application_status.append({'URL': url, 'Status': 'No Apply Button'})
        
#         except Exception as e:
#             print(f"❌ Failed to apply: {e}")
#             failed += 1
#             application_status.append({'URL': url, 'Status': f'Error: {str(e)}'})

# # ===== SAVE STATUS =====
# def save_status():
#     status_df = pd.DataFrame(application_status)
    
#     # ✅ Append to existing application_status.csv if it exists
#     if os.path.exists('data/application_status.csv'):
#         existing_df = pd.read_csv('data/application_status.csv')
#         status_df = pd.concat([existing_df, status_df], ignore_index=True)
    
#     # ✅ Remove duplicates
#     status_df.drop_duplicates(subset=['URL'], keep='last', inplace=True)
    
#     # ✅ Save the final result
#     status_df.to_csv('data/application_status.csv', index=False)
#     print("✅ Application status saved.")

# # ===== MAIN FUNCTION =====
# def main():
#     login()
#     apply_from_csv()
#     save_status()

#     print(f"✅ Direct Applies: {applied}")
#     print(f"❌ Failed Attempts: {failed}")

#     driver.quit()

# # ===== EXECUTE SCRIPT =====
# if __name__ == "__main__":
#     main()



""""
apply status updater
"""

import os 
import time
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# ===== CONFIGURATION =====
load_dotenv('auth.env')

EMAIL = os.getenv('NAUKRI_EMAIL')
PASSWORD = os.getenv('NAUKRI_PASSWORD')
FIRST_NAME = os.getenv('FIRST_NAME')
LAST_NAME = os.getenv('LAST_NAME')

MAX_APPLY_COUNT = 100

# ===== VARIABLES =====
applied = 0
failed = 0

# ===== DRIVER SETUP =====
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ===== LOGIN FUNCTION =====
def login():
    print("🚀 Logging into Naukri...")
    driver.get('https://login.naukri.com/')
    time.sleep(10)

    driver.find_element(By.ID, 'usernameField').send_keys(EMAIL)
    driver.find_element(By.ID, 'passwordField').send_keys(PASSWORD)
    driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

    print("✅ Logged in successfully!")
    time.sleep(15)

# ===== original APPLY FROM CSV =====
# def apply_from_csv():
#     global applied, failed
#     urls = pd.read_csv('data/cleaned_direct_apply_urls.csv')['DirectApplyURL'].tolist()

#     for url in urls:
#         if applied >= MAX_APPLY_COUNT:
#             break
        
#         print(f"🌐 Opening job URL: {url}")
#         driver.get(url)

#         # ✅ Wait to ensure full page load
#         print("🕒 Waiting 30 seconds to ensure full page load...")
#         time.sleep(30)

#         try:
#             # ✅ Check if "Already Applied" button exists
#             already_applied = driver.find_elements(By.ID, 'already-applied')
#             conpanysite = driver.find_elements(By.ID, 'company-site-button')
#             if already_applied:
#                 print(f"⚠️ Already applied for {url}. Skipping to next URL...")
#                 save_status(url, 'Already Applied')
#                 continue
#             if conpanysite:
#                 print(f"⚠️ company site {url}. Skipping to next URL...")
#                 save_status(url, 'company site')
#                 continue
            
#             # ✅ Check if apply button exists
#             apply_button = driver.find_elements(By.ID, 'apply-button')
#             if apply_button:
#                 apply_button[0].click()
#                 time.sleep(60)

#                 # ✅ Check for error message after clicking apply
#                 error_message = driver.find_elements(By.CSS_SELECTOR, 'section.styles_user-msg__YLRsE.styles_error__PZ5op span')
#                 if error_message:
#                     print(f"❌ Error while applying to {url}: {error_message[0].text}")
#                     save_status(url, 'Failed')
#                     failed += 1
#                     continue

#                 print(f"✅ Applied successfully to {url}")
#                 save_status(url, 'Applied')
#                 applied += 1
#             else:
#                 print(f"❌ No apply button found for {url}")
#                 save_status(url, 'No Apply Button')
#                 failed += 1
        
#         except Exception as e:
#             print(f"❌ Failed to apply: {e}")
#             save_status(url, f'Error: {str(e)}')
#             failed += 1
# ===== APPLY FROM CSV ===== 
def apply_from_csv():
    global applied, failed
    urls = pd.read_csv('data/cleaned_direct_apply_urls.csv')['DirectApplyURL'].tolist()

    for url in urls:
        if applied >= MAX_APPLY_COUNT:
            break
        
        print(f"🌐 Opening job URL: {url}")
        driver.get(url)

        # ✅ Wait to ensure full page load
        print("🕒 Waiting 30 seconds to ensure full page load...")
        time.sleep(30)

        try:
            # ✅ Check if "Already Applied" button exists
            already_applied = driver.find_elements(By.ID, 'already-applied')
            company_site = driver.find_elements(By.ID, 'company-site-button')
            if already_applied:
                print(f"⚠️ Already applied for {url}. Skipping to next URL...")
                save_status(url, 'Already Applied')
                continue
            if company_site:
                print(f"⚠️ Company site for {url}. Skipping to next URL...")
                save_status(url, 'Company Site')
                continue
            
            # ✅ Check if apply button exists
            apply_button = driver.find_elements(By.ID, 'apply-button')
            if apply_button:
                apply_button[0].click()

                # ✅ Check for error message (short wait)
                try:
                    # Short wait to catch fast-disappearing error
                    error_message = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, 'section.styles_user-msg__YLRsE.styles_error__PZ5op span')
                        )
                    )
                    if error_message:
                        print(f"❌ Error while applying to {url}: {error_message.text}")
                        save_status(url, 'Failed')
                        failed += 1
                        continue
                except TimeoutException:
                    # ✅ No error message found — assume success
                    print(f"✅ Applied successfully to {url}")
                    save_status(url, 'Applied')
                    applied += 1
                except StaleElementReferenceException:
                    # ✅ Handle disappearing element case
                    print(f"⚠️ Error message disappeared quickly — recording as failure for {url}")
                    save_status(url, 'Failed')
                    failed += 1
                    continue

            else:
                print(f"❌ No apply button found for {url}")
                save_status(url, 'No Apply Button')
                failed += 1
        
        except Exception as e:
            print(f"❌ Failed to apply: {e}")
            save_status(url, f'Error: {str(e)}')
            failed += 1
# ===== SAVE STATUS TO CSV DIRECTLY =====
def save_status(url, status):
    status_df = pd.DataFrame([{'URL': url, 'Status': status}])

    # ✅ Append to CSV directly
    file_exists = os.path.exists('data/application_status.csv')

    status_df.to_csv('data/application_status.csv', mode='a', header=not file_exists, index=False)

# ===== MAIN FUNCTION =====
def main():
    login()
    apply_from_csv()

    print(f"✅ Direct Applies: {applied}")
    print(f"❌ Failed Attempts: {failed}")

    driver.quit()

# ===== EXECUTE SCRIPT =====
if __name__ == "__main__":
    main()
