## Script for get passport data from ESIA and the employment history

## How to run this app?
1) Create a project directory.
2) Change into the project directory.
3) Create virtual environment: 
  ```bash
  pip install virtualenv
  ```
  ```bash
  virtualenv venv --python=<YOUR_PYTHON_VERSION>
  ``` 
  For example: 
  ```bash 
  virtualenv venv --python=3.7.6
  ```
4) Activate virtual environment: 
  ```bash 
  venv/Scripts/activate
  ```
5) Install [python packages](https://github.com/ZaytsevNS/esia_get_data/blob/main/requirements.txt) into a virtual environment:
  ```bash 
  pip install -r requirements.txt
  ```
6) Download [ChromeDriver](https://chromedriver.chromium.org/downloads)
7) Change this line, where executable_path is directory path that contains the executable:
  ```python
  driver = webdriver.Chrome(executable_path=r"YOUR_PATH", chrome_options=options)
  ```
8) Run [esia.py](https://github.com/ZaytsevNS/esia_get_data/blob/main/esia.py)
9) When you’re done working on a project deactivate virtual environment: 
  ```bash 
  venv/Scripts/deactivate
  ```
  
**Passport file after run script**:
![PassportFile](https://github.com/ZaytsevNS/esia_get_data/blob/main/passport.jpg)

**Project directory after run script**
![Directory](https://github.com/ZaytsevNS/esia_get_data/blob/main/directory.jpg)
