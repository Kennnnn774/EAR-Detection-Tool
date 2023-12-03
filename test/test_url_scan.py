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
import csv
import matplotlib.pyplot as plt
import time

class EAR_Scanner:
    def __init__(self):
        self.vulnerable_urls      = []
        self.progress             = []
        self.errors               = []

    def get_arguments(self):
        parser = argparse.ArgumentParser(description="default argument for fuzz scan tool")
        parser.add_argument("-u", "--url", dest="url")
        parser.add_argument("-uL", "--url-list", dest="file_containing_urls", default = "top-100k.csv")    
        parser.add_argument("-w", "--wordlist", dest="wordlist", default='content_discovery_all.txt') 
        parser.add_argument("-t", "--timeout", dest="timeout", default=60)
        parser.add_argument("-th", "--thread", dest="ThreadNumber", default=100)
        parser.add_argument("-c", "--content-length", dest="ContentLength", default=200)

        return parser.parse_args()

    def start(self):
        start_time = time.time()
        self.arguments = self.get_arguments()
        self.ThreadNumber         = int(self.arguments.ThreadNumber)
        self.timeout              = int(self.arguments.timeout)
        self.content_length       = int(self.arguments.ContentLength)

        self.file_containing_urls = self.arguments.file_containing_urls
        print("="*85)
        print(f'{Fore.YELLOW}[*] Initiating {Fore.GREEN}Exection After Redirect{Fore.YELLOW} (EAR) Vulnerability Scanner ...{Style.RESET_ALL}')
        print("="*85)
        final_url_list = []

        with open(self.file_containing_urls) as f:
            data_list = f.readlines()
        
        #data processing
        for url in data_list:
            if url != '\n':
                url = url.strip()  # Remove whitespace characters
                if not url.startswith('https://www.'):
                    if url.startswith('www.'):
                        url = 'https://' + url  # Prepend the scheme and www to the URL
                    else:
                        url = 'https://www.' + url
                
                final_url_list.append(url)

        self.total = len(final_url_list)  # Used in showing progressbar 

        # Multi-Threaded Implementation
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.ThreadNumber)
        futures = [executor.submit(self.check_ear, url) for url in final_url_list]
        concurrent.futures.wait(futures)    

        results = []
        vulnerable_results = []

        for future in futures:
            try:
                result = future.result()
                results.append(result)
                if result['vulnerable']:
                    vulnerable_results.append(result)
            except Exception as e:
                print(f"Error processing a URL: {e}")
        
        # Write the vulnerable results to a new CSV file
        with open('vulnerable_results.csv', 'w', newline='') as file:
            fieldnames = ['url', 'status_code', 'vulnerable', 'message']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for result in vulnerable_results:
                writer.writerow(result)
        
        # Counting vulnerable and non-vulnerable sites for the graph
        vulnerable_count = len(vulnerable_results)
        non_vulnerable_count = len(results) - vulnerable_count

        # Creating a bar graph
        labels = ['Vulnerable', 'Non-Vulnerable']
        values = [vulnerable_count, non_vulnerable_count]

        fig, ax = plt.subplots()
        bars = ax.bar(labels, values)

        # Adding the text on top of the bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

        plt.bar(labels, values, color='blue')
        plt.xlabel('Status')
        plt.ylabel('Number of Websites')
        plt.title('Vulnerability Scan Results')
        plt.savefig('vulnerability_scan_results.png')

        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        print(f"Execution took {elapsed_time} seconds.")

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
    
def scan_single_url(url):
    scanner = EAR_Scanner()
    scanner.timeout = 60  # Set the desired timeout
    scanner.content_length = 200  # Set the desired content length for vulnerability check
    return scanner.check_ear(url)

if __name__ == '__main__':
    test = EAR_Scanner()
    test.start()
        
