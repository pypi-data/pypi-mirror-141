# AWS Nitro Secure Module (NSM) interface in native Python 

This library offers a native Python interface to the `/dev/nsm` device in AWS Nitro Enclaves. This is an updated version from [aws-nsm-interface](https://github.com/donkersgoed/aws-nsm-interface).

## Installation
To install `aws_nsm_interface`, run:

```
pip install aws_nsm_interface
```

### Requirements
* To install: python>=3.6
* To run: a Python application running in an AWS Nitro Enclave

## Quickstart
```python
import base64
import aws_nsm_interface

file_desc = aws_nsm_interface.open_nsm_device()

rand_bytes = aws_nsm_interface.get_random(file_desc, 12) # Get 12 random bytes from /dev/nsm
print(rand_bytes)

public_rsa_key = b'1234' # An RSA public key exported as DER

attestation_doc = aws_nsm_interface.get_attestation_doc(
    file_desc,
    public_key=public_rsa_key
)['document']

attestation_doc_b64 = base64.b64encode(attestation_doc).decode('utf-8')

aws_nsm_interface.close_nsm_device(file_desc)

# Use `attestation_doc_b64` in your AWS KMS Decrypt call
```
