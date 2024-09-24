import requests
import json

MY_API_KEY = 'AuahkYV8gyLfJjQW9d7B-W0JEVNbeeojSLFHbNC5vGp_SXfr2wj6nPb2aqbc3CRbmhOPxgAmDqwj08L2KH-GNa3fCTU3F7Jk2NMdVigSE6P72tYPVxy99q-SbWDsZnYx'
ENDPOINT = 'https://api.yelp.com/v3/businesses/'
HEADERS = {'Authorization': 'bearer %s' % MY_API_KEY}
# This function is contacting the Yelp API through our endpoint and checking for error handling as well.
def yelp_api_request_by_id(restaurant_id):
    try:
        response = requests.get(url=f"{ENDPOINT}{restaurant_id}", headers=HEADERS)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request to Yelp API: {e}")
        return None

def get_restaurant_details_by_id(restaurant_id):
    # Call the Yelp API using the business ID
    response = yelp_api_request_by_id(restaurant_id)
    
    if response is None:
        return None

    restaurant_info = {
        'name': response.get('name'),
        'location': ', '.join(response.get('location', {}).get('display_address', [])),
        'phone': response.get('display_phone'), 
        'category': response.get('categories')[0]['title'] if response.get('categories') else 'Unknown',
        'image_url': response.get('image_url', 'default-image-url'),
    }

    return restaurant_info