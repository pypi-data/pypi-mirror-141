import os
import requests
from urllib.parse import urlparse, urlencode

from .utils import valid_public_api_key, valid_secret_api_key
from .utils import valid_order_id, valid_payment_id
from .utils import validate_checkout_session_payload, normalize_checkout_session_payload

from .version import __version__

API_PREFIX = 'https://api.smartpay.co/v1'
CHECKOUT_URL = 'https://checkout.smartpay.co'

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

STATUS_SUCCEEDED = 'succeeded'
STATUS_REJECTED = 'rejected'
STATUS_FAILED = 'failed'
STATUS_REQUIRES_AUTHORIZATION = 'requires_authorization'

api_prefix_candidate = os.environ.get('SMARTPAY_API_PREFIX', None)

SMARTPAY_API_PREFIX = api_prefix_candidate if api_prefix_candidate and 'api.smartpay' in api_prefix_candidate else None
SMARTPAY_CHECKOUT_URL = os.environ.get('SMARTPAY_CHECKOUT_URL', None)


class Smartpay:
    REJECT_REQUEST_BY_CUSTOMER = 'requested_by_customer'
    REJECT_FRAUDULENT = 'fraudulent'

    def __init__(self, secret_key, public_key=None, api_prefix=None, checkout_url=None):
        if not secret_key:
            raise Exception('Secret Key is required.')

        if not valid_secret_api_key(secret_key):
            raise Exception('Secret Key is invalid.')

        if public_key and not valid_public_api_key(public_key):
            raise Exception('Public Key is invalid.')

        self._secret_key = secret_key
        self._public_key = public_key
        self._api_prefix = api_prefix or SMARTPAY_API_PREFIX or API_PREFIX
        self._checkout_url = checkout_url or SMARTPAY_CHECKOUT_URL or CHECKOUT_URL

    def request(self, endpoint, method='GET', params=None, payload=None):
        r = requests.request(method, '%s%s' % (self._api_prefix, endpoint), headers={
            'Authorization': 'Basic %s' % (self._secret_key,),
        }, params=params, json=payload)

        if r.status_code < 200 or r.status_code > 299:
            raise Exception('%s: %s' % (r.status_code, r.text))

        return r.json()

    def normalize_checkout_session_payload(self, payload):
        normalize_payload = normalize_checkout_session_payload(payload)
        errors = validate_checkout_session_payload(normalize_payload)

        if len(errors) > 0:
            raise Exception(errors)

        return normalize_payload

    def create_checkout_session(self, payload):
        normalized_payload = self.normalize_checkout_session_payload(payload)

        params = {
            'dev-lang': 'python',
            'sdk-version': __version__,
        }

        session = self.request(
            '/checkout-sessions', POST, params, payload=normalized_payload)

        try:
            session['url'] = self.get_session_url(session, {
                'promotionCode': payload.get('promotionCode', None)
            })
        except Exception:
            pass

        return session

    def get_orders(self, page_token=None, max_results=None, expand=None):
        params = {
            'dev-lang': 'python',
            'sdk-version': __version__,
            'pageToken': page_token,
            'maxResults': max_results,
            'expand': expand,
        }

        return self.request('/orders', GET, params)

    def get_order(self, id=None, expand=None):
        if not id:
            raise Exception('Order Id is required.')

        params = {
            'dev-lang': 'python',
            'sdk-version': __version__,
            'expand': expand,
        }

        return self.request('/orders/%s' % id, GET, params)

    def create_payment(self, order=None, amount=None, currency=None, reference=None, description=None, metadata=None):
        if not order:
            raise Exception('Order Id is required.')

        if not amount:
            raise Exception('Payment Amount is required.')

        if not currency:
            raise Exception('Payment Amount Currency is required.')

        params = {
            'dev-lang': 'python',
            'sdk-version': __version__,
        }

        payload = {
            'order': order,
            'amount': amount,
            'currency': currency,
            'reference': reference,
            'description': description,
            'metadata': metadata,
        }

        return self.request('/payments', POST, params, payload=payload)

    def capture(self, **kwargs):
        return self.create_payment(**kwargs)

    def create_refund(self, payment=None, amount=None, currency=None, reason=None, reference=None, description=None, metadata=None):
        if not payment:
            raise Exception('Payment Id is required.')

        if not amount:
            raise Exception('Refund Amount is required.')

        if not currency:
            raise Exception('Refund Amount Currency is required.')

        if not reason:
            raise Exception('Refund Reason is required.')

        params = {
            'dev-lang': 'python',
            'sdk-version': __version__,
        }

        payload = {
            'payment': payment,
            'amount': amount,
            'currency': currency,
            'reason': reason,
            'reference': reference,
            'description': description,
            'metadata': metadata,
        }

        return self.request('/refunds', POST, params, payload=payload)

    def refund(self, **kwargs):
        return self.create_refund(**kwargs)

    def set_public_key(self, public_key):
        if not public_key:
            raise Exception('Public API Key is required.')

        if not valid_public_api_key(public_key):
            raise Exception('Public API Key is invalid.')

        self._public_key = public_key

    def get_session_url(self, session, options={}):
        if not session:
            raise Exception('Checkout Session is required.')

        checkoutURL = session.get('url', None)
        promotionCode = options.get('promotionCode', None)

        if not checkoutURL:
            raise Exception('Checkout URL is not available.')

        params = {
            'promotion-code': promotionCode,
        }
        qs = urlencode([(key, params[key])
                       for key in params if params[key] is not None])

        if qs:
            return '%s?%s' % (checkoutURL, qs)

        return checkoutURL
