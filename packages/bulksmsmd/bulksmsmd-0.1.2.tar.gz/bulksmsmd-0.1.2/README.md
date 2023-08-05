<div align="center">

# `bulksmsmd` - Python wrapper for Unifun BulkSMSAPI (bulksms.md)

![PyPI Version](https://img.shields.io/pypi/pyversions/dash.svg)
![PyPI Version](https://img.shields.io/pypi/v/bulksmsmd.svg)
![License](https://img.shields.io/pypi/l/bulksmsmd.svg)

Condsider the official documentation before using this package or to understand the more advanced options __dlrurl__, __dlrmask__, __charset__ and __coding__.

[2021 Official documentation .DOCX](https://github.com/markmelnic/bulksmsmd/blob/main/res/docs_2021.docx)

[2021 Official documentation .PDF](https://github.com/markmelnic/bulksmsmd/blob/main/res/docs_2021.pdf)

</div>

## Installation

Installation is done using the following command:

    pip install bulksmsmd

## Usage

The `username` and `password` are the credentials for the API. The `sender` is the name of the sender.

    client = SMSClient(
        username = 'username',
        password = 'password',
        sender = 'sender',
    )

The `client` object is used to send messages and contains two methods: `send_sms_simple` & `send_sms_nde`.

    client.send_sms_simple(
        msisdn = '69123456',
        body = 'Test message.',
        prefix = '373',
    )

    client.send_sms_nde(
        msisdn = '69123456',
        body = 'Test message.',
        prefix = '373',
        dlr_url = 'https://example.com/dlr',
        dlr_mask = '31',
        charset = 'utf8',
        coding = '2',
    )
