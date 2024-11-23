import sys
import os

# Redirect stderr to a file
sys.stderr = open("errors.log", "w")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_visites.settings')

def main():
    """Run administrative tasks."""
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
