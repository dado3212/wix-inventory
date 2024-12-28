# wix-inventory
A Python script for uploading to Wix and syncing to Instagram

## Initial Install
Check out this repo and run the following commands to install the necessary Python libraries:
```
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

From https://manage.wix.com/account/api-keys generate an API key. Then we need to add three constants to a file called secret.py with the format
```
API_KEY = '<insert api key>'
ACCOUNT_ID = '<account id>'
SITE_ID = '<site id>'
```

The `API_KEY` is the API Key you created. The `ACCOUNT_ID` is on the right side of the aforementioned API keys page. The `SITE_ID` is the alphanumeric if you go to your site dashboard and copy the `<code>` from the URL in the format `https://manage.wix.com/dashboard/<code>/home?referralInfo=my-sites`.

## Developing
https://dev.wix.com/docs/rest/ has the full REST API.