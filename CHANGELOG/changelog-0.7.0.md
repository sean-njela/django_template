# **0.7.0 - 2025-10-05**

## **Release highlights**

* **Unfold Integration**: Replaced Django’s default admin interface with the modern Unfold admin UI, providing full Tailwind-based styling and better UX consistency.
* **Theme System**: Added dark/light theme support with toggle and custom branding (Sky blue accent, neutral base, rounded borders).
* **Internationalisation (i18n)**: Introduced full multilingual support with English, Polish, and German locales.

---

## **Added**

* Added **Unfold admin UI** (`django-unfold`) for a modern, Tailwind-based Django admin interface.
* Added **Unfold contrib modules** (`filters`, `forms`, `inlines`, `import_export`, `guardian`, `simple_history`, `location_field`, `constance`) for extended admin functionality.
* Added **multi-language support** (`LANGUAGES`, `USE_I18N`, `USE_L10N`, and `i18n_patterns` in URLs).
* Added **language switcher** in admin navigation using `SHOW_LANGUAGES` and `LANGUAGES.navigation`.
* Added **Unfold theming** with configurable `"THEME"`, `"BORDER_RADIUS"`, and `"COLORS"`.
* Added **dark/light theme toggle** (`"THEME": None`, `"THEME_DEFAULT": "dark"`).
* Added **custom admin branding**: site title, header, dropdown links, and login background image.
* Added **crispy-forms integration** with `"unfold_crispy"` template pack for consistent Unfold form styling.
* Added **custom Unfold callbacks** (`dashboard_callback`, `environment_callback`, `badge_callback`, `permission_callback`) in `admin_config.py`.
* Added **Group admin re-registration** using `BaseGroupAdmin` + `ModelAdmin` for Unfold styling.
* Added **dockerised locale generation** with language-specific `.po` files and ignore configuration via `.makemessagesignore`.
* Added **new visual palette** — Sky (#2AA5F4) accent, neutral base (#171717), and light mode base (#FAF7F5).
* Added **theme-friendly font contrast mapping** for light/dark modes.
* Added **custom dashboard and sidebar configuration** with icons, navigation, and tabs.

---

## **Changed**

* Changed **UserAdmin** to inherit from `unfold.admin.ModelAdmin` for Unfold styling.
* Changed **settings base.py** to include Unfold configuration under a single `UNFOLD` dictionary.
* Changed **URL configuration** to use `i18n_patterns` for multilingual routes.
* Changed **form renderer** to `django.forms.renderers.TemplatesSetting` for compatibility with crispy forms.
* Changed **`CRISPY_TEMPLATE_PACK`** to `unfold_crispy` to unify admin form appearance.
* Changed **theme colour structure** to Oklch-neutral palette for readability across modes.
* Changed **login redirection** and images under `UNFOLD["LOGIN"]` for a consistent branded login screen.
* Changed **`SHOW_BACK_BUTTON`** default to `True` to improve admin navigation.

---

## **Deprecated**

* Deprecated using plain `django.contrib.admin.ModelAdmin` in project-admin classes. Use `unfold.admin.ModelAdmin` instead.
* Deprecated direct modification of built-in Django admin templates; all UI customisations should now go through Unfold’s configuration.

---

## **Fixed**

* Fixed inconsistent admin button spacing and fieldset layout caused by mixing default and custom admin templates.
* Fixed broken Allauth admin login redirect when using secure login wrappers (`secure_admin_login`).
* Fixed unstyled Group admin view by re-registering it under Unfold.
* Fixed `makemessages` permission issues inside Docker by documenting non-root execution and `.makemessagesignore` support.

---

## **Security**

* Improved session and CSRF hardening by enforcing `SESSION_COOKIE_HTTPONLY` and `CSRF_COOKIE_HTTPONLY`.
* Improved admin access safety through `DJANGO_ADMIN_FORCE_ALLAUTH`, ensuring login flow passes through Allauth.
* Improved Celery configuration to use Redis SSL (when `rediss://` is detected) for encrypted broker connections.

---

## **Breaking changes**

* Replaced **default Django admin** with Unfold — custom admin templates or CSS relying on default Django styles will no longer work.
* Moved **URL routing** under `i18n_patterns`, changing route prefixes (`/en/`, `/pl/`, `/de/`); bookmarks to old `/admin/` URLs may break.
* Required **Crispy Forms dependency** (`django-crispy-forms`) for form rendering — missing installation will break Unfold admin pages.
* All admin customisations must now subclass `unfold.admin.ModelAdmin` instead of `django.contrib.admin.ModelAdmin`.
* Environment and dashboard callbacks moved to new file `admin_config.py`; any hardcoded dashboard customisations must be migrated.

---

**Authored by:** [@sean-njela](https://github.com/sean-njela)
**Commit range:** `v0.6.9` → `v0.7.0`
