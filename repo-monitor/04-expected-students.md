# Repo Monitor — Step 4: Expected Students + Branch Comparison

TASK_ID = repo-monitor

Continue in the same file: `monitor.py`.

At this stage you already have:

- branch fetch working
- branch name extraction
- basic error handling

Now you turn it into a real submission checker.

---

## Work

1. Define a temporary list of expected students inside the script:

- `expected_students = [...]`

2. Define a task identifier:

- `TASK_NAME`

3. Define the required branch naming convention:

- `{TASK_NAME}-{student}`

Example:

- `task-3-dana`
- `task-3-yossi`

4. Generate the expected branch list from the student list.

Use:

- list comprehension (preferred)
- or `map()` (optional practice)

---

## Compare Against Actual Branches

5. You now have:

- `expected_branches`
- `actual_branches`

Compute missing submissions:

- expected minus actual

Recommended Python tool:

- `set` difference

6. Print results clearly:

- If some are missing → print missing branch names
- If none are missing → print success message

---

## Exit Codes (initial)

Add basic status behavior:

- Missing submissions → `sys.exit(2)`
- Everything submitted → `sys.exit(0)`

At this stage the tool can already act as a checker.

Next: remove hardcoded student lists and move configuration into `config.yaml`.
