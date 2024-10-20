import os
import sys
import dotenv
from django.core.management import execute_from_command_line

def main():
    dotenv.load_dotenv()  # Cargar las variables de entorno
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firebase_django_auth.settings')
    try:
        execute_from_command_line(sys.argv)
    except Exception as exc:
        raise exc

if __name__ == '__main__':
    main()

