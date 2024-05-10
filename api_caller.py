from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

import requests
import json
import validators


class ApiCallerThread(QThread):
    """
    A class representing a thread for making API calls.

    This class extends the QThread class from PyQt and provides functionality
    for making API calls in a separate thread.

    Attributes:
        status (pyqtSignal): A signal emitted to indicate the status of the API call.
        result (pyqtSignal): A signal emitted to provide the result of the API call.

    Methods:
        run() -> None: The main method of the thread that performs the API call.
        setUrl(url: str) -> None: Sets the URL for the API call.
        isValidUrl(url: str) -> bool: Checks if a given URL is valid.
    """

    status = pyqtSignal(str)
    result = pyqtSignal(str)

    @pyqtSlot()
    def run(self) -> None:
        """
        The main method of the thread that performs the API call.

        This method is automatically called when the thread is started.
        It makes the API call, processes the response, and emits the
        appropriate signals to indicate the status and result of the call.

        Returns:
            None
        """
        try:
            self.status.emit("Calling API...")

            response = requests.get(self.url)

            result = response.json()

            self.result.emit(json.dumps(result, indent=4))
            self.status.emit("Ready")
        except requests.exceptions.JSONDecodeError as e:
            self.result.emit(f"JSONError: {str(e)}")
            self.status.emit("JSONDecodeError")
        except Exception as e:
            self.result.emit(f"Error: {str(e)}")
            self.status.emit("Error")

    def setUrl(self, url: str) -> None:
        """
        Sets the URL for the API call.

        Args:
            url (str): The URL to be set.

        Returns:
            None
        """
        if not self.isValidUrl(url):
            self.status.emit("Invalid URL")
            return
        self.url = url

    def isValidUrl(self, url: str) -> bool:
        """
        Checks if a given URL is valid.

        Args:
            url (str): The URL to be validated.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        if (not url) or (url is None):
            return False
        if url.isspace():
            return False
        if not validators.url(url):
            return False
        return True
