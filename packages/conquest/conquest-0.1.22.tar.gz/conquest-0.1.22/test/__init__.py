import dotenv
import os

dotenv.load_dotenv()
print('Environment variables loaded, using host: {}'.format(os.environ['API_HOST']))

API_HOST=os.environ['API_HOST']
PREFIX = 'Bearer'
API_TOKEN='{} {}'.format(PREFIX, os.environ['API_TOKEN'])
print('Using host {}'.format(API_HOST))

import conquest as c
config = c.Configuration()
config.host = API_HOST
config.api_key['Authorization'] = API_TOKEN
config.api_key_prefix['Authorizations'] = PREFIX
api_instance = c.ApiClient(configuration=config)