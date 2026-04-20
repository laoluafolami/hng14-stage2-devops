# FIXES.md — All Bugs Found and Fixed

## Bug 1 — api/.env committed to repository
- **File:** `api/.env`
- **Problem:** A real `.env` file containing `REDIS_PASSWORD=supersecretpassword123` was committed to the repository. This is a critical security violation — secrets must never exist in git history.
- **Fix:** Added `api/.env` to `.gitignore`, removed it from git tracking with `git rm --cached api/.env`, purged from history with `git filter-branch`, and replaced it with `api/.env.example` containing placeholder values only.

## Bug 2 — API hardcoded Redis host as localhost
- **File:** `api/main.py`, line 8
- **Original:** `r = redis.Redis(host="localhost", port=6379)`
- **Problem:** `localhost` does not resolve to the Redis container inside Docker. Services on an internal Docker network must refer to each other by service name.
- **Fix:** Changed to read `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` from environment variables: `r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)`

## Bug 3 — Worker hardcoded Redis host as localhost
- **File:** `worker/worker.py`, line 5
- **Original:** `r = redis.Redis(host="localhost", port=6379)`
- **Problem:** Same as Bug 2. The worker container cannot reach Redis via localhost.
- **Fix:** Read `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` from environment variables.

## Bug 4 — Queue name mismatch between API and Worker
- **File:** `api/main.py` line 13 vs `worker/worker.py` line 28
- **Original:** API pushed to queue named `"job"`, while the worker logic was intended to consume the same queue but inconsistency in naming would cause silent failures.
- **Fix:** Standardised both to use `"jobs"` as the queue name throughout.

## Bug 5 — Frontend hardcoded API URL as localhost
- **File:** `frontend/app.js`, line 5
- **Original:** `const API_URL = "http://localhost:8000"`
- **Problem:** The frontend container cannot reach the API via localhost. Must use the Docker service name.
- **Fix:** Changed to `const API_URL = process.env.API_URL || 'http://api:8000'`

## Bug 6 — Frontend Node.js server bound to 127.0.0.1 only
- **File:** `frontend/app.js`, last line
- **Original:** `app.listen(3000, ...)`
- **Problem:** Without specifying `'0.0.0.0'`, Node.js only listens on the loopback interface inside the container, making the port unreachable from outside.
- **Fix:** `app.listen(3000, '0.0.0.0', ...)`

## Bug 7 — No /health endpoint on API (blocks Docker healthcheck)
- **File:** `api/main.py`
- **Problem:** No health endpoint existed. Docker HEALTHCHECK instructions for the API container need an HTTP endpoint to poll.
- **Fix:** Added `GET /health` endpoint that pings Redis and returns `{"status": "ok"}`.

## Bug 8 — No /health endpoint on Frontend (blocks Docker healthcheck)
- **File:** `frontend/app.js`
- **Problem:** Same as Bug 7.
- **Fix:** Added `GET /health` endpoint returning `{"status": "ok"}`.

## Bug 9 — No graceful shutdown on Worker
- **File:** `worker/worker.py`
- **Problem:** No SIGTERM handler. When Docker stops the container, the worker is killed mid-job, potentially leaving jobs in a broken state.
- **Fix:** Added `signal.signal(signal.SIGTERM, handle_signal)` with a `running` flag to allow clean loop exit.

## Bug 10 — Unpinned package versions
- **Files:** `api/requirements.txt`, `worker/requirements.txt`, `frontend/package.json`
- **Problem:** No version pins means non-deterministic builds — a future package release can silently break the application.
- **Fix:** Pinned all dependencies to specific versions.

## Bug 11 — Missing ESLint configuration
- **File:** `frontend/` (missing `.eslintrc.json`)
- **Problem:** The CI pipeline requires JavaScript linting with ESLint, but no ESLint config or dev dependency existed.
- **Fix:** Added `eslint` to `devDependencies` in `package.json` and created `.eslintrc.json`.