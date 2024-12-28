from secret import API_KEY, ACCOUNT_ID, SITE_ID
import requests, json, time

'''
This is a one-off script. We load all of the products in the shop, clear their variants, and establish the new ones.

Lots of copy-and-paste from main.py, this is hacky because I don't expect to use this again.
'''

PRINTS_COLLECTION = 'fa016b57-2546-b7cc-8a30-743695fe1f5e'
PRODUCTS = {
    "11x14 Print": 50,
    "16x20 Print": 70,
    "16x20 Ready-to-Hang Canvas": 300,
    "24x30 Ready-to-Hang Canvas": 400,
}

# Load all of the products
url = "https://www.wixapis.com/stores/v1/products/query"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Authorization": API_KEY,
    "wix-site-id": SITE_ID,
}
data = {
    "query": {
        "paging": {
            "limit": 100,
        }
    },
    # Filtering collections.id doesn't seem to work, so do it manually
}

response = requests.post(url, headers=headers, json=data)
for item in response.json()['products']:
    if PRINTS_COLLECTION not in item['collectionIds']:
        continue
    
    # print(json.dumps(item, indent=2))
    # continue
    print('Processing ' + item['name'])

    # Update to new variant info
    productId = item['id']
    
    url = f"https://www.wixapis.com/stores/v1/products/{productId}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": API_KEY,
        "wix-site-id": SITE_ID,
    }
    data = {
       "product": {
           "priceData": {
                "price": 50 # default price for the 11x14
            },
            "costAndProfitData": {
                "itemCost": 17 # default cost for the 11x14
            },
            "additionalInfoSections": [
                {
                    "title": "Free Shipping",
                    "description": "Will ship anywhere in the US! I live in a van and camp pretty often, so please be patient with ship times, it may be up to a month.",
                },
            ],
            "manageVariants": True,
            "productOptions": [
                {
                    "name": "Size",
                    "choices": [{"value": x, "description": x} for x in PRODUCTS.keys()],
                }
            ],
       }
        # Filtering collections.id doesn't seem to work, so do it manually
    }

    response = requests.patch(url, headers=headers, json=data)
    
    url = f"https://www.wixapis.com/stores/v1/products/{productId}/variants"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": API_KEY,
        "wix-site-id": SITE_ID,
    }
    data = {
        "variants": [{"choices": {"Size": x}, "price": PRODUCTS[x]} for x in PRODUCTS.keys()],
    }

    response = requests.patch(url, headers=headers, json=data)
    
    time.sleep(5)
    
    url = "https://www.wixapis.com/stores-reader/v2/inventoryItems/query"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": API_KEY,
        "wix-site-id": SITE_ID,
    }
    data = {
        "query": {
            "filter": "{\"productId\": \"" + productId + "\"}",
            "paging": {
                "limit": "50"
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    data = response.json()['inventoryItems']
    variantIds = [x['variantId'] for x in data[0]['variants']]
    
    url = f"https://www.wixapis.com/stores/v2/inventoryItems/product/{productId}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": API_KEY,
        "wix-site-id": SITE_ID,
    }
    data = {
        "inventoryItem": {
            "trackQuantity": True,
            "variants": [{'variantId': x, 'quantity': 100} for x in variantIds],
        }
    }

    response = requests.patch(url, headers=headers, json=data)