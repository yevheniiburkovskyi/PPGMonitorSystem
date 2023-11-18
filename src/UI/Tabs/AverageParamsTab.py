from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import  QPushButton, QVBoxLayout, QFileDialog, QSizePolicy, QTextEdit, QWidget,QTableWidget, QTableWidgetItem,QHBoxLayout

import pandas as pd


from matplotlib.figure import Figure

from helpers.file_helpers import getParsedSignal
from helpers.signal_helpers import getAverageParams, getMesures

class AverageParamsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.paths: list[str] = []
        self.avarage_params: dict

        self.layout = QVBoxLayout()
        
        self.setLayout(self.layout)
        
        self.file_browse_layout = QHBoxLayout()

        self.file_path_edit = QTextEdit(self)
        font = QFont()
        font.setPointSize(12)
        self.file_path_edit.setFont(font)
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.viewport().setCursor(Qt.ArrowCursor)
        self.file_path_edit.setFocusPolicy(Qt.NoFocus)
        self.file_path_edit.setPlaceholderText("Place file path here")

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_file)
        self.browse_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        self.file_browse_layout.addWidget(self.file_path_edit)
        self.file_browse_layout.addWidget(self.browse_button)
        
        self.layout.addLayout(self.file_browse_layout)

        self.parse_button = QPushButton("Parse", self)
        self.parse_button.clicked.connect(self.parse_excel)
        self.layout.addWidget(self.parse_button)
        
        self.signal_params_table = QTableWidget(self)
        self.signal_params_table.setMinimumHeight(200)
        self.layout.addWidget(self.signal_params_table)
        
        # self.canvas = FigureCanvas(Figure())
        # self.main_layout.addWidget(self.canvas)

    def browse_file(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Open Excel File", "", "Excel Files (*.xls);;All Files (*)", options=options)

        if files:
            self.paths = [file_path for file_path in files]
            paths_text = '\n'.join(self.paths)[:-1]
            self.file_path_edit.setText(paths_text)

    def parse_excel(self):
        if self.paths:
            params_data = []
            for path in self.paths:
                raw_signal = getParsedSignal(path)
                _,signal_params = getMesures(raw_signal)
                params_data.append(signal_params)
                
            self.avarage_params = getAverageParams(params_data)
            self.init_table(self.signal_params_table,self.avarage_params,headers = ['Parameter', 'Value'])
            
            df = pd.DataFrame(self.avarage_params.items(), columns = ['Parameter', 'Value'])
            df.to_excel("results/table_data.xlsx", index=False)
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
    
    def plot_graph(self, data: pd.DataFrame):
        figure = self.canvas.figure
        axes = figure.add_subplot(111)
        axes.plot(data.iloc[:, 0], data.iloc[:, 1])
        axes.set_title("Raw PPG signal")
        axes.set_xlabel("Time")
        axes.set_ylabel("Signal")
        
        self.canvas.draw()