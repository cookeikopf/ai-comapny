class SlackMCP:
    """Stub class for interacting with Slack via an MCP.

    This client exposes a handful of Slack operations that an agent may
    perform.  In a real system these calls would be forwarded to an MCP
    service which wraps the Slack API and enforces rate limits, scopes
    and logging.
    """

    def list_channels(self):
        """List available Slack channels.

        :return: A list of channel identifiers and names.
        """
        print("[MCP/Slack] Listing channels")
        return []

    def post_message(self, channel: str, text: str) -> None:
        """Post a message to a Slack channel.

        Use this only for internal channels designated for drafts or
        summaries.  Customer‑facing messages must always be gated via
        HITL and a separate action.

        :param channel: The channel ID or name.
        :param text: The message text to post.
        """
        print(f"[MCP/Slack] Posting message to {channel}: {text}")

    def reply_thread(self, channel: str, thread_ts: str, text: str) -> None:
        """Reply to a message thread in Slack.

        :param channel: Channel ID.
        :param thread_ts: Timestamp of the thread to reply to.
        :param text: Message content.
        """
        print(
            f"[MCP/Slack] Replying in {channel} at {thread_ts}: {text}"
        )