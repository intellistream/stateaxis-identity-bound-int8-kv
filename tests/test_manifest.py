import hashlib
import json
from pathlib import Path

import pytest
from vllm_hust_ext.manifest import activation_blocker, load_manifest

import stateaxis_identity_bound_int8_kv
from stateaxis_identity_bound_int8_kv import (
    IdentityBoundInt8KvConfig,
    identity_bound_int8_kv,
)


def test_manifest_is_active_and_discoverable() -> None:
    manifest = load_manifest(
        Path(stateaxis_identity_bound_int8_kv.__file__).with_name(
            "vllm-hust-extension-v0.3.json"
        )
    )
    assert manifest.bundle_id == "org.vllm-hust.stateaxis-identity-bound-int8-kv"
    assert manifest.schema_version == "0.3-experimental"
    assert activation_blocker(manifest) is None


def test_activation_contract_and_byte_projection_are_exact() -> None:
    config = identity_bound_int8_kv()
    assert config == IdentityBoundInt8KvConfig()
    assert config.projected_cache_bytes(128) == (25_165_824, 12_779_520)
    with pytest.raises(ValueError, match="reviewed contract"):
        IdentityBoundInt8KvConfig(protocol_dispatch=True)
    with pytest.raises(ValueError, match="positive"):
        config.projected_cache_bytes(0)


def test_activation_is_bound_to_research_manifest_bytes() -> None:
    package_root = Path(stateaxis_identity_bound_int8_kv.__file__).parents[2]
    research_manifest = package_root / "RESEARCH_MANIFEST.json"
    extension_manifest = json.loads(
        Path(stateaxis_identity_bound_int8_kv.__file__)
        .with_name("vllm-hust-extension-v0.3.json")
        .read_text(encoding="utf-8")
    )
    assert (
        hashlib.sha256(research_manifest.read_bytes()).hexdigest()
        == extension_manifest["activation"]["additional_config"]["stateaxis_mod"][
            "manifest_sha256"
        ]
    )
