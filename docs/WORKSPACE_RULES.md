# StudentSync — Workspace Rules (Development Workflow)

These rules keep the team's work consistent and reviewable on GitHub. They apply to every contributor, including AI assistants such as Devin.

---

## 1. Naming conventions

### Files and folders

| What | Convention | Example |
|---|---|---|
| Top-level folders | lowercase | `client/`, `api/`, `database/`, `docs/` |
| React components and pages | `PascalCase.jsx` | `TaskCard.jsx`, `CalendarPage.jsx` |
| Other JS modules (hooks, utils, services, routes) | `camelCase.js` | `useAuth.js`, `conflictService.js`, `itemsRoutes.js` |
| Test files | same name as the file under test + `.test.js(x)` | `conflictService.test.js` |
| CSS files | match the component, or `kebab-case.css` for globals | `TaskCard.css`, `global-variables.css` |
| SQL migrations | `NNN_snake_case_description.sql` | `003_create_items.sql` |
| Seed files | `NNN_snake_case_description.sql` | `001_demo_user.sql` |
| Documentation | `UPPER_SNAKE_CASE.md` in `docs/` | `PRD.md`, `WORKSPACE_RULES.md` |

### Code

| What | Convention | Example |
|---|---|---|
| Variables and functions | `camelCase` | `dueAt`, `findConflicts()` |
| React components and classes | `PascalCase` | `CourseColorPicker` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_TITLE_LENGTH` |
| Booleans | start with `is`/`has`/`should` | `isCompleted`, `hasConflict` |
| Environment variables | `UPPER_SNAKE_CASE` (client vars prefixed `VITE_`) | `DATABASE_URL`, `VITE_API_URL` |

### Database

- Tables: plural `snake_case` (`users`, `courses`, `items`, `reminders`).
- Columns: `snake_case` (`due_at`, `is_completed`). Foreign keys are `<singular>_id` (`user_id`, `course_id`).
- Timestamps end in `_at` and use `TIMESTAMPTZ`.

### API routes

- Plural nouns, lowercase, kebab-case if multi-word: `/api/items`, `/api/items/:id/reminders`, `/api/items/check-conflicts`.
- HTTP verbs describe the action (`GET` read, `POST` create, `PATCH` update, `DELETE` remove).

## 2. Branching strategy

We use a simple **GitHub Flow** model.

- `main` is always in a working, demo-ready state. **Nobody pushes directly to `main`.** All changes arrive by pull request.
- Create one short-lived branch per task from the latest `main`:

  ```
  <type>/<task-id>-<short-description>
  ```

  | Type | Use for | Example |
  |---|---|---|
  | `feature/` | new functionality | `feature/T-2.3-item-crud-api` |
  | `fix/` | bug fixes | `fix/T-4.2-conflict-off-by-one` |
  | `docs/` | documentation only | `docs/update-prd-reminders` |
  | `chore/` | tooling, config, dependencies | `chore/add-eslint` |
  | `test/` | adding or fixing tests only | `test/T-3.4-todo-sort` |

  Branches created by Devin may use the `devin/<timestamp>-<description>` format. They follow the same review rules.
- Keep branches small (ideally one task from `docs/TASKS.md`) and merge within a few days to avoid conflicts.
- Before opening a PR, update your branch with the latest `main` (`git pull origin main` or rebase) and resolve conflicts locally.
- Delete the branch after it is merged.
- At the end of each prototype, tag `main` (for example, `prototype-2`) so the submitted version can be found later.

## 3. Commit message guidelines

Use the **Conventional Commits** style:

```
<type>(<optional scope>): <short summary in imperative mood>

<optional body: what and why, wrapped at ~72 characters>

<optional footer: Refs #12, Closes #12>
```

- **Types:** `feat`, `fix`, `docs`, `style` (formatting only), `refactor`, `test`, `chore`.
- **Scopes:** `client`, `api`, `database`, `docs`, or a feature (`auth`, `calendar`, `reminders`).
- **Summary:** imperative mood ("add", not "added"), 50 characters or fewer, no trailing period.
- Make one logical change per commit. Don't mix unrelated changes.
- Reference the GitHub issue or task ID when there is one.
- Never commit secrets, `.env` files, `node_modules/`, local database files, or build output (see `.gitignore`).

**Examples**

```
feat(api): add POST /api/items with validation
fix(calendar): show all-day events in weekly view
docs: add acceptance criteria for reminder tasks
chore(client): configure ESLint and Prettier
test(api): cover overlapping event conflict cases
```

## 4. Pull request and review process

1. **Pick a task.** Each task in `docs/TASKS.md` becomes a GitHub issue. Assign it to yourself and move it to "In Progress" on the project board.
2. **Branch and build.** Create a branch (Section 2) and commit using the guidelines in Section 3.
3. **Self-check before opening the PR:**
   - The app builds and runs locally.
   - Lint passes and the tests pass (once tooling exists).
   - The task's acceptance criteria are met.
   - Docs are updated if behavior, setup, or the data model changed.
4. **Open a pull request into `main`** with:
   - A clear title in commit style (for example, `feat(api): item CRUD endpoints`).
   - A description: what changed, why, how to test it, and a link to the issue (`Closes #12`).
   - Screenshots or a short recording for UI changes (mobile and desktop widths).
   - Draft status if it is still a work in progress.
5. **Review.**
   - At least **one teammate approval** is required before merging. The author cannot approve their own PR.
   - Reviewers check correctness, the acceptance criteria, readability, security (auth checks, no secrets), and mobile layout.
   - Reviewers should respond within **48 hours**. Keep comments specific and respectful. Use "suggestion:" for optional changes and "required:" for blocking changes.
   - The author addresses every comment, either by changing the code or by replying with a reason, and then re-requests review.
6. **Merge.**
   - Use **Squash and merge** so each PR becomes one clean commit on `main`, and keep the squash message in Conventional Commit format.
   - The author merges after approval and passing checks, deletes the branch, and moves the issue to "Done".

### Working with Devin (AI assistant)

- Give Devin a specific task ID from `docs/TASKS.md` and point it to this file and `docs/PRD.md`.
- Devin opens pull requests like any team member. **A human teammate must review and approve every Devin PR**, and Devin does not merge its own PRs.
- Check AI-generated code and docs for scope creep. They must not add features listed as out of scope, or behavior that is not in the Analyst requirements (Part A of `docs/PRD.md`).
- Credit AI assistance in the PR description when required by the course's academic integrity policy.

## 5. Repository settings (recommended)

- Protect `main`: require a pull request, at least one approval, and passing status checks before merging, and disallow force-pushes.
- Use GitHub Issues and a GitHub Projects board with the columns **Backlog → To Do → In Progress → In Review → Done**.
- Add labels: `client`, `api`, `database`, `docs`, `bug`, `enhancement`, plus one per user story (`US-01` … `US-11`).
