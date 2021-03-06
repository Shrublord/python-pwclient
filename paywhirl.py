"""PayWhirl API Library
====================

This library has been made available to simplify
interfacing with PayWhirl's API
located at [api.paywhirl.com](https://api.paywhirl.com)

API keys can be obtained after making an account on
[PayWhirl's account page](https://app.paywhirl.com/api-keys)


Example Usage:
--------------
```
import paywhirl as pw

api_key = '<your_api_key_here>'
api_secret = '<your_secret_key_here>'
paywhirl = pw.PayWhirl(api_key, api_secret)

list_size_limit = {'limit': 2}
myobj = paywhirl.get_customers(list_size_limit)
print(myobj)
```

For information on type hints in Python 3.5 and higher see
https://www.python.org/dev/peps/pep-0484/
"""
from typing import Any
import requests


class PayWhirl:
    _api_key = ''
    _api_secret = ''
    _api_base = ''

    def __init__(
            self,
            api_key: str,
            api_secret: str,
            api_base: str = 'https://api.paywhirl.com') -> None:
        """Initialize the paywhirl object for making requests.

        Args:
            api_key: the api key for your account
            api_secret: your secret key
            api_base: the target URL for requests.
                Defaults to 'https://api.paywhirl.com'
        """

        self._api_key = api_key
        self._api_secret = api_secret
        self._api_base = api_base

    def get_customers(self, data: dict) -> list:
        """Get a list of customers associated with your account.

        Args:
            data:
                {
                    'limit': (int),
                    'order_key': (str),
                    'order_direction': (str),
                    'before_id': (int),
                    'after_id': (int),
                    'keyword': (str)
                }

                'limit' defaults to 100. 'order_key' defaults to 'id'.
                'order_direction' options are 'asc' and 'desc'
                for ascend and descend, respectively.
                'before_id' returns all customers less than the
                specified id, and 'after_id' returns
                all customers greater than the specified id.
                'keyword' will filter the results by the chosen string.

        Returns:
            A list of customer dicts filtered by your arguments,
            or an error message indicating what went wrong.
        """

        return self._get('/customers', data)

    def get_customer(self, customer_id: int) -> Any:
        """Get a single customer.

        Args:
            customer_id: the id number obtained from paywhirl's servers.
                (use the get_customers() method to find your IDs)

        Returns:
            A dictionary with complete customer data
            or an error message indicating what went wrong.
        """

        return self._get(str.format('/customer/{0}', customer_id))

    def create_customer(self, data: dict) -> Any:
        """Create a new customer with supplied data.

        Args:
            data:
                {
                    'first_name': (str),
                    'last_name': (str),
                    'email': (str),
                    'password': (str),
                    'currency': (str)
                }

            Only the required key: value pairs are listed above,
            more information about additional options can be found
            on the docs site located in the header of this file.

        Returns:
            A response containing either the created customer dictionary
            or an error message indicating what went wrong.
        """

        return self._post('/create/customer', data)

    def update_customer(self, data: dict) -> Any:
        """Update an existing customer (selected by id) with new info.

        Args:
            data:
                {
                    'id': (int),
                    ...
                }

            Any element existing in a current customer object should
            be a viable key-value pair to pass in for modification.

        Returns:
            A dict containing either the updated customer
            or an error message indicating what went wrong.
        """

        return self._post('/update/customer', data)

    def get_questions(self, return_list_size: int = 100) -> Any:
        """Retrieve a list of all questions associated with your
           account.

        Args:
            return_list_size: on a successful query, this will
                specify the number of elements in the returned list.
                Default value is 100.

        Returns:
            A list containing answer dicts,
            or an error message indicating what went wrong.
        """

        data = {'limit': return_list_size}
        return self._get('/questions', data)

    def update_answer(self, data: dict) -> Any:
        """Update an existing answer with new info.

        Args:
            data:
                {
                    'customer_id': (int),
                    'question_name': (str),
                    'answer': (str),
                    'address_id': (int)
                }

        Returns:
            A dict containing either the updated answer,
            a list of answers,
            or an error message indicating what went wrong.
        """

        return self._post('/update/answer', data)

    def get_answers(self, customer_id: int) -> Any:
        """Get a list of answers associated with a customer.

        Args:
            customer_id: the 'id' value from a customer dict.
                you can find this via the get_customers() method.

        Returns:
            A list containing answer dictionaries,
            or an error message indicating what went wrong.
        """

        data = {'customer_id': customer_id}
        return self._get('/answers', data)

    def get_plans(self, data: dict) -> Any:
        """Get a list of plans associated with your account.

        Args:
            data:
            {
                'limit': (int),
                'order_key': (str),
                'order_direction': (str),
                'before_id': (int),
                'after_id': (int)
            }

            'limit' defaults to 100. 'order_key' defaults to 'id'.
            'order_direction' can be 'asc' or 'desc'. Defaults to
            descending. 'before_id' and 'after_id' will return plans
            with 'id's less than or greater than the selected 'id'
            number, respectively.

        Returns:
            A list containing plan dictionaries,
            or an error message indicating what went wrong.
        """

        return self._get('/plans', data)

    def get_plan(self, plan_id: int) -> Any:
        """Get a single plan using the plan's ID

        Args:
            plan_id: the id number obtained from paywhirl's servers.
                (use the get_plans() method to find your IDs)
        Returns:
            A dictionary with data for a given plan
            or an error message indicating what went wrong.
        """

        return self._get(str.format('/plan/{0}', plan_id))

    def create_plan(self, data: dict) -> Any:
        """Create a plan to set rules for how a customer will be billed.

        Args:
            data: A dictionary containing plan rules.
            See the docs linked in the header for more info.

        Returns:
            A dictionary containing the created plan
            or an error message indicating what went wrong.
        """

        return self._post('/create/plan', data)

    def update_plan(self, data: dict) -> Any:
        """Update an existing plan selected by a plan's 'id' member.

        Args:
            data: A dictionary containing plan rules. the 'id' field
                is required.
            See the docs linked in the header for more info.

        Returns:
            A dictionary containing the updated plan
            or an error message indicating what went wrong.
        """

        return self._post('/update/plan', data)

    def get_subscriptions(self, customer_id: int) -> Any:
        """Retrieve a list of all subscriptions for a given customer.

        Args:
            customer_id: This can be found using the get_customers()
                method.

        Returns:
            A list containing plan dictionaries
            or an error message indicating what went wrong.
        """

        return self._get(str.format('/subscriptions/{0}', customer_id))

    def get_subscription(self, subscription_id: int) -> Any:
        """Retrieve a single subscription by passing in an ID.

        Args:
            subscription_id: These can be found by using the
                get_subscriptions() method.

        Returns:
            A single dict containing subscription information
            or an error message indicating what went wrong.
        """

        return self._get(str.format('/subscription/{0}', subscription_id))

    def subscribe_customer(self, data: dict) -> Any:
        """Subscribe a customer to a given plan.

        Args:
            data:
                {
                    'customer_id': (int),
                    'plan_id': (int),
                    'quantity': (int),
                    'promo_id': (int),
                    'trial_end': (int)
                }
            customer_id: The existing customer. (These can be found
                with the get_customers() method).

            plan_id: The plan to subscribe to. (These can be found
                with the get_plans() method).

            trial_end(optional): A UNIX timestamp indicating when a
                trial period should end. The docs linked in the header
                have extra information on how to generate these.
                Defaults to no trial.

            promo_id(optional): An existing promo code ID number.
                (These can be found with the get_promos() method).

            quantity(optional): Number of subscriptions to subscribe to.
                This defaults to 1.

        Returns:
            A dictionary containing information about the subscription
            or an error message indicating what went wrong.
        """

        return self._post('/subscribe/customer', data)

    def update_subscription(self, subscription_id: int, plan_id: int, quantity: int=None) -> Any:
        """Change a customer's subscription to a different plan.

        Args:
            subscription_id: The current subscription id.
            plan_id: The new plan for the subscription.

        Returns:
            A dictionary containing information about the subscription
            or an error message indicating what went wrong.
        """

        data = dict([('subscription_id', subscription_id),
                     ('plan_id', plan_id)])
        if quantity is not None:
            data['quantity'] = quantity
        return self._post('/update/subscription', data)

    def unsubscribe_customer(self, subscription_id: int) -> Any:
        """Cancel a customer's existing subscription.

        Args:
            subscription_id: You can find these by using the
                get_subscriptions() method for a given customer.

        Returns:
            A dictionary with {'status: 'success' or 'fail'}
            or an error message indicating what went wrong.
        """

        data = dict([('subscription_id', subscription_id)])
        return self._post('/unsubscribe/customer', data)

    def get_subscribers(self, data: dict) -> Any:
        """Get a list of all active subscribers.

        Args:
            data:
            {
                'limit': (int),
                'order': (str),
                'keyword': (str),
                'starting_after': (int),
                'starting_before': (int)
            }

            'limit' defaults to 20.
            'order' can be 'asc', 'desc', or 'rand'.
            'starting_after' will return subscribers with
            subscription IDs greater than 'starting_after'.
            'starting_before' will return subscribers with
            subscription IDs greater than 'starting_before'.
            'keyword' will filter the results by that word.

        Returns:
            A list containing subscriber dictionaries,
            or an error message indicating what went wrong.
        """

        return self._get('/subscribers', data)

    def get_invoice(self, invoice_id: int) -> Any:
        """Get the data for a single invoice when given an ID number.

        Args:
            invoice_id: Pass in a known invoice ID or use get_invoices()
                to get a collection of them from a single customer.

        Returns:
            A dictionary containing information about the selected
            invoice, or an error message indicating what went wrong.
        """

        return self._get(str.format('/invoice/{0}', invoice_id))

    def get_invoices(self, customer_id: int) -> Any:
        """Get a list of upcoming invoices for a specified customer.

        Args:
            customer_id: These can be found using the get_customers()
                method.

        Returns:
            A dictionary or list of dictionaries containing invoice
            data, or an error message indicating what went wrong.
        """

        return self._get(str.format('/invoices/{0}', customer_id))

    def get_gateways(self) -> Any:
        """Returns a list of your payment gateways.

        Returns:
            A dictionary or list of dictionaries containing gateway
            data, or an error message indicating what went wrong.
        """

        return self._get('/gateways')

    def get_gateway(self, gateway_id: int) -> Any:
        """Get a gateway specified by its ID number.

        Args:
            gateway_id: this can be found using get_gateways().

        Returns:
            A dictionary or list of dictionaries containing gateway
            data, or an error message indicating what went wrong.
        """

        return self._get(str.format('/gateway/{0}', gateway_id))

    def create_charge(self, data: dict) -> Any:
        """Attempt to a customer and return an invoice.

        Args:
            dict:
                See docs linked in the header for param options.

        Returns:
            A dictionary containing an invoice, or an error message
            indicating what went wrong.
        """

        return self._post('/create/charge', data)

    def get_charge(self, charge_id: int) -> Any:
        """Get a single charge using the charge ID.

        Args:
            charge_id: these can be found in each invoice.

        Returns:
            A dictionary containing charge information, or an error
            message indicating what went wrong.
        """

        return self._get(str.format('/charge/{0}', charge_id))

    def get_cards(self, customer_id: int) -> Any:
        """Get a list of cards associated with a customer.

        Args:
            customer_id: these can be obtained via get_customers()

        Returns:
            A list of dicts containing card information, or an error
            message indicating what went wrong.
        """

        return self._get(str.format('/cards/{0}', customer_id))

    def get_card(self, card_id: int) -> Any:
        """Get a single card by ID.

        Args:
            customer_id: these can be via get_customers()

        Returns:
            A list of dicts containing card information, or an error
            message indicating what went wrong.
        """

        return self._get(str.format('/card/{0}', card_id))

    def create_card(self, data: dict) -> Any:
        """Create a payment method and add it to an existing customer.

        Args:
            data: See docs linked in the header for param options.

        Returns:
            A dict containing card information, or an error
            message indicating what went wrong.
        """

        return self._post('/create/card', data)

    def delete_card(self, card_id: int) -> Any:
        """Delete an existing card by its ID number.

        Args:
            card_id: this can be found via the get_cards() method.

        Returns:
            A dictionary with {'status: 'success' or 'fail'}
            or an error message indicating what went wrong.
        """

        data = dict([('id', card_id)])
        return self._post('/delete/card', data)

    def get_promos(self) -> Any:
        """Return a list of all promos on file."""

        return self._get('/promo')

    def get_promo(self, promo_id: int) -> Any:
        """Get a single promo by ID.

        Args:
            promo_id: these can be obtained via get_customers()

        Returns:
            A dict containing promo information, or an error
            message indicating what went wrong.
        """

        return self._get(str.format('/promo/{0}', promo_id))

    def create_promo(self, data: dict) -> Any:
        """Create a promo code to use with subscriptions.

        Args:
            data: See docs linked in the header for param options.

        Returns:
            A dict containing promo information, or an error
            message indicating what went wrong.
        """

        return self._post('/create/promo', data)

    def delete_promo(self, promo_id: int) -> Any:
        """Delete an existing promo by its ID number.

        Args:
            promo_id: this can be found via the get_promos() method.

        Returns:
            A dictionary with {'status: 'success' or 'fail'}
            or an error message indicating what went wrong.
        """

        data = dict([('id', promo_id)])
        return self._post('/delete/promo', data)

    def get_email_template(self, template_id: int) -> Any:
        """Get the data for an email template when given an ID number.

        Args:
            template_id: Pass in a known template ID.
            You can find these on the paywhirl app template page.

        Returns:
            A dictionary containing information about the selected
            template, or an error message indicating what went wrong.
        """

        return self._get(str.format('/email/{0}', template_id))

    def send_email(self, data: dict) -> Any:
    	"""Send a system generated email based on one of your pre-
    		 defined templates on your paywhirl account page

    		Args:
    			see api.paywhirl.com, the list depends on what
    			email templates you have available

    		Returns:
    			either a string with "status" => "success" or an error message indicating
    			the need for another parameter
    	"""

    	return self._post('/send-email', data)

    def get_account(self) -> Any:
        """Get a dictionary containing your account information."""

        return self._get('/account')

    def get_stats(self) -> Any:
        """Get invoice and revenue statistics about your account."""

        return self._get('/stats')

    def get_shipping_rules(self) -> Any:
        """Get a list of shipping rules in dict format."""

        return self._get('/shipping/')

    def get_shipping_rule(self, shipping_rule_id: int) -> Any:
        """Get the data for a shipping rule when given an ID number.

        Args:
            shipping_rule_id: Pass in a known template ID.
            You can find these using the get_shipping_rules() method.

        Returns:
            A dictionary containing information about the selected
            rule, or an error message indicating what went wrong.
        """

        return self._get(str.format('/shipping/{0}', shipping_rule_id))

    def get_tax_rules(self) -> Any:
        """Get a list of all tax rules created by your account."""

        return self._get('/tax')

    def get_tax_rule(self, rule_id: int) -> Any:
        """Get the data for a tax rule when given an ID number.

        Args:
            rule_id: Pass in a known tax rule ID.
            You can find these using the get_tax_rules() method.

        Returns:
            A dictionary containing information about the selected
            rule, or an error message indicating what went wrong.
        """

        return self._get(str.format('/tax/{0}', rule_id))

    def get_multi_auth_token(self, data: dict) -> Any:
        """Get a MultiAuth token to use to automatically
                login a customer to a widget.

        Args:
            data: See docs linked in the header for param options.

        Returns:
            A dict containing a multiauth token, or an error
            message indicating what went wrong.
        """
        return self._post('/multiauth', data)

    def _post(self, endpoint: str, params: Any = None) -> Any:
        if params is None:
            params = {}
        url = (self._api_base + '/' + endpoint)
        headers = {'api_key': self._api_key, 'api_secret': self._api_secret}
        print(url, headers)
        resp = requests.post(url, headers=headers, params=params)
        if resp.status_code == requests.codes['ok']:
            ret = resp.json()
            resp.close()
            return ret

        return resp.status_code

    def _get(self, endpoint: str, params: Any = None) -> Any:
        if params is None:
            params = {}
        url = self._api_base + '/' + endpoint
        headers = {'api_key': self._api_key, 'api_secret': self._api_secret}
        print(url, headers)
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == requests.codes['ok']:
            ret = resp.json()
            resp.close()
            return ret

        return resp.status_code
