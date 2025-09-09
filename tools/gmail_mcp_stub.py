class GmailMCP:
    """Stub class for interacting with Gmail via an MCP.

    This class demonstrates how a Gmail MCP could be used.  Real
    implementations would forward requests to a remote service that
    authenticates with Google and handles OAuth, scopes and quotas.
    """

    def search_emails(self, query: str):
        """Search for emails that match a given query.

        :param query: A Gmail search query.
        :return: A list of email identifiers or summaries.
        """
        print(f"[MCP/Gmail] Searching emails with query: {query}")
        return []

    def draft_email(self, to: str, subject: str, body: str) -> str:
        """Create an email draft but do not send it.

        :param to: Recipient email address.
        :param subject: Subject line of the email.
        :param body: Body text of the email.
        :return: An identifier for the created draft.
        """
        draft_id = "draft123"
        print(f"[MCP/Gmail] Drafting email to {to}: {subject}")
        # TODO: Replace with actual MCP call to create a draft and return its ID
        return draft_id

    def send_email(self, draft_id: str) -> None:
        """Send a previously drafted email.

        Sending emails should be gated by a human approval workflow to prevent
        accidental or malicious sends.  This method demonstrates the final
        sending step.

        :param draft_id: Identifier of the draft to send.
        """
        print(f"[MCP/Gmail] Sending draft {draft_id}")

    # Convenience method for our send_messages script. It drafts and
    # immediately sends an email in one step. In a real MCP, you might
    # separate these steps and require a human approval before calling
    # send_email.
    def send_email(self, to: str, subject: str, body: str) -> None:  # type: ignore[override]
        draft_id = self.draft_email(to, subject, body)
        print(f"[MCP/Gmail] Immediately sending email to {to}: {subject}")
        # In a real implementation, call the remote service to send using the draft ID
        # Here we just simulate sending the email
        # self.send_email(draft_id)  # comment to avoid recursion
        return