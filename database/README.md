# /database — Schema, migrations, and seed data

This folder will hold everything needed to create and populate the StudentSync database (proposed: PostgreSQL).

**Status (Prototype 1):** placeholder only. No schema or migrations yet.

## Layout

```
database/
  migrations/          # numbered SQL migration files, applied in order
  seeds/               # sample data for local development and demos
  README.md
```

## Conventions

- Migrations are plain SQL files named `NNN_short_description.sql` (for example, `001_create_users.sql`).
- Never edit a migration that has already been merged to `main`. Add a new migration instead.
- Seed files contain fake data only. Never commit real student information.
- Local database files and dumps are ignored by `.gitignore`.

The DRAFT data model (users, courses, items, reminders) is in [`docs/PRD.md`](../docs/PRD.md#b4-draft-data-model-proposed).
