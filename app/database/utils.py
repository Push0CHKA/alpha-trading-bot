import re
from os import getenv

REGULAR_COMP = re.compile(r"((?<=[a-z\d])[A-Z]|(?!^)[A-Z](?=[a-z]))")


def camel_to_snake(camel_string):
    return REGULAR_COMP.sub(r"_\1", camel_string).lower()


def get_db_url() -> str:
    return (
        f"postgresql+asyncpg://"
        f"{getenv('DB_USER')}:"
        f"{getenv('DB_PASS')}@"
        f"{getenv('DB_HOST')}:"
        f"{getenv('DB_PORT')}/"
        f"{getenv('DB_NAME')}"
    )
