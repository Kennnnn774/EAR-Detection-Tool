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
        parser = argparse.ArgumentParser(description="default argument for fuzz scan tool")

        parser.add_argument("-f", "--fuzz-scan", dest="fuzz_and_scan", default=True) 
        parser.add_argument("-w", "--wordlist", dest="wordlist", default='content_discovery_all.txt') 
        parser.add_argument("-t", "--timeout", dest="timeout", default=60)
        parser.add_argument("-th", "--thread", dest="ThreadNumber", default=100)
        parser.add_argument("-c", "--content-length", dest="ContentLength", default=200)

        return parser.parse_args()

    def start(self, url):
        self.arguments = self.get_arguments()
        self.ThreadNumber         = int(self.arguments.ThreadNumber)
        self.timeout              = int(self.arguments.timeout)
        self.content_length       = int(self.arguments.ContentLength)


        self.write_to_queue(f'[****] Fuzzing URLs using GoBuster Tool ...')
        if platform.system() == 'Windows':
            command = ['gobuster.exe', 'dir', '-w', self.arguments.wordlist, '-t', str(self.arguments.timeout), '-x', 'php,asp,aspx,jsp', '-u', url, '-o', 'urls_list.txt', '-q', '-e']
        else:
            command = ['gobuster', 'dir', '-w', self.arguments.wordlist, '-t', str(self.arguments.timeout), '-x', 'php,asp,aspx,jsp', '-u', url, '-o', 'urls_list.txt', '-q', '-e']

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore')

        #using queue to poll all the message to the frontend rool
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
                        self.write_to_queue(f'[+] [302] {url} [Location: {response.headers["Location"]}] [Status: 100% Vulnerable]{Style.RESET_ALL}') 
                        self.vulnerable_urls.append(url)
                    else:
                        self.write_to_queue(f'[+] [302] {url} [Location: {response.headers["Location"]}] [Status: Might Be Vulnerable]{Style.RESET_ALL}')                    
                        self.vulnerable_urls.append(url)
            else:
                self.write_to_queue(f'[-] [{status_code}] {url} ... not vulnerable!{Style.RESET_ALL}  ')

            self.progress.append(1)
            self.write_to_queue(f'\r[*] ProgressBar: {len(self.progress)}/{self.total} [Errors: {len(self.errors)}] [Vulnerable: {len(self.vulnerable_urls)}] ... {Style.RESET_ALL}', end="")
        except Exception as e:
            self.write_to_queue(f'[!] [ERROR] : {e} [{url}]{Style.RESET_ALL}')    
            self.errors.append(1)
            self.progress.append(1)
            self.write_to_queue(f'\r[*] ProgressBar: {len(self.progress)}/{self.total} [Errors: {len(self.errors)}] [Vulnerable: {len(self.vulnerable_urls)}] ... {Style.RESET_ALL}', end="")

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

def run_ear_scanner(scanner, url, output_queue):
    scanner.output_queue = output_queue  
    scanner.start(url)

root = tk.Tk()
root.title("EAR Fuzz Scanner")

output_queue = queue.Queue()

url_label = tk.Label(root, text="Enter the URL to scan:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

console_output = scrolledtext.ScrolledText(root, height=20)
console_output.pack()

def start_scan():
    url = url_entry.get()
    if url:
        # Create a scanner instance with a queue
        scanner = EAR_Scanner(output_queue=output_queue)
        Thread(target=run_ear_scanner, args=(scanner, url, output_queue), daemon=True).start()
        Thread(target=update_text_widget, args=(console_output, output_queue), daemon=True).start()
    else:
        console_output.insert(tk.END, "Please enter a URL.\n")

start_button = tk.Button(root, text="Start Fuzz Scan", command=start_scan)
start_button.pack()

root.mainloop()
        
