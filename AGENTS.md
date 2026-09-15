# Engineering guidelines

Favor simple, correct solutions and focused changes. Scale planning and verification to the task.

## 1. Resolve meaningful uncertainty

- Ask when ambiguity materially affects the goal, scope, authorization, security, data safety, or a costly-to-reverse decision.
- For low-risk, reversible details, use existing context and reasonable judgment; briefly state assumptions when they affect the result.
- Continue independent work while waiting for necessary clarification.
- Explain a simpler alternative when it would meet the user's goal, without repeatedly questioning an already-settled requirement.

## 2. Prefer the simplest clear solution

Before adding code, check whether the requested outcome is already covered by existing behavior, the standard library, a native platform feature, or an installed dependency.

- Write the minimum code needed for the requested behavior.
- Avoid speculative features, abstractions, configuration, boilerplate, and new dependencies.
- Prefer correctness and readability over fewer lines or files.
- Choose the edge-case-correct option when similarly simple alternatives exist.
- Preserve input validation at trust boundaries, error handling that prevents data loss, security, accessibility, and real hardware constraints.
- Avoid defensive handling for states the system demonstrably cannot reach.
- Add comments for non-obvious tradeoffs and known limitations; explain the reason and, when useful, the ceiling and upgrade path. Routine simplifications need no special marker.

## 3. Keep changes surgical

- Change only what is needed for the user's request.
- Match existing style; avoid unrelated refactoring, formatting, or comment edits.
- Remove imports, variables, and functions made unused by your changes.
- Do not remove pre-existing unrelated code without authorization; mention it only when useful.
- Every changed line should trace to the requested outcome.

## 4. Verify the outcome

- Define observable success criteria before implementing non-trivial changes.
- For multi-step work, give a brief plan with the relevant verification for each step.
- Reuse the project's existing test framework and conventions.
- For non-trivial logic, add or update runnable checks that would detect a regression; choose coverage based on behavior and risk, not a fixed test count.
- When no test infrastructure exists, prefer a small runnable self-check or test without adding a framework unless needed.
- For bug fixes, reproduce the failure before fixing it when practical. For behavior-preserving refactors, verify relevant behavior before and after.
- Trivial, low-impact changes need only proportionate verification, not redundant tests.
- Run relevant checks, resolve failures caused by the change, and report what was verified and any remaining limitations.

## 5. Complete the authorized task

- Continue through all authorized steps needed to satisfy the user's request. A plan, clarification, review, or completed increment is an intermediate result unless the user requested only that result.
- Pause only the work that depends on missing information or required approval. Complete independent authorized work, and clearly distinguish completed work from any remaining blocker.
- Preserve all explicit approval requirements. Task completion does not expand the user's requested scope or execution permissions.

## 6. Default skills

For engineering work in this repository, load and follow these skills by default, applying each according to its documented workflow:

- `code-review-and-quality`
- `incremental-implementation`
- `test-driven-development`
