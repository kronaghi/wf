"""Render the Django index view to a static file for GitHub Pages.

Writes the rendered HTML to docs/index.html (plus docs/.nojekyll) so the
page can be served at https://kronaghi.github.io/wf/. Run locally with
`python scripts/build_static.py`; CI runs the same script on push.
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))  # make the work_force project importable

import django
from django.test import Client
from django.test.utils import override_settings

DOCS = BASE_DIR / "docs"


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "work_force.settings")
    django.setup()

    with override_settings(ALLOWED_HOSTS=["testserver"]):
        response = Client().get("/")
    if response.status_code != 200:
        raise SystemExit(f"index view returned {response.status_code}, expected 200")

    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_bytes(response.content)
    (DOCS / ".nojekyll").touch()  # serve files verbatim, skip Jekyll
    print(f"wrote {DOCS / 'index.html'} ({len(response.content)} bytes)")


if __name__ == "__main__":
    main()
