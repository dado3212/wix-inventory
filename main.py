from secret import API_KEY, ACCOUNT_ID, SITE_ID
import requests

def getProducts():
    url = "https://www.wixapis.com/stores/v1/products/query"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": API_KEY,
        "wix-site-id": SITE_ID,
    }
    data = {
        "query": {
            # "filter": "{\"paymentStatus\":\"PAID\"}",
            # "sort": "{\"number\": \"desc\"}",
            "paging": {
                "limit": "50"
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())

getProducts()