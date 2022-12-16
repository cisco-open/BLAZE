import os
import tempfile
import yaml
import pytest
from aski.flask_servers.app import create_app

data = None
with open("../../yaml/04_summary_custom.yaml", mode="rt", encoding="utf-8") as file:
        data = yaml.safe_load(file)


@pytest.fixture
def app():
    app = create_app(data)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
