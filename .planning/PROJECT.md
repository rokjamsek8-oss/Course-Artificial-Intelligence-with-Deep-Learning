# Course: Artificial Intelligence with Deep Learning

## What This Is

A comprehensive course on Artificial Intelligence and Deep Learning, currently featuring structured presentation materials for foundational topics like Linear Regression. It aims to provide high-quality educational content for learners and instructors.

## Core Value

Provide clear, visually engaging, and mathematically rigorous educational content for AI and Deep Learning topics.

## Requirements

### Validated

- âœ“ **Linear Regression Presentation**: Foundational module with comprehensive coverage (reveal.js) â€” existing
- âœ“ **PDF Rendering**: Automated export of presentation slides to A4 PDF format â€” existing

### Active

- [ ] **Curriculum Research**: Identify standard modules and sequence for a modern AI/DL course
- [ ] **Deep Learning Fundamentals**: Create presentation materials for neural network basics
- [ ] **Interactive Components**: Add code examples or interactive widgets to the slides
- [ ] **Content Standardization**: Ensure consistent styling and depth across all course modules

### Out of Scope

- **Video Production** â€” focus on static and interactive presentation materials first
- **LMS Development** â€” focus on content creation rather than building a hosting platform

## Context

- The project uses `reveal.js` for slide decks, allowing for web-based presentations with MathJax support.
- A Python-based renderer using `playwright` is used to generate static PDF versions of the slides.
- Initial content focus is on foundational statistical methods before moving into deep learning.

## Constraints

- **Tech Stack**: Python (rendering), HTML/JS/CSS (slides/reveal.js).
- **Presentation Framework**: `reveal.js` version 4.5.0+.
- **Design Style**: Clean, white-theme professional aesthetic with clear mathematical notation.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use reveal.js | Enables web-native, interactive, and easily version-controlled presentations | âœ“ Good |
| Playwright for PDF | Reliable rendering of web content including MathJax/Markdown | âœ“ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? â†’ Move to Out of Scope with reason
2. Requirements validated? â†’ Move to Validated with phase reference
3. New requirements emerged? â†’ Add to Active
4. Decisions to log? â†’ Add to Key Decisions
5. "What This Is" still accurate? â†’ Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check â€” still the right priority?
3. Audit Out of Scope â€” reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-23 after initialization*
