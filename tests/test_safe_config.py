# -*- coding: utf-8 -*-
"""Offline checks for shipped configuration.

These tests must not open sockets or contact Redis, a bastion, or any
other external service. Failure messages include a path and a risk
category only.
"""

import importlib
import ipaddress
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import types
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from login_jumper.utils import config  # noqa: E402

IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
SECRET_ASSIGN_RE = re.compile(
    r"(?i)^(?P<key>password|passwd|secret|secret_key|api_key|api_token|"
    r"sentry_id|roll_bar)\s*=\s*(?P<val>\S.*?)\s*$"
)
URL_CREDENTIAL_RE = re.compile(r"://[^/\s:@]+:[^/\s@]+@|https://[A-Za-z0-9]+@")
CODE_MARKERS = (
    "config.",
    "os.getenv",
    "os.environ",
    "blank_to_none",
    "get_config",
    "self.",
)
SKIP_DIRS = {
    ".git",
    "env",
    "build",
    "dist",
    "login_jumper.egg-info",
    "__pycache__",
    "tests",
}
SENSITIVE_ENV_KEYS = {
    "password",
    "host",
    "port",
    "database",
    "jumper_host",
    "jumper_port",
    "sentry_id",
    "roll_bar",
}


def _tracked_text_files():
    output = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=REPO_ROOT
    )
    if isinstance(output, bytes):
        output = output.decode("utf-8")
    for name in output.split("\0"):
        if not name:
            continue
        parts = set(name.split("/"))
        if parts & SKIP_DIRS:
            continue
        path = os.path.join(REPO_ROOT, name)
        if not os.path.isfile(path):
            continue
        yield path


class ConfigSafetyTests(unittest.TestCase):
    def test_shipped_files_have_no_secrets_or_routable_hosts(self):
        for path in _tracked_text_files():
            with open(path, "r") as handle:
                for lineno, line in enumerate(handle, 1):
                    stripped = line.strip()
                    if not stripped or stripped.startswith("#"):
                        continue
                    if URL_CREDENTIAL_RE.search(line):
                        self.fail("%s:%s risk=embedded-url-credential" % (path, lineno))
                    for token in IPV4_RE.findall(line):
                        try:
                            address = ipaddress.ip_address(token)
                        except ValueError:
                            self.fail("%s:%s risk=unparsed-address" % (path, lineno))
                        if not address.is_loopback:
                            self.fail("%s:%s risk=non-loopback-address" % (path, lineno))
                    match = SECRET_ASSIGN_RE.match(stripped)
                    if not match:
                        continue
                    value = match.group("val")
                    if any(marker in value for marker in CODE_MARKERS):
                        continue
                    self.fail("%s:%s risk=non-empty-secret-field" % (path, lineno))

    def test_example_files_match_shipped_defaults(self):
        pairs = (
            ("login_jumper/conf/redis.ini", "login_jumper/conf/redis.ini.example"),
            ("login_jumper/conf/config.ini", "login_jumper/conf/config.ini.example"),
        )
        for left, right in pairs:
            with open(os.path.join(REPO_ROOT, left), "r") as left_file:
                with open(os.path.join(REPO_ROOT, right), "r") as right_file:
                    self.assertEqual(left_file.read(), right_file.read())

    def test_redis_sample_endpoints_are_loopback_and_passwords_blank(self):
        parser = self._parser("login_jumper/conf/redis.ini")
        for section in ("single", "cluster"):
            self.assertEqual(parser.get(section, "password"), "")
        self.assertEqual(parser.get("single", "host"), "127.0.0.1")
        nodes = json.loads(parser.get("cluster", "nodes"))
        self.assertTrue(nodes)
        for node in nodes:
            self.assertTrue(ipaddress.ip_address(node["host"]).is_loopback)

    def test_bastion_sample_is_loopback(self):
        parser = self._parser("login_jumper/conf/config.ini")
        host = parser.get("Server", "jumper_host")
        self.assertTrue(ipaddress.ip_address(host).is_loopback)
        self.assertEqual(parser.get("App", "roll_bar"), "")
        self.assertEqual(parser.get("App", "sentry_id"), "")

    def test_gitignore_blocks_local_secret_files(self):
        ignored = (
            "login_jumper/conf/redis.local.ini",
            "login_jumper/conf/config.local.ini",
            ".env",
        )
        tracked = (
            "login_jumper/conf/redis.ini",
            "login_jumper/conf/config.ini",
            "login_jumper/conf/redis.ini.example",
            "login_jumper/conf/config.ini.example",
        )
        for name in ignored:
            result = subprocess.call(
                ["git", "check-ignore", "-q", name], cwd=REPO_ROOT
            )
            self.assertEqual(result, 0, name)
        for name in tracked:
            result = subprocess.call(
                ["git", "check-ignore", "-q", name], cwd=REPO_ROOT
            )
            self.assertNotEqual(result, 0, name)

    def _parser(self, relative_path):
        import configparser

        parser = configparser.RawConfigParser()
        with open(os.path.join(REPO_ROOT, relative_path), "r") as handle:
            parser.read_file(handle)
        return parser


class ConfigLoadTests(unittest.TestCase):
    def setUp(self):
        self._saved_env = os.environ.copy()
        for key in list(os.environ):
            if key in SENSITIVE_ENV_KEYS or key.startswith("LOGIN_JUMPER_"):
                del os.environ[key]
        self._connect = socket.socket.connect
        self._create_connection = socket.create_connection
        socket.socket.connect = self._refuse_network
        socket.create_connection = self._refuse_network
        self.redis_path = os.path.join(REPO_ROOT, "login_jumper/conf/redis.ini")
        self.config_path = os.path.join(REPO_ROOT, "login_jumper/conf/config.ini")

    def tearDown(self):
        socket.socket.connect = self._connect
        socket.create_connection = self._create_connection
        os.environ.clear()
        os.environ.update(self._saved_env)

    @staticmethod
    def _refuse_network(*_args, **_kwargs):
        raise AssertionError("risk=unexpected-network-call")

    def test_blank_password_becomes_unset(self):
        self.assertIsNone(config.blank_to_none(""))
        self.assertIsNone(config.blank_to_none("   "))
        self.assertIsNone(config.blank_to_none(None))
        self.assertEqual(config.blank_to_none("unit-test-only"), "unit-test-only")

    def test_shipped_redis_and_bastion_resolve_to_loopback_without_password(self):
        host = config.get_config("single", "host", file_path=self.redis_path)
        password = config.get_config("cluster", "password", file_path=self.redis_path)
        bastion = config.get_config("Server", "jumper_host", file_path=self.config_path)
        self.assertTrue(ipaddress.ip_address(host).is_loopback)
        self.assertTrue(ipaddress.ip_address(bastion).is_loopback)
        self.assertEqual(password, "")
        self.assertIsNone(config.blank_to_none(password))

    def test_prefixed_env_overrides_file_and_unprefixed_name(self):
        os.environ["password"] = "unit-test-unprefixed"
        os.environ["LOGIN_JUMPER_CLUSTER_PASSWORD"] = "unit-test-prefixed"
        value = config.get_config("cluster", "password", file_path=self.redis_path)
        self.assertEqual(value, "unit-test-prefixed")

    def test_legacy_env_names_still_apply(self):
        os.environ["jumper_host"] = "127.0.0.1"
        os.environ["jumper_port"] = "2222"
        host = config.get_config("Server", "jumper_host", file_path=self.config_path)
        port = config.get_config("Server", "jumper_port", file_path=self.config_path)
        self.assertEqual(host, "127.0.0.1")
        self.assertEqual(port, "2222")

    def test_local_ini_overrides_example_and_env_overrides_local(self):
        temp_dir = tempfile.mkdtemp(prefix="login-jumper-config-")
        base_path = os.path.join(temp_dir, "redis.ini")
        local_path = os.path.join(temp_dir, "redis.local.ini")
        with open(base_path, "w") as handle:
            handle.write("[single]\nhost = 127.0.0.1\nport = 6379\npassword =\n")
        with open(local_path, "w") as handle:
            handle.write("[single]\nhost = 127.0.0.1\nport = 6390\npassword = unit-test-local\n")
        port = config.get_config("single", "port", file_path=base_path)
        password = config.get_config("single", "password", file_path=base_path)
        self.assertEqual(port, "6390")
        self.assertEqual(password, "unit-test-local")
        os.environ["LOGIN_JUMPER_SINGLE_PASSWORD"] = "unit-test-env"
        overridden = config.get_config("single", "password", file_path=base_path)
        self.assertEqual(overridden, "unit-test-env")
        self.assertTrue(ipaddress.ip_address(
            config.get_config("single", "host", file_path=base_path)
        ).is_loopback)

    def test_redis_handler_uses_loopback_sample_and_does_not_connect(self):
        calls = []

        class RecordingRedis(object):
            def __init__(self, host=None, port=None, db=None, password=None, **kwargs):
                calls.append({
                    "host": host,
                    "port": None if port is None else str(port),
                    "db": None if db is None else str(db),
                    "password": password,
                })

        fake_module = types.ModuleType("redis")
        fake_module.Redis = RecordingRedis
        sys.modules["redis"] = fake_module
        previous = os.getcwd()
        os.chdir(REPO_ROOT)
        try:
            import logging
            import login_jumper.utils.get_logger as get_logger
            get_logger.logger_generate = (
                lambda name="logs/jumper_server.log": logging.getLogger("safe-config-test")
            )
            my_redis = importlib.import_module("login_jumper.utils.my_redis")
            importlib.reload(my_redis)
            my_redis.redis_handler(mode="single")
            my_redis.redis_handler(mode="cluster")
        finally:
            os.chdir(previous)

        self.assertEqual(len(calls), 2)
        single, cluster = calls
        self.assertEqual(single["host"], "127.0.0.1")
        self.assertTrue(ipaddress.ip_address(single["host"]).is_loopback)
        self.assertEqual(single["port"], "6379")
        self.assertEqual(single["db"], "2")
        self.assertIsNone(single["password"])
        self.assertIsNone(cluster["host"])
        self.assertIsNone(cluster["password"])


if __name__ == "__main__":
    unittest.main()
