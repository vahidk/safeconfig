import unittest

from safeconfig import Array, Variable


class TestArrayMethods(unittest.TestCase):
    def setUp(self):
        self.array = Array(int, description="Test array", default=[1, 2, 3])

    def test_default_value(self):
        self.assertEqual(self.array.default, [1, 2, 3])

    def test_set_get_value(self):
        self.array.set([4, 5, 6])
        self.assertEqual(self.array.get(), [4, 5, 6])

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            self.array.set(["invalid"])

    def test_optional_array(self):
        optional_array = Array(int, description="Optional array", optional=True)
        self.assertIsNone(optional_array.get(), "Default value for an optional array should be None")
        optional_array.set([1, 2, 3])
        self.assertEqual(optional_array.get(), [1, 2, 3], "Optional array should accept new values")

    def test_required_array(self):
        required_array = Array(int, description="Required array")
        with self.assertRaises(AttributeError):
            required_array.get()
        required_array.set([4, 5, 6])
        self.assertEqual(required_array.get(), [4, 5, 6], "Required array should accept new values")

    def test_append_value(self):
        self.array.set([1, 2])
        self.array.append(3)
        self.assertEqual(self.array.get(), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
