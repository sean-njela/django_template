# v0.8.0 — Split Hybrid Monolith

* New interface layer for web and API.
* New service layer for reusable domain logic.
* URLs reorganized. API routes no longer localized.
* Basic user list page with HTMX partial refresh.
* Public read-only users API.

## Breaking changes

* None at the database level.
* If you previously routed `/` from app code, ensure only one home route exists (see URLs).

## Migration guide

1. Install as usual. No schema changes.
2. Verify settings and URLs edits below.
3. Run checks:

   ```
   python manage.py check
   python manage.py runserver
   ```
4. Test:

   * Web: `/{lang}/people/`
   * API: `/api/public-users/` (auth required)

## Added

### New apps

```
django_template/apps/
├── shared/
│   ├── apps.py
│   ├── models.py                  # placeholder
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── integrations/              # placeholder
│   └── validators.py
├── api/
│   ├── apps.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
└── web/
    ├── apps.py
    ├── urls.py
    ├── views.py
    ├── static/                    # app static root
    └── templates/
        ├── web/
        │   └── user_list.html
        └── htmx_partials/
            └── user_row.html
```

### Service layer

`shared/services/user_service.py`

```python
from django.contrib.auth import get_user_model
User = get_user_model()

def list_users():
    return User.objects.all().only("id", "email", "name").order_by("id")

def get_user(pk: int):
    return User.objects.only("id", "email", "name").get(pk=pk)
```

### API

* `api/serializers.py` exposes `id`, `email`, `name`.
* `api/views.py` adds `PublicUserViewSet` (read-only, authenticated).
* `api/urls.py` registers `public-users/`.

### Web

* `web/urls.py`:

  * `people/` → users table.
  * `htmx/user-row/<int:pk>/` → row refresh partial.
* `web/views.py` renders list and partial using the service layer.
* `web/templates/web/user_list.html` includes HTMX and a refresh button per row.
* `web/templates/htmx_partials/user_row.html` updates a single row.

## Changed

### Settings (`config/settings/base.py`)

* `INSTALLED_APPS`:

  ```python
  LOCAL_APPS = [
      "django_template.users",
      "django_template.apps.shared",
      "django_template.apps.api",
      "django_template.apps.web",
  ]
  ```
* Templates dirs:

  ```python
  TEMPLATES[0]["DIRS"] = [
      str(APPS_DIR / "templates"),
      str(APPS_DIR / "apps" / "web" / "templates"),
  ]
  ```
* Static dirs:

  ```python
  STATICFILES_DIRS = [
      str(APPS_DIR / "static"),
      str(APPS_DIR / "apps" / "web" / "static"),
  ]
  ```

### URLs (`config/urls.py`)

* Keep API outside `i18n_patterns`. Add web include inside.

  ```python
  # i18n block
  urlpatterns += i18n_patterns(
      path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
      path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
      path(settings.ADMIN_URL, admin.site.urls),
      path("users/", include("django_template.users.urls", namespace="users")),
      path("accounts/", include("allauth.urls")),
      path("", include("django_template.apps.web.urls")),
      *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
  )

  # API (no locale)
  urlpatterns += [
      path("api/", include("config.api_router")),                 # existing users router
      path("api/", include("django_template.apps.api.urls")),     # new API endpoints
      path("api/auth-token/", obtain_auth_token, name="obtain_auth_token"),
      path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
      path("api/docs/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
  ]
  ```

### HTMX partial path

* `web/views.py` renders:

  ```python
  return render(request, "htmx_partials/user_row.html", {"u": u})
  ```

## Fixed

* None.

## Removed

* None.

## Verification steps

1. Create two users. Ensure at least one has `name` set.
2. Visit `/{lang}/people/`. Confirm table renders with `id`, `email`, `name`.
3. Click “Refresh row”. Network should show `GET /{lang}/htmx/user-row/<id>/ 200`. The row updates with a timestamp.
4. Call `/api/public-users/` with an authenticated session or token. Expect JSON:

   ```json
   [{"id":1,"email":"x@example.com","name":"X"}]
   ```

## Notes

* `config/api_router.py` remains as the legacy router. New endpoints live in `apps/api/urls.py`. Paths must be unique (`users/` vs `public-users/`).
* Keep only one home route. If you later move home into `apps/web`, remove the `TemplateView` line.

## Ops

* No env var changes.
* No Celery changes.
* Collect static as usual in production.

## Known issues

* If HTMX does not trigger, ensure the script is loaded:

  ```html
  <script src="{% static 'unfold/js/htmx/htmx.js' %}"></script>
  ```
* If the table never updates, confirm the partial template path and 200 response.

## Files touched (concise)

* New: `django_template/apps/{shared,api,web}/**` as listed.
* Edited: `config/settings/base.py`, `config/urls.py`.

Hit:

Web list: [http://localhost:8000/en/people/](http://localhost:8000/en/people/)

API list: [http://localhost:8000/api/public-users/](http://localhost:8000/api/public-users/)