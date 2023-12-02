import requests
requests.packages.urllib3.disable_warnings()
import concurrent.futures

from colorama import init
from colorama import Fore, Back, Style
init()
import argparse
import pyfiglet
import sys 
import os 
import platform

class EAR_Scanner:
    def __init__(self):
        self.vulnerable_urls      = []
        self.progress             = []
        self.errors               = []

    def get_arguments(self):
        parser = argparse.ArgumentParser(description="default argument for fuzz scan tool")
        parser.add_argument("-u", "--url", dest="url")
        parser.add_argument("-w", "--wordlist", dest="wordlist", default='content_discovery_all.txt') 
        parser.add_argument("-t", "--timeout", dest="timeout", default=60)
        parser.add_argument("-th", "--thread", dest="ThreadNumber", default=100)
        parser.add_argument("-c", "--content-length", dest="ContentLength", default=200)
        return parser.parse_args()

    def start(self):
        self.arguments = self.get_arguments()
        self.ThreadNumber         = int(self.arguments.ThreadNumber)
        self.timeout              = int(self.arguments.timeout)
        self.content_length       = int(self.arguments.ContentLength)

        if self.arguments.url:
            self.check_ear(self.arguments.url)   

    def check_ear(self, url):
        try:
            response = requests.get(url, timeout=self.timeout, verify=False, allow_redirects=False)
            result = {
                'url': url,
                'status_code': response.status_code,
                'vulnerable': False,
                'message': ''
            }

            if response.status_code == 302:
                if 'Location' in response.headers:
                    response_length = len(response.text)
                    if response_length >= self.content_length:
                        result['vulnerable'] = True
                        result['message'] = f"Found 302 with Location header. Content length: {response_length}. Likely vulnerable."
                    else:
                        result['message'] = "Found 302 with Location header but content length is less than expected."
                else:
                    result['message'] = "302 status code found, but no Location header."
            else:
                result['message'] = "No redirect found. Not vulnerable."

            return result

        except Exception as e:
            return {
                'url': url,
                'error': True,
                'message': str(e)
            }
            
    def write_results_to_file(self, filename):
        with open(filename, 'w') as f:
            # First, write the vulnerable URLs
            for vuln_url in self.vulnerable_urls:
                f.write(f"[VULNERABLE] {vuln_url}\n")

            # Then, write the rest of the URLs
            for url in self.progress:
                if url not in self.vulnerable_urls:
                    f.write(f"[OK] {url}\n")

            for error in self.errors:
                f.write(f"[ERROR] {error}\n")
    
def scan_single_url(url):
    scanner = EAR_Scanner()
    scanner.timeout = 60  # Set the desired timeout
    scanner.content_length = 200  # Set the desired content length for vulnerability check
    return scanner.check_ear(url)

if __name__ == '__main__':
    test = EAR_Scanner()
    test.start()

    ##########need to rewrite this part############
        
