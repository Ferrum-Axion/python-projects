# Repo Monitor — Step 5: Load Configuration from config.yaml

TASK_ID = repo-monitor


Continue in the same project.

At this stage, the script works, but still requires editing code for:

- students
- task name
- repo identifiers

Now you move configuration out of Python.

---

## Files

Add a new file:

- `config.yaml`

This file will later contain:

- repository owner
- repository name
- current task identifier
- expected students list

---

## Packages

Install:

- `PyYAML`

Import:

- `yaml`

---

## Work

1. Create `config.yaml` with the required fields.

2. In `monitor.py`, replace hardcoded values:

- remove `expected_students = [...]`
- remove inline repo/task constants

3. Load configuration at runtime:

- open the YAML file
- parse it into a Python dictionary

4. Extract values from the parsed config:

- owner
- repo name
- task name
- expected student list

5. Keep the monitoring logic unchanged.

Only the source of the data changes.

---

## Output

The tool should behave exactly as before, but now:

- updating students/tasks requires only editing YAML
- no code changes needed

