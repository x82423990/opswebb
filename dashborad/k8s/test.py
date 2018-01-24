from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint

# Configure API key authorization: BearerToken
configuration = kubernetes.client.Configuration()
configuration.api_key['authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['authorization'] = 'Bearer'

# create an instance of the API class
api_instance = kubernetes.client.AdmissionregistrationApi(kubernetes.client.ApiClient(configuration))

try:
    api_response = api_instance.get_api_group()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdmissionregistrationApi->get_api_group: %s\n" % e)