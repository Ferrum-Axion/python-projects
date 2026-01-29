# Repo Monitor — Step 1: Fetch Branches (requests)

TASK_ID = repo-monitor

## Files

- `monitor.py`

## Packages

Install:

- `requests`

## Work

1. Create `monitor.py`.

2. Define repository identifiers at the top:

   - `OWNER`
   - `REPO_NAME`

3. Use the GitHub Branches endpoint:

   `GET https://api.github.com/repos/<OWNER>/<REPO>/branches`

4. Send a request using `requests.get(...)`.

5. Print:

   - the HTTP status code
   - the raw JSON response

## Output

At this stage you should only confirm:

- you can reach the API
- you receive a list of branch objects

Do not extract names yet.
Do not handle errors yet.

