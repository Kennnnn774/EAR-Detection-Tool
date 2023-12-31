<a name="readme-top"></a>

<!-- PROJECT LOGO -->
# EAR (Execution After Redirection) Detection tool
<br />
<div align="center">
  <a href="https://github.com/Kennnnn774/EAR-Detection-Tool">
    <img src="images/Search-PNG.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">EAR-Tool-README</h3>

  <p align="center">
    An awesome tool to search EAR and secure your website!
    <br />
    <a href="https://github.com/Kennnnn774/EAR-Detection-Tool"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Kennnnn774/EAR-Detection-Tool/issues">Report Bug</a>
    ·
    <a href="https://github.com/Kennnnn774/EAR-Detection-Tool/issues">Request Feature</a>
  </p>
</div>

## About The Project
EAR Scanner Tools is a set of security tools designed to detect Excessive Access Rights (EAR) vulnerabilities in web applications. It comprises a Chrome extension for real-time scanning of active web pages and a separate fuzz scanning tool that searches for and scans subdomains.

## Features

- **Chrome Extension**: 
    - Allows users to scan the currently active website in their browser for EAR vulnerabilities.
    - If the current tab's URL is vulnerable to EAR, the extension will display the vulnerability details.

- **Fuzz Scanner**: 
    - Discovers subdomains for a given domain and scans each one for EAR vulnerabilities.
    - Results will be displayed in the console and saved to a log file.

- **Database Integration**: 
    - Saves scan results to a database to prevent redundant scanning and speed up the process by using cached results within a 10-day window.

### Built With

Here are major frameworks/libraries we used to build our project.
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* [MongoDB](https://www.mongodb.com/)
* [gobuster](https://github.com/OJ/gobuster)

## Getting Started
### Chrome Extension
![extension](https://i.imgur.com/RGRbjQb.png)
1. Git clone and repo and navigate to the folder

```bash
git clone https://github.com/Kennnnn774/EAR-Detection-Tool.git
cd EAR-Detection-Tool
```

2. OPTIONAL: To run locally, install the required Python packages. ONLY DO THIS if you are running this locally rather than with the hosted service- typically would just be for testing.
```sh
pip install -r requirements.txt
```
Additionally, create a .env file with a 'DB_API_KEY' and 'DB_URL_API_BASE' as keys, with an api key and base url from MongoDB Atlas. ONLY DO THIS if you are running this locally rather than with the hosted service- typically would just be for testing.

![image](https://github.com/Kennnnn774/EAR-Detection-Tool/assets/76461173/02f89fa3-4c14-48f8-ae2e-c611187168a3)

Finally, change the url in 'scripts/content.js' on line 4 to the localhost url. ONLY DO THIS if you are running it locally rather than with the hosted service- typically would just be for testing. To switch it back to the hosted service, remove the localhost URL and replace it with 'https://ear-extension-backend.onrender.com/scan'

3. Load the Chrome extension into your browser
    - Navigate to chrome://extensions/
    - Enable Developer mode
    - Click on Load unpacked and select the entire folder from the cloned repository.

### Fuzz Scan Tool 
![fuzzscantool](https://i.imgur.com/boqVmIL.png)
1. After cloning the repository, install the required Python packages
```sh
pip install -r requirements.txt
```
2. navigate to the `fuzz_scan_tool`folder after following the previous two steps

```bash
cd fuzz_scan_tool
```

3. Run the fuzz scanner tool:
```bash
python fuzz_scan.py
```


## Contributing

Contributions are what make the development community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork this repo and create a pull request. 

Don't forget to give the project a star! :star: Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b`)
3. Commit your Changes (`git commit -m 'RandomMessage'`)
4. Push to the Branch (`git push origin`)
5. Open a Pull Request

## Contact (listed in alphabetical order)
- Emily Berger - [@heyitsM](https://github.com/heyitsM) - eberge11@jh.edu
- Aya Habbas - [@ahabbs20](https://github.com/ahabbs20) - ahabbas1@jh.edu
- Yujian (Ken) He - [@Kennnnn774](https://github.com/Kennnnn774) - yhe99@jhu.edu

## Acknowledgments

We are thankful for these resources which have helped us on our development journey:

* [Paper: Fear the EAR: Discovering and Mitigating Execution After Redirect Vulnerabilities](https://sites.cs.ucsb.edu/~chris/research/doc/ccs11_ear.pdf)
* [gobuster tool](https://github.com/OJ/gobuster)

