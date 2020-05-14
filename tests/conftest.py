import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def change_settings(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
