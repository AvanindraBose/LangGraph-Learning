# Short-Term Memory in LLMs: Complete Guide

## Table of Contents
1. [Simple Definition](#simple-definition)
2. [How It Works](#how-it-works)
3. [Key Concepts](#key-concepts)
4. [Scenarios & Problems](#scenarios--problems)
5. [Solutions & Strategies](#solutions--strategies)
6. [Real-World Examples](#real-world-examples)
7. [Q&A](#qa)

---

## Simple Definition

### What is Short-Term Memory?

**Short-term memory** is the conversation history that an LLM can see and use RIGHT NOW.

```
Simple Analogy:
───────────────
Person A: "My name is John"
Person B: "Nice to meet you John"  ← Can remember "John" from 1 sec ago
Person B: "What did you say 10 minutes ago?" ← Can't remember that far back

That's short-term memory!
```

### In LLM Terms:

```
User: "My favorite color is blue"      ← Message 1
User: "What color did I mention?"      ← Message 2
LLM: "You said blue"                   ← Can remember (in short-term)
        because message 1 is still in context

Days later...
User: "What color did I mention?"
LLM: "I don't know"                    ← Can't remember (beyond short-term)
        message from days ago is gone
```

---

## How It Works

### The Context Window

```
THE BRAIN (Token Limit):
─────────────────────────

GPT-4: 8,192 tokens max
Claude 3 Sonnet: 200,000 tokens max
Claude 3 Opus: 200,000 tokens max

Token = roughly a word (not exact)

┌─────────────────────────────────────────────────┐
│ Context Window (e.g., 8,192 tokens)             │
│ ┌─────────────────────────────────────────────┐ │
│ │ [System Message] [Past Messages] [New Input] │ │
│ │ 2,000 tokens    3,000 tokens    1,000 tokens│ │
│ │ ← Everything in here is SHORT-TERM memory  │ │
│ └─────────────────────────────────────────────┘ │
│ Everything OUTSIDE is gone (not in memory)     │
└─────────────────────────────────────────────────┘
```

### Real-Time Processing

```
User Sends Message:
        ↓
┌──────────────────────────┐
│ Construct Message List:  │
│ ├─ System prompt         │
│ ├─ Past messages         │
│ └─ New message           │
└──────────────────────────┘
        ↓
    Fit in context window?
        ↓
   ├─ YES → Send to LLM ✅
   └─ NO → Drop old messages ❌
        ↓
   LLM generates response
        ↓
   Response sent to user
```

---

## Key Concepts

### 1. Context Window

The total amount of text (tokens) the LLM can process at once.

```
Small Context (like GPT-3.5):
├─ 4,096 tokens
├─ ~1-2 pages of text
└─ Short conversations only

Medium Context (like GPT-4):
├─ 8,192 - 32,000 tokens
├─ ~5-20 pages of text
└─ Medium conversations

Large Context (like Claude 3):
├─ 100,000 - 200,000 tokens
├─ ~50-100 pages of text
└─ Very long conversations + documents

Problem:
├─ More context = slower + more expensive
├─ Need to manage carefully
└─ Can't store forever
```

### 2. Token Counting

```
Text: "Hello, how are you?"
├─ Word count: 4 words
├─ Token count: ~5-6 tokens
└─ Tokens slightly more than words

Formula:
├─ 1 token ≈ 4 characters
├─ 1 token ≈ 0.75 words
└─ Variable based on text

Example:
┌──────────────────────────────┐
│ "The quick brown fox"        │
│ 4 words = ~5-6 tokens        │
└──────────────────────────────┘
```

### 3. Message Role Types

```
SYSTEM MESSAGE:
├─ Instructions to the LLM
├─ How to behave
└─ Example: "You are a helpful assistant"

ASSISTANT MESSAGE:
├─ Previous LLM responses
├─ Part of conversation history
└─ Shows the assistant's reasoning

HUMAN/USER MESSAGE:
├─ User's messages
├─ Questions/statements
└─ Current or past user input
```

### 4. Summarization Strategy

```
Instead of keeping ALL old messages:
│
├─ Summarize old conversations
├─ Keep key facts
├─ Compress history

Example:
OLD (uses many tokens):
├─ Message 1: "I work as a software engineer"
├─ Message 2: "I live in New York"
├─ Message 3: "I like Python"
└─ Total: 20 tokens

NEW (summarized, uses fewer tokens):
├─ Summary: "User is a Python engineer in NY"
└─ Total: 7 tokens

Memory saved: 13 tokens
```

---

## Scenarios & Problems

### Scenario 1: Long Conversation (Context Overflow)

```
Problem:
────────
User and LLM chat for 1 hour:
├─ User: "Hi, my name is Alice"
├─ LLM: "Nice to meet Alice"
├─ User: "I work in tech"
├─ LLM: "That's interesting"
├─ ... (100 more messages)
├─ User: "What's my name?"
└─ LLM: ???

Accumulated messages:
├─ First 50 messages = 10,000 tokens
├─ Middle 50 messages = 10,000 tokens
├─ Total = 20,000 tokens
├─ Context limit = 8,192 tokens
├─ PROBLEM: Can't fit everything!

Result:
├─ Oldest messages dropped
├─ LLM forgets the beginning
├─ Can't answer "What's my name?" ❌
```

### Scenario 2: Token Limit Exceeded

```
User tries to paste a 50-page document:
├─ Document = 100,000 tokens
├─ Context window = 8,192 tokens
├─ Can't fit!

Error:
├─ "Prompt too long"
├─ Request rejected
└─ User can't get help ❌

Solution needed:
├─ Chunk the document
├─ Process piece by piece
├─ Summarize sections
```

### Scenario 3: Forgetting Mid-Task

```
Multi-step task:
────────────────
1. User: "Write a 5-section essay about climate"
2. LLM: Writes section 1
3. LLM: Writes section 2
4. LLM: Writes section 3
5. User: "Now write section 4"

Problem:
├─ Context now full:
│  ├─ System prompt: 1,000 tokens
│  ├─ User request: 500 tokens
│  ├─ Section 1: 2,000 tokens
│  ├─ Section 2: 2,000 tokens
│  ├─ Section 3: 2,000 tokens
│  └─ Total: 7,500 tokens (almost full!)
│
├─ New request drops oldest messages
├─ LLM forgets the essay topic
└─ Writes misaligned section 4 ❌
```

### Scenario 4: Context Interference

```
Too much history causes confusion:

Conversation history:
├─ [10 messages about Python]
├─ [10 messages about JavaScript]
├─ [10 messages about Rust]
├─ [10 messages about Go]
├─ User: "How do I loop?"

LLM might:
├─ Confuse which language
├─ Mix up concepts
├─ Provide wrong syntax ❌

Problem:
└─ Too much irrelevant history in context
```

### Scenario 5: Memory for Decisions

```
Multi-turn conversation:

Turn 1:
├─ User: "I want to buy a laptop"
├─ LLM: "What's your budget?"
├─ User: "$1000"

Turn 2 (new message):
├─ LLM: "What budget?"  ❌
├─ Why? Previous conversation dropped from context

Turn 10 (much later):
├─ User: "Can I afford this $800 laptop?"
├─ LLM: Can't reference the $1000 budget from turn 1
└─ Has to ask again ❌
```

---

## Solutions & Strategies

### Strategy 1: Message Windowing (Sliding Window)

```
Keep only the LAST N messages:

Conversation:
├─ Message 1 (old) - DROPPED
├─ Message 2 (old) - DROPPED
├─ Message 3 ✅
├─ Message 4 ✅
├─ Message 5 ✅
└─ Message 6 (newest) ✅

Keep last 4 messages, drop older ones

Code Example:
──────────────
def keep_last_n_messages(messages, n=10):
    return messages[-n:]  # Keep last 10

messages = [msg1, msg2, ... msg50]
recent = keep_last_n_messages(messages, 10)
# Now only last 10 messages in context
```

### Strategy 2: Summarization

```
Compress old messages into summary:

Before (50 messages = 20,000 tokens):
├─ Message 1-49: Full history
└─ Message 50: New question

After (summarization):
├─ Summary: "User asked about Python, we discussed functions, classes, decorators. User wants to learn async/await"
│            (500 tokens instead of 19,500!)
├─ Message 50: New question
└─ Total: ~1,000 tokens (saved 19,000!)

Implementation:
──────────────
messages_to_summarize = messages[:-1]  # All except last
summary = llm.summarize(messages_to_summarize)

new_context = [
    SystemMessage(content=summary),
    messages[-1]  # Latest message
]
```

### Strategy 3: Explicit Memory Store (Long-Term)

```
Don't rely on short-term alone:

Conversation Flow:
│
├─ User asks something
├─ LLM responds
├─ Store key facts in database
├─ SHORT-TERM: Keep only recent messages (4 messages)
├─ LONG-TERM: Store facts in vector DB
│
User asks later: "What did I say about Python?"
├─ Query vector DB (long-term): Get Python conversation summary
├─ Combine with current context (short-term)
└─ LLM can answer with both! ✅

Benefits:
├─ Context window stays manageable
├─ No loss of important facts
└─ Solves both short + long-term memory
```

### Strategy 4: Prompt Injection for Context

```
Include crucial context in system message:

System Message:
├─ "You are helping a user"
├─ "Key fact 1: User is a Python developer"
├─ "Key fact 2: User works in NYC"
├─ "Key fact 3: User wants to learn async/await"
│
├─ This takes up ~200 tokens (small cost)
├─ Ensures facts are ALWAYS available
└─ Works even if conversation history dropped

Advantage:
└─ Important context never forgotten
```

### Strategy 5: Relevance Filtering

```
Instead of keeping last N messages:
Keep MOST RELEVANT messages

Example:
┌───────────────────────────────┐
│ All Messages (100)            │
│ ├─ Messages about Python ✅   │
│ ├─ Messages about JavaScript  │
│ ├─ Messages about AI ✅       │
│ └─ Messages about lunch       │
└───────────────────────────────┘
        ↓
        Filter (keep relevant to current question)
        ↓
┌───────────────────────────────┐
│ Filtered Messages (20)        │
│ ├─ Messages about Python ✅   │
│ └─ Messages about AI ✅       │
└───────────────────────────────┘

Current question: "How do I use async in Python?"
├─ Relevant: Python messages ✅
├─ Relevant: AI messages (maybe, depends on context)
└─ Not relevant: JavaScript, lunch ❌
```

---

## Real-World Examples

### Example 1: ChatGPT-Like Conversation

```
User: "What's the capital of France?"
LLM: "Paris"

Short-term memory:
├─ User message: "What's the capital of France?"
├─ LLM response: "Paris"
└─ Takes ~20 tokens

User (5 minutes later): "What was my first question?"
LLM: "What's the capital of France?"  ✅
└─ Still in context (5 minutes = short-term)

User (2 hours later): "What was my first question?"
LLM: "I don't remember"  ❌
└─ Dropped from short-term (too old)
└─ Would need long-term memory to recall
```

### Example 2: Code Generation Task

```
Task: Generate a complete web app

User: "Create a React app with login page"
LLM: Writes Login.jsx (2,000 tokens)

User: "Now add a dashboard"
LLM: Writes Dashboard.jsx
     But context getting full...
     ├─ System: 1,000 tokens
     ├─ User request: 500 tokens
     ├─ Login.jsx: 2,000 tokens
     ├─ New dashboard request: 500 tokens
     └─ Total: 4,000 tokens (good)

User: "Now add styling with CSS"
LLM: Writes CSS
     ├─ Context now: 5,500 tokens
     ├─ Still has Login.jsx memory
     └─ Styling consistent ✅

User (message 20): "Fix the auth bug"
LLM: ❌ Context overflowing!
     ├─ Lost Login.jsx details
     ├─ Can't remember original design
     └─ Might suggest wrong fix

Solution: Save components to files, summarize design
```

### Example 3: Customer Support Bot

```
Conversation:

Message 1:
├─ Customer: "I can't login"
├─ Bot: Troubleshoots
├─ Customer: "Still broken"

Message 5:
├─ Customer: "Reset my password"
├─ Bot: Sends reset link
├─ Customer: "Password reset worked"

Message 10:
├─ Customer: "Now I can't reset my profile"
├─ Bot: Should remember the password reset issue ✅
└─ Can reference past solution

Message 30 (end of conversation):
├─ Customer: "What was my original issue?"
├─ Bot: ❌ Might forget (long conversation)

Solution:
├─ Keep summary: "User had login issues, reset password, now updating profile"
├─ This 20-token summary keeps full context
└─ No loss of important info
```

### Example 4: Research Assistant

```
User: "Summarize the impact of AI on healthcare"
LLM: Writes 3-page response (5,000 tokens)

User: "Expand the diagnosis section"
LLM: Expands section
     ├─ Needs to remember original structure
     ├─ Short-term memory helps ✅
     └─ Context: 7,000 tokens (still good)

User: (Message 15) "Compare with finance industry impact"
LLM: ❌ Might forget healthcare details!
     ├─ Context overflowing
     ├─ Original research dropped
     └─ Might give poor comparison

Solution:
├─ Keep healthcare summary in context
├─ Build comparison from summaries
└─ More efficient use of tokens
```

---

## Q&A

### Q1: What is short-term memory in simple terms?

**Answer:**
Short-term memory is what the LLM can see and remember RIGHT NOW during a conversation. It's limited by the context window (token limit). Once you exceed it, older messages are forgotten.

```
Analogy: Like a person's short-term memory
├─ You remember what someone said 5 minutes ago (short-term)
├─ You forget what they said 2 hours ago (unless you wrote it down)
└─ Writing it down = long-term memory (database)
```

### Q2: Why do LLMs forget after long conversations?

**Answer:**
Every LLM has a **context window limit** (maximum tokens it can process). Once you add enough messages to exceed this limit, old messages get dropped to make room for new ones.

```
Context window = 8,192 tokens

Messages:
├─ Message 1: 1,000 tokens ❌ DROPPED
├─ Message 2: 1,000 tokens ❌ DROPPED
├─ Message 3: 1,000 tokens ✅ KEPT
├─ Message 4: 1,000 tokens ✅ KEPT
├─ Message 5: 1,000 tokens ✅ KEPT
└─ New message: 3,000 tokens ✅ KEPT
   └─ Total: ~7,000 tokens (fits!)
```

### Q3: How can I make an LLM remember important facts?

**Answer:**
Three main strategies:

1. **Keep messages in context** - Don't exceed token limit
2. **Summarize old messages** - Compress history
3. **Use system prompt** - Put key facts there (always visible)
4. **Store in database** - Retrieve relevant facts when needed (long-term memory)

### Q4: What's the difference between short-term and long-term memory?

**Answer:**

```
SHORT-TERM (Current context):
├─ What's visible to LLM right now
├─ Limited (token window)
├─ Fast (immediate access)
└─ Temporary (lost after conversation)

LONG-TERM (Persistent storage):
├─ Stored in database/vector store
├─ Unlimited (theoretically)
├─ Slower (must retrieve)
└─ Permanent (survives conversation)
```

### Q5: How many messages can an LLM remember?

**Answer:**
Depends on message length and context window:

```
GPT-4 (8,192 tokens):
├─ If each message = 500 tokens
├─ Can keep: 8,192 ÷ 500 = ~16 messages

Claude 3 (200,000 tokens):
├─ If each message = 500 tokens
├─ Can keep: 200,000 ÷ 500 = ~400 messages

Important:
├─ Also need room for system prompt
├─ Also need room for new response
├─ So practical limit is lower
```

### Q6: Should I summarize or keep all messages?

**Answer:**
It depends:

**Keep all messages when:**
- Short conversations (< 20 messages)
- Messages are short
- Need full context

**Summarize when:**
- Long conversations (> 50 messages)
- Saving tokens is important
- Only recent details matter

### Q7: How do I prevent forgetting important facts?

**Answer:**
```
Best practice:
│
├─ SHORT-TERM: Keep recent messages in context
├─ SYSTEM PROMPT: Put critical facts here
└─ LONG-TERM: Store in database for later

Example implementation:

system_prompt = """
You are a helpful assistant.

Key user facts:
- Name: Alice
- Works in: Tech/Python
- Location: NYC

Use this information for all responses.
"""

messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=last_5_messages),
    # Keep last 5 messages in context
    # Critical facts in system prompt
    # Old details in database
]

response = llm.invoke(messages)
```

### Q8: What happens if I send a very long message?

**Answer:**
```
If message exceeds context window:

User sends: 50-page document (100,000 tokens)
Context limit: 8,192 tokens

Result:
├─ ❌ Error: "Prompt too long"
├─ Request rejected
└─ User can't send document

Solutions:
├─ Split document into chunks
├─ Send one chunk at a time
├─ LLM processes piece by piece
├─ Summarize and aggregate results
```

### Q9: Can I increase the context window?

**Answer:**
Not really. Context window is a **model property**, not configurable:

```
GPT-3.5: 4,096 tokens (fixed)
GPT-4: 8,192 tokens (fixed, newer versions have 32k/128k)
Claude 3: 200,000 tokens (fixed)

You can't increase them, but you can:
├─ Choose a model with larger window
├─ Manage tokens efficiently (summarization)
├─ Use multiple requests (chain of thought)
└─ Combine with long-term memory
```

### Q10: How do I design a system with both short and long-term memory?

**Answer:**
```
Architecture:

USER INPUT
    ↓
RETRIEVE from Long-Term (Vector DB)
    ├─ Find relevant past conversations
    └─ Extract key facts
    ↓
BUILD CONTEXT:
    ├─ System prompt (facts, instructions)
    ├─ Retrieved summaries (long-term)
    ├─ Recent messages (short-term)
    └─ Current question
    ↓
Check token count:
    ├─ If over limit → Summarize more
    ├─ If under limit → Keep more context
    └─ If good → Send to LLM
    ↓
LLM PROCESSES (short-term memory)
    ↓
STORE important facts:
    ├─ Extract facts from response
    ├─ Save to vector DB (long-term)
    └─ Ready for next conversation

Result:
├─ User feels like LLM remembers everything
├─ Efficient token usage
├─ Handles long conversations
└─ Works across multiple sessions
```

---

## Key Strategies for Managing Short-Term Memory

### ✅ DO:

```
1. Monitor token usage
   └─ Count before sending to LLM

2. Summarize old messages
   └─ Compress history periodically

3. Use system prompts strategically
   └─ Critical facts always available

4. Implement sliding window
   └─ Keep last N messages only

5. Combine with long-term storage
   └─ Best of both worlds

6. Test with long conversations
   └─ Catch memory issues early

7. Log what gets dropped
   └─ Understand what's being forgotten
```

### ❌ DON'T:

```
1. Assume LLM remembers everything
   └─ It doesn't (limited context)

2. Keep unlimited message history
   └─ Eventually exceeds token limit

3. Ignore token counting
   └─ Leads to surprising failures

4. Repeat information every message
   └─ Wastes tokens

5. Store everything in context
   └─ Better to use database

6. Assume older messages matter
   └─ Relevance filtering better

7. Mix important + irrelevant data
   └─ Causes confusion/errors
```

---

## Common Patterns

### Pattern 1: Windowing

```python
# Keep only last N messages
def keep_recent_messages(messages, n=10):
    return messages[-n:]
```

### Pattern 2: Summarization

```python
# Compress old messages
def compress_history(messages):
    old = messages[:-1]
    recent = messages[-1]
    summary = llm_summarize(old)
    return [summary, recent]
```

### Pattern 3: Dual Memory

```python
# Short-term (context) + Long-term (database)
recent_context = messages[-5:]  # Last 5
stored_facts = database.retrieve(query)  # From DB
combined = [system_prompt] + stored_facts + recent_context
```

---

## Real-World Problem Solving

### Problem: Long Customer Service Chat

```
Challenge: 100-message conversation
│
├─ Context window: 8,192 tokens
├─ Average message: 500 tokens
├─ All 100 messages: 50,000 tokens (TOO MUCH!)

Solution:
├─ Keep last 10 messages in context (5,000 tokens)
├─ Summarize messages 1-90:
│  "Customer reported billing issue, was refunded, now asking about refund status"
│  └─ Only 30 tokens!
├─ Total context: ~5,030 tokens ✅

Result:
├─ Full history accessible
├─ Efficient token usage
└─ Bot can answer about refund status
```

### Problem: Multi-Session Memory

```
Challenge: User comes back days later
│
Day 1:
├─ User: "I want to learn Python"
├─ Bot: Teaches Python basics
└─ Conversation ends (memory lost)

Day 7:
├─ User: "Continue teaching"
├─ Bot: "What's your goal?" ❌ (forgot!)

Solution:
├─ Save to database on Day 1:
│  "User_123: wants to learn Python, completed basics, interested in Web"
├─ Retrieve on Day 7:
│  "Welcome back! Let's continue with web frameworks since you completed basics"
└─ User: "Perfect!" ✅
```

---

## Performance Considerations

### Token Usage Impact

```
SHORT MESSAGE:
├─ "Hi" = 1 token
├─ Small response = 10 tokens
└─ Total: 11 tokens

LONG MESSAGE:
├─ "Can you write a detailed essay about..." = 100 tokens
├─ Large response = 1,000 tokens
└─ Total: 1,100 tokens

Implication:
├─ One long message uses as many tokens as 100 short ones
├─ Token efficiency matters for cost + speed
└─ Summarization saves significantly
```

### Speed Implications

```
Smaller context window:
├─ Fewer tokens to process
├─ Faster response time
└─ Lower latency

Larger context window:
├─ More tokens to process
├─ Slower response time
├─ Higher latency
└─ Example: 8k tokens = ~1 second, 50k tokens = ~5 seconds

Tradeoff:
├─ More context = better quality but slower
├─ Less context = faster but might miss context
└─ Summarization helps both (less tokens, keeps meaning)
```

---

## Summary Checklist

- [ ] Understand context window limits
- [ ] Know your model's token limit
- [ ] Count tokens before sending
- [ ] Implement message windowing if needed
- [ ] Consider summarization for long chats
- [ ] Use system prompts for critical facts
- [ ] Plan for long-term memory separately
- [ ] Test with long conversations
- [ ] Monitor what gets dropped
- [ ] Combine short + long-term memory

---

**Last Updated**: 2026
**Purpose**: Understanding Short-Term Memory in LLMs
**Difficulty**: Beginner to Intermediate