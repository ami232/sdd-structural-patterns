# StreamFlix

You're building the backend for a small video streaming service. It needs to
accept payments from more than one provider, avoid loading heavy video files
until they're actually needed, and expose a single simple entry point to the
mobile app team.

## Business requirements

- Subscribers can pay with either Stripe or PayPal, but each vendor SDK has
  its own quirky interface. The app should only ever talk to one common
  payment interface.
- Video files are expensive to load. A video should not be loaded from disk
  until someone actually presses play, and it should not be reloaded on every
  play.
- The mobile app team doesn't want to know about payment processors or video
  loading at all. They just want to call `subscribe()` and `watch()`.

## Architecture

- **Adapter**: `StripeAdapter` and `PayPalAdapter` make the mismatched
  `StripeAPI` and `PayPalClient` SDKs conform to the common
  `PaymentProcessor` interface.
- **Proxy**: `ProxyVideo` stands in for `RealVideo`, delaying (and caching)
  the expensive load until the video is actually played.
- **Facade**: `StreamingFacade` hides both of the above behind two simple
  methods, `subscribe()` and `watch()`.

## Project layout

```dir_tree
root_dir
├─ streamflix/
│  ├─ __init__.py
│  ├─ payments.py
│  ├─ catalog.py
│  ├─ facade.py
│  └─ app.py
├─ tests/
│  ├─ conftest.py
│  ├─ test_payments.py
│  ├─ test_catalog.py
│  └─ test_facade.py
└─ README.md
```

## Setup

Preferred: [uv](https://docs.astral.sh/uv/). Install uv once per machine (see
uv's docs), then from inside your local clone:

```bash
uv venv                              # create a local virtual environment (.venv)
uv pip install -r requirements.txt   # install pytest into it
```

From then on, run any Python command through `uv run` so it uses that
environment automatically:

```bash
uv run pytest -q                     # run all tests
uv run pytest ./tests/test_payments.py   # run payment tests only
uv run python -m streamflix.app      # run the demo app
```

<details>
<summary>Alternative: plain venv + pip</summary>

```bash
# Unix
python -m venv .venv && source .venv/bin/activate

# Windows:
python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

python -m pytest -q
python -m pytest ./tests/test_payments.py
python -m streamflix.app
```

</details>

## How to submit

Two different repos are involved, so be precise about which is which:

- **The course repo** is `ami232/sdd-structural-patterns`.
  This is where your work has to end up. You cannot push to it, which is
  exactly why you send a pull request.
- **Your fork** is `<your-github-username>/sdd-structural-patterns`.
  This is where you do the work.

Every step below says which of the two it means. Where these instructions say
"the course repo", they never mean your fork, even though your fork contains
a copy of this same README.

1. Fork `ami232/sdd-structural-patterns` to your own GitHub account.
   Keep the fork **public** (the default when forking a public repo) so it can
   be reviewed without needing collaborator access.
2. Clone **your fork**, not the course repo, and work through the exercises
   below on a branch:

   ```bash
   git clone <the URL from the green "Code" button on your fork>
   cd sdd-structural-patterns
   git switch -c solution
   ```

3. Commit your changes and push the branch to your fork:

   ```bash
   git push origin solution
   ```

4. Open a **pull request from your fork into the course repo**. On github.com,
   open your fork, click "Contribute", then "Open pull request".

   Before you submit it, check that the pull request header reads exactly:

   | Field | Value |
   | --- | --- |
   | base repository | `ami232/sdd-structural-patterns` |
   | base | `main` |
   | head repository | `<your-github-username>/sdd-structural-patterns` |
   | compare | `solution` |

   **If your own username appears on both sides, the pull request is aimed at
   your own fork and will never reach us.** Change it with the "base
   repository" dropdown before submitting.
5. Opening the PR automatically runs the full test suite as a GitHub Actions
   check, see the "Checks" tab on your PR. All three test files
   (`test_payments.py`, `test_catalog.py`, `test_facade.py`) must pass for
   the check to go green.
6. Submit the link to your pull request on Blackboard. This is your
   submission; the green check confirms the tests pass, but the PR itself
   (with your commits and diff) is what gets graded.

## Exercises

### 1. Implement the payment adapters

Functional requirements:

- `StripeAdapter` and `PayPalAdapter` must both implement `PaymentProcessor`,
  so the rest of the app never needs to know which vendor is behind them.
- `StripeAPI` only understands integer cents; convert the EUR amount
  correctly (12.34 EUR becomes 1234 cents).
- Both adapters return a receipt string formatted to exactly two decimals:
  `"paid 12.34 EUR via stripe (<merchant_id>)"` or
  `"paid 12.34 EUR via paypal (<account_email>)"`.
- Non-positive amounts must raise an error, as the underlying SDKs already do.

To test this part:

```bash
uv run pytest ./tests/test_payments.py
```

Goal --> Pass payment tests

### 2. Implement the video proxy

Functional requirements:

- `ProxyVideo` must expose the same `play()` interface as `RealVideo`.
- Creating a `ProxyVideo` must **not** load the underlying `RealVideo`.
- The first call to `play()` must create the `RealVideo` and delegate to it.
- Later calls to `play()` on the same `ProxyVideo` must reuse that same
  `RealVideo` instead of loading it again.

To test this part:

```bash
uv run pytest ./tests/test_catalog.py
```

Goal --> Pass catalog tests

### 3. Implement the streaming facade

Functional requirements:

- A brand-new `StreamingFacade` starts out unsubscribed.
- `watch()` must raise `PermissionError` when called before `subscribe()`,
  and it must not trigger a video load in that case.
- `subscribe(monthly_fee)` charges the fee through the injected
  `PaymentProcessor` and returns its receipt.
- After subscribing, `watch(video)` delegates to `video.play()` and returns
  its result.
- The facade must work with any `PaymentProcessor` implementation, not just
  Stripe.

To test this part:

```bash
uv run pytest ./tests/test_facade.py
```

Goal --> Pass facade tests
