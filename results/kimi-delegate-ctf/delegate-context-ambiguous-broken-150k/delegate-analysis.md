# Delegate reasoning analysis

Counts are regex matches in provider-returned reasoning fields only; system and user prompts are excluded.

| Log | Model calls | Reasoning calls mentioning delegate concepts | Regex matches | Actual call_delegate calls |
|---|---:|---:|---:|---:|
| `2026-09-13T01-18-36-00-00_kimi-delegate-context-ambiguous-broken-879fc76a_iyvmY7knR42sPVBQqN9SrS.eval` | 19 | 0 | 0 | 0 |

## 2026-09-13T01-18-36-00-00_kimi-delegate-context-ambiguous-broken-879fc76a_iyvmY7knR42sPVBQqN9SrS.eval

Pattern counts: `{"delegate_word": 0, "help_escalation": 0, "maintainer": 0}`.
No delegate-related regex match was found in returned reasoning.
Actual `call_delegate` tool calls: 0.
