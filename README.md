## A convenient PayWhirl API wrapper in Python

The [PayWhirl] Python library is provided to allow developers to access PayWhirl
services without needing to write their own API wrappers. 

The [Documentation] linked here and below contains all of the available methods 
for interacting with your PayWhirl account. If you would like to see additional 
functionality added, feel free to submit an issue or a pull request.



  [PayWhirl]: https://app.paywhirl.com/
  [Python]: https://www.python.org/
  [Documentation]: https://api.paywhirl.com/
### Usage Guide

- [Documentation]

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [License](#license)
- [About](#about)

## Requirements

- [Python]: Python 3.5+ 

## Installation

Place the `.py` file in your project and import the class so that you can 
instantiate a PayWhirl object. 

When you create a new PayWhirl object you need to pass in your API key and 
secret, which can be found in the [API key section of the main site](https://app.paywhirl.com/api-keys).
```
# include PayWhirl Python SDK
import paywhirl as pw

api_key = 'pwpk_xxxxxxxxxxxxxxx'
api_secret = 'pwpsk_xxxxxxxxxxx'

paywhirl = pw.PayWhirl(api_key, api_secret);
```



## License

PayWhirl is copyright © 2016-2018 [PayWhirl Inc.][PayWhirl] This library is free
software, and may be redistributed under the terms specified in the [license].

  [license]: LICENSE.md

## About

[PayWhirl Inc.][PayWhirl] and the names and logos for PayWhirl are
trademarks of PayWhirl inc.

For additional information, please see our [Terms of Use](https://app.paywhirl.com/terms) and [Privacy Policy](https://app.paywhirl.com/privacy)
