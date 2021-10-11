import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPlainTextEdit, QDesktopWidget, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import datetime
import subprocess
import mysql.connector
import csv
import itertools
import os
import os.path
import random

global count
count = 0

CS = [[], [], [], [], []]
CS2 = [[], [], [], [], []]
global cultsub
cultsub = 0

table_check = False

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.database_create()

        self.mycursor.execute("USE Time_Table")
        self.mycursor.execute("SHOW TABLES")
        tables = self.mycursor.fetchone()
        
        self.mycursor.execute("select main_check from csv_check")
        main_check_value = self.mycursor.fetchone() 

        if tables[0] == "csv_check" and main_check_value[0] == 0:
            self.rowcount()

        elif main_check_value[0] == 1:
            self.cs()
            self.initUI()
            self.csv_read()

    def initUI(self):

        self.mainWindow = QtWidgets.QWidget()
        self.mainWindow.setGeometry(0, 0, 1600, 900)
        self.mainWindow.setWindowTitle("Time Table")

        self.mycursor.execute("USE Time_Table")
        self.mycursor.execute("Select * from csv_check")
        tables = self.mycursor.fetchone()

        self.row_size = int(tables[0])
        self.column_size = int(tables[1])

        self.tableWidget = QTableWidget(self.mainWindow)
        self.tableWidget.setRowCount(self.row_size)
        self.tableWidget.setColumnCount(self.column_size)

        self.drp_box_lbl = QtWidgets.QLabel(self.mainWindow)
        self.drp_box_lbl.setText("Semester:")
        self.drop_box = QComboBox(self.mainWindow)

        self.drop_box.addItem("Semester 1")
        self.drop_box.addItem("Semester 2")
        self.drop_box.addItem("Semester 3")
        self.drop_box.addItem("Semester 4")
        self.drop_box.addItem("Semester 5")
        self.drop_box.addItem("Semester 6")
        self.drop_box.addItem("Semester 7")
        self.drop_box.addItem("Semester 8")

        self.drop_box.activated[str].connect(self.onActivated)

        self.save_button = QtWidgets.QPushButton("Save", self.mainWindow)

        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()

        self.resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.width = (self.resolution.width() / 2) - 450
        self.height = (self.resolution.height() / 2) - 125

        self.frame_size = self.mainWindow.frameGeometry()

        self.tableWidget.move(self.width, self.height)

        self.tableWidget.setColumnWidth(0, 125)
        self.tableWidget.setColumnWidth(1, 125)
        self.tableWidget.setColumnWidth(2, 125)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 125)
        self.tableWidget.setColumnWidth(5, 125)
        self.tableWidget.setColumnWidth(6, 150)
        self.tableWidget.setColumnWidth(7, 125)
        self.tableWidget.setColumnWidth(8, 125)
        self.tableWidget.setColumnWidth(9, 125)

        self.tableWidget.setRowHeight(0, 50)
        self.tableWidget.setRowHeight(1, 50)
        self.tableWidget.setRowHeight(2, 50)
        self.tableWidget.setRowHeight(3, 50)
        self.tableWidget.setRowHeight(4, 50)
        self.tableWidget.setRowHeight(5, 50)
        self.tableWidget.setRowHeight(6, 50)
        self.tableWidget.setRowHeight(7, 50)
        self.tableWidget.setRowHeight(8, 50)
        self.tableWidget.setRowHeight(9, 50)

        self.tableWidget.resize(927, 252)

        self.drp_box_lbl.move((self.frame_size.width() - 1525), (self.frame_size.height() - 800))
        self.drop_box.move((self.frame_size.width() - 1450), (self.frame_size.height() - 800))
        self.drop_box.resize(150, 25)

        self.save_button.move((self.frame_size.width() - 300), (self.frame_size.height() - 175))
        self.save_button.resize(75, 50)
        self.save_button.clicked.connect(self.csv_write)

        gg = self.cs()
    
        for i in range(0,len(gg)):
            for j in range(0,len(gg[0])):
      
                ggs = gg[i][j]
                self.tableWidget.setItem(i, j, QTableWidgetItem(ggs))

        

        

        self.mainWindow.show()

    def onActivated(self, text):

        self.semester_value = text
        print(self.semester_value)
        self.csv_read()

    def database_create(self):

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            buffered=True
        )

        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SHOW DATABASES")
        self.db_exists = False

        for x in self.mycursor:

            if x[0] == 'Time_Table':
                self.db_exists = True

        if self.db_exists == False:
            self.mycursor.execute("CREATE DATABASE Time_Table")

    def database_table(self):

        self.mycursor.execute("use Time_Table")
        self.mycursor.execute("show tables")
        self.table_exists = False

        for a in self.mycursor:
            if a[0] == 'csv_check':
                self.table_exists = True

        if self.table_exists == False:
            self.mycursor.execute("create table csv_check(row_value int,col_val int,init_sem_value int)")

    def table_insert(self):

        row_size = int(self.row_entry.text())
        col_size = int(self.column_entry.text())
        
        self.mycursor.execute("update csv_check set row_value = %s, col_val = %s,init_sem_value = 1 where value_check = 1" % (row_size,col_size))

        self.mydb.commit()

    def csv_write(self):

        with open("/Users/srinivas/output_csv_{0}".format(self.file_end), "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            for i in range(0, self.row_size):
                for j in range(0, self.column_size):
                    item = self.tableWidget.item(i, j)          
                    writer.writerow([item.text()])

    def csv_read(self):

        try:
            self.file_end = self.semester_value[-1]
        except AttributeError:
            self.file_end = 1

        exists = os.path.isfile('/Users/srinivas/output_csv_{0}'.format(self.file_end))
        if exists:

            with open('/Users/srinivas/output_csv_{0}'.format(self.file_end), newline='') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                value = []
                for val in reader:
                    value.append(val)
                print(value)
                for i in range(0, self.row_size):
                    for j in range(0, self.column_size):

                        global count
                        gg = next(iter(value[count]))
                        self.tableWidget.setItem(i, j, QTableWidgetItem(gg))

                        count += 1

        else:

            self.initUI()

    def cs(self):
        condition = 1
        while condition == 1:  # to avoid infinite loop
            a = {"java": 3, "dbms": 3, "PC5": 2, "PP3": 2, "BM": 3, "BD": 3, "FLAT": 3, "LAB1": 2, "LAB2": 2, "MP": 2,
                 "Free": 1, "Cult": 3, "PC3": 1, "PP1": 2, "CN": 3}
            flag = 0

            lab_check = 0
            infi = 0

            for sublist in range(5):  # 5 days in a week
                while len(CS[sublist]) < 7:  # 7 hours in a day
                    ch = random.choice(list(a.keys()))
                    for j in CS[sublist]:  # make sure same subject doesn't repeat twice in a day
                        if ch == j:
                            flag = 1
                    if flag == 0:
                        if ch == 'LAB1' or ch == 'LAB2' or ch == 'MP' or ch == 'PP1' or ch == 'PP3':
                            if len(CS[sublist]) == 0 or len(CS[sublist]) == 2 or len(CS[sublist]) == 4 or len(
                                    CS[sublist]) == 5:  # 2 hour subjects shouldn't come in between breaks
                                if lab_check == 0:  # make sure labs don't repeat in the same day
                                    lab_check = 1
                                    CS[sublist].append(ch)
                                    CS[sublist].append(ch)
                                    a[ch] = a[ch] - 2

                        elif ch == 'Cult':
                            if len(CS[sublist]) == 4:
                                CS[sublist].append(ch)
                                CS[sublist].append(ch)
                                CS[sublist].append(ch)
                                a[ch] = a[ch] - 3
                                global cultsub
                                cultsub = sublist
                        else:
                            CS[sublist].append(ch)
                            a[ch] = a[ch] - 1
                        if a[ch] == 0:
                            del a[ch]
                    flag = 0
                    infi = infi + 1  # to break from infinite loop
                    if infi > 100:
                        break
                lab_check = 0

            if len(CS[4]) == 7:
                condition = 0

        return (CS)

    def rowcount(self):

        self.rowWindow = QtWidgets.QWidget()
        self.resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.window_1_width = (self.resolution.width() / 2) - 150
        self.window_1_height = (self.resolution.height() / 2) - 50

        self.rowWindow.setGeometry(self.window_1_width, self.window_1_height, 310, 100)

        self.row_label = QtWidgets.QLabel(self.rowWindow)
        self.row_label.setText("Enter row size")

        self.row_entry = QtWidgets.QLineEdit(self.rowWindow)

        self.row_ok = QtWidgets.QPushButton("OK", self.rowWindow)

        self.row_ok.clicked.connect(self.row_ok_click)

        self.row_ok.move(220, 70)
        self.row_label.move(25, 35)
        self.row_entry.move(130, 32)

        self.rowWindow.setFixedSize(310, 100)

        self.mycursor.execute("update csv_check set main_check = 1 where main_check = 0")
        self.mydb.commit()

        self.rowWindow.show()

    def columncount(self):

        self.columnWindow = QtWidgets.QWidget()

        self.resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.window_2_width = (self.resolution.width() / 2) - 175
        self.window_2_height = (self.resolution.height() / 2) - 50

        self.columnWindow.setGeometry(self.window_2_width, self.window_2_height, 350, 100)

        self.column_label = QtWidgets.QLabel(self.columnWindow)
        self.column_label.setText("Enter column size")

        self.column_entry = QtWidgets.QLineEdit(self.columnWindow)

        self.column_ok = QtWidgets.QPushButton("OK", self.columnWindow)

        self.column_ok.clicked.connect(self.column_ok_click)

        self.column_ok.move(250, 70)
        self.column_label.move(25, 35)
        self.column_entry.move(150, 32)

        self.columnWindow.setFixedSize(350, 100)

        self.columnWindow.show()

        self.database_table()

    def row_ok_click(self):

        self.columncount()
        self.rowWindow.close()

    def column_ok_click(self):

        self.csv_check = True
        self.table_insert()

        self.initUI()
        self.columnWindow.close()


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        
        self.database_create()

        self.mycursor.execute("USE Time_Table")
        self.mycursor.execute("SHOW TABLES")
        tables = self.mycursor.fetchone()

        if tables == None:
            pass
       
        else:
            self.mycursor.execute("select value_check from csv_check")
            self.checks = self.mycursor.fetchone()

            
        if tables == None:
            self.database_table()
            self.table_insert()
            uic.loadUi('/Users/srinivas/Downloads/les/main.ui', self)
            self.ok_button.clicked.connect(self.values)
            # self.ok_button.clicked.connect(self.value_2)
         
        # self.okbutton.clicked.connect(self.value_2)
        # if self.checks[0] == 0:
        #     uic.loadUi('/Users/srinivas/Downloads/les/main.ui', self)
        #     self.ok_button.clicked.connect(self.values)
        
        # else:
        #     pass
            

    def values(self):

        self.no_of_Slots = self.Slots_day.toPlainText()
        self.start = []
        self.end = []
        self.start.append(self.Start_1.toPlainText())
        self.start.append(self.Start_2.toPlainText())
        self.start.append(self.Start_3.toPlainText())
        self.start.append(self.Start_4.toPlainText())
        self.start.append(self.Start_5.toPlainText())
        self.start.append(self.Start_6.toPlainText())
        self.start.append(self.Start_7.toPlainText())
        self.end.append(self.End_1.toPlainText())
        self.end.append(self.End_2.toPlainText())
        self.end.append(self.End_3.toPlainText())
        self.end.append(self.End_4.toPlainText())
        self.end.append(self.End_5.toPlainText())
        self.end.append(self.End_6.toPlainText())
        self.end.append(self.End_7.toPlainText())
        self.breaks = []
        self.breaks.append(self.break_1.toPlainText())
        self.breaks.append(self.break_2.toPlainText())
        self.days_week = self.days_week.toPlainText()

        # try:
        #     self.file_end = self.semester_value[-1]
        # except AttributeError:
        #     self.file_end = 1

        with open("/Users/srinivas/output_csv_time", "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            for i in range(0, len(self.start)):
                value_1 = self.start[i]
                value_2 = self.end[i]
                writer.writerow([value_1])
                writer.writerow([value_2])
    
        uic.loadUi('/Users/srinivas/Downloads/les/lol.ui', self)

        self.okbutton.clicked.connect(self.value_2)

    def value_2(self):

        
        self.teacher_numbers = self.Teacher_no.toPlainText()
        self.subjects = []
        self.time_req = []
        self.subjects.append(self.subj_select_1.toPlainText())
        self.subjects.append(self.subj_select_2.toPlainText())
        self.subjects.append(self.subj_select_3.toPlainText())
        self.subjects.append(self.subj_select_4.toPlainText())
        self.subjects.append(self.subj_select_5.toPlainText())
        self.subjects.append(self.subj_select_6.toPlainText())
        self.subjects.append(self.subj_select_7.toPlainText())
        self.time_req.append(self.Time_req_1.toPlainText())
        self.time_req.append(self.Time_req_2.toPlainText())
        self.time_req.append(self.Time_req_3.toPlainText())
        self.time_req.append(self.Time_req_4.toPlainText())
        self.time_req.append(self.Time_req_5.toPlainText())
        self.time_req.append(self.Time_req_6.toPlainText())
        self.time_req.append(self.Time_req_7.toPlainText())
        self.batch_no = self.no_batch.toPlainText()
        self.batch = self.batch_name.toPlainText()
        self.semester_name = self.semester_value_1.toPlainText()

        with open("/Users/srinivas/output_csv_time", "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            for i in range(0, len(self.subjects)):
                value_1 = self.subjects[i]
                value_2 = self.time_req[i]
                writer.writerow([value_1])
                writer.writerow([value_2])
    
        self.okbutton.clicked.connect(self.check)
        
        
        

    def check(self):

        sql = "update csv_check set value_check = 1 where value_check = 0"
        self.mycursor.execute(sql)
        self.mydb.commit()
        self.checker()
        self.close()
        


    def database_create(self):

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            buffered=True
        )

        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SHOW DATABASES")
        self.db_exists = False

        for x in self.mycursor:

            if x[0] == 'Time_Table':
                self.db_exists = True

        if self.db_exists == False:
            self.mycursor.execute("CREATE DATABASE Time_Table")

    def database_table(self):

        self.mycursor.execute("use Time_Table")
        self.mycursor.execute("show tables")
        self.table_exists = False

        for a in self.mycursor:
            if a[0] == 'csv_check':
                self.table_exists = True

        if self.table_exists == False:
            self.mycursor.execute("create table csv_check(row_value int,col_val int,init_sem_value int,value_check int,main_check int)")

    def table_insert(self):

        sql = "INSERT INTO csv_check (value_check,main_check) VALUEs(%s,%s)"
        val = [0,0]
        self.mycursor.execute(sql, val)
        self.mydb.commit()
    
    def checker(self):
        sql = "select value_check from csv_check"
        self.mycursor.execute(sql)
        check = self.mycursor.fetchone()
        return (check[0])

class db_connect():
    
    def __init__(self):
        pass

    def database_create(self):

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            buffered=True
        )

        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SHOW DATABASES")
        self.db_exists = False

        for x in self.mycursor:

            if x[0] == 'Time_Table':
                self.db_exists = True

        if self.db_exists:
            return (0)
        else:
            return (1)
        

            
    



if __name__ == '__main__':


    app = QtWidgets.QApplication(sys.argv)

    # window = MyWindow()
    # window_check = window.checker()
    # window.show()

    checkss = db_connect()
    vars = checkss.database_create()
    window_check = ''

    print (vars)
    if vars == 1:
        window = MyWindow()
        window_check = window.checker()
        window.show()
    else:
        pass

 
    if vars == 0:
        window_2 = Window()
        window_2.show()

    
    sys.exit(app.exec_())