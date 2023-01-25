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


from eth_utils import function_signature_to_4byte_selector
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

from ethereum_dasm.evmdasm import EvmCode, Contract
from klaytnetl.erc165_abi import ERC165_ABI

ERC20_INTERFACE = "0x36372b07"
ERC721_INTERFACE = "0x80ac58cd"
ERC1155_INTERFACE = "0xd9b67a26"


class KlaytnContractService:
    def __init__(self, web3):
        self._web3 = web3

    def get_function_sighashes(self, bytecode):
        bytecode = clean_bytecode(bytecode)
        function_sighashes = []
        if bytecode is not None:
            evm_code = EvmCode(
                contract=Contract(bytecode=bytecode),
                static_analysis=False,
                dynamic_analysis=False,
            )
            evm_code.disassemble(bytecode)
            basic_blocks = evm_code.basicblocks
            if basic_blocks and len(basic_blocks) > 0:
                instructions = [
                    inst for block in basic_blocks for inst in block.instructions
                ]

                for inst in instructions:
                    # Special case when balanceOf(address,uint256) becomes PUSH3 due to optimization
                    # https://github.com/blockchain-etl/ethereum-etl/issues/349#issuecomment-1243352201
                    if inst.name == "PUSH3" and inst.operand == "fdd58e":
                        function_sighashes.append("0x00" + inst.operand)
                    if inst.name == "PUSH4":
                        function_sighashes.append("0x" + inst.operand)

                return sorted(list(set(function_sighashes)))
            else:
                return []
        else:
            return []

    def contract_interface_support(self, contract_address, block_number, interface):
        checksum_address = self._web3.toChecksumAddress(contract_address)
        contract_165 = self._web3.eth.contract(address=checksum_address, abi=ERC165_ABI)
        try:
            contract_interface_support = contract_165.functions.supportsInterface(interface) \
                .call(block_identifier=block_number)
        except (BadFunctionCallOutput, ContractLogicError) :
            contract_interface_support = False
        return contract_interface_support

    # https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md
    # https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/token/ERC20/ERC20.sol
    def is_erc20_contract(self, contract_address, function_sighashes, block_number='latest'):
        c = ContractWrapper(function_sighashes)
        support_interface_20 = (
            c.implements("supportsInterface(bytes4)")
            and self.contract_interface_support(contract_address, block_number, ERC20_INTERFACE)
        )

        return support_interface_20 or (
            c.implements("totalSupply()")
            and c.implements("balanceOf(address)")
            and c.implements("transfer(address,uint256)")
            and c.implements("transferFrom(address,address,uint256)")
            and c.implements("approve(address,uint256)")
            and c.implements("allowance(address,address)")
        )

    # https://github.com/ethereum/EIPs/blob/master/EIPS/eip-721.md
    # https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/token/ERC721/ERC721Basic.sol
    # Doesn't check the below ERC721 methods to match CryptoKitties contract
    # getApproved(uint256)
    # setApprovalForAll(address,bool)
    # isApprovedForAll(address,address)
    # transferFrom(address,address,uint256)
    # safeTransferFrom(address,address,uint256)
    # safeTransferFrom(address,address,uint256,bytes)
    def is_erc721_contract(self, contract_address, function_sighashes, block_number='latest'):
        c = ContractWrapper(function_sighashes)
        support_interface_721 = (
                c.implements("supportsInterface(bytes4)")
                and self.contract_interface_support(contract_address, block_number, ERC721_INTERFACE)
        )

        return support_interface_721 or (
            c.implements("balanceOf(address)")
            and c.implements("ownerOf(uint256)")
            and c.implements_any_of(
                "transfer(address,uint256)", "transferFrom(address,address,uint256)"
            )
            and c.implements("approve(address,uint256)")
        )

    # https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1155.md
    # https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC1155/ERC1155.sol
    def is_erc1155_contract(self, contract_address, function_sighashes, block_number='latest'):
        c = ContractWrapper(function_sighashes)
        support_interface_1155 = (
                c.implements("supportsInterface(bytes4)")
                and self.contract_interface_support(contract_address, block_number, ERC1155_INTERFACE)
        )

        return support_interface_1155 or (
            c.implements("balanceOf(address, uint256)")
            and c.implements("balanceOfBatch(address[],uint256[])")
            and c.implements("setApprovalForAll(address, bool)")
            and c.implements("isApprovedForAll(address,address)")
            and c.implements("safeTransferFrom(address,address,uint256,uint256,bytes)")
            and c.implements(
                "safeBatchTransferFrom(address,address,uint256[],uint256[],bytes)"
            )
        )


def clean_bytecode(bytecode):
    if bytecode is None or bytecode == "0x":
        return None
    elif bytecode.startswith("0x"):
        return bytecode[2:]
    else:
        return bytecode


def get_function_sighash(signature):
    return "0x" + function_signature_to_4byte_selector(signature).hex()


class ContractWrapper:
    def __init__(self, sighashes):
        self.sighashes = sighashes

    def implements(self, function_signature):
        sighash = get_function_sighash(function_signature)
        return sighash in self.sighashes

    def implements_any_of(self, *function_signatures):
        return any(
            self.implements(function_signature)
            for function_signature in function_signatures
        )
