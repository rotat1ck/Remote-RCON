import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remote RCON 2.0")
        self.setGeometry(100, 100, 750, 500)  # Adjusted window size for better scaling

        # Create a web view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://77.37.246.6:7777/"))  # Replace with your web app URL
        self.setCentralWidget(self.browser)

        # Set the zoom factor to 1.25x
        self.browser.setZoomFactor(1.25)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())