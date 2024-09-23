import requests
import json

MY_API_KEY = '4Z2h2Gios3QOnYb-UZ-qDhMs8udoVoB5OTPLFdD13gtsxCHEWBVjWDuuj6zJPO4l5FfnGHJfpxbaqYCKRrgXzydXRYKxfK-nZww7S3mfnNqfpMhEuBxKTdMOMF_sZnYx'
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
# THis function is actually getting the response via the given restaurant id using the Yelp API connection established in the previous function.
def get_restaurant_details_by_id(restaurant_id):
    # Call the Yelp API using the business ID
    response = yelp_api_request_by_id(restaurant_id)
    
    if response is None:
        return None

    restaurant_info = {
        'name': response.get('name'),
        'location': ', '.join(response.get('location', {}).get('display_address', [])),
        'phone': response.get('display_phone')  # You can change this to another attribute if you prefer
    }

    return restaurant_info
