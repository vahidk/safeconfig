import unittest
from safeconfig import Struct, Variable, Array


class NestedStruct(Struct):
    nested_field1 = Variable(int, description="Nested integer field")
    nested_field2 = Variable(str, description="Nested string field")


class TestStruct(Struct):
    field1 = Variable(int, description="An integer field")
    field2 = Variable(str, description="An string field")
    field3 = Array(int, description="An array of integers")
    nested_struct = NestedStruct(description="A nested struct", optional=True)


class TestStructMethods(unittest.TestCase):
    def setUp(self):
        self.struct = TestStruct(description="Test struct")

    def test_set_get_simple_fields(self):
        self.struct.set({'field1': 10, 'field2': 'test', 'field3': [1, 2, 3]})
        self.assertEqual(self.struct.field1.get(), 10)
        self.assertEqual(self.struct.field2.get(), 'test')
        self.assertEqual(self.struct.field3.get(), [1, 2, 3])

    def test_set_get_nested_fields(self):
        self.struct.set({
            'field1': 10,
            'field2': 'test',
            'field3': [1, 2, 3],
            'nested_struct': {
                'nested_field1': 20,
                'nested_field2': 'nested'
            }
        })
        self.assertEqual(self.struct.nested_struct.nested_field1.get(), 20)
        self.assertEqual(self.struct.nested_struct.nested_field2.get(), 'nested')

    def test_validate_simple_fields(self):
        valid_data = {'field1': 30, 'field2': 'validate', 'field3': [4, 5, 6], 'nested_struct': None}
        self.assertEqual(self.struct.validate(valid_data), valid_data)

    def test_validate_nested_fields(self):
        valid_data = {
            'field1': 30,
            'field2': 'validate',
            'field3': [4, 5, 6],
            'nested_struct': {
                'nested_field1': 40,
                'nested_field2': 'validate_nested'
            }
        }
        self.assertEqual(self.struct.validate(valid_data), valid_data)

    def test_invalid_field_type(self):
        with self.assertRaises(ValueError):
            self.struct.set({'field1': 'invalid', 'field2': 'test', 'field3': [1, 2, 3]})

    def test_missing_required_field(self):
        with self.assertRaises(AttributeError):
            self.struct.set({'field1': 10, 'field2': 'test'})  # Missing 'field3'

    def test_optional_struct(self):
        struct = NestedStruct(description="A nested struct", optional=True)
        self.assertIsNone(struct.get(), "Default value for an optional variable should be None")
        value = {'nested_field1': 50, 'nested_field2': 'nested'}
        struct.set(value)
        self.assertEqual(struct.get(), value, "Optional variable should accept new values")
    
    def test_required_struct(self):
        required_struct = NestedStruct(description="A required nested struct")
        with self.assertRaises(AttributeError):
            required_struct.get()
        value = {'nested_field1': 50, 'nested_field2': 'nested'}
        required_struct.set(value)
        self.assertEqual(required_struct.get(), value, "Required variable should accept new values")

    def test_set_flat(self):
        self.struct.set({
            'field1': 10,
            'field2': 'test',
            'field3': [1, 2, 3],
            'nested_struct': {
                'nested_field1': 20,
                'nested_field2': 'nested'
            }
        })
        self.struct.set_flat('nested_struct.nested_field1', 50)
        self.assertEqual(self.struct.nested_struct.nested_field1.get(), 50)

    def test_get_flat(self):
        self.struct.set({
            'field1': 10,
            'field2': 'test',
            'field3': [1, 2, 3],
            'nested_struct': {
                'nested_field1': 20,
                'nested_field2': 'nested'
            }
        })
        self.assertEqual(self.struct.get_flat('nested_struct.nested_field1').get(), 20)


if __name__ == '__main__':
    unittest.main()
