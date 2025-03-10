import os
import logging
from distutils.util import strtobool
import digikey.oauth.oauth2
from digikey.exceptions import DigikeyError
from digikey.v4.productinformation import (KeywordRequest, KeywordResponse, ProductDetails, DigiReelPricing,
                                           )
from digikey.v4.productinformation.rest import ApiException
from digikey.v4.ordersupport import (OrderStatusResponse, SalesOrderHistoryItem)
from digikey.v4.batchproductdetails import (BatchProductDetailsRequest, BatchProductDetailsResponse)

logger = logging.getLogger(__name__)


class DigikeyApiWrapper(object):
    def __init__(self, wrapped_function, module):
        self.sandbox = False

        apinames = {
            digikey.v4.productinformation: 'products',
            digikey.v4.ordersupport: 'OrderDetails',
            digikey.v4.batchproductdetails: 'BatchSearch'
        }

        apiclasses = {
            digikey.v4.productinformation: digikey.v4.productinformation.ProductSearchApi,
            digikey.v4.ordersupport: digikey.v4.ordersupport.OrderDetailsApi,
            digikey.v4.batchproductdetails: digikey.v4.batchproductdetails.BatchSearchApi
        }

        apiname = apinames[module]
        apiclass = apiclasses[module]

        # Configure API key authorization: apiKeySecurity
        configuration = module.Configuration()
        configuration.api_key['X-DIGIKEY-Client-Id'] = os.getenv('DIGIKEY_CLIENT_ID')

        # Return quietly if no clientid has been set to prevent errors when importing the module
        if os.getenv('DIGIKEY_CLIENT_ID') is None or os.getenv('DIGIKEY_CLIENT_SECRET') is None:
            raise DigikeyError('Please provide a valid DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET in your env setup')

        # Use normal API by default, if DIGIKEY_CLIENT_SANDBOX is True use sandbox API
        configuration.host = 'https://api.digikey.com/' + apiname + '/v4'
        try:
            if bool(strtobool(os.getenv('DIGIKEY_CLIENT_SANDBOX'))):
                configuration.host = 'https://sandbox-api.digikey.com/' + apiname + '/v4'
                self.sandbox = True
        except (ValueError, AttributeError):
            pass

        # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
        # configuration.api_key_prefix['X-DIGIKEY-Client-Id'] = 'Bearer'

        # Configure OAuth2 access token for authorization: oauth2AccessCodeSecurity
        self._digikeyApiToken = digikey.oauth.oauth2.TokenHandler(version=3, sandbox=self.sandbox).get_access_token()
        configuration.access_token = self._digikeyApiToken.access_token

        # create an instance of the API class
        self._api_instance = apiclass(module.ApiClient(configuration))

        # Populate reused ids
        self.authorization = self._digikeyApiToken.get_authorization()
        self.x_digikey_client_id = os.getenv('DIGIKEY_CLIENT_ID')

        self.wrapped_function = wrapped_function

    @staticmethod
    def _remaining_requests(header, api_limits):
        try:
            rate_limit = header['X-RateLimit-Limit']
            rate_limit_rem = header['X-RateLimit-Remaining']

            if api_limits is not None and type(api_limits) == dict:
                api_limits['api_requests_limit'] = int(rate_limit)
                api_limits['api_requests_remaining'] = int(rate_limit_rem)

            logger.debug('Requests remaining: [{}/{}]'.format(rate_limit_rem, rate_limit))
        except (KeyError, ValueError) as e:
            logger.debug(f'No api limits returned -> {e.__class__.__name__}: {e}')
            if api_limits is not None and type(api_limits) == dict:
                api_limits['api_requests_limit'] = None
                api_limits['api_requests_remaining'] = None

    @staticmethod
    def _store_api_statuscode(statuscode, status):
        if status is not None and type(status) == dict:
            status['code'] = int(statuscode)

        logger.debug('API returned code: {}'.format(statuscode))

    def call_api_function(self, *args, **kwargs):
        try:
            # If optional api_limits, status mutable object is passed use it to store API limits and status code
            api_limits = kwargs.pop('api_limits', None)
            status = kwargs.pop('status', None)

            func = getattr(self._api_instance, self.wrapped_function)
            logger.debug(f'CALL wrapped -> {func.__qualname__}')
            api_response = func(*args, self.x_digikey_client_id, authorization = self.authorization, **kwargs)
            self._remaining_requests(api_response[2], api_limits)
            self._store_api_statuscode(api_response[1], status)

            return api_response[0]
        except ApiException as e:
            logger.error(f'Exception when calling {self.wrapped_function}: {e}')
            self._store_api_statuscode(e.status, status)


def keyword_search(*args, **kwargs) -> KeywordResponse:
    client = DigikeyApiWrapper('keyword_search_with_http_info', digikey.v4.productinformation)

    if 'body' in kwargs and type(kwargs['body']) == KeywordRequest:
        logger.info(f'Search for: {kwargs["body"].keywords}')
        logger.debug('CALL -> keyword_search')
        return client.call_api_function(*args, **kwargs)
    else:
        raise DigikeyError('Please provide a valid KeywordSearchRequest argument')


def product_details(*args, **kwargs) -> ProductDetails:
    client = DigikeyApiWrapper('product_details_with_http_info', digikey.v4.productinformation)

    if len(args):
        logger.info(f'Get product details for: {args[0]}')
        return client.call_api_function(*args, **kwargs)


def digi_reel_pricing(*args, **kwargs) -> DigiReelPricing:
    client = DigikeyApiWrapper('digi_reel_pricing_with_http_info', digikey.v4.productinformation)

    if len(args):
        logger.info(f'Calculate the DigiReel pricing for {args[0]} with quantity {args[1]}')
        return client.call_api_function(*args, **kwargs)


def suggested_parts(*args, **kwargs) -> ProductDetails:
    client = DigikeyApiWrapper('suggested_parts_with_http_info', digikey.v4.productinformation)

    if len(args):
        logger.info(f'Retrieve detailed product information and two suggested products for: {args[0]}')
        return client.call_api_function(*args, **kwargs)


def status_salesorder_id(*args, **kwargs) -> OrderStatusResponse:
    client = DigikeyApiWrapper('order_status_with_http_info', digikey.v4.ordersupport)

    if len(args):
        logger.info(f'Get order details for: {args[0]}')
        return client.call_api_function(*args, **kwargs)


def salesorder_history(*args, **kwargs) -> [SalesOrderHistoryItem]:
    client = DigikeyApiWrapper('order_history_with_http_info', digikey.v4.ordersupport)

    if 'start_date' in kwargs and type(kwargs['start_date']) == str \
            and 'end_date' in kwargs and type(kwargs['end_date']) == str:
        logger.info(f'Searching for orders in date range ' + kwargs['start_date'] + ' to ' + kwargs['end_date'])
        return client.call_api_function(*args, **kwargs)
    else:
        raise DigikeyError('Please provide valid start_date and end_date strings')


def batch_product_details(*args, **kwargs) -> BatchProductDetailsResponse:
    client = DigikeyApiWrapper('batch_product_details_with_http_info', digikey.v4.batchproductdetails)

    if 'body' in kwargs and type(kwargs['body']) == BatchProductDetailsRequest:
        logger.info(f'Batch product search: {kwargs["body"].products}')
        logger.debug('CALL -> batch_product_details')
        return client.call_api_function(*args, **kwargs)
    else:
        raise DigikeyError('Please provide a valid BatchProductDetailsRequest argument')
