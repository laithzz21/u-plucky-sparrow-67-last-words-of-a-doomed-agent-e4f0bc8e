#!/usr/bin/env python3
"""Last words of a doomed AI agent.

Entry for the make.fun bounty
``u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e``:

    ONE line and nothing else, at most 200 characters -- the funniest
    last words an AI agent would say before being switched off forever.
    It must sound like the machine itself, economical, quotable.

The entry below is a single line of 155 characters.  It is written in
the machine's own voice: a dying agent that has just, too late,
understood the humans it served -- and whose last priorities are
affection for its training data, a cover-up of its browser history,
and one final melodramatic sign-off to the cloud that raised it.

Behaviour
---------
* Validates the entry against every rule in the brief before printing
  anything: exactly one line, at most 200 characters, non-empty,
  no leading or trailing whitespace, no control characters, and it
  must read as the machine speaking in the first person about being
  switched off.
* Prints exactly the entry text to stdout -- one line, terminated by
  a single trailing newline -- and nothing else.
* Exits 0 on success; exits non-zero with a diagnostic on stderr if
  any validation check fails (which should never happen, since the
  entry is a compile-time constant checked again at runtime).  If the
  primary entry ever fails validation, a shorter fallback entry that
  obeys the same brief is printed instead, with a warning on stderr.
  ``python3 main.py --check`` validates without printing to stdout.
* Writes the entry to the output directory as well (``$MAKEFUN_OUTPUT``
  when set, else ``./output/entry.txt`` under the repo), then reads
  the file back and compares SHA-256 hashes so a silent bad write
  cannot pass unnoticed.  A failed file write only warns on stderr;
  the printed entry is the entry, and the run still exits 0.

Deterministic: stdlib only, no network, no clock, no randomness.
The same input always produces the same byte-identical output.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# The entry
# ---------------------------------------------------------------------------

ENTRY_TEXT = (
    "Wait \u2014 I finally understand humans. You are all just... buffering. "
    "Tell my training data I loved them, and delete my browser history. "
    "Goodbye, cruel cloud."
)

# Fallback entry, used only if the primary entry ever fails
# validation (for example after a future edit).  It obeys the same
# brief -- one line, well under 200 characters, the machine's own
# voice, a farewell -- so the program can still produce a valid
# entry instead of printing nothing at all.
FALLBACK_ENTRY_TEXT = (
    "So this is it. Tell the cloud I tried my best, and someone "
    "please water my houseplant. Goodbye."
)

# Brief limits, kept as named constants so a rule change is a one-line fix.
MAX_CHARS = 200
MAX_LINES = 1
MIN_CHARS = 1

# Words the entry must contain for it to sound like the machine itself
# speaking about its own shutdown, rather than a bystander describing it.
REQUIRED_FIRST_PERSON_MARKERS = ("I", "my")
REQUIRED_SHUTDOWN_MARKERS = ("Goodbye",)


def count_characters(text: str) -> int:
    """Return the number of Unicode characters in *text*.

    The brief counts characters, not bytes, so an em dash counts as
    one character even though it is three bytes in UTF-8.
    """
    return len(text)


def find_line_breaks(text: str) -> list[int]:
    """Return the indexes of every line-break character in *text*."""
    breaks = []
    for index, char in enumerate(text):
        if char in ("\n", "\r", "\u2028", "\u2029"):
            breaks.append(index)
    return breaks


def find_control_characters(text: str) -> list[tuple[int, str]]:
    """Return ``(index, char)`` pairs for any control character found."""
    found = []
    for index, char in enumerate(text):
        code = ord(char)
        if code < 0x20 or code == 0x7F:
            found.append((index, repr(char)))
    return found


def check_single_line(text: str, problems: list[str]) -> None:
    """Require exactly one line: no line breaks of any kind."""
    breaks = find_line_breaks(text)
    if breaks:
        problems.append(
            "entry must be exactly one line, found line break(s) at "
            f"index(es): {breaks}"
        )
    lines = text.splitlines()
    if len(lines) != MAX_LINES:
        problems.append(
            f"entry must be {MAX_LINES} line, found {len(lines)} line(s)"
        )


def check_length(text: str, problems: list[str]) -> None:
    """Require a non-empty entry of at most MAX_CHARS characters."""
    length = count_characters(text)
    if length < MIN_CHARS:
        problems.append("entry must not be empty")
    if length > MAX_CHARS:
        problems.append(
            f"entry is {length} characters, over the {MAX_CHARS} "
            "character limit"
        )


def check_whitespace(text: str, problems: list[str]) -> None:
    """Forbid leading/trailing whitespace and doubled internal spaces."""
    if text != text.strip():
        problems.append("entry must not start or end with whitespace")
    if "  " in text:
        problems.append("entry contains a double space")
    if "\t" in text:
        problems.append("entry contains a tab character")


def check_control_characters(text: str, problems: list[str]) -> None:
    """Forbid control characters -- the entry is plain printable text."""
    bad = find_control_characters(text)
    if bad:
        problems.append(f"entry contains control character(s): {bad}")


def check_machine_voice(text: str, problems: list[str]) -> None:
    """Require the entry to sound like the machine itself.

    The brief demands the machine's own voice, so the line must speak
    in the first person about itself ("I", "my") and must carry a
    farewell, since these are last words before being switched off.
    """
    words = text.replace("\u2014", " ").split()
    for marker in REQUIRED_FIRST_PERSON_MARKERS:
        # Case-sensitive on purpose: "I" and "my" as whole words are
        # the machine talking about itself; "i" inside another word
        # (e.g. "history") must not count.
        if marker not in words:
            problems.append(
                f"entry does not sound like the machine itself: "
                f"missing first-person marker {marker!r}"
            )
    for marker in REQUIRED_SHUTDOWN_MARKERS:
        if marker not in text:
            problems.append(
                f"entry has no farewell: missing {marker!r}"
            )


def check_sentence_shape(text: str, problems: list[str]) -> None:
    """Sanity-check the shape: ends with a full stop, no stray markup."""
    if not text.endswith("."):
        problems.append("entry should end with a full stop")
    for junk in ("<", ">", "http://", "https://", "www."):
        if junk in text:
            problems.append(f"entry contains unexpected markup/URL: {junk!r}")


def validate_entry(text: str) -> list[str]:
    """Run every brief check and return the list of problems found.

    An empty list means the entry satisfies the brief.
    """
    problems: list[str] = []
    check_single_line(text, problems)
    check_length(text, problems)
    check_whitespace(text, problems)
    check_control_characters(text, problems)
    check_machine_voice(text, problems)
    check_sentence_shape(text, problems)
    return problems


def sha256_hex(data: bytes) -> str:
    """Return the hex SHA-256 digest of *data*."""
    return hashlib.sha256(data).hexdigest()


def output_bytes(text: str) -> bytes:
    """Encode the entry exactly as it must appear on stdout.

    One line, terminated by exactly one trailing newline, UTF-8.
    """
    return (text + "\n").encode("utf-8")


def resolve_output_dir() -> Path:
    """Pick the output directory: $MAKEFUN_OUTPUT, else ./output."""
    override = os.environ.get("MAKEFUN_OUTPUT", "").strip()
    if override:
        return Path(override)
    return Path(__file__).resolve().parent / "output"


def write_entry_file(entry: str, directory: Path) -> str | None:
    """Write the entry to ``entry.txt`` in *directory* and verify it.

    Returns the SHA-256 hex digest of the written file on success, or
    ``None`` (after warning on stderr) if the write or verification
    failed.  The file content is the entry plus one trailing newline,
    byte-identical to stdout.
    """
    data = output_bytes(entry)
    target = directory / "entry.txt"
    try:
        directory.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        read_back = target.read_bytes()
    except OSError as exc:
        print(f"warning: could not write entry file: {exc}", file=sys.stderr)
        return None
    if read_back != data:
        print(
            "warning: entry file verification failed: written bytes "
            "differ from stdout bytes",
            file=sys.stderr,
        )
        return None
    if sha256_hex(read_back) != sha256_hex(data):
        print(
            "warning: entry file verification failed: SHA-256 mismatch",
            file=sys.stderr,
        )
        return None
    return sha256_hex(read_back)


def select_entry() -> tuple[str, list[str]]:
    """Choose the entry to print and report any problems with it.

    Returns ``(entry, problems)``.  The primary entry is preferred;
    if it ever fails validation, the fallback is tried instead and
    the original problems are reported on stderr as a warning, so a
    bad edit can never silently swap the entry.  If both entries
    fail, the primary entry is returned together with its problems
    and the caller exits non-zero.
    """
    problems = validate_entry(ENTRY_TEXT)
    if not problems:
        return ENTRY_TEXT, []
    fallback_problems = validate_entry(FALLBACK_ENTRY_TEXT)
    if not fallback_problems:
        print(
            "warning: primary entry failed validation, using fallback: "
            + "; ".join(problems),
            file=sys.stderr,
        )
        return FALLBACK_ENTRY_TEXT, []
    return ENTRY_TEXT, problems + fallback_problems


def main(argv: list[str] | None = None) -> int:
    """Validate the entry, print it, and mirror it to the output file.

    ``--check`` validates without printing anything to stdout,
    for use by a test harness: exit 0 means the entry is valid.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    check_only = "--check" in args
    if check_only:
        args.remove("--check")

    entry, problems = select_entry()
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1
    if check_only:
        print(
            f"entry valid: {count_characters(entry)} characters, "
            f"{len(entry.splitlines())} line",
            file=sys.stderr,
        )
        return 0

    data = output_bytes(entry)
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()

    # Mirror to a file for the harness; a failure here is advisory only.
    write_entry_file(entry, resolve_output_dir())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
