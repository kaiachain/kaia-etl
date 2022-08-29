# MIT License
#
# Modifications Copyright (c) klaytn authors
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os

from web3 import HTTPProvider

from klaytnetl.providers.rpc import BatchHTTPProvider
from tests.klaytnetl.job.mock_batch_web3_provider import MockBatchWeb3Provider
from tests.klaytnetl.job.mock_web3_provider import MockWeb3Provider


def get_web3_provider(provider_type, read_resource_lambda=None, batch=False):
    if provider_type == "mock":
        if read_resource_lambda is None:
            raise ValueError(
                "read_resource_lambda must not be None for provider type mock".format(
                    provider_type
                )
            )
        if batch:
            provider = MockBatchWeb3Provider(read_resource_lambda)
        else:
            provider = MockWeb3Provider(read_resource_lambda)
    elif provider_type == "fantrie":
        provider_url = os.environ.get(
            "PROVIDER_URL", "https://cypress.fandom.finance/archive"
        )
        if batch:
            provider = BatchHTTPProvider(provider_url)
        else:
            provider = HTTPProvider(provider_url)
    else:
        raise ValueError("Provider type {} is unexpected".format(provider_type))
    return provider
