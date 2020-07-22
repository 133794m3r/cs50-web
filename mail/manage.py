#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
\tos.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project3.settings')
\ttry:
\t\tfrom django.core.management import execute_from_command_line
\texcept ImportError as exc:
\t\traise ImportError(
\t\t\t"Couldn't import Django. Are you sure it's installed and "
\t\t\t"available on your PYTHONPATH environment variable? Did you "
\t\t\t"forget to activate a virtual environment?"
\t\t) from exc
\texecute_from_command_line(sys.argv)


if __name__ == '__main__':
\tmain()
