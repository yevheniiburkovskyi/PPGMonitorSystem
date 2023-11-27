import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import  QPushButton, QVBoxLayout, QFileDialog,  QMessageBox, QTextEdit, QWidget,QTableWidget, QTableWidgetItem,QHBoxLayout,QLabel

import pandas as pd

from helpers.file_helpers import getFileNames, getParsedSignal
from helpers.signal_helpers import getAverageParams, getMesures

class AverageParamsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.paths: list[str] = []
        self.avarage_params: dict
        self.avarage_params_list: list[dict] = []
        self.params_df: pd.DataFrame

        self.layout = QVBoxLayout()
        
        self.setLayout(self.layout)

        self.file_path_edit = QTextEdit(self)
        font = QFont()
        font.setPointSize(12)
        self.file_path_edit.setFont(font)
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.viewport().setCursor(Qt.ArrowCursor)
        self.file_path_edit.setFocusPolicy(Qt.NoFocus)
        self.file_path_edit.setMaximumHeight(50)
        self.file_path_edit.setPlaceholderText("Here you will see your file paths")

        self.browse_button = QPushButton("Browse File", self)
        self.browse_button.clicked.connect(self.browse_file)
        self.browse_button.setFont(font)
        
        self.layout.addWidget(self.file_path_edit)
        self.layout.addWidget(self.browse_button)

        self.parse_button = QPushButton("Calculate average params", self)
        self.parse_button.clicked.connect(self.parse_excel)
        self.parse_button.setFont(font)
        self.layout.addWidget(self.parse_button)
        
        self.signal_params_table = QTableWidget(self)
        self.signal_params_table.setMinimumHeight(200)
        self.layout.addWidget(self.signal_params_table)
        
        self.save_file_layout = QHBoxLayout()
        
        self.save_file_path_label = QLabel("Enter file name:", self)
        self.save_file_path_label.setFont(font)
        self.layout.addWidget(self.save_file_path_label)
        
        self.save_file_path_edit = QTextEdit(self)
        self.save_file_path_edit.setFont(font)
        self.save_file_path_edit.setMaximumHeight(30)
        self.save_file_path_edit.setPlaceholderText("Please enter a file name")

        self.save_browse_button = QPushButton("Save", self)
        self.save_browse_button.setFixedHeight(30)
        self.save_browse_button.clicked.connect(self.save_file)
        self.save_browse_button.setFont(font)
        
        self.save_file_layout.addWidget(self.save_file_path_edit)
        self.save_file_layout.addWidget(self.save_browse_button)
        
        self.layout.addLayout(self.save_file_layout)
        
        self.save_file_path_error_label = QLabel("", self)
        self.save_file_path_error_label.setStyleSheet("color: red")
        self.save_file_path_error_label.setFont(font)
        self.layout.addWidget(self.save_file_path_error_label)

    def browse_file(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Open Excel File", "", "Excel Files (*.xls);;All Files (*)", options=options)

        if files:
            self.paths = [file_path for file_path in files]
            paths_text = '\n'.join(self.paths)[:-1]
            self.file_path_edit.setText(paths_text)

    def parse_excel(self):
        if self.paths:
            self.avarage_params_list = []
            for path in self.paths:
                raw_signal = getParsedSignal(path)
                _,signal_params = getMesures(raw_signal)
                self.avarage_params_list.append(signal_params)
            # self.build_param_plot()
            self.avarage_params = getAverageParams(self.avarage_params_list)
            self.init_table(self.signal_params_table,self.avarage_params,headers = ['Parameter', 'Value'])
            
            self.params_df = pd.DataFrame(self.avarage_params.items(), columns = ['Parameter', 'Value'])
        else:
            self.file_path_edit.setText('Place path here')
    
    def init_table(self, table, data, headers):
        table.setRowCount(len(data))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(headers)

        for row, (key, value) in enumerate(data.items()):
            item_key = QTableWidgetItem(str(key))
            item_value = QTableWidgetItem('{:.5f}'.format(value))

            table.verticalHeader().setVisible(False)

            item_key.setFlags(item_key.flags() & ~Qt.ItemIsEditable)
            item_value.setFlags(item_value.flags() & ~Qt.ItemIsEditable)

            table.setItem(row, 0, item_key)
            table.setItem(row, 1, item_value)
    
    def save_file(self):
        existing_names = getFileNames('results/single_average_params')
        file_name = self.save_file_path_edit.toPlainText()
        if not file_name:
            self.save_file_path_error_label.setText("Please enter a file name")
        elif f'{file_name}.xlsx' in existing_names:
            self.save_file_path_error_label.setText("File already exists. Please enter a different name !")
        else:
            self.params_df.to_excel(f"results/single_average_params/{file_name}.xlsx", index=False)
            self.clear_ui()
            self.show_alert(file_name)

    def show_alert(self, file_name):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText(f"File '{file_name}' successfully saved!")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    def clear_ui(self):
        self.file_path_edit.setPlainText('')
        self.save_file_path_error_label.setText("")
        self.save_file_path_edit.setPlainText('')
        self.signal_params_table.clearContents()
        self.signal_params_table.setRowCount(0)