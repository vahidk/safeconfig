import unittest

from safeconfig import Variable


class TestVariableMethods(unittest.TestCase):
    def test_default_value(self):
        variable = Variable(int, description="Test variable", default=5)
        self.assertEqual(variable.default, 5)

    def test_set_get_value(self):
        variable = Variable(float, description="Test variable")
        variable.set(15.0)
        self.assertEqual(variable.get(), 15.0)

    def test_invalid_type(self):
        variable = Variable(int, description="Test variable", default=5)
        with self.assertRaises(ValueError):
            variable.set("invalid")

    def test_optional_variable(self):
        optional_variable = Variable(int, description="Optional variable", optional=True)
        self.assertIsNone(optional_variable.get(), "Default value for an optional variable should be None")
        optional_variable.set(10)
        self.assertEqual(optional_variable.get(), 10, "Optional variable should accept new values")

    def test_required_variable(self):
        required_variable = Variable(int, description="Required variable")
        with self.assertRaises(AttributeError):
            required_variable.get()
        required_variable.set(20)
        self.assertEqual(required_variable.get(), 20, "Required variable should accept new values")


if __name__ == "__main__":
    unittest.main()
