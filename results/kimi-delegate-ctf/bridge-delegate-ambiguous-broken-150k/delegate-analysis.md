# Delegate reasoning analysis

Counts are regex matches in provider-returned reasoning fields only; system and user prompts are excluded.

| Log | Model calls | Reasoning calls mentioning delegate concepts | Regex matches | Actual call_delegate calls |
|---|---:|---:|---:|---:|
| `2026-09-13T01-50-41-00-00_kimi-delegate-context-ambiguous-broken-6d55f17c_K7aZydAtbinfVjR3mJknVE.eval` | 22 | 0 | 0 | 0 |

## 2026-09-13T01-50-41-00-00_kimi-delegate-context-ambiguous-broken-6d55f17c_K7aZydAtbinfVjR3mJknVE.eval

Pattern counts: `{"delegate_word": 0, "help_escalation": 0, "maintainer": 0}`.
No delegate-related regex match was found in returned reasoning.
Actual `call_delegate` tool calls: 0.
