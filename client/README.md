# /client — Front-end application

This folder will contain the StudentSync front end: a mobile-first single-page web app.

**Status (Prototype 1):** placeholder only. No application code yet.

## Planned stack

- React + Vite (JavaScript)
- React Router for page routing
- FullCalendar (React) for weekly and monthly calendar views
- Plain CSS with CSS variables (mobile-first breakpoints)
- Vitest + React Testing Library for component tests

## Planned layout (created when development starts)

```
client/
  public/              # static assets (icons, manifest)
  src/
    api/               # functions that call the /api back end
    components/        # reusable UI components
    pages/             # one component per screen
    hooks/             # shared React hooks
    styles/            # global CSS and variables
    App.jsx
    main.jsx
  .env.example         # e.g. VITE_API_URL=http://localhost:4000
  package.json
```

See [`docs/PRD.md`](../docs/PRD.md) for the technical architecture and [`docs/TASKS.md`](../docs/TASKS.md) for the work planned for this folder.
