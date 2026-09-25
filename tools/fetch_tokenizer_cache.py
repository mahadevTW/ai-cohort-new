"""Pre-download the tiktoken vocabularies into a repo-local cache.

Why this exists
---------------
`tiktoken.get_encoding(...)` downloads its vocabulary from the internet the first time it
is called. On a corporate or venue network that intercepts TLS, that download fails with

    SSLError: certificate verify failed: self-signed certificate in certificate chain

because `tiktoken` uses `requests`, which trusts only certifi's CA bundle and not the
machine's system trust store. Every student on such a network hits this in the first ten
minutes of week 1.

The fix is to ship the vocabulary with the repo. This script downloads it once (via
`curl`, which on macOS *does* use the system keychain and therefore trusts the corporate
root CA) and writes it into `tiktoken_cache/` using tiktoken's own cache-key scheme.
After that, `TIKTOKEN_CACHE_DIR` pointed at that folder makes tokenisation work with no
network at all.

Run once from the repo root:

    ./.venv/bin/python tools/fetch_tokenizer_cache.py
"""

from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
CACHE = REPO / "tiktoken_cache"

# Vocabularies used across the ten weeks. o200k_base covers the gpt-4o / o-series family;
# cl100k_base is kept so switching MODEL to an older model does not re-trigger a download.
BLOBS = [
    "https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken",
    "https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken",
]


def cache_key(url: str) -> str:
    """tiktoken stores each blob under sha1(url) — see tiktoken/load.py:read_file_cached."""
    return hashlib.sha1(url.encode()).hexdigest()


def fetch(url: str, dest: pathlib.Path) -> None:
    """Download with curl, which uses the system trust store and survives TLS interception."""
    result = subprocess.run(
        ["curl", "-sSfL", "--retry", "3", "-o", str(dest), url],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed for {url}\n{result.stderr.strip()}")


def main() -> int:
    CACHE.mkdir(parents=True, exist_ok=True)

    for url in BLOBS:
        dest = CACHE / cache_key(url)
        name = url.rsplit("/", 1)[-1]
        if dest.exists():
            print(f"  cached   {name}  ({dest.stat().st_size:,} bytes)")
            continue
        print(f"  fetching {name} ...")
        fetch(url, dest)
        print(f"  saved    {name}  ({dest.stat().st_size:,} bytes)")

    # Prove the cache is sufficient: forbid all network reads, then load both encodings.
    import os

    os.environ["TIKTOKEN_CACHE_DIR"] = str(CACHE)

    import tiktoken
    import tiktoken.load

    def _no_network(blobpath, *a, **kw):
        raise AssertionError(f"cache miss — tried to download {blobpath}")

    tiktoken.load.read_file = _no_network  # any download now fails loudly

    for enc_name in ("o200k_base", "cl100k_base"):
        enc = tiktoken.get_encoding(enc_name)
        assert enc.decode(enc.encode("leave policy")) == "leave policy"
        print(f"  verified {enc_name} offline — {enc.n_vocab:,} tokens in vocabulary")

    print(f"\nCache ready at {CACHE.relative_to(REPO)}/ — commit it so students never download.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
