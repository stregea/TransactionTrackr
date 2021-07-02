import threading


class Thread(threading.Thread):
    """
    This class will be used to spawn a daemon thread.
    """

    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.setDaemon(daemonic=True)  # set as a Daemon thread.
        self.running = True

    def run(self) -> None:
        pass

    def stop(self) -> None:
        self.running = False
