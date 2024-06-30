import unittest

from safeconfig import Variable


class TestVariableMethods(unittest.TestCase):
    def setUp(self):
        self.variable = Variable(int, description="Test variable", default=5)

    def test_default_value(self):
        self.assertEqual(self.variable.default, 5)

    def test_set_get_value(self):
        self.variable.set(15)
        self.assertEqual(self.variable.get(), 15)

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            self.variable.set("invalid")


if __name__ == "__main__":
    unittest.main()
