# StudentSync — Development Task List

This file breaks the 11 selected user stories in [`PRD.md`](PRD.md) into development tasks that can be built one at a time in later prototypes. Each phase builds on the one before it.

**How to use this list**

- Each task becomes a GitHub issue named `T-x.y <title>` and is labeled with its user story.
- Work on a task in its own branch (see [`WORKSPACE_RULES.md`](WORKSPACE_RULES.md)).
- A task is **done** only when *all* of its acceptance criteria are true and its PR has been reviewed and merged.
- Tasks marked **⚠ Depends on Qn** need an answer to that open question ([PRD A5](PRD.md#a5-open-questions-for-the-analyst)) before they can be finished. Do not invent the missing behavior.
- Technical details (endpoints, tables, libraries) follow the **proposed** design in PRD Part B and can change.
- The phase-to-prototype mapping is a suggestion and can change with the course schedule.

**User story key**

| ID | Selected user story |
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
  - [x] The four folders exist, each with a README describing its purpose.
  - [x] `.gitignore` excludes dependencies, environment files, local database files, OS files, and build artifacts.
  - [x] The root `README.md` explains the project, the Prototype 1 purpose, the repository structure, and the development plan.

### T-0.2 Write planning documentation
- **Description:** Write the PRD, this task list, the workspace rules, and a site map placeholder.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [x] `docs/PRD.md`, `docs/TASKS.md`, `docs/WORKSPACE_RULES.md`, and `docs/SITEMAP.md` exist.
  - [x] Every selected user story (US-01 to US-11) appears in the PRD and in at least one task.
  - [x] `docs/SITEMAP.md` is a placeholder only. The site map is hand-drawn and submitted separately.

---

## Phase 1: Project setup and accounts (suggested: Prototype 2)

### T-1.1 Initialize the client app
- **Description:** Create the front-end app in `/client` (proposed: React + Vite) with routing and a responsive base layout.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [ ] One documented command installs the dependencies and another starts the client locally.
  - [ ] A placeholder page renders in both mobile and desktop browsers.
  - [ ] `client/.env.example` lists the required configuration (for example, the API URL).

### T-1.2 Initialize the API
- **Description:** Create the back-end app in `/api` (proposed: Node.js + Express) with JSON handling, error handling, and a health check.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [ ] One documented command installs the dependencies and another starts the API locally.
  - [ ] `GET /api/health` returns a success response.
  - [ ] Unknown routes and server errors return JSON error responses.
  - [ ] `api/.env.example` lists the required configuration (for example, database URL and session secret).

### T-1.3 Set up the database and migrations
- **Description:** Configure the database (proposed: PostgreSQL), a migration runner, and the first migration that creates the `users` table.
- **Feature / user story:** SETUP, US-03
- **Acceptance criteria:**
  - [ ] One documented command applies all migrations in `database/migrations/` to an empty database.
  - [ ] The `users` table stores a unique email and a password hash.
  - [ ] `database/README.md` explains how to create the local database and run the migrations and seeds.

### T-1.4 Add code quality and test tooling
- **Description:** Add linting, formatting, and test runners for the client and API, and a GitHub Actions workflow that runs them.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [ ] Lint and test commands work in both `/client` and `/api`.
  - [ ] A GitHub Actions workflow runs lint and tests on every pull request.
  - [ ] At least one sample test passes in each app.

### T-1.5 Account creation (API)
- **Description:** An endpoint that creates an account with an email and password.
- **Feature / user story:** US-03
- **Acceptance criteria:**
  - [ ] A valid email and password create an account. The response never includes the password or its hash.
  - [ ] An email that is already registered is rejected with an error.
  - [ ] Invalid input (for example, a malformed email or a missing password) is rejected with an error.
  - [ ] The password is stored only as a hash.
  - [ ] Automated tests cover success, duplicate email, and invalid input.

### T-1.6 Login and logout (API)
- **Description:** Endpoints to log in with email and password, log out, and get the current user.
- **Feature / user story:** US-03
- **Acceptance criteria:**
  - [ ] Correct credentials start a session. Incorrect credentials are rejected.
  - [ ] The current-user endpoint returns the logged-in user, or an unauthorized error when no one is logged in.
  - [ ] Logging out ends the session.

### T-1.7 Auth guard and data ownership
- **Description:** Middleware that requires login, and a query pattern that limits data to the logged-in user.
- **Feature / user story:** US-03
- **Acceptance criteria:**
  - [ ] Endpoints other than registration and login reject requests that have no session.
  - [ ] A user cannot read, edit, or delete another user's data. A test with two users proves this.

### T-1.8 Account creation, login, and logout screens
- **Description:** Front-end screens and flow for creating an account, logging in, and logging out.
- **Feature / user story:** US-03
- **Acceptance criteria:**
  - [ ] A user can create an account with email and password.
  - [ ] A user can log in with email and password and log out.
  - [ ] Screens that require an account are not reachable while logged out.
  - [ ] Errors from the API are shown to the user.

---

## Phase 2: Assignments and events with dates and times (suggested: Prototype 2–3)

### T-2.1 Items table migration
- **Description:** Add the table that stores assignments and events, including their date/time fields.
- **Feature / user story:** US-01, US-02
- **Acceptance criteria:**
  - [ ] The migration creates the items table with an owner (`user_id`), title, description, item type, and date/time columns.
  - [ ] Date/time columns store time zone information.

### T-2.2 Item CRUD API
- **Description:** Endpoints to add, list, view, edit, and delete the logged-in user's assignments and events.
- **Feature / user story:** US-01
- **Acceptance criteria:**
  - [ ] A user can add, edit, and delete their own assignments and events through the API.
  - [ ] Changes are saved in the database and remain after the API restarts.
  - [ ] The ownership rules from T-1.7 apply and are covered by tests.

### T-2.3 Dates and times on items (API)
- **Description:** Accept, validate, and store dates and times for assignments and events.
- **Feature / user story:** US-02
- **Acceptance criteria:**
  - [ ] A date and time can be set when an assignment or event is created, and changed when it is edited.
  - [ ] Invalid dates or times are rejected with an error.
  - [ ] Saved dates and times are returned in a consistent, documented format.

### T-2.4 Item form (add and edit)
- **Description:** A front-end form for adding and editing assignments and events, including their date and time.
- **Feature / user story:** US-01, US-02
- **Acceptance criteria:**
  - [ ] A user can add an assignment or event with a date and time.
  - [ ] A user can edit an existing assignment or event, and the form shows its current values.
  - [ ] Validation errors are shown to the user.

### T-2.5 View and delete items
- **Description:** A front-end view of the user's assignments and events, with edit and delete actions.
- **Feature / user story:** US-01, US-02
- **Acceptance criteria:**
  - [ ] The user's assignments and events are displayed with their dates and times.
  - [ ] Each item can be opened for editing or deleted.
  - [ ] A user sees only their own items.

---

## Phase 3: Courses, importance, and completion (suggested: Prototype 3)

### T-3.1 Courses and colors (API)
- **Description:** Store courses with a color and let items be linked to a course.
- **Feature / user story:** US-04
- **Acceptance criteria:**
  - [ ] A user can create courses and assign or change each course's color.
  - [ ] An assignment or event can be linked to one of the user's courses.
  - [ ] Users can access only their own courses.
- **⚠ Depends on Q3:** deleting courses, and what happens to their items, is not defined yet.

### T-3.2 Courses and colors (UI)
- **Description:** Front-end controls to create courses, choose their colors, and link items to a course.
- **Feature / user story:** US-04
- **Acceptance criteria:**
  - [ ] A user can create a course and assign it a color from the UI.
  - [ ] A user can change a course's color.
  - [ ] The item form lets the user link an item to a course.

### T-3.3 Show course colors on related events
- **Description:** Display a course's color on its related events and items.
- **Feature / user story:** US-04
- **Acceptance criteria:**
  - [ ] Items linked to a course are shown in that course's color.
  - [ ] Changing a course's color updates how its related items are displayed.

### T-3.4 Importance rating
- **Description:** Store an importance rating on tasks and let users set and change it.
- **Feature / user story:** US-05
- **Acceptance criteria:**
  - [ ] A user can give a task an importance rating and change it later.
  - [ ] The importance rating is saved and shown with the task.
- **⚠ Depends on Q1 and Q2:** which items are "tasks," and the rating scale. (A proposed implementation detail, *not* a requirement, is a three-level scale such as low / medium / high.)

### T-3.5 Unfinished tasks ordered by importance
- **Description:** A view that lists the user's unfinished tasks ordered by importance.
- **Feature / user story:** US-08
- **Acceptance criteria:**
  - [ ] Only unfinished tasks are listed.
  - [ ] Tasks are ordered by importance rating.
- **⚠ Depends on Q1 and Q2.** Proposed UI ideas, *not* requirements: a secondary sort by date and an indicator for past-due tasks.

### T-3.6 Mark tasks complete
- **Description:** Let users mark a task complete (API and UI).
- **Feature / user story:** US-09
- **Acceptance criteria:**
  - [ ] A user can mark a task complete, and the change is saved.
  - [ ] Completed tasks no longer appear in the unfinished-tasks view (T-3.5).

### T-3.7 Review completed work
- **Description:** A view where users can review the tasks they have completed.
- **Feature / user story:** US-09
- **Acceptance criteria:**
  - [ ] A user can see their completed tasks.
  - [ ] Users see only their own completed work.
- **⚠ Depends on Q7:** what "review" includes beyond listing completed tasks.

---

## Phase 4: Calendar views and conflict detection (suggested: Prototype 4)

### T-4.1 Monthly calendar view
- **Description:** Show the user's assignments and events on a monthly calendar.
- **Feature / user story:** US-07
- **Acceptance criteria:**
  - [ ] Assignments and events appear on their dates in a monthly view.
  - [ ] The user can move between months.
  - [ ] Course colors (US-04) are used for related events.

### T-4.2 Weekly view and view switching
- **Description:** Add a weekly calendar view and a control to switch between weekly and monthly views.
- **Feature / user story:** US-07
- **Acceptance criteria:**
  - [ ] Assignments and events appear at their dates and times in a weekly view.
  - [ ] The user can switch between the weekly and monthly views.
  - [ ] The user can move between weeks.

### T-4.3 Conflict check (API)
- **Description:** Check a timed event for scheduling conflicts with the user's other timed events before it is saved.
- **Feature / user story:** US-06
- **Acceptance criteria:**
  - [ ] Before a timed event is saved (created or edited), the API detects whether it overlaps any of the user's other timed events and returns the conflicting events.
  - [ ] Only the same user's events are checked, and an edited event is not compared with itself.
  - [ ] The API never moves or changes events to resolve a conflict.
  - [ ] Unit tests cover overlapping, non-overlapping, and edited events.

### T-4.4 Conflict check (UI)
- **Description:** Run the conflict check before saving a timed event and tell the user about any conflicts.
- **Feature / user story:** US-06
- **Acceptance criteria:**
  - [ ] When a user saves a timed event, the conflict check runs before the event is saved.
  - [ ] Detected conflicts are shown to the user, including which events conflict.
  - [ ] No event is changed automatically.
- **⚠ Depends on Q4:** the options the user has after a conflict is detected.

---

## Phase 5: Reminders (suggested: Prototype 5)

### T-5.1 Reminder data model
- **Description:** Add storage for deadline and follow-up reminders.
- **Feature / user story:** US-10, US-11
- **Acceptance criteria:**
  - [ ] A migration creates a reminders table linked to items, with the reminder type and time.
  - [ ] Users can access only reminders on their own items.

### T-5.2 Set and change deadline reminders
- **Description:** Let users set and change deadline reminders on their items (API and UI).
- **Feature / user story:** US-10
- **Acceptance criteria:**
  - [ ] A user can set a deadline reminder on an assignment or event.
  - [ ] A user can change or remove a reminder they set.
  - [ ] Reminders are saved and shown with the item.
- **⚠ Depends on Q6:** whether there are default reminder times.

### T-5.3 Reminder scheduler
- **Description:** A scheduled background job in the API that finds reminders that are due.
- **Feature / user story:** US-10, US-11
- **Acceptance criteria:**
  - [ ] The job finds reminders whose time has arrived and that have not been delivered.
  - [ ] Each reminder is delivered at most once.
  - [ ] Reminders on completed or deleted items are not delivered.

### T-5.4 Receive due-date reminders
- **Description:** Deliver due-date reminders to the user.
- **Feature / user story:** US-10
- **Acceptance criteria:**
  - [ ] When a deadline reminder is due, the user receives it.
  - [ ] The reminder identifies the assignment or event and when it is due.
- **⚠ Depends on Q5:** the delivery channel. A proposed implementation detail, *not* a requirement, is in-app notifications.

### T-5.5 Follow-up reminders for incomplete tasks
- **Description:** Send follow-up reminders for tasks that are still incomplete.
- **Feature / user story:** US-11
- **Acceptance criteria:**
  - [ ] The user receives a follow-up reminder for a task that is still incomplete.
  - [ ] Once a task is marked complete, its follow-up reminders stop.
  - [ ] Tests use a controllable clock to verify when follow-ups are generated.
- **⚠ Depends on Q1, Q5, and Q6:** which items get follow-ups, the delivery channel, and timing and frequency.

---

## Phase 6: Polish and release (suggested: final prototype)

### T-6.1 Responsive review
- **Description:** Review every screen in mobile and desktop browsers.
- **Feature / user story:** All
- **Acceptance criteria:**
  - [ ] Every screen is usable in current mobile and desktop browsers.
  - [ ] Form fields have labels, and the main flows can be completed with a keyboard.

### T-6.2 Seed data and demo script
- **Description:** Add demo seed data and a short demo walkthrough.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [ ] One command loads fake demo data that exercises each user story.
  - [ ] `docs/` contains a step-by-step demo script that covers every selected user story.

### T-6.3 Deployment
- **Description:** Deploy the client, API, and database to a hosting provider.
- **Feature / user story:** SETUP
- **Acceptance criteria:**
  - [ ] The app is reachable over HTTPS at a public URL, with secrets set as environment variables.
  - [ ] Migrations and the reminder job run in the deployed environment.
  - [ ] The README documents the URL and the deployment steps.

---

## Traceability: user stories → tasks

| User story | Tasks |
|---|---|
| US-01 Add, edit, and delete assignments and events | T-2.1, T-2.2, T-2.4, T-2.5 |
| US-02 Set dates and times | T-2.1, T-2.3, T-2.4, T-2.5 |
| US-03 Create an account and log in with email and password | T-1.3, T-1.5, T-1.6, T-1.7, T-1.8 |
| US-04 Assign colors to courses and related events | T-3.1, T-3.2, T-3.3, T-4.1 |
| US-05 Give tasks an importance rating | T-3.4 |
| US-06 Detect scheduling conflicts before saving timed events | T-4.3, T-4.4 |
| US-07 Switch between weekly and monthly calendar views | T-4.1, T-4.2 |
| US-08 View unfinished tasks ordered by importance | T-3.5 |
| US-09 Mark tasks complete and review completed work | T-3.6, T-3.7 |
| US-10 Set/change deadline reminders and receive due-date reminders | T-5.1, T-5.2, T-5.3, T-5.4 |
| US-11 Receive follow-up reminders for incomplete tasks | T-5.1, T-5.3, T-5.5 |
