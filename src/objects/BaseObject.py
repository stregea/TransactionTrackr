class BaseObject:
    """
    Abstract class that will be used to construct several different type of objects.
    """

    def __init__(self) -> None:
        pass

    def __repr__(self) -> repr:
        return str(self.to_dictionary())

    def __str__(self) -> str:
        return str(self.to_dictionary())

    def to_list(self) -> list:
        pass

    def to_tuple(self) -> tuple:
        pass

    def to_dictionary(self) -> dict:
        pass

    def insert_to_db(self) -> None:
        pass

    def exists_in_db(self) -> bool:
        pass

    def get_id(self) -> int:
        pass

    def get_type(self) -> str:
        pass
