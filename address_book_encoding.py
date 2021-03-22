"""
Custom file encoding and decoding for the module address_book.py

How to run:
    register_codecs()

    with codecs.open(file_path, mode='w', encoding='json') as f:
        f.write('this is a test')
"""

__author__ = 'Bridgette Perrers'
__email__ = 'bperrers@hotmail.com'

import codecs
import json
import yaml
import logging
import lxml.etree
import io

logger = logging.getLogger(__name__)


def write_file(file_path, encoding, obj):
    """
    Encode the given python object, and write it to the given file path,
    using the specified encoding. The file will be created if it does not exist.

    Args:
        file_path (str): expects the path to a file
        encoding (stsr): expects the name of a registered codec
    """

    with open(file_path, mode='w') as f:
        encoded_object = codecs.encode(obj, encoding=encoding)
        f.write(encoded_object)


def read_file(file_path, encoding):
    """
    Decode the contents of the given file, using the specified encoding.

    Args:
        file_path (str): expects the path to an encoded file
        encoding (stsr): expects the name of a registered codec

    Returns:
        decoded_object (object): the decoded file contents
    """

    with open(file_path, mode='r') as f:
        decoded_object = codecs.decode(str(f.read()), encoding=encoding)

    return decoded_object


def register_codecs():
    """
    Register custom codecs.
    """

    codecs.register(json_search)
    logger.info('Registered codec: json')

    codecs.register(yaml_search)
    logger.info('Registered codec: yaml')

    codecs.register(html_table_search)
    logger.info('Registered codec: html_table')

    codecs.register(formatted_text_search)
    logger.info('Registered codec: formatted_text')


def json_encode(obj):
    """
    Encode the given python object as a json string.

    Args:
        obj (object): expects a pythonn object to encode

    Returns (str): the encoded json string
    """

    return (json.dumps(obj), len(obj))


def json_decode(json_string):
    """
    Decode the given json string to a python object.

    Args:
        json_string(str): expects a string of json data

    Returns:
        (object): the decoded python object
    """

    return (json.loads(json_string), len(json_string))


def json_search(encoding):
    """
    If the given encoding string is 'json', return the json codec object,
    otherwise return None.

    Args:
        encoding (str('json')): expects the name of the encoding, json

    Returns:
        (codecs.CodecInfo): the json codec object
    """

    if encoding == 'json':
        return codecs.CodecInfo(json_encode, json_decode, name='json')

    return None


def yaml_encode(obj):
    """
    Encode the given python object as a yaml string.

    Args:
        obj (object): expects a python object to encode
    """

    return (yaml.dump(obj), len(obj))


def yaml_decode(yaml_string):
    """
    Decode the given yaml string to a python object.

    Args:
        yaml_string (str): expects a string of yaml data

    Returns:
        (object): the decoded python object
    """

    return (yaml.safe_load(yaml_string), len(yaml_string))


def yaml_search(encoding):
    """
    If the given encoding string is 'yaml', return the yaml codec object,
    otherwise return None.

    Args:
        encoding (str('yaml')): expects the name of the encoding, yaml

    Returns:
        (codecs.CodecInfo): the yaml codec object
    """

    if encoding == 'yaml':
        return codecs.CodecInfo(yaml_encode, yaml_decode, name='yaml')

    return None


def html_table_encode(contact_details):
    """
    Encode the given contact_details as a html table.

    example: [{'Bridgette Perrers': {
    'address': '1515/22 Dorcas Street, Southbank, 3006', 'phone_number': '0447784777'}}]

    Args:
        contact_details(list[dict{str}]): expects a list of contact details dictionaries

    Returns:
        html_table (str): the given contact details in a html table
    """

    html_table = '''
    <table>
    <style>table, th, td {border: 1px solid black; border-collapse: collapse; padding: 10px}</style>
    <tr><th>Name</th><th>Address</th><th>Phone Number</th></tr>
    '''

    for contact in contact_details:
        for name, value in contact.items():
            address = value.get('address')
            phone_number = value.get('phone_number')
            table_row = '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>'.format(name, address, phone_number)

            html_table += table_row

    html_table += '</table>'

    return (html_table, len(html_table))


def html_table_decode(html_table_str):
    """
    Decode the given html table string to a list of dictionaries.

    Args:
        html_table_str (str): expects a string of formatted text data

    Returns:
        (tuple(contacts (list[dict{str}])), len(contacts): the decoded contact details
    """

    contacts = []

    parser = lxml.etree.HTMLParser()
    tree = lxml.etree.parse(io.StringIO(html_table_str), parser)
    table_rows = tree.findall('.//tr')

    for row in table_rows:
        row_values = row.findall('.//td')

        if not row_values:
            continue

        name = row_values[0].text
        address = row_values[1].text
        phone_number = row_values[2].text

        contact_dict = {name: {'address': address, 'phone_number': phone_number, }}
        contacts.append(contact_dict)

    return (contacts, len(contacts))


def html_table_search(encoding):
    """
    If the given encoding string is 'html_table', return the html_table codec object,
    otherwise return None.

    Args:
        encoding (str('html_table')): expects the name of the encoding, html_table

    Returns:
        (codecs.CodecInfo): the html_table codec object
    """

    if encoding == 'html_table':
        return codecs.CodecInfo(html_table_encode, html_table_decode, name='html_table')


def formatted_text_encode(contact_details):
    """
    Encode the given contact_details as formatted text.

    example: [{'Bridgette Perrers': {
    'address': '1515/22 Dorcas Street, Southbank, 3006', 'phone_number': '0447784777'}}]

    Args:
        contact_details(list[dict{str}]): expects a list of contact details dictionaries

    Returns:
        formatted_text (str): the given contact details as formatted text
    """

    formatted_text = ''

    for contact in contact_details:
        for key, value in contact.items():
            formatted_text += '\n'
            formatted_text += key + '\n'

            for sub_key, sub_value in value.items():
                formatted_text += sub_key + ': ' + sub_value + '\n'

    return (formatted_text, len(formatted_text))


def formatted_text_decode(formatted_text_str):
    """
    Decode the given formatted text string to a list of dictionaries.

    Args:
        formatted_text_str (str): expects a string of formatted text data

    Returns:
        (tuple(contacts (list[dict{str}])), len(contacts): the decoded contact details
    """

    contacts = []
    contact_strings = formatted_text_str.split('\n\n')

    for contact in contact_strings:

        if contact == '':
            continue

        contact_data = contact.split('\n')

        name = contact_data[1]
        address = contact_data[2].split(': ')[-1]
        phone_number = contact_data[3].split(': ')[-1]

        contact_dict = {name: {'address': address, 'phone_number': phone_number, }}

        contacts.append(contact_dict)

    return (contacts, len(contacts))


def formatted_text_search(encoding):
    """
    If the given encoding string is 'formatted_text', return the formatted_text codec object,
    otherwise return None.

    Args:
        encoding (str('formatted_text')): expects the name of the encoding, formatted_text

    Returns:
        (codecs.CodecInfo): the formatted_text codec object
    """

    if encoding == 'formatted_text':
        return codecs.CodecInfo(formatted_text_encode, formatted_text_decode, name='formatted_text')



