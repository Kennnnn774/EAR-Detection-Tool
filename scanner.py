import requests
requests.packages.urllib3.disable_warnings()
import concurrent.futures

from colorama import init
from colorama import Fore, Back, Style
init()

class EAR_Scanner:
    def __init__(self):
        self.vulnerable_urls      = []
        self.progress             = []
        self.errors               = []

    def start(self):
        return None

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
                if 'Location' in response.headers: # this is the best way to check the length of the response
                    response_length = len(response.text)
                    if response_length >= self.content_length: # a redirect is not very long
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
    
def scan_single_url(url):
    scanner = EAR_Scanner()
    scanner.timeout = 60  # Set the desired timeout
    scanner.content_length = 200  # Set the desired content length for vulnerability check
    return scanner.check_ear(url)

if __name__ == '__main__':
    print(scan_single_url("https://realpython.com/run-python-scripts/"))
    
