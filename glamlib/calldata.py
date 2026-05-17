"""
glamlib — Calldata floor cost calculation.
"""

from .eips import EIP_7976_FLOOR_PRE, EIP_7976_FLOOR_POST, STANDARD_TOKEN_COST


def count_calldata_tokens(data_bytes: bytes) -> int:
    """
    EIP-7623 token counting:
    tokens = zero_bytes + nonzero_bytes * 4
    """
    zero = sum(1 for b in data_bytes if b == 0)
    nonzero = len(data_bytes) - zero
    return zero + nonzero * 4


def calldata_floor_cost(data_bytes: bytes, pre: bool = True) -> int:
    """Calculate calldata gas cost with floor pricing."""
    floor = EIP_7976_FLOOR_PRE if pre else EIP_7976_FLOOR_POST
    tokens = count_calldata_tokens(data_bytes)
    return tokens * floor


def compute_headroom(data_bytes: bytes) -> dict:
    """
    Compute headroom — execution gas needed to NOT be floor-dominated.
    
    Formula: headroom = (FLOOR_PER_TOKEN - STANDARD_TOKEN_COST) * tokens
    """
    tokens = count_calldata_tokens(data_bytes)
    
    floor_pre = EIP_7976_FLOOR_PRE * tokens
    floor_post = EIP_7976_FLOOR_POST * tokens
    standard_cost = STANDARD_TOKEN_COST * tokens
    
    headroom_pre = max(0, floor_pre - standard_cost)
    headroom_post = max(0, floor_post - standard_cost)
    
    return {
        "calldata_bytes": len(data_bytes),
        "tokens": tokens,
        "standard_cost": standard_cost,
        "floor_pre": floor_pre,
        "floor_post": floor_post,
        "headroom_pre": headroom_pre,
        "headroom_post": headroom_post,
    }
