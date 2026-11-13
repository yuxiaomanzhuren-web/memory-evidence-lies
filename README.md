[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24197495.svg)](https://doi.org/10.5281/zenodo.24197495)

# Where Memory Systems Lie — failure cases for evidence-grounded recall

This repository collects **real failure cases** observed in a long-running personal memory system (raw-dialogue store → extracted memories → gate checks → prompt injection → outgoing reply check).

It is not a model and not a benchmark. It is a **failure taxonomy plus a contract**, published early because the same mistakes are easy to repeat and hard to notice.

Every case here was observed in production, on real data, with the failure reproduced at least once. Personal content has been rewritten; the structure, labels and error shapes are preserved.

## The one-paragraph summary

An assistant that remembers must be able to answer three different questions separately:

1. **Did I look?** (`not_checked` vs. everything else)
2. **What did I find, and how strong is it?** (`found` / `suspected` / `absent`)
3. **Is what I just said backed by what I actually had in context?**

Most systems collapse (1) into (3), and (3) into "the model sounds confident". That collapse is where the lies come from.

## Cases

See [`docs/failure-taxonomy.md`](docs/failure-taxonomy.md) and the machine-readable [`cases/cases.jsonl`](cases/cases.jsonl).

| # | Case | Symptom |
|---|---|---|
| 1 | Quoted document treated as first-person claim | `found`, evidence is a pasted file |
| 2 | The question itself used as evidence | `found`, evidence is the sentence being asked |
| 3 | Assistant's own reply used as evidence | `found`, evidence is what the assistant said |
| 4 | One matching citation excuses the whole message | fabricated sentence shipped alongside a real quote |
| 5 | "Not checked" reported as "checked, nothing there" | `absent` used as a claim of search |
| 6 | Trigger too narrow: question never inspected | 4 of 5 natural questions returned `not_checked` |
| 7 | Fallback sentence attributed to the assistant | a canned line posted as if it were her words |
| 8 | Fallback silently mutes the rest of the turn | `ok: true, sent: 0`, no error |
| 9 | Statement mistaken for a question about the past | statement triggers a history lookup |
| 10 | Cost already settled keeps firing | resolved item still blocks/allows as if unresolved |

## The contract we ended up with

See [`docs/four-states.md`](docs/four-states.md).

- Four states, not three: `not_checked` / `found` / `suspected` / `absent`.
- `not_checked` is a **different kind of answer** from `absent` and must never be rendered as "I looked and there was nothing".
- Every check records `trigger_reason` (`time_word` / `memory_question` / `object_hit`) so a miss can be told apart from a non-trigger.
- Outgoing text is checked against the **frozen allowlist of what was actually in context** — injected memories *and* the current conversation — never against "does it exist somewhere in the database".

## What is deliberately *not* claimed here

- No accuracy numbers. This repo contains failure cases, not results.
- No claim of novelty for the individual pieces: graded belief, bi-temporal edges, citation verification and stance checks all exist in the literature. What is offered here is the **observed failure set** and a **separation contract**, not a new algorithm.
- No claim that these cases are exhaustive.

## License

Apache-2.0 (see `LICENSE`). Use the cases; if you ship a memory system, please add them to your regression suite.
