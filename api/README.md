# /api — Back-end / REST API

This folder will contain the StudentSync back end: a JSON REST API for accounts, courses, assignments/events, conflict checks, and reminders.

**Status (Prototype 1):** placeholder only. No application code yet.

## Proposed stack (not final)

- Node.js (LTS) + Express
- `pg` (node-postgres) for PostgreSQL access
- `bcrypt` for password hashing
- `express-session` + `connect-pg-simple` for login sessions (HTTP-only cookies)
- `node-cron` for the scheduled reminder job
- Jest + Supertest for API tests

## Planned layout (created when development starts)

```
api/
  src/
    routes/            # Express routers (auth, courses, items, reminders)
    controllers/       # request handlers
    services/          # business logic (conflict checks, reminders)
    db/                # database connection and queries
    middleware/        # auth guard, validation, error handling
    jobs/              # scheduled jobs (reminder sender)
    app.js
    server.js
  tests/
  .env.example         # e.g. DATABASE_URL, SESSION_SECRET
  package.json
```

See Part B of [`docs/PRD.md`](../docs/PRD.md) for the DRAFT endpoints and data model.
