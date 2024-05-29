from typing import List

import dlt
from dlt.extract.source import DltResource
from rest_api import rest_api_source
from rest_api.typing import RESTAPIConfig


@dlt.source(name="stripe_source", max_table_nesting=2)
def stripe_source(
    username: str = dlt.secrets.value,
    password: str = dlt.secrets.value,
    base_url: str = dlt.config.value,
) -> List[DltResource]:

    # source configuration
    source_config: RESTAPIConfig = {
        "client": {
            "base_url": base_url,
            "auth": {
                "type": "http_basic",
                "username": username,
                "password": password,
            },
            "paginator": {
                "type": "cursor",
                "cursor_path": "id",
                "cursor_param": "starting_after",
            },
        },
        "resources": [
            # <p>Returns a list of accounts connected to your platform via <a href="/docs/connect">Connect</a>. If you’re not a platform, the list is empty.</p>
            {
                "name": "get_accounts",
                "table_name": "account",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/accounts",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an account.</p>
            {
                "name": "get_accounts_account",
                "table_name": "account",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/accounts/{account}",
                    "params": {
                        "account": {
                            "type": "resolve",
                            "resource": "get_accounts",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>List apple pay domains.</p>
            {
                "name": "get_apple_pay_domains",
                "table_name": "apple_pay_domain",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/apple_pay/domains",
                    "params": {
                        # the parameters below can optionally be configured
                        # "domain_name": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve an apple pay domain.</p>
            {
                "name": "get_apple_pay_domains_domain",
                "table_name": "apple_pay_domain",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/apple_pay/domains/{domain}",
                    "params": {
                        "domain": {
                            "type": "resolve",
                            "resource": "get_apple_pay_domains",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of application fees you’ve previously collected. The application fees are returned in sorted order, with the most recent fees appearing first.</p>
            {
                "name": "get_application_fees",
                "table_name": "application_fee",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/application_fees",
                    "params": {
                        # the parameters below can optionally be configured
                        # "charge": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an application fee that your account has collected. The same information is returned when refunding the application fee.</p>
            {
                "name": "get_application_fees_id",
                "table_name": "application_fee",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/application_fees/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_application_fees",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>List all secrets stored on the given scope.</p>
            {
                "name": "get_apps_secrets",
                "table_name": "apps_secret",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/apps/secrets",
                    "params": {
                        "scope": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Finds a secret in the secret store by name and scope.</p>
            {
                "name": "get_apps_secrets_find",
                "table_name": "apps_secret",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/apps/secrets/find",
                    "params": {
                        "name": "FILL_ME_IN",  # TODO: fill in required query parameter
                        "scope": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the current account balance, based on the authentication that was used to make the request.  For a sample request, see <a href="/docs/connect/account-balances#accounting-for-negative-balances">Accounting for negative balances</a>.</p>
            {
                "name": "get_balance",
                "table_name": "balance_amount",
                "endpoint": {
                    "data_selector": "available",
                    "path": "/v1/balance",
                    "params": {
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of transactions that have contributed to the Stripe account balance (e.g., charges, transfers, and so forth). The transactions are returned in sorted order, with the most recent transactions appearing first.</p>  <p>Note that this endpoint was previously called “Balance history” and used the path <code>/v1/balance/history</code>.</p>
            {
                "name": "get_balance_history",
                "table_name": "balance_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/balance/history",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "currency": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "payout": "OPTIONAL_CONFIG",
                        # "source": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "type": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the balance transaction with the given ID.</p>  <p>Note that this endpoint previously used the path <code>/v1/balance/history/:id</code>.</p>
            {
                "name": "get_balance_history_id",
                "table_name": "balance_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/balance/history/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_balance_history",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of transactions that have contributed to the Stripe account balance (e.g., charges, transfers, and so forth). The transactions are returned in sorted order, with the most recent transactions appearing first.</p>  <p>Note that this endpoint was previously called “Balance history” and used the path <code>/v1/balance/history</code>.</p>
            {
                "name": "get_balance_transactions",
                "table_name": "balance_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/balance_transactions",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "currency": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "payout": "OPTIONAL_CONFIG",
                        # "source": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "type": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the balance transaction with the given ID.</p>  <p>Note that this endpoint previously used the path <code>/v1/balance/history/:id</code>.</p>
            {
                "name": "get_balance_transactions_id",
                "table_name": "balance_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/balance_transactions/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_balance_transactions",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve a dispute for a specified charge.</p>
            {
                "name": "get_charges_charge_dispute",
                "table_name": "balance_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "balance_transactions",
                    "path": "/v1/charges/{charge}/dispute",
                    "params": {
                        "charge": {
                            "type": "resolve",
                            "resource": "get_charges",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>You can see a list of the bank accounts belonging to a Customer. Note that the 10 most recent sources are always available by default on the Customer. If you need more than those 10, you can use this API method and the <code>limit</code> and <code>starting_after</code> parameters to page through additional bank accounts.</p>
            {
                "name": "get_customers_customer_bank_accounts",
                "table_name": "bank_account",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/customers/{customer}/bank_accounts",
                    "params": {
                        "customer": {
                            "type": "resolve",
                            "resource": "get_customers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>By default, you can see the 10 most recent sources stored on a Customer directly on the object, but you can also retrieve details about a specific bank account stored on the Stripe account.</p>
            {
                "name": "get_customers_customer_bank_accounts_id",
                "table_name": "bank_account",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/customers/{customer}/bank_accounts/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_customers_customer_bank_accounts",
                            "field": "id",
                        },
                        "customer": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve a list of billing meters.</p>
            {
                "name": "get_billing_meters",
                "table_name": "billing_meter",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/billing/meters",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a billing meter given an ID</p>
            {
                "name": "get_billing_meters_id",
                "table_name": "billing_meter",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/billing/meters/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_billing_meters",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve a list of billing meter event summaries.</p>
            {
                "name": "get_billing_meters_id_event_summaries",
                "table_name": "billing_meter_event_summary",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/billing/meters/{id}/event_summaries",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_billing_meters",
                            "field": "id",
                        },
                        "customer": "FILL_ME_IN",  # TODO: fill in required query parameter
                        "end_time": "FILL_ME_IN",  # TODO: fill in required query parameter
                        "start_time": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "value_grouping_window": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of configurations that describe the functionality of the customer portal.</p>
            {
                "name": "get_billing_portal_configurations",
                "table_name": "billing_portal_configuration",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/billing_portal/configurations",
                    "params": {
                        # the parameters below can optionally be configured
                        # "active": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "is_default": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a configuration that describes the functionality of the customer portal.</p>
            {
                "name": "get_billing_portal_configurations_configuration",
                "table_name": "billing_portal_configuration",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/billing_portal/configurations/{configuration}",
                    "params": {
                        "configuration": {
                            "type": "resolve",
                            "resource": "get_billing_portal_configurations",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of capabilities associated with the account. The capabilities are returned sorted by creation date, with the most recent capability appearing first.</p>
            {
                "name": "get_accounts_account_capabilities",
                "table_name": "capability",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/accounts/{account}/capabilities",
                    "params": {
                        "account": {
                            "type": "resolve",
                            "resource": "get_accounts",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves information about the specified Account Capability.</p>
            {
                "name": "get_accounts_account_capabilities_capability",
                "table_name": "capability",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/accounts/{account}/capabilities/{capability}",
                    "params": {
                        "capability": {
                            "type": "resolve",
                            "resource": "get_accounts_account_capabilities",
                            "field": "id",
                        },
                        "account": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>You can see a list of the cards belonging to a customer. Note that the 10 most recent sources are always available on the <code>Customer</code> object. If you need more than those 10, you can use this API method and the <code>limit</code> and <code>starting_after</code> parameters to page through additional cards.</p>
            {
                "name": "get_customers_customer_cards",
                "table_name": "card",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/customers/{customer}/cards",
                    "params": {
                        "customer": {
                            "type": "resolve",
                            "resource": "get_customers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>You can always see the 10 most recent cards directly on a customer; this method lets you retrieve details about a specific card stored on the customer.</p>
            {
                "name": "get_customers_customer_cards_id",
                "table_name": "card",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/customers/{customer}/cards/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_customers_customer_cards",
                            "field": "id",
                        },
                        "customer": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a customer’s cash balance.</p>
            {
                "name": "get_customers_customer_cash_balance",
                "table_name": "cash_balance",
                "primary_key": "customer",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/customers/{customer}/cash_balance",
                    "params": {
                        "customer": {
                            "type": "resolve",
                            "resource": "get_customers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of charges you’ve previously created. The charges are returned in sorted order, with the most recent charges appearing first.</p>
            {
                "name": "get_charges",
                "table_name": "charge",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/charges",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "payment_intent": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "transfer_group": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Search for charges you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
            {
                "name": "get_charges_search",
                "table_name": "charge",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/charges/search",
                    "params": {
                        "query": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                    },
                    "paginator": {
                        "type": "page_number",
                        "page_param": "page",
                        "total_path": "data.[*].invoice.total",
                    },
                },
            },
            # <p>Retrieves the details of a charge that has previously been created. Supply the unique charge ID that was returned from your previous request, and Stripe will return the corresponding charge information. The same information is returned when creating or refunding the charge.</p>
            {
                "name": "get_charges_charge",
                "table_name": "charge",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/charges/{charge}",
                    "params": {
                        "charge": {
                            "type": "resolve",
                            "resource": "get_charges",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of Checkout Sessions.</p>
            {
                "name": "get_checkout_sessions",
                "table_name": "checkout_session",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/checkout/sessions",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "customer_details": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "payment_intent": "OPTIONAL_CONFIG",
                        # "payment_link": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                        # "subscription": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a Session object.</p>
            {
                "name": "get_checkout_sessions_session",
                "table_name": "checkout_session",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/checkout/sessions/{session}",
                    "params": {
                        "session": {
                            "type": "resolve",
                            "resource": "get_checkout_sessions",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Lists all Climate order objects. The orders are returned sorted by creation date, with the most recently created orders appearing first.</p>
            {
                "name": "get_climate_orders",
                "table_name": "climate_order",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/climate/orders",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of a Climate order object with the given ID.</p>
            {
                "name": "get_climate_orders_order",
                "table_name": "climate_order",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/climate/orders/{order}",
                    "params": {
                        "order": {
                            "type": "resolve",
                            "resource": "get_climate_orders",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Lists all available Climate product objects.</p>
            {
                "name": "get_climate_products",
                "table_name": "climate_product",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/climate/products",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of a Climate product with the given ID.</p>
            {
                "name": "get_climate_products_product",
                "table_name": "climate_product",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/climate/products/{product}",
                    "params": {
                        "product": {
                            "type": "resolve",
                            "resource": "get_climate_products",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Lists all available Climate supplier objects.</p>
            {
                "name": "get_climate_suppliers",
                "table_name": "climate_supplier",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/climate/suppliers",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a Climate supplier object.</p>
            {
                "name": "get_climate_suppliers_supplier",
                "table_name": "climate_supplier",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/climate/suppliers/{supplier}",
                    "params": {
                        "supplier": {
                            "type": "resolve",
                            "resource": "get_climate_suppliers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a <code>Configuration</code> object.</p>
            {
                "name": "get_terminal_configurations_configuration",
                "table_name": "configuration",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/terminal/configurations/{configuration}",
                    "params": {
                        "configuration": {
                            "type": "resolve",
                            "resource": "get_terminal_configurations",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an existing ConfirmationToken object</p>
            {
                "name": "get_confirmation_tokens_confirmation_token",
                "table_name": "confirmation_token",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/confirmation_tokens/{confirmation_token}",
                    "params": {
                        "confirmation_token": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Lists all Country Spec objects available in the API.</p>
            {
                "name": "get_country_specs",
                "table_name": "country_spec",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/country_specs",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a Country Spec for a given Country code.</p>
            {
                "name": "get_country_specs_country",
                "table_name": "country_spec",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/country_specs/{country}",
                    "params": {
                        "country": {
                            "type": "resolve",
                            "resource": "get_country_specs",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your coupons.</p>
            {
                "name": "get_coupons",
                "table_name": "coupon",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/coupons",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the coupon with the given ID.</p>
            {
                "name": "get_coupons_coupon",
                "table_name": "coupon",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/coupons/{coupon}",
                    "params": {
                        "coupon": {
                            "type": "resolve",
                            "resource": "get_coupons",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of credit notes.</p>
            {
                "name": "get_credit_notes",
                "table_name": "credit_note",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/credit_notes",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "invoice": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the credit note object with the given identifier.</p>
            {
                "name": "get_credit_notes_id",
                "table_name": "credit_note",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/credit_notes/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_credit_notes",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>When retrieving a credit note preview, you’ll get a <strong>lines</strong> property containing the first handful of those items. This URL you can retrieve the full (paginated) list of line items.</p>
            {
                "name": "get_credit_notes_preview_lines",
                "table_name": "credit_note_line_item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/credit_notes/preview/lines",
                    "params": {
                        "invoice": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "amount": "OPTIONAL_CONFIG",
                        # "credit_amount": "OPTIONAL_CONFIG",
                        # "effective_at": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "lines": "OPTIONAL_CONFIG",
                        # "memo": "OPTIONAL_CONFIG",
                        # "metadata": "OPTIONAL_CONFIG",
                        # "out_of_band_amount": "OPTIONAL_CONFIG",
                        # "reason": "OPTIONAL_CONFIG",
                        # "refund": "OPTIONAL_CONFIG",
                        # "refund_amount": "OPTIONAL_CONFIG",
                        # "shipping_cost": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>When retrieving a credit note, you’ll get a <strong>lines</strong> property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.</p>
            {
                "name": "get_credit_notes_credit_note_lines",
                "table_name": "credit_note_line_item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/credit_notes/{credit_note}/lines",
                    "params": {
                        "credit_note": {
                            "type": "resolve",
                            "resource": "get_credit_notes",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your customers. The customers are returned sorted by creation date, with the most recent customers appearing first.</p>
            {
                "name": "get_customers",
                "table_name": "customer",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/customers",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "email": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "test_clock": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Search for customers you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
            {
                "name": "get_customers_search",
                "table_name": "customer",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/customers/search",
                    "params": {
                        "query": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a Customer object.</p>
            {
                "name": "get_customers_customer",
                "table_name": "customer",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/customers/{customer}",
                    "params": {
                        "customer": {
                            "type": "resolve",
                            "resource": "get_customers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of transactions that updated the customer’s <a href="/docs/billing/customer/balance">balances</a>.</p>
            {
                "name": "get_customers_customer_balance_transactions",
                "table_name": "customer_balance_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/customers/{customer}/balance_transactions",
                    "params": {
                        "customer": {
                            "type": "resolve",
                            "resource": "get_customers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a specific customer balance transaction that updated the customer’s <a href="/docs/billing/customer/balance">balances</a>.</p>
            {
                "name": "get_customers_customer_balance_transactions_transaction",
                "table_name": "customer_balance_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/customers/{customer}/balance_transactions/{transaction}",
                    "params": {
                        "transaction": {
                            "type": "resolve",
                            "resource": "get_customers_customer_balance_transactions",
                            "field": "id",
                        },
                        "customer": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of transactions that modified the customer’s <a href="/docs/payments/customer-balance">cash balance</a>.</p>
            {
                "name": "get_customers_customer_cash_balance_transactions",
                "table_name": "customer_cash_balance_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/customers/{customer}/cash_balance_transactions",
                    "params": {
                        "customer": {
                            "type": "resolve",
                            "resource": "get_customers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a specific cash balance transaction, which updated the customer’s <a href="/docs/payments/customer-balance">cash balance</a>.</p>
            {
                "name": "get_customers_customer_cash_balance_transactions_transaction",
                "table_name": "customer_cash_balance_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/customers/{customer}/cash_balance_transactions/{transaction}",
                    "params": {
                        "transaction": {
                            "type": "resolve",
                            "resource": "get_customers_customer_cash_balance_transactions",
                            "field": "id",
                        },
                        "customer": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            {
                "name": "get_customers_customer_discount",
                "table_name": "discount",
                "endpoint": {
                    "data_selector": "customer.preferred_locales",
                    "path": "/v1/customers/{customer}/discount",
                    "params": {
                        "customer": {
                            "type": "resolve",
                            "resource": "get_customers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            {
                "name": "get_customers_customer_subscriptions_subscription_exposed_id_discount",
                "table_name": "discount",
                "endpoint": {
                    "data_selector": "customer.preferred_locales",
                    "path": "/v1/customers/{customer}/subscriptions/{subscription_exposed_id}/discount",
                    "params": {
                        "subscription_exposed_id": {
                            "type": "resolve",
                            "resource": "get_customers_customer_subscriptions",
                            "field": "id",
                        },
                        "customer": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Get a preview of a credit note without creating it.</p>
            {
                "name": "get_credit_notes_preview",
                "table_name": "discounts_resource_discount_amount",
                "endpoint": {
                    "data_selector": "discount_amounts",
                    "path": "/v1/credit_notes/preview",
                    "params": {
                        "invoice": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "amount": "OPTIONAL_CONFIG",
                        # "credit_amount": "OPTIONAL_CONFIG",
                        # "effective_at": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "lines": "OPTIONAL_CONFIG",
                        # "memo": "OPTIONAL_CONFIG",
                        # "metadata": "OPTIONAL_CONFIG",
                        # "out_of_band_amount": "OPTIONAL_CONFIG",
                        # "reason": "OPTIONAL_CONFIG",
                        # "refund": "OPTIONAL_CONFIG",
                        # "refund_amount": "OPTIONAL_CONFIG",
                        # "shipping_cost": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your disputes.</p>
            {
                "name": "get_disputes",
                "table_name": "dispute",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/disputes",
                    "params": {
                        # the parameters below can optionally be configured
                        # "charge": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "payment_intent": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the dispute with the given ID.</p>
            {
                "name": "get_disputes_dispute",
                "table_name": "dispute",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/disputes/{dispute}",
                    "params": {
                        "dispute": {
                            "type": "resolve",
                            "resource": "get_disputes",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve a list of active entitlements for a customer</p>
            {
                "name": "get_entitlements_active_entitlements",
                "table_name": "entitlements_active_entitlement",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/entitlements/active_entitlements",
                    "params": {
                        "customer": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve an active entitlement</p>
            {
                "name": "get_entitlements_active_entitlements_id",
                "table_name": "entitlements_active_entitlement",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/entitlements/active_entitlements/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_entitlements_active_entitlements",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve a list of features</p>
            {
                "name": "get_entitlements_features",
                "table_name": "entitlements_feature",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/entitlements/features",
                    "params": {
                        # the parameters below can optionally be configured
                        # "archived": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "lookup_key": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a feature</p>
            {
                "name": "get_entitlements_features_id",
                "table_name": "entitlements_feature",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/entitlements/features/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_entitlements_features",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>List events, going back up to 30 days. Each event data is rendered according to Stripe API version at its creation time, specified in <a href="https://docs.stripe.com/api/events/object">event object</a> <code>api_version</code> attribute (not according to your current Stripe API version or <code>Stripe-Version</code> header).</p>
            {
                "name": "get_events",
                "table_name": "event",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/events",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "delivery_success": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "type": "OPTIONAL_CONFIG",
                        # "types": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an event. Supply the unique identifier of the event, which you might have received in a webhook.</p>
            {
                "name": "get_events_id",
                "table_name": "event",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/events/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_events",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of objects that contain the rates at which foreign currencies are converted to one another. Only shows the currencies for which Stripe supports.</p>
            {
                "name": "get_exchange_rates",
                "table_name": "exchange_rate",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/exchange_rates",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the exchange rates from the given currency to every supported currency.</p>
            {
                "name": "get_exchange_rates_rate_id",
                "table_name": "exchange_rate",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/exchange_rates/{rate_id}",
                    "params": {
                        "rate_id": {
                            "type": "resolve",
                            "resource": "get_exchange_rates",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve a specified external account for a given account.</p>
            {
                "name": "get_accounts_account_bank_accounts_id",
                "table_name": "external_account",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/accounts/{account}/bank_accounts/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_accounts",
                            "field": "id",
                        },
                        "account": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve a specified external account for a given account.</p>
            {
                "name": "get_accounts_account_external_accounts_id",
                "table_name": "external_account",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/accounts/{account}/external_accounts/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_accounts_account_external_accounts",
                            "field": "id",
                        },
                        "account": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>By default, you can see the 10 most recent refunds stored directly on the application fee object, but you can also retrieve details about a specific refund stored on the application fee.</p>
            {
                "name": "get_application_fees_fee_refunds_id",
                "table_name": "fee_refund",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/application_fees/{fee}/refunds/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_application_fees",
                            "field": "id",
                        },
                        "fee": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>You can see a list of the refunds belonging to a specific application fee. Note that the 10 most recent refunds are always available by default on the application fee object. If you need more than those 10, you can use this API method and the <code>limit</code> and <code>starting_after</code> parameters to page through additional refunds.</p>
            {
                "name": "get_application_fees_id_refunds",
                "table_name": "fee_refund",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/application_fees/{id}/refunds",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_application_fees",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of the files that your account has access to. Stripe sorts and returns the files by their creation dates, placing the most recently created files at the top.</p>
            {
                "name": "get_files",
                "table_name": "file",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/files",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "purpose": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing file object. After you supply a unique file ID, Stripe returns the corresponding file object. Learn how to <a href="/docs/file-upload#download-file-contents">access file contents</a>.</p>
            {
                "name": "get_files_file",
                "table_name": "file",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/files/{file}",
                    "params": {
                        "file": {
                            "type": "resolve",
                            "resource": "get_files",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of file links.</p>
            {
                "name": "get_file_links",
                "table_name": "file_link",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/file_links",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "expired": "OPTIONAL_CONFIG",
                        # "file": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the file link with the given ID.</p>
            {
                "name": "get_file_links_link",
                "table_name": "file_link",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/file_links/{link}",
                    "params": {
                        "link": {
                            "type": "resolve",
                            "resource": "get_file_links",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of Financial Connections <code>Account</code> objects.</p>
            {
                "name": "get_financial_connections_accounts",
                "table_name": "financial_connections_account",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/financial_connections/accounts",
                    "params": {
                        # the parameters below can optionally be configured
                        # "account_holder": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "session": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an Financial Connections <code>Account</code>.</p>
            {
                "name": "get_financial_connections_accounts_account",
                "table_name": "financial_connections_account",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/financial_connections/accounts/{account}",
                    "params": {
                        "account": {
                            "type": "resolve",
                            "resource": "get_financial_connections_accounts",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of Financial Connections <code>Account</code> objects.</p>
            {
                "name": "get_linked_accounts",
                "table_name": "financial_connections_account",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/linked_accounts",
                    "params": {
                        # the parameters below can optionally be configured
                        # "account_holder": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "session": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an Financial Connections <code>Account</code>.</p>
            {
                "name": "get_linked_accounts_account",
                "table_name": "financial_connections_account",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/linked_accounts/{account}",
                    "params": {
                        "account": {
                            "type": "resolve",
                            "resource": "get_linked_accounts",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Lists all owners for a given <code>Account</code></p>
            {
                "name": "get_financial_connections_accounts_account_owners",
                "table_name": "financial_connections_account_owner",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/financial_connections/accounts/{account}/owners",
                    "params": {
                        "account": {
                            "type": "resolve",
                            "resource": "get_financial_connections_accounts",
                            "field": "id",
                        },
                        "ownership": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Lists all owners for a given <code>Account</code></p>
            {
                "name": "get_linked_accounts_account_owners",
                "table_name": "financial_connections_account_owner",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/linked_accounts/{account}/owners",
                    "params": {
                        "account": {
                            "type": "resolve",
                            "resource": "get_linked_accounts",
                            "field": "id",
                        },
                        "ownership": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of a Financial Connections <code>Session</code></p>
            {
                "name": "get_financial_connections_sessions_session",
                "table_name": "financial_connections_session",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/financial_connections/sessions/{session}",
                    "params": {
                        "session": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of a Financial Connections <code>Session</code></p>
            {
                "name": "get_link_account_sessions_session",
                "table_name": "financial_connections_session",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/link_account_sessions/{session}",
                    "params": {
                        "session": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of Financial Connections <code>Transaction</code> objects.</p>
            {
                "name": "get_financial_connections_transactions",
                "table_name": "financial_connections_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/financial_connections/transactions",
                    "params": {
                        "account": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "transacted_at": "OPTIONAL_CONFIG",
                        # "transaction_refresh": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of a Financial Connections <code>Transaction</code></p>
            {
                "name": "get_financial_connections_transactions_transaction",
                "table_name": "financial_connections_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/financial_connections/transactions/{transaction}",
                    "params": {
                        "transaction": {
                            "type": "resolve",
                            "resource": "get_financial_connections_transactions",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Lists all ForwardingRequest objects.</p>
            {
                "name": "get_forwarding_requests",
                "table_name": "forwarding_request",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/forwarding/requests",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a ForwardingRequest object.</p>
            {
                "name": "get_forwarding_requests_id",
                "table_name": "forwarding_request",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/forwarding/requests/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_forwarding_requests",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>List all verification reports.</p>
            {
                "name": "get_identity_verification_reports",
                "table_name": "identity_verification_report",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/identity/verification_reports",
                    "params": {
                        # the parameters below can optionally be configured
                        # "client_reference_id": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "type": "OPTIONAL_CONFIG",
                        # "verification_session": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an existing VerificationReport</p>
            {
                "name": "get_identity_verification_reports_report",
                "table_name": "identity_verification_report",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/identity/verification_reports/{report}",
                    "params": {
                        "report": {
                            "type": "resolve",
                            "resource": "get_identity_verification_reports",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of VerificationSessions</p>
            {
                "name": "get_identity_verification_sessions",
                "table_name": "identity_verification_session",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/identity/verification_sessions",
                    "params": {
                        # the parameters below can optionally be configured
                        # "client_reference_id": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of a VerificationSession that was previously created.</p>  <p>When the session status is <code>requires_input</code>, you can use this method to retrieve a valid <code>client_secret</code> or <code>url</code> to allow re-submission.</p>
            {
                "name": "get_identity_verification_sessions_session",
                "table_name": "identity_verification_session",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/identity/verification_sessions/{session}",
                    "params": {
                        "session": {
                            "type": "resolve",
                            "resource": "get_identity_verification_sessions",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>You can list all invoices, or list the invoices for a specific customer. The invoices are returned sorted by creation date, with the most recently created invoices appearing first.</p>
            {
                "name": "get_invoices",
                "table_name": "invoice",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/invoices",
                    "params": {
                        # the parameters below can optionally be configured
                        # "collection_method": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "due_date": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                        # "subscription": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Search for invoices you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
            {
                "name": "get_invoices_search",
                "table_name": "invoice",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/invoices/search",
                    "params": {
                        "query": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                    },
                    "paginator": {
                        "type": "page_number",
                        "page_param": "page",
                        "total_path": "data.[*].total",
                    },
                },
            },
            # <p>Retrieves the invoice with the given ID.</p>
            {
                "name": "get_invoices_invoice",
                "table_name": "invoice",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/invoices/{invoice}",
                    "params": {
                        "invoice": {
                            "type": "resolve",
                            "resource": "get_invoices",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your invoice items. Invoice items are returned sorted by creation date, with the most recently created invoice items appearing first.</p>
            {
                "name": "get_invoiceitems",
                "table_name": "invoiceitem",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/invoiceitems",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "invoice": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "pending": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the invoice item with the given ID.</p>
            {
                "name": "get_invoiceitems_invoiceitem",
                "table_name": "invoiceitem",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/invoiceitems/{invoiceitem}",
                    "params": {
                        "invoiceitem": {
                            "type": "resolve",
                            "resource": "get_invoiceitems",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of Issuing <code>Authorization</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
            {
                "name": "get_issuing_authorizations",
                "table_name": "issuing_authorization",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/issuing/authorizations",
                    "params": {
                        # the parameters below can optionally be configured
                        # "card": "OPTIONAL_CONFIG",
                        # "cardholder": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an Issuing <code>Authorization</code> object.</p>
            {
                "name": "get_issuing_authorizations_authorization",
                "table_name": "issuing_authorization",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/issuing/authorizations/{authorization}",
                    "params": {
                        "authorization": {
                            "type": "resolve",
                            "resource": "get_issuing_authorizations",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of Issuing <code>Card</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
            {
                "name": "get_issuing_cards",
                "table_name": "issuing_card",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/issuing/cards",
                    "params": {
                        # the parameters below can optionally be configured
                        # "cardholder": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "exp_month": "OPTIONAL_CONFIG",
                        # "exp_year": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "last4": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "personalization_design": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                        # "type": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an Issuing <code>Card</code> object.</p>
            {
                "name": "get_issuing_cards_card",
                "table_name": "issuing_card",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/issuing/cards/{card}",
                    "params": {
                        "card": {
                            "type": "resolve",
                            "resource": "get_issuing_cards",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of Issuing <code>Cardholder</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
            {
                "name": "get_issuing_cardholders",
                "table_name": "issuing_cardholder",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/issuing/cardholders",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "email": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "phone_number": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                        # "type": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an Issuing <code>Cardholder</code> object.</p>
            {
                "name": "get_issuing_cardholders_cardholder",
                "table_name": "issuing_cardholder",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/issuing/cardholders/{cardholder}",
                    "params": {
                        "cardholder": {
                            "type": "resolve",
                            "resource": "get_issuing_cardholders",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of Issuing <code>Dispute</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
            {
                "name": "get_issuing_disputes",
                "table_name": "issuing_dispute",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/issuing/disputes",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                        # "transaction": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an Issuing <code>Dispute</code> object.</p>
            {
                "name": "get_issuing_disputes_dispute",
                "table_name": "issuing_dispute",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/issuing/disputes/{dispute}",
                    "params": {
                        "dispute": {
                            "type": "resolve",
                            "resource": "get_issuing_disputes",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of personalization design objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
            {
                "name": "get_issuing_personalization_designs",
                "table_name": "issuing_personalization_design",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/issuing/personalization_designs",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "lookup_keys": "OPTIONAL_CONFIG",
                        # "preferences": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a personalization design object.</p>
            {
                "name": "get_issuing_personalization_designs_personalization_design",
                "table_name": "issuing_personalization_design",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/issuing/personalization_designs/{personalization_design}",
                    "params": {
                        "personalization_design": {
                            "type": "resolve",
                            "resource": "get_issuing_personalization_designs",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of physical bundle objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
            {
                "name": "get_issuing_physical_bundles",
                "table_name": "issuing_physical_bundle",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/issuing/physical_bundles",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                        # "type": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a physical bundle object.</p>
            {
                "name": "get_issuing_physical_bundles_physical_bundle",
                "table_name": "issuing_physical_bundle",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/issuing/physical_bundles/{physical_bundle}",
                    "params": {
                        "physical_bundle": {
                            "type": "resolve",
                            "resource": "get_issuing_physical_bundles",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an Issuing <code>Settlement</code> object.</p>
            {
                "name": "get_issuing_settlements_settlement",
                "table_name": "issuing_settlement",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/issuing/settlements/{settlement}",
                    "params": {
                        "settlement": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Lists all Issuing <code>Token</code> objects for a given card.</p>
            {
                "name": "get_issuing_tokens",
                "table_name": "issuing_token",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/issuing/tokens",
                    "params": {
                        "card": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an Issuing <code>Token</code> object.</p>
            {
                "name": "get_issuing_tokens_token",
                "table_name": "issuing_token",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/issuing/tokens/{token}",
                    "params": {
                        "token": {
                            "type": "resolve",
                            "resource": "get_issuing_tokens",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of Issuing <code>Transaction</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
            {
                "name": "get_issuing_transactions",
                "table_name": "issuing_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/issuing/transactions",
                    "params": {
                        # the parameters below can optionally be configured
                        # "card": "OPTIONAL_CONFIG",
                        # "cardholder": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "type": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an Issuing <code>Transaction</code> object.</p>
            {
                "name": "get_issuing_transactions_transaction",
                "table_name": "issuing_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/issuing/transactions/{transaction}",
                    "params": {
                        "transaction": {
                            "type": "resolve",
                            "resource": "get_issuing_transactions",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>When retrieving a Checkout Session, there is an includable <strong>line_items</strong> property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.</p>
            {
                "name": "get_checkout_sessions_session_line_items",
                "table_name": "item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/checkout/sessions/{session}/line_items",
                    "params": {
                        "session": {
                            "type": "resolve",
                            "resource": "get_checkout_sessions",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>When retrieving a payment link, there is an includable <strong>line_items</strong> property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.</p>
            {
                "name": "get_payment_links_payment_link_line_items",
                "table_name": "item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/payment_links/{payment_link}/line_items",
                    "params": {
                        "payment_link": {
                            "type": "resolve",
                            "resource": "get_payment_links",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>When retrieving a quote, there is an includable <a href="https://stripe.com/docs/api/quotes/object#quote_object-computed-upfront-line_items"><strong>computed.upfront.line_items</strong></a> property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of upfront line items.</p>
            {
                "name": "get_quotes_quote_computed_upfront_line_items",
                "table_name": "item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/quotes/{quote}/computed_upfront_line_items",
                    "params": {
                        "quote": {
                            "type": "resolve",
                            "resource": "get_quotes",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>When retrieving a quote, there is an includable <strong>line_items</strong> property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.</p>
            {
                "name": "get_quotes_quote_line_items",
                "table_name": "item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/quotes/{quote}/line_items",
                    "params": {
                        "quote": {
                            "type": "resolve",
                            "resource": "get_quotes",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>When retrieving an upcoming invoice, you’ll get a <strong>lines</strong> property containing the total count of line items and the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.</p>
            {
                "name": "get_invoices_upcoming_lines",
                "table_name": "line_item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/invoices/upcoming/lines",
                    "params": {
                        # the parameters below can optionally be configured
                        # "automatic_tax": "OPTIONAL_CONFIG",
                        # "coupon": "OPTIONAL_CONFIG",
                        # "currency": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "customer_details": "OPTIONAL_CONFIG",
                        # "discounts": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "invoice_items": "OPTIONAL_CONFIG",
                        # "issuer": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "on_behalf_of": "OPTIONAL_CONFIG",
                        # "preview_mode": "OPTIONAL_CONFIG",
                        # "schedule": "OPTIONAL_CONFIG",
                        # "schedule_details": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "subscription": "OPTIONAL_CONFIG",
                        # "subscription_billing_cycle_anchor": "OPTIONAL_CONFIG",
                        # "subscription_cancel_at": "OPTIONAL_CONFIG",
                        # "subscription_cancel_at_period_end": "OPTIONAL_CONFIG",
                        # "subscription_cancel_now": "OPTIONAL_CONFIG",
                        # "subscription_default_tax_rates": "OPTIONAL_CONFIG",
                        # "subscription_details": "OPTIONAL_CONFIG",
                        # "subscription_items": "OPTIONAL_CONFIG",
                        # "subscription_proration_behavior": "OPTIONAL_CONFIG",
                        # "subscription_proration_date": "OPTIONAL_CONFIG",
                        # "subscription_resume_at": "OPTIONAL_CONFIG",
                        # "subscription_start_date": "OPTIONAL_CONFIG",
                        # "subscription_trial_end": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>When retrieving an invoice, you’ll get a <strong>lines</strong> property containing the total count of line items and the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.</p>
            {
                "name": "get_invoices_invoice_lines",
                "table_name": "line_item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/invoices/{invoice}/lines",
                    "params": {
                        "invoice": {
                            "type": "resolve",
                            "resource": "get_invoices",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a <code>Location</code> object.</p>
            {
                "name": "get_terminal_locations_location",
                "table_name": "location",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/terminal/locations/{location}",
                    "params": {
                        "location": {
                            "type": "resolve",
                            "resource": "get_terminal_locations",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a Mandate object.</p>
            {
                "name": "get_mandates_mandate",
                "table_name": "mandate",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/mandates/{mandate}",
                    "params": {
                        "mandate": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of PaymentIntents.</p>
            {
                "name": "get_payment_intents",
                "table_name": "payment_intent",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/payment_intents",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Search for PaymentIntents you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
            {
                "name": "get_payment_intents_search",
                "table_name": "payment_intent",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/payment_intents/search",
                    "params": {
                        "query": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                    },
                    "paginator": {
                        "type": "page_number",
                        "page_param": "page",
                        "total_path": "data.[*].invoice.total",
                    },
                },
            },
            # <p>Retrieves the details of a PaymentIntent that has previously been created. </p>  <p>You can retrieve a PaymentIntent client-side using a publishable key when the <code>client_secret</code> is in the query string. </p>  <p>If you retrieve a PaymentIntent with a publishable key, it only returns a subset of properties. Refer to the <a href="#payment_intent_object">payment intent</a> object reference for more details.</p>
            {
                "name": "get_payment_intents_intent",
                "table_name": "payment_intent",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/payment_intents/{intent}",
                    "params": {
                        "intent": {
                            "type": "resolve",
                            "resource": "get_payment_intents",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "client_secret": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your payment links.</p>
            {
                "name": "get_payment_links",
                "table_name": "payment_link",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/payment_links",
                    "params": {
                        # the parameters below can optionally be configured
                        # "active": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve a payment link.</p>
            {
                "name": "get_payment_links_payment_link",
                "table_name": "payment_link",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/payment_links/{payment_link}",
                    "params": {
                        "payment_link": {
                            "type": "resolve",
                            "resource": "get_payment_links",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of PaymentMethods for a given Customer</p>
            {
                "name": "get_customers_customer_payment_methods",
                "table_name": "payment_method",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/customers/{customer}/payment_methods",
                    "params": {
                        "customer": {
                            "type": "resolve",
                            "resource": "get_customers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "allow_redisplay": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "type": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a PaymentMethod object for a given Customer.</p>
            {
                "name": "get_customers_customer_payment_methods_payment_method",
                "table_name": "payment_method",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/customers/{customer}/payment_methods/{payment_method}",
                    "params": {
                        "payment_method": {
                            "type": "resolve",
                            "resource": "get_customers_customer_payment_methods",
                            "field": "id",
                        },
                        "customer": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of PaymentMethods for Treasury flows. If you want to list the PaymentMethods attached to a Customer for payments, you should use the <a href="/docs/api/payment_methods/customer_list">List a Customer’s PaymentMethods</a> API instead.</p>
            {
                "name": "get_payment_methods",
                "table_name": "payment_method",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/payment_methods",
                    "params": {
                        # the parameters below can optionally be configured
                        # "customer": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "type": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a PaymentMethod object attached to the StripeAccount. To retrieve a payment method attached to a Customer, you should use <a href="/docs/api/payment_methods/customer">Retrieve a Customer’s PaymentMethods</a></p>
            {
                "name": "get_payment_methods_payment_method",
                "table_name": "payment_method",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/payment_methods/{payment_method}",
                    "params": {
                        "payment_method": {
                            "type": "resolve",
                            "resource": "get_payment_methods",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>List payment method configurations</p>
            {
                "name": "get_payment_method_configurations",
                "table_name": "payment_method_configuration",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/payment_method_configurations",
                    "params": {
                        # the parameters below can optionally be configured
                        # "application": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve payment method configuration</p>
            {
                "name": "get_payment_method_configurations_configuration",
                "table_name": "payment_method_configuration",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/payment_method_configurations/{configuration}",
                    "params": {
                        "configuration": {
                            "type": "resolve",
                            "resource": "get_payment_method_configurations",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Lists the details of existing payment method domains.</p>
            {
                "name": "get_payment_method_domains",
                "table_name": "payment_method_domain",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/payment_method_domains",
                    "params": {
                        # the parameters below can optionally be configured
                        # "domain_name": "OPTIONAL_CONFIG",
                        # "enabled": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing payment method domain.</p>
            {
                "name": "get_payment_method_domains_payment_method_domain",
                "table_name": "payment_method_domain",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/payment_method_domains/{payment_method_domain}",
                    "params": {
                        "payment_method_domain": {
                            "type": "resolve",
                            "resource": "get_payment_method_domains",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve a specified source for a given customer.</p>
            {
                "name": "get_customers_customer_sources_id",
                "table_name": "payment_source",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/customers/{customer}/sources/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_customers_customer_sources",
                            "field": "id",
                        },
                        "customer": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of existing payouts sent to third-party bank accounts or payouts that Stripe sent to you. The payouts return in sorted order, with the most recently created payouts appearing first.</p>
            {
                "name": "get_payouts",
                "table_name": "payout",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/payouts",
                    "params": {
                        # the parameters below can optionally be configured
                        # "arrival_date": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "destination": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing payout. Supply the unique payout ID from either a payout creation request or the payout list. Stripe returns the corresponding payout information.</p>
            {
                "name": "get_payouts_payout",
                "table_name": "payout",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/payouts/{payout}",
                    "params": {
                        "payout": {
                            "type": "resolve",
                            "resource": "get_payouts",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Download the PDF for a finalized quote. Explanation for special handling can be found <a href="https://docs.corp.stripe.com/quotes/overview#quote_pdf">here</a></p>
            {
                "name": "get_quotes_quote_pdf",
                "table_name": "pdf",
                "endpoint": {
                    "path": "/v1/quotes/{quote}/pdf",
                    "params": {
                        "quote": {
                            "type": "resolve",
                            "resource": "get_quotes",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of people associated with the account’s legal entity. The people are returned sorted by creation date, with the most recent people appearing first.</p>
            {
                "name": "get_accounts_account_people",
                "table_name": "person",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/accounts/{account}/people",
                    "params": {
                        "account": {
                            "type": "resolve",
                            "resource": "get_accounts",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "relationship": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an existing person.</p>
            {
                "name": "get_accounts_account_people_person",
                "table_name": "person",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/accounts/{account}/people/{person}",
                    "params": {
                        "person": {
                            "type": "resolve",
                            "resource": "get_accounts_account_people",
                            "field": "id",
                        },
                        "account": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of people associated with the account’s legal entity. The people are returned sorted by creation date, with the most recent people appearing first.</p>
            {
                "name": "get_accounts_account_persons",
                "table_name": "person",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/accounts/{account}/persons",
                    "params": {
                        "account": {
                            "type": "resolve",
                            "resource": "get_accounts",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "relationship": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an existing person.</p>
            {
                "name": "get_accounts_account_persons_person",
                "table_name": "person",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/accounts/{account}/persons/{person}",
                    "params": {
                        "person": {
                            "type": "resolve",
                            "resource": "get_accounts_account_persons",
                            "field": "id",
                        },
                        "account": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your plans.</p>
            {
                "name": "get_plans",
                "table_name": "plan",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/plans",
                    "params": {
                        # the parameters below can optionally be configured
                        # "active": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "product": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the plan with the given ID.</p>
            {
                "name": "get_plans_plan",
                "table_name": "plan",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/plans/{plan}",
                    "params": {
                        "plan": {
                            "type": "resolve",
                            "resource": "get_plans",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an account.</p>
            {
                "name": "get_account",
                "table_name": "polymorphic",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "external_accounts.data",
                    "path": "/v1/account",
                    "params": {
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>List external accounts for an account.</p>
            {
                "name": "get_accounts_account_external_accounts",
                "table_name": "polymorphic",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/accounts/{account}/external_accounts",
                    "params": {
                        "account": {
                            "type": "resolve",
                            "resource": "get_accounts",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "object": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>List sources for a specified customer.</p>
            {
                "name": "get_customers_customer_sources",
                "table_name": "polymorphic",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/customers/{customer}/sources",
                    "params": {
                        "customer": {
                            "type": "resolve",
                            "resource": "get_customers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "object": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your active prices, excluding <a href="/docs/products-prices/pricing-models#inline-pricing">inline prices</a>. For the list of inactive prices, set <code>active</code> to false.</p>
            {
                "name": "get_prices",
                "table_name": "price",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/prices",
                    "params": {
                        # the parameters below can optionally be configured
                        # "active": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "currency": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "lookup_keys": "OPTIONAL_CONFIG",
                        # "product": "OPTIONAL_CONFIG",
                        # "recurring": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "type": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Search for prices you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
            {
                "name": "get_prices_search",
                "table_name": "price",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/prices/search",
                    "params": {
                        "query": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the price with the given ID.</p>
            {
                "name": "get_prices_price",
                "table_name": "price",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/prices/{price}",
                    "params": {
                        "price": {
                            "type": "resolve",
                            "resource": "get_prices",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your products. The products are returned sorted by creation date, with the most recently created products appearing first.</p>
            {
                "name": "get_products",
                "table_name": "product",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/products",
                    "params": {
                        # the parameters below can optionally be configured
                        # "active": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "ids": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "shippable": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "url": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Search for products you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
            {
                "name": "get_products_search",
                "table_name": "product",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/products/search",
                    "params": {
                        "query": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing product. Supply the unique product ID from either a product creation request or the product list, and Stripe will return the corresponding product information.</p>
            {
                "name": "get_products_id",
                "table_name": "product",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/products/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_products",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve a list of features for a product</p>
            {
                "name": "get_products_product_features",
                "table_name": "product_feature",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/products/{product}/features",
                    "params": {
                        "product": {
                            "type": "resolve",
                            "resource": "get_products",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a product_feature, which represents a feature attachment to a product</p>
            {
                "name": "get_products_product_features_id",
                "table_name": "product_feature",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/products/{product}/features/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_products_product_features",
                            "field": "id",
                        },
                        "product": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your promotion codes.</p>
            {
                "name": "get_promotion_codes",
                "table_name": "promotion_code",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/promotion_codes",
                    "params": {
                        # the parameters below can optionally be configured
                        # "active": "OPTIONAL_CONFIG",
                        # "code": "OPTIONAL_CONFIG",
                        # "coupon": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the promotion code with the given ID. In order to retrieve a promotion code by the customer-facing <code>code</code> use <a href="/docs/api/promotion_codes/list">list</a> with the desired <code>code</code>.</p>
            {
                "name": "get_promotion_codes_promotion_code",
                "table_name": "promotion_code",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/promotion_codes/{promotion_code}",
                    "params": {
                        "promotion_code": {
                            "type": "resolve",
                            "resource": "get_promotion_codes",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your quotes.</p>
            {
                "name": "get_quotes",
                "table_name": "quote",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/quotes",
                    "params": {
                        # the parameters below can optionally be configured
                        # "customer": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                        # "test_clock": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the quote with the given ID.</p>
            {
                "name": "get_quotes_quote",
                "table_name": "quote",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/quotes/{quote}",
                    "params": {
                        "quote": {
                            "type": "resolve",
                            "resource": "get_quotes",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of early fraud warnings.</p>
            {
                "name": "get_radar_early_fraud_warnings",
                "table_name": "radar_early_fraud_warning",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/radar/early_fraud_warnings",
                    "params": {
                        # the parameters below can optionally be configured
                        # "charge": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "payment_intent": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an early fraud warning that has previously been created. </p>  <p>Please refer to the <a href="#early_fraud_warning_object">early fraud warning</a> object reference for more details.</p>
            {
                "name": "get_radar_early_fraud_warnings_early_fraud_warning",
                "table_name": "radar_early_fraud_warning",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/radar/early_fraud_warnings/{early_fraud_warning}",
                    "params": {
                        "early_fraud_warning": {
                            "type": "resolve",
                            "resource": "get_radar_early_fraud_warnings",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of <code>ValueList</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
            {
                "name": "get_radar_value_lists",
                "table_name": "radar_value_list",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/radar/value_lists",
                    "params": {
                        # the parameters below can optionally be configured
                        # "alias": "OPTIONAL_CONFIG",
                        # "contains": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a <code>ValueList</code> object.</p>
            {
                "name": "get_radar_value_lists_value_list",
                "table_name": "radar_value_list",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/radar/value_lists/{value_list}",
                    "params": {
                        "value_list": {
                            "type": "resolve",
                            "resource": "get_radar_value_lists",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of <code>ValueListItem</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
            {
                "name": "get_radar_value_list_items",
                "table_name": "radar_value_list_item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/radar/value_list_items",
                    "params": {
                        "value_list": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "value": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a <code>ValueListItem</code> object.</p>
            {
                "name": "get_radar_value_list_items_item",
                "table_name": "radar_value_list_item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/radar/value_list_items/{item}",
                    "params": {
                        "item": {
                            "type": "resolve",
                            "resource": "get_radar_value_list_items",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a <code>Reader</code> object.</p>
            {
                "name": "get_terminal_readers_reader",
                "table_name": "reader",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/terminal/readers/{reader}",
                    "params": {
                        "reader": {
                            "type": "resolve",
                            "resource": "get_terminal_readers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>You can see a list of the refunds belonging to a specific charge. Note that the 10 most recent refunds are always available by default on the charge object. If you need more than those 10, you can use this API method and the <code>limit</code> and <code>starting_after</code> parameters to page through additional refunds.</p>
            {
                "name": "get_charges_charge_refunds",
                "table_name": "refund",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/charges/{charge}/refunds",
                    "params": {
                        "charge": {
                            "type": "resolve",
                            "resource": "get_charges",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing refund.</p>
            {
                "name": "get_charges_charge_refunds_refund",
                "table_name": "refund",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/charges/{charge}/refunds/{refund}",
                    "params": {
                        "refund": {
                            "type": "resolve",
                            "resource": "get_charges_charge_refunds",
                            "field": "id",
                        },
                        "charge": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of all refunds you created. We return the refunds in sorted order, with the most recent refunds appearing first The 10 most recent refunds are always available by default on the Charge object.</p>
            {
                "name": "get_refunds",
                "table_name": "refund",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/refunds",
                    "params": {
                        # the parameters below can optionally be configured
                        # "charge": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "payment_intent": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing refund.</p>
            {
                "name": "get_refunds_refund",
                "table_name": "refund",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/refunds/{refund}",
                    "params": {
                        "refund": {
                            "type": "resolve",
                            "resource": "get_refunds",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of Report Runs, with the most recent appearing first.</p>
            {
                "name": "get_reporting_report_runs",
                "table_name": "reporting_report_run",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/reporting/report_runs",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing Report Run.</p>
            {
                "name": "get_reporting_report_runs_report_run",
                "table_name": "reporting_report_run",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/reporting/report_runs/{report_run}",
                    "params": {
                        "report_run": {
                            "type": "resolve",
                            "resource": "get_reporting_report_runs",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a full list of Report Types.</p>
            {
                "name": "get_reporting_report_types",
                "table_name": "reporting_report_type",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/reporting/report_types",
                    "params": {
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of a Report Type. (Certain report types require a <a href="https://stripe.com/docs/keys#test-live-modes">live-mode API key</a>.)</p>
            {
                "name": "get_reporting_report_types_report_type",
                "table_name": "reporting_report_type",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/reporting/report_types/{report_type}",
                    "params": {
                        "report_type": {
                            "type": "resolve",
                            "resource": "get_reporting_report_types",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of <code>Review</code> objects that have <code>open</code> set to <code>true</code>. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
            {
                "name": "get_reviews",
                "table_name": "review",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/reviews",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a <code>Review</code> object.</p>
            {
                "name": "get_reviews_review",
                "table_name": "review",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/reviews/{review}",
                    "params": {
                        "review": {
                            "type": "resolve",
                            "resource": "get_reviews",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of scheduled query runs.</p>
            {
                "name": "get_sigma_scheduled_query_runs",
                "table_name": "scheduled_query_run",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/sigma/scheduled_query_runs",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an scheduled query run.</p>
            {
                "name": "get_sigma_scheduled_query_runs_scheduled_query_run",
                "table_name": "scheduled_query_run",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/sigma/scheduled_query_runs/{scheduled_query_run}",
                    "params": {
                        "scheduled_query_run": {
                            "type": "resolve",
                            "resource": "get_sigma_scheduled_query_runs",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves Tax <code>Settings</code> for a merchant.</p>
            {
                "name": "get_tax_settings",
                "table_name": "setting",
                "endpoint": {
                    "data_selector": "status_details.pending.missing_fields",
                    "path": "/v1/tax/settings",
                    "params": {
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of SetupAttempts that associate with a provided SetupIntent.</p>
            {
                "name": "get_setup_attempts",
                "table_name": "setup_attempt",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/setup_attempts",
                    "params": {
                        "setup_intent": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of SetupIntents.</p>
            {
                "name": "get_setup_intents",
                "table_name": "setup_intent",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/setup_intents",
                    "params": {
                        # the parameters below can optionally be configured
                        # "attach_to_self": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "payment_method": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of a SetupIntent that has previously been created. </p>  <p>Client-side retrieval using a publishable key is allowed when the <code>client_secret</code> is provided in the query string. </p>  <p>When retrieved with a publishable key, only a subset of properties will be returned. Please refer to the <a href="#setup_intent_object">SetupIntent</a> object reference for more details.</p>
            {
                "name": "get_setup_intents_intent",
                "table_name": "setup_intent",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/setup_intents/{intent}",
                    "params": {
                        "intent": {
                            "type": "resolve",
                            "resource": "get_setup_intents",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "client_secret": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your shipping rates.</p>
            {
                "name": "get_shipping_rates",
                "table_name": "shipping_rate",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/shipping_rates",
                    "params": {
                        # the parameters below can optionally be configured
                        # "active": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "currency": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns the shipping rate object with the given ID.</p>
            {
                "name": "get_shipping_rates_shipping_rate_token",
                "table_name": "shipping_rate",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/shipping_rates/{shipping_rate_token}",
                    "params": {
                        "shipping_rate_token": {
                            "type": "resolve",
                            "resource": "get_shipping_rates",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an existing source object. Supply the unique source ID from a source creation request and Stripe will return the corresponding up-to-date source object information.</p>
            {
                "name": "get_sources_source",
                "table_name": "source",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/sources/{source}",
                    "params": {
                        "source": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "client_secret": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a new Source MandateNotification.</p>
            {
                "name": "get_sources_source_mandate_notifications_mandate_notification",
                "table_name": "source_mandate_notification",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/sources/{source}/mandate_notifications/{mandate_notification}",
                    "params": {
                        "source": "FILL_ME_IN",  # TODO: fill in required path parameter
                        "mandate_notification": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>List source transactions for a given source.</p>
            {
                "name": "get_sources_source_source_transactions",
                "table_name": "source_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/sources/{source}/source_transactions",
                    "params": {
                        "source": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieve an existing source transaction object. Supply the unique source ID from a source creation request and the source transaction ID and Stripe will return the corresponding up-to-date source object information.</p>
            {
                "name": "get_sources_source_source_transactions_source_transaction",
                "table_name": "source_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/sources/{source}/source_transactions/{source_transaction}",
                    "params": {
                        "source_transaction": {
                            "type": "resolve",
                            "resource": "get_sources_source_source_transactions",
                            "field": "id",
                        },
                        "source": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>You can see a list of the customer’s active subscriptions. Note that the 10 most recent active subscriptions are always available by default on the customer object. If you need more than those 10, you can use the limit and starting_after parameters to page through additional subscriptions.</p>
            {
                "name": "get_customers_customer_subscriptions",
                "table_name": "subscription",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/customers/{customer}/subscriptions",
                    "params": {
                        "customer": {
                            "type": "resolve",
                            "resource": "get_customers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the subscription with the given ID.</p>
            {
                "name": "get_customers_customer_subscriptions_subscription_exposed_id",
                "table_name": "subscription",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/customers/{customer}/subscriptions/{subscription_exposed_id}",
                    "params": {
                        "subscription_exposed_id": {
                            "type": "resolve",
                            "resource": "get_customers_customer_subscriptions",
                            "field": "id",
                        },
                        "customer": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>By default, returns a list of subscriptions that have not been canceled. In order to list canceled subscriptions, specify <code>status=canceled</code>.</p>
            {
                "name": "get_subscriptions",
                "table_name": "subscription",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/subscriptions",
                    "params": {
                        # the parameters below can optionally be configured
                        # "automatic_tax": "OPTIONAL_CONFIG",
                        # "collection_method": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "current_period_end": "OPTIONAL_CONFIG",
                        # "current_period_start": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "price": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                        # "test_clock": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Search for subscriptions you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
            {
                "name": "get_subscriptions_search",
                "table_name": "subscription",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/subscriptions/search",
                    "params": {
                        "query": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                    },
                    "paginator": {
                        "type": "page_number",
                        "page_param": "page",
                        "total_path": "data.[*].latest_invoice.total",
                    },
                },
            },
            # <p>Retrieves the subscription with the given ID.</p>
            {
                "name": "get_subscriptions_subscription_exposed_id",
                "table_name": "subscription",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/subscriptions/{subscription_exposed_id}",
                    "params": {
                        "subscription_exposed_id": {
                            "type": "resolve",
                            "resource": "get_subscriptions",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your subscription items for a given subscription.</p>
            {
                "name": "get_subscription_items",
                "table_name": "subscription_item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/subscription_items",
                    "params": {
                        "subscription": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the subscription item with the given ID.</p>
            {
                "name": "get_subscription_items_item",
                "table_name": "subscription_item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/subscription_items/{item}",
                    "params": {
                        "item": {
                            "type": "resolve",
                            "resource": "get_subscription_items",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the list of your subscription schedules.</p>
            {
                "name": "get_subscription_schedules",
                "table_name": "subscription_schedule",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/subscription_schedules",
                    "params": {
                        # the parameters below can optionally be configured
                        # "canceled_at": "OPTIONAL_CONFIG",
                        # "completed_at": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "released_at": "OPTIONAL_CONFIG",
                        # "scheduled": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing subscription schedule. You only need to supply the unique subscription schedule identifier that was returned upon subscription schedule creation.</p>
            {
                "name": "get_subscription_schedules_schedule",
                "table_name": "subscription_schedule",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/subscription_schedules/{schedule}",
                    "params": {
                        "schedule": {
                            "type": "resolve",
                            "resource": "get_subscription_schedules",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the line items of a persisted tax calculation as a collection.</p>
            {
                "name": "get_tax_calculations_calculation_line_items",
                "table_name": "tax_calculation_line_item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/tax/calculations/{calculation}/line_items",
                    "params": {
                        "calculation": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>A list of <a href="https://stripe.com/docs/tax/tax-categories">all tax codes available</a> to add to Products in order to allow specific tax calculations.</p>
            {
                "name": "get_tax_codes",
                "table_name": "tax_code",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/tax_codes",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing tax code. Supply the unique tax code ID and Stripe will return the corresponding tax code information.</p>
            {
                "name": "get_tax_codes_id",
                "table_name": "tax_code",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/tax_codes/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_tax_codes",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of tax IDs for a customer.</p>
            {
                "name": "get_customers_customer_tax_ids",
                "table_name": "tax_id",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/customers/{customer}/tax_ids",
                    "params": {
                        "customer": {
                            "type": "resolve",
                            "resource": "get_customers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the <code>tax_id</code> object with the given identifier.</p>
            {
                "name": "get_customers_customer_tax_ids_id",
                "table_name": "tax_id",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/customers/{customer}/tax_ids/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_customers_customer_tax_ids",
                            "field": "id",
                        },
                        "customer": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of tax IDs.</p>
            {
                "name": "get_tax_ids",
                "table_name": "tax_id",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/tax_ids",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "owner": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves an account or customer <code>tax_id</code> object.</p>
            {
                "name": "get_tax_ids_id",
                "table_name": "tax_id",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/tax_ids/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_tax_ids",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your tax rates. Tax rates are returned sorted by creation date, with the most recently created tax rates appearing first.</p>
            {
                "name": "get_tax_rates",
                "table_name": "tax_rate",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/tax_rates",
                    "params": {
                        # the parameters below can optionally be configured
                        # "active": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "inclusive": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a tax rate with the given ID</p>
            {
                "name": "get_tax_rates_tax_rate",
                "table_name": "tax_rate",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/tax_rates/{tax_rate}",
                    "params": {
                        "tax_rate": {
                            "type": "resolve",
                            "resource": "get_tax_rates",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of Tax <code>Registration</code> objects.</p>
            {
                "name": "get_tax_registrations",
                "table_name": "tax_registration",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/tax/registrations",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a Tax <code>Registration</code> object.</p>
            {
                "name": "get_tax_registrations_id",
                "table_name": "tax_registration",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/tax/registrations/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_tax_registrations",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a Tax <code>Transaction</code> object.</p>
            {
                "name": "get_tax_transactions_transaction",
                "table_name": "tax_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/tax/transactions/{transaction}",
                    "params": {
                        "transaction": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the line items of a committed standalone transaction as a collection.</p>
            {
                "name": "get_tax_transactions_transaction_line_items",
                "table_name": "tax_transaction_line_item",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/tax/transactions/{transaction}/line_items",
                    "params": {
                        "transaction": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of <code>Configuration</code> objects.</p>
            {
                "name": "get_terminal_configurations",
                "table_name": "terminal_configuration",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/terminal/configurations",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "is_account_default": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of <code>Location</code> objects.</p>
            {
                "name": "get_terminal_locations",
                "table_name": "terminal_location",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/terminal/locations",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of <code>Reader</code> objects.</p>
            {
                "name": "get_terminal_readers",
                "table_name": "terminal_reader",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/terminal/readers",
                    "params": {
                        # the parameters below can optionally be configured
                        # "device_type": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "location": "OPTIONAL_CONFIG",
                        # "serial_number": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your test clocks.</p>
            {
                "name": "get_test_helpers_test_clocks",
                "table_name": "test_helpers_test_clock",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/test_helpers/test_clocks",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a test clock.</p>
            {
                "name": "get_test_helpers_test_clocks_test_clock",
                "table_name": "test_helpers_test_clock",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/test_helpers/test_clocks/{test_clock}",
                    "params": {
                        "test_clock": {
                            "type": "resolve",
                            "resource": "get_test_helpers_test_clocks",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the token with the given ID.</p>
            {
                "name": "get_tokens_token",
                "table_name": "token",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/tokens/{token}",
                    "params": {
                        "token": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of top-ups.</p>
            {
                "name": "get_topups",
                "table_name": "topup",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/topups",
                    "params": {
                        # the parameters below can optionally be configured
                        # "amount": "OPTIONAL_CONFIG",
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of a top-up that has previously been created. Supply the unique top-up ID that was returned from your previous request, and Stripe will return the corresponding top-up information.</p>
            {
                "name": "get_topups_topup",
                "table_name": "topup",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/topups/{topup}",
                    "params": {
                        "topup": {
                            "type": "resolve",
                            "resource": "get_topups",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of existing transfers sent to connected accounts. The transfers are returned in sorted order, with the most recently created transfers appearing first.</p>
            {
                "name": "get_transfers",
                "table_name": "transfer",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/transfers",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "destination": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "transfer_group": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing transfer. Supply the unique transfer ID from either a transfer creation request or the transfer list, and Stripe will return the corresponding transfer information.</p>
            {
                "name": "get_transfers_transfer",
                "table_name": "transfer",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/transfers/{transfer}",
                    "params": {
                        "transfer": {
                            "type": "resolve",
                            "resource": "get_transfers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>You can see a list of the reversals belonging to a specific transfer. Note that the 10 most recent reversals are always available by default on the transfer object. If you need more than those 10, you can use this API method and the <code>limit</code> and <code>starting_after</code> parameters to page through additional reversals.</p>
            {
                "name": "get_transfers_id_reversals",
                "table_name": "transfer_reversal",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/transfers/{id}/reversals",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_transfers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>By default, you can see the 10 most recent reversals stored directly on the transfer object, but you can also retrieve details about a specific reversal stored on the transfer.</p>
            {
                "name": "get_transfers_transfer_reversals_id",
                "table_name": "transfer_reversal",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/transfers/{transfer}/reversals/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_transfers",
                            "field": "id",
                        },
                        "transfer": "FILL_ME_IN",  # TODO: fill in required path parameter
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of CreditReversals.</p>
            {
                "name": "get_treasury_credit_reversals",
                "table_name": "treasury_credit_reversal",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/treasury/credit_reversals",
                    "params": {
                        "financial_account": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "received_credit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing CreditReversal by passing the unique CreditReversal ID from either the CreditReversal creation request or CreditReversal list</p>
            {
                "name": "get_treasury_credit_reversals_credit_reversal",
                "table_name": "treasury_credit_reversal",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/treasury/credit_reversals/{credit_reversal}",
                    "params": {
                        "credit_reversal": {
                            "type": "resolve",
                            "resource": "get_treasury_credit_reversals",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of DebitReversals.</p>
            {
                "name": "get_treasury_debit_reversals",
                "table_name": "treasury_debit_reversal",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/treasury/debit_reversals",
                    "params": {
                        "financial_account": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "received_debit": "OPTIONAL_CONFIG",
                        # "resolution": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a DebitReversal object.</p>
            {
                "name": "get_treasury_debit_reversals_debit_reversal",
                "table_name": "treasury_debit_reversal",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/treasury/debit_reversals/{debit_reversal}",
                    "params": {
                        "debit_reversal": {
                            "type": "resolve",
                            "resource": "get_treasury_debit_reversals",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of FinancialAccounts.</p>
            {
                "name": "get_treasury_financial_accounts",
                "table_name": "treasury_financial_account",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/treasury/financial_accounts",
                    "params": {
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of a FinancialAccount.</p>
            {
                "name": "get_treasury_financial_accounts_financial_account",
                "table_name": "treasury_financial_account",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/treasury/financial_accounts/{financial_account}",
                    "params": {
                        "financial_account": {
                            "type": "resolve",
                            "resource": "get_treasury_financial_accounts",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves Features information associated with the FinancialAccount.</p>
            {
                "name": "get_treasury_financial_accounts_financial_account_features",
                "table_name": "treasury_financial_accounts_resource_toggles_setting_status_details",
                "endpoint": {
                    "data_selector": "card_issuing.status_details",
                    "path": "/v1/treasury/financial_accounts/{financial_account}/features",
                    "params": {
                        "financial_account": {
                            "type": "resolve",
                            "resource": "get_treasury_financial_accounts",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of InboundTransfers sent from the specified FinancialAccount.</p>
            {
                "name": "get_treasury_inbound_transfers",
                "table_name": "treasury_inbound_transfer",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/treasury/inbound_transfers",
                    "params": {
                        "financial_account": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing InboundTransfer.</p>
            {
                "name": "get_treasury_inbound_transfers_id",
                "table_name": "treasury_inbound_transfer",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/treasury/inbound_transfers/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_treasury_inbound_transfers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of OutboundPayments sent from the specified FinancialAccount.</p>
            {
                "name": "get_treasury_outbound_payments",
                "table_name": "treasury_outbound_payment",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/treasury/outbound_payments",
                    "params": {
                        "financial_account": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing OutboundPayment by passing the unique OutboundPayment ID from either the OutboundPayment creation request or OutboundPayment list.</p>
            {
                "name": "get_treasury_outbound_payments_id",
                "table_name": "treasury_outbound_payment",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/treasury/outbound_payments/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_treasury_outbound_payments",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of OutboundTransfers sent from the specified FinancialAccount.</p>
            {
                "name": "get_treasury_outbound_transfers",
                "table_name": "treasury_outbound_transfer",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/treasury/outbound_transfers",
                    "params": {
                        "financial_account": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing OutboundTransfer by passing the unique OutboundTransfer ID from either the OutboundTransfer creation request or OutboundTransfer list.</p>
            {
                "name": "get_treasury_outbound_transfers_outbound_transfer",
                "table_name": "treasury_outbound_transfer",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/treasury/outbound_transfers/{outbound_transfer}",
                    "params": {
                        "outbound_transfer": {
                            "type": "resolve",
                            "resource": "get_treasury_outbound_transfers",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of ReceivedCredits.</p>
            {
                "name": "get_treasury_received_credits",
                "table_name": "treasury_received_credit",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/treasury/received_credits",
                    "params": {
                        "financial_account": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "linked_flows": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing ReceivedCredit by passing the unique ReceivedCredit ID from the ReceivedCredit list.</p>
            {
                "name": "get_treasury_received_credits_id",
                "table_name": "treasury_received_credit",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/treasury/received_credits/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_treasury_received_credits",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of ReceivedDebits.</p>
            {
                "name": "get_treasury_received_debits",
                "table_name": "treasury_received_debit",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/treasury/received_debits",
                    "params": {
                        "financial_account": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing ReceivedDebit by passing the unique ReceivedDebit ID from the ReceivedDebit list</p>
            {
                "name": "get_treasury_received_debits_id",
                "table_name": "treasury_received_debit",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/treasury/received_debits/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_treasury_received_debits",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a list of Transaction objects.</p>
            {
                "name": "get_treasury_transactions",
                "table_name": "treasury_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/treasury/transactions",
                    "params": {
                        "financial_account": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "order_by": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "status": "OPTIONAL_CONFIG",
                        # "status_transitions": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the details of an existing Transaction.</p>
            {
                "name": "get_treasury_transactions_id",
                "table_name": "treasury_transaction",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/treasury/transactions/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_treasury_transactions",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a list of TransactionEntry objects.</p>
            {
                "name": "get_treasury_transaction_entries",
                "table_name": "treasury_transaction_entry",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/treasury/transaction_entries",
                    "params": {
                        "financial_account": "FILL_ME_IN",  # TODO: fill in required query parameter
                        # the parameters below can optionally be configured
                        # "created": "OPTIONAL_CONFIG",
                        # "effective_at": "OPTIONAL_CONFIG",
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "order_by": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                        # "transaction": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves a TransactionEntry object.</p>
            {
                "name": "get_treasury_transaction_entries_id",
                "table_name": "treasury_transaction_entry",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/treasury/transaction_entries/{id}",
                    "params": {
                        "id": {
                            "type": "resolve",
                            "resource": "get_treasury_transaction_entries",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>At any time, you can preview the upcoming invoice for a customer. This will show you all the charges that are pending, including subscription renewal charges, invoice item charges, etc. It will also show you any discounts that are applicable to the invoice.</p>  <p>Note that when you are viewing an upcoming invoice, you are simply viewing a preview – the invoice has not yet been created. As such, the upcoming invoice will not show up in invoice listing calls, and you cannot use the API to pay or edit the invoice. If you want to change the amount that your customer will be billed, you can add, remove, or update pending invoice items, or update the customer’s discount.</p>  <p>You can preview the effects of updating a subscription, including a preview of what proration will take place. To ensure that the actual proration is calculated exactly the same as the previewed proration, you should pass the <code>subscription_details.proration_date</code> parameter when doing the actual subscription update. The recommended way to get only the prorations being previewed is to consider only proration line items where <code>period[start]</code> is equal to the <code>subscription_details.proration_date</code> value passed in the request.</p>  <p>Note: Currency conversion calculations use the latest exchange rates. Exchange rates may vary between the time of the preview and the time of the actual invoice creation. <a href="https://docs.stripe.com/currencies/conversions">Learn more</a></p>
            {
                "name": "get_invoices_upcoming",
                "table_name": "upcoming",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "account_tax_ids",
                    "path": "/v1/invoices/upcoming",
                    "params": {
                        # the parameters below can optionally be configured
                        # "automatic_tax": "OPTIONAL_CONFIG",
                        # "coupon": "OPTIONAL_CONFIG",
                        # "currency": "OPTIONAL_CONFIG",
                        # "customer": "OPTIONAL_CONFIG",
                        # "customer_details": "OPTIONAL_CONFIG",
                        # "discounts": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "invoice_items": "OPTIONAL_CONFIG",
                        # "issuer": "OPTIONAL_CONFIG",
                        # "on_behalf_of": "OPTIONAL_CONFIG",
                        # "preview_mode": "OPTIONAL_CONFIG",
                        # "schedule": "OPTIONAL_CONFIG",
                        # "schedule_details": "OPTIONAL_CONFIG",
                        # "subscription": "OPTIONAL_CONFIG",
                        # "subscription_billing_cycle_anchor": "OPTIONAL_CONFIG",
                        # "subscription_cancel_at": "OPTIONAL_CONFIG",
                        # "subscription_cancel_at_period_end": "OPTIONAL_CONFIG",
                        # "subscription_cancel_now": "OPTIONAL_CONFIG",
                        # "subscription_default_tax_rates": "OPTIONAL_CONFIG",
                        # "subscription_details": "OPTIONAL_CONFIG",
                        # "subscription_items": "OPTIONAL_CONFIG",
                        # "subscription_proration_behavior": "OPTIONAL_CONFIG",
                        # "subscription_proration_date": "OPTIONAL_CONFIG",
                        # "subscription_resume_at": "OPTIONAL_CONFIG",
                        # "subscription_start_date": "OPTIONAL_CONFIG",
                        # "subscription_trial_end": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>For the specified subscription item, returns a list of summary objects. Each object in the list provides usage information that’s been summarized from multiple usage records and over a subscription billing period (e.g., 15 usage records in the month of September).</p>  <p>The list is sorted in reverse-chronological order (newest first). The first list item represents the most current usage period that hasn’t ended yet. Since new usage records can still be added, the returned summary information for the subscription item’s ID should be seen as unstable until the subscription billing period ends.</p>
            {
                "name": "get_subscription_items_subscription_item_usage_record_summaries",
                "table_name": "usage_record_summary",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/subscription_items/{subscription_item}/usage_record_summaries",
                    "params": {
                        "subscription_item": {
                            "type": "resolve",
                            "resource": "get_subscription_items",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Returns a list of your webhook endpoints.</p>
            {
                "name": "get_webhook_endpoints",
                "table_name": "webhook_endpoint",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "data",
                    "path": "/v1/webhook_endpoints",
                    "params": {
                        # the parameters below can optionally be configured
                        # "ending_before": "OPTIONAL_CONFIG",
                        # "expand": "OPTIONAL_CONFIG",
                        # "limit": "OPTIONAL_CONFIG",
                        # "starting_after": "OPTIONAL_CONFIG",
                    },
                },
            },
            # <p>Retrieves the webhook endpoint with the given ID.</p>
            {
                "name": "get_webhook_endpoints_webhook_endpoint",
                "table_name": "webhook_endpoint",
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "data_selector": "$",
                    "path": "/v1/webhook_endpoints/{webhook_endpoint}",
                    "params": {
                        "webhook_endpoint": {
                            "type": "resolve",
                            "resource": "get_webhook_endpoints",
                            "field": "id",
                        },
                        # the parameters below can optionally be configured
                        # "expand": "OPTIONAL_CONFIG",
                    },
                },
            },
        ],
    }

    return rest_api_source(source_config)
