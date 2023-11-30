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
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import queue
import time
import subprocess

class EAR_Scanner:
    def __init__(self, output_queue=None):
        self.vulnerable_urls      = []
        self.progress             = []
        self.errors               = []
        self.output_queue = output_queue or queue.Queue()
    
    def write_to_queue(self, message):
        if self.output_queue:
            self.output_queue.put(message)
        else:
            print(message)

    def get_arguments(self):
        parser = argparse.ArgumentParser(description=f'{Fore.RED}EAR Scanner v1.0 {Fore.YELLOW}[Author: {Fore.GREEN}Pushpender Singh{Fore.YELLOW}] [{Fore.GREEN}https://github.com/PushpenderIndia{Fore.YELLOW}]')
        parser._optionals.title = f"{Fore.GREEN}Optional Arguments{Fore.YELLOW}"
        parser.add_argument("-u", "--url", dest="url", help=f"{Fore.GREEN}Scan Single URL for EAR{Fore.YELLOW}")
        parser.add_argument("-uL", "--url-list", dest="file_containing_urls", help=f"{Fore.GREEN}Provide a File Containing URLs {Fore.YELLOW}[PRO_TIP: {Fore.GREEN}Fuzz ALL URLs using tools such as ffuf,gobuster,disbuter,etc & then pass urls_list.txt using this argument{Fore.YELLOW}] [NOTE: {Fore.RED}One URL in One Line{Fore.YELLOW}].")    
        parser.add_argument("-f", "--fuzz-scan", dest="fuzz_and_scan", help=f"{Fore.GREEN}Provide a domain for scanning [It will Fuzz ALL URLs using GoBuster & Then It will scan them.] {Fore.YELLOW}") 
        parser.add_argument("-w", "--wordlist", dest="wordlist", help=f"{Fore.GREEN}Provide a wordlist for fuzzing. {Fore.YELLOW}[Only Use With {Fore.GREEN}--fuzz-scan{Fore.YELLOW}]. {Fore.WHITE}default=content_discovery_all.txt{Fore.YELLOW}", default='content_discovery_all.txt') 
        parser.add_argument("-t", "--timeout", dest="timeout", help=f"{Fore.GREEN}HTTP Request Timeout. {Fore.WHITE}default=60{Fore.YELLOW}", default=60)
        parser.add_argument("-th", "--thread", dest="ThreadNumber", help=f"{Fore.GREEN}Parallel HTTP Request Number. {Fore.WHITE}default=100{Fore.YELLOW}", default=100)
        parser.add_argument("-c", "--content-length", dest="ContentLength", help=f"{Fore.GREEN}Any Content Length for Confirming EAR Vulnerability. {Fore.WHITE}default=200{Fore.YELLOW}", default=200)
        parser.add_argument("-o", "--output", dest="output", help=f"{Fore.GREEN}Output filename [Script will save vulnerable urls by given name]. {Fore.WHITE}default=vulnerable.txt{Fore.YELLOW}", default='vulnerable.txt')

        return parser.parse_args()

    def start(self, url):
        self.arguments = self.get_arguments()
        self.ThreadNumber         = int(self.arguments.ThreadNumber)
        self.timeout              = int(self.arguments.timeout)
        self.content_length       = int(self.arguments.ContentLength)
        # url = input("Enter the domain to scan: ")
        self.write_to_queue(f'[*] Fuzzing URLs using GoBuster Tool ...')
        if platform.system() == 'Windows':
            command = ['gobuster.exe', 'dir', '-w', self.arguments.wordlist, '-t', str(self.arguments.timeout), '-x', 'php,asp,aspx,jsp', '-u', url, '-o', 'urls_list.txt', '-q', '-e']
        else:
            command = ['gobuster', 'dir', '-w', self.arguments.wordlist, '-t', str(self.arguments.timeout), '-x', 'php,asp,aspx,jsp', '-u', url, '-o', 'urls_list.txt', '-q', '-e']

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore')

        while True:
            output_line = process.stdout.readline()
            if output_line == '' and process.poll() is not None:
                break
            if output_line:
                self.write_to_queue(output_line)

        self.write_to_queue(f'[*] Initiating Exection After Redirect (EAR) Vulnerability Scanner ...')    
        final_url_list = []

        with open('urls_list.txt') as f:
            data_list = f.readlines()
        
        for url in data_list:
            if url != '\n':
                final_url_list.append(url.split(' ')[0].strip())

        self.total = len(final_url_list)  # Used in showing progressbar 

        # Multi-Threaded Implementation
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.ThreadNumber)
        futures = [executor.submit(self.check_ear, potential_url) for potential_url in final_url_list]
        concurrent.futures.wait(futures)          

    def check_ear(self, url):
        try:
            response = requests.get(url, timeout=60, verify=False, allow_redirects=False)
            # Step-1: Checking Whether Status Code is 302
            status_code = response.status_code
            if status_code == 302:
                # Step-2: Checking Whether 'Location' Header is Present
                if 'Location' in response.headers.keys():
                    response_length = len(response.text)
                    if response_length >= self.content_length:
                        if self.arguments.url:
                            self.write_to_queue(f'{Fore.GREEN}[+] [302] {Fore.WHITE}{url} {Fore.YELLOW}[Location: {Fore.GREEN}{response.headers["Location"]}{Fore.WHITE}] {Fore.YELLOW}[Status: {Fore.GREEN}100% Vulnerable{Fore.YELLOW}]{Style.RESET_ALL}') 
                        self.vulnerable_urls.append(url)
                    else:
                        if self.arguments.url:
                            self.write_to_queue(f'{Fore.GREEN}[+] [302] {Fore.WHITE}{url} {Fore.YELLOW}[Location: {Fore.GREEN}{response.headers["Location"]}{Fore.WHITE}] {Fore.YELLOW}[Status: {Fore.GREEN}Might Be Vulnerable{Fore.YELLOW}]{Style.RESET_ALL}')                    
                        self.vulnerable_urls.append(url)
            else:
                if self.arguments.url:
                    self.write_to_queue(f'{Fore.YELLOW}[-] [{status_code}] {Fore.WHITE}{url}{Fore.YELLOW} ... not vulnerable!{Style.RESET_ALL}  ')
        
            if self.arguments.file_containing_urls or self.arguments.fuzz_and_scan:
                self.progress.append(1)
                self.write_to_queue(f'\r{Fore.YELLOW}[*] ProgressBar: {Fore.WHITE}{len(self.progress)}/{self.total} {Fore.YELLOW}[Errors: {Fore.RED}{len(self.errors)}{Fore.YELLOW}] [Vulnerable: {Fore.GREEN}{len(self.vulnerable_urls)}{Fore.YELLOW}] ... {Style.RESET_ALL}', end="")
        except Exception as e:
            if self.arguments.url:
                self.write_to_queue(f'{Fore.RED}[!] {Fore.YELLOW}[ERROR] : {e} {Fore.YELLOW}[{Fore.GREEN}{url}{Fore.YELLOW}]{Style.RESET_ALL}')
            
            elif self.arguments.file_containing_urls or self.arguments.fuzz_and_scan:
                self.errors.append(1)
                self.progress.append(1)
                self.write_to_queue(f'\r{Fore.YELLOW}[*] ProgressBar: {Fore.WHITE}{len(self.progress)}/{self.total} {Fore.YELLOW}[Errors: {Fore.RED}{len(self.errors)}{Fore.YELLOW}] [Vulnerable: {Fore.GREEN}{len(self.vulnerable_urls)}{Fore.YELLOW}] ... {Style.RESET_ALL}', end="")

def update_text_widget(text_widget, output_queue):
    while True:
        try:
            message = output_queue.get(block=False)
            text_widget.insert(tk.END, message)
            text_widget.see(tk.END)
            text_widget.update_idletasks()
        except queue.Empty:
            pass
        time.sleep(0.1)

# Function to run the EAR_Scanner and capture its output
def run_ear_scanner(scanner, url, output_queue):
    scanner.output_queue = output_queue  # Set the queue to the scanner
    scanner.start(url)

# Tkinter GUI setup
root = tk.Tk()
root.title("EAR Fuzz Scanner")

output_queue = queue.Queue()

url_label = tk.Label(root, text="Enter the URL to scan:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

console_output = scrolledtext.ScrolledText(root, height=20)
console_output.pack()

# Start button command
def start_scan():
    url = url_entry.get()
    if url:
        # Create a scanner instance with a queue
        scanner = EAR_Scanner(output_queue=output_queue)
        # Start the scanner in a separate thread
        Thread(target=run_ear_scanner, args=(scanner, url, output_queue), daemon=True).start()
        # Start updating the GUI from the queue in a separate thread
        Thread(target=update_text_widget, args=(console_output, output_queue), daemon=True).start()
    else:
        console_output.insert(tk.END, "Please enter a URL.\n")

start_button = tk.Button(root, text="Start Fuzz Scan", command=start_scan)
start_button.pack()

root.mainloop()
# if __name__ == '__main__':
#     test = EAR_Scanner()
#     test.start()
        
