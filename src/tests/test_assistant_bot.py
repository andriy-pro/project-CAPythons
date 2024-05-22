import unittest

import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.assistant_bot import AddressBook, Record


class TestAddressBook(unittest.TestCase):

    def setUp(self):
        """Set up the initial records for testing."""
        self.book = AddressBook()

        self.john_record = Record("John")
        self.john_record.add_phone("1234567890")
        self.john_record.add_phone("5555555555")
        self.book.add_record(self.john_record)

        self.jane_record = Record("Jane")
        self.jane_record.add_phone("9876543210")
        self.book.add_record(self.jane_record)

    def test_add_record(self):
        """Test adding a new record to the address book."""
        new_record = Record("Alice")
        new_record.add_phone("1112223333")
        self.book.add_record(new_record)
        self.assertIn("Alice", self.book.data)

    def test_delete_record(self):
        """Test removing a record from the address book."""
        self.book.delete("Jane")
        self.assertNotIn("Jane", self.book.data)
        with self.assertRaises(KeyError):
            self.book.delete("Jane")

    def test_find_record(self):
        """Test searching for a record in the address book."""
        john = self.book.find("John")
        self.assertEqual(john.name.value, "John")
        non_existent = self.book.find("NonExistent")
        self.assertIsNone(non_existent)

    def test_edit_phone(self):
        """Test editing a phone number in a record."""
        self.john_record.edit_phone("1234567890", "5554444666")
        self.assertIn("5554444666", [phone.value for phone in self.john_record.phones])
        self.assertNotIn(
            "1234567890", [phone.value for phone in self.john_record.phones]
        )

    def test_find_phone(self):
        """Test finding a phone number in a record."""
        found_phone = self.john_record.find_phone("5555555555")
        self.assertIsNotNone(found_phone)
        self.assertEqual(found_phone.value, "5555555555")
        not_found_phone = self.john_record.find_phone("0000000000")
        self.assertIsNone(not_found_phone)

    def test_str(self):
        """Test the string representation of the address book."""
        output = str(self.book)
        self.assertIn("John", output)
        self.assertIn("Jane", output)
        self.assertIn("5555555555", output)
        self.assertIn("9876543210", output)

    def test_add_phone(self):
        """Test adding a phone number to a record."""
        self.jane_record.add_phone("2233445566")
        self.assertIn("2233445566", [phone.value for phone in self.jane_record.phones])

    def test_remove_phone(self):
        """Test removing a phone number from a record."""
        self.john_record.remove_phone("1234567890")
        self.assertNotIn(
            "1234567890", [phone.value for phone in self.john_record.phones]
        )


if __name__ == "__main__":
    unittest.main()
