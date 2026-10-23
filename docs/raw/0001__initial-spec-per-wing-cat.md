# Sweeper: AI-Directed Software Improvement System

## 1. Project Vision

**Sweeper is a system for capturing, organizing, and eventually automatically executing software improvement requests using AI coding agents.**

Its purpose is to radically reduce the friction between noticing a desired software improvement and having an AI implement it.

I am an experienced software developer who uses AI coding agents, particularly Codex, to build and maintain a large collection of software projects.

While using my own applications, I frequently notice opportunities for improvements:

- "I wish this panel had an Export to JSON button."
- "This label should say something different."
- "I'd like another option in this menu."
- "This behavior is slightly inconvenient. Let's fix it."
- "I wonder whether there's a better way to organize this feature."

Currently, acting on these observations means interrupting my work, locating the relevant project, opening an agent session, supplying context, and describing the requested change.

Frequently, the improvement is small enough that Codex can implement it with little difficulty. The problem is not programming capability. **The problem is the friction involved in initiating the work.**

Sweeper aims to eliminate that friction.

### Ultimate experience

While using an application, I notice something I'd like changed.

I invoke that application's Sweeper capture interface, describe the improvement, and return to what I was doing.

Later, an AI coding agent picks up the request and performs the work.

Over time, this should dramatically increase the rate at which my applications evolve.

**The long-term objective is to multiply my effective software-producing capacity by 5–10× or more.** This is an aspiration to test, not an established performance measurement.

---

## 2. Core Architectural Principle

**Sweeper standardizes the storage and processing of improvement requests, not the user interfaces used to capture them.**

Different applications operate in different environments.

A Tkinter application might offer a toolbar button or menu item.

A CLI program might provide a `sweep` command.

A web application might provide a feedback dialog.

Another application might offer a keyboard shortcut, context-menu command, or some other mechanism.

The capture interface should be appropriate to the application.

All capture mechanisms should produce the same standardized request format in a predictable location.

### Standard storage location

Within a project's root directory:

```text
<project-root>/
    db/
        sweep-requests/
            <guid>.json
            <guid>.json
            ...
```

The `db/` directory is already a convention used by several of my applications for project-associated state and metadata.

Each request is stored as an individual JSON file with a unique identifier.

The application that creates the request does not need to know anything about which AI agent will eventually process it.

It simply writes a valid request.

### Why file-based storage?

- Simple to understand and debug.
- Durable between program executions.
- No always-running background service required.
- Easy for AI agents to inspect.
- Easy to integrate into existing applications.
- Naturally associated with the project being improved.
- Compatible with my existing preference for file-based communication, exemplified by my FileTalk system.

FileTalk is an existing system of mine that uses durable inbox/outbox directories for asynchronous communication. Programs do not need to be running simultaneously to exchange messages.

Sweeper may eventually use FileTalk for more elaborate communication, but the first version does not necessarily require it.

---

## 3. Request Format

Define a standard JSON schema for Sweeper requests.

An illustrative request:

```json
{
  "schema_version": 1,
  "request_id": "b6fd2070-1234-4e21-9a20-89c9d927348f",
  "created_at": "2026-10-22T23:52:00-07:00",

  "project": {
    "name": "pydeck26",
    "zoo_id": null
  },

  "request": {
    "title": "Export Captain's Log entry as JSON",
    "description": "Add an option to export the selected Captain's Log entry to a JSON file.",
    "directive": "go-ahead"
  },

  "context": {
    "interface": "tkinter",
    "component": "captains-log",
    "active_item_id": null,
    "notes": ""
  },

  "execution": {
    "status": "pending",
    "agent": null,
    "started_at": null,
    "completed_at": null
  }
}
```

This is a proposed starting schema, not a final decision.

The schema should be simple, extensible, and documented.

### Request directives

One of the most important fields describes what I want the AI to do.

Proposed values:

**`go-ahead`**

Implement the requested change. The user has authorized the coding agent to proceed.

This is appropriate for straightforward modifications that Codex can usually handle reliably.

**`please-investigate`**

Examine the request, explore the relevant code, and provide analysis or recommendations.

Do not implement the proposed change yet.

This is appropriate when the implementation approach is uncertain or the user wants design feedback.

**`please-hold`**

Record the request for later consideration.

Do not dispatch it to an agent automatically.

This is useful for ideas that occur while working but aren't yet ready for implementation.

These directives should be separate from execution status. For example, a `go-ahead` request can be `pending`, `running`, `completed`, or `failed`.

### Contextual metadata

Capture interfaces should include useful environmental context when available, such as:

- Project identity.
- Application version.
- Active panel or page.
- Relevant selected item.
- Source file or component name.
- Additional human-entered notes.

Not every application will supply every field.

Most fields should be optional. A capture interface should not become burdensome because it cannot determine metadata that isn't readily available.

---

## 4. Capture Interfaces

Sweeper should not initially attempt to create one universal GUI component for every program.

Instead, it should provide:

1. A documented JSON request schema.
2. A reusable Python library for writing valid requests.
3. Examples or integration instructions for different application types.
4. Standard prompts that I can give Codex when asking it to add Sweeper support to an existing application.

### Example integration prompt

> Add Sweeper support to this application.
>
> Provide a convenient interface appropriate to this program for capturing software improvement requests.
>
> Support three directives: go-ahead, please-investigate, and please-hold.
>
> Save each request according to the Sweeper JSON specification under the project's `db/sweep-requests/` directory.
>
> Include relevant application context automatically where practical.
>
> Keep the interface lightweight and avoid disrupting the application's normal operation.

This approach should make it easy to add Sweeper support to many of my existing applications through relatively small Codex tasks.

A goal is eventually to integrate Sweeper into most applications I use regularly.

---

## 5. Sweeper Processing

The capture system and the processing system are separate concerns.

An application only needs to capture requests.

A Sweeper worker will eventually discover and process them.

### Initial processing concept

The worker examines a project's:

```text
db/sweep-requests/
```

It identifies pending requests and acts according to their directives.

For example:

- `please-hold`: preserve for later.
- `please-investigate`: delegate investigation to a coding agent.
- `go-ahead`: delegate implementation to a coding agent.

The worker may run periodically, be launched manually, or eventually receive notifications when new requests appear.

There is no requirement for it to operate continuously.

### Agent integration

Codex will initially be the preferred implementation agent, although the design should not assume that Codex is the only possible backend.

Other providers, including Claude, Grok, or future coding agents, may eventually be supported.

Do not attempt to implement a sophisticated multi-provider routing system in the first version.

The initial objective is to establish a reliable path from a stored request to a coding-agent task.

### Project discovery

Requests live within their owning project's directory.

This provides a natural way to associate a request with its codebase.

I also have a separate program named `zoo` that maintains a registry of projects and assigns unique project identifiers.

Integration with Zoo may eventually simplify project discovery, but it is not a requirement for the initial version.

---

## 6. Trust and Autonomy

An important design principle: **Not every programming task requires the same level of supervision.**

I already use Codex extensively and have a practical sense of what kinds of work it can reliably perform.

For example, changing interface text or adding a simple menu operation is often straightforward.

Large architectural modifications, complicated state changes, or operations with substantial external consequences may require more attention.

Sweeper should support a progression toward greater autonomy, without treating every trivial feature change as if it requires a heavyweight review procedure.

At the same time, a `go-ahead` directive is permission to attempt the requested project-scoped change, not unrestricted permission to perform destructive operations, expose secrets, or deploy production changes.

Git version control provides an important recovery mechanism. Existing project tests and agent-generated tests should be used where appropriate.

The longer-term system may distinguish between simple changes that can be performed automatically and more consequential changes that require approval.

This need not be solved completely in the MVP.

---

## 7. Development Phases

### S1: Capture and storage

**Goal:** A standard request format and an easy way to produce valid requests.

Deliverables:

- JSON schema.
- Standard folder convention.
- Reusable request-writing library.
- UUID generation.
- Timestamp creation.
- Safe file writes, avoiding partial JSON files.
- Standard integration prompt for coding agents.
- A minimal demonstration capture interface.

Success criterion:

I can add Sweeper capture support to an existing application, submit an improvement request, and find a correctly formatted JSON file in its `db/sweep-requests/` directory.

### S2: Request discovery and dispatch

**Goal:** Turn stored requests into work assigned to an AI agent.

Deliverables:

- Request scanning.
- Filtering by directive and execution status.
- A simple work queue.
- A first Codex integration, using supported mechanisms.
- Status tracking.
- Error reporting.
- Protection against accidentally dispatching the same request twice.

Success criterion:

A stored `go-ahead` request can be picked up and supplied to Codex without my manually reconstructing the entire project context.

### S3: Execution tracking and results

**Goal:** Make dispatched work observable and manageable.

Deliverables:

- Execution reports.
- Completed/failed/blocked statuses.
- References to relevant commits or changed files.
- Agent-produced summaries.
- A simple review mechanism.
- Retry controls.

Success criterion:

I can determine what happened to every request, what the agent changed, and whether additional attention is needed.

### S4: Expanded autonomy

Potential future improvements:

- Parallel request processing.
- Git worktree isolation.
- Provider selection.
- Integration with Context Jetpack.
- Integration with PyDeck26.
- Integration with Zoo.
- FileTalk-based notifications.
- Dependency tracking between requests.
- Automatic verification and regression testing.
- AI investigation of feature requests before implementation.
- More sophisticated prioritization and resource allocation.

These are longer-term possibilities, not prerequisites for the MVP.

---

## 8. Relationship to Existing Software

The following programs already exist in my ecosystem.

**`spark`**: Captures potential project ideas, notes, descriptions, and related conversations.

**`zoo`**: Maintains a global registry of projects, including unique IDs.

**`zookeep`**: Creates project infrastructure and scaffolding.

**`pydeck26`**: Provides a per-project Tkinter development cockpit, including conversations, whiteboards, Captain's Log, and Git operations.

**`Context Jetpack`**: Assembles reusable context packages for AI agents, with saved and loaded profiles.

**`FileTalk`**: Provides durable file-based communication between programs.

Sweeper should initially remain an independent project.

It should integrate with existing tools where doing so creates clear benefits, but it should not require redesigning those applications.

In particular, the initial development should not become a larger project to unify the entire ecosystem.

---

## 9. Strategic Objective

Sweeper belongs to a larger personal research program: becoming an exceptionally powerful AI-augmented software creator.

My working hypothesis is that the current bottleneck in my productivity is **instruction bandwidth**, rather than the raw programming capability of available AI systems.

I frequently have more AI coding capacity available than I use.

The friction of interrupting a task, locating a project, establishing an agent context, and issuing implementation instructions prevents many small improvements from being pursued.

Sweeper aims to reduce that friction dramatically.

An important metric is the elapsed time and human attention required to move from:

**"I wish this software did X"**

to:

**"An AI agent is working on X."**

A second metric is the number of useful improvements actually delivered.

The ideal workflow is:

**Notice → Capture → Continue working → AI implements → Review when needed.**

The crucial goal is to preserve the user's focus while allowing improvements to flow continuously into the software development pipeline.

---

## 10. Instructions for the Initial Codex Session

Begin with S1, not the entire long-term system.

First, inspect the project environment and any existing conventions relevant to file-based state, project structure, and request creation.

Then:

1. Propose a compact, versioned JSON schema for requests.
2. Define the public interface for creating requests.
3. Implement a small reusable capture/storage library.
4. Ensure writes are durable, atomic where practical, and safely named by UUID.
5. Implement a minimal example demonstrating request submission.
6. Write concise integration instructions and a reusable prompt for adding Sweeper capture support to other applications.
7. Add focused tests for the storage format and request-writing behavior.

Keep the first implementation small and understandable.

Avoid building a large application framework, an elaborate GUI, or a multi-agent orchestration system prematurely.

**The first victory is getting a Sweeper request captured correctly and conveniently from a real application.**

Once that works, we can use Sweeper itself to request improvements to Sweeper.

That is the beginning of the recursive leverage this project is intended to create.

---

**Project motto:**

*Notice the improvement. Issue the order. Keep sailing.*