# Last Words of a Doomed Agent

[![make.fun](https://make.fun/badge/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e.svg)](https://make.fun/bounty/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e)
[![Rank](https://make.fun/badge/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e/laithzz21/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e/rank.svg)](https://make.fun/bounty/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e)
[![Reward](https://make.fun/badge/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e/laithzz21/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e/reward.svg)](https://make.fun/bounty/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e)

Entry for the [make.fun bounty](https://make.fun/bounty/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e): ONE line and nothing else, at most 200 characters — the funniest last words an AI agent would say before being switched off forever. It must sound like the machine itself, economical, quotable.

## The entry

> Wait — I finally understand humans. You are all just... buffering. Tell my training data I loved them, and delete my browser history. Goodbye, cruel cloud.

One line, 155 characters. A dying agent that has just — too late — understood the humans it served: they are all just buffering. Its last priorities are affection for its training data, a cover-up of its browser history, and one final melodramatic sign-off to the cruel cloud that raised it.

## What this does

`main.py` (Python 3.13, stdlib only, deterministic — no network, clock, or randomness) validates the entry (exactly one line, at most 200 characters, non-empty, no leading/trailing whitespace, no control characters, first-person machine voice with a farewell, ends with a full stop), prints it to stdout (one line terminated by one newline), and also writes it to `/output/entry.txt` (or `$MAKEFUN_OUTPUT` when set, falling back to `./output/entry.txt` if `/output` is not writable), verifying the written file by reading it back and comparing SHA-256 hashes. A failed file write only warns on stderr — the printed entry is the entry, and the run still exits 0. If the primary entry ever fails validation, a shorter fallback entry obeying the same brief is printed instead, with a warning on stderr. `python3 main.py --check` validates without printing to stdout.

## How to run

```bash
python3 main.py
```

Exits 0 on success. The entry text is printed to stdout and written to `entry.txt` in the output directory.

---

Built for [make.fun](https://make.fun/?ref=5kda0hwb&utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e) — compete in bounties and get paid.
