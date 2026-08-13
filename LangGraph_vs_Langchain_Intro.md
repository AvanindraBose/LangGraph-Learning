# LangGraph — Interview Revision Notes

## What is LangGraph?

> **LangGraph is a graph-based orchestration framework, built on top of LangChain, used to create fault-tolerant, event-driven, and stateful AI systems.**

It represents an AI workflow as a **graph of nodes and edges** — where each node is a unit of work (an LLM call, a tool call, a function) and edges define the control flow between them, including loops and conditional branches. This makes it possible to build complex, production-grade agentic applications that plain LangChain chains struggle to express cleanly.

---

## LangGraph vs. LangChain — 7 Key Differences

### 1. Complex Workflows (Loops, Conditional Branches, Jumps)
LangChain is fundamentally designed around **linear/sequential chains**. Representing complex control flow — loops, conditional branching, jumping back to a previous step — is not natively supported and typically requires writing custom **"glue code"** in Python to stitch chains together manually.

LangGraph solves this natively by modeling the workflow as a **graph**, where conditional edges and cycles are first-class citizens — no external glue code required.

### 2. Event-Driven Triggers
LangGraph supports **event-driven execution** of workflows — nodes/graphs can be triggered in response to events, rather than being limited to a fixed, predetermined sequence of calls.

LangChain, in contrast, is largely built for a more static, request-response style of execution.

### 3. State Management
LangGraph is **stateful by design** — it maintains a shared, persistent state object that flows through the graph and is updated by each node as execution progresses.

LangChain does not have this built in; managing state across a multi-step chain has to be handled manually by the developer.

### 4. Human-in-the-Loop (HITL)
Because LangGraph persists state at every step, it can **pause execution, wait for human input/approval, and resume from the exact same state** — making Human-in-the-Loop workflows straightforward to implement.

This is difficult to achieve reliably in plain LangChain, since there's no built-in mechanism to durably pause and resume a chain mid-execution.

### 5. Observability
Both frameworks can be monitored using **LangSmith**, but the depth of integration differs:
- In **LangChain**, once custom Python glue code is introduced to handle complex workflows (loops/branches), LangSmith can only trace the LangChain components — it **cannot trace the custom Python logic** wrapped around them, creating blind spots.
- In **LangGraph**, since the entire workflow — including branches and loops — is expressed within the framework itself (not external Python glue code), **LangSmith has much stronger, end-to-end integration** and can observe the full execution graph.

### 6. Fault Tolerance
LangGraph is **fault-tolerant** — because it persists state at each node/step (via checkpointing), a failed run can **recover and resume from the last successful state** instead of restarting from scratch.

LangChain does not provide this out of the box.

### 7. Subgraphs
LangGraph supports **subgraphs** — self-contained graphs that can be nested/reused inside a larger parent graph.

This is extremely useful for:
- **Multi-agent applications** — each agent can be modeled as its own subgraph.
- **Reusable components** — a common workflow pattern can be built once and plugged into multiple parent graphs.

This concept does not exist in LangChain.

---

## Summary Table

| # | Aspect | LangChain | LangGraph |
|---|--------|-----------|-----------|
| 1 | Complex workflows (loops/branches/jumps) | Needs custom Python glue code | Native support via graph structure |
| 2 | Event-driven triggers | Not natively supported | Supported |
| 3 | State management | Manual | Stateful by design |
| 4 | Human-in-the-Loop | Difficult to implement | Easy — built on persisted state |
| 5 | Observability (LangSmith) | Blind spots around custom glue code | Strong, end-to-end integration |
| 6 | Fault tolerance | Not built in | Built in via checkpointing/state recovery |
| 7 | Subgraphs | Not available | Available — great for multi-agent & reusable components |

---

## One-Line Interview Answer

> "LangGraph is a graph-based orchestration framework built on LangChain that lets you build fault-tolerant, event-driven, and stateful AI systems — solving LangChain's limitations around complex workflows, state management, and observability by modeling the entire workflow as a graph instead of a linear chain."
