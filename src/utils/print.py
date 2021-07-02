from sys import stdout, stderr


def print_error(error_message: str) -> None:
    """
    Print an error message to stderr.
    :param error_message: The message to write.
    """
    stderr.write(f"{error_message}\n")
    stderr.flush()  # flush the buffer


def print_message(message: str) -> None:
    """
    Print a message to stdout.
    :param message: The message to write.
    """
    stdout.write(f"{message}\n")
    stdout.flush()  # flush the buffer
