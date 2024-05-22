import unittest
import sys
import os

# Додавання теки src до sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app.entities import AddressBook, Record, Name, Phone

class TestAddressBook(unittest.TestCase):

    def setUp(self):
        """Set up the initial records for testing."""
        self.book = AddressBook()

        self.john_record = Record(Name("John"))
        self.john_record.add_phone(Phone("1234567890"))
        self.john_record.add_phone(Phone("5555555555"))
        self.book.add_record(self.john_record)

        self.jane_record = Record(Name("Jane"))
        self.jane_record.add_phone(Phone("9876543210"))
        self.book.add_record(self.jane_record)

    def test_add_record(self):
        """Test adding a new record to the address book."""
        new_record = Record(Name("Alice"))
        new_record.add_phone(Phone("1112223333"))
        self.book.add_record(new_record)
        self.assertTrue(any(record.name.value == "Alice" for record in self.book.data.values()))

    def test_delete_record(self):
        """Test removing a record from the address book."""
        jane_record_id = next(record.id for record in self.book.data.values() if record.name.value == "Jane")
        self.book.delete(jane_record_id)
        self.assertFalse(any(record.name.value == "Jane" for record in self.book.data.values()))
        with self.assertRaises(KeyError):
            self.book.delete(jane_record_id)

    def test_find_record(self):
        """Test searching for a record in the address book."""
        john = self.book.find_by_name(Name("John"))
        self.assertEqual(john.name.value, "John")
        non_existent = self.book.find_by_name(Name("NonExistent"))
        self.assertIsNone(non_existent)

    def test_edit_phone(self):
        """Test editing a phone number in a record."""
        self.john_record.edit_phone(Phone("1234567890"), Phone("5554444666"))
        self.assertIn("5554444666", [phone.value for phone in self.john_record.phones])
        self.assertNotIn(
            "1234567890", [phone.value for phone in self.john_record.phones]
        )

    def test_str(self):
        """Test the string representation of the address book."""
        output = str(self.book)
        self.assertIn("John", output)
        self.assertIn("Jane", output)
        self.assertIn("5555555555", output)
        self.assertIn("9876543210", output)

    def test_add_phone(self):
        """Test adding a phone number to a record."""
        self.jane_record.add_phone(Phone("2233445566"))
        self.assertIn("2233445566", [phone.value for phone in self.jane_record.phones])

    def test_remove_phone(self):
        """Test removing a phone number from a record."""
        self.john_record.remove_phone(Phone("1234567890"))
        self.assertNotIn(
            "1234567890", [phone.value for phone in self.john_record.phones]
        )

if __name__ == "__main__":
    unittest.main()
