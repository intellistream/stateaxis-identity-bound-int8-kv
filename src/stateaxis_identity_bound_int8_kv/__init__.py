"""Exact activation contract for identity-bound INT8 KV eligibility audit."""

from __future__ import annotations

from dataclasses import asdict, dataclass

MOD_ID = "org.vllm-hust.stateaxis-identity-bound-int8-kv"


@dataclass(frozen=True, slots=True)
class IdentityBoundInt8KvConfig:
    """The sole research contract accepted by the StateAxis host."""

    enabled: bool = True
    audit_only: bool = True
    control_cache_dtype: str = "bf16"
    candidate_cache_dtype: str = "int8"
    layout: str = "NZ-5D"
    scale_schema: str = "symmetric-per-layer-per-channel-bf16-v1"
    rounding: str = "nearest-even"
    clamp_min: int = -127
    clamp_max: int = 127
    zero_point: str = "none"
    layers: int = 48
    kv_heads: int = 8
    head_dim: int = 128
    block_tokens: int = 128
    max_batch: int = 32
    accuracy_qualified: bool = False
    protocol_dispatch: bool = False
    fallback_to_bf16: bool = True
    fail_closed: bool = True

    def __post_init__(self) -> None:
        expected = {
            "enabled": True,
            "audit_only": True,
            "control_cache_dtype": "bf16",
            "candidate_cache_dtype": "int8",
            "layout": "NZ-5D",
            "scale_schema": "symmetric-per-layer-per-channel-bf16-v1",
            "rounding": "nearest-even",
            "clamp_min": -127,
            "clamp_max": 127,
            "zero_point": "none",
            "layers": 48,
            "kv_heads": 8,
            "head_dim": 128,
            "block_tokens": 128,
            "max_batch": 32,
            "accuracy_qualified": False,
            "protocol_dispatch": False,
            "fallback_to_bf16": True,
            "fail_closed": True,
        }
        if asdict(self) != expected:
            raise ValueError("identity-bound INT8 KV requires the reviewed contract")

    def projected_cache_bytes(self, tokens: int) -> tuple[int, int]:
        """Return BF16 and INT8+scale bytes for one independent state."""

        if tokens <= 0:
            raise ValueError("tokens must be positive")
        elements = tokens * self.layers * 2 * self.kv_heads * self.head_dim
        scale_elements = self.layers * 2 * self.kv_heads * self.head_dim
        return elements * 2, elements + scale_elements * 2


def identity_bound_int8_kv() -> IdentityBoundInt8KvConfig:
    """Return the default-off audit candidate's admitted ON configuration."""

    return IdentityBoundInt8KvConfig()


__all__ = [
    "MOD_ID",
    "IdentityBoundInt8KvConfig",
    "identity_bound_int8_kv",
]
