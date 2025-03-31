# # loading in same window 
# import os
# import time
# import pandas as pd
# import subprocess
# from dotenv import load_dotenv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

# # ===== CONFIGURATION =====
# load_dotenv('auth.env')

# EMAIL = os.getenv('NAUKRI_EMAIL')
# PASSWORD = os.getenv('NAUKRI_PASSWORD')
# FIRST_NAME = os.getenv('FIRST_NAME')
# LAST_NAME = os.getenv('LAST_NAME')

# MAX_APPLY_COUNT = 100

# # ===== VARIABLES =====
# applied = 0
# failed = 0
# application_status = []

# # ===== OPEN IN EXISTING CHROME SESSION =====
# def open_url_in_chrome(url):
#     try:
#         subprocess.run(f'start chrome.exe --new-tab "{url}"', shell=True)
#         print(f"🚀 Opened URL: {url}")
#         time.sleep(3)
#     except Exception as e:
#         print(f"❌ Failed to open URL: {e}")

# # ===== LOGIN FUNCTION =====
# def login():
#     try:
#         print("🚀 Logging into Naukri...")
#         open_url_in_chrome('https://login.naukri.com/')
#         time.sleep(5)
#         print("✅ Logged in successfully!")
#     except Exception as e:
#         print(f"❌ Failed to log in: {e}")

# # ===== APPLY FROM CSV =====
# def apply_from_csv():
    
#     global applied, failed
#     urls = pd.read_csv('data/direct_apply_urls.csv')['Direct Apply URL'].tolist()

#     for url in urls:
#         if applied >= MAX_APPLY_COUNT:
#             break

#         open_url_in_chrome(url)
#         time.sleep(3)

#         try:
#             # Use Selenium to check the apply button after opening the tab
#             options = webdriver.ChromeOptions()
#             options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#             driver = webdriver.Chrome(options=options)

#             driver.get(url)
#             time.sleep(3)

#             if driver.find_elements(By.ID, 'apply-button'):
#                 driver.find_elements(By.ID, 'apply-button').click()
#                 time.sleep(3)

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
#     apply_from_csv()
#     save_status()

#     print("\n===== ✅ Summary ✅ =====")
#     print(f"Total Jobs Applied: {applied}")
#     print(f"Total Failed Attempts: {failed}")

# if __name__ == "__main__":
#     main()


# # Updated code on top is opening tabs in existing chrome 

import os
import time
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
application_status = []

# ===== DRIVER SETUP =====
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Attach to existing session

driver = webdriver.Chrome(options=options)

# ===== LOGIN FUNCTION =====
def login():
    print("🚀 Logging into Naukri...")
    driver.get('https://login.naukri.com/')
    time.sleep(2)

    driver.find_element(By.ID, 'usernameField').send_keys(EMAIL)
    driver.find_element(By.ID, 'passwordField').send_keys(PASSWORD)
    driver.find_element(By.ID, 'passwordField').send_keys(Keys.RETURN)

    print("✅ Logged in successfully!")
    time.sleep(5)

# ===== APPLY FROM CSV =====
def apply_from_csv():
    global applied, failed
    urls = pd.read_csv('data/direct_apply_urls.csv')['Direct Apply URL'].tolist()

    for url in urls:
        if applied >= MAX_APPLY_COUNT:
            break

        try:
            driver.execute_script(f"window.open('{url}', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)

            if driver.find_elements(By.ID, 'apply-button'):
                driver.find_element(By.ID, 'apply-button').click()
                time.sleep(3)

                error_message = driver.find_elements(By.CSS_SELECTOR, 'section.styles_user-msg__YLRsE.styles_error__PZ5op span')
                if error_message:
                    print(f"❌ Error while applying to {url}: {error_message[0].text}")
                    failed += 1
                    application_status.append({'URL': url, 'Status': 'Failed'})
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue

                print(f"✅ Applied successfully to {url}")
                application_status.append({'URL': url, 'Status': 'Applied'})
                applied += 1
            else:
                print(f"❌ No apply button found for {url}")
                failed += 1
                application_status.append({'URL': url, 'Status': 'Failed'})

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"❌ Failed to apply to {url}: {e}")
            failed += 1
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

# ===== SAVE STATUS =====
def save_status():
    pd.DataFrame(application_status).to_csv('data/application_status.csv', index=False)
    print("✅ Application status saved.")

# ===== MAIN FUNCTION =====
def main():
    login()
    apply_from_csv()
    save_status()

    print("\n===== ✅ Summary ✅ =====")
    print(f"Total Jobs Applied: {applied}")
    print(f"Failed Attempts: {failed}")

    driver.quit()

if __name__ == "__main__":
    main()
