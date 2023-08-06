import os
import shutil
from unittest import TestCase

from openmodule.config import override_context, override_settings
from openmodule.utils.package_reader import PackageReader, is_bridged_slave


class PackageUtils(TestCase):
    dir = "/tmp/package_reader"

    def clean_dir(self):
        try:
            shutil.rmtree(self.dir)
        except Exception:
            pass

    def setUp(self) -> None:
        self.clean_dir()
        os.makedirs(self.dir)
        self.reader = PackageReader(self.dir)
        super().setUp()

    def create_service(self, service_dir, revision=1, env=None, yml=None):
        service_dir = "_".join(service_dir.replace("_", "-").rsplit("-", 1))
        service_path = os.path.join(self.dir, service_dir)
        os.makedirs(service_path)

        for file_name, content in dict(yml=yml, revision=revision, env=env).items():

            if content is not None:
                with open(os.path.join(service_path, file_name), "w") as file:
                    file.write(str(content))

    def tearDown(self) -> None:
        super().tearDown()
        self.clean_dir()

class PackageReaderTest(PackageUtils):
    def test_missing_revision(self):
        self.create_service("om-service-eventlog_1", revision=None, env="NAME=om_service_eventlog_1", yml="")
        self.create_service("om-service-eventlog_2", env="NAME=om_service_eventlog_2\n", yml="")

        res = self.reader.load_with_service_prefix("")
        self.assertEqual(1, len(res))
        res = res.get("om_service_eventlog_2")
        self.assertIsNotNone(res)
        self.assertEqual("om_service_eventlog_2", res.env["NAME"])

        self.assertEqual(["om_service_eventlog_2"], self.reader.installed_services(""))

    def test_missing_files(self):
        self.create_service("om-service-eventlog_1", yml="")
        with self.assertLogs() as cm:
            res = self.reader.load_with_service_prefix("")
        self.assertIn("ENV file /tmp/package_reader/om-service-eventlog_1/env does not exist", str(cm.output))
        self.assertEqual(1, len(res))

        self.create_service("om-service-eventlog_2", env="")
        with self.assertLogs() as cm1:
            res = self.reader.load_with_service_prefix("")
        # no log triggered for yml
        self.assertEqual(len(cm.output), len(cm1.output))
        self.assertEqual(2, len(res))

    def test_corrupt_files(self):
        self.create_service("om-service-eventlog_1", env="", yml="a\nb:1")
        with self.assertLogs() as cm:
            self.reader.load_with_service_prefix("")
        self.assertIn("YML file /tmp/package_reader/om-service-eventlog_1/yml could not be read", str(cm.output))

        self.create_service("om-service-eventlog_2", env="=")
        with self.assertLogs() as cm1:
            self.reader.load_with_service_prefix("")
        self.assertIn("Python-dotenv could not parse statement", str(cm1.output))

    def test_prefix(self):
        self.create_service("om-service-eventlog_1", env="")
        self.create_service("hw-compute-nuc_1", env="")
        self.create_service("om-service-stuff_1", env="")


        services = list(self.reader.load_with_service_prefix("om").keys())
        self.assertEqual(2, len(services))
        for x in ["om_service_eventlog_1", "om_service_stuff_1"]:
            self.assertTrue(x in services)
        self.assertEqual(["om_service_eventlog_1"],
                         list(self.reader.load_with_service_prefix("om-service-e").keys()))
        self.assertEqual(["hw_compute_nuc_1"],
                         list(self.reader.load_with_service_prefix("hw").keys()))

    def test_parent(self):
        self.create_service("om-fancy-ass_1", env="PARENT=hw_compute_nuc_1")
        self.create_service("hw-compute-nuc_1", env="")
        self.create_service("om-service-stuff_1", env="")

        res = self.reader.load_with_service_prefix("om", with_parent=True)
        self.assertEqual(2, len(res))
        self.assertIsNone(res["om_service_stuff_1"].parent)
        self.assertIsNotNone(res["om_fancy_ass_1"].parent)

    def test_hw_type(self):
        self.create_service("hw-compute-nuc_1", env='HARDWARE_TYPE=["compute-nuc", "nice-stuff", "stuff-bad"]')
        self.assertEqual(1, len(self.reader.load_with_hardware_type_prefix("compute")))
        self.assertEqual(1, len(self.reader.load_with_hardware_type_prefix("nice")))
        self.assertEqual(1, len(self.reader.load_with_hardware_type_prefix("nice-st")))
        self.assertEqual(0, len(self.reader.load_with_hardware_type_prefix("bad")))

    def test_parent_type(self):
        self.create_service("om-fancy-ass_1", env="PARENT=hw_compute_nuc_1\nPARENT_TYPE=[\"compute-nuc\", \"bad-nuc\"]")
        self.assertEqual(1, len(self.reader.load_with_parent_type_prefix("compute")))
        self.assertEqual(1, len(self.reader.load_with_parent_type_prefix("bad")))
        self.assertEqual(0, len(self.reader.load_with_parent_type_prefix("nuc")))

class BridgedSlaveTest(PackageUtils):
    def test_overwrite(self):
        with override_context(BRIDGED_SLAVE=False):
            self.assertFalse(is_bridged_slave())
        with override_context(BRIDGED_SLAVE=True):
            self.assertTrue(is_bridged_slave())

    def test_master_from_directory(self):
        self.create_service("om_service_bridge_1", env="MASTER=")
        self.assertFalse(is_bridged_slave(self.dir))

    def test_slave_from_directory(self):
        self.create_service("om_service_bridge_1", env="MASTER=10.1.1.1")
        self.assertTrue(is_bridged_slave(self.dir))

    def test_config_fail(self):
        # multiple bridges
        self.create_service("om_service_bridge_1", env="MASTER=", yml="")
        self.create_service("om_service_bridge_2", env="MASTER=1234", yml="")
        self.assertIsNone(is_bridged_slave(self.dir))

        # wrong directory
        self.assertIsNone(is_bridged_slave())

