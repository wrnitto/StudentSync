# /api — Back-end / REST API

This folder will contain the StudentSync back end: a JSON REST API that handles accounts, courses, tasks/events, conflict detection, and reminders.

**Status (Prototype 1):** placeholder only. No application code yet.

## Planned stack

- Node.js (LTS) + Express
- `pg` (node-postgres) for PostgreSQL access
- `bcrypt` for password hashing
- `express-session` + `connect-pg-simple` for login sessions (HTTP-only cookies)
- `node-cron` for the reminder scheduler
- `nodemailer` for email reminders
- Jest + Supertest for API tests

## Planned layout (created when development starts)

```
api/
  src/
    routes/            # Express routers (auth, courses, items, reminders)
    controllers/       # request handlers
    services/          # business logic (conflict detection, reminders)
    db/                # database connection and queries
    middleware/        # auth guard, validation, error handling
    jobs/              # scheduled jobs (reminder sender)
    app.js
    server.js
  tests/
  .env.example         # DATABASE_URL, SESSION_SECRET, SMTP_* settings
  package.json
```

See [`docs/PRD.md`](../docs/PRD.md) for the planned endpoints and data model.
