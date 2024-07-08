# -------------------------------------------------------------------------------
# Name:             Dates.py
# Purpose:          Simple app to track and view special events
#
# Author:           Jeffreaux
#
# Created:          08July24
#
# Required Packages:    PyQt5, PyQt5-Tools
# -------------------------------------------------------------------------------

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QAction,
    QLineEdit,
    QLabel,
    QStackedWidget,
    QDateEdit,
    QComboBox
)
from PyQt5 import uic
from datetime import date

#from fileModule import *
import sys
import sqlite3


# Create dBase and create cursor
conn = sqlite3.connect("Dates.db")
c = conn.cursor()

command_create_table = """
                    CREATE TABLE IF NOT EXISTS people(
                    firstname TEXT,
                    lastname TEXT,
                    DBirth TEXT,
                    DDeath TEXT,
                    EDate TEXT,
                    event TEXT
                    )"""

c.execute(command_create_table)

# c.execute("CREATE TABLE IF NOT EXISTS people (firstname, lastname, age)")
# c.execute("INSERT INTO people VALUES ('John', 'Richard', 23)")

conn.commit()
conn.close()

# Set current date in forms



class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the UI file
        uic.loadUi("Dates_GUI.ui", self)

        # define Widgets ############################################################
        self.btnExit = self.findChild(QPushButton, "btnExit")
        self.btnEnterNewRecord = self.findChild(QPushButton, "btnEnterNewRecord")
        self.btnSaveNewRecord = self.findChild(QPushButton, "btnSaveNewRecord")
        self.btnSearchRecords = self.findChild(QPushButton, "btnSearchRecords")

        self.txtFirstName = self.findChild(QLineEdit, "txtFirstName")
        self.txtLastName = self.findChild(QLineEdit, "txtLastName")

        self.lblBirth = self.findChild(QLabel, "lblBirth")
        self.lblDeath = self.findChild(QLabel, "lblDeath")
        self.lblEvent = self.findChild(QLabel, "lblEvent")

        self.dtBirth = self.findChild(QDateEdit, "dtBirth")
        self.dtDeath = self.findChild(QDateEdit,"dtDeath")
        self.dtEvent = self.findChild(QDateEdit, "dtEvent")

        self.cboEvent = self.findChild(QComboBox, "cboEvent")
        
        self.actExit = self.findChild(QAction, "actExit")

        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")


        # Define the actions ###########################################################
        self.btnExit.clicked.connect(self.closeEvent)
        self.btnEnterNewRecord.clicked.connect(self.enter_new_record)
        self.btnSaveNewRecord.clicked.connect(self.write_to_db)
        self.btnSearchRecords.clicked.connect(self.search_records)
        self.actExit.triggered.connect(self.closeEvent)
        self.cboEvent.currentIndexChanged.connect(self.death_date_status)

        # Set Home Screen
        self.stackedWidget.setCurrentWidget(self.Home)

        # Set current date in labels
        self.dtBirth.setDate(date.today())
        self.dtDeath.setVisible(False)
        self.lblDeath.setVisible(False)
        self.dtDeath.setDate(date.today())
        self.dtEvent.setVisible(False)
        self.lblEvent.setVisible(False)
        self.dtEvent.setDate(date.today())

        # Load ComboBox
        #self.cboEvent.addItem(" ")
        self.cboEvent.addItem("Birthday")
        self.cboEvent.addItem("Anniversary")
        self.cboEvent.addItem("Death")


        # Show the app
        self.show()

    def death_date_status(self):  # Enable / Disable available date options depending on event
        if self.cboEvent.currentText() == "Death":
            self.dtDeath.setVisible(True)
            self.lblDeath.setVisible(True)
            self.dtBirth.setVisible(True)
            self.lblBirth.setVisible(True)
            self.dtEvent.setVisible(False)
            self.lblEvent.setVisible(False)
        elif self.cboEvent.currentText() == "Anniversary":
            self.dtEvent.setVisible(True)
            self.lblEvent.setVisible(True)
            self.dtDeath.setVisible(False)
            self.lblDeath.setVisible(False)
            self.dtBirth.setVisible(False)
            self.lblBirth.setVisible(False)
        else:
            self.dtBirth.setVisible(True)
            self.lblBirth.setVisible(True)
            self.dtDeath.setVisible(False)
            self.lblDeath.setVisible(False)
            self.dtEvent.setVisible(False)
            self.lblEvent.setVisible(False)
        
        
    def search_records(self):
        print("Ready to search??")
        self.stackedWidget.setCurrentWidget(self.Search)
    


    def enter_new_record(self):
        self.stackedWidget.setCurrentWidget(self.Entry)
        self.dtBirth.setVisible(True)


    def write_to_db(self):
        # Setting up Variables
        fName = self.txtFirstName.text()
        print(fName)
        lName = self.txtLastName.text()
        print(lName)
        eventType = self.cboEvent.currentText()
        print(eventType)
        birthDay = self.dtBirth.date().toString("MM-dd-yyyy")
        print(birthDay)
        if self.cboEvent.currentText() == "Death":
            deathDay = self.dtDeath.date().toString("MM-dd-yyyy")
        else:
            deathDay = "   "
        print(deathDay)
        if self.cboEvent.currentText() == "Anniversary":
            eventDay = self.dtEvent.date().toString("MM-dd-yyyy")
        else:
            eventDay = "   "
        print(eventDay)
        event = self.cboEvent.currentText()
        print(event)
        
        # Writing to dB
        conn = sqlite3.connect("Dates.db")  # Open dBase
        c = conn.cursor()  # Create Cursor
        # Write Data
        c.execute("INSERT INTO people (firstname, lastname, DBirth, DDeath, EDate, event) VALUES (? ,? ,?, ?, ?, ?)", (fName, lName, birthDay, deathDay, eventDay, event))

        conn.commit()  # Save Write
        conn.close()  # Close connection

        # Resetting boxes and return to home page
        self.txtFirstName.clear()
        self.txtLastName.clear()
        self.dtDeath.setVisible(False)
        self.dtEvent.setVisible(False)
        self.stackedWidget.setCurrentWidget(self.Home)

    def closeEvent(self, *args, **kwargs):
        # print("Program closed Successfully!")
        self.close()


# Initialize the App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
