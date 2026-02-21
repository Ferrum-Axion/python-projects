# Repo Monitor — Step 3: Error Handling + sys basics

TASK_ID = repo-monitor


Continue in the same file: `monitor.py`.

## Packages

Add:

- `sys`

## Work

1. Wrap the GitHub request logic with `try/except`.

2. Handle:

- Network errors (connection/timeout)
- Repository not found (404)
- Unauthorized request (401)
- Any non-200 status code

3. On failure:

- Print a short error message
- Print errors to `sys.stderr`

4. Exit properly:

- Critical API error → `sys.exit(1)`

## Output Rules

- Success: print branch names normally
- Failure: print a clean error message and stop

At this stage you now have:

- requests
- branch name extraction
- stable error handling

