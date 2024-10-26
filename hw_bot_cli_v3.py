from collections import UserDict
import re
from typing import List, Optional


class Field:
    """
    Base class for fields in a contact record.

    Attributes:
        value (str): The value of the field.
    """

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """
    Class for storing a contact's name. This field is required.
    """

    pass


class Phone(Field):
    """
    Class for storing a contact's phone number with validation.

    Attributes:
        value (str): The phone number, validated to ensure 10 digits.
    """

    def __init__(self, value: str):
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Record:
    """
    Class for managing a contact's details, including their name and phone numbers.

    Attributes:
        name (Name): The contact's name.
        phones (List[Phone]): List of phone numbers associated with the contact.
    """

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []

    def add_phone(self, phone: str) -> str:
        """
        Adds a new phone number to the contact.

        Args:
            phone (str): The phone number to add.

        Returns:
            str: Confirmation message.
        """
        new_phone = Phone(phone)
        self.phones.append(new_phone)
        return f"Phone {phone} added to {self.name}."

    def remove_phone(self, phone: str) -> str:
        """
        Removes a phone number from the contact if it exists.

        Args:
            phone (str): The phone number to remove.

        Returns:
            str: Confirmation message if phone was removed or an error message if not found.
        """
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return f"Phone {phone} removed from {self.name}."
        return "Phone number not found."

    def edit_phone(self, old_phone: str, new_phone: str) -> str:
        """
        Edits an existing phone number, replacing it with a new one.

        Args:
            old_phone (str): The phone number to replace.
            new_phone (str): The new phone number.

        Returns:
            str: Confirmation message if phone was updated or an error message if not found.
        """
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return f"Phone {old_phone} updated to {new_phone} for {self.name}."
        return "Old phone number not found."

    def find_phone(self, phone: str) -> Optional[Phone]:
        """
        Finds and returns a phone number if it exists in the contact.

        Args:
            phone (str): The phone number to search for.

        Returns:
            Optional[Phone]: The found phone number or None if not found.
        """
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        phones_str = "; ".join([str(phone) for phone in self.phones])
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    """
    Class for managing a collection of contact records.

    Methods:
        add_record(record): Adds a new contact record.
        find(name): Finds a contact record by name.
        delete(name): Deletes a contact record by name.
    """

    def add_record(self, record: Record) -> str:
        """
        Adds a new record to the address book.

        Args:
            record (Record): The contact record to add.

        Returns:
            str: Confirmation message.
        """
        self.data[record.name.value] = record
        return f"Contact {record.name.value} added to the address book."

    def find(self, name: str) -> Optional[Record]:
        """
        Finds a contact record by name.

        Args:
            name (str): The name of the contact.

        Returns:
            Optional[Record]: The found contact record or None if not found.
        """
        return self.data.get(name)

    def delete(self, name: str) -> str:
        """
        Deletes a contact record by name.

        Args:
            name (str): The name of the contact to delete.

        Returns:
            str: Confirmation message if contact was deleted or an error message if not found.
        """
        if name in self.data:
            del self.data[name]
            return f"Contact {name} has been deleted."
        return "Contact not found."

    def __str__(self) -> str:
        """
        Returns a string representation of all contacts in the address book.
        """
        return "\n".join([str(record) for record in self.data.values()])


# Example usage
if __name__ == "__main__":
    # Creating a new address book
    book = AddressBook()

    # Adding records for John and Jane
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Displaying all records in the address book
    print("All contacts:")
    print(book)

    # Editing John's phone number
    john = book.find("John")
    if john:
        print(john.edit_phone("1234567890", "1112223333"))
        print(john)

    # Finding a specific phone number for John
    found_phone = john.find_phone("5555555555") if john else None
    print(f"Found phone for John: {found_phone.value if found_phone else 'Not found'}")

    # Deleting Jane's record and displaying all records again
    print(book.delete("Jane"))
    print("\nAll contacts after deleting Jane:")
    print(book)
