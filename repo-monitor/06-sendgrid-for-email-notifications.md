# Repo Monitor — Step 6: Setup SendGrid for Email Notifications

TASK_ID = repo-monitor


Continue working in the same project.

## Work

1. Create a SendGrid account.

   Go to:

   sendgrid.com

   Register and verify your email.

2. Login to SendGrid dashboard.

3. Complete Single Sender Verification.

   Go to:

   Settings → Sender Authentication → Single Sender Verification

   Create a new sender.

   Use your own email address.

   Complete the verification process from your email inbox.

   This allows SendGrid to send emails from your address.

4. Create API Key.

   Go to:

   Settings → API Keys

   Create new key.

   Name it:

   repo-monitor

   Set permission level:

   Full Access

   Copy the key.

5. Store the API key as environment variable.

   The script will later use this key to authenticate.

6. Install SendGrid Python library.

   This library allows sending email through SendGrid API.

7. Verify everything is ready.

   At this stage you have:

   - SendGrid account
   - verified sender email
   - API key
   - environment variable configured
   - SendGrid library installed

Email sending will be implemented in the next step.
