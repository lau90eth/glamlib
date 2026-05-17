"""
glamlib — Ethereum EIP constants for Glamsterdam upgrade.
Single source of truth for EIP-7976 and EIP-8037 parameters.
"""

# EIP-7976 — Increase Calldata Floor Cost
# Source: https://eips.ethereum.org/EIPS/eip-7976
# TOTAL_COST_FLOOR_PER_TOKEN (not gas/byte)
EIP_7976_FLOOR_PRE = 10    # EIP-7623: 10 gas per token
EIP_7976_FLOOR_POST = 16   # EIP-7976: 16 gas per token (64/64 = 16 per token)

# Standard token cost (gas per byte, immutato)
STANDARD_TOKEN_COST = 4    # 4 gas per byte standard


# EIP-8037 — State Creation Gas Cost Increase
# Source: https://eips.ethereum.org/EIPS/eip-8037
CPSB = 1530  # cost per state byte

# State bytes per operation
STATE_BYTES_NEW_ACCOUNT = 120
STATE_BYTES_SSTORE_INIT = 64
STATE_BYTES_PER_CODE_BYTE = 1  # each code byte costs CPSB

# Derived costs
COST_NEW_ACCOUNT_PRE = 25_000
COST_NEW_ACCOUNT_POST = STATE_BYTES_NEW_ACCOUNT * CPSB  # 183,600

COST_SSTORE_INIT_PRE = 20_000
COST_SSTORE_INIT_POST = STATE_BYTES_SSTORE_INIT * CPSB   # 97,920

COST_CODE_BYTE_PRE = 200
COST_CODE_BYTE_POST = CPSB  # 1,530


def get_eip_7976_floor(pre: bool = True) -> int:
    """Get calldata floor gas per token."""
    return EIP_7976_FLOOR_PRE if pre else EIP_7976_FLOOR_POST
