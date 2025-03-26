import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import urllib3

# Disable SSL warnings for testing (only if necessary)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    url = input("Enter the URL: ")
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the webpage: {e}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Use regex on the entire HTML text for unstructured data
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", response.text)
    ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', response.text)

    # Extract structured metadata
    meta_data = {}
    for meta in soup.find_all('meta'):
        name = meta.get('name', None)
        content = meta.get('content', None)
        if name and content:
            meta_data[name] = content

    # Combine results into a structured format
    data = {
        'emails': emails,
        'ips': ips,
        'meta_data': meta_data
    }

    # Optionally, if you want to store it in a DataFrame, adjust based on your needs:
    df = pd.DataFrame({'Type': ['Emails', 'IP Addresses'], 'Data': [emails, ips]})
    df.to_csv('scraped_sensitive_data.csv', index=False)
    print("Data has been scraped and saved to scraped_sensitive_data.csv")
    print("Meta Data extracted:", meta_data)

if __name__ == "__main__":
    main()
