from secret import API_KEY, ACCOUNT_ID, SITE_ID
import requests

'''
Create a new product. There will be a base image.
'''
def createProduct():
    products = {
        "11x14 Print": 50,
        "16x20 Print": 70,
        "16x20 Ready-to-Hang Canvas": 300,
        "24x30 Ready-to-Hang Canvas": 400,
    }
    
    url = "https://www.wixapis.com/stores/v1/products"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": API_KEY,
        "wix-site-id": SITE_ID,
    }
    data = {
        "product": {
            "name": "New Product [RENAME]",
            "productType": "physical",
            "visible": False, # by default it won't be visible, you will need to update it first
            "description": "Description [EDIT]",
            "priceData": {
                "price": 50 # default price for the 11x14
            },
            "costAndProfitData": {
                "itemCost": 17 # default cost for the 11x14
            },
            "additionalInfoSections": [
                {
                    "title": "Free Shipping",
                    "description": "Will ship anywhere in the US! I live in a van and camp pretty often, so please be patient with ship times, it may be up to a month.",
                },
            ],
            "manageVariants": True,
            "productOptions": [
                {
                    "name": "Size",
                    "choices": [{"value": x, "description": x} for x in products.keys()],
                }
            ],
        }
    }
    

    response = requests.post(url, headers=headers, json=data)
    
    if (response.status_code != 200):
        print('Error, not created successfully.')
        return
    
    # And setup the variants
    new_id = response.json()['product']['id']
    
    url = f"https://www.wixapis.com/stores/v1/products/{new_id}/variants"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": API_KEY,
        "wix-site-id": SITE_ID,
    }
    data = {
        "variants": [{"choices": {"Size": x}, "price": products[x]} for x in products.keys()],
    }

    response = requests.patch(url, headers=headers, json=data)
    print(response.json())

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

createProduct()