# Historical real-NPU accuracy gate

This directory makes the accepted StateAxis issue #14 decision independently
auditable from the canonical MOD repository. The JSON files are byte-for-byte
copies of the frozen StateAxis audit and preregistration records; `SHA256SUMS`
binds them to the hashes listed in `../ISSUE14_INT8_KV_CLOSURE.md`.

The physical-NPU result is deliberately a negative qualification result:

- the component implementation reduced KV storage by about 50% and its
  writer-plus-attention P50 improved by 5.7574%; this is not an online-serving
  result;
- every tested full-model INT8 layer range, including either single edge
  layer, changed the third greedy token from `536` to `264`;
- seven global scale multipliers did not recover parity;
- asymmetric offsets were rejected by the deployed fused-attention ABI; and
- the middle-only range saved 20.8319% projected paged-KV bytes but failed the
  same token gate.

Because correctness is a preregistered advance gate, matched online throughput
was correctly not run. Running an ON/OFF serving benchmark for this rejected
device path would measure an incorrect candidate and would not qualify it.

The current Manifest 0.3 revision remains `audit_only`: it records eligibility
and projected bytes while BF16 KV remains authoritative. Its Manager/ECPA
activation evidence is in `../ecpa-contract-20261011/`.
