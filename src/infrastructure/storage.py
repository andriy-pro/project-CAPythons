import pickle
from typing import Dict
from app.entities import Record
from app.interfaces import StorageInterface
import uuid


# Це "заплатка", яка була потрібна для того, щоб 'pickle' працював без помилок, якщо викликається з модуля.
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "__main__":
            module = "app.entities"
        elif module.startswith("src."):
            module = module[4:]
        return super().find_class(module, name)


class FileStorage(StorageInterface):
    """Class for saving and loading contacts to and from a file."""

    def __init__(self, filename: str = "addressbook.pkl"):
        self.filename = filename

    def save_contacts(self, contacts: Dict[uuid.UUID, Record]) -> None:
        """Save contacts to a file.

        Parameters
        ----------
        contacts : Dict[uuid.UUID, Record]
            A dictionary of contacts to save.
        """
        with open(self.filename, "wb") as f:
            pickle.dump(contacts, f)

    def load_contacts(self) -> Dict[uuid.UUID, Record]:
        """Load contacts from a file.

        Returns
        -------
        Dict[uuid.UUID, Record]
            A dictionary of loaded contacts.

        Raises
        ------
        FileNotFoundError
            If the file is not found.
        """
        try:
            with open(self.filename, "rb") as f:
                return CustomUnpickler(f).load()
        except FileNotFoundError:
            return {}
