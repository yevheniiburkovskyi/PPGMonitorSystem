import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import  QPushButton, QVBoxLayout, QFileDialog,  QTextEdit, QWidget,QTableWidget, QTableWidgetItem,QHBoxLayout

from helpers.file_helpers import getParsedAverageParamsDict

from constants.constants import headers, params_keys

class CompareAverageParamsTab(QWidget):
    def __init__(self):
        super().__init__()
        
        self.paths = ''
        self.file_names: list[str] = []
        
        self.headers = headers

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

        self.parse_button = QPushButton("Compare average params", self)
        self.parse_button.clicked.connect(self.parse_excel)
        self.parse_button.setFont(font)
        self.layout.addWidget(self.parse_button)
        
        self.tables_layout = QHBoxLayout()
        self.layout.addLayout(self.tables_layout)
    
        self.signal_params_table = QTableWidget(self)
        self.signal_params_table.horizontalHeader().setStyleSheet("QHeaderView::section { border: 1px solid black; }")
        self.signal_params_table.setMinimumHeight(390)
        self.signal_params_table.setRowCount(len(params_keys))
        self.signal_params_table.setColumnCount(2)
        self.signal_params_table.setHorizontalHeaderLabels(self.headers)
        self.signal_params_table.verticalHeader().setVisible(False)
        self.signal_params_table.setColumnWidth(0,400)
        self.signal_params_table.setColumnWidth(1,100)
        
        for row, key in enumerate(params_keys):
            item_key = QTableWidgetItem(key)
            self.signal_params_table.setItem(row, 0, item_key)
            item_key.setFlags(item_key.flags() & ~Qt.ItemIsEditable)
        
        self.tables_layout.addWidget(self.signal_params_table)

    def browse_file(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Open Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        self.file_names = [os.path.splitext(os.path.basename(file_path))[0] for file_path in files]
        print(files)
        if files:
            self.paths = [file_path for file_path in files]
            paths_text = '\n'.join(self.paths)[:-1]
            self.file_path_edit.setText(paths_text)

    def parse_excel(self):
        if self.paths:
            params_data = []
            for path in self.paths:
                signal_params = getParsedAverageParamsDict(path)
                params_data.append(signal_params)

            self.init_table(params_data)

        else:
            self.file_path_edit.setText('Place path here')
    
    def init_table(self, data: list[dict]):
        self.signal_params_table.setColumnCount(len(data) + 1)
        
        header_labels = ['Parameter']
        
        for counter, signal_params_dict in enumerate(data):
            header_labels.append(self.file_names[counter])
            for row, (key, value) in enumerate(signal_params_dict.items()):

                item_value = QTableWidgetItem('{:.5f}'.format(value))

                self.signal_params_table.verticalHeader().setVisible(False)

                item_value.setFlags(item_value.flags() & ~Qt.ItemIsEditable)

                self.signal_params_table.setItem(row, counter + 1, item_value)
        
        self.signal_params_table.setHorizontalHeaderLabels(header_labels)