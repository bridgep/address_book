"""
A command line interface for the module address_book.py

How to run:

python address_book_command.py -name "Bridgette Perrers" -address "1917/22 Dorcas Street, Southbank, 3006" -phone_number "0447784777" -add
"""

__author__ = 'Bridgette Perrers'
__email__ = 'bperrers@hotmail.com'

import argparse
import address_book


def address_book_command():
    """
    A command line interface for interacting with the address_book module
    via the terminal.
    """

    parser = argparse.ArgumentParser(prog='Address Book',
                                     description='an application for storing and retrieving contact information')

    parser.add_argument('-name', type=str, help='expects a contact name enclosed in double quotes', nargs='?')
    parser.add_argument('-address', type=str, help='expects an address enclosed in double quotes', nargs='?')
    parser.add_argument('-phone_number', type=str, help='expects a phone number enclosed in double quotes', nargs='?')

    argument_group = parser.add_mutually_exclusive_group(required=True)

    argument_group.add_argument('-add', help='add a new contact to the address book', action='store_true',
                                default=False)
    argument_group.add_argument('-search', help='filter contacts by name', action='store_true', default=False)
    argument_group.add_argument('-show_txt', help='', action='store_true', default=False)
    argument_group.add_argument('-show_html', help='', action='store_true', default=False)

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = address_book_command()

    name = args.name
    address = args.address
    phone_number = args.phone_number

    add = args.add
    search = args.search
    show_txt = args.show_txt
    show_html = args.show_html

    address_book.address_book(name, address, phone_number, add, search, show_txt, show_html)
