import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pyfiglet
import requests.packages.urllib3

# Disable SSL certificate verification
requests.packages.urllib3.disable_warnings()

text = pyfiglet.figlet_format("ZWN _ CRAWL")
print(text)

def normalize_url(url):
    if url.startswith('www.'):
        url = 'http://' + url
    elif url.startswith('https://'):
        pass
    elif url.startswith('http://'):
        pass
    else:
        url = 'http://' + url
    return url

def extract_domains(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        anchor_tags = soup.find_all('a', href=True)
        
        domains = set()
        for tag in anchor_tags:
            href = tag['href']
            parsed_url = urlparse(href)
            if parsed_url.netloc:
                domains.add(parsed_url.netloc)
        
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

