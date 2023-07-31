###########################################################################################
# In order to use this tool you have to export your API-KEY into your enviroment variable #
#                   export SHODAN_API_KEY=<YOUR-API-KEY>                                  #
#                   export ZOOMEYE_API_KEY=<YOUR-API-KEY>                                 #
###########################################################################################

import os
import re
import sys
import datetime
import requests
import json
import mmh3
import hashlib
import base64
import ipaddress
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from censys.search import CensysHosts
from zoomeye.sdk import ZoomEye
from shodan import Shodan, APIError


sender_email = "tengistest@gmail.com" # Your email address
allowed_networks = ['103.51.60.0/24', '103.142.243.0/24'] # Your network subnet
recipients = ["xyptonize@gmail.com", "theifurymongolia@gmail.com"]  # Mail Receiver's email address


# Retrieve API keys and credentials from environment variables
shodan_api_key = os.environ.get('SHODAN_API_KEY') #  export SHODAN_API_KEY=<YOUR-API-KEY>  
zoomeye_api_key = os.environ.get('ZOOMEYE_API_KEY') # export ZOOMEYE_API_KEY=<YOUR-API-KEY>  
censys_api_id = os.environ.get('CENSYS_API_ID') # export CENSYS_API_ID=<YOUR-API-KEY>  
censys_api_secret = os.environ.get('CENSYS_API_SECRET') # export CENSYS_API_SECRET=<YOUR-API-KEY>  
mail_password = os.environ.get('MAIL_PASSWORD') # export MAIL_PASSWORD=<APP PASSWORD>  in Gmail Go to Google Account Page>Security>Signing in to Google section turn on 2-Step Verification. You need this feature on. When 2SV is on, click 2-Step Verification, scroll to the bottom to App Password.Generate new-app-password for mail access. It will generate it for you, then use that password in this.

# Check if all the required API keys are present
if not all([shodan_api_key, zoomeye_api_key, censys_api_id, censys_api_secret]):
    print("Error: Missing one or more API keys.")
    print("Make sure to export the following environment variables:")
    print("SHODAN_API_KEY, ZOOMEYE_API_KEY, CENSYS_API_ID, CENSYS_API_SECRET")
    sys.exit(1)

# Create API instances
try:
    sh = Shodan(shodan_api_key)
except APIError as e:
    print("Error: Shodan API key is invalid or unauthorized.")
    print("Make sure the SHODAN_API_KEY environment variable contains the correct API key.")
    sys.exit(1)

try:
    zm = ZoomEye(api_key=zoomeye_api_key)
except Exception as e:
    print("Error: ZoomEye API key is invalid or unauthorized.")
    print("Make sure the ZOOMEYE_API_KEY environment variable contains the correct API key.")
    sys.exit(1)

try:
    cs = CensysHosts(api_id=censys_api_id, api_secret=censys_api_secret)
except Exception as e:
    print("Error: Censys API credentials are invalid or unauthorized.")
    print("Make sure the CENSYS_API_ID and CENSYS_API_SECRET environment variables contain the correct credentials.")
    sys.exit(1)

# sh = Shodan(shodan_api_key)
# zm = ZoomEye(api_key=zoomeye_api_key)
# cs = CensysHosts(api_id=censys_api_id, api_secret=censys_api_secret)

# Get Hash from favicon
def faviconhash(favicon_url):
    res = requests.get(favicon_url)
    favicon = base64.encodebytes(res.content)
    mmh3_hash = mmh3.hash(favicon)
    md5hash = hashlib.md5(res.content).hexdigest()
    # print(mmh3_hash)
    # print(str(md5hash))
    return str(mmh3_hash), str(md5hash)

# Dork using Zoomeye

def ipfilter(data):
    # allowed_networks = ['103.51.60.0/24', '103.142.243.0/24']
    filtered_data = []

    for entry in data:
        ip = entry['IP']
        is_allowed = False
        for allowed_network in allowed_networks:
            if ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(allowed_network):
                is_allowed = True
                break
        if not is_allowed:
            filtered_data.append(entry)

    return filtered_data

def useZoomEye(favicon_url):
    mmh3_hash, _ = faviconhash(favicon_url)
    datastr = zm.dork_search('iconhash:"' + mmh3_hash + '"')
    # Parse the JSON data
    data = json.dumps(datastr)
    data = json.loads(data)

    # print(data)
    extracted_data = []
    ssl_data= data[0]["ssl"]
    pattern = r'DNS:(.*?)(?:,|$)'
    dns_matches = re.findall(pattern, ssl_data)
    dns = []
    for dns_name in dns_matches:
        dns.append(dns_name.strip())
    ip = data[0]["ip"]
    org = data[0]["geoinfo"]["organization"]
    # extracted_data.append({'Organization': org, 'IP': ip, 'DNS': dns})
    extracted_data.append({'IP': ip, 'DNS':  dns, 'Orgnanization': org})
    extracted_data = str(extracted_data)[1:-1]

    # print("DNS:", dns)
    # print("IP:", ip)
    # print("Organization:", org)
    
    return extracted_data

# Dork using Shodan
def useShodan(favicon_url):
    try:
        mmh3_hash, _ = faviconhash(favicon_url)
        # shdata = sh.search("http.favicon.hash:" + faviconhash(favicon_url))
        shdata = sh.search("http.favicon.hash:"+mmh3_hash)
        results = shdata['matches']
        extracted_data = []
        for result in results:
            ip = result['ip_str']
            dns = result['domains']
            org = result.get('org', 'N/A')
            extracted_data.append({'IP': ip, 'DNS': dns, 'Organization': org})
        return extracted_data
    except APIError as e:
        print('Error:', e, '\nYou have to become a Shodan member to use this feature')
        sys.exit(1)

# Search using Censys
def useCensys(favicon_url):
    try:
        _, md5hash = faviconhash(favicon_url)
        results = cs.search("services.http.response.favicons.md5_hash=" + md5hash)
        extracted_data = []
        for page in results:
            for entry in page:
                asname = entry['autonomous_system']['name']
                ip = entry['ip']
                dns = entry.get('dns', {}).get('reverse_dns', {}).get('names', [])
                extracted_data.append({'IP': ip, 'DNS': dns, 'Organization': asname})

        # json_data = json.dumps(results, indent=2)
        # extracted_data = []
        # for page in results:
        #     for result in page:
        #         if 'ip' in result and 'dns' in result:
        #             ip = result['ip']
        #             domain = result['dns']['reverse_dns']['names']
        #             asname = result['autonomous_system']['name']  # Access 'name' from 'autonomous_system'
        #             extracted_data.append([domain, ip, asname])
        #         else:
        #             # Handle the case where 'ip' or 'dns' key is missing in the result
        #             print("Skipping invalid result:", result)
        # return json_data
        # print(results)
        return extracted_data

    except Exception as e:
        print('Error:', e)
        sys.exit(1)

def send_email(subject, body, recipients):

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject_with_time = f"{subject} - {current_time}"
    # sender_email = "tengistest@gmail.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject_with_time

    body_part = MIMEText(body, "plain")
    message.attach(body_part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, mail_password)
        server.sendmail(sender_email, recipients, message.as_string())
        print("Email sent successfully.")
        server.quit()
    except Exception as e:
        print("Error sending email:", e)


if __name__ == '__main__':
    if len(sys.argv) < 4 or sys.argv[1].lower() != '-u' or sys.argv[3].lower() != '-s':
        print('Usage: python3 faviconfinder.py -u <favicon-url1,favicon-url2,...> -s <platform>')
        print('Choose between Shodan, ZoomEye, or Censys:')
        sys.exit(1)

    # Get the platform and remove it from the sys.argv list
    platform = sys.argv[4].lower()
    sys.argv = sys.argv[:4]

    if platform == 'shodan':
        print("If the results give some benign DNS address or IP address, then it is most likely a phishing/impersonated website!!!\n")
    elif platform == 'zoomeye':
        print("If the results give some benign DNS address or IP address, then it is most likely a phishing/impersonated website!!!\n")
    elif platform == 'censys':
        print("If the results give some benign DNS address or IP address, then it is most likely a phishing/impersonated website!!!\n")
    elif platform == 'wildcard':
        print("If the results give some benign DNS address or IP address, then it is most likely a phishing/impersonated website!!!\n")
    else:
        print('Invalid platform')
        sys.exit(1)

    # Get all favicon URLs from the command line arguments and split them by comma
    favicon_urls = sys.argv[2].split(',')
    merged = []

    for favicon_url in favicon_urls:
        if platform == 'shodan':
            output = useShodan(favicon_url)
            for line in output:
                merged.append(line)
                # print(line)
        elif platform == 'zoomeye':
            output = useZoomEye(favicon_url)
            merged.append(line)
            # print(output)
            # for line in output:
            #     print(line)
            #     print("\n")
        elif platform == 'censys':
            output = useCensys(favicon_url)
            for line in output:
                merged.append(line)
                # print(line)

        elif platform == 'wildcard':
            output = useCensys(favicon_url)
            for line in output:
                merged.append(line)
            output = useZoomEye(favicon_url)
            merged.append(line)
            output = useShodan(favicon_url)
            for line in output:
                merged.append(line)

    for line in merged:
        print(line)
    print("\nFiltered: ",ipfilter(merged))
    formatted_data = "\n".join(str(entry) for entry in ipfilter(merged))

    # recipients = ["xyptonize@gmail.com", "theifurymongolia@gmail.com"]  # Add email addresses here
    subject = "Favicon Finder Results"
    send_email(subject, formatted_data, recipients)

# if __name__ == '__main__':
#     if len(sys.argv) < 4 or sys.argv[1].lower() != '-u' or sys.argv[3].lower() != '-s':
#         print('Usage: python3 faviconfinder.py -u <favicon-url> -s <platform>')
#         print('Choose between Shodan, ZoomEye, or Censys:')
#         sys.exit(1)

#     favicon_url = sys.argv[2]
#     platform = sys.argv[4].lower()

#     if platform == 'shodan':
#         print("If the results give some benign DNS address or IP address, then it is most likely a phishing/impersonated website!!!\n")
#         # print(useShodan(favicon_url))
#         output = useShodan(favicon_url)
#         for line in output:
#             print(line)
#     elif platform == 'zoomeye':
#         print("If the results give some benign DNS address or IP address, then it is most likely a phishing/impersonated website!!!\n")
#         print(useZoomEye(favicon_url))
#     elif platform == 'censys':
#         print("If the results give some benign DNS address or IP address, then it is most likely a phishing/impersonated website!!!\n")
#         # print(useCensys(favicon_url))
#         output = useCensys(favicon_url)
#         for line in output:
#             print(line)
#     else:
#         print('Invalid platform')
