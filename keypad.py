import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, QSize


class PhoneAppClone(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))

        self.setWindowTitle('Keypad')
        self.setWindowIcon(QIcon(os.path.join(base_path, 'images', 'appicon.png')))
        self.setGeometry(1000, 100, 300, 500)  # Increase window height to 500
        self.setFixedSize(300, 500)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setStyleSheet("background-color: #ffffff;")

        main_layout = QGridLayout()
        main_layout.setHorizontalSpacing(21)
        main_layout.setVerticalSpacing(15)

        self.number_label = QLabel('', self)
        font = QFont("SF Pro", 20)
        self.number_label.setFont(font)
        main_layout.addWidget(self.number_label, 0, 0, 1, 3, alignment=Qt.AlignCenter)

        buttons_info = [
            ('1', ' '),
            ('2', 'ABC'),
            ('3', 'DEF'),
            ('4', 'GHI'),
            ('5', 'JKL'),
            ('6', 'MNO'),
            ('7', 'PQRS'),
            ('8', 'TUV'),
            ('9', 'WXYZ'),
            ('*', ''),
            ('0', '+'),
            ('#', ''),
        ]

        self.buttons_dict = {}
        self.current_number = ""
        self.color_timer = QTimer(self)  # Timer for resetting button colors
        self.color_timer.setInterval(100)  # 100 milliseconds (0.1 seconds)
        self.color_timer.timeout.connect(self.reset_button_colors)  # Connect the timeout signal to reset_button_colors

        self.clipboard_timer = QTimer(self) # Timer for showing clipboard icon when copied
        self.clipboard_timer.setInterval(650)
        self.clipboard_timer.timeout.connect(self.update_clipboard_visibility)

        # Create the dictionary to map letter keys to button objects
        self.letter_to_button = {}

        row, col = 1, 0
        for number, letters in buttons_info:
            button = QPushButton('', self)
            button.setFixedSize(80, 80)
            button.setStyleSheet('background-color: #e5e5e5; color: black; border-radius: 40px;')
            button.clicked.connect(self.on_button_click)

            font = QFont("SF Pro", 20)
            number_label = QLabel(number, self)
            number_label.setFont(font)

            font.setPointSize(8)
            letters_label = QLabel(letters, self)
            letters_label.setFont(font)

            button_layout = QGridLayout(button)
            button_layout.addWidget(number_label, 0, 0, alignment=Qt.AlignCenter)

            if letters:
                button_layout.addWidget(letters_label, 1, 0, alignment=Qt.AlignCenter)
                button_layout.setVerticalSpacing(10)
            else:
                button_layout.setVerticalSpacing(10)

            main_layout.addWidget(button, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

            for letter in letters:
                self.buttons_dict[letter] = number
                self.letter_to_button[letter] = button  # Store the button object in the letter_to_button dictionary

        self.setLayout(main_layout)

        # Create the backspace button and set its properties
        self.backspace_button = QPushButton('', self)  # No text on the button
        self.backspace_button.setFixedSize(80, 94)
        # Load icon images
        self.backpsaceicon = QPixmap(os.path.join(base_path, 'images', 'bspace_icon.png'))
        self.backpsaceicon_pressed = QPixmap(os.path.join(base_path, 'images', 'bspace_icon_pressed.png'))
        # Set the icon for the button
        self.backspace_button.setIcon(QIcon(self.backpsaceicon))
        self.backspace_button.setIconSize(QSize(50,50)) #self.backspace_button.size())  # Scale the icon to fit the button size
        self.backspace_button.setStyleSheet('background-color: rgba(2,122,254,0);')
        self.backspace_button.clicked.connect(self.on_backspace_click)
        self.backspace_button.setVisible(False)  # Initially, hide the backspace button
        main_layout.addWidget(self.backspace_button, 0, 2)  # Add the backspace button to the layout       

        # Create the clipboard button and set its properties
        self.clipboard_button = QPushButton('', self)  # No text on the button
        self.clipboard_button.setFixedSize(80, 94)
        # Set the icon for the button
        self.clipboard_button.setIcon(QIcon(QPixmap(os.path.join(base_path, 'images', 'clipboard_icon.png'))))
        self.clipboard_button.setIconSize(QSize(50,50)) #self.clipboard_button.size())  # Scale the icon to fit the button size
        self.clipboard_button.setStyleSheet('background-color: rgba(2,122,254,0);')
        self.clipboard_button.setVisible(False)  # Initially, hide the clipboard button
        main_layout.addWidget(self.clipboard_button, 0, 0)  # Add the clipboard button to the layout       

    def on_button_click(self):
        button = self.sender()
        if button:
            number = button.findChild(QLabel).text()

            # Change the button's background color to #b2b2b2 to indicate that it is pressed
            button.setStyleSheet('background-color: #b2b2b2; color: black; border-radius: 40px;')
            self.color_timer.start()  # Start the timer

            if len(self.current_number) < 6:
                self.current_number += number
                self.update_display()
                self.update_backspace_visibility()

    def reset_button_colors(self):
        # Reset the background color of keypad buttons to normal after the timer expires
        for letter, button in self.letter_to_button.items():
            button.setStyleSheet('background-color: #e5e5e5; color: black; border-radius: 40px;')
            button.repaint()

        # Reset the icon of backspace button to normal after the timer expires
        self.backspace_button.setIcon(QIcon(self.backpsaceicon))

        self.color_timer.stop()

    def on_backspace_click(self):
        self.backspace_button.setIcon(QIcon(self.backpsaceicon_pressed))
        self.color_timer.start()  # Start the timer

        self.current_number = self.current_number[:-1]
        self.update_display()
        self.update_backspace_visibility()

    def keyReleaseEvent(self, event):
        key = event.text().upper()

        if key in self.buttons_dict:
            # Change the button's background color to #b2b2b2 to indicate that it is pressed
            self.letter_to_button[key].setStyleSheet('background-color: #b2b2b2; color: black; border-radius: 40px;')
            self.color_timer.start()  # Start the timer

            if len(self.current_number) < 6:
                number = self.buttons_dict[key]
                self.current_number += number
                self.update_display()
                self.update_backspace_visibility()
        elif key == '\x08':
            self.on_backspace_click()
        elif key == '\x7F':
            self.current_number = ""
            self.update_display()
            self.update_backspace_visibility()
        elif key == '\r':
            if self.current_number:
                clipboard = QApplication.clipboard()
                clipboard.setText(self.current_number)

                # Show clipboard icon to indicate number is copied
                self.update_clipboard_visibility()
                self.clipboard_timer.start()

                self.update_display()
                self.update_backspace_visibility()
        elif key == '\x1B':
            self.close()

    def update_display(self):
        if len(self.current_number) > 4:
            formatted_number = ' '.join(self.current_number[i:i+3] for i in range(0, len(self.current_number), 3))
        else:
            formatted_number = self.current_number
        self.number_label.setText(formatted_number)

    def update_backspace_visibility(self):
        # Show/hide the backspace button based on whether there are numbers on the display or not
        self.backspace_button.setVisible(bool(self.current_number))

    def update_clipboard_visibility(self):
        # Show/hide the clipboard icon
        self.clipboard_button.setVisible(not self.clipboard_button.isVisible())
        self.clipboard_timer.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PhoneAppClone()
    window.show()
    app.exec_()