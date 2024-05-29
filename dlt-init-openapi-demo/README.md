# `dlt-init-openapi`, REST API Clients and `dlt`

A REST API (Representational State Transfer Application Programming Interface) is a set of rules and conventions for building and interacting with web services. It allows different systems to communicate over the internet using standard HTTP methods.

Generating a REST API client in Python can be done in several ways. Two popular methods are:

- Manually creating the client using the requests library.
- Automatically generating the client using an OpenAPI spec.

Another method is using [dlt rest_api source.](https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api)

`dlt` is an open-source library that you can add to your Python scripts to load data from various and often messy data sources into well-structured, live datasets.

The `rest_api` source in `dlt` is a versatile and generic tool designed to help you extract data from any REST API. By using a declarative configuration, you can define API endpoints, their relationships, pagination handling, and authentication methods effortlessly.

> See [dlt Rest API helpers tutorial](https://colab.research.google.com/drive/1qnzIM2N4iUL8AOX1oBUypzwoM3Hj5hhG?usp=sharing) for details.

`dlt` went ahead and created a RestAPI clients generator based on `rest_api` source and OpenAPI spec -- [`dlt-init-openapi`](https://pypi.org/project/dlt-init-openapi/).

## Installation

```sh
pip install dlt-init-openapi
```

## Initialize the source with Stripe OpenAPI Spec

This will take a while, you have time to make a coffee...

```sh
dlt-init-openapi stripe --url "https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.json"
```

Pipeline was generated, 247 endpoints were found, but **we do not believe in magic** and we need to make sure that source was generated correctly. 
For example, need to provide `base_url`, secrets, query parameters, etc.

Stripe is well known for its high-quality API and documentation, so you will find
[here](https://docs.stripe.com/api) all required information:
- base url;
- authentication type;
- pagination type;
- available query parameters;
- child endpoints.


Walk through this [dlt REST API tutorial](https://colab.research.google.com/drive/1qnzIM2N4iUL8AOX1oBUypzwoM3Hj5hhG?usp=sharing) to learn how to investigate API documentation and avoid struggling with building a REST API client.

We're gonna explore a few endpoints: [customers list](https://docs.stripe.com/api/customers/list), [subscriptions list](https://docs.stripe.com/api/subscriptions/list).

## Authentication

As you know, to gain access to the API you will need a secret token. [Here is a guide](https://docs.stripe.com/keys) how to get the key.


Let's explore the [Stripe API Authentication methods.](https://docs.stripe.com/stripe-apps/api-authentication)

It says here:

>Authentication to the API is performed via HTTP Basic Auth. Provide your API key as the basic auth username value. You do not need to provide a password.
>


## Pagination

Well, let's take a look at how the tool coped with pagination.
First, we will find out what type of pagination the Stripe API has:

>Stripe’s list API methods use **cursor-based pagination** through the `starting_after` and `ending_before` parameters. 
> Both parameters accept an existing object `ID` value (see below) and return objects in reverse chronological order.
> 

We can easily fix it, go to [the rest_api documentation](https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api#pagination) and find correct pagination type:

>**JSONResponseCursorPaginator** handles pagination based on a cursor in the JSON response. \
*Parameters*: \
`cursor_path`: A JSONPath expression pointing to the cursor in the JSON response. This cursor is used to fetch subsequent pages. Defaults to "cursors.next".\
`cursor_param`: The query parameter used to send the cursor value in the next request. Defaults to "after".


```
"paginator": {
    "type": "cursor",
    "cursor_path": "id",
    "cursor_param": "starting_after",
},
```


## Run the pipeline

```shell
python stripe_pipeline.py
```