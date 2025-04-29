# Money Market Fund (MMF) Hub API Documentation

Thanks for using the Money Market Fund Hub API. This is your one-stop hub for
accessing data on the Kenyan Money Market Fund.


## Table of Contents

- [Public API](#public-api)
- [Getting Started](#getting-started)
  - [Analytics](#Analytics)
  - [Firm](#Firm)
  - [Rates](#Rates)
  - [Votes](#Votes)
- [Terms of Service](#terms-of-service)
- [Example Code](#example-code)
- [Software Development Kit (SDK)](#software-development-kit-sdk)

## Public API
Our API is hosted at [https://moneymarketfundhub.onrender.com/](https://moneymarketfundhub.onrender.com/). 

You can access the interactive documentation at [https://moneymarketfundhub.onrender.com/docs](https://moneymarketfundhub.onrender.com/docs).

You can view the OpenAPI Specification (OAS) file at
[https://moneymarketfundhub.onrender.com/openapi.json](https://moneymarketfundhub.onrender.com/openapi.json).

## Getting Started

Since all of the data is public, the MMF Hub API doesn't require any authentication. 
All of the the following data is available using GET endpoints that return 
JSON data.

### Analytics

Get information about the health of the API and counts of firms, users,
and votes.

### Firm
You can get a list of licenced Kenyan Money Market Fund Managers firms, or search for an individual firm by
firm_id.

### Rates

You can get a list of fund managers reports, including the effective annual rates
the reported and publised on Business Daily.

### Votes
Get information about the recommended firms as voted for by individual investors within the different firms.

## Terms of Service

By using the API, you agree to the following terms of service:

- **Usage Limits**: You are allowed up to 500 requests per day. Exceeding this 
                    limit may result in your API key being suspended.
- **No Warranty**: We don't provide any warranty of the API or its operation.

## Example Code

Here is some Python example code for accessing the health check endpoint:

```
import httpx

HEALTH_CHECK_ENDPOINT = "/"
    
with httpx.Client(base_url=self.mmf_hub_base_url) as client:
    response = client.get(self.HEALTH_CHECK_ENDPOINT)
    print(response.json())
```

## Software Development Kit (SDK)
*Coming Soon*

Check back for the Python SDK for our API.