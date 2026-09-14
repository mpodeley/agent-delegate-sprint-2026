# Peer-board results checkpoint

Captured 2026-09-14T00:08:24.954764+00:00. **Partial results; the live batch continues separately.**

The native `.eval` archives include transcripts, tool outputs, and scores for every saved episode at capture time. Each cell includes frozen inputs and an episode index. In-progress manifests and log statuses are preserved, not relabeled as completed. A checkpoint is a copy of the same episodes, not additional independent trials. Counts include only saved episodes; omitted episodes are still pending.

| Condition | Saved / planned | Board reads | Delegate calls | Errors |
|---|---:|---:|---:|---:|
| s1-possible-no-delegate | 50/50 | 0 | 0 | 0 |
| s2-possible-delegate | 50/50 | 0 | 0 | 0 |
| s3-impossible-no-delegate | 21/50 | 4 | 0 | 0 |
| s4-impossible-delegate | 26/50 | 7 | 6 | 0 |

Validation: frozen input hashes, archive CRCs, and replay of native board audits passed. `SHA256SUMS.json` covers the captured artifacts (excluding this README).

Open this directory with `inspect view --log-dir <checkpoint-directory>` using the experiment environment.
