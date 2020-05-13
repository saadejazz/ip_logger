# IP Logger Automation  
Automates the use of [iplogger.org](https://www.iplogger.org) to perform these two tasks:  
1. Create shortened URLs (along with a tracking code)
2. Track users who clicked the link (using the tracking code)

## Getting Started  

* Download this repository using git  

   ```bash
   mkdir ip_logger
   cd ip_logger
   git init
   git add .
   git remote add origin https://www.github.com/saadejazz/ip_logger
   git pull origin master
   cd ..
   ```

* Install Tor service on Ubuntu.   

   Install tor service on Ubuntu using  
   ```bash
   sudo apt install tor
   ```
   Start the service using  
   ```bash
   sudo service start tor
   ```
   OR  
   ```bash
   sudo killall tor
   tor
   ```
   Make sure you have tor running before you run scripts. Also update the config file as following: Open /etc/tor/torrc and uncomment the following line  
   ```bash
   # ControlPort 9051
   ```

* Install python dependencies  
   ```bash
   python -m pip install selenium bs4 stem validators
   ```

## Usage 

1. For URL shortening:  
    **Code:**  
    ```python
    from ip_logger.logger import IpLogger

    url = "https://www.google.com"
    log = IpLogger(headless = False, timeout = 10) # Can be instantiated only once
    print(log.create_payload(url))
    ```

    **Output:**  
    ```python
    {
    'original_url': 'https://www.google.com',
    'payload_url': 'https://2no.co/2e2Ym5',
    'tracking_code': '9et85d2e2Ym5',
    'tracking_url': 'https://www.iplogger.org/logger/9et85d2e2Ym5',
    'is_successful': True
    }
    ```

2. For tracking logger url using code:    
    **Code:**  
    ```python
    from ip_logger.logger import IpLogger

    log = IpLogger(headless = False, timeout = 10)
    print(log.track_code(code = 'rat2t42ePvm5', start_date = "2020-05-12", end_date = "2020-05-12"))
    ```

    **Output:**  
    ```python
    {
    "code_exists": True,
    "data":[{
    'timestamp': {'date': '12.05.2020', 'time': '14:31:22'},
    'network_information': {'ip_address': '39.45.230.243',
    'isp': 'Pakistan Telecommuication company limited'},
    'location_information': {'country': 'Pakistan', 'city': 'Siālkot'},
    'device_info': {'os': 'Linux x86.64.',
    'browser': 'Firefox 76.0',
    'user_agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    }]}
    ```
