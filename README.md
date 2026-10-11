# stateaxis-identity-bound-int8-kv

Extension ID: `org.vllm-hust.stateaxis-identity-bound-int8-kv`

Identity-bound eligibility and byte-accounting audit for the Qwen2.5-14B INT8
NZ-5D KV candidate split from StateAxis issue #14.

Version `0.2.0` is Manifest 0.3 active experimental, default-off, and can only
be enabled through vLLM-HUST Extension Manager/ECPA. It binds the exact cache
dtype, layout, scale schema, rounding, clamp, geometry, and accuracy status into
the StateAxis assembly. The host counts candidate KV writes and projected BF16
versus INT8-plus-scale bytes.

The revision is deliberately `audit_only`: BF16 KV remains authoritative and
the historical INT8 device consumer is not dispatched. The frozen component
reduced cache bytes by about 50% and improved component P50 by 5.7574%, but
every tested full-model layer range failed exact greedy token parity, including
a one-layer candidate. Projected bytes are not measured HBM or capacity gains.

## Install and validate

```bash
python -m pip install -e '.[test]'
pytest -q
vllm-hust-ext extension inspect org.vllm-hust.stateaxis-identity-bound-int8-kv
VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261011/manager-config.json \
  vllm-hust-ext extension check org.vllm-hust.stateaxis-identity-bound-int8-kv
VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261011/manager-config.json \
  vllm-hust-ext run --dry-run -- /bin/true
```

Omitting the MOD is the OFF arm and leaves StateAxis unchanged. A future device
revision requires a richer supported consumer schema and fresh preregistered
accuracy gates before matched serving performance tests are authorized.

Maintainer: Shuhao Zhang (Tony), directly responsible; no advisor is declared.
