import sys
import subprocess
import argparse
from urllib.parse import urlparse, urlunparse
import re

def get_gau_urls(root_domain):
    """Runs gau to get all URLs for the given root domain."""
    try:
        result = subprocess.run(["gau", root_domain, "--subs"], capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError:
        return []

def remove_port(url):
    """Removes any port number from the URL (e.g., :80, :443)."""
    parsed_url = urlparse(url)
    netloc = re.sub(r':\d+', '', parsed_url.netloc)
    return urlunparse(parsed_url._replace(netloc=netloc))

def hop_urls(urls, target_domain, output_file=None):
    """Replaces root domain with target domain, removes port, and optionally writes to file."""
    for url in urls:
        parsed_url = urlparse(url)
        
        if parsed_url.netloc:
            new_url = urlunparse(parsed_url._replace(netloc=target_domain))
            cleaned_url = remove_port(new_url)

            if output_file:
                with open(output_file, 'a') as f:
                    f.write(cleaned_url + '\n')
            else:
                print(cleaned_url)

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Replace root domain with a target domain for URL hopping.")
    parser.add_argument('-r', '--root', required=True, help="Root domain(s) to extract URLs from (comma separated). Example: example.com,otherdomain.com")
    parser.add_argument('-t', '--target', required=True, help="Target domain to replace the root domain with (e.g., test.example.com)")
    parser.add_argument('-o', '--output', help="Output file to save the new URLs.")
    args = parser.parse_args()
    
    # Split root domains into a list
    root_domains = args.root.split(',')

    for root_domain in root_domains:
        urls = get_gau_urls(root_domain.strip())  # Strip any surrounding whitespace

        if not urls:
            # print(f"[-] No URLs found for root domain: {root_domain}.")
            continue
        
        hop_urls(urls, args.target, args.output)

if __name__ == "__main__":
    main()