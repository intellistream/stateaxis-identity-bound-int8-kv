# Evidence index

Version `0.2.0` is active experimental and not performance-qualified. Its
active mechanism binds the rejected INT8 KV schema into the managed assembly
and audits eligible write volume and projected bytes while BF16 KV remains
authoritative.

- `evidence/ISSUE14_INT8_KV_CLOSURE.md` preserves the real-NPU component
  positive and full-model accuracy-negative result.
- `evidence/historical-real-npu-accuracy-gate/` contains the four frozen
  real-NPU audit records, three preregistrations, and a repo-local SHA-256
  manifest. It makes the accuracy stop decision independently verifiable.
- `evidence/on-off-preflight-20261010/RESULT.json` preserves the earlier inert
  activation rejection and is not an ON/OFF result.
- `evidence/ecpa-contract-20261011/` records the hash-bound Manager/host audit
  contract and deterministic ON/OFF effect counters; it is non-performance
  evidence.

The historical component reduced KV bytes by about 50% and improved component
P50 by 5.7574%, but every tested layer range failed exact greedy parity. Those
figures do not authorize serving, capacity, latency, or throughput claims.
Matched online ON/OFF was not run because exact greedy parity is an advance
gate, not because performance data was silently omitted.
