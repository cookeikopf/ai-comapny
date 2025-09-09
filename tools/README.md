# Model Context Protocol (MCP) Stubs

This directory contains *stub implementations* of Model‑Context Protocol (MCP) clients.  In
production these modules would call a dedicated MCP server to interact with external
services such as GitHub, Gmail or Slack.  The stubs here illustrate the method
signatures and document the principle of **least privilege** and **auditability**.

## Design Principles

1. **Least privilege** – Each MCP client exposes only the minimal set of actions
   needed by your agents.  For example, the Gmail client allows reading,
   searching and drafting emails without sending.  Sending is separated into
   its own method so that it can be gated by a human‑in‑the‑loop (HITL).

2. **Side‑effect separation** – Actions that can cause external side effects
   (sending messages, merging code) must be isolated.  Your orchestrator should
   never call those methods directly.  Instead, tasks with side effects are
   queued and executed only after you approve them in GitHub (via workflows).

3. **Auditability** – Every call to an MCP should produce a trace or log entry
   (see OpenTelemetry integration).  This allows you to trace back from an
   external action (e.g. an email sent) to the agent and prompt that initiated
   it.

These stubs do not implement any real functionality; they simply print
messages to the console.  Replace them with actual MCP calls once you have
deployed an MCP server or integrated with a provider such as Composio or
LangChain.