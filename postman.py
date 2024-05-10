from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from api_caller import ApiCallerThread


class PostmanApp(QMainWindow):
    def __init__(self):
        super(PostmanApp, self).__init__()
        self.setupUi()

        # Link for testing purpose
        self.apiText.setText("https://jsonplaceholder.typicode.com/posts/1")

        self.apiCaller = ApiCallerThread(self)
        self.apiCaller.status.connect(self.statusLabel.setText)
        self.apiCaller.result.connect(self.resultsText.setPlainText)

        self.callApiButton.clicked.connect(self.callApiButton_Clicked)

    def setupUi(self):
        self.setWindowTitle("Postman Clone")
        self.setWindowIcon(QIcon("icon.png"))

        layout = QVBoxLayout()
        self.container = QWidget()

        apiLayout = QHBoxLayout()
        self.apiLabel = QLabel("API:")
        self.apiText = QLineEdit()
        self.callApiButton = QPushButton("Get")

        self.apiText.setMinimumWidth(300)
        self.apiText.setClearButtonEnabled(True)

        apiLayout.addWidget(self.apiLabel)
        apiLayout.addWidget(self.apiText)
        apiLayout.addWidget(self.callApiButton)
        layout.addLayout(apiLayout)

        resultsLayout = QVBoxLayout()
        self.resultsLabel = QLabel("Results")
        self.resultsText = QPlainTextEdit()

        self.resultsText.setReadOnly(True)

        resultsLayout.addWidget(self.resultsLabel)
        resultsLayout.addWidget(self.resultsText)
        layout.addLayout(resultsLayout)

        self.statusbar = self.statusBar()
        self.statusLabel = QLabel("Ready")
        self.statusbar.addWidget(self.statusLabel)

        self.container.setLayout(layout)
        self.setCentralWidget(self.container)

    def callApiButton_Clicked(self):
        self.resultsText.clear()
        api = self.apiText.text()
        if self.apiCaller.isRunning():
            self.apiCaller.terminate()

        self.apiCaller.setUrl(api)
        if self.apiCaller.isValidUrl(api):
            self.apiCaller.start()


if __name__ == "__main__":
    app = QApplication([])
    window = PostmanApp()
    window.show()
    app.exec()
