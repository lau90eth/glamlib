# glamlib

Ethereum Glamsterdam upgrade constants and calculators. Single source of truth for EIP-7623 / EIP-7976 / EIP-8037 parameters.

## Install

```bash
pip install git+https://github.com/lau90eth/glamlib.git
```

## Use

```python
from glamlib.eips import EIP_7976_FLOOR_PRE, EIP_7976_FLOOR_POST
from glamlib.calldata import count_calldata_tokens, calldata_floor_cost
```

## Spec sources

- EIP-7623: https://eips.ethereum.org/EIPS/eip-7623
- EIP-7976: https://eips.ethereum.org/EIPS/eip-7976
- EIP-8037: https://eips.ethereum.org/EIPS/eip-8037

MIT License.
