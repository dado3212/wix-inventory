from secret import API_KEY, ACCOUNT_ID, SITE_ID
import requests, json, time

PRINTS_COLLECTION = 'fa016b57-2546-b7cc-8a30-743695fe1f5e'

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
    productId = response.json()['product']['id']
    
    url = f"https://www.wixapis.com/stores/v1/products/{productId}/variants"
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
        
    print('Waiting 5 seconds for product to become available for editing...')
    time.sleep(5)

    variantIds = getVariantIDs(productId)
    if updateInventory(productId, variantIds):
        print('Updated inventory.')
    else:
        print('Something went wrong updating variant prices.')
    
    # Add to prints collection
    if addToPrints(productId):
        print('Added to prints.')
    else:
        print('Something went wrong added to prints.')
    print(f'\n\nClick this link to finish setting it up: https://manage.wix.com/dashboard/{SITE_ID}/store/products/product/{productId}')

def addToPrints(productId):
    url = f"https://www.wixapis.com/stores/v1/collections/{PRINTS_COLLECTION}/productIds"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": API_KEY,
        "wix-site-id": SITE_ID,
    }
    data = {
        "productIds": [
            productId
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200
    
def updateInventory(productId, variant_ids):
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
            "variants": [{'variantId': x, 'quantity': 100} for x in variant_ids],
        }
    }

    response = requests.patch(url, headers=headers, json=data)
    if (response.status_code == 200):
        return True
    else:
        print(response.json())
        return False
    
def getVariantIDs(productId):
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
    
    if (response.status_code != 200):
        print("Failed to find item.")
        return
        
    data = response.json()['inventoryItems']
    if (len(data) != 1):
        print("Failed to find item.")
        return
    
    return [x['variantId'] for x in data[0]['variants']]

createProduct()
