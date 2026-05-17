"""
glamlib — Ethereum EIP constants for Glamsterdam upgrade.
Single source of truth for EIP-7976 and EIP-8037 parameters.
"""

# EIP-7976 — Increase Calldata Floor Cost
# Source: https://eips.ethereum.org/EIPS/eip-7976
EIP_7976_FLOOR_PRE = 10   # gas per token pre-Glamsterdam
EIP_7976_FLOOR_POST = 64  # gas per token post-Glamsterdam

# Token definition: 4 nonzero bytes = 1 token, OR 1 zero byte = 1 token
# Practical: floor applies when execution gas is low


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


def get_state_creation_cost(operation: str, pre: bool = True) -> int:
    """Get state creation cost for operation type."""
    costs = {
        "new_account": (COST_NEW_ACCOUNT_PRE, COST_NEW_ACCOUNT_POST),
        "sstore_init": (COST_SSTORE_INIT_PRE, COST_SSTORE_INIT_POST),
        "code_byte": (COST_CODE_BYTE_PRE, COST_CODE_BYTE_POST),
    }
    pre_cost, post_cost = costs.get(operation, (0, 0))
    return pre_cost if pre else post_cost
