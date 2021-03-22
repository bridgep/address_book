"""
For this code test, I was tasked with creating a simple address book module that allows users to add new records,
and filter users based on some simple search syntax.

This module supports serialisation in two formats (JSON and Yaml),
and will output a copy of the entire address book in both text and HTML.

I was also asked to focus on extensibility - using the codecs module makes it simple for other developers to add or
remove file formats with little change to the main system itself.


There is a simple command line interface that allows users to add, search and display contact details.
I have also written some simple unit test functions that validate the data output by the address book is correct.
"""