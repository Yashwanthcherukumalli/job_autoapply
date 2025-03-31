import pandas as pd


def copy_data():
    # Load the job_apply_urls CSV
    job_apply_urls = pd.read_csv('data/jobs_apply_urls.csv', header=None)
    job_apply_urls.columns = ['keyword', 'CompanyName', 'PostedBy', 'JobTitle', 'DirectApplyURL','JobAge','ApplyType',]
    
    # Copy the DataFrame to a new CSV file
    job_apply_urls.to_csv('data/jobs_apply_urls_copy.csv', index=False)
    print("Data copied to 'data/job_apply_urls_copy.csv'.")



def remove_duplicates():
    # Load the job_apply_urls CSV
    job_apply_urls = pd.read_csv('data/jobs_apply_urls_copy.csv')
    # Remove duplicate rows based on the 'DirectApplyURL' column
    job_apply_urls.drop_duplicates(subset=['DirectApplyURL'], inplace=True)
    # Save the filtered rows to cleaned_direct_apply_urls.csv
    job_apply_urls.to_csv('data/jobs_apply_urls_copy.csv', index=False)
    # Print the number of duplicate rows removed
    print(f"Number of duplicate rows removed: {len(job_apply_urls)}")
    print("Duplicates removed and saved to 'data/jobs_apply_urls_copy.csv'.")

# Function to filter CSV based on Apply Type
# This function reads a CSV file containing job application URLs and filters out those that are not of type 'Direct'.
# The filtered URLs are then saved to a new CSV file.

def filter_csv():
    job_apply_urls = pd.read_csv('data/jobs_apply_urls_copy.csv', header=None)
    print("Data loaded from 'data/job_apply_urls_copy.csv'.")
    job_apply_urls.columns = ['keyword', 'CompanyName', 'PostedBy', 'JobTitle', 'DirectApplyURL','JobAge','ApplyType',]
    job_apply_urls = pd.read_csv('data/jobs_apply_urls_copy.csv')
    print("Data loaded from 'data/job_apply_urls_copy.csv'.")
    # Filter rows where Apply Type is 'Direct'
    direct_apply_urls = job_apply_urls[job_apply_urls['ApplyType'] == 'Direct']
    # Filter rows where Apply Type is 'Company'
    company_apply_urls = job_apply_urls[job_apply_urls['ApplyType'] == 'Company Site']
    # Save the filtered rows to cleaned_direct_apply_urls.csv
    direct_apply_urls.to_csv('data/cleaned_direct_apply_urls.csv', index=False)
    company_apply_urls.to_csv('data/cleaned_company_apply_urls.csv', index=False)
    # Save the lengths of the two filtered files to a text file
    print(f"Length of cleaned_direct_apply_urls.csv: {len(direct_apply_urls)}")
    print(f"Length of cleaned_company_apply_urls.csv: {len(company_apply_urls)}")
    print("Filtered URLs saved to 'data/cleaned_direct_apply_urls.csv' and 'data/cleaned_company_apply_urls.csv'.")

def findspam():
    # Load the job_apply_urls CSV
    job_apply_urls = pd.read_csv('data/jobs_apply_urls_copy.csv', header=None)
    job_apply_urls.columns = ['keyword', 'CompanyName', 'PostedBy', 'JobTitle', 'DirectApplyURL','JobAge','ApplyType',]
    # Load the cleaned_direct_apply_urls CSV
    top_it_mnc_companies = [
    "TCS", "Infosys", "Wipro", "HCL Technologies", "Tech Mahindra", "Cognizant",
    "Capgemini", "Accenture", "IBM", "Oracle", "Microsoft", "Google", "Amazon",
    "SAP", "Deloitte", "EY", "KPMG", "PwC", "Mindtree", "LTI (Larsen & Toubro Infotech)",
    "Mphasis", "UST Global", "Virtusa", "Hexaware", "Zensar Technologies", "Persistent Systems",
    "Cyient", "Birlasoft", "QuEST Global", "Sasken Technologies", "Sonata Software",
    "LTTS (L&T Technology Services)", "Happiest Minds", "NIIT Technologies", "Informatica",
    "Dell Technologies", "HP Inc", "NVIDIA", "Adobe", "Intuit", "Salesforce", "VMware",
    "PayPal", "LinkedIn", "Intel", "Cisco", "Juniper Networks", "Red Hat", "Fujitsu",
    "Hitachi Vantara", "Symantec", "ServiceNow", "Snowflake", "Dropbox", "Zoom",
    "Veritas Technologies", "McAfee", "NetApp", "Epicor", "Micro Focus", "Tanium",
    "CrowdStrike", "Check Point", "Fortinet", "Palo Alto Networks", "Trend Micro",
    "Okta", "Splunk", "Elastic", "New Relic", "Atlassian", "Freshworks", "Zoho",
    "Razorpay", "Zscaler", "Cloudflare", "Akamai", "Coupa", "Confluent", "Databricks",
    "Cloudera", "MongoDB", "Postman", "ThoughtSpot", "Alteryx", "Tableau", "Qlik",
    "Fivetran", "Talend", "Domo", "Looker", "Boomi", "Workday", "ServiceTitan",
    "Gainsight", "AppDynamics", "PagerDuty", "Sumo Logic", "RingCentral", "Twilio",
    "Pluralsight", "Coursera", "Udacity", "Udemy", "Byju's", "Unacademy", "Scaler",
    "Simplilearn", "UpGrad", "Great Learning", "Vedantu", "WhiteHat Jr", "CodeChef",
    "Codeforces", "HackerRank", "LeetCode", "GeeksforGeeks", "TopCoder", "Cvent",
    "Reltio", "Epsilon", "Netcracker", "Cimpress", "Sutherland", "EXL", "Genpact",
    "Mu Sigma", "Fractal Analytics", "Nagarro", "Xebia", "HashedIn", "Sigmoid",
    "Tredence", "Brillio", "Kryterion", "SumTotal Systems", "Apttus", "Veeva Systems",
    "Finastra", "Temenos", "Fiserv", "Mastercard", "Visa", "Paytm", "PhonePe",
    "Google Pay", "Razorpay", "Cashfree", "Pine Labs", "Stripe", "CRED", "Groww",
    "Zerodha", "Angel One", "Upstox", "ICICI Bank", "HDFC Bank", "Axis Bank",
    "Kotak Mahindra Bank", "SBI", "Bank of Baroda", "IDFC First Bank", "Yes Bank",
    "JPMorgan Chase", "Goldman Sachs", "Morgan Stanley", "Bank of America", "Citi",
    "Wells Fargo", "Deutsche Bank", "Standard Chartered", "HSBC", "UBS", "Barclays",
    "BNP Paribas", "Societe Generale", "ANZ", "RBS", "AIG", "American Express",
    "PayU", "PolicyBazaar", "MobiKwik", "Instamojo", "NeoGrowth", "Niyo", "Paysa",
    "Hewlett Packard Enterprise", "Broadcom", "Arm Holdings", "Qualcomm", "Texas Instruments",
    "NXP Semiconductors", "Infineon", "Marvell Technology", "Micron Technology",
    "Western Digital", "Seagate", "SanDisk", "AMD", "Synopsys", "Cadence", "Mentor Graphics",
    "Analog Devices", "STMicroelectronics", "Skyworks", "Maxim Integrated", "ON Semiconductor",
    "Renesas Electronics", "ROHM Semiconductor", "Xilinx", "Allegro Microsystems",
    "Keysight Technologies", "Avnet", "Arrow Electronics", "Digi-Key Electronics",
    "Farnell", "Mouser Electronics", "Tata Elxsi", "KPIT Technologies", "LTIMindtree",
    "Hexagon", "Dassault Systemes", "PTC", "ANSYS", "Autodesk", "MathWorks",
    "Bentley Systems", "Siemens Digital Industries", "Altair", "C3.ai", "Informatica",
    "Snowflake", "Databricks", "DataRobot", "Domino Data Lab", "AI21 Labs", "Hugging Face",
    "OpenAI", "Anthropic", "DeepMind", "MindsDB", "Cohere", "Abacus.AI", "Dataiku",
    "Alteryx", "DataRobot", "Numenta", "Vianai Systems", "DataStax", "SingleStore",
    "PlanetScale", "ScyllaDB", "Yugabyte", "Neo4j", "TigerGraph", "ArangoDB",
    "Redis", "Memgraph", "RocksDB", "FoundationDB", "Cockroach Labs", "Starburst",
    "Dremio", "Trifacta", "Fivetran", "MindsDB", "Cribl", "Aiven", "Redpanda",
    "StreamNative", "Confluent", "Materialize", "DeltaStream", "HVR Software",
    "Rivery", "Hevo Data", "Dataddo", "Estuary", "Datafold", "Great Expectations",
    "Monte Carlo", "Soda.io", "Lightdash", "Metabase", "Superset", "Power BI",
    "Looker", "Tableau", "Qlik", "Domo", "Mode Analytics", "Sisense", "ThoughtSpot",
    "Kibana", "Grafana", "Splunk", "Elastic", "New Relic", "Dynatrace", "Datadog",
    "AppDynamics", "Instana", "Coralogix", "Humio", "LogDNA", "Sentry", "Rollbar",
    "Raygun", "BugSnag", "Airbrake", "Honeycomb", "LightStep", "Thundra", "IOpipe",
    "Epsagon", "Lumigo", "Dashbird", "Nimbella", "Serverless Framework", "Pulumi",
    "Terraform", "CloudFormation", "Ansible", "Chef", "Puppet", "SaltStack",
    "Rundeck", "Spinnaker", "Argo CD", "Flux", "Jenkins", "Travis CI", "CircleCI",
    "GitLab CI", "GitHub Actions", "Drone", "Buildkite", "TeamCity", "Bamboo",
    "Bitrise", "AppVeyor", "Wercker", "Semaphore", "Octopus Deploy", "Codefresh",
    "CloudBees", "Harness", "AWS", "Azure", "Google Cloud", "IBM Cloud", "Oracle Cloud",
    "DigitalOcean", "Linode", "Vultr", "Cloudflare", "Akamai", "Fastly", "Imperva"]
        # Filter rows where the company name is not in the top IT MNC companies list
    non_spam_urls = job_apply_urls[job_apply_urls['CompanyName'].isin(top_it_mnc_companies)]

    # Identify duplicate rows based on Company Name, Posted By, and Job Title
    spam_urls = job_apply_urls[job_apply_urls.duplicated(subset=['CompanyName', 'PostedBy', 'JobTitle'], keep=False)]
    print(f"Number of spam URLs found: {len(spam_urls)}")
    # Exclude non-spam URLs from the spam list
    print(f"Number of non-spam URLs found: {len(non_spam_urls)}")
    spam_urls = spam_urls[~spam_urls['CompanyName'].isin(top_it_mnc_companies)]
    # Save the filtered rows to cleaned_spam_urls.csv
    spam_urls.to_csv('data/spam.csv', index=False)
    print("Filtered URLs saved to 'data/spam.csv'.")
    print(f"Number of spam URLs found: {len(spam_urls)}")
    # Save the non-spam URLs to cleaned_non_spam_urls.csv


def removing_spam():
    # Load CSV files
    cleaned_direct_apply_urls = pd.read_csv('data/cleaned_direct_apply_urls.csv')
    spam_urls = pd.read_csv('data/spam.csv')

    # Handle missing columns and type mismatches
    required_columns = {'CompanyName', 'PostedBy', 'DirectApplyURL'}
    if not required_columns.issubset(cleaned_direct_apply_urls.columns):
        raise KeyError(f"Missing columns in cleaned_direct_apply_urls: {required_columns - set(cleaned_direct_apply_urls.columns)}")
    if not {'CompanyName', 'PostedBy'}.issubset(spam_urls.columns):
        raise KeyError("Missing required columns in spam.csv")
    print("Data loaded from 'data/cleaned_direct_apply_urls.csv' and 'data/spam.csv'.")

    cleaned_direct_apply_urls.fillna('', inplace=True)
    spam_urls.fillna('', inplace=True)

    # Identify spam entries (create a copy to avoid SettingWithCopyWarning)
    spam_in_cleaned = cleaned_direct_apply_urls[
        cleaned_direct_apply_urls[['CompanyName', 'PostedBy']].apply(tuple, axis=1).isin(
            spam_urls[['CompanyName', 'PostedBy']].apply(tuple, axis=1)
        )
    ].copy()
    print(f"Number of spam entries found: {len(spam_in_cleaned)}")

    # Count spam entries (use .loc[] to avoid warnings)
    spam_in_cleaned.loc[:, 'RepeatCount'] = spam_in_cleaned.groupby(
        ['CompanyName', 'PostedBy']
    )['DirectApplyURL'].transform('count')

    # Append and remove duplicates
    spam_urls = pd.concat([spam_urls, spam_in_cleaned], ignore_index=True).drop_duplicates(subset=['CompanyName', 'PostedBy', 'DirectApplyURL'])
    print(f"Number of unique spam entries: {len(spam_urls)}")
    # Save updated spam list
    spam_urls.to_csv('data/spam.csv', index=False)

    # Remove spam from cleaned list
    cleaned_direct_apply_urls = cleaned_direct_apply_urls[
        ~cleaned_direct_apply_urls[['CompanyName', 'PostedBy']].apply(tuple, axis=1).isin(
            spam_in_cleaned[['CompanyName', 'PostedBy']].apply(tuple, axis=1)
        )
    ]
    print(f"Number of non-spam entries remaining: {len(cleaned_direct_apply_urls)}")
    # Save cleaned URLs
    cleaned_direct_apply_urls.to_csv('data/cleaned_direct_apply_urls.csv', index=False)
    print("Filtered URLs saved to 'data/cleaned_direct_apply_urls.csv'.")

# Function to filter URLs based on application status
# This function reads a CSV file containing application statuses and filters out URLs that are already applied or in the process of applying.

def filtering_data_from_application_type():
    # Load the application status CSV
    application_status = pd.read_csv('data/application_status.csv')

# Filter rows where status is 'applied' or 'already applied'
    filtered_status = application_status[application_status['Status'].isin(['Applied', 'Already Applied', 'Company Site'])]

# Load the cleaned-directapply_url CSV
    cleaned_urls = pd.read_csv('data/cleaned_direct_apply_urls.csv')

# Remove URLs that match the filtered application IDs
    filtered_urls = cleaned_urls[~cleaned_urls['DirectApplyURL'].isin(filtered_status['URL'])]

# Save the filtered URLs back to a new CSV
    print(f"Number of URLs after filtering: {len(filtered_urls)}")
    filtered_urls.to_csv('data/cleaned_direct_apply_urls.csv', index=False)
    print("Filtered URLs saved to 'data/cleaned_direct_apply_urls.csv'.")

"""filtering false companies"""

def filtering_false_companies():
    false_companies=["Leading Client", "Muthoot Finance", "Barclays", "Indusind Bank", "Deutsche Bank"]
    # Load the job_apply_urls CSV
    job_apply_urls = pd.read_csv('data/jobs_apply_urls_copy.csv', header=None)
    job_apply_urls.columns = ['keyword', 'CompanyName', 'PostedBy', 'JobTitle', 'DirectApplyURL','JobAge','ApplyType',]
    # Filter rows where the company name is not in the false companies list
    non_false_urls = job_apply_urls[~job_apply_urls['CompanyName'].isin(false_companies)]
    # Identify false entries
    false_urls = job_apply_urls[job_apply_urls['CompanyName'].isin(false_companies)]
    print(f"Number of false URLs found: {len(false_urls)}")
    # Save the filtered rows to cleaned_false_urls.csv
    false_urls.to_csv('data/false.csv', index=False)
    print("Filtered URLs saved to 'data/false.csv'.")
    print(f"Number of false URLs found: {len(false_urls)}")
    # Save the non-false URLs to cleaned_non_false_urls.csv
    non_false_urls.to_csv('data/non_false.csv', index=False)
    print("Filtered URLs saved to 'data/non_false.csv'.")
    print(f"Number of non-false URLs found: {len(non_false_urls)}")


def remove_spam_and_false_companies():
    # Load the cleaned_direct_apply_urls CSV
    cleaned_direct_apply_urls = pd.read_csv('data/cleaned_direct_apply_urls.csv')
    # Load the spam and false CSVs
    spam_urls = pd.read_csv('data/spam.csv')
    false_urls = pd.read_csv('data/false.csv')

    # Combine spam and false company names
    spam_and_false_companies = set(spam_urls['CompanyName']).union(set(false_urls['CompanyName']))

    # Filter out rows where the CompanyName is in the spam or false company list
    filtered_urls = cleaned_direct_apply_urls[~cleaned_direct_apply_urls['CompanyName'].isin(spam_and_false_companies)]

    # Save the filtered URLs back to the cleaned_direct_apply_urls.csv
    print(f"Number of URLs after removing spam and false companies: {len(filtered_urls)}")
    filtered_urls.to_csv('data/cleaned_direct_apply_urls.csv', index=False)
    print("Filtered URLs saved to 'data/cleaned_direct_apply_urls.csv'.")

    # Load non_false.csv
    non_false_urls = pd.read_csv('data/non_false.csv')

    # Filter rows where ApplyType is 'Direct'
    direct_non_false_urls = non_false_urls[non_false_urls['ApplyType'] == 'Direct']

    # Append these rows to cleaned_direct_apply_urls
    updated_cleaned_direct_apply_urls = pd.concat([filtered_urls, direct_non_false_urls], ignore_index=True)

    # Save the updated cleaned_direct_apply_urls.csv
    print(f"Number of URLs after adding rows from non_false.csv with ApplyType 'Direct': {len(updated_cleaned_direct_apply_urls)}")
    updated_cleaned_direct_apply_urls.to_csv('data/cleaned_direct_apply_urls.csv', index=False)
    print("Updated URLs saved to 'data/cleaned_direct_apply_urls.csv'.")


copy_data()
remove_duplicates()
# filtering_false_companies()
filter_csv()
findspam()
removing_spam()
remove_spam_and_false_companies()
filtering_data_from_application_type()