# Repo Monitor — Step 2: Extract Branch Names (map + lambda)

TASK_ID = repo-monitor


Continue working in the same file: `monitor.py`.

## Work

1. Start from the API response list (branch objects).

2. Convert the branch objects into a list of branch name strings.

   Each branch object contains:

   - `"name"`

3. Implement name extraction twice:

   - Using list comprehension
   - Using `map()` with `lambda`

4. Print the final list of branch names.

## Output

You should now print something like:

- `main`
- `task-3-dana`
- `task-3-yossi`

At this stage you have:

- a request working
- branch names extracted

