# Copyright (C) 2020-2022  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import copy
import os

import pytest
import yaml

from swh.core.api.serializers import json_dumps, msgpack_dumps, msgpack_loads
from swh.vault.api.serializers import ENCODERS
import swh.vault.api.server
from swh.vault.api.server import app, check_config, make_app_from_configfile
from swh.vault.tests.test_backend import TEST_SWHID


def test_make_app_from_file_missing():
    with pytest.raises(ValueError, match="Missing configuration path."):
        make_app_from_configfile()


def test_make_app_from_file_does_not_exist(tmp_path):
    conf_path = os.path.join(str(tmp_path), "vault-server.yml")
    assert os.path.exists(conf_path) is False

    with pytest.raises(
        ValueError, match=f"Configuration path {conf_path} should exist."
    ):
        make_app_from_configfile(conf_path)


def test_make_app_from_env_variable(swh_vault_config_file):
    """Server initialization happens through env variable when no path is provided

    """
    app = make_app_from_configfile()
    assert app is not None
    assert "vault" in app.config

    # Cleanup app
    del app.config["vault"]
    swh.vault.api.server.vault = None


def test_make_app_from_file(swh_local_vault_config, tmp_path):
    """Server initialization happens through path if provided

    """
    conf_path = os.path.join(str(tmp_path), "vault-server.yml")
    with open(conf_path, "w") as f:
        f.write(yaml.dump(swh_local_vault_config))

    app = make_app_from_configfile(conf_path)
    assert app is not None
    assert "vault" in app.config

    # Cleanup app
    del app.config["vault"]
    swh.vault.api.server.vault = None


@pytest.fixture
def vault_app(swh_local_vault_config):
    # Set app config
    app.config["vault"] = swh_local_vault_config["vault"]

    yield app

    # Cleanup app
    del app.config["vault"]
    swh.vault.api.server.vault = None


@pytest.fixture
def cli(vault_app):
    cli = vault_app.test_client()
    return cli


def test_client_index(cli):
    resp = cli.get("/")
    assert resp.status == "200 OK"


def test_client_cook_notfound(cli):
    resp = cli.post(
        "/cook",
        data=json_dumps(
            {"bundle_type": "flat", "swhid": TEST_SWHID}, extra_encoders=ENCODERS
        ),
        headers=[("Content-Type", "application/json")],
    )
    assert resp.status == "400 BAD REQUEST"
    content = msgpack_loads(resp.data)
    assert content["type"] == "NotFoundExc"
    assert content["args"] == [f"flat {TEST_SWHID} was not found."]


def test_client_progress_notfound(cli):
    resp = cli.post(
        "/progress",
        data=json_dumps(
            {"bundle_type": "flat", "swhid": TEST_SWHID}, extra_encoders=ENCODERS
        ),
        headers=[("Content-Type", "application/json")],
    )
    assert resp.status == "400 BAD REQUEST"
    content = msgpack_loads(resp.data)
    assert content["type"] == "NotFoundExc"
    assert content["args"] == [f"flat {TEST_SWHID} was not found."]


def test_client_batch_cook_invalid_type(cli):
    resp = cli.post(
        "/batch_cook",
        data=msgpack_dumps({"batch": [("foobar", [])]}),
        headers={"Content-Type": "application/x-msgpack"},
    )
    assert resp.status == "400 BAD REQUEST"
    content = msgpack_loads(resp.data)
    assert content["type"] == "NotFoundExc"
    assert content["args"] == ["foobar is an unknown type."]


def test_client_batch_progress_notfound(cli):
    resp = cli.post(
        "/batch_progress",
        data=msgpack_dumps({"batch_id": 1}),
        headers={"Content-Type": "application/x-msgpack"},
    )
    assert resp.status == "400 BAD REQUEST"
    content = msgpack_loads(resp.data)
    assert content["type"] == "NotFoundExc"
    assert content["args"] == ["Batch 1 does not exist."]


def test_check_config_missing_vault_configuration() -> None:
    """Irrelevant configuration file path raises"""
    with pytest.raises(ValueError, match="missing 'vault' configuration"):
        check_config({})


def test_check_config_not_local() -> None:
    """Wrong configuration raises"""
    expected_error = (
        "The vault backend can only be started with a 'local' configuration"
    )
    with pytest.raises(EnvironmentError, match=expected_error):
        check_config({"vault": {"cls": "remote"}})


@pytest.mark.parametrize("missing_key", ["storage", "cache", "scheduler"])
def test_check_config_missing_key(missing_key, swh_vault_config) -> None:
    """Any other configuration than 'local' (the default) is rejected"""
    config_ok = {"vault": {"cls": "local", **swh_vault_config}}
    config_ko = copy.deepcopy(config_ok)
    config_ko["vault"].pop(missing_key, None)

    expected_error = f"invalid configuration: missing {missing_key} config entry"
    with pytest.raises(ValueError, match=expected_error):
        check_config(config_ko)


@pytest.mark.parametrize("missing_key", ["storage", "cache", "scheduler"])
def test_check_config_ok(missing_key, swh_vault_config) -> None:
    """Any other configuration than 'local' (the default) is rejected"""
    config_ok = {"vault": {"cls": "local", **swh_vault_config}}
    assert check_config(config_ok) is not None
