# Email Setup

The repository supports sending emails via MCP stubs. To enable real email sends:

1. Choose a provider (e.g. Resend, SendGrid, Postmark, SMTP).
2. Store provider credentials in repository secrets.
3. Set `allow_outbound_email: true` in `config/feature_flags.yaml`.
4. Configure the `production` environment in GitHub with required reviewers to approve real sends.

During dry runs the script only logs the target `to` address, subject, and a body preview.
