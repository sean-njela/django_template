# 0.8.0 - 2025-10-07

## Release highlights

* Split hybrid monolith: Introduced `shared/`, `api/`, and `web/` apps to implement a 4-layer architecture.
* API routing: Moved API outside `i18n_patterns` and added modular endpoints alongside existing router.
* HTMX demo: Added `/people/` page and row-level partial refresh using the service layer.

## Added

* Add `django_template/apps/shared/` with `apps.py`, `validators.py`, `services/user_service.py`, and `integrations/` scaffold. [local](https://github.com/sean-njela/django_template) [@sean-njela](https://github.com/sean-njela)
* Add `django_template/apps/api/` with `ApiConfig`, `serializers.PublicUserSerializer` (`id`, `email`, `name`), `views.PublicUserViewSet` (read-only), and `urls` registering `public-users/`. [local](https://github.com/sean-njela/django_template) [@sean-njela](https://github.com/sean-njela)
* Add `django_template/apps/web/` with `WebConfig`, `urls`, `views.people`, `views.user_row_partial`, and templates `web/user_list.html` and `htmx_partials/user_row.html`. [local](https://github.com/sean-njela/django_template) [@sean-njela](https://github.com/sean-njela)
* Add URL includes for `apps.web` (inside `i18n_patterns`) and `apps.api` (outside localization). [local](https://github.com/sean-njela/django_template) [@sean-njela](https://github.com/sean-njela)

## Changed

* Update `INSTALLED_APPS` to register `django_template.apps.shared`, `django_template.apps.api`, and `django_template.apps.web`. [local](https://github.com/sean-njela/django_template) [@sean-njela](https://github.com/sean-njela)
* Update `TEMPLATES[0]["DIRS"]` to include `apps/web/templates`; update `STATICFILES_DIRS` to include `apps/web/static`. [local](https://github.com/sean-njela/django_template) [@sean-njela](https://github.com/sean-njela)
* Reorganize `config/urls.py`: keep API outside `i18n_patterns`; include web URLs inside; retain existing admin, users, accounts, and legacy `config.api_router`. [local](https://github.com/sean-njela/django_template) [@sean-njela](https://github.com/sean-njela)

## Deprecated

* De-emphasize placing business logic directly in views; prefer `shared/services/*` for reusable domain operations. (No runtime removal; guidance only.) [local](https://github.com/sean-njela/django_template) [@sean-njela](https://github.com/sean-njela)

## Fixed

* Fix HTMX partial rendering path: render `"htmx_partials/user_row.html"` to enable row refresh. [local](https://github.com/sean-njela/django_template) [@sean-njela](https://github.com/sean-njela)
* Ensure HTMX script inclusion on `user_list.html` for client-side triggers. [local](https://github.com/sean-njela/django_template) [@sean-njela](https://github.com/sean-njela)

## Security

* Improve API exposure clarity by removing localization prefixes from API routes, reducing misrouting risk and ambiguous endpoints. (No auth model changes; DRF default auth and permissions remain.) [local](https://github.com/sean-njela/django_template) [@sean-njela](https://github.com/sean-njela)

## Breaking changes

* None at the database or settings level. Avoid defining multiple home routes: if `apps/web` later defines `""`, remove the existing `TemplateView` home to prevent route/name conflicts. [local](https://github.com/sean-njela/django_template) [@sean-njela](https://github.com/sean-njela)
