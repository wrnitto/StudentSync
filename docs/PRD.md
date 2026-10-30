# StudentSync — Product Requirements Document (PRD)

| | |
|---|---|
| **Project title** | StudentSync |
| **Document status** | Prototype 1 (scaffolding) |
| **Repository** | `wrnitto/StudentSync` |

## How to read this document

This PRD separates two kinds of content:

| Label | Meaning |
|---|---|
| **Analyst requirement** (Part A) | Established by the Analyst's StudentSync specification and the project instructions. These define the product's scope. |
| **Proposed technical decision** (Part B) | Choices made to scaffold future development (stack, folder layout, draft API, draft data model). They are **not** product requirements, add no user-facing behavior, and may change in later prototypes. |

Anything the specification does not settle is listed under [Open questions](#a5-open-questions-for-the-analyst) instead of being decided here.

---

# Part A: Requirements established by the Analyst's specification

## A1. Project description

StudentSync is a mobile-first web application that helps college students organize schoolwork and personal responsibilities in one place.

## A2. Purpose and target users

- **Purpose:** give college students one place to organize their schoolwork and personal responsibilities.
- **Target users:** college students. Each student uses a personal account, created and accessed with an email and password, to reach their own saved schedule.

## A3. Scope: selected user stories

| ID | Selected user story |
|---|---|
| US-01 | Add, edit, and delete assignments and events. |
| US-02 | Set dates and times for assignments and events. |
| US-03 | Create an account and log in with email and password. |
| US-04 | Assign colors to courses and related events. |
| US-05 | Give tasks an importance rating. |
| US-06 | Detect scheduling conflicts before saving timed events. |
| US-07 | Switch between weekly and monthly calendar views. |
| US-08 | View unfinished tasks ordered by importance. |
| US-09 | Mark tasks complete and review completed work. |
| US-10 | Set/change deadline reminders and receive due-date reminders. |
| US-11 | Receive follow-up reminders for incomplete tasks. |

## A4. Out of scope

The following features are **rejected / out of scope** and will not be built:

- Canvas importing
- Assignment submission
- Grade calculation
- Instructor accounts
- Employer accounts
- Shared calendars
- Messaging
- Payments
- External appointment booking
- Automatic study scheduling
- Automatic conflict resolution

## A5. Open questions for the Analyst

The specification does not define the details below. They should be confirmed before the related tasks in [`TASKS.md`](TASKS.md) are implemented, and no behavior is assumed for them in this PRD.

| # | Question | Related story |
|---|---|---|
| Q1 | How are "tasks" related to "assignments" and "events" (the same thing, or a separate item type)? | US-05, US-08, US-09, US-11 |
| Q2 | What scale should the importance rating use? | US-05, US-08 |
| Q3 | What happens to a course's related items if the course is deleted? Can courses be deleted? | US-04 |
| Q4 | After a conflict is detected, what options does the user have? | US-06 |
| Q5 | How are reminders delivered to the user (for example, in-app)? | US-10, US-11 |
| Q6 | Are there default reminder times, and how often are follow-up reminders sent? | US-10, US-11 |
| Q7 | What does "review completed work" include (for example, a list, or more detail)? | US-09 |

## A6. Constraints from the project instructions

- StudentSync is a **mobile-first web application**.
- Accounts are created and accessed with **email and password**.
- Each user's assignments and events belong to their own account (a personal saved schedule).
- Conflicts are **detected** before saving timed events. Conflict resolution is **not** automatic (see A4).
- Features in the out-of-scope list (A4) must not be added.
- **Prototype 1 is scaffolding only:** project structure, technical plan, documentation, development tasks, and workspace rules. It does not include a working application.
- The **site map is hand-drawn** and submitted separately. It is not generated in this repository (see [`SITEMAP.md`](SITEMAP.md)).

---

# Part B: Proposed technical decisions (for future prototypes)

> Everything in Part B is a **proposal** for scaffolding later development. It does not add product requirements, and it can be revised as the Analyst answers the open questions in A5.

## B1. Proposed technical architecture

The proposal is a three-tier client/server architecture, with one repository folder per tier:

```
┌────────────────────────┐   HTTPS / JSON    ┌────────────────────────┐    SQL     ┌──────────────────┐
│  /client               │ ────────────────▶ │  /api                  │ ─────────▶ │  /database       │
│  React SPA (Vite)      │ ◀──────────────── │  Node.js + Express     │ ◀───────── │  PostgreSQL      │
│  mobile-first UI       │                   │  REST API              │            │  schema + seeds  │
└────────────────────────┘                   └────────────────────────┘            └──────────────────┘
```

### Front-end approach (`/client`) — proposed

- A React single-page application built with Vite.
- Client-side routing between screens. The screens themselves are defined by the hand-drawn site map.
- A calendar component that supports weekly and monthly views (US-07).
- Mobile-first, responsive CSS.
- All server communication goes through one small API module.

### Back-end approach (`/api`) — proposed

- A Node.js + Express REST API that returns JSON.
- Email + password authentication (US-03). Passwords are stored only as hashes, and sessions are kept with secure cookies.
- Every query is scoped to the logged-in user so that users can access only their own data.
- Server-side input validation.
- **Conflict check (US-06):** before a timed event is saved, the API checks for overlap with the user's other timed events and returns any conflicts to the client. What the user can do next depends on Q4. The API never changes events automatically.
- **Reminders (US-10, US-11):** a scheduled background job in the API finds reminders that are due and delivers them. The delivery channel depends on Q5.

### Database approach (`/database`) — proposed

- A PostgreSQL relational database.
- Numbered SQL migration files in `database/migrations/`, applied in order.
- Fake demo data in `database/seeds/`.
- Date-times stored with time zone information.

## B2. Proposed tools and frameworks

These are proposed technical choices for future prototypes and are not product requirements.

| Area | Proposed tool |
|---|---|
| Front end | React, Vite, React Router, FullCalendar (or a similar calendar library), CSS |
| Back end | Node.js (LTS), Express, bcrypt (password hashing), express-session, node-cron (scheduled reminder job), a validation library such as zod |
| Database | PostgreSQL, a SQL migration runner such as node-pg-migrate |
| Testing | Vitest + React Testing Library (client), Jest + Supertest (API) |
| Code quality | ESLint, Prettier |
| Collaboration | Git, GitHub (issues, pull requests, project board), Devin |

## B3. DRAFT API endpoints (proposed)

> **DRAFT / PROPOSED technical design.** This is not an Analyst requirement. Endpoints will change as the open questions are answered.

| Method | Path | Purpose | Story |
|---|---|---|---|
| POST | `/api/auth/register` | Create account (email, password) | US-03 |
| POST | `/api/auth/login` | Log in | US-03 |
| POST | `/api/auth/logout` | Log out | US-03 |
| GET | `/api/auth/me` | Current user | US-03 |
| GET / POST | `/api/courses` | List / create courses | US-04 |
| PATCH | `/api/courses/:id` | Update course (for example, its color) | US-04 |
| GET | `/api/items` | List the user's items (with filters for calendar range, completion, and sort order) | US-01, US-07, US-08, US-09 |
| POST | `/api/items` | Create item | US-01, US-02 |
| GET / PATCH / DELETE | `/api/items/:id` | Read / edit / delete item | US-01, US-02, US-05 |
| POST | `/api/items/check-conflicts` | Check a proposed timed event for conflicts before saving | US-06 |
| PATCH | `/api/items/:id/completion` | Mark an item complete or incomplete | US-09 |
| GET / POST | `/api/items/:id/reminders` | List / set reminders on an item | US-10 |
| PATCH / DELETE | `/api/reminders/:id` | Change / remove a reminder | US-10 |

Course deletion and reminder-delivery endpoints are left out until Q3 and Q5 are answered.

## B4. DRAFT data model (proposed)

> **DRAFT / PROPOSED technical design.** This is not an Analyst requirement. Columns marked *(pending Qn)* depend on the open questions.

| Table | Proposed columns |
|---|---|
| `users` | `id`, `email` (unique), `password_hash`, `created_at` |
| `courses` | `id`, `user_id` → users, `name`, `color`, `created_at` |
| `items` | `id`, `user_id` → users, `course_id` → courses (nullable), `type` *(pending Q1)*, `title`, `description`, date/time columns for due dates and timed events, `importance` *(scale pending Q2)*, `is_completed`, `completed_at`, `created_at`, `updated_at` |
| `reminders` | `id`, `item_id` → items, `kind` (deadline / follow-up), `remind_at`, `sent_at`, `created_at` *(delivery details pending Q5/Q6)* |

Relationships: a user has many courses and items, a course has many related items, and an item has many reminders.

## B5. Proposed engineering practices

- Secrets and configuration live in environment variables. Each app has a committed `.env.example`, and real `.env` files are never committed.
- Passwords are hashed and SQL queries are parameterized.
- Branching, commits, and reviews follow [`WORKSPACE_RULES.md`](WORKSPACE_RULES.md).
- Work is split into the incremental tasks in [`TASKS.md`](TASKS.md).

---

## Related documents

- [`TASKS.md`](TASKS.md): development task list with acceptance criteria
- [`WORKSPACE_RULES.md`](WORKSPACE_RULES.md): naming, commits, branching, and PR process
- [`SITEMAP.md`](SITEMAP.md): placeholder for the hand-drawn site map
