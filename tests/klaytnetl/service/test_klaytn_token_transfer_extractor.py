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


from klaytnetl.domain.receipt_log import KlaytnReceiptLog
from klaytnetl.service.token_transfer_extractor import KlaytnTokenTransferExtractor

token_transfer_extractor = KlaytnTokenTransferExtractor()


def test_extract_transfer_from_receipt_log():
    log = KlaytnReceiptLog()
    log.address = "0xcee8faf64bb97a73bb51e115aa89c17ffa8dd167"
    log.block_number = 81165353
    log.data = "0x000000000000000000000000000000000000000000000000000000000501cdf5"
    log.log_index = 70
    log.topics = [
        "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
        "0x0000000000000000000000002bdf4c055102371aadb9b6bbe883b0b0a3a78ce0",
        "0x0000000000000000000000002abe3e13f3e82beb9708705164e4cc726d9802c3",
    ]
    log.transaction_hash = (
        "0xf83fbed71a38ee3ce24d88ef3a60495cb88e3622ee2770a3dd74622d2ef473c6"
    )
    log.transaction_index = 67
    log.block_hash = (
        "0xfcb46ee2e0656c5a6da13fdd05a306f5d0cd583a2516cba95a1b492e4086c068"
    )

    token_transfer = token_transfer_extractor.extract_transfer_from_log(log)

    assert token_transfer.token_address == "0xcee8faf64bb97a73bb51e115aa89c17ffa8dd167"
    assert token_transfer.from_address == "0x2bdf4c055102371aadb9b6bbe883b0b0a3a78ce0"
    assert token_transfer.to_address == "0x2abe3e13f3e82beb9708705164e4cc726d9802c3"
    assert token_transfer.value == 84004341
    assert (
        token_transfer.transaction_hash
        == "0xf83fbed71a38ee3ce24d88ef3a60495cb88e3622ee2770a3dd74622d2ef473c6"
    )
    assert token_transfer.block_number == 81165353
