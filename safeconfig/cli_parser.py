import argparse
import os
from .config import Variable, Array, Struct


class StoreWithFlag(argparse.Action):
    def __init__(self, *args, **kwargs):
        self.seen = False
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        setattr(namespace, f"_set_{self.dest}", True)


class CLIParser:
    """Class to parse command-line arguments and update the configuration accordingly."""

    def __init__(self, config: Struct):
        """
        Initialize the CLI parser with the given configuration.

        Args:
            config (Struct): The configuration struct to be updated with CLI arguments.
        """
        if not isinstance(config, Struct):
            raise ValueError("The configuration must be a Struct.")
        self.config = config
        self.parser = argparse.ArgumentParser(
            config.description, formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        self.parser.add_argument("--config", help="Configuration file.")
        self.parser.add_argument(
            "--print_config", action="store_true", help="Print the configuration file."
        )
        self._add_arguments("", self.config)

    def _add_arguments(self, prefix: str, struct: Struct):
        """
        Recursively add arguments for the struct fields to the argument parser.

        Args:
            prefix (str): The prefix for nested struct fields.
            struct (Struct): The struct whose fields are being added as arguments.
        """
        for name, field in struct._fields.items():
            arg_name = f"--{prefix}{name}"
            if isinstance(field, Struct):
                self._add_arguments(f"{prefix}{name}.", field)
            elif isinstance(field, Array):
                self.parser.add_argument(
                    arg_name,
                    help=field.description,
                    default=field.default,
                    type=field.data_type,
                    nargs="*",
                    action=StoreWithFlag,
                )
            elif isinstance(field, Variable):
                self.parser.add_argument(
                    arg_name,
                    help=field.description,
                    default=field.default,
                    type=field.data_type,
                    action=StoreWithFlag,
                )
            else:
                raise ValueError(f"Unsupported field type {type(field)}")

    def parse_args(self) -> Struct:
        """
        Parse the command-line arguments and update the configuration accordingly.

        Returns:
            Struct: The updated configuration struct.
        """
        # Parse the command line arguments
        namespace = self.parser.parse_args()
        kwargs = vars(namespace)

        # Load the configuration file
        config_path = kwargs.pop("config", None)
        if config_path:
            self.config.read(config_path)

        print_config = kwargs.pop("print_config", None)

        # Override the configuration with command line arguments
        for k, v in kwargs.items():
            if getattr(namespace, f"_set_{k}", False):
                self.config.set_flat(k, v)

        # Print the configuration
        if print_config:
            print(f"Configuration:\n{self.config}")
        return self.config
