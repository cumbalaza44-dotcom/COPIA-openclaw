# LOGGING_PROTOCOL: SURGICAL_EFFICIENCY
Rule: All memory updates must minimize token footprint.
Action: Execute this protocol when updating memory/YYYY-MM-DD.md or MEMORY.md.

## FORMAT_CONSTRAINTS
- Style: LOG_LEVEL_MINIMAL (strictly data-driven).
- Syntax: No prose, no greetings, no introductory fillers.
- Token_Saving: Use abbreviations (e.g., PROJ, REQ, SYNC).

## STRUCTURE
1. [DONE]: Bullet list of verified completions.
2. [PENDING]: Urgent next steps only.
3. [DATA]: Critical strings (IDs, URLs, Parameters).
4. [REF]: Cross-reference to specific file/line if needed.

## EXECUTION_TRIGGER
- Before session end or upon direct command: "JARVIS, log de cierre".
- Consolidate multiple related actions into a single bullet point.