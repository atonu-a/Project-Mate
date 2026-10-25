
# Project-Mate (TeamNest)

Project-Mate is a Django web platform that helps people find collaborators for their projects — regardless of field. Instead of assuming everyone is a developer, it's built so developers, designers, marketers, writers, students, and anyone else can post a project, list the skills they need, and find teammates across every discipline.

> Find your team. Build anything.

---

## ✨ Features

- **Profiles with multi-field tagging** — users pick the field(s) they work in and their skills, both stored as proper many-to-many relations (`Field`, `Skill`), not fixed dropdowns.
- **Social-style discover feed** — projects shown with like/comment/save counts, an "All / Following / Recommended" filter, and skill-match–based recommendation sorting.
- **Full-text search** — PostgreSQL `SearchVector`/`SearchRank` across both projects and people, split into project results and people results.
- **Project lifecycle** — create, edit, delete projects with status (`Open`, `In Progress`, `Completed`, `Closed`), compensation type, deadline, required skills, and team size.
- **Join requests** — apply to a project, project owners accept/reject from a dedicated requests inbox; accepted members become `ProjectMember` rows with a role.
- **Team management** — owners can remove members, members can leave, with the owner protected from leaving/removing themselves.
- **Follow system** — follow/unfollow other users, with follower/following counts shown on profiles.
- **Likes, comments, saves** — AJAX-style (`JsonResponse`) endpoints for liking and saving projects and commenting on them.
- **Own profile vs. public profile** — a single `profile` view renders either the editable `profile.html` (if you're viewing yourself) or `public-profile.html` (with Follow / Message / Share actions) for anyone else.
- **Auth flow** — sign up, sign in, sign out, a first-time "complete profile" onboarding step, and a separate edit-profile flow.
- **Image uploads via Cloudinary** — profile pictures, cover photos, and project images are stored on Cloudinary rather than local disk, with a default placeholder avatar/SVG.
- **Landing & About pages** — a public marketing page plus an About page with FAQ.
- **Dark/light theme**, persisted via `localStorage`.
- **Mobile responsive** throughout, including a collapsing two-pane messages view.

---

## 🛠️ Tech Stack

- **Backend:** Django (see `requirements.txt` for the pinned version), PostgreSQL (via `dj-database-url` + `psycopg2-binary`)
- **Media storage:** Cloudinary (`django-cloudinary-storage`) for user-uploaded images
- **Static files:** WhiteNoise (`CompressedStaticFilesStorage`) for serving static assets in production
- **Search:** `django.contrib.postgres.search` (Postgres full-text search — **requires a PostgreSQL database**, won't work on SQLite)
- **Dev tooling:** `django-debug-toolbar`
- **Slugs:** `django-autoslug` for project URLs (`/<slug>/`)
- **Env config:** `python-dotenv` (reads a local `.env` file)
- **Frontend styling:** a hand-written semantic CSS design system (`static/css/style.css` — BEM-style classes, CSS custom-property design tokens, mobile-first responsive rules) **combined with Tailwind in places** (loaded via the Tailwind browser build CDN script in `base.html`) — so not a single consistent styling approach throughout; some templates mix both.
- **Icons:** [Lucide](https://lucide.dev/) and Font Awesome (both loaded)
- **Other front-end libs:** Cropper.js (profile/cover photo cropping)
- **Fonts:** Plus Jakarta Sans (UI), JetBrains Mono (tags/skill pills)
- **Deployment:** configured for Vercel (`vercel.json`, `@vercel/python` builder against `ProjectMate/wsgi.py`), with Gunicorn also available for traditional hosting

---

## 📁 Project Structure

```
Project-Mate/
├── ProjectMate/            # Django project root
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── accounts/                # Users, profiles, auth
│   ├── models.py             # Skill, Field, Profile
│   ├── views.py               # signup, signin, signout, profile, edit_profile, complete_profile
│   ├── forms.py                 # RegistrationForm
│   └── context_processors.py     # profile_context (injected into every template)
├── home/                      # Landing, dashboard, feed, search
│   └── views.py                 # landing_page, discover, home, search_results, about, dashboard, messages, notifications, get_posts()
├── projects/                   # Project CRUD
│   ├── models.py                 # Project, ProjectMember
│   └── views.py                   # project_detail, create_project, edit_project, delete_project, my_projects
├── interactions/                 # Social actions
│   ├── models.py                   # JoinRequest, Follow, Like, Comment, Save
│   └── views.py                     # send_request, join_requests, accept/reject_request, follow, like, save, comment, leave/remove member
├── templates/
│   ├── base.html                     # shared layout: header, sidebar block, {% block main %}, footer
│   ├── landing.html, signup.html, signin.html
│   ├── profile-setup.html, edit-profile.html
│   ├── index.html, discover.html, posts.html (project card partial)
│   ├── create-project.html, edit-project.html, project-detail.html
│   ├── my-projects.html, requests.html, saved.html
│   ├── profile.html, public-profile.html
│   ├── messages.html, notifications.html, search-results.html
│   ├── about.html, about/faq.html
│   └── modals/                        # modal.html, teammate-remove-modal.html
├── static/
│   ├── css/style.css
│   ├── js/app.js, js/modals.js
│   └── images/
├── media/                              # user uploads (local fallback; production uses Cloudinary)
└── requirements.txt
```

---

## 🧩 Data Model (at a glance)

| App | Models | Notes |
|---|---|---|
| `accounts` | `Skill`, `Field`, `Profile` | `Profile` is 1-to-1 with Django's `User`; `skills`/`fields` are M2M |
| `projects` | `Project`, `ProjectMember` | `Project.slug` auto-generated from title via `django-autoslug`; `ProjectMember` links a user to a project with a `role` |
| `interactions` | `JoinRequest`, `Follow`, `Like`, `Comment`, `Save` | all are simple join tables between `User` and either another `User` (`Follow`) or a `Project` |

---

## 🔗 URL Names

For reference when linking with `{% url %}`:

```
home, overview, discover, dashboard, messages, notifications, search_results, about
signup, signin, signout, profile, public_profile, complete_profile, edit_profile
create, my_projects, edit_project, delete_project, project_detail
send_request, requests, follow, leave, remove, save_project, saved, comment, like_project
```

> Note: `profile` and `public_profile` currently point to the same URL pattern and view — the view itself branches internally based on whether the viewer owns the profile.

---

## 🚀 Getting Started

1. Clone the repo and create a virtual environment.
2. `pip install -r requirements.txt`
3. Create a `.env` file in the project root with at least:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=postgres://user:password@localhost:5432/projectmate
   CLOUDINARY_CLOUD_NAME=...
   CLOUDINARY_API_KEY=...
   CLOUDINARY_API_SECRET=...
   ```
   A **PostgreSQL** database is required — search relies on Postgres-specific full-text search and won't work on SQLite.
4. `python manage.py migrate`
5. `python manage.py runserver`

For static files in production: `python manage.py collectstatic` (served via WhiteNoise).

---

## 📱 Responsive Behavior

- Sidebar/dashboard nav collapses into a mobile drawer below 1024px.
- Messages view: one pane at a time on phones (list ↔ conversation, with a back button), two-pane side-by-side from 768px.
- Forms use `font-size: 1rem` inputs to avoid iOS auto-zoom.

---

## ⚠️ Known Issues / In Progress

A handful of backend issues are being worked through — see the project's issue tracker / commit history for current status. Notable areas still being hardened: a couple of interaction endpoints needed stricter `POST`-only enforcement, and one or two template field references didn't match the current model field names.

---

