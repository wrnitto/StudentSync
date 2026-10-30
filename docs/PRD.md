# StudentSync — Product Requirements Document (PRD)

| | |
|---|---|
| **Project title** | StudentSync |
| **Document status** | Draft for Prototype 1 (scaffolding) |
| **Repository** | `wrnitto/StudentSync` |

---

## 1. Project description

StudentSync is a mobile-first web application that helps college students organize schoolwork and personal responsibilities in one place. Students can record assignments, tasks, and events, give them dates, times, colors, and importance ratings, view them on weekly or monthly calendars, find scheduling conflicts before saving, and get reminders so that deadlines are not missed.

## 2. Purpose and target users

### Purpose

College students often track deadlines in several places: syllabi, an LMS, a paper planner, phone reminders, and memory. StudentSync gives them one personal, private place to:

- see everything that is due or scheduled,
- decide what to work on next based on importance,
- avoid double-booking their time, and
- be reminded before (and after) deadlines.

### Target users

| User | Description |
|---|---|
| **Primary: college student** | An undergraduate or graduate student juggling several courses plus work, clubs, or personal commitments. Uses a phone most of the time and a laptop for longer planning sessions. |

There is only **one user role**: the individual student. Each student sees and manages only their own data.

## 3. Scope

### 3.1 In scope (selected user stories)

| ID | User story | Summary |
|---|---|---|
| US-01 | As a college student, I want to **add, edit, and delete assignments and events** so that I can keep my schoolwork and personal plans up to date. | Item management |
| US-02 | As a college student, I want to **set dates and times for assignments and events** so that I know when my responsibilities are due or scheduled. | Dates and times |
| US-03 | As a college student, I want to **create an account and log in with my email and password** so that I can access my own saved schedule. | Accounts |
| US-04 | As a college student, I want to **assign colors to courses and their related events** so that I can tell my classes apart at a glance. | Course colors |
| US-05 | As a college student, I want to **give tasks an importance rating** so that I can focus on what matters most. | Importance |
| US-06 | As a college student, I want the app to **detect scheduling conflicts before I save a timed event** so that I don't double-book myself. | Conflict detection |
| US-07 | As a college student, I want to **switch between weekly and monthly calendar views** so that I can see both short-term detail and the big picture. | Calendar views |
| US-08 | As a college student, I want to **view my unfinished tasks ordered by importance** so that I know what to work on next. | Prioritized task list |
| US-09 | As a college student, I want to **mark tasks complete and review my completed work** so that I can track my progress. | Completion and history |
| US-10 | As a college student, I want to **set and change deadline reminders and receive due-date reminders** so that I don't miss deadlines. | Deadline reminders |
| US-11 | As a college student, I want to **receive follow-up reminders for incomplete tasks** so that overdue work doesn't get forgotten. | Follow-up reminders |

### 3.2 Functional requirements

**Accounts (US-03)**
- FR-1: A visitor can register with a name, email, and password. Emails are unique and not case-sensitive.
- FR-2: A registered user can log in with email and password and log out.
- FR-3: Passwords are stored only as salted hashes (bcrypt).
- FR-4: Every course, item, and reminder belongs to exactly one user. The API never returns or changes another user's data.

**Items: assignments, tasks, and events (US-01, US-02, US-05, US-09)**
- FR-5: A user can create, view, edit, and delete items. Each item has a title, an optional description, a type (`assignment`, `task`, or `event`), and an optional course.
- FR-6: Assignments and tasks have a **due date** and an optional due time. Events have a **start date/time** and an **end date/time**, or are marked all-day.
- FR-7: Assignments and tasks have an **importance rating**: `low`, `medium`, or `high` (default `medium`).
- FR-8: Assignments and tasks can be marked **complete** and marked incomplete again. The completion timestamp is recorded.
- FR-9: A "Completed" view lists completed items, newest first, and can be filtered by course.

**Courses and colors (US-04)**
- FR-10: A user can create, edit, and delete courses (name plus a color from a preset palette).
- FR-11: Items linked to a course are shown in that course's color in lists and calendars.
- FR-12: Deleting a course does not delete its items; they become "no course".

**Prioritized list (US-08)**
- FR-13: A "To-Do" view lists unfinished assignments and tasks sorted by importance (high → low), then by due date (soonest first).
- FR-14: Overdue items are visually flagged.

**Calendar (US-07)**
- FR-15: A calendar shows items by date in a **weekly** view and a **monthly** view, with a toggle between them and controls to go to the previous, next, or current period.
- FR-16: Selecting an item on the calendar opens its details, where it can be edited.

**Conflict detection (US-06)**
- FR-17: When a user saves a **timed** event (not all-day) whose time range overlaps another of their timed events, the app **warns** them before saving and lists the conflicting events.
- FR-18: The user can choose **Save anyway** or **Go back and edit**. The app never moves or changes events on its own (no automatic conflict resolution).
- FR-19: Conflict checks run on the server so that they are always applied, and the client shows the result.

**Reminders (US-10, US-11)**
- FR-20: A user can add, change, or remove one or more **deadline reminders** on an assignment, task, or event, either as an offset (for example, 1 hour, 1 day, or 1 week before) or as a specific date/time.
- FR-21: A user can set a **default reminder offset** in their settings that is applied to new items.
- FR-22: When a reminder is due, the user receives it **in the app** (notification list/badge) and **by email**.
- FR-23: If an assignment or task passes its due date without being completed, the user receives a **follow-up reminder**, repeated at a user-configurable interval (default every 24 hours, up to a maximum count) until it is completed or the follow-ups are turned off.
- FR-24: Completing or deleting an item cancels its pending reminders.

### 3.3 Non-functional requirements

- NFR-1 **Mobile-first:** layouts are designed for a 360–430 px wide phone screen first, then expanded for tablet and desktop. Touch targets are at least 44×44 px.
- NFR-2 **Browser support:** current versions of Chrome, Safari (iOS and macOS), Firefox, and Edge.
- NFR-3 **Security:** HTTPS in deployment, HTTP-only and `SameSite` session cookies, server-side validation of all input, parameterized SQL queries, and secrets kept in environment variables.
- NFR-4 **Privacy:** only the minimum personal data is stored (name, email, password hash, and the user's own schedule).
- NFR-5 **Accessibility:** semantic HTML, labeled form fields, keyboard navigation, and color never used as the *only* indicator (course names are shown next to colors).
- NFR-6 **Time zones:** date-times are stored in UTC and displayed in the user's local time zone.
- NFR-7 **Performance:** main screens load in under 2 seconds on a typical 4G phone connection.

### 3.4 Out of scope

These features were considered and **rejected** for this project. They will not be built:

- Canvas / LMS importing
- Assignment submission
- Grade calculation
- Instructor accounts
- Employer accounts
- Shared calendars
- Messaging
- Payments
- External appointment booking
- Automatic study scheduling
- Automatic conflict resolution (StudentSync only *detects* conflicts and warns. See FR-18.)

## 4. Technical architecture

StudentSync uses a three-tier client/server architecture, and each tier has its own folder in the repository:

```
┌────────────────────────┐   HTTPS / JSON    ┌────────────────────────┐    SQL     ┌──────────────────┐
│  /client               │ ────────────────▶ │  /api                  │ ─────────▶ │  /database       │
│  React SPA (Vite)      │ ◀──────────────── │  Node.js + Express     │ ◀───────── │  PostgreSQL      │
│  mobile-first UI       │  session cookie   │  REST API + scheduler  │            │  schema + seeds  │
└────────────────────────┘                   └───────────┬────────────┘            └──────────────────┘
                                                         │ SMTP
                                                         ▼
                                                 Email reminders
```

### 4.1 Front-end approach (`/client`)

- **React** single-page application built with **Vite**.
- **React Router** for client-side routing between screens.
- **FullCalendar (React)** for the weekly and monthly calendar views.
- **Plain CSS with CSS variables**, written mobile-first (`min-width` media queries). The course color palette is defined as variables.
- All server calls go through one small API module (`src/api/`) that uses `fetch` with `credentials: "include"`.
- The client never trusts itself for security. All validation and ownership checks are repeated by the API.

### 4.2 Back-end approach (`/api`)

- **Node.js (LTS) + Express** REST API that returns JSON.
- **Authentication:** email + password, hashed with **bcrypt**. Sessions use **express-session**, are stored in PostgreSQL with **connect-pg-simple**, and are sent as an HTTP-only cookie.
- **Authorization:** a `requireAuth` middleware is applied to every route except register and login, and every query is filtered by `user_id`.
- **Validation:** request bodies are validated (for example with `zod`) before they reach the database.
- **Conflict detection:** a service that, for a proposed timed event, finds the user's other timed events where `existing.start < new.end AND existing.end > new.start`.
- **Reminders:** a **node-cron** job runs every minute, finds reminders whose `remind_at` has passed and that have not been sent, creates in-app notifications, and sends email through **Nodemailer** (SMTP). The same job schedules follow-up reminders for overdue, incomplete items.

**Planned endpoints (draft)**

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Log in |
| POST | `/api/auth/logout` | Log out |
| GET | `/api/auth/me` | Current user |
| GET/POST | `/api/courses` | List / create courses |
| PATCH/DELETE | `/api/courses/:id` | Update / delete course |
| GET | `/api/items?from=&to=&status=&type=&sort=` | List items (calendar range, to-do list, completed list) |
| POST | `/api/items` | Create item (returns `409` with conflicts unless `force=true`) |
| POST | `/api/items/check-conflicts` | Check a proposed event time range without saving |
| GET/PATCH/DELETE | `/api/items/:id` | Read / update / delete item |
| POST | `/api/items/:id/complete` · `/api/items/:id/reopen` | Mark complete / incomplete |
| GET/POST | `/api/items/:id/reminders` | List / add reminders on an item |
| PATCH/DELETE | `/api/reminders/:id` | Change / remove reminder |
| GET | `/api/notifications` · PATCH `/api/notifications/:id/read` | In-app reminder inbox |
| GET/PATCH | `/api/settings` | Default reminder offset, follow-up interval, time zone |

### 4.3 Database approach (`/database`)

- **PostgreSQL** relational database.
- Schema changes are managed as **numbered SQL migration files** in `database/migrations/` and applied in order by a migration runner (`node-pg-migrate`).
- `database/seeds/` holds fake demo data for development and presentations.
- All timestamps are stored as `TIMESTAMPTZ` (UTC).

#### Data model (draft)

| Table | Key columns |
|---|---|
| `users` | `id`, `name`, `email` (unique), `password_hash`, `time_zone`, `default_reminder_minutes`, `followup_interval_hours`, `followup_max_count`, `created_at` |
| `courses` | `id`, `user_id` → users, `name`, `color`, `created_at` |
| `items` | `id`, `user_id` → users, `course_id` → courses (nullable), `type` (`assignment` \| `task` \| `event`), `title`, `description`, `importance` (`low` \| `medium` \| `high`), `due_at`, `start_at`, `end_at`, `all_day`, `is_completed`, `completed_at`, `created_at`, `updated_at` |
| `reminders` | `id`, `item_id` → items, `kind` (`deadline` \| `follow_up`), `remind_at`, `sent_at`, `created_at` |
| `notifications` | `id`, `user_id` → users, `item_id` → items, `message`, `read_at`, `created_at` |
| `sessions` | managed by `connect-pg-simple` |

Relationships: a user has many courses, items, and notifications. A course has many items. An item has many reminders.

### 4.4 Tools and frameworks

| Area | Tool |
|---|---|
| Front end | React, Vite, React Router, FullCalendar, CSS |
| Back end | Node.js (LTS), Express, bcrypt, express-session, node-cron, Nodemailer, zod |
| Database | PostgreSQL, node-pg-migrate |
| Testing | Vitest + React Testing Library (client), Jest + Supertest (API) |
| Code quality | ESLint, Prettier |
| Collaboration | Git, GitHub (issues, pull requests, Projects board), Devin |
| Deployment (later prototype) | A free tier host such as Render or Railway for the API and database, and Netlify or Vercel for the client |

### 4.5 Development environments

- **Local:** the client runs on `http://localhost:5173`, the API on `http://localhost:4000`, and PostgreSQL locally or in Docker.
- **Configuration:** each app has an `.env.example` listing the required variables. Real `.env` files are never committed.

## 5. Important constraints

- **Timeline:** one academic semester, delivered as a series of prototypes. Prototype 1 is scaffolding and documentation only.
- **Team and skills:** a small student team. Technologies were chosen for good documentation and a gentle learning curve (one language, JavaScript, across the front end and back end).
- **Budget:** $0. Only free and open-source tools and free hosting tiers are used.
- **Single role:** only student accounts exist. There are no admin, instructor, or employer roles.
- **No third-party integrations:** no LMS, calendar sync, payment, or messaging APIs. The only external service is an SMTP provider for reminder emails.
- **Data privacy:** students' data is private to them. No sharing features.
- **Conflict handling:** the system may only *detect and warn* about conflicts. It must never change a user's schedule automatically.
- **Reminder delivery:** reminders are best-effort, within about a minute of the scheduled time, because they depend on the scheduler job and the email provider.
- **Site map:** the site map is hand-drawn and submitted separately (see [`SITEMAP.md`](SITEMAP.md)).

## 6. Related documents

- [`TASKS.md`](TASKS.md): development task list with acceptance criteria
- [`WORKSPACE_RULES.md`](WORKSPACE_RULES.md): naming, commits, branching, and pull request process
- [`SITEMAP.md`](SITEMAP.md): placeholder for the hand-drawn site map
