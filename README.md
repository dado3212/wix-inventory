# wix-inventory
A Python script for uploading to Wix and syncing to Instagram

## Initially Install

Check out this repo and run the following commands to install the necessary Python libraries:
```
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
```

From https://manage.wix.com/account/api-keys generate an API key and add it to a file called secret.py with the format
```
TOKEN = '<insert token>'
```