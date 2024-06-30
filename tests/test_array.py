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

    def test_append_value(self):
        self.array.set([1, 2])
        self.array.append(3)
        self.assertEqual(self.array.get(), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
