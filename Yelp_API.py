# #Transaction Search   URL -- 'https://api.yelp.com/v3/transactions/{transaction_type}/search'
# #Autocomplete         URL -- 'https://api.yelp.com/v3/autocomplete'
# #Categories           URL -- 'https://api.yelp.com/v3/categories'
# #Categories Alias     URL -- 'https://api.yelp.com/v3/categories/{alias}'
# # Import the modules
# import requests
# import json
# # Define a business ID
# business_id = '3_TnIeQNt3Wgpn6rMjcwQA'
# # Define API Key, Search Type, and header
# MY_API_KEY = 'Gg65rpmjeX_dtHi23G6_dX9GrUnRI8i-p5x4SSTcmyUi8C2pElUS-bvsn2nbuIrPc1QvfxV9lMxvGeVGmkeI3D8b8tIw7CfTqdvr36sXpCtPSIjMO493ccuH5QHqZnYx'
# ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
# HEADERS = {'Authorization': 'bearer %s' % MY_API_KEY}
# def yelp_api_request(params=None):
#     try:
#         response = requests.get(ENDPOINT, headers=HEADERS, params=params)
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error making request to Yelp API: {e}")
#         return None
# def search_restaurants(location, term='restaurants', limit=10):
#     params = {
#         'location': location,
#         'term': term,
#         'limit': limit
#     }
#     return yelp_api_request(params)












#Transaction Search   URL -- 'https://api.yelp.com/v3/transactions/{transaction_type}/search'
#Autocomplete         URL -- 'https://api.yelp.com/v3/autocomplete'
#Categories           URL -- 'https://api.yelp.com/v3/categories'
#Categories Alias     URL -- 'https://api.yelp.com/v3/categories/{alias}'
# Import the modules
import requests
import json
# Define a business ID
# business_id = '3_TnIeQNt3Wgpn6rMjcwQA'
# Define API Key, Search Type, and header
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



