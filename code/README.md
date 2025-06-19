# wix-inventory
A Python script for uploading to Wix and syncing to Instagram.


## Initial Install
Check out this repo and run the following commands to install the necessary Python libraries:
```
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

From https://manage.wix.com/account/api-keys generate an API key. Then create a new file with `touch secret.py` and add three constants to it with the format
```
API_KEY = '<insert api key>'
ACCOUNT_ID = '<account id>'
SITE_ID = '<site id>'
```

The `API_KEY` is the API Key you created. The `ACCOUNT_ID` is on the right side of the aforementioned API keys page. The `SITE_ID` is the alphanumeric if you go to your site dashboard and copy the `<code>` from the URL in the format `https://manage.wix.com/dashboard/<code>/home?referralInfo=my-sites`.

You'll then need to double-click the `.command` files and unblock them in Settings > Privacy & Security. You should only have to do this once.

You then need to automatically forward product items from Wix to Instagram. You can do this by <TODO>

## Developing
https://dev.wix.com/docs/rest/ has the full REST API.
