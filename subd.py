import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import pyfiglet

text = pyfiglet.figlet_format("ZWN _ CRAWL")
print(text)

def normalize_url(url):
    # Check if the URL starts with 'www'
    if url.startswith('www.'):
        # Prepend 'http://' to the URL
        url = 'http://' + url
    # Check if the URL starts with 'https://'
    elif url.startswith('https://'):
        pass
    # Check if the URL starts with 'http://'
    elif url.startswith('http://'):
        pass
    # If none of the above, assume 'http://' is missing
    else:
        url = 'http://' + url
        
    return url

def extract_domains(url):
    try:
        # Sending GET request to the provided URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        
        # Parsing HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extracting all anchor tags
        anchor_tags = soup.find_all('a', href=True)
        
        # Extracting domains from anchor tags
        domains = set()
        for tag in anchor_tags:
            href = tag['href']
            parsed_url = urlparse(href)
            if parsed_url.netloc:
                domains.add(parsed_url.netloc)
        
        # Extracting unique subdomains from domains
        subdomains = set()
        for domain in domains:
            parts = domain.split('.')
            if len(parts) > 2:
                subdomains.add('.'.join(parts[:-2]))
        
        return subdomains, domains
    
    except requests.RequestException as e:
        print("Error:", e)
        return set(), set()

def main():
    url = input("[+]Enter a website URL: ")
    normalized_url = normalize_url(url)
    subdomains, domains = extract_domains(normalized_url)
    
    print("\n Subdomains-->")
    for subdomain in subdomains:
        print(subdomain)
        
    print("\nDomains-->")
    for domain in domains:
        print(domain)

if __name__ == "__main__":
    main()
