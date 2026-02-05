# Repo Monitor — Step 8: Create GitHub Action to Run Repo Monitor Automatically

TASK_ID = repo-monitor


Continue working in the same project.

## Work

1. Create GitHub Actions directory.

   Inside your repository, create folders:

   .github  
   .github/workflows  

2. Create a workflow file.

   Inside:

   .github/workflows

   Create a new file.

   Name it:

   repo-monitor.yml

3. Configure when the Action runs.

   The Action should run automatically.

   Configure the trigger to run only on the branch you are working on.

   Use the same branch used for this project.

   This ensures the monitor runs only in your working branch.

4. Create repository secret for SendGrid.

   Go to your repository on GitHub.

   Open:

   Settings → Secrets and variables → Actions

   Click:

   New repository secret

   Name the secret:

   SENDGRID_API_KEY

   Paste your SendGrid API key.

   Save the secret.

   This allows GitHub Action to authenticate with SendGrid securely.

5. Configure the environment.

   The Action should use:

   - Ubuntu runner
   - latest available version

   GitHub will create a fresh environment for each run.

6. Configure Python setup.

   The Action must install Python.

   Use the same Python version used in your project.

7. Install project dependencies.

   The Action must install required Python libraries.

   This allows the monitor script to run correctly.

8. Run the monitor script.

   The Action should execute:

   monitor.py

   The script will access the SENDGRID_API_KEY from the repository secret.

9. Commit and push the workflow file to your working branch.

   Push the workflow file to the same branch configured in the trigger.

   This activates the GitHub Action.

## Result

At this stage:

- GitHub automatically runs Repo Monitor
- Repo Monitor runs without manual execution
- Submission checking is fully automated
- GitHub Action runs monitor.py in your working branch
- GitHub Action can securely send email using SendGrid
