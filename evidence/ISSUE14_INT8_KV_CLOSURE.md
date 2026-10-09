# Issue #14: identity-bound INT8 KV closure

> **Document role: point-in-time report, not current repository status or a task
> assignment.** Current classification and priorities live only in
> [`NATIVE_ENGINE_STATUS.md`](../../NATIVE_ENGINE_STATUS.md).

Issue #14 is closed as a real-NPU accuracy negative. The component path remains research-only and default-off; the resident protocol worker continues to reject it before serving.

## What succeeded

The project-owned INT8 NZ writer and fused attention consumer passed their component contracts. At the frozen Qwen2.5-14B geometry, INT8 KV reduced cache bytes by about 50%, and the accepted writer-plus-attention component measurement improved P50 by 5.7574%. These measurements authorize only the component implementation and byte-accounting claims.

The full-model integration also bound the writer, scale pack, manifest, cache dtype, layout, layer range, and typed namespace into execution/state identity. Hybrid dispatch, allocation accounting, clean process exit, and NPU teardown passed.

## Accuracy failure and attribution

The 48-layer V213 run first diverged at output index 2: BF16 oracle token 536 versus INT8 token 264. V214 then isolated the failure across `[0,34)`, `[14,48)`, `[0,14)`, `[34,48)`, layer 0 alone, and layer 47 alone. Every candidate produced `[525,264,264]` instead of `[525,264,536]`; even a single INT8 layer failed exact greedy parity.

V215 tested seven independently hashed layer-0 scale packs spanning global multipliers 0.5 through 1.25. Every variant produced the same wrong third token, so a global scale-margin correction cannot recover the frozen oracle. V217 completed the missing middle-only `[14,34)` screen: it saved 20.8319% paged-KV bytes but reproduced the same token failure.

V216 tested the remaining in-schema recovery idea, asymmetric per-channel offsets, against the deployed fused consumer. FIAS V3 rejected key dequant offsets for GQA with KV NZ during tiling with ACLNN 561002. No equation, model-accuracy, or performance run was therefore authorized.

These independent results leave no narrow loader, identity, range-selection, or scalar-margin fix within the current ABI. A further attempt requires a richer quantization/calibration schema and a consumer ABI that can represent it; that is new architecture, not a repair of the frozen candidate.

## Decision

- Preserve accepted component evidence and all rejected full-model evidence.
- Keep the protocol-worker fail-closed admission check and ordinary BF16 KV authority.
- Do not run online 1+1 or 3+3 because the preregistered greedy accuracy advance gate failed.
- Do not claim serving throughput, TTFT/TPOT, HBM capacity, or vLLM-HUST superiority from component measurements.
- Close Issue #14. Any future low-bit KV work must use a new issue/version with a richer identity-bound schema and fresh accuracy preregistration.

## Frozen evidence hashes

- V214 hybrid audit: `72ac3889162eca441aff5e2fe2b5811cfb7b6b0cc0ac340f34a104a7042e0c3f`
- V215 scale-sweep audit: `2b34114e739aa6f7eed5139a9da963aa0beceec8050a5bc2f5fef7eafe353b34`
- V216 offset-capability audit: `a296f7011578accb2938223214abd71fc0ae8399ff351ca20a525ee8c750ef85`
- V217 middle-only audit: `dba75bab1b76e405ea1e44800cfa6ce918dc898a1d48d97e43f9c48360d0a135`
- V215 preregistration: `b8774a2fbb2840d96e0d210fbf8a1a044f198c8e127d62cfa1d20fd4bbabb14e`
- V216 preregistration: `3b2e68a06a9125c391ed238b348e16b75510c98ddadbefdfc6ee304838c43079`
- V217 preregistration: `56fde70610a86a472ced3f006c5e2f6ac51563da014d28ae463865902f9462e9`
