"""
A module for the creation, storage and retrieval of contact data.
"""

__author__ = 'Bridgette Perrers'
__email__ = 'bperrers@hotmail.com'

import os
import fnmatch
import pprint
import logging
import address_book_encoding

logger = logging.getLogger(__name__)

_DIRECTORY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contacts')


class AddressBookError(Exception):
    """
    Base class for exceptions.
    """
    pass


class AddressBookValueError(AddressBookError):
    """
    For exceptions raised when an object is of an incorrect value.
    """
    pass


def address_book(name, address, phone_number, add=False, search=False,
                 show_txt=False, show_html=False):
    """
    A function for interacting with the AddressBook class.

    Args:
        name (str): expects a contact name
        address (str): expects an address
        phone_number (str): expects a phone number
        add (bool): if True create a new contact with the given details
        search (bool): if True filter existing contacts by the given name string
        show_txt (bool): if True display all contacts in a txt file
        show_html (bool): if True display all contacts in a html file
    """

    try:
        address_book = AddressBook(_DIRECTORY_PATH)

    except AddressBookValueError as e:
        logger.exception(str(e))
        return

    if add:
        address_book.create_contact(name, address, phone_number)
        logger.info('Created new contact: ' + name)

    elif search:
        matching_contacts = address_book.filter_contacts(name)
        matching_contacts = [i.to_dict() for i in matching_contacts]
        logger.info('Found {0} matching contacts'.format(len(matching_contacts)))

        for contact in matching_contacts:
            pprint.pprint(contact, indent=4)

    elif show_txt:
        file_paths = address_book.save_address_book()

        for file_path in file_paths:
            if file_path.endswith('.txt'):
                logger.info('Text file saved: ' + file_path)

                os.startfile(file_path)

    elif show_html:
        file_paths = address_book.save_address_book()

        for file_path in file_paths:
            if file_path.endswith('.html'):
                logger.info('HTML file saved: ' + file_path)

                os.startfile(file_path)


class AddressBook(object):
    def __init__(self, directory):
        """
        Args:
            directory (str): expects a directory path to save contacts to
        """

        self.directory = directory
        self.all_contacts = []

        self.validate_directory()
        self.reload_contacts()

        self._supported_file_formats = {'html_table': '.html', 'formatted_text': '.txt',}
        address_book_encoding.register_codecs()

    @property
    def supported_file_formats(self):
        return self._supported_file_formats

    def validate_directory(self):
        """
        Confirm that the given directory path exists.
        """

        if not os.path.isdir(self.directory):
            raise AddressBookValueError('Provide a valid directory path')

    def reload_contacts(self):
        """
        Get all contact data from json files in the address book directory.
        """

        self.all_contacts = []

        for file_path in os.scandir(self.directory):
            if file_path.is_file() and file_path.name.endswith('json'):
                contact = Contact()
                contact.load_contact_details(file_path)

                self.all_contacts.append(contact)


    def create_contact(self, name, address, phone_number):
        """
        Args:
            name (str): expects a contact name
            address (str): expects an address
            phone_number (str): expects a phone number

        Returns:
            new_contact (address_book.Contact): the new contact object
        """

        new_contact = Contact(name, address, phone_number)
        new_contact.save_contact_details(self.directory)

        self.reload_contacts()

        return new_contact

    def filter_contacts(self, name):
        """
        Filter contacts by name using the given string.
        """
        matches = []
        matching_contacts = []

        for contact in os.scandir(self.directory):
            if fnmatch.fnmatch(contact.name, name.replace(' ', '_') + '.json'):
                matches.append(contact)

        for file_path in matches:
            contact = Contact()
            contact.load_contact_details(file_path)

            matching_contacts.append(contact)

        return matching_contacts

    def to_dict(self):
        """
        Returns:
            (list[dict]): a list of dictionaries containing contact details.
        """
        return [i.to_dict() for i in self.all_contacts]

    def save_address_book(self):
        """
        Export all contact details to a single file in the given directory.

        Returns:
            saved_files (list[str]): the newly created file paths in list form
        """

        saved_files = []

        for encoding, extension in self._supported_file_formats.items():
            file_name = 'address_book' + extension
            file_path = os.path.join(self.directory, file_name)

            address_book_data = self.to_dict()
            address_book_encoding.write_file(file_path, encoding, address_book_data)

            saved_files.append(file_path)

        return saved_files


class Contact(object):
    def __init__(self, name=None, address=None, phone_number=None):
        """
        A class for creating and exporting contact details.

        Args:
            name (str): expects a contact name
            address (str): expects an address
            phone_number (str): expects a phone number
        """

        self._name = name
        self._address = address
        self._phone_number = phone_number

        self._supported_file_formats = {'json': '.json', 'yaml': '.yaml',}
        address_book_encoding.register_codecs()

    @property
    def supported_file_formats(self):
        return self._supported_file_formats

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def phone_number(self):
        return self._phone_number

    def to_dict(self):
        """
        Returns contact details in dictionary form.
        """

        return {
                self._name: {
                        'address': self._address,
                        'phone_number': self._phone_number,
                        }
                }

    def save_contact_details(self, directory):
        """
        Save a dictionary of contact details in the given directory.

        Args:
            directory (str): expects a directory path

        Returns:
            saved_files (list[str]): the newly created file paths in list form
        """
        saved_files = []

        for encoding, extension in self._supported_file_formats.items():

            file_name = self._name.replace(' ', '_') + extension
            file_path = os.path.join(directory, file_name)

            contact_data = self.to_dict()
            address_book_encoding.write_file(file_path, encoding, contact_data)

            saved_files.append(file_path)

        return saved_files


    def load_contact_details(self, file_path):
        """
        Load contact details from the given contact file.

        Args:
            file_path (str): expects the path to a contact file
        """

        file_encoding = ''
        file_name, file_extension = os.path.splitext(file_path)

        for encoding, extension in self._supported_file_formats.items():
            if file_extension == extension:
                file_encoding = encoding

        if not file_encoding:
            message = 'file type {0} is not supported. Supported filetypes are: {1}'
            error_message = message.format(file_extension, self._supported_file_formats)
            raise AddressBookValueError(error_message)

        contact_details = address_book_encoding.read_file(file_path, file_encoding)

        for key, value in contact_details.items():
            self._name = key
            self._address = value.get('address')
            self._phone_number = value.get('phone_number')
