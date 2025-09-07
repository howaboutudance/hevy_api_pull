"""Tests for app.config module."""

import os

import pytest

from app.config import ENV, settings



@pytest.mark.skipif(os.getenv("ENV", "dev").lower() != "test", reason="Skipping test that requires ENV to be 'test'")
def test_cicd_secrets_in_env():
    """Test that the CI/CD secrets are available in the environment."""
    assert os.getenv("DYNACONF_MONGODB__PASSWORD") is not None, "Expected MONGODB__PASSWORD to be set in environment"
    assert os.getenv("DYNACONF_HEVY_API__KEY") is not None, "Expected HEVY_API__KEY to be set in environment"

@pytest.mark.skipif(os.getenv("ENV", "dev").lower() != "test", reason="Skipping test that requires ENV to be 'test'")
def test_cicd_secrets_on_settings():
    """Test that the CI/CD secrets are available in the settings."""
    # check if there are mongdb and hevy_api on settings
    assert hasattr(settings, "mongodb"), "Expected settings to have attribute 'mongodb'"
    assert hasattr(settings, "hevy_api"), "Expected settings to have attribute 'hevy_api'"

    # check if the env variable set values exist on settings
    assert hasattr(settings.mongodb, "password"), "Expected settings.mongodb to have attribute 'password'"
    assert hasattr(settings.hevy_api, "key"), "Expected settings.heavy_api to have attribute 'key'"

def test_env():
    """Test that the ENV constant matches the os.environ variable."""
    assert ENV == os.getenv("ENV", "dev").upper(), f"Expected ENV to be 'dev', but got '{ENV}'"

def test_settings():
    """Test the configuration settings."""
    expected_env = os.getenv("ENV", "dev").upper()

    # check the settings_files list
    expected_settings_file = [
        "config/default.yaml",
        f"config/{expected_env.lower()}.yaml",
        "config/.secrets.yaml",
    ]
    assert settings.settings_file == expected_settings_file, (
        f"Expected settings_files to be {expected_settings_file}, but got {settings.settings_files}"
    )
