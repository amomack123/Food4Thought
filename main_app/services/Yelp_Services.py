# from Yelp_API import search_restaurants

# def get_restaurants_by_id(location, term='restaurants', limit=10):
    
#     # Call Yelp API function from yelp_api.py
#     response = search_restaurants(location=location, term=term, limit=limit)
    
#     if response is None:
#         return [] 
    
#     businesses = response.get('businesses', [])
    

#     restaurant_data = []
#     for business in businesses:
#         restaurant_info = {
#             'name': business.get('name'),
#             'location': ', '.join(business['location'].get('display_address', [])),
#             'phone': business.get('display_phone')
#         }
#         restaurant_data.append(restaurant_info)
    
#     return restaurant_data
