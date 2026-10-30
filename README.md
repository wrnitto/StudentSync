# StudentSync

StudentSync is a **mobile-first web application that helps college students organize schoolwork and personal responsibilities in one place.** Students will be able to track assignments, tasks, and events with dates and times; color-code courses; rate importance; see a weekly or monthly calendar; get warnings about scheduling conflicts before saving; mark work complete; and receive deadline and follow-up reminders.

## Current stage: Prototype 1 (scaffolding)

Prototype 1 is a **scaffolding** milestone. It is **not** the working application and **not** the final UI design. Its purpose is to set up the foundation for later development:

- the **project structure** (`/client`, `/api`, `/database`, `/docs`),
- the **technical plan** and requirements ([`docs/PRD.md`](docs/PRD.md)),
- the **development tasks** with acceptance criteria ([`docs/TASKS.md`](docs/TASKS.md)),
- the **workspace rules** for naming, commits, branching, and reviews ([`docs/WORKSPACE_RULES.md`](docs/WORKSPACE_RULES.md)), and
- a placeholder for the **site map** ([`docs/SITEMAP.md`](docs/SITEMAP.md)). The site map itself is hand-drawn and submitted separately.

There is no runnable application code yet.

## Repository structure

```
StudentSync/
├── client/          # Front-end application (React + Vite, mobile-first). Placeholder in Prototype 1
├── api/             # Back-end REST API (Node.js + Express). Placeholder in Prototype 1
├── database/        # PostgreSQL schema, migrations, and seed data
│   ├── migrations/  # Numbered SQL migrations (added in later prototypes)
│   └── seeds/       # Demo/sample data (added in later prototypes)
├── docs/            # Project documentation
│   ├── PRD.md               # Product Requirements Document
│   ├── TASKS.md             # Development task list with acceptance criteria
│   ├── WORKSPACE_RULES.md   # Naming, commits, branching, and PR/review process
│   └── SITEMAP.md           # Placeholder: the site map is hand-drawn and submitted separately
├── .gitignore
└── README.md
```

Each folder has its own `README.md` describing what will go there.

## Planned technology

| Layer | Technology |
|---|---|
| Front end (`/client`) | React, Vite, React Router, FullCalendar, CSS (mobile-first) |
| Back end (`/api`) | Node.js, Express, bcrypt, express-session, node-cron, Nodemailer |
| Database (`/database`) | PostgreSQL with SQL migrations |
| Testing and quality | Vitest, Jest + Supertest, ESLint, Prettier, GitHub Actions |

See [`docs/PRD.md`](docs/PRD.md#4-technical-architecture) for the full architecture, data model, and planned API endpoints.

## How future development will be organized

Development will happen in **phases**, each delivered in a later prototype. Each phase leaves the app working, with more features than the phase before:

| Phase | Focus | User stories |
|---|---|---|
| 0 | Scaffolding and documentation (**Prototype 1**) | — |
| 1 | Project setup and accounts (register, log in, log out) | US-03 |
| 2 | Add, edit, and delete assignments, tasks, and events with dates and times | US-01, US-02 |
| 3 | Course colors, importance ratings, To-Do list, completing work | US-04, US-05, US-08, US-09 |
| 4 | Weekly and monthly calendar views and conflict detection | US-06, US-07 |
| 5 | Deadline and follow-up reminders | US-10, US-11 |
| 6 | Mobile and accessibility polish, demo data, deployment | — |

Workflow summary (details in [`docs/WORKSPACE_RULES.md`](docs/WORKSPACE_RULES.md)):

1. Each task in [`docs/TASKS.md`](docs/TASKS.md) becomes a GitHub issue.
2. Work happens on a short-lived branch, for example `feature/T-2.2-item-crud-api`.
3. Commits follow Conventional Commits, for example `feat(api): add item CRUD endpoints`.
4. Changes are merged into `main` through a pull request after at least one teammate approves it. This also applies to PRs opened by Devin.
5. A task is done only when all of its acceptance criteria are met.

## Out of scope

Canvas/LMS importing, assignment submission, grade calculation, instructor or employer accounts, shared calendars, messaging, payments, external appointment booking, automatic study scheduling, and automatic conflict resolution are **not** part of StudentSync. See [`docs/PRD.md`](docs/PRD.md#34-out-of-scope).
