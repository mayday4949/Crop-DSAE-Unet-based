import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create stacked widget
        self.stack_widget = QStackedWidget()
        self.setCentralWidget(self.stack_widget)

        # Create main page
        main_page = QWidget()
        main_layout = QVBoxLayout()
        main_label = QLabel("Main Page")
        main_button = QPushButton("About")
        main_button.clicked.connect(self.show_about_page)
        main_layout.addWidget(main_label)
        main_layout.addWidget(main_button)
        main_page.setLayout(main_layout)

        # Create about page
        about_page = QWidget()
        about_layout = QVBoxLayout()
        about_label = QLabel("About Page")
        about_layout.addWidget(about_label)
        about_page.setLayout(about_layout)

        # Add pages to stacked widget
        self.stack_widget.addWidget(main_page)
        self.stack_widget.addWidget(about_page)

        # Set current index to main page
        self.stack_widget.setCurrentIndex(0)

    def show_about_page(self):
        # Switch to about page
        self.stack_widget.setCurrentIndex(1)

    def show_main_page(self):
        # Switch to main page
        self.stack_widget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
