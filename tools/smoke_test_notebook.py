"""Run a week's notebook top to bottom against a stubbed OpenAI client.

Proves the notebook has no ordering bugs, no NameErrors and no syntax errors, without an
API key and without spending a cent. It does NOT prove the prompts produce good answers —
only that the code runs.

    ./.venv/bin/python tools/smoke_test_notebook.py week-01-llm-foundations/week1.ipynb
"""

from __future__ import annotations

import math
import pathlib
import random
import sys
import types

import nbformat

REPO = pathlib.Path(__file__).resolve().parent.parent


# --------------------------------------------------------------- stub client
def _obj(**kw):
    return types.SimpleNamespace(**kw)


class _StubCompletions:
    """Mimics client.chat.completions.create for both blocking and streaming calls."""

    def create(self, model, messages, stream=False, logprobs=False,
               top_logprobs=None, max_tokens=None, **kwargs):
        # Reasoning models reject sampling parameters — reproduce that so the notebook's
        # try/except cell exercises the path it claims to.
        if "o4" in model or model.startswith("o1") or model.startswith("o3"):
            for p in ("temperature", "top_p"):
                if p in kwargs:
                    raise ValueError(
                        f"Unsupported parameter: '{p}' is not supported with this model."
                    )

        prompt_tokens = sum(len(m["content"]) // 4 + 4 for m in messages)
        text = "STUBBED REPLY: employees receive 18 days of earned leave per year."
        completion_tokens = len(text) // 4
        reasoning = 180 if "o4" in model else 0

        usage = _obj(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            completion_tokens_details=_obj(reasoning_tokens=reasoning),
        )

        if stream:
            return self._stream(text, usage)

        lp = None
        if logprobs:
            n = top_logprobs or 5
            picks = [" Paris", " the", " a", " Lyon", " France"][:n]
            lp = _obj(content=[_obj(top_logprobs=[
                _obj(token=t, logprob=math.log(max(p, 1e-6)))
                for t, p in zip(picks, [0.92, 0.04, 0.02, 0.01, 0.01][:n])
            ])])

        if max_tokens == 1:
            text = " Paris"

        return _obj(choices=[_obj(message=_obj(content=text), logprobs=lp)], usage=usage)

    @staticmethod
    def _stream(text, usage):
        for word in text.split(" "):
            yield _obj(usage=None, choices=[_obj(delta=_obj(content=word + " "))])
        yield _obj(usage=usage, choices=[])


class StubOpenAI:
    def __init__(self, *a, **kw):
        self.chat = _obj(completions=_StubCompletions())


# --------------------------------------------------------------- runner
def run(path: pathlib.Path) -> int:
    nb = nbformat.read(path, as_version=4)

    import openai
    openai.OpenAI = StubOpenAI          # every notebook builds its client from this

    import tiktoken.load
    real_read = tiktoken.load.read_file

    def _no_net(blobpath, *a, **kw):
        raise AssertionError(
            f"notebook tried to DOWNLOAD {blobpath} — the vendored cache is not being used"
        )

    tiktoken.load.read_file = _no_net   # force the offline path

    g: dict = {"__name__": "__main__"}
    random.seed(0)

    code_cells = [c for c in nb.cells if c.cell_type == "code"]
    for i, cell in enumerate(code_cells, start=1):
        src = "".join(cell.source)
        try:
            exec(compile(src, f"<cell {i}>", "exec"), g)
        except Exception as e:
            print(f"\nFAILED at code cell {i}/{len(code_cells)}: {type(e).__name__}: {e}")
            print("-" * 70)
            print(src)
            tiktoken.load.read_file = real_read
            return 1

    tiktoken.load.read_file = real_read
    print(f"\n{'=' * 70}")
    print(f"PASS — all {len(code_cells)} code cells ran top to bottom")
    print("       (stubbed API, no key, no spend, no network reads)")
    calls = g.get("SPEND")
    if calls is not None:
        print(f"       llm() was exercised; SPEND holds {len(calls)} record(s)")
    return 0


if __name__ == "__main__":
    target = REPO / (sys.argv[1] if len(sys.argv) > 1 else "week-01-llm-foundations/week1.ipynb")
    sys.exit(run(target))
