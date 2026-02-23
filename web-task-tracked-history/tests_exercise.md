# NGINX Deploy Testing — Exercises (Python + Path + pytest)

Goal: build a small **integration test suite** for an NGINX deploy project, using Python, `pathlib.Path`, `subprocess`, and `pytest`.

runnig pytest with sudo within venv - sudo -E venv/bin/python3 -m  pytest -q

## Exercise 1 — Minimal pytest + Path (not project-related)
**Objective:** prove you can write a working pytest test using `Path`.

1. Create `tests/test_sanity.py`.
2. Use `Path` to create a temp directory under the project (e.g. `.tmp/`).
3. Write a small text file and read it back.
4. Assert the content matches.

**Expected:** `pytest` runs and passes without touching NGINX or system paths.

---

## Exercise 2 — Deploy copies site files (marker test)
**Objective:** verify deploy copied the site to the destination.

**Idea:** add a marker to the source `site/index.html`, run deploy, and verify the marker appears in the deployed file.

1. Define:
   - `project_root = Path(__file__).resolve().parents[1]`
   - `site_source = project_root / "site"`
   - `site_dest = Path("/var/www/devops-site")`
2. Backup current deployed site:
   - copy `/var/www/devops-site` to a backup folder (choose a location you can manage).
3. Read `site_source/index.html`, append a unique marker string, write it back.
4. Run deploy: `subprocess.run([...], check=True)`
5. Assert:
   - `/var/www/devops-site/index.html` exists
   - marker string exists in deployed `index.html`
6. Cleanup (must run even if assertions fail):
   - restore original `site_source/index.html`
   - restore deployed site from backup

**Expected:** deploy truly copied updated HTML into the served path.

---
## Exercise 3 — Deploy copies NGINX config to the correct location
**Objective:** verify nginx/site.conf was copied into:
/etc/nginx/sites-available/devops-site

1. Define:
   - config_source = project_root / "nginx" / "site.conf"
   - config_dest = Path("/etc/nginx/sites-available/devops-site")
2. Run deploy.
3. Assert:
   - destination file exists and is a file
4. Compare content:
   - strict: read_text() equality
   - or relaxed: assert key lines exist (e.g. server {, listen, root)

**Expected:** configuration file is present and matches what you shipped.

---


## Exercise 4 — Deploy logs an operation row to Postgres (and clean it)
**Objective:** verify deploy inserts a row into `operations` and clean it afterward.

1. Connect with `psycopg` to `ops_db`.
2. Before deploy:
   - read `COUNT(*)` from `operations` (or read max `id`)
3. Run deploy.
4. After deploy:
   - assert count increased by 1
   - fetch the latest row and assert:
     - `action_type == "deploy"`
     - `status == "success"`
5. Cleanup:
   - delete the inserted row(s) created by this test.

**Expected:** deploy + Python logging + Postgres insert is verified end-to-end.

---



