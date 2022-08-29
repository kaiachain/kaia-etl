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


import csv
import json

import click
from blockchainetl.csv_utils import set_max_field_size_limit
from blockchainetl.file_utils import smart_open
from klaytnetl.jobs.exporters.tokens_item_exporter import tokens_item_exporter
from klaytnetl.jobs.extract_tokens_job import ExtractTokensJob
from blockchainetl.logging_utils import logging_basic_config
from klaytnetl.providers.auto import get_provider_from_uri
from klaytnetl.thread_local_proxy import ThreadLocalProxy
from klaytnetl.utils import return_provider

from web3 import Web3
from web3.middleware import geth_poa_middleware

logging_basic_config()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-c",
    "--contracts",
    type=str,
    required=True,
    help="The JSON file containing contracts.",
)
@click.option(
    "-p",
    "--provider-uri",
    default="https://cypress.fandom.finance/archive",
    show_default=True,
    type=str,
    help="The URI of the web3 provider e.g. "
    "file://$HOME/var/kend/data/klay.ipc or https://cypress.fandom.finance/archive",
)
@click.option(
    "-o",
    "--output",
    default="-",
    type=str,
    help="The output file. If not specified stdout is used.",
)
@click.option(
    "-w",
    "--max-workers",
    default=5,
    show_default=True,
    type=int,
    help="The maximum number of workers.",
)
@click.option(
    "--network",
    default=None,
    type=str,
    help="Input either baobab or cypress to obtain public provider"
    "If not provided, the option will be disabled.",
)
def extract_tokens(contracts, provider_uri, output, max_workers, network):
    """Extracts tokens from contracts file."""
    if network:
        provider_uri = return_provider(network)

    set_max_field_size_limit()

    web3 = Web3(get_provider_from_uri(provider_uri))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    with smart_open(contracts, "r") as contracts_file:
        if contracts.endswith(".json"):
            contracts_iterable = (json.loads(line) for line in contracts_file)
        else:
            contracts_iterable = csv.DictReader(contracts_file)
        job = ExtractTokensJob(
            contracts_iterable=contracts_iterable,
            web3=ThreadLocalProxy(lambda: web3),
            max_workers=max_workers,
            item_exporter=tokens_item_exporter(output),
        )

        job.run()
