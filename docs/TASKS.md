# StudentSync — Development Task List

This file breaks the selected user stories in [`PRD.md`](PRD.md) into development tasks that can be built one at a time in later prototypes. Each phase builds on the one before it, so the app works (in a limited form) at the end of every phase.

**How to use this list**

- Each task becomes a GitHub issue named `T-x.y <title>` and is labeled with its user story.
- Work on a task in its own branch (see [`WORKSPACE_RULES.md`](WORKSPACE_RULES.md)).
- A task is **done** only when *all* of its acceptance criteria are true and its PR has been reviewed and merged.
- The mapping of phases to prototype numbers is a suggestion and can change with the course schedule.

**User story key**

| ID | User story |
|---|---|
| US-01 | Add, edit, and delete assignments and events |
| US-02 | Set dates and times for assignments and events |
| US-03 | Create an account and log in with email and password |
| US-04 | Assign colors to courses and related events |
| US-05 | Give tasks an importance rating |
| US-06 | Detect scheduling conflicts before saving timed events |
| US-07 | Switch between weekly and monthly calendar views |
| US-08 | View unfinished tasks ordered by importance |
| US-09 | Mark tasks complete and review completed work |
| US-10 | Set/change deadline reminders and receive due-date reminders |
| US-11 | Receive follow-up reminders for incomplete tasks |
| SETUP | Project infrastructure that supports all stories |

---

## Phase 0: Scaffolding (Prototype 1) ✅

### T-0.1 Create repository structure
- **Description:** Create the `/client`, `/api`, `/database`, and `/docs` folders, a root `README.md`, and a `.gitignore`.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [x] The four folders exist on `main`, each with a README describing its purpose.
  - [x] `.gitignore` excludes dependencies, environment files, local database files, OS files, and build artifacts.
  - [x] The root `README.md` explains the project, the Prototype 1 purpose, the repository structure, and the development plan.

### T-0.2 Write planning documentation
- **Description:** Write the PRD, this task list, the workspace rules, and a site map placeholder.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [x] `docs/PRD.md`, `docs/TASKS.md`, `docs/WORKSPACE_RULES.md`, and `docs/SITEMAP.md` exist.
  - [x] Every selected user story (US-01 to US-11) appears in the PRD and in at least one task.
  - [x] `docs/SITEMAP.md` is a placeholder only. The site map itself is hand-drawn and submitted separately.

---

## Phase 1: Project setup and accounts (suggested: Prototype 2)

### T-1.1 Initialize the client app
- **Description:** Create a React + Vite app in `/client` with React Router and a mobile-first base stylesheet.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [ ] `npm install && npm run dev` inside `/client` starts the app at `http://localhost:5173`.
  - [ ] A placeholder home route renders and the layout fits a 375 px wide screen without horizontal scrolling.
  - [ ] `client/.env.example` documents `VITE_API_URL`.

### T-1.2 Initialize the API
- **Description:** Create an Express app in `/api` with JSON parsing, CORS for the client origin, central error handling, and a health check.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [ ] `npm install && npm run dev` inside `/api` starts the server at `http://localhost:4000`.
  - [ ] `GET /api/health` returns `200` with `{ "status": "ok" }`.
  - [ ] Unknown routes return a JSON `404`, and thrown errors return a JSON `500` without stack traces in production.
  - [ ] `api/.env.example` documents `PORT`, `DATABASE_URL`, `SESSION_SECRET`, and `CLIENT_ORIGIN`.

### T-1.3 Set up the database and migrations
- **Description:** Configure PostgreSQL, the migration runner, and the first migration that creates the `users` table.
- **Feature / user story:** SETUP, US-03
- **Acceptance criteria:**
  - [ ] One documented command (for example, `npm run migrate`) applies all migrations in `database/migrations/` to an empty database.
  - [ ] The `users` table has `id`, `name`, `email` (unique, case-insensitive), `password_hash`, and `created_at`.
  - [ ] `database/README.md` explains how to create the local database and run the migrations and seeds.

### T-1.4 Add code quality and test tooling
- **Description:** Add ESLint, Prettier, and test runners (Vitest for the client, Jest + Supertest for the API), plus a GitHub Actions workflow.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [ ] `npm run lint` and `npm test` work in both `/client` and `/api`.
  - [ ] A GitHub Actions workflow runs lint and tests on every pull request.
  - [ ] At least one sample test passes in each app.

### T-1.5 Registration API
- **Description:** `POST /api/auth/register` creates a user with a bcrypt-hashed password and starts a session.
- **Feature / user story:** US-03
- **Acceptance criteria:**
  - [ ] A valid name, email, and password (at least 8 characters) creates a user and returns `201` with the user (never the password hash).
  - [ ] A duplicate email (any letter case) returns `409`. Invalid input returns `400` with field messages.
  - [ ] The stored `password_hash` is a bcrypt hash, not the plain password.
  - [ ] Automated tests cover success, duplicate email, and validation errors.

### T-1.6 Login, logout, and session API
- **Description:** Add session-based login (`POST /api/auth/login`), logout (`POST /api/auth/logout`), and current user (`GET /api/auth/me`) endpoints.
- **Feature / user story:** US-03
- **Acceptance criteria:**
  - [ ] Correct credentials return `200` and set an HTTP-only session cookie. Wrong credentials return `401` with a generic message that does not reveal which field was wrong.
  - [ ] `GET /api/auth/me` returns the logged-in user, or `401` when logged out.
  - [ ] Logout destroys the session, so `/api/auth/me` returns `401` afterward.
  - [ ] Sessions survive an API restart (stored in PostgreSQL).

### T-1.7 Auth guard and data ownership
- **Description:** Add `requireAuth` middleware and a shared pattern that filters every query by the logged-in user's ID.
- **Feature / user story:** US-03
- **Acceptance criteria:**
  - [ ] Every non-auth endpoint returns `401` when there is no session.
  - [ ] Requests for another user's resource return `404`, and the resource is not changed.
  - [ ] A test with two users proves that neither can read, edit, or delete the other's data.

### T-1.8 Registration, login, and logout screens
- **Description:** Build the register and login screens, protected routes, and a logout control in the client.
- **Feature / user story:** US-03
- **Acceptance criteria:**
  - [ ] A user can register, is logged in automatically, and lands on the main screen.
  - [ ] A user can log out and log back in. Refreshing the page keeps them logged in.
  - [ ] Visiting a protected screen while logged out redirects to login.
  - [ ] Validation and server errors are shown next to the form fields. The forms are usable on a phone.

---

## Phase 2: Assignments, tasks, and events with dates and times (suggested: Prototype 2–3)

### T-2.1 Items table migration
- **Description:** Add the `items` table (type, title, description, due/start/end times, all-day, timestamps).
- **Feature / user story:** US-01, US-02
- **Acceptance criteria:**
  - [ ] The migration creates `items` with the columns listed in the PRD data model, a `user_id` foreign key (cascade on user delete), and a `CHECK` on `type`.
  - [ ] All date-time columns are `TIMESTAMPTZ`.
  - [ ] An index on `(user_id, due_at)` and `(user_id, start_at)` exists.

### T-2.2 Item CRUD API
- **Description:** Add `GET/POST /api/items` and `GET/PATCH/DELETE /api/items/:id`, scoped to the logged-in user.
- **Feature / user story:** US-01
- **Acceptance criteria:**
  - [ ] A user can create, list, read, update, and delete their own items.
  - [ ] `title` (1–200 characters) and `type` are required. `description` is optional.
  - [ ] Changes are saved in the database and still exist after an API restart.
  - [ ] Ownership rules from T-1.7 are enforced and covered by tests.

### T-2.3 Date and time rules
- **Description:** Validate and store dates and times for each item type.
- **Feature / user story:** US-02
- **Acceptance criteria:**
  - [ ] Assignments and tasks require `due_at`. The due time is optional; if it is missing, the item is due at the end of that day.
  - [ ] Events require `start_at` and `end_at` with `end_at > start_at`, unless `all_day` is true.
  - [ ] Times are stored in UTC and returned in ISO 8601 format. The client displays them in the user's local time zone.
  - [ ] Invalid dates or times return `400` with a clear message.

### T-2.4 Item form (create and edit)
- **Description:** Build one mobile-friendly form for adding and editing items, with fields that change based on the item type.
- **Feature / user story:** US-01, US-02
- **Acceptance criteria:**
  - [ ] The form has title, description, type, and date/time inputs (due date/time for assignments and tasks; start/end or all-day for events).
  - [ ] Saving creates or updates the item and returns to the previous screen with a success message.
  - [ ] Editing pre-fills the current values.
  - [ ] Required-field and date errors are shown before submitting and also when the API rejects the request.

### T-2.5 Item list with edit and delete
- **Description:** Show the user's items in a simple list with Edit and Delete actions.
- **Feature / user story:** US-01, US-02
- **Acceptance criteria:**
  - [ ] Items are listed in chronological order and show their type, title, and date/time.
  - [ ] Each item has Edit (opens the form) and Delete actions. Delete asks for confirmation before removing the item.
  - [ ] Users only ever see their own items.

---

## Phase 3: Courses, importance, and progress (suggested: Prototype 3)

### T-3.1 Courses data and API
- **Description:** Add a `courses` migration (`name`, `color`), add `course_id` to `items`, and add course CRUD endpoints.
- **Feature / user story:** US-04
- **Acceptance criteria:**
  - [ ] A user can create, list, edit, and delete their own courses through `/api/courses`.
  - [ ] `color` must be one of the preset palette values. Invalid colors return `400`.
  - [ ] Deleting a course sets `course_id` to `NULL` on its items instead of deleting them.

### T-3.2 Course management screen and color picker
- **Description:** Build UI to manage courses and pick a color from the palette.
- **Feature / user story:** US-04
- **Acceptance criteria:**
  - [ ] A user can add, rename, recolor, and delete courses from the UI.
  - [ ] The color picker shows the palette as swatches with accessible labels (for example, "Blue").
  - [ ] The item form has a course dropdown that includes "No course".

### T-3.3 Show course colors on items
- **Description:** Use course colors wherever items appear.
- **Feature / user story:** US-04
- **Acceptance criteria:**
  - [ ] Items linked to a course show that course's color (for example, as a colored bar or dot) and the course name.
  - [ ] Changing a course's color updates all of its items without editing each item.
  - [ ] Text on colored backgrounds meets WCAG AA contrast.

### T-3.4 Importance rating
- **Description:** Add `importance` (`low` | `medium` | `high`, default `medium`) to items in the API and the form.
- **Feature / user story:** US-05
- **Acceptance criteria:**
  - [ ] Assignments and tasks can be created or edited with an importance rating. Omitting it saves `medium`.
  - [ ] Invalid values return `400`.
  - [ ] Importance is shown on each item with both text and an icon or color, not color alone.

### T-3.5 To-Do view ordered by importance
- **Description:** Add a screen that lists unfinished assignments and tasks, sorted by importance and then by due date.
- **Feature / user story:** US-08
- **Acceptance criteria:**
  - [ ] Only incomplete assignments and tasks are shown. Events and completed items are excluded.
  - [ ] Items are ordered high → medium → low, then by soonest due date within each level.
  - [ ] Overdue items are clearly flagged.
  - [ ] An empty state appears when there is nothing left to do.

### T-3.6 Mark complete and incomplete
- **Description:** Add `is_completed` and `completed_at`, the `complete` and `reopen` endpoints, and a checkbox or button in the UI.
- **Feature / user story:** US-09
- **Acceptance criteria:**
  - [ ] Marking an item complete records `completed_at` and removes it from the To-Do view right away.
  - [ ] An item can be marked incomplete again, which clears `completed_at` and returns it to the To-Do view.
  - [ ] The change is saved and survives a page refresh.

### T-3.7 Completed work view
- **Description:** Add a screen to review completed items.
- **Feature / user story:** US-09
- **Acceptance criteria:**
  - [ ] Completed items are listed newest first, with their completion date.
  - [ ] The list can be filtered by course.
  - [ ] Each item can be reopened from this view.

---

## Phase 4: Calendar views and conflict detection (suggested: Prototype 4)

### T-4.1 Monthly calendar view
- **Description:** Show items on a monthly calendar using FullCalendar.
- **Feature / user story:** US-07
- **Acceptance criteria:**
  - [ ] The current month shows all of the user's items on their dates, in course colors.
  - [ ] Previous, Next, and Today controls change the month, and only that date range is loaded from the API (`from`/`to`).
  - [ ] Tapping an item opens its details or edit form.
  - [ ] The view is readable on a 375 px screen (for example, with "+N more" for busy days).

### T-4.2 Weekly view and view toggle
- **Description:** Add a weekly time-grid view and a toggle between the weekly and monthly views.
- **Feature / user story:** US-07
- **Acceptance criteria:**
  - [ ] A Week/Month toggle switches views without reloading the page.
  - [ ] The weekly view places timed events in their time slots and shows all-day items and due dates in an all-day row.
  - [ ] The selected view is remembered when the user returns to the calendar.

### T-4.3 Conflict detection service and API
- **Description:** Detect overlapping timed events on the server before saving.
- **Feature / user story:** US-06
- **Acceptance criteria:**
  - [ ] Creating or updating a timed event that overlaps another of the user's timed events returns `409` with the list of conflicting events, unless the request includes `force: true`.
  - [ ] Back-to-back events (one ends exactly when the next starts) are **not** conflicts. All-day events, assignments, tasks, and other users' events are ignored.
  - [ ] When editing an event, it is not compared with itself.
  - [ ] `POST /api/items/check-conflicts` returns conflicts for a proposed time range without saving.
  - [ ] Unit tests cover overlap, no overlap, touching edges, and edits.

### T-4.4 Conflict warning in the UI
- **Description:** Show a warning dialog when saving an event causes a conflict.
- **Feature / user story:** US-06
- **Acceptance criteria:**
  - [ ] Saving a conflicting event opens a dialog that lists each conflicting event's title and time.
  - [ ] **Save anyway** saves the event with `force: true`. **Go back** returns to the form with no changes saved.
  - [ ] The app never moves or changes any event automatically.

---

## Phase 5: Reminders (suggested: Prototype 5)

### T-5.1 Reminder data model and user settings
- **Description:** Add the `reminders` and `notifications` tables and the reminder settings columns on `users`.
- **Feature / user story:** US-10, US-11
- **Acceptance criteria:**
  - [ ] The migrations create `reminders` (`kind`, `remind_at`, `sent_at`) and `notifications` as described in the PRD.
  - [ ] `users` has `default_reminder_minutes`, `followup_interval_hours` (default 24), `followup_max_count` (default 3), and `time_zone`.
  - [ ] Deleting an item deletes its reminders.

### T-5.2 Reminder API (set and change)
- **Description:** Add endpoints to add, list, change, and remove deadline reminders on an item, and a settings endpoint.
- **Feature / user story:** US-10
- **Acceptance criteria:**
  - [ ] A user can add one or more reminders to their own item, either as an offset before the due/start time or as an exact date/time.
  - [ ] A user can change or delete a reminder that has not been sent.
  - [ ] When an item's due/start time changes, its offset-based reminders are recalculated.
  - [ ] `GET/PATCH /api/settings` reads and updates the default reminder offset and follow-up settings.
  - [ ] New items automatically get the user's default reminder (if one is set).

### T-5.3 Reminder controls in the UI
- **Description:** Add reminder controls to the item form and a reminder settings screen.
- **Feature / user story:** US-10
- **Acceptance criteria:**
  - [ ] The item form lets the user add, change, and remove reminders with presets (10 min, 1 hour, 1 day, 1 week before) or a custom date/time.
  - [ ] The settings screen lets the user choose a default reminder.
  - [ ] Saved reminders appear on the item's details.

### T-5.4 Reminder scheduler and in-app notifications
- **Description:** Add a `node-cron` job that delivers due reminders as in-app notifications.
- **Feature / user story:** US-10
- **Acceptance criteria:**
  - [ ] Every minute, the job finds unsent reminders with `remind_at <= now` for incomplete items, creates a notification, and sets `sent_at`.
  - [ ] Each reminder is delivered only once, even if the job runs again or overlaps with a previous run.
  - [ ] The client shows an unread-count badge and a notification list. Opening a notification goes to its item and marks it read.
  - [ ] Reminders for completed or deleted items are not delivered.

### T-5.5 Email reminders
- **Description:** Send reminder emails through Nodemailer when a reminder is delivered.
- **Feature / user story:** US-10
- **Acceptance criteria:**
  - [ ] Each delivered reminder also sends an email to the user that includes the item title, due/start time (in the user's time zone), and a link to the app.
  - [ ] SMTP settings come from environment variables. In development, emails go to a test inbox (for example, Ethereal or Mailpit).
  - [ ] An email failure is logged and does not stop the in-app notification or other reminders.

### T-5.6 Follow-up reminders for incomplete tasks
- **Description:** Automatically remind users about overdue, incomplete assignments and tasks.
- **Feature / user story:** US-11
- **Acceptance criteria:**
  - [ ] When an assignment or task passes its due time without being completed, a `follow_up` reminder is delivered (in-app and email).
  - [ ] Follow-ups repeat every `followup_interval_hours` until the item is completed, `followup_max_count` is reached, or follow-ups are turned off.
  - [ ] Completing or deleting the item stops all further follow-ups.
  - [ ] Tests use a controllable clock to cover first follow-up, repeat, max count, and stop on completion.

### T-5.7 Follow-up settings in the UI
- **Description:** Let users configure or turn off follow-up reminders.
- **Feature / user story:** US-11
- **Acceptance criteria:**
  - [ ] The settings screen has an on/off switch, an interval, and a maximum count for follow-ups.
  - [ ] Changes are saved and apply to the next scheduled follow-up.

---

## Phase 6: Polish and release (suggested: final prototype)

### T-6.1 Mobile and accessibility pass
- **Description:** Review every screen at phone, tablet, and desktop widths and against basic accessibility checks.
- **Feature / user story:** All (NFR-1, NFR-5)
- **Acceptance criteria:**
  - [ ] No screen scrolls horizontally at 360 px. Touch targets are at least 44×44 px.
  - [ ] All form fields have labels. Every screen can be used with the keyboard only.
  - [ ] Lighthouse accessibility score of 90 or higher on the main screens.

### T-6.2 Seed data and demo script
- **Description:** Add demo seed data and a short demo walkthrough.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [ ] One command loads a demo user with courses, items of each type, completed items, one conflict, and reminders.
  - [ ] `docs/` contains a step-by-step demo script that covers every user story.

### T-6.3 Deployment
- **Description:** Deploy the client, API, and database to free-tier hosting.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [ ] The app is reachable over HTTPS at a public URL, with secrets set as environment variables on the host.
  - [ ] Migrations run against the production database. The reminder job runs in production.
  - [ ] The README has the live URL and deployment notes.

---

## Traceability: user stories → tasks

| User story | Tasks |
|---|---|
| US-01 Add, edit, and delete assignments and events | T-2.1, T-2.2, T-2.4, T-2.5 |
| US-02 Set dates and times | T-2.1, T-2.3, T-2.4, T-2.5 |
| US-03 Account and email/password login | T-1.3, T-1.5, T-1.6, T-1.7, T-1.8 |
| US-04 Course colors | T-3.1, T-3.2, T-3.3 |
| US-05 Importance rating | T-3.4 |
| US-06 Conflict detection before saving | T-4.3, T-4.4 |
| US-07 Weekly and monthly calendar views | T-4.1, T-4.2 |
| US-08 Unfinished tasks ordered by importance | T-3.5 |
| US-09 Mark complete and review completed work | T-3.6, T-3.7 |
| US-10 Deadline reminders | T-5.1, T-5.2, T-5.3, T-5.4, T-5.5 |
| US-11 Follow-up reminders | T-5.1, T-5.6, T-5.7 |
