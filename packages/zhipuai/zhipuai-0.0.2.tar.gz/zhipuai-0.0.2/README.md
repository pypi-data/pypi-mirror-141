# ZhipuAI Python Library

The zhipuAI Python library provides convenient access to the zhipuAI API
from applications written in the Python language. It includes a
pre-defined set of classes for API resources that initialize
themselves dynamically from API responses which makes it compatible
with a wide range of versions of the zhipuAI API.

## Documentation

See the [zhipuAI API docs](https://wudao.aminer.cn/dev_doc_v2/zh-CN/document/get_started/developer_quickstart).

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip install --upgrade zhipuai
```

Install from source with:

```sh
python setup.py install
```

## Usage

The library needs to be configured with your account's secret key which is available on the [website](https://beta.zhipuai.com/account/api-keys). Either set it as the `zhipuAI_API_KEY` environment variable before using the library:

```bash
export zhipuAI_API_KEY='sk-...'
```

Or set `zhipuai.api_key` to its value:

```python
import zhipuai
zhipuai.api_key = "sk-..."

# print the first engine's id
print(engines.data[0].id)

# create a completion
completion = zhipuai.Completion.create(model="glm", prompt="Hello world")

# print the completion
print(completion.choices[0].text)
```

### Command-line interface

Coming soon

## Example code

Coming soon

## Requirements

- Python 3.7.1+

In general we want to support the versions of Python that our
customers are using, so if you run into issues with any version
issues, please let us know at support@zhipuai.com.

## Credit

This library is forked from the [Stripe Python Library](https://github.com/stripe/stripe-python).
