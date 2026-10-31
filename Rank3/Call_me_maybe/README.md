*This project has been created as part of the 42 curriculum by yuhli.*

# Call Me Maybe

Function calling for a small local language model using constrained decoding.

## Description

Call Me Maybe converts natural-language requests into structured function calls
using Qwen3-0.6B and the provided `llm_sdk`. It selects a function and generates
its typed arguments; it does not execute the function.

For example, given `What is the sum of 40 and 2?`, the expected output is:

```json
{
  "prompt": "What is the sum of 40 and 2?",
  "name": "fn_add_numbers",
  "parameters": {"a": 40.0, "b": 2.0}
}
```

The model selects the function and argument values from its logits. The decoder
restricts generation to the supported JSON structure and parameter types, without
using keyword matching or regular expressions to interpret the user request.

**Structural validity and semantic accuracy are different:** a valid call may
still contain the wrong function or values. Failed generations are reported
rather than included as successful results.

## Instructions

### Requirements

- Python 3.10 or later.
- [uv](https://docs.astral.sh/uv/).
- The provided `llm_sdk/` package in the repository root.
- The model runtime and weights required by the SDK.

```text
.
├── src/
├── llm_sdk/
├── data/input/
│   ├── functions_definition.json
│   └── function_calling_tests.json
├── tests/
├── pyproject.toml
├── uv.lock
├── Makefile
└── README.md
```

The SDK is provided separately and is excluded from project linting. Its runtime
dependencies must be declared in `pyproject.toml` and included in `uv.lock` for
`uv sync` to install them.

### Installation

From the repository root:

```bash
make install
```

This runs `uv sync`.

### Running the program

Use the default input and output paths:

```bash
make run
```

Or specify the paths explicitly:

```bash
uv run python -m src \
    --functions_definition data/input/functions_definition.json \
    --input data/input/function_calling_tests.json \
    --output data/output/function_calling_results.json
```

The output directory is created if needed. Generated files in `data/output/`
are excluded from version control.

### Input and output format

Function definitions are provided as a JSON array:

```json
[
  {
    "name": "fn_greet",
    "description": "Generate a greeting message for a person by name.",
    "parameters": {"name": {"type": "string"}},
    "returns": {"type": "string"}
  }
]
```

Requests are provided in a separate JSON array:

```json
[
  {"prompt": "Greet shrek"}
]
```

An illustrative result is:

```json
[
  {
    "prompt": "Greet shrek",
    "name": "fn_greet",
    "parameters": {"name": "shrek"}
  }
]
```

Supported parameter types are `number`, `integer`, `string`, and `boolean`.
Unsupported types are rejected when loading the definitions. Numeric output
uses Python floats for `number` and integers for `integer`.

### Makefile targets

| Command | Purpose |
| --- | --- |
| `make install` | Install dependencies with `uv sync` |
| `make run` | Run with the default paths |
| `make debug` | Run under `pdb` |
| `make clean` | Remove Python, mypy, and pytest caches |
| `make lint` | Run flake8 and the configured mypy checks |
| `make lint-strict` | Run flake8 and mypy in strict mode |
| `make test` | Run the test suite |

### Error handling

Input, SDK initialization, generation, and output errors are reported to stderr.
A failed prompt is skipped while processing continues for the remaining prompts.
The program returns a non-zero exit code if inputs cannot be loaded, the model
cannot start, output cannot be written, or every prompt fails. Individual prompt
failures do not necessarily make the entire run fail.

## Project structure

| File | Responsibility |
| --- | --- |
| `src/__main__.py` | CLI entry point and per-prompt error handling |
| `src/models.py` | Pydantic models for input and output data |
| `src/io_utils.py` | JSON loading, validation, and output writing |
| `src/prompt.py` | Model prompt construction |
| `src/vocab.py` | Vocabulary decoding, token trie, and token lookup |
| `src/grammar.py` | Grammar phases and legal-token constraints |
| `src/generator.py` | Generation, masking, and model-based selection |
| `tests/` | Unit, randomized, and CLI tests |

## Algorithm explanation

### Constrained generation

The prompt contains the available functions, their typed parameters, and the
user request. Generation follows a grammar for this structure:

```json
{"name": "<function name>", "parameters": {"<parameter>": "<typed value>"}}
```

The placeholders above illustrate the structure; actual values use their
required JSON types. The original request is added as `prompt` in the final
output record.

At each model-driven token step, the generator:

1. Obtains next-token logits using `get_logits_from_input_ids`.
2. Finds the token IDs allowed by the current grammar state.
3. Masks disallowed logits with `-inf`.
4. Selects the highest-scoring legal token.
5. Updates the generated sequence and grammar state.

Generation stops when the object is complete. A step limit and an explicit
error for states with no legal next token prevent endless generation. Completed
text is parsed with `json.loads` before serialization.

### Grammar phases

The grammar is a chain of specialized phases rather than a general JSON Schema
compiler. Parameter phases are assembled after the function name is selected.

| Phase | Role |
| --- | --- |
| `LiteralPhase` | Emit fixed keys, punctuation, and other required text |
| `EnumPhase` | Restrict closed choices, such as function names or booleans |
| `NumberValuePhase` | Enforce JSON number syntax or integer-only syntax |
| `StringValuePhase` | Enforce string syntax and supported escapes |

The vocabulary is decoded from byte-level BPE representations into text and
stored in a trie. Prefix lookup avoids scanning the entire vocabulary for each
fixed-text constraint. Tokens containing incomplete UTF-8 fragments are excluded.

Numbers use a state machine covering signs, digits, fractions, and exponents.
It rejects leading zeros and incomplete numeric forms. Integer parameters do
not allow fractions or exponents. Non-finite values are rejected, and output is
written with `allow_nan=False`.

Strings allow ordinary text and the simple JSON escapes: `\"`, `\\`, `\/`,
`\b`, `\f`, `\n`, `\r`, and `\t`. Tokens may combine final string content,
the closing quote, and the fixed text that follows. Legal string-token tables
are cached by escape state.

### Fixed text and closed choices

The generator avoids model calls for fixed text by emitting matching tokens
directly. This reduces inference work for syntax that has no semantic choice.

For closed choices, such as function names and booleans, the implementation
described here scores complete candidate sequences using the tokenizer's own
token boundaries. Candidate scores sum the deciding tokens' log-probabilities;
the highest-scoring option is selected. A candidate can be pruned when its
running score is already below the best completed score. If exact token
round-tripping is unavailable, selection falls back to token-by-token decoding.

These paths differ from greedy generation of free-form argument values. Forced
text does not require a model decision, while closed choices still depend on
model scores.

## Design decisions

- **A phase-based grammar:** the fixed output format allows a small, explicit
  state machine instead of a general schema compiler.
- **Deterministic selection:** free-form values use greedy legal-token selection;
  closed choices use candidate scoring when available.
- **Model-compatible formatting:** the prompt uses Qwen3's chat format, disables
  thinking, and opens a JSON answer block. Generated text uses spaced JSON to
  better match the model's expected continuation.
- **Tokenizer-aware boundaries:** merged punctuation and string-closing tokens
  are supported to avoid forcing unnatural continuations.
- **Validated data models:** Pydantic validates JSON input and output records;
  grammar phases and vocabulary helpers remain ordinary behavior classes.
- **SDK isolation:** SDK calls are typed as `Any` at the integration boundary.
  Encoded IDs are flattened to support both one-dimensional and batched outputs
  without importing a tensor library into the project code.
- **Per-prompt isolation:** generation limits and error handling keep one failed
  request from interrupting other requests.

## Performance analysis

The following figures were reported during development with a **synthetic
vocabulary and a stand-in model**. They measure decoder overhead, not real
Qwen3 inference speed, and have not been re-measured for this README revision.

| Measurement | Reported result |
| --- | --- |
| Vocabulary decoding and trie construction | 2.7 s; approximately 216 MB additional peak memory |
| Initial string-token table | 0.14 s; cached afterward |
| Fixed-literal mask | Approximately 0.001 ms |
| Function-name enum mask | Approximately 0.003 ms |
| Number mask | Approximately 5 ms |
| Cached string-body mask | Approximately 0.5 ms |
| Generation loop excluding inference, over 1,272 steps | Approximately 5.3 ms per step |

The synthetic vocabulary contained approximately 151,650 tokens, including
1–4 digit runs to exercise numeric constraints.

An earlier CPU run was reported as taking 6 minutes 42 seconds for eight prompts,
before skipping fixed-text inference. A comparable end-to-end measurement after
the optimizations, together with final real-model accuracy, is still pending.
The synthetic timings above should not be treated as final-model benchmarks.

Model inference is expected to dominate runtime. The SDK receives the full ID
sequence on each call; the cost depends on whether it caches previous
computation internally.

## Known limitations

- Only `number`, `integer`, `string`, and `boolean` parameters are supported;
  arrays and nested objects are not.
- Strings have a growth threshold of 200 characters and numbers of 32
  characters. A token crossing either threshold may overshoot it. Numeric
  exponents are limited to two digits.
- Unicode escapes in the form `\uXXXX` are not generated. Characters requiring
  excluded UTF-8 fragment tokens may be unavailable.
- Number endings have more restrictive token boundaries than string endings;
  their effect on model accuracy has not been measured.
- Grammar constraints enforce supported structure and types, not the correctness
  of the chosen function or argument values.
- Runtime dependencies and real-model behavior must be checked with the
  separately provided SDK.

## Challenges faced

**Numeric validity.** Randomized testing exposed leading zeros, invalid exponent
prefixes, and float overflow. The number state machine, length and exponent
limits, finite-value checks, and strict JSON serialization address these cases.

**Byte-level vocabulary decoding.** Token text requires the inverse byte-to-Unicode
mapping used by GPT-2-style BPE. Incomplete UTF-8 fragments cannot be treated as
standalone text tokens.

**String termination.** Restricting closing tokens to a bare quote can exclude
the continuation preferred by the model. Supporting merged string endings allows
content, closing quotes, and required punctuation to be consumed together.

**Function-name tokenization.** Forcing shared prefixes into separate tokens can
create an unfamiliar model context. Scoring complete, naturally tokenized
candidates avoids relying only on the first fragment of a function name.

**SDK and tooling integration.** Encoded tensor shapes require flattening, and
mypy must use an interpreter version compatible with installed NumPy type stubs.

## Testing strategy

```bash
make test
make lint
```

| Test file | Coverage |
| --- | --- |
| `tests/test_vocab.py` | Byte decoding, trie lookup, and string-state tables |
| `tests/test_grammar.py` | Random-logit generations, numeric overflow, length limits, unclosable strings, and individual phases |
| `tests/test_grammar_bpe.py` | Merged tokens, grammar boundaries, control characters, duplicate text, and partial UTF-8 fragments |
| `tests/test_prompt.py` | Function descriptions, typed parameters, user requests, and answer cues |
| `tests/test_generator.py` | Logit masking, out-of-range IDs, all-masked states, and tensor flattening |
| `tests/test_io_utils.py` | Invalid inputs, duplicates, unsupported types, and non-finite output |
| `tests/test_cli.py` | End-to-end CLI behavior with a fake SDK and initialization failures |

The development notes report 300 randomized generations checked for schema
compliance, including functions with no parameters. BPE-like test vocabularies
also exercise tokens that span grammar boundaries, which character-level tests
alone cannot adequately cover.

These tests target structural correctness. Real-model evaluation must separately
check function selection and argument accuracy, including ambiguous requests,
empty strings, special characters, large numbers, and multiple parameters.

## Resources

- [Qwen3-0.6B model card](https://huggingface.co/Qwen/Qwen3-0.6B)
- Willard, B. T. and Louf, R. (2023),
  [Efficient Guided Generation for Large Language Models](https://arxiv.org/abs/2307.09702).
  Reference for finite-state logit masking; its library is not used.
- Radford, A. et al. (2019), *Language Models are Unsupervised Multitask Learners*.
  Reference for GPT-2 byte-level BPE.
- [RFC 8259: The JSON Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [uv documentation](https://docs.astral.sh/uv/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [PEP 257: Docstring Conventions](https://peps.python.org/pep-0257/)

### How AI was used

Claude was used to produce the initial implementation of the modules in `src/`,
the test suite, the Makefile, and the original README from the project subject.
It also assisted with debugging and iterative fixes for issues exposed by
randomized testing. A temporary SDK stub was used for CLI testing.

ChatGPT assisted with editing this README's Markdown, organization, and wording,
including distinguishing historical measurements from pending evaluation.
This documentation revision did not include source-code inspection or a new
execution of the test suite.
