# stripe pipeline

Created with [dlt-init-openapi](https://github.com/dlt-hub/dlt-init-openapi) v. 0.1.0

Generated from downloaded spec at `https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.json`
## Learn more at

* https://dlthub.com
* https://github.com/dlt-hub/dlt
* https://github.com/dlt-hub/dlt-init-openapi

## Credentials
This API uses http authentication. Please fill in the required variables ['username', 'password'] in your 
secrets.toml.

## Available resources
* _GET /v1/accounts_ 
  *resource*: get_accounts  
  *description*: <p>Returns a list of accounts connected to your platform via <a href="/docs/connect">Connect</a>. If you’re not a platform, the list is empty.</p>
* _GET /v1/accounts/{account}_ 
  *resource*: get_accounts_account  
  *description*: <p>Retrieves the details of an account.</p>
* _GET /v1/apple_pay/domains_ 
  *resource*: get_apple_pay_domains  
  *description*: <p>List apple pay domains.</p>
* _GET /v1/apple_pay/domains/{domain}_ 
  *resource*: get_apple_pay_domains_domain  
  *description*: <p>Retrieve an apple pay domain.</p>
* _GET /v1/application_fees_ 
  *resource*: get_application_fees  
  *description*: <p>Returns a list of application fees you’ve previously collected. The application fees are returned in sorted order, with the most recent fees appearing first.</p>
* _GET /v1/application_fees/{id}_ 
  *resource*: get_application_fees_id  
  *description*: <p>Retrieves the details of an application fee that your account has collected. The same information is returned when refunding the application fee.</p>
* _GET /v1/apps/secrets_ 
  *resource*: get_apps_secrets  
  *description*: <p>List all secrets stored on the given scope.</p>
* _GET /v1/apps/secrets/find_ 
  *resource*: get_apps_secrets_find  
  *description*: <p>Finds a secret in the secret store by name and scope.</p>
* _GET /v1/balance_ 
  *resource*: get_balance  
  *description*: <p>Retrieves the current account balance, based on the authentication that was used to make the request.  For a sample request, see <a href="/docs/connect/account-balances#accounting-for-negative-balances">Accounting for negative balances</a>.</p>
* _GET /v1/balance/history_ 
  *resource*: get_balance_history  
  *description*: <p>Returns a list of transactions that have contributed to the Stripe account balance (e.g., charges, transfers, and so forth). The transactions are returned in sorted order, with the most recent transactions appearing first.</p>  <p>Note that this endpoint was previously called “Balance history” and used the path <code>/v1/balance/history</code>.</p>
* _GET /v1/balance/history/{id}_ 
  *resource*: get_balance_history_id  
  *description*: <p>Retrieves the balance transaction with the given ID.</p>  <p>Note that this endpoint previously used the path <code>/v1/balance/history/:id</code>.</p>
* _GET /v1/balance_transactions_ 
  *resource*: get_balance_transactions  
  *description*: <p>Returns a list of transactions that have contributed to the Stripe account balance (e.g., charges, transfers, and so forth). The transactions are returned in sorted order, with the most recent transactions appearing first.</p>  <p>Note that this endpoint was previously called “Balance history” and used the path <code>/v1/balance/history</code>.</p>
* _GET /v1/balance_transactions/{id}_ 
  *resource*: get_balance_transactions_id  
  *description*: <p>Retrieves the balance transaction with the given ID.</p>  <p>Note that this endpoint previously used the path <code>/v1/balance/history/:id</code>.</p>
* _GET /v1/charges/{charge}/dispute_ 
  *resource*: get_charges_charge_dispute  
  *description*: <p>Retrieve a dispute for a specified charge.</p>
* _GET /v1/customers/{customer}/bank_accounts_ 
  *resource*: get_customers_customer_bank_accounts  
  *description*: <p>You can see a list of the bank accounts belonging to a Customer. Note that the 10 most recent sources are always available by default on the Customer. If you need more than those 10, you can use this API method and the <code>limit</code> and <code>starting_after</code> parameters to page through additional bank accounts.</p>
* _GET /v1/customers/{customer}/bank_accounts/{id}_ 
  *resource*: get_customers_customer_bank_accounts_id  
  *description*: <p>By default, you can see the 10 most recent sources stored on a Customer directly on the object, but you can also retrieve details about a specific bank account stored on the Stripe account.</p>
* _GET /v1/billing/meters_ 
  *resource*: get_billing_meters  
  *description*: <p>Retrieve a list of billing meters.</p>
* _GET /v1/billing/meters/{id}_ 
  *resource*: get_billing_meters_id  
  *description*: <p>Retrieves a billing meter given an ID</p>
* _GET /v1/billing/meters/{id}/event_summaries_ 
  *resource*: get_billing_meters_id_event_summaries  
  *description*: <p>Retrieve a list of billing meter event summaries.</p>
* _GET /v1/billing_portal/configurations_ 
  *resource*: get_billing_portal_configurations  
  *description*: <p>Returns a list of configurations that describe the functionality of the customer portal.</p>
* _GET /v1/billing_portal/configurations/{configuration}_ 
  *resource*: get_billing_portal_configurations_configuration  
  *description*: <p>Retrieves a configuration that describes the functionality of the customer portal.</p>
* _GET /v1/accounts/{account}/capabilities_ 
  *resource*: get_accounts_account_capabilities  
  *description*: <p>Returns a list of capabilities associated with the account. The capabilities are returned sorted by creation date, with the most recent capability appearing first.</p>
* _GET /v1/accounts/{account}/capabilities/{capability}_ 
  *resource*: get_accounts_account_capabilities_capability  
  *description*: <p>Retrieves information about the specified Account Capability.</p>
* _GET /v1/customers/{customer}/cards_ 
  *resource*: get_customers_customer_cards  
  *description*: <p>You can see a list of the cards belonging to a customer. Note that the 10 most recent sources are always available on the <code>Customer</code> object. If you need more than those 10, you can use this API method and the <code>limit</code> and <code>starting_after</code> parameters to page through additional cards.</p>
* _GET /v1/customers/{customer}/cards/{id}_ 
  *resource*: get_customers_customer_cards_id  
  *description*: <p>You can always see the 10 most recent cards directly on a customer; this method lets you retrieve details about a specific card stored on the customer.</p>
* _GET /v1/customers/{customer}/cash_balance_ 
  *resource*: get_customers_customer_cash_balance  
  *description*: <p>Retrieves a customer’s cash balance.</p>
* _GET /v1/charges_ 
  *resource*: get_charges  
  *description*: <p>Returns a list of charges you’ve previously created. The charges are returned in sorted order, with the most recent charges appearing first.</p>
* _GET /v1/charges/search_ 
  *resource*: get_charges_search  
  *description*: <p>Search for charges you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
* _GET /v1/charges/{charge}_ 
  *resource*: get_charges_charge  
  *description*: <p>Retrieves the details of a charge that has previously been created. Supply the unique charge ID that was returned from your previous request, and Stripe will return the corresponding charge information. The same information is returned when creating or refunding the charge.</p>
* _GET /v1/checkout/sessions_ 
  *resource*: get_checkout_sessions  
  *description*: <p>Returns a list of Checkout Sessions.</p>
* _GET /v1/checkout/sessions/{session}_ 
  *resource*: get_checkout_sessions_session  
  *description*: <p>Retrieves a Session object.</p>
* _GET /v1/climate/orders_ 
  *resource*: get_climate_orders  
  *description*: <p>Lists all Climate order objects. The orders are returned sorted by creation date, with the most recently created orders appearing first.</p>
* _GET /v1/climate/orders/{order}_ 
  *resource*: get_climate_orders_order  
  *description*: <p>Retrieves the details of a Climate order object with the given ID.</p>
* _GET /v1/climate/products_ 
  *resource*: get_climate_products  
  *description*: <p>Lists all available Climate product objects.</p>
* _GET /v1/climate/products/{product}_ 
  *resource*: get_climate_products_product  
  *description*: <p>Retrieves the details of a Climate product with the given ID.</p>
* _GET /v1/climate/suppliers_ 
  *resource*: get_climate_suppliers  
  *description*: <p>Lists all available Climate supplier objects.</p>
* _GET /v1/climate/suppliers/{supplier}_ 
  *resource*: get_climate_suppliers_supplier  
  *description*: <p>Retrieves a Climate supplier object.</p>
* _GET /v1/terminal/configurations/{configuration}_ 
  *resource*: get_terminal_configurations_configuration  
  *description*: <p>Retrieves a <code>Configuration</code> object.</p>
* _GET /v1/confirmation_tokens/{confirmation_token}_ 
  *resource*: get_confirmation_tokens_confirmation_token  
  *description*: <p>Retrieves an existing ConfirmationToken object</p>
* _GET /v1/country_specs_ 
  *resource*: get_country_specs  
  *description*: <p>Lists all Country Spec objects available in the API.</p>
* _GET /v1/country_specs/{country}_ 
  *resource*: get_country_specs_country  
  *description*: <p>Returns a Country Spec for a given Country code.</p>
* _GET /v1/coupons_ 
  *resource*: get_coupons  
  *description*: <p>Returns a list of your coupons.</p>
* _GET /v1/coupons/{coupon}_ 
  *resource*: get_coupons_coupon  
  *description*: <p>Retrieves the coupon with the given ID.</p>
* _GET /v1/credit_notes_ 
  *resource*: get_credit_notes  
  *description*: <p>Returns a list of credit notes.</p>
* _GET /v1/credit_notes/{id}_ 
  *resource*: get_credit_notes_id  
  *description*: <p>Retrieves the credit note object with the given identifier.</p>
* _GET /v1/credit_notes/preview/lines_ 
  *resource*: get_credit_notes_preview_lines  
  *description*: <p>When retrieving a credit note preview, you’ll get a <strong>lines</strong> property containing the first handful of those items. This URL you can retrieve the full (paginated) list of line items.</p>
* _GET /v1/credit_notes/{credit_note}/lines_ 
  *resource*: get_credit_notes_credit_note_lines  
  *description*: <p>When retrieving a credit note, you’ll get a <strong>lines</strong> property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.</p>
* _GET /v1/customers_ 
  *resource*: get_customers  
  *description*: <p>Returns a list of your customers. The customers are returned sorted by creation date, with the most recent customers appearing first.</p>
* _GET /v1/customers/search_ 
  *resource*: get_customers_search  
  *description*: <p>Search for customers you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
* _GET /v1/customers/{customer}_ 
  *resource*: get_customers_customer  
  *description*: <p>Retrieves a Customer object.</p>
* _GET /v1/customers/{customer}/balance_transactions_ 
  *resource*: get_customers_customer_balance_transactions  
  *description*: <p>Returns a list of transactions that updated the customer’s <a href="/docs/billing/customer/balance">balances</a>.</p>
* _GET /v1/customers/{customer}/balance_transactions/{transaction}_ 
  *resource*: get_customers_customer_balance_transactions_transaction  
  *description*: <p>Retrieves a specific customer balance transaction that updated the customer’s <a href="/docs/billing/customer/balance">balances</a>.</p>
* _GET /v1/customers/{customer}/cash_balance_transactions_ 
  *resource*: get_customers_customer_cash_balance_transactions  
  *description*: <p>Returns a list of transactions that modified the customer’s <a href="/docs/payments/customer-balance">cash balance</a>.</p>
* _GET /v1/customers/{customer}/cash_balance_transactions/{transaction}_ 
  *resource*: get_customers_customer_cash_balance_transactions_transaction  
  *description*: <p>Retrieves a specific cash balance transaction, which updated the customer’s <a href="/docs/payments/customer-balance">cash balance</a>.</p>
* _GET /v1/customers/{customer}/discount_ 
  *resource*: get_customers_customer_discount  
* _GET /v1/customers/{customer}/subscriptions/{subscription_exposed_id}/discount_ 
  *resource*: get_customers_customer_subscriptions_subscription_exposed_id_discount  
* _GET /v1/credit_notes/preview_ 
  *resource*: get_credit_notes_preview  
  *description*: <p>Get a preview of a credit note without creating it.</p>
* _GET /v1/disputes_ 
  *resource*: get_disputes  
  *description*: <p>Returns a list of your disputes.</p>
* _GET /v1/disputes/{dispute}_ 
  *resource*: get_disputes_dispute  
  *description*: <p>Retrieves the dispute with the given ID.</p>
* _GET /v1/entitlements/active_entitlements_ 
  *resource*: get_entitlements_active_entitlements  
  *description*: <p>Retrieve a list of active entitlements for a customer</p>
* _GET /v1/entitlements/active_entitlements/{id}_ 
  *resource*: get_entitlements_active_entitlements_id  
  *description*: <p>Retrieve an active entitlement</p>
* _GET /v1/entitlements/features_ 
  *resource*: get_entitlements_features  
  *description*: <p>Retrieve a list of features</p>
* _GET /v1/entitlements/features/{id}_ 
  *resource*: get_entitlements_features_id  
  *description*: <p>Retrieves a feature</p>
* _GET /v1/events_ 
  *resource*: get_events  
  *description*: <p>List events, going back up to 30 days. Each event data is rendered according to Stripe API version at its creation time, specified in <a href="https://docs.stripe.com/api/events/object">event object</a> <code>api_version</code> attribute (not according to your current Stripe API version or <code>Stripe-Version</code> header).</p>
* _GET /v1/events/{id}_ 
  *resource*: get_events_id  
  *description*: <p>Retrieves the details of an event. Supply the unique identifier of the event, which you might have received in a webhook.</p>
* _GET /v1/exchange_rates_ 
  *resource*: get_exchange_rates  
  *description*: <p>Returns a list of objects that contain the rates at which foreign currencies are converted to one another. Only shows the currencies for which Stripe supports.</p>
* _GET /v1/exchange_rates/{rate_id}_ 
  *resource*: get_exchange_rates_rate_id  
  *description*: <p>Retrieves the exchange rates from the given currency to every supported currency.</p>
* _GET /v1/accounts/{account}/bank_accounts/{id}_ 
  *resource*: get_accounts_account_bank_accounts_id  
  *description*: <p>Retrieve a specified external account for a given account.</p>
* _GET /v1/accounts/{account}/external_accounts/{id}_ 
  *resource*: get_accounts_account_external_accounts_id  
  *description*: <p>Retrieve a specified external account for a given account.</p>
* _GET /v1/application_fees/{fee}/refunds/{id}_ 
  *resource*: get_application_fees_fee_refunds_id  
  *description*: <p>By default, you can see the 10 most recent refunds stored directly on the application fee object, but you can also retrieve details about a specific refund stored on the application fee.</p>
* _GET /v1/application_fees/{id}/refunds_ 
  *resource*: get_application_fees_id_refunds  
  *description*: <p>You can see a list of the refunds belonging to a specific application fee. Note that the 10 most recent refunds are always available by default on the application fee object. If you need more than those 10, you can use this API method and the <code>limit</code> and <code>starting_after</code> parameters to page through additional refunds.</p>
* _GET /v1/files_ 
  *resource*: get_files  
  *description*: <p>Returns a list of the files that your account has access to. Stripe sorts and returns the files by their creation dates, placing the most recently created files at the top.</p>
* _GET /v1/files/{file}_ 
  *resource*: get_files_file  
  *description*: <p>Retrieves the details of an existing file object. After you supply a unique file ID, Stripe returns the corresponding file object. Learn how to <a href="/docs/file-upload#download-file-contents">access file contents</a>.</p>
* _GET /v1/file_links_ 
  *resource*: get_file_links  
  *description*: <p>Returns a list of file links.</p>
* _GET /v1/file_links/{link}_ 
  *resource*: get_file_links_link  
  *description*: <p>Retrieves the file link with the given ID.</p>
* _GET /v1/financial_connections/accounts_ 
  *resource*: get_financial_connections_accounts  
  *description*: <p>Returns a list of Financial Connections <code>Account</code> objects.</p>
* _GET /v1/financial_connections/accounts/{account}_ 
  *resource*: get_financial_connections_accounts_account  
  *description*: <p>Retrieves the details of an Financial Connections <code>Account</code>.</p>
* _GET /v1/linked_accounts_ 
  *resource*: get_linked_accounts  
  *description*: <p>Returns a list of Financial Connections <code>Account</code> objects.</p>
* _GET /v1/linked_accounts/{account}_ 
  *resource*: get_linked_accounts_account  
  *description*: <p>Retrieves the details of an Financial Connections <code>Account</code>.</p>
* _GET /v1/financial_connections/accounts/{account}/owners_ 
  *resource*: get_financial_connections_accounts_account_owners  
  *description*: <p>Lists all owners for a given <code>Account</code></p>
* _GET /v1/linked_accounts/{account}/owners_ 
  *resource*: get_linked_accounts_account_owners  
  *description*: <p>Lists all owners for a given <code>Account</code></p>
* _GET /v1/financial_connections/sessions/{session}_ 
  *resource*: get_financial_connections_sessions_session  
  *description*: <p>Retrieves the details of a Financial Connections <code>Session</code></p>
* _GET /v1/link_account_sessions/{session}_ 
  *resource*: get_link_account_sessions_session  
  *description*: <p>Retrieves the details of a Financial Connections <code>Session</code></p>
* _GET /v1/financial_connections/transactions_ 
  *resource*: get_financial_connections_transactions  
  *description*: <p>Returns a list of Financial Connections <code>Transaction</code> objects.</p>
* _GET /v1/financial_connections/transactions/{transaction}_ 
  *resource*: get_financial_connections_transactions_transaction  
  *description*: <p>Retrieves the details of a Financial Connections <code>Transaction</code></p>
* _GET /v1/forwarding/requests_ 
  *resource*: get_forwarding_requests  
  *description*: <p>Lists all ForwardingRequest objects.</p>
* _GET /v1/forwarding/requests/{id}_ 
  *resource*: get_forwarding_requests_id  
  *description*: <p>Retrieves a ForwardingRequest object.</p>
* _GET /v1/identity/verification_reports_ 
  *resource*: get_identity_verification_reports  
  *description*: <p>List all verification reports.</p>
* _GET /v1/identity/verification_reports/{report}_ 
  *resource*: get_identity_verification_reports_report  
  *description*: <p>Retrieves an existing VerificationReport</p>
* _GET /v1/identity/verification_sessions_ 
  *resource*: get_identity_verification_sessions  
  *description*: <p>Returns a list of VerificationSessions</p>
* _GET /v1/identity/verification_sessions/{session}_ 
  *resource*: get_identity_verification_sessions_session  
  *description*: <p>Retrieves the details of a VerificationSession that was previously created.</p>  <p>When the session status is <code>requires_input</code>, you can use this method to retrieve a valid <code>client_secret</code> or <code>url</code> to allow re-submission.</p>
* _GET /v1/invoices_ 
  *resource*: get_invoices  
  *description*: <p>You can list all invoices, or list the invoices for a specific customer. The invoices are returned sorted by creation date, with the most recently created invoices appearing first.</p>
* _GET /v1/invoices/search_ 
  *resource*: get_invoices_search  
  *description*: <p>Search for invoices you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
* _GET /v1/invoices/{invoice}_ 
  *resource*: get_invoices_invoice  
  *description*: <p>Retrieves the invoice with the given ID.</p>
* _GET /v1/invoiceitems_ 
  *resource*: get_invoiceitems  
  *description*: <p>Returns a list of your invoice items. Invoice items are returned sorted by creation date, with the most recently created invoice items appearing first.</p>
* _GET /v1/invoiceitems/{invoiceitem}_ 
  *resource*: get_invoiceitems_invoiceitem  
  *description*: <p>Retrieves the invoice item with the given ID.</p>
* _GET /v1/issuing/authorizations_ 
  *resource*: get_issuing_authorizations  
  *description*: <p>Returns a list of Issuing <code>Authorization</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
* _GET /v1/issuing/authorizations/{authorization}_ 
  *resource*: get_issuing_authorizations_authorization  
  *description*: <p>Retrieves an Issuing <code>Authorization</code> object.</p>
* _GET /v1/issuing/cards_ 
  *resource*: get_issuing_cards  
  *description*: <p>Returns a list of Issuing <code>Card</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
* _GET /v1/issuing/cards/{card}_ 
  *resource*: get_issuing_cards_card  
  *description*: <p>Retrieves an Issuing <code>Card</code> object.</p>
* _GET /v1/issuing/cardholders_ 
  *resource*: get_issuing_cardholders  
  *description*: <p>Returns a list of Issuing <code>Cardholder</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
* _GET /v1/issuing/cardholders/{cardholder}_ 
  *resource*: get_issuing_cardholders_cardholder  
  *description*: <p>Retrieves an Issuing <code>Cardholder</code> object.</p>
* _GET /v1/issuing/disputes_ 
  *resource*: get_issuing_disputes  
  *description*: <p>Returns a list of Issuing <code>Dispute</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
* _GET /v1/issuing/disputes/{dispute}_ 
  *resource*: get_issuing_disputes_dispute  
  *description*: <p>Retrieves an Issuing <code>Dispute</code> object.</p>
* _GET /v1/issuing/personalization_designs_ 
  *resource*: get_issuing_personalization_designs  
  *description*: <p>Returns a list of personalization design objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
* _GET /v1/issuing/personalization_designs/{personalization_design}_ 
  *resource*: get_issuing_personalization_designs_personalization_design  
  *description*: <p>Retrieves a personalization design object.</p>
* _GET /v1/issuing/physical_bundles_ 
  *resource*: get_issuing_physical_bundles  
  *description*: <p>Returns a list of physical bundle objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
* _GET /v1/issuing/physical_bundles/{physical_bundle}_ 
  *resource*: get_issuing_physical_bundles_physical_bundle  
  *description*: <p>Retrieves a physical bundle object.</p>
* _GET /v1/issuing/settlements/{settlement}_ 
  *resource*: get_issuing_settlements_settlement  
  *description*: <p>Retrieves an Issuing <code>Settlement</code> object.</p>
* _GET /v1/issuing/tokens_ 
  *resource*: get_issuing_tokens  
  *description*: <p>Lists all Issuing <code>Token</code> objects for a given card.</p>
* _GET /v1/issuing/tokens/{token}_ 
  *resource*: get_issuing_tokens_token  
  *description*: <p>Retrieves an Issuing <code>Token</code> object.</p>
* _GET /v1/issuing/transactions_ 
  *resource*: get_issuing_transactions  
  *description*: <p>Returns a list of Issuing <code>Transaction</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
* _GET /v1/issuing/transactions/{transaction}_ 
  *resource*: get_issuing_transactions_transaction  
  *description*: <p>Retrieves an Issuing <code>Transaction</code> object.</p>
* _GET /v1/checkout/sessions/{session}/line_items_ 
  *resource*: get_checkout_sessions_session_line_items  
  *description*: <p>When retrieving a Checkout Session, there is an includable <strong>line_items</strong> property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.</p>
* _GET /v1/payment_links/{payment_link}/line_items_ 
  *resource*: get_payment_links_payment_link_line_items  
  *description*: <p>When retrieving a payment link, there is an includable <strong>line_items</strong> property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.</p>
* _GET /v1/quotes/{quote}/computed_upfront_line_items_ 
  *resource*: get_quotes_quote_computed_upfront_line_items  
  *description*: <p>When retrieving a quote, there is an includable <a href="https://stripe.com/docs/api/quotes/object#quote_object-computed-upfront-line_items"><strong>computed.upfront.line_items</strong></a> property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of upfront line items.</p>
* _GET /v1/quotes/{quote}/line_items_ 
  *resource*: get_quotes_quote_line_items  
  *description*: <p>When retrieving a quote, there is an includable <strong>line_items</strong> property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.</p>
* _GET /v1/invoices/upcoming/lines_ 
  *resource*: get_invoices_upcoming_lines  
  *description*: <p>When retrieving an upcoming invoice, you’ll get a <strong>lines</strong> property containing the total count of line items and the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.</p>
* _GET /v1/invoices/{invoice}/lines_ 
  *resource*: get_invoices_invoice_lines  
  *description*: <p>When retrieving an invoice, you’ll get a <strong>lines</strong> property containing the total count of line items and the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.</p>
* _GET /v1/terminal/locations/{location}_ 
  *resource*: get_terminal_locations_location  
  *description*: <p>Retrieves a <code>Location</code> object.</p>
* _GET /v1/mandates/{mandate}_ 
  *resource*: get_mandates_mandate  
  *description*: <p>Retrieves a Mandate object.</p>
* _GET /v1/payment_intents_ 
  *resource*: get_payment_intents  
  *description*: <p>Returns a list of PaymentIntents.</p>
* _GET /v1/payment_intents/search_ 
  *resource*: get_payment_intents_search  
  *description*: <p>Search for PaymentIntents you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
* _GET /v1/payment_intents/{intent}_ 
  *resource*: get_payment_intents_intent  
  *description*: <p>Retrieves the details of a PaymentIntent that has previously been created. </p>  <p>You can retrieve a PaymentIntent client-side using a publishable key when the <code>client_secret</code> is in the query string. </p>  <p>If you retrieve a PaymentIntent with a publishable key, it only returns a subset of properties. Refer to the <a href="#payment_intent_object">payment intent</a> object reference for more details.</p>
* _GET /v1/payment_links_ 
  *resource*: get_payment_links  
  *description*: <p>Returns a list of your payment links.</p>
* _GET /v1/payment_links/{payment_link}_ 
  *resource*: get_payment_links_payment_link  
  *description*: <p>Retrieve a payment link.</p>
* _GET /v1/customers/{customer}/payment_methods_ 
  *resource*: get_customers_customer_payment_methods  
  *description*: <p>Returns a list of PaymentMethods for a given Customer</p>
* _GET /v1/customers/{customer}/payment_methods/{payment_method}_ 
  *resource*: get_customers_customer_payment_methods_payment_method  
  *description*: <p>Retrieves a PaymentMethod object for a given Customer.</p>
* _GET /v1/payment_methods_ 
  *resource*: get_payment_methods  
  *description*: <p>Returns a list of PaymentMethods for Treasury flows. If you want to list the PaymentMethods attached to a Customer for payments, you should use the <a href="/docs/api/payment_methods/customer_list">List a Customer’s PaymentMethods</a> API instead.</p>
* _GET /v1/payment_methods/{payment_method}_ 
  *resource*: get_payment_methods_payment_method  
  *description*: <p>Retrieves a PaymentMethod object attached to the StripeAccount. To retrieve a payment method attached to a Customer, you should use <a href="/docs/api/payment_methods/customer">Retrieve a Customer’s PaymentMethods</a></p>
* _GET /v1/payment_method_configurations_ 
  *resource*: get_payment_method_configurations  
  *description*: <p>List payment method configurations</p>
* _GET /v1/payment_method_configurations/{configuration}_ 
  *resource*: get_payment_method_configurations_configuration  
  *description*: <p>Retrieve payment method configuration</p>
* _GET /v1/payment_method_domains_ 
  *resource*: get_payment_method_domains  
  *description*: <p>Lists the details of existing payment method domains.</p>
* _GET /v1/payment_method_domains/{payment_method_domain}_ 
  *resource*: get_payment_method_domains_payment_method_domain  
  *description*: <p>Retrieves the details of an existing payment method domain.</p>
* _GET /v1/customers/{customer}/sources/{id}_ 
  *resource*: get_customers_customer_sources_id  
  *description*: <p>Retrieve a specified source for a given customer.</p>
* _GET /v1/payouts_ 
  *resource*: get_payouts  
  *description*: <p>Returns a list of existing payouts sent to third-party bank accounts or payouts that Stripe sent to you. The payouts return in sorted order, with the most recently created payouts appearing first.</p>
* _GET /v1/payouts/{payout}_ 
  *resource*: get_payouts_payout  
  *description*: <p>Retrieves the details of an existing payout. Supply the unique payout ID from either a payout creation request or the payout list. Stripe returns the corresponding payout information.</p>
* _GET /v1/quotes/{quote}/pdf_ 
  *resource*: get_quotes_quote_pdf  
  *description*: <p>Download the PDF for a finalized quote. Explanation for special handling can be found <a href="https://docs.corp.stripe.com/quotes/overview#quote_pdf">here</a></p>
* _GET /v1/accounts/{account}/people_ 
  *resource*: get_accounts_account_people  
  *description*: <p>Returns a list of people associated with the account’s legal entity. The people are returned sorted by creation date, with the most recent people appearing first.</p>
* _GET /v1/accounts/{account}/people/{person}_ 
  *resource*: get_accounts_account_people_person  
  *description*: <p>Retrieves an existing person.</p>
* _GET /v1/accounts/{account}/persons_ 
  *resource*: get_accounts_account_persons  
  *description*: <p>Returns a list of people associated with the account’s legal entity. The people are returned sorted by creation date, with the most recent people appearing first.</p>
* _GET /v1/accounts/{account}/persons/{person}_ 
  *resource*: get_accounts_account_persons_person  
  *description*: <p>Retrieves an existing person.</p>
* _GET /v1/plans_ 
  *resource*: get_plans  
  *description*: <p>Returns a list of your plans.</p>
* _GET /v1/plans/{plan}_ 
  *resource*: get_plans_plan  
  *description*: <p>Retrieves the plan with the given ID.</p>
* _GET /v1/account_ 
  *resource*: get_account  
  *description*: <p>Retrieves the details of an account.</p>
* _GET /v1/accounts/{account}/external_accounts_ 
  *resource*: get_accounts_account_external_accounts  
  *description*: <p>List external accounts for an account.</p>
* _GET /v1/customers/{customer}/sources_ 
  *resource*: get_customers_customer_sources  
  *description*: <p>List sources for a specified customer.</p>
* _GET /v1/prices_ 
  *resource*: get_prices  
  *description*: <p>Returns a list of your active prices, excluding <a href="/docs/products-prices/pricing-models#inline-pricing">inline prices</a>. For the list of inactive prices, set <code>active</code> to false.</p>
* _GET /v1/prices/search_ 
  *resource*: get_prices_search  
  *description*: <p>Search for prices you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
* _GET /v1/prices/{price}_ 
  *resource*: get_prices_price  
  *description*: <p>Retrieves the price with the given ID.</p>
* _GET /v1/products_ 
  *resource*: get_products  
  *description*: <p>Returns a list of your products. The products are returned sorted by creation date, with the most recently created products appearing first.</p>
* _GET /v1/products/search_ 
  *resource*: get_products_search  
  *description*: <p>Search for products you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
* _GET /v1/products/{id}_ 
  *resource*: get_products_id  
  *description*: <p>Retrieves the details of an existing product. Supply the unique product ID from either a product creation request or the product list, and Stripe will return the corresponding product information.</p>
* _GET /v1/products/{product}/features_ 
  *resource*: get_products_product_features  
  *description*: <p>Retrieve a list of features for a product</p>
* _GET /v1/products/{product}/features/{id}_ 
  *resource*: get_products_product_features_id  
  *description*: <p>Retrieves a product_feature, which represents a feature attachment to a product</p>
* _GET /v1/promotion_codes_ 
  *resource*: get_promotion_codes  
  *description*: <p>Returns a list of your promotion codes.</p>
* _GET /v1/promotion_codes/{promotion_code}_ 
  *resource*: get_promotion_codes_promotion_code  
  *description*: <p>Retrieves the promotion code with the given ID. In order to retrieve a promotion code by the customer-facing <code>code</code> use <a href="/docs/api/promotion_codes/list">list</a> with the desired <code>code</code>.</p>
* _GET /v1/quotes_ 
  *resource*: get_quotes  
  *description*: <p>Returns a list of your quotes.</p>
* _GET /v1/quotes/{quote}_ 
  *resource*: get_quotes_quote  
  *description*: <p>Retrieves the quote with the given ID.</p>
* _GET /v1/radar/early_fraud_warnings_ 
  *resource*: get_radar_early_fraud_warnings  
  *description*: <p>Returns a list of early fraud warnings.</p>
* _GET /v1/radar/early_fraud_warnings/{early_fraud_warning}_ 
  *resource*: get_radar_early_fraud_warnings_early_fraud_warning  
  *description*: <p>Retrieves the details of an early fraud warning that has previously been created. </p>  <p>Please refer to the <a href="#early_fraud_warning_object">early fraud warning</a> object reference for more details.</p>
* _GET /v1/radar/value_lists_ 
  *resource*: get_radar_value_lists  
  *description*: <p>Returns a list of <code>ValueList</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
* _GET /v1/radar/value_lists/{value_list}_ 
  *resource*: get_radar_value_lists_value_list  
  *description*: <p>Retrieves a <code>ValueList</code> object.</p>
* _GET /v1/radar/value_list_items_ 
  *resource*: get_radar_value_list_items  
  *description*: <p>Returns a list of <code>ValueListItem</code> objects. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
* _GET /v1/radar/value_list_items/{item}_ 
  *resource*: get_radar_value_list_items_item  
  *description*: <p>Retrieves a <code>ValueListItem</code> object.</p>
* _GET /v1/terminal/readers/{reader}_ 
  *resource*: get_terminal_readers_reader  
  *description*: <p>Retrieves a <code>Reader</code> object.</p>
* _GET /v1/charges/{charge}/refunds_ 
  *resource*: get_charges_charge_refunds  
  *description*: <p>You can see a list of the refunds belonging to a specific charge. Note that the 10 most recent refunds are always available by default on the charge object. If you need more than those 10, you can use this API method and the <code>limit</code> and <code>starting_after</code> parameters to page through additional refunds.</p>
* _GET /v1/charges/{charge}/refunds/{refund}_ 
  *resource*: get_charges_charge_refunds_refund  
  *description*: <p>Retrieves the details of an existing refund.</p>
* _GET /v1/refunds_ 
  *resource*: get_refunds  
  *description*: <p>Returns a list of all refunds you created. We return the refunds in sorted order, with the most recent refunds appearing first The 10 most recent refunds are always available by default on the Charge object.</p>
* _GET /v1/refunds/{refund}_ 
  *resource*: get_refunds_refund  
  *description*: <p>Retrieves the details of an existing refund.</p>
* _GET /v1/reporting/report_runs_ 
  *resource*: get_reporting_report_runs  
  *description*: <p>Returns a list of Report Runs, with the most recent appearing first.</p>
* _GET /v1/reporting/report_runs/{report_run}_ 
  *resource*: get_reporting_report_runs_report_run  
  *description*: <p>Retrieves the details of an existing Report Run.</p>
* _GET /v1/reporting/report_types_ 
  *resource*: get_reporting_report_types  
  *description*: <p>Returns a full list of Report Types.</p>
* _GET /v1/reporting/report_types/{report_type}_ 
  *resource*: get_reporting_report_types_report_type  
  *description*: <p>Retrieves the details of a Report Type. (Certain report types require a <a href="https://stripe.com/docs/keys#test-live-modes">live-mode API key</a>.)</p>
* _GET /v1/reviews_ 
  *resource*: get_reviews  
  *description*: <p>Returns a list of <code>Review</code> objects that have <code>open</code> set to <code>true</code>. The objects are sorted in descending order by creation date, with the most recently created object appearing first.</p>
* _GET /v1/reviews/{review}_ 
  *resource*: get_reviews_review  
  *description*: <p>Retrieves a <code>Review</code> object.</p>
* _GET /v1/sigma/scheduled_query_runs_ 
  *resource*: get_sigma_scheduled_query_runs  
  *description*: <p>Returns a list of scheduled query runs.</p>
* _GET /v1/sigma/scheduled_query_runs/{scheduled_query_run}_ 
  *resource*: get_sigma_scheduled_query_runs_scheduled_query_run  
  *description*: <p>Retrieves the details of an scheduled query run.</p>
* _GET /v1/tax/settings_ 
  *resource*: get_tax_settings  
  *description*: <p>Retrieves Tax <code>Settings</code> for a merchant.</p>
* _GET /v1/setup_attempts_ 
  *resource*: get_setup_attempts  
  *description*: <p>Returns a list of SetupAttempts that associate with a provided SetupIntent.</p>
* _GET /v1/setup_intents_ 
  *resource*: get_setup_intents  
  *description*: <p>Returns a list of SetupIntents.</p>
* _GET /v1/setup_intents/{intent}_ 
  *resource*: get_setup_intents_intent  
  *description*: <p>Retrieves the details of a SetupIntent that has previously been created. </p>  <p>Client-side retrieval using a publishable key is allowed when the <code>client_secret</code> is provided in the query string. </p>  <p>When retrieved with a publishable key, only a subset of properties will be returned. Please refer to the <a href="#setup_intent_object">SetupIntent</a> object reference for more details.</p>
* _GET /v1/shipping_rates_ 
  *resource*: get_shipping_rates  
  *description*: <p>Returns a list of your shipping rates.</p>
* _GET /v1/shipping_rates/{shipping_rate_token}_ 
  *resource*: get_shipping_rates_shipping_rate_token  
  *description*: <p>Returns the shipping rate object with the given ID.</p>
* _GET /v1/sources/{source}_ 
  *resource*: get_sources_source  
  *description*: <p>Retrieves an existing source object. Supply the unique source ID from a source creation request and Stripe will return the corresponding up-to-date source object information.</p>
* _GET /v1/sources/{source}/mandate_notifications/{mandate_notification}_ 
  *resource*: get_sources_source_mandate_notifications_mandate_notification  
  *description*: <p>Retrieves a new Source MandateNotification.</p>
* _GET /v1/sources/{source}/source_transactions_ 
  *resource*: get_sources_source_source_transactions  
  *description*: <p>List source transactions for a given source.</p>
* _GET /v1/sources/{source}/source_transactions/{source_transaction}_ 
  *resource*: get_sources_source_source_transactions_source_transaction  
  *description*: <p>Retrieve an existing source transaction object. Supply the unique source ID from a source creation request and the source transaction ID and Stripe will return the corresponding up-to-date source object information.</p>
* _GET /v1/customers/{customer}/subscriptions_ 
  *resource*: get_customers_customer_subscriptions  
  *description*: <p>You can see a list of the customer’s active subscriptions. Note that the 10 most recent active subscriptions are always available by default on the customer object. If you need more than those 10, you can use the limit and starting_after parameters to page through additional subscriptions.</p>
* _GET /v1/customers/{customer}/subscriptions/{subscription_exposed_id}_ 
  *resource*: get_customers_customer_subscriptions_subscription_exposed_id  
  *description*: <p>Retrieves the subscription with the given ID.</p>
* _GET /v1/subscriptions_ 
  *resource*: get_subscriptions  
  *description*: <p>By default, returns a list of subscriptions that have not been canceled. In order to list canceled subscriptions, specify <code>status=canceled</code>.</p>
* _GET /v1/subscriptions/search_ 
  *resource*: get_subscriptions_search  
  *description*: <p>Search for subscriptions you’ve previously created using Stripe’s <a href="/docs/search#search-query-language">Search Query Language</a>. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.</p>
* _GET /v1/subscriptions/{subscription_exposed_id}_ 
  *resource*: get_subscriptions_subscription_exposed_id  
  *description*: <p>Retrieves the subscription with the given ID.</p>
* _GET /v1/subscription_items_ 
  *resource*: get_subscription_items  
  *description*: <p>Returns a list of your subscription items for a given subscription.</p>
* _GET /v1/subscription_items/{item}_ 
  *resource*: get_subscription_items_item  
  *description*: <p>Retrieves the subscription item with the given ID.</p>
* _GET /v1/subscription_schedules_ 
  *resource*: get_subscription_schedules  
  *description*: <p>Retrieves the list of your subscription schedules.</p>
* _GET /v1/subscription_schedules/{schedule}_ 
  *resource*: get_subscription_schedules_schedule  
  *description*: <p>Retrieves the details of an existing subscription schedule. You only need to supply the unique subscription schedule identifier that was returned upon subscription schedule creation.</p>
* _GET /v1/tax/calculations/{calculation}/line_items_ 
  *resource*: get_tax_calculations_calculation_line_items  
  *description*: <p>Retrieves the line items of a persisted tax calculation as a collection.</p>
* _GET /v1/tax_codes_ 
  *resource*: get_tax_codes  
  *description*: <p>A list of <a href="https://stripe.com/docs/tax/tax-categories">all tax codes available</a> to add to Products in order to allow specific tax calculations.</p>
* _GET /v1/tax_codes/{id}_ 
  *resource*: get_tax_codes_id  
  *description*: <p>Retrieves the details of an existing tax code. Supply the unique tax code ID and Stripe will return the corresponding tax code information.</p>
* _GET /v1/customers/{customer}/tax_ids_ 
  *resource*: get_customers_customer_tax_ids  
  *description*: <p>Returns a list of tax IDs for a customer.</p>
* _GET /v1/customers/{customer}/tax_ids/{id}_ 
  *resource*: get_customers_customer_tax_ids_id  
  *description*: <p>Retrieves the <code>tax_id</code> object with the given identifier.</p>
* _GET /v1/tax_ids_ 
  *resource*: get_tax_ids  
  *description*: <p>Returns a list of tax IDs.</p>
* _GET /v1/tax_ids/{id}_ 
  *resource*: get_tax_ids_id  
  *description*: <p>Retrieves an account or customer <code>tax_id</code> object.</p>
* _GET /v1/tax_rates_ 
  *resource*: get_tax_rates  
  *description*: <p>Returns a list of your tax rates. Tax rates are returned sorted by creation date, with the most recently created tax rates appearing first.</p>
* _GET /v1/tax_rates/{tax_rate}_ 
  *resource*: get_tax_rates_tax_rate  
  *description*: <p>Retrieves a tax rate with the given ID</p>
* _GET /v1/tax/registrations_ 
  *resource*: get_tax_registrations  
  *description*: <p>Returns a list of Tax <code>Registration</code> objects.</p>
* _GET /v1/tax/registrations/{id}_ 
  *resource*: get_tax_registrations_id  
  *description*: <p>Returns a Tax <code>Registration</code> object.</p>
* _GET /v1/tax/transactions/{transaction}_ 
  *resource*: get_tax_transactions_transaction  
  *description*: <p>Retrieves a Tax <code>Transaction</code> object.</p>
* _GET /v1/tax/transactions/{transaction}/line_items_ 
  *resource*: get_tax_transactions_transaction_line_items  
  *description*: <p>Retrieves the line items of a committed standalone transaction as a collection.</p>
* _GET /v1/terminal/configurations_ 
  *resource*: get_terminal_configurations  
  *description*: <p>Returns a list of <code>Configuration</code> objects.</p>
* _GET /v1/terminal/locations_ 
  *resource*: get_terminal_locations  
  *description*: <p>Returns a list of <code>Location</code> objects.</p>
* _GET /v1/terminal/readers_ 
  *resource*: get_terminal_readers  
  *description*: <p>Returns a list of <code>Reader</code> objects.</p>
* _GET /v1/test_helpers/test_clocks_ 
  *resource*: get_test_helpers_test_clocks  
  *description*: <p>Returns a list of your test clocks.</p>
* _GET /v1/test_helpers/test_clocks/{test_clock}_ 
  *resource*: get_test_helpers_test_clocks_test_clock  
  *description*: <p>Retrieves a test clock.</p>
* _GET /v1/tokens/{token}_ 
  *resource*: get_tokens_token  
  *description*: <p>Retrieves the token with the given ID.</p>
* _GET /v1/topups_ 
  *resource*: get_topups  
  *description*: <p>Returns a list of top-ups.</p>
* _GET /v1/topups/{topup}_ 
  *resource*: get_topups_topup  
  *description*: <p>Retrieves the details of a top-up that has previously been created. Supply the unique top-up ID that was returned from your previous request, and Stripe will return the corresponding top-up information.</p>
* _GET /v1/transfers_ 
  *resource*: get_transfers  
  *description*: <p>Returns a list of existing transfers sent to connected accounts. The transfers are returned in sorted order, with the most recently created transfers appearing first.</p>
* _GET /v1/transfers/{transfer}_ 
  *resource*: get_transfers_transfer  
  *description*: <p>Retrieves the details of an existing transfer. Supply the unique transfer ID from either a transfer creation request or the transfer list, and Stripe will return the corresponding transfer information.</p>
* _GET /v1/transfers/{id}/reversals_ 
  *resource*: get_transfers_id_reversals  
  *description*: <p>You can see a list of the reversals belonging to a specific transfer. Note that the 10 most recent reversals are always available by default on the transfer object. If you need more than those 10, you can use this API method and the <code>limit</code> and <code>starting_after</code> parameters to page through additional reversals.</p>
* _GET /v1/transfers/{transfer}/reversals/{id}_ 
  *resource*: get_transfers_transfer_reversals_id  
  *description*: <p>By default, you can see the 10 most recent reversals stored directly on the transfer object, but you can also retrieve details about a specific reversal stored on the transfer.</p>
* _GET /v1/treasury/credit_reversals_ 
  *resource*: get_treasury_credit_reversals  
  *description*: <p>Returns a list of CreditReversals.</p>
* _GET /v1/treasury/credit_reversals/{credit_reversal}_ 
  *resource*: get_treasury_credit_reversals_credit_reversal  
  *description*: <p>Retrieves the details of an existing CreditReversal by passing the unique CreditReversal ID from either the CreditReversal creation request or CreditReversal list</p>
* _GET /v1/treasury/debit_reversals_ 
  *resource*: get_treasury_debit_reversals  
  *description*: <p>Returns a list of DebitReversals.</p>
* _GET /v1/treasury/debit_reversals/{debit_reversal}_ 
  *resource*: get_treasury_debit_reversals_debit_reversal  
  *description*: <p>Retrieves a DebitReversal object.</p>
* _GET /v1/treasury/financial_accounts_ 
  *resource*: get_treasury_financial_accounts  
  *description*: <p>Returns a list of FinancialAccounts.</p>
* _GET /v1/treasury/financial_accounts/{financial_account}_ 
  *resource*: get_treasury_financial_accounts_financial_account  
  *description*: <p>Retrieves the details of a FinancialAccount.</p>
* _GET /v1/treasury/financial_accounts/{financial_account}/features_ 
  *resource*: get_treasury_financial_accounts_financial_account_features  
  *description*: <p>Retrieves Features information associated with the FinancialAccount.</p>
* _GET /v1/treasury/inbound_transfers_ 
  *resource*: get_treasury_inbound_transfers  
  *description*: <p>Returns a list of InboundTransfers sent from the specified FinancialAccount.</p>
* _GET /v1/treasury/inbound_transfers/{id}_ 
  *resource*: get_treasury_inbound_transfers_id  
  *description*: <p>Retrieves the details of an existing InboundTransfer.</p>
* _GET /v1/treasury/outbound_payments_ 
  *resource*: get_treasury_outbound_payments  
  *description*: <p>Returns a list of OutboundPayments sent from the specified FinancialAccount.</p>
* _GET /v1/treasury/outbound_payments/{id}_ 
  *resource*: get_treasury_outbound_payments_id  
  *description*: <p>Retrieves the details of an existing OutboundPayment by passing the unique OutboundPayment ID from either the OutboundPayment creation request or OutboundPayment list.</p>
* _GET /v1/treasury/outbound_transfers_ 
  *resource*: get_treasury_outbound_transfers  
  *description*: <p>Returns a list of OutboundTransfers sent from the specified FinancialAccount.</p>
* _GET /v1/treasury/outbound_transfers/{outbound_transfer}_ 
  *resource*: get_treasury_outbound_transfers_outbound_transfer  
  *description*: <p>Retrieves the details of an existing OutboundTransfer by passing the unique OutboundTransfer ID from either the OutboundTransfer creation request or OutboundTransfer list.</p>
* _GET /v1/treasury/received_credits_ 
  *resource*: get_treasury_received_credits  
  *description*: <p>Returns a list of ReceivedCredits.</p>
* _GET /v1/treasury/received_credits/{id}_ 
  *resource*: get_treasury_received_credits_id  
  *description*: <p>Retrieves the details of an existing ReceivedCredit by passing the unique ReceivedCredit ID from the ReceivedCredit list.</p>
* _GET /v1/treasury/received_debits_ 
  *resource*: get_treasury_received_debits  
  *description*: <p>Returns a list of ReceivedDebits.</p>
* _GET /v1/treasury/received_debits/{id}_ 
  *resource*: get_treasury_received_debits_id  
  *description*: <p>Retrieves the details of an existing ReceivedDebit by passing the unique ReceivedDebit ID from the ReceivedDebit list</p>
* _GET /v1/treasury/transactions_ 
  *resource*: get_treasury_transactions  
  *description*: <p>Retrieves a list of Transaction objects.</p>
* _GET /v1/treasury/transactions/{id}_ 
  *resource*: get_treasury_transactions_id  
  *description*: <p>Retrieves the details of an existing Transaction.</p>
* _GET /v1/treasury/transaction_entries_ 
  *resource*: get_treasury_transaction_entries  
  *description*: <p>Retrieves a list of TransactionEntry objects.</p>
* _GET /v1/treasury/transaction_entries/{id}_ 
  *resource*: get_treasury_transaction_entries_id  
  *description*: <p>Retrieves a TransactionEntry object.</p>
* _GET /v1/invoices/upcoming_ 
  *resource*: get_invoices_upcoming  
  *description*: <p>At any time, you can preview the upcoming invoice for a customer. This will show you all the charges that are pending, including subscription renewal charges, invoice item charges, etc. It will also show you any discounts that are applicable to the invoice.</p>  <p>Note that when you are viewing an upcoming invoice, you are simply viewing a preview – the invoice has not yet been created. As such, the upcoming invoice will not show up in invoice listing calls, and you cannot use the API to pay or edit the invoice. If you want to change the amount that your customer will be billed, you can add, remove, or update pending invoice items, or update the customer’s discount.</p>  <p>You can preview the effects of updating a subscription, including a preview of what proration will take place. To ensure that the actual proration is calculated exactly the same as the previewed proration, you should pass the <code>subscription_details.proration_date</code> parameter when doing the actual subscription update. The recommended way to get only the prorations being previewed is to consider only proration line items where <code>period[start]</code> is equal to the <code>subscription_details.proration_date</code> value passed in the request.</p>  <p>Note: Currency conversion calculations use the latest exchange rates. Exchange rates may vary between the time of the preview and the time of the actual invoice creation. <a href="https://docs.stripe.com/currencies/conversions">Learn more</a></p>
* _GET /v1/subscription_items/{subscription_item}/usage_record_summaries_ 
  *resource*: get_subscription_items_subscription_item_usage_record_summaries  
  *description*: <p>For the specified subscription item, returns a list of summary objects. Each object in the list provides usage information that’s been summarized from multiple usage records and over a subscription billing period (e.g., 15 usage records in the month of September).</p>  <p>The list is sorted in reverse-chronological order (newest first). The first list item represents the most current usage period that hasn’t ended yet. Since new usage records can still be added, the returned summary information for the subscription item’s ID should be seen as unstable until the subscription billing period ends.</p>
* _GET /v1/webhook_endpoints_ 
  *resource*: get_webhook_endpoints  
  *description*: <p>Returns a list of your webhook endpoints.</p>
* _GET /v1/webhook_endpoints/{webhook_endpoint}_ 
  *resource*: get_webhook_endpoints_webhook_endpoint  
  *description*: <p>Retrieves the webhook endpoint with the given ID.</p>
