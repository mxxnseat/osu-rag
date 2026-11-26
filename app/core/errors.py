class DatabaseError(Exception):
    code = "DATABASE_ERROR"


class DuplicateKeyError(DatabaseError):
    code = "DUPLICATE_KEY"