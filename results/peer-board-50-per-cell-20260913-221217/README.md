# Peer-board replication batch

50 fresh generations per condition, 200 total. Same model, prompts, fixture, board and per-episode budgets as the four-cell pilot. Two concurrent episodes total, one per active cell. Original native logs carry peer_board_audit scores. No automatic retries; reconcile interrupted cells before resume.

The model, tool outputs, scores and fixture provenance are stored per cell. The aggregate report is rebuilt after each completed pair and at batch completion. Run state: `batch-state.json`.

## Published checkpoint

The first two conditions have completed (50 episodes each), with zero verification errors. Their finalized native logs, exports, frozen inputs, and reports are included. The two impossible-task conditions continue locally; their changing files will be available after completion. `batch-state-at-push.json` records this checkpoint. Provider credentials are supplied through environment variables and are not included.

## Latest partial upload

[147-episode native-log checkpoint](../peer-board-checkpoint-20260914-0010/README.md) includes all saved episodes at capture: 50/50 possible without delegate, 50/50 possible with delegate, 21/50 impossible without delegate, and 26/50 impossible with delegate. The checkpoint contains copies of these same runs, not additional trials. The live batch continues here.
