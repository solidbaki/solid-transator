from googletrans import Translator
from datetime import date
import sys
import os.path
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel, QWidget
from PyQt5.QtCore import pyqtSlot, Qt, QSize
import re

class EMailWindow(QWidget):
    def __init__(self):
        QMainWindow.__init__(self)
        self.title = 'E-mail Sender'
        self.width = 400
        self.height = 100
        self.initUI()
        #self.center
    
    def initUI(self):
        self.line = QLineEdit(self)
        self.button = QPushButton('Send Me!', self)

        self.line.move(50, 20)
        self.line.resize(200, 20)

        self.button.move(270,19)
        self.button.resize(100, 22)

        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('E-mail Sender')
        self.button.clicked.connect(self.on_click_mailbutton)
        self.show()
    
    def closeEvent(self, event):
        window.show()
    
    @pyqtSlot()
    def on_click_mailbutton(self):
        email = ""
        if email_is_valid(self.line.text()) is True:
            email = str(self.line.text())
            #Sending email to the address
            print(email)
        else:
            pass


class Window(QMainWindow):
    __instance = None
    @staticmethod 
    def get_instance():
        """ Accessor method """
        if Window.__instance == None:
            Window()
        return Window.__instance
         
    def __init__(self):
        """ Virtually private constructor. """
        if Window.__instance is not None:
            raise GuiAlreadyExistsException()
        else:
            super().__init__()
            self.title = 'Translator - Word List'
            self.left = 10
            self.top = 10
            self.width = 400
            self.height = 100
            self.initUI()
    def initUI(self):
        self.button = QPushButton('Translate', self)
        self.line = QLineEdit(self)
        self.label = QLabel(self)
        self.mail_button = QPushButton('!', self)
        
        self.label.move(50,50)
        self.label.setStyleSheet("font: 8pt")
        
        self.button.move(250,19)
        self.button.resize(100,22)
        
        self.mail_button.move(350,19)
        self.mail_button.resize(20,22)
        self.mail_button.setStyleSheet("background-color: blue")
        self.mail_button.setToolTip('Click this button for sending your list to your e-mail address')
        
        self.line.move(50, 20)
        self.line.resize(200, 20)
        self.line.returnPressed.connect(self.on_pressed)

        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.button.clicked.connect(self.on_click)
        self.mail_button.clicked.connect(self.mail_screen)
        self.statusBar().showMessage('Welcome to Translator -WordList :)')
        self.show()
    
    def mail_screen(self):                                            
        self.w = EMailWindow()
        self.w.show()
        self.hide()
    
    @pyqtSlot()
    def on_click(self):
        non_text = any(char.isdigit() for char in self.line.text())
        if non_text is False:
            self.statusBar().showMessage("{} translated from {}".format(self.line.text(),detect_it(self.line.text())))
            self.label.setText(str(translate_it(self.line.text()).capitalize()))
            the_file.write("{}:{}\n".format(str(self.line.text()).capitalize(),translate_it(str(self.line.text())).capitalize()))
            self.line.clear()
        else:
            raise NonTextFoundException()

    def on_pressed(self):
        self.on_click()

def translate_it(user_input):
    if not any(char.isdigit() for char in user_input) and isinstance(user_input, str):
        window.label.setText(translator.translate(user_input,dest='tr').text)
        return translator.translate(user_input,dest='tr').text
    elif any(char.isdigit() for char in user_input):
        raise NonTextFoundException()
    elif user_input=="":
        raise EmptyInputException()
#This function translates user_input if it doesn't have any numbers or the input is not empty

def detect_it(user_input):
    if (not any(char.isdigit() for char in user_input)) and isinstance(user_input, str):
        return str(translator.detect(user_input).lang)
    else:
        return("Language couldn't detected")
#Detects language of the given input

def open_file():
    file_name = "WL {}.txt".format(date.today())
    if not(os.path.isfile(file_name)):
        the_file = open(file_name,"x")
        the_file.write("Words List:\n")
        return the_file
    else:
        return open(file_name,"a")
#If such a file doesn't exist, it creates one with following format "WL 2019-09-27.txt"
#If the file already exists, it just opens the file and appends the words later on.

def restarter():
    os.system("python user_interface_2.py")
#Restarts the program, will be used when an exception raised.

def email_is_valid(user_input):
    email_pattern = '[a-zA-Z]@[a-zA-Z]\.[a-zA-Z]'
    return re.match(email_pattern, str(user_input))
#Checks given input, returns true if it's a valid address.
try:
    #User-defined exception classes
    translation_list = {}
    the_file = type("file")
    language_detected = ""
    #Global variables that will be used

    translator  = Translator()
    the_file = open_file()
    App = QApplication(sys.argv)
    window = Window()
    user_input = str(window.line.text())
    sys.exit(App.exec())

    class Error(Exception):
        """Base class for other exceptions"""
        print("Oops, {} occurred.".format(Exception.__text_signature__))
        restarter()
    class EmptyInputException(Error):
        window.label.setText('Input can not be empty.')
        restarter()
    class GuiAlreadyExistsException(Error):
        window.label.setText('Only one GUI can be created at the time.')
        restarter()
    class InvalidEmailException(Error):
        print('Please enter a valid email address.')
        restarter()
    class NonTextFoundException(Error):
        print("Nontext values can't be translated")
except NonTextFoundException:
    window.label.setText(NonTextFoundException.with_traceback)
finally:
    the_file.write("Thanks for choosing me!")
    the_file.close()
