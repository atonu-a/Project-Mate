
# TeamNest

TeamNest is a web platform that helps people find collaborators for their projects — regardless of field. Unlike typical "find a co-founder" tools that assume everyone is a developer, TeamNest is built for developers, designers, marketers, writers, students, and anyone else who wants to build something with a team.

> Find your team. Build anything.

---

## ✨ Features

- **Multi-field profiles** — users pick the field(s) they work in (Technology, Design, Marketing, Business, Writing, Education, Healthcare, Finance, Student, Other), not just developer tags.
- **Project discovery feed** — a social-style feed of projects looking for collaborators, with likes, comments, and join requests.
- **Create & manage projects** — post a project with required skills, team size, and category.
- **Join requests** — apply to join a project, or review and accept/reject incoming requests.
- **Direct messaging** — a two-pane inbox on desktop that collapses into a list → conversation mobile flow with a back button.
- **Profiles** — includes headline, bio, location, organization, skills, and external links (portfolio, GitHub, LinkedIn), plus follow/message/share actions on other users' profiles.
- **Search** — results split across All Results / Users / Projects tabs.
- **Saved projects** — bookmark projects to revisit later.
- **Notifications** — join request updates, new applicants, etc.
- **Auth flow** — sign up, sign in, first-time profile onboarding, and a separate edit-profile flow.
- **Landing & About pages** — public-facing marketing page plus an About page with a "How It Works" guide, team info, FAQ accordion, and a contact form.
- **Dark/light theme** — toggle persisted via `localStorage`.
- **Fully mobile responsive** — mobile-first CSS throughout, with a slide-out drawer nav, collapsing two-pane chat, and horizontally scrollable tab bars where needed.

---

## 🛠️ Tech Stack

- **Backend templating:** Django templates (`{% extends %}`, `{% block %}`, `{% url %}`, `{% for %}` / `{% empty %}`, `{% if %}`)
- **Styling:** Hand-written semantic CSS (`style.css`) — **no Tailwind, no CSS framework**. Every element has a purpose-named class (`post__title`, `btn-primary`, `chat__sidebar`, etc.) instead of inline utility classes.
- **Icons:** [Lucide](https://lucide.dev/) (`data-lucide="..."` + `lucide.createIcons()`)
- **Fonts:** Plus Jakarta Sans (UI), JetBrains Mono (tags/skill pills)
- **JavaScript:** Vanilla JS (`app.js`) — no framework, no build step

---

## 📁 Project Structure

```

teamnest/
├── style.css              # entire design system — tokens, components, responsive rules
├── js/
│   └── app.js              # all interactivity (vanilla JS, no dependencies)
├── landing.html             # public marketing / "intro" page
├── signup.html               # create account
├── signin.html                # sign in
├── profile-setup.html          # first-time onboarding (after signup)
├── edit-profile.html            # returning-user profile edit
├── index.html                    # dashboard
├── discover.html                  # social feed of projects
├── create-project.html             # post a new project
├── my-projects.html                 # owned + joined projects
├── project-detail.html               # single project view
├── requests.html                      # incoming/outgoing join requests
├── messages.html                       # DM inbox (mobile list↔chat toggle)
├── notifications.html                   # notifications list
├── profile.html                          # logged-in user's own profile
├── (public profile template)              # another user's profile — follow/message/share
├── search-results.html                     # All Results / Users / Projects tabs
├── saved-projects.html                      # bookmarked projects
├── about.html                                # about, how-it-works, FAQ, contact form
└── base.html                                  # shared layout (header + {% block main %} + footer)

```

---

## 🎨 Design System

All visual styling lives in `style.css`, organized into numbered sections:

| # | Section | # | Section |
|---|---|---|---|
| 1 | Design tokens | 13 | My projects |
| 2 | Base / reset | 14 | Notifications |
| 3 | Glass surfaces | 15 | Profile |
| 4 | Page layout | 16 | Project detail |
| 5 | Header | 17 | Join requests |
| 6 | Buttons | 18 | Messages |
| 7 | Mobile drawer | 19 | Toasts |
| 8 | Sidebars | 20 | Motion |
| 9 | Shared bits | 21 | Auth (sign in / sign up) |
| 10 | Dashboard | 22 | Onboarding / edit profile |
| 11 | Feed (discover) | 23 | Spinner |
| 12 | Forms | | |

### Color tokens (CSS custom properties, theme-aware via `.dark`)

```css
--color-primary: #FF5A36;    /* brand orange */
--color-secondary: #7C3AED;  /* purple */
--color-accent: #06B6D4;     /* cyan */
--color-success: #10B981;
--color-warning: #F59E0B;
--color-danger: #EF4444;
```

Light/dark mode is handled entirely by swapping these variables on `<html class="dark">` — toggled via `toggleTheme()` in `app.js` and persisted to `localStorage`.

### Naming convention
BEM-style: `.block`, `.block__element`, `.block--modifier`, `.is-state` (e.g. `.chat__item.is-active`, `.post__join`).

---

## 🚀 Getting Started

1. Clone the repo.
2. Serve the templates through your Django project (`base.html` expects `{% static %}` for images and `{% url %}` for internal links — wire up the corresponding views/URLs).
3. No build step, no `npm install` — `style.css` and `app.js` are plain files, loaded directly:

```html
<link rel="stylesheet" href="style.css">
<script src="https://unpkg.com/lucide@latest"></script>
<script src="js/app.js"></script>
```

---

## 📱 Responsive Behavior

- **< 1024px:** sidebar nav collapses into a hamburger drawer (`toggleMobileMenu()`).
- **< 768px (Messages):** only one pane shown at a time — conversation list by default, tapping a chat opens it full-screen with a back button (`openConversation()` / `closeConversation()`).
- **All forms:** inputs use `font-size: 1rem` to prevent iOS auto-zoom on focus.
- **Tab bars** (search results, feed filters): horizontally scrollable on narrow screens with hidden scrollbars.

---

## 🙋 Who This Is For

| | |
|---|---|
| **Developers** | find a designer/marketer/co-founder |
| **Designers** | partner with developers to ship their work |
| **Marketers & Writers** | join early-stage projects |
| **Students** | get real project experience |

---
