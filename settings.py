SITE = 'vancouver'

# Bike

# WRAPPER = 'CraigslistForSale'
# CATEGORY = 'bia'
# FILTERS = {'bicycle_frame_material': ['carbon fiber', 'composite']}

# Housing

WRAPPER = 'CraigslistHousing'
CATEGORY = 'hhh'
FILTERS = extra_filters = {
    'has_image': True,
    'max_price': 1400,
    'search_distance': 3,
    'bundle_duplicates': True,
    'zip_code': 'V5T2Z3',
    # 'zip_code': 'V7M1B1',
    'laundry': 'w/d in unit',
}
