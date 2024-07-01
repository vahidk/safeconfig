import argparse
import json
import os
import tempfile
import unittest
from unittest.mock import patch

import yaml

from safeconfig import CLIParser, Struct, Variable, Array


class TestConfigStruct(Struct):
    field1 = Variable(int, description="An integer field")
    field2 = Variable(str, description="A string field")


class TestNestedStruct(Struct):
    nested = Array(TestConfigStruct, description="A nested struct")


class TestCLIParser(unittest.TestCase):
    def setUp(self):
        self.test_json_config = tempfile.NamedTemporaryFile(
            delete=False, suffix=".json", mode="w"
        )
        self.test_yaml_config = tempfile.NamedTemporaryFile(
            delete=False, suffix=".yaml", mode="w"
        )
        self.test_nested_config = tempfile.NamedTemporaryFile(
            delete=False, suffix=".yaml", mode="w"
        )

        json.dump({"field1": 10, "field2": "test"}, self.test_json_config)
        yaml.dump({"field1": 20, "field2": "yaml_test"}, self.test_yaml_config)
        yaml.dump(
            {
                "nested": [
                    {"field1": 30, "field2": "nested_test1"},
                    {"field1": 40, "field2": "nested_test2"},
                ]
            },
            self.test_nested_config,
        )

        self.test_json_config.close()
        self.test_yaml_config.close()

    def tearDown(self):
        os.remove(self.test_json_config.name)
        os.remove(self.test_yaml_config.name)

    @patch("argparse.ArgumentParser.parse_args")
    def test_load_json_config(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            config=self.test_json_config.name
        )

        cli_parser = CLIParser(TestConfigStruct())
        config = cli_parser.parse_args()

        self.assertEqual(config.field1.get(), 10)
        self.assertEqual(config.field2.get(), "test")

    @patch("argparse.ArgumentParser.parse_args")
    def test_load_yaml_config(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            config=self.test_yaml_config.name
        )

        cli_parser = CLIParser(TestConfigStruct())
        config = cli_parser.parse_args()

        self.assertEqual(config.field1.get(), 20)
        self.assertEqual(config.field2.get(), "yaml_test")

    @patch("argparse.ArgumentParser.parse_args")
    def test_override_config(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            config=self.test_json_config.name, field1=30, field2="override"
        )

        cli_parser = CLIParser(TestConfigStruct())
        config = cli_parser.parse_args()

        self.assertEqual(config.field1.get(), 30)
        self.assertEqual(config.field2.get(), "override")
    
    @patch("argparse.ArgumentParser.parse_args")
    def test_load_nested_config(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            config=self.test_nested_config.name
        )

        cli_parser = CLIParser(TestNestedStruct())
        config = cli_parser.parse_args()

        self.assertEqual(config.nested[0].field1.get(), 30)
        self.assertEqual(config.nested[0].field2.get(), "nested_test1")
        self.assertEqual(config.nested[1].field1.get(), 40)
        self.assertEqual(config.nested[1].field2.get(), "nested_test2")


if __name__ == "__main__":
    unittest.main()
