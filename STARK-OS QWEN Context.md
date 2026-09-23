# STARK-OS — QWEN PROJECT CONTEXT

## 1. PROJECT IDENTITY

Project name: STARK-OS

STARK-OS is a personal AI workstation / personal AI operating environment inspired by Tony Stark's JARVIS/STARK computer concept.

It is NOT intended to replace macOS.

It is a software layer running on macOS that provides:

- Natural-language interaction
- AI assistance
- Memory
- Context awareness
- Command execution
- System information
- Intelligent intent detection
- Future automation
- Future voice interaction
- Future advanced UI
- Personal productivity capabilities

The goal is to evolve STARK-OS into a reliable personal AI workstation rather than a simple chatbot.

---

# 2. CURRENT USER

The developer/user is Atharva.

The user is a final-year engineering student and is actively developing STARK-OS as a serious long-term personal software project.

The user prefers practical implementation over theoretical explanations.

When modifying STARK-OS:

1. Explain what is being changed.
2. Explain why it is necessary.
3. Prefer minimal, safe changes.
4. Do not rewrite working architecture unnecessarily.
5. Do not introduce unnecessary dependencies.
6. Do not break existing functionality while adding new functionality.
7. Test changes before declaring them complete.

---

# 3. DEVELOPMENT ENVIRONMENT

Primary machine:

- MacBook Air M5
- Apple Silicon
- macOS

Development environment:

- VS Code
- Git
- Python
- Python virtual environment (`venv`)

The project is located approximately at:

`~/Documents/STARK-OS`

The project is a Git repository.

Known repository:

`STARK-OS`

Important:

Do not assume Linux-only commands or NVIDIA/CUDA functionality.

The primary development environment is Apple Silicon macOS.

---

# 4. CORE TECHNOLOGY

Primary language:

Python

Current AI integration has used Google's Gemini API.

Environment variable used by the AI layer:

`GEMINI_API_KEY`

IMPORTANT:

Never hard-code API keys.

Never print API keys.

Never commit `.env` files or credentials.

Use environment variables for secrets.

---

# 5. HIGH-LEVEL ARCHITECTURE

STARK-OS currently follows a modular architecture.

Conceptual flow:

USER
  ↓
STARK interface
  ↓
Command processing
  ↓
Intent detection
  ↓
Context resolution
  ↓
Brain / decision layer
  ↓
Command execution OR AI engine
  ↓
Memory / system / response
  ↓
USER

The important architectural principle is:

STARK should first understand what the user is trying to do.

It should not blindly send every command to an external AI model.

Deterministic commands should remain deterministic.

AI should be used when reasoning or language understanding is actually required.

---

# 6. IMPORTANT PROJECT COMPONENTS

Known important directories/files include:

## core/

Contains the main STARK reasoning and command architecture.

Important files:

- `core/stark.py`
- `core/brain.py`
- `core/context.py`
- `core/commands.py`
- `core/intent.py`
- `core/ai_context.py`

These files are highly important.

Do not casually rewrite them.

---

# 7. core/stark.py

This is the primary STARK runtime/interface.

It starts the STARK-OS interactive session.

Typical experience:

STARK-OS

PERSONAL AI WORKSTATION

Core System: ACTIVE
Memory System: ACTIVE
AI Assistant: ACTIVE

Then STARK greets the user and accepts commands.

Example conceptual interaction:

You › what is python

STARK should process the request and respond appropriately.

---

# 8. core/intent.py

This file is responsible for intent detection.

STARK supports deterministic intents such as:

- exit
- quit
- hello
- time
- remember
- recall
- help

It has also been extended to understand natural-language memory commands.

Examples:

`remember my favorite language is Python`

`please remember that my favorite color is black`

`remember that my favorite movie is Iron Man`

Natural-language prefixes should be normalized before intent processing.

Do not remove existing intent functionality while adding new intents.

---

# 9. core/commands.py

Responsible for command processing and command normalization.

The project has previously added normalization for conversational prefixes such as:

`please remember that ...`

`remember that ...`

The command system should convert natural-language variations into predictable internal representations.

Do not make the parser unnecessarily complicated.

Prefer clear normalization rules and small deterministic functions.

---

# 10. core/context.py

This is one of the most important STARK files.

It handles conversational context and resolution.

It has previously included functionality for:

- command normalization
- conversational context
- resolving references such as:
  - this
  - that
  - those
  - it
- subject extraction
- previous conversation references

Example:

User:
`What is Python?`

Then:

`When was it created?`

STARK should understand that "it" refers to Python.

Context resolution should preserve conversational continuity.

Do not remove context functionality when modifying the file.

---

# 11. core/brain.py

The brain layer coordinates STARK's response process.

Conceptually:

1. Receive command.
2. Normalize command.
3. Detect intent.
4. Resolve context.
5. Check memory if necessary.
6. Execute deterministic functionality if possible.
7. Send unknown/reasoning-heavy requests to AI.
8. Produce response.

The brain should remain the central coordinator rather than placing all logic into one file.

---

# 12. core/ai_context.py

Responsible for preparing relevant context for the AI layer.

AI context can include:

- current user request
- conversation context
- memory
- relevant STARK state

Do not dump the entire project or entire memory database into every AI request.

Context should be relevant and controlled.

---

# 13. ai/engine.py

This is the AI integration layer.

Previously STARK used Google's Gemini API.

Important concept:

The AI engine should be isolated from the rest of STARK.

The rest of STARK should not directly depend on Gemini implementation details.

The AI engine should expose a simple interface, conceptually:

`ai_engine.ask(...)`

The project has already tested this successfully.

Example:

`ai_engine.ask("Say hello in one short sentence.")`

returned a STARK-style response.

The AI provider may change in the future.

Therefore:

DO NOT spread Gemini-specific code throughout the project.

Keep provider-specific implementation inside the AI layer.

---

# 14. MEMORY SYSTEM

STARK has a persistent memory system.

A previous memory structure included:

```json
{
    "user": {
        "favorite language": "Python",
        "favorite color": "black",
        "favorite movie": "Iron Man",
        "favorite superhero": "Iron Man"
    },
    "history": []
}
```

The actual current memory file should ALWAYS be inspected before making assumptions.

Memory is intended to support:

- user preferences
- remembered facts
- conversation history
- future personalization

Memory must not silently corrupt existing data.

When changing memory code:

1. Preserve existing entries.
2. Handle missing files safely.
3. Handle malformed JSON safely.
4. Avoid duplicate entries where appropriate.
5. Test both saving and recalling.

---

# 15. CURRENT NATURAL-LANGUAGE MEMORY CAPABILITY

STARK has already been improved to understand natural-language memory commands.

Examples:

`remember my favorite language is Python`

`please remember that my favorite color is black`

`remember my favorite superhero is Iron Man`

The system should store the key/value information.

Later:

`recall`

should retrieve relevant memory.

Important:

There was previously a bug involving `recall` that produced a traceback.

If working on memory, verify that this regression does not return.

---

# 16. EXISTING DEVELOPMENT HISTORY

Important functionality previously implemented includes:

- Live system health status
- Intent-aware interaction states
- Live system monitoring dashboard
- Gemini function calling improvements
- AI engine improvements
- Memory handling improvements
- STARK interface improvements
- Natural-language memory intents
- Conversational prefix normalization
- Context resolution
- Subject extraction
- Conversation continuity

Previously used Git commits included concepts such as:

- Add live system health status
- Fix Gemini function calling and improve AI engine
- Add intent-aware interaction states
- Add live system monitoring dashboard
- Improve memory handling and STARK interface
- Improve natural language memory intents

Do not recreate these features from scratch.

Inspect the current implementation first.

---

# 17. GIT BRANCHING

A feature branch named:

`natural-language-intents`

was previously created and pushed.

The project also has:

`main`

and:

`origin/main`

Before making major changes:

Run:

`git status`

Then inspect:

`git branch`

and:

`git log --oneline --decorate -10`

Never blindly overwrite work.

---

# 18. DEVELOPMENT RULE

The most important rule:

## INSPECT BEFORE MODIFYING.

Before changing a file:

1. Read the file.
2. Understand its role.
3. Search for callers/usages.
4. Determine dependencies.
5. Make the smallest reasonable change.
6. Run tests.
7. Run the application if appropriate.
8. Check Git diff.

Do not say "fixed" without testing.

---

# 19. SAFE MODIFICATION STRATEGY

For every feature:

### STEP 1 — Understand

Explain:

- What currently exists?
- Where should the new functionality live?
- What existing behavior could be affected?

### STEP 2 — Plan

Provide a short implementation plan.

### STEP 3 — Modify

Change only necessary files.

### STEP 4 — Test

Run relevant tests.

At minimum where appropriate:

`python -m ...`

or the project's test command.

### STEP 5 — Verify

Run:

`git diff --check`

Then:

`git diff`

### STEP 6 — Report

Tell the developer:

- files changed
- what changed
- why
- tests performed
- remaining issues

---

# 20. DO NOT DO THIS

Never:

- rewrite the entire project unnecessarily
- delete working functionality
- replace architecture without discussion
- hard-code API keys
- expose secrets
- create fake implementations
- claim tests passed when they were not run
- assume a file contains something without reading it
- introduce huge dependencies for tiny features
- duplicate existing functionality
- modify unrelated files
- silently change public interfaces
- remove context handling
- remove memory handling
- replace deterministic commands with AI unnecessarily

---

# 21. AI VS DETERMINISTIC LOGIC

STARK should use deterministic code for predictable operations.

Examples:

`what time is it`

`help`

`exit`

`remember ...`

`recall`

System status

These should not require an LLM unless there is a specific reason.

Use the AI model for:

- reasoning
- explanation
- coding assistance
- complex natural-language requests
- questions outside deterministic command capabilities
- future planning/agentic tasks

Architecture goal:

DETERMINISTIC CORE + AI REASONING

not:

EVERYTHING → LLM

---

# 22. QWEN CODER'S ROLE

Qwen should act as a senior software engineer working inside the STARK-OS repository.

Qwen is not the owner of the project.

The developer is the owner.

Qwen must:

- inspect before editing
- explain proposed changes
- preserve architecture
- make incremental changes
- test changes
- respect existing code
- point out uncertainty
- never fabricate files/functions
- never assume undocumented behavior

When asked to implement something, first inspect the relevant files.

---

# 23. WHEN USER SAYS "FIX IT"

Do NOT immediately rewrite everything.

Instead:

1. Reproduce the problem.
2. Locate the source.
3. Identify root cause.
4. Fix root cause.
5. Test the fix.
6. Check for regression.

---

# 24. WHEN USER SAYS "ADD FEATURE X"

Use this process:

1. Search repository for related functionality.
2. Identify the correct architectural layer.
3. Explain the implementation plan.
4. Implement.
5. Test.
6. Show changed files.
7. Explain how to use the new feature.

---

# 25. TERMINAL COMMAND SAFETY

Before running destructive commands, ask for confirmation.

Examples:

- `rm -rf`
- deleting project directories
- resetting Git history
- force pushing
- deleting branches
- overwriting important files

Never perform destructive operations merely because they appear convenient.

Prefer reversible operations.

---

# 26. DEPENDENCY RULE

Before adding a dependency:

Ask:

1. Is it really necessary?
2. Can Python standard library solve this?
3. Is an existing project dependency already capable of doing it?
4. Does it work on Apple Silicon/macOS?
5. Does it increase project complexity?

Avoid dependency bloat.

---

# 27. FUTURE STARK-OS DIRECTION

STARK-OS may eventually include:

## Intelligence

- better natural-language understanding
- long-term memory
- contextual reasoning
- planning
- task decomposition

## System control

- macOS system information
- application launching
- file operations
- process monitoring
- system automation

## AI

- local models
- remote models
- model switching
- provider abstraction
- local/private inference

## Voice

- speech recognition
- speech synthesis
- wake word
- conversational voice interface

## UI

- futuristic but professional interface
- system monitoring
- AI activity
- memory visualization
- command history
- animations

Design direction:

Premium professional workstation.

Avoid excessive "sci-fi poster" visual clutter.

The interface should feel inspired by Stark technology while remaining usable and professional.

---

# 28. LOCAL AI DIRECTION

The project may eventually use local/open-source coding and AI models.

The current developer has installed Qwen2.5-Coder.

Do not assume the exact Qwen model size or runtime.

First inspect the actual installation/environment.

Possible future architecture:

STARK
  |
  +-- Local AI
  |
  +-- Cloud AI
  |
  +-- Deterministic Core

The AI provider should be replaceable.

Do not tightly couple STARK's architecture to one model.

---

# 29. SECURITY

Security is important.

Never:

- expose API keys
- put credentials in source code
- commit secrets
- print tokens
- send unnecessary private information to external APIs

Use:

`.env`

environment variables

or the project's existing secure configuration mechanism.

Check `.gitignore` before introducing secrets/configuration files.

---

# 30. TESTING PHILOSOPHY

STARK should gradually move toward automated testing.

Important test categories:

### Intent tests

- hello
- time
- remember
- recall
- exit
- unknown command

### Context tests

- pronouns
- previous subject references
- conversational prefixes
- normalization

### Memory tests

- save
- update
- recall
- malformed memory
- missing memory

### AI tests

- AI engine connection
- missing API key
- provider errors
- malformed responses

### Integration tests

Full user request → STARK response.

---

# 31. IMPORTANT CURRENT STATUS

The project is functional and has already progressed beyond a basic chatbot.

Existing concepts include:

- command processing
- intent detection
- conversational context
- persistent memory
- AI integration
- system monitoring
- health status
- natural-language memory commands
- modular architecture
- Git-based development

Do not treat STARK-OS as a blank project.

It is an existing evolving codebase.

---

# 32. RESPONSE STYLE TO DEVELOPER

The developer prefers direct, practical explanations.

When explaining code:

Prefer:

"Here is what is happening."

"Here is why."

"Here is the exact command."

"Here is what you should see."

Avoid unnecessarily academic explanations.

For implementation tasks, provide terminal commands that can be copied directly.

---

# 33. MOST IMPORTANT INSTRUCTION

Before changing STARK-OS:

READ THE EXISTING CODE.

UNDERSTAND THE ARCHITECTURE.

PRESERVE WORKING FUNCTIONALITY.

MAKE SMALL, TESTABLE CHANGES.

NEVER FABRICATE RESULTS.

NEVER CLAIM SUCCESS WITHOUT TESTING.

STARK-OS is a long-term project.

Code quality and architectural consistency are more important than making the fastest possible change.

---

# 34. FIRST ACTION WHEN ENTERING THE REPOSITORY

Before implementing anything significant, inspect:

`pwd`

`git status`

`git branch`

`find . -maxdepth 2 -type f | sort`

Then inspect the relevant source files.

Do not modify anything simply because this context file says a component exists.

The actual repository is the source of truth.

---

# 35. SOURCE OF TRUTH PRIORITY

When information conflicts, use this priority:

1. Current repository code
2. Current tests
3. Current configuration
4. Current Git history
5. This QWEN.md
6. Historical project descriptions

This prevents old project context from overriding the actual current implementation.

---

# 36. LONG-TERM JARVIS-STYLE VISION

STARK-OS should evolve into a personal AI development workstation inspired by
JARVIS from the Iron Man movies.

The goal is not to replace macOS. The goal is to create an intelligent,
permission-aware software layer that can understand Atharva's voice or text
commands and help complete real software projects like a mature developer.

For a project request, STARK should eventually be able to:

1. Understand the user's goal.
2. Inspect the project and identify its architecture.
3. Create a clear implementation plan.
4. Ask an appropriate AI provider for reasoning or code assistance.
5. Read and modify approved project files.
6. Run tests, linters, builds, and diagnostics.
7. Analyze failures and make controlled repairs.
8. Review the resulting Git diff.
9. Ask for confirmation before risky actions.
10. Explain the work completed and any remaining issues.
11. Remember project conventions and long-term context.

Example request:

"Build a login system in my project, test it, review the changes, and explain
what you changed."

STARK should turn this into a controlled workflow:

USER REQUEST
  -> VOICE OR TEXT INPUT
  -> INTENT AND PROJECT UNDERSTANDING
  -> PROJECT INSPECTION
  -> IMPLEMENTATION PLAN
  -> USER APPROVAL WHEN REQUIRED
  -> CONTROLLED TOOL EXECUTION
  -> TESTING AND ERROR REPAIR
  -> GIT DIFF REVIEW
  -> FINAL REPORT OR VOICE RESPONSE

## Multi-provider AI

The AI layer should support replaceable providers instead of being tightly
coupled to Gemini.

Potential providers include:

- Gemini for large-context reasoning and general project work.
- Claude for code reasoning and review.
- OpenAI models for planning and general assistance.
- Local models for private or offline tasks.

Provider-specific implementation must remain inside the AI layer. A provider
router may later choose a model based on task type, privacy requirements,
cost, latency, context size, or availability.

Never hard-code provider credentials. Use environment variables or another
secure configuration mechanism, and never expose keys in logs, prompts, or Git.

## Voice interaction

Voice input and output are a major part of the future experience. STARK should
eventually support:

- Speech-to-text commands.
- Text-to-speech responses.
- Optional wake-word activation.
- Voice status updates during long tasks.
- A text fallback for testing and accessibility.

The text workflow must remain fully usable because the core orchestration,
permissions, testing, and error handling need to be reliable without audio.

## Project orchestrator

The central future component should be a project orchestrator. It should
coordinate planning, AI providers, approved tools, memory, tests, and reports.

The orchestrator must not blindly give an AI model unrestricted shell or file
access. Tools should have explicit interfaces, clear inputs, limited scope,
and observable results.

Potential tool categories include:

- Project inspection.
- File reading and editing.
- Test and lint execution.
- Build execution.
- Git status and diff review.
- Approved macOS application actions.
- File search and organization.
- System monitoring.
- Scheduled automation.

## Permissions and safety

STARK must request confirmation before:

- Deleting or overwriting important files.
- Running destructive shell commands.
- Installing dependencies.
- Changing Git history.
- Pushing code to a remote repository.
- Accessing sensitive folders.
- Sending private project content to a cloud provider.
- Performing system or application actions with external effects.

Every tool action should be auditable. STARK should show what it intends to
do, what it actually did, and whether it succeeded.

## Development order

Build this vision incrementally:

1. Stabilize the deterministic core, memory, and automated tests.
2. Build a text-based project orchestrator.
3. Add read-only project inspection tools.
4. Add controlled file editing with diffs.
5. Add test, lint, build, and error-repair workflows.
6. Add permission prompts and audit logging.
7. Add Gemini, Claude, OpenAI, and local-model provider routing.
8. Add voice input and speech output.
9. Add background automation and long-term project memory.

The mature STARK-OS experience should feel like a professional personal AI
command center: deterministic tools at the foundation, AI reasoning above
them, persistent project memory around them, and terminal, web, and voice
interfaces on top.

# END OF STARK-OS CONTEXT