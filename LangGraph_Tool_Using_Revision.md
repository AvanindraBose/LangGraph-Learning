# LangGraph — Tool Using Revision

## 1. LangGraph Basics

LangGraph is a framework for building **stateful, graph-based LLM and agentic workflows**.

A graph consists mainly of:

- **State** — data carried through the workflow
- **Nodes** — functions/components that perform work
- **Edges** — determine where execution goes
- **Conditional edges** — dynamically choose the next node

```text
START
  ↓
Node
  ↓
Node
  ↓
END
```

---

## 2. What Is a Tool?

An LLM can generate text, but a tool gives it access to an external capability.

Examples:

- Calculator
- Database
- Web search
- Weather API
- Python function
- Internal company API

Typical flow:

```text
User
 ↓
LLM
 ↓
Does it need a tool?
 ├── No → Final Answer
 └── Yes
      ↓
   Tool Call
      ↓
   Tool Execution
      ↓
   Tool Result
      ↓
      LLM
```

---

## 3. Creating a Tool

A Python function can be exposed as a LangChain tool:

```python
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
```

A tool has:

- Name
- Description
- Input schema
- Implementation

The description and schema help the LLM understand when and how to use the tool.

---

## 4. Binding Tools to the LLM

Tools can be made available to the model:

```python
llm_with_tools = llm.bind_tools([add])
```

Important:

> **Binding a tool does not execute the tool.**

It only tells the model which tools are available.

The model may then return a **tool call**.

---

## 5. Tool Call vs Tool Execution

These are different things.

If the user asks:

```text
What is 10 + 20?
```

The LLM might produce:

```text
Tool call:
add(a=10, b=20)
```

At this point the LLM has **requested** the tool. The Python function still needs to execute.

```text
LLM
 ↓
Tool Call
 ↓
Tool Execution
 ↓
Tool Result
```

---

# 6. ToolNode

`ToolNode` is a prebuilt LangGraph node for executing tools.

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode([add])
```

It handles the mechanics of:

1. Reading tool calls from the graph state
2. Identifying the requested tool
3. Passing the arguments
4. Executing the tool
5. Producing the tool result
6. Adding the result back to the message state

Conceptually:

```text
State
 ↓
ToolNode
 ↓
Tool execution
 ↓
Tool result
```

---

# 7. Message State

Tool workflows commonly use a message-based state.

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

The message history can contain:

```text
HumanMessage
    ↓
AIMessage (tool call)
    ↓
ToolMessage (tool result)
    ↓
AIMessage (final answer)
```

This history allows the LLM to see what happened during the workflow.

---

# 8. Nodes

A typical tool-using graph has two important nodes:

```python
builder.add_node("llm", call_model)
builder.add_node("tools", ToolNode(tools))
```

Here:

- `llm` is your LLM node
- `tools` is the prebuilt `ToolNode`

---

# 9. Normal Edges

A normal edge always goes to the same destination.

```python
builder.add_edge("tools", "llm")
```

Meaning:

```text
ToolNode
   ↓
LLM
```

---

# 10. Conditional Edges

Conditional edges dynamically decide where execution should go.

For a tool-using agent:

```text
             LLM
              ↓
       Tool required?
          /       \
        Yes        No
         ↓          ↓
     ToolNode      END
```

Instead of always doing:

```text
LLM → ToolNode
```

the graph can choose:

```text
LLM → ToolNode
```

or:

```text
LLM → END
```

depending on the current state.

---

# 11. `tools_condition`

LangGraph provides a prebuilt routing function for this common pattern:

```python
from langgraph.prebuilt import tools_condition
```

It can be used as a conditional edge:

```python
builder.add_conditional_edges(
    "llm",
    tools_condition,
)
```

Conceptually:

```text
LLM
 │
 ├── AI message contains tool calls → ToolNode
 │
 └── No tool calls → END
```

So:

> **`tools_condition` is for routing.**

---

# 12. ToolNode vs tools_condition

This distinction is extremely important.

### `tools_condition`

Determines **where the graph should go**.

```text
"Does the AI message contain a tool call?"
```

### `ToolNode`

Determines **what to execute**.

```text
"Execute the requested tool."
```

Remember:

> **Condition = routing**
>
> **ToolNode = execution**

---

# 13. Complete Tool-Using Graph

A common architecture is:

```text
                    START
                      ↓
                     LLM
                      ↓
               tools_condition
                  /         \
                 /           \
          Tool required     No tool
               ↓              ↓
           ToolNode           END
               ↓
          Tool Result
               ↓
              LLM
               ↓
        tools_condition
```

The loop is important because the LLM needs to see the tool result before producing the final answer or deciding to call another tool.

---

# 14. Example Execution

User asks:

```text
What is 25 × 4?
```

Execution:

```text
User
 ↓
LLM
 ↓
Tool call: calculator(25, 4)
 ↓
ToolNode
 ↓
Tool result: 100
 ↓
LLM
 ↓
"25 × 4 = 100."
 ↓
END
```

---

# 15. Multiple Tools

An agent can have multiple tools:

```python
tools = [
    calculator,
    search_web,
    get_weather,
    get_customer_details
]

llm_with_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)
```

Conceptually:

```text
                    LLM
                     │
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
 Calculator      Web Search     Weather
       │             │             │
       └─────────────┼─────────────┘
                     ↓
                    LLM
```

The **LLM chooses which tool to request**.

The **ToolNode executes the requested tool**.

---

# 16. Tool-Using Agent Loop

A more general agent can perform multiple actions:

```text
LLM
 ↓
Decide action
 ↓
Tool
 ↓
Observe result
 ↓
LLM
 ↓
Decide next action
 ↓
Tool
 ↓
Observe result
 ↓
LLM
 ↓
Final Answer
```

LangGraph is useful because you can explicitly model and control this loop.

---

# 17. Tool Errors

Tools can fail.

Example:

```text
ToolNode
   ↓
Database unavailable
```

A production graph may handle this with:

```text
ToolNode
   ↓
 ┌──────────────┐
 │              │
Success        Error
 │              │
 ↓              ↓
LLM        Error Handler
               ↓
          Retry / END
```

Tool execution should therefore be considered part of the application's reliability design.

---

# 18. Tool Calling Is Not Automatically a Sophisticated Agent

A tool-enabled LLM can simply do:

```text
LLM
 ↓
Tool
 ↓
LLM
```

A more agentic workflow can repeatedly make decisions:

```text
LLM
 ↓
Decision
 ↓
Tool
 ↓
Observation
 ↓
Decision
 ↓
Tool
 ↓
Observation
 ↓
Final Answer
```

LangGraph gives you explicit control over this workflow.

---

# 19. Mental Model

Remember this:

```text
                    ┌─────────────┐
                    │    START    │
                    └──────┬──────┘
                           ↓
                    ┌─────────────┐
                    │     LLM     │
                    └──────┬──────┘
                           ↓
                    tools_condition
                       /         \
                     /             \
              Tool required       No tool
                  ↓                  ↓
             ┌─────────┐           END
             │ToolNode │
             └────┬────┘
                  ↓
             Tool Result
                  ↓
                 LLM
                  ↓
           condition again
```

---

# 20. Quick Revision Table

| Concept | Meaning |
|---|---|
| **State** | Data carried through the graph |
| **Node** | Unit of work |
| **Edge** | Determines the next node |
| **Conditional Edge** | Dynamically determines the next node |
| **Tool** | External function/capability available to the LLM |
| **`bind_tools()`** | Makes tools available to the LLM |
| **Tool Call** | LLM's request to execute a tool |
| **ToolNode** | Executes tool calls |
| **`tools_condition`** | Routes based on whether tool calls exist |
| **Tool Result** | Output returned by a tool |
| **Agent Loop** | LLM → Tool → LLM → Tool → ... → Final Answer |

---

# 21. Three Things to Remember

### 1. The LLM decides

```text
"Should I use a tool?"
```

### 2. `tools_condition` routes

```text
Tool call exists → ToolNode
No tool call → END
```

### 3. `ToolNode` executes

```text
Run the requested tool and return its result.
```

Together:

```text
LLM
 ↓
tools_condition
 ↓
ToolNode
 ↓
Tool Result
 ↓
LLM
 ↓
END / ToolNode
```

This is the foundation for understanding tool-using agents in LangGraph.
