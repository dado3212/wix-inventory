from secret import API_KEY, ACCOUNT_ID, SITE_ID
import requests, json

PRINTS_COLLECTION = '2102ce4e-5949-5f58-4b2c-40688ecd5cb3'

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
    print(productId)

    variantIds = getVariantIDs(productId)
    print(variantIds)
    updateInventory(productId, variantIds)
    
    # Add to prints collection
    addToPrints(productId)


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

    response = requests.patch(url, headers=headers, json=data)
    
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
    print(response.json())
    
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
            "filter": json.dumps({'productId': productId}),
            "paging": {
                "limit": "50"
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    
    if (response.status_code != 200):
        print("Failed to find item.")
        return
        
    data = response.json()['inventoryItems']
    if (len(data) != 1):
        print("Failed to find item.")
        return
    
    return [x['variantId'] for x in data[0]['variants']]

# getInventory()
# product = '47b33cd2-57fc-40f5-9466-d2b757b07894'
# variant_ids = getVariantIDs('47b33cd2-57fc-40f5-9466-d2b757b07894')
# updateInventory(product, variant_ids)
# # updateInventory(
createProduct()