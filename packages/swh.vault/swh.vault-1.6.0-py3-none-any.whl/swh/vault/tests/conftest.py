# Copyright (C) 2020  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from functools import partial
import os
from typing import Any, Dict

import pkg_resources.extern.packaging.version
import pytest
from pytest_postgresql import factories
import yaml

from swh.core.db.pytest_plugin import initialize_database_for_module, postgresql_fact
from swh.storage.postgresql.db import Db as StorageDb
from swh.vault import get_vault
from swh.vault.backend import VaultBackend

os.environ["LC_ALL"] = "C.UTF-8"

# needed for directory tests on git-cloned repositories
# 022 is usually the default value, but some environments (eg. Debian builds) have
# a different one.
os.umask(0o022)

pytest_v = pkg_resources.get_distribution("pytest").parsed_version
if pytest_v < pkg_resources.extern.packaging.version.parse("3.9"):

    @pytest.fixture
    def tmp_path():
        import pathlib
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            yield pathlib.Path(tmpdir)


storage_postgresql_proc = factories.postgresql_proc(
    dbname="storage",
    load=[
        partial(initialize_database_for_module, "storage", StorageDb.current_version)
    ],
)

vault_postgresql_proc = factories.postgresql_proc(
    dbname="vault",
    load=[
        partial(initialize_database_for_module, "vault", VaultBackend.current_version)
    ],
)

postgres_vault = postgresql_fact("vault_postgresql_proc")
postgres_storage = postgresql_fact(
    "storage_postgresql_proc", no_db_drop=True,  # keep the db for performance reasons
)


@pytest.fixture
def swh_vault_config(postgres_vault, postgres_storage, tmp_path) -> Dict[str, Any]:
    tmp_path = str(tmp_path)
    return {
        "db": postgres_vault.dsn,
        "storage": {
            "cls": "postgresql",
            "db": postgres_storage.dsn,
            "objstorage": {
                "cls": "pathslicing",
                "args": {"root": tmp_path, "slicing": "0:1/1:5",},
            },
        },
        "cache": {
            "cls": "pathslicing",
            "args": {"root": tmp_path, "slicing": "0:1/1:5", "allow_delete": True},
        },
        "scheduler": {"cls": "remote", "url": "http://swh-scheduler:5008",},
    }


@pytest.fixture
def swh_local_vault_config(swh_vault_config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vault": {"cls": "local", **swh_vault_config},
        "client_max_size": 1024 ** 3,
    }


@pytest.fixture
def swh_vault_config_file(swh_local_vault_config, monkeypatch, tmp_path):
    conf_path = os.path.join(str(tmp_path), "vault-server.yml")
    with open(conf_path, "w") as f:
        f.write(yaml.dump(swh_local_vault_config))
    monkeypatch.setenv("SWH_CONFIG_FILENAME", conf_path)
    return conf_path


@pytest.fixture
def swh_vault(swh_vault_config):
    return get_vault("local", **swh_vault_config)


@pytest.fixture
def swh_storage(swh_vault):
    return swh_vault.storage
