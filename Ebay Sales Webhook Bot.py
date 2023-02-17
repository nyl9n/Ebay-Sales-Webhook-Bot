import requests
import json
import time

# Your eBay API credentials
app_id = "YOUR_APP_ID"
cert_id = "YOUR_CERT_ID"
dev_id = "YOUR_DEV_ID"
auth_token = "YOUR_AUTH_TOKEN"

# Your Discord webhook URL
discord_url = "YOUR_DISCORD_WEBHOOK_URL"

# Function to send a message to Discord
def send_to_discord(listing_id, sale_price):
    data = {
        "embeds": [
            {
                "fields": [
                    {
                        "name": "Item Sale Price",
                        "value": f"${sale_price}",
                        "inline": True
                    },
                    {
                        "name": "Listing ID",
                        "value": f"{listing_id}",
                        "inline": True
                    }
                ],
                "title": "Congratulations!",
                "description": "",
                "url": "https://www.ebay.com/mys/overview",
                "color": 11461496
            }
        ],
        "components": [],
        "username": "Ebay Sales",
        "avatar_url": "https://ir.ebaystatic.com/cr/v/c1/ebay-logo-1-1200x1200-margin.png",
        "content": ""
    }
    requests.post(discord_url, data=json.dumps(data), headers={"Content-Type": "application/json"})

# Function to get eBay sales
def get_ebay_sales():
    url = "https://api.ebay.com/sell/fulfillment/v1/order"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        "X-EBAY-C-ENDUSERCTX": "contextualLocation=country=<COUNTRY>,zip=<ZIP_CODE>"
    }
    params = {
        "filter": "orderFulfillmentStatus:{INCOMPLETE}",
        "limit": 1,
        "offset": 0
    }
    response = requests.get(url, headers=headers, params=params)
    response_json = response.json()
    return response_json["orders"]

# Continuously check for new eBay sales and send a message to Discord when detected
while True:
    sales = get_ebay_sales()
    if sales:
        sale = sales[0]
        sale_id = sale["orderId"]
        sale_price = sale["pricingSummary"]["total"]["value"]
        send_to_discord(sale_id, sale_price)
    time.sleep(60) # Wait for 60 seconds before checking again
