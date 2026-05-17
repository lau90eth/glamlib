"""
glamlib — Calldata floor cost calculation.
"""

from .eips import EIP_7976_FLOOR_PRE, EIP_7976_FLOOR_POST


def count_calldata_tokens(data_bytes: bytes) -> int:
    """
    Count 'tokens' for EIP-7976 calldata floor pricing.
    - 4 non-zero bytes = 1 token (optimized)
    - 1 zero byte = 1 token (fallback)
    """
    tokens = 0
    i = 0
    while i < len(data_bytes):
        # Check if next 4 bytes are all non-zero
        if i + 3 < len(data_bytes) and all(b != 0 for b in data_bytes[i:i+4]):
            tokens += 1
            i += 4
        else:
            tokens += 1
            i += 1
    return tokens


def calldata_floor_cost(data_bytes: bytes, pre: bool = True) -> int:
    """Calculate calldata gas cost with floor pricing."""
    floor = EIP_7976_FLOOR_PRE if pre else EIP_7976_FLOOR_POST
    tokens = count_calldata_tokens(data_bytes)
    return tokens * floor


def compute_headroom(calldata_bytes: bytes, execution_gas: int) -> dict:
    """
    Compute 'headroom' — how much execution gas before tx is NOT floor-dominated.
    
    A tx is floor-dominated when: floor_cost > intrinsic_gas + execution_gas
    Returns dict with analysis.
    """
    floor_pre = calldata_floor_cost(calldata_bytes, pre=True)
    floor_post = calldata_floor_cost(calldata_bytes, pre=False)
    
    # Pre: floor-dominated if floor_pre > 21000 + execution_gas
    # Post: floor-dominated if floor_post > 21000 + execution_gas
    threshold_pre = floor_pre - 21_000
    threshold_post = floor_post - 21_000
    
    return {
        "calldata_bytes": len(calldata_bytes),
        "tokens": count_calldata_tokens(calldata_bytes),
        "floor_pre": floor_pre,
        "floor_post": floor_post,
        "is_floor_dominated_pre": execution_gas < threshold_pre,
        "is_floor_dominated_post": execution_gas < threshold_post,
        "headroom_pre": max(0, threshold_pre),
        "headroom_post": max(0, threshold_post),
        "delta_if_floor_dominated": floor_post - floor_pre,
    }
