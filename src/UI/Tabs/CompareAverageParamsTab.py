from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import  QPushButton, QVBoxLayout, QFileDialog, QSizePolicy, QTextEdit, QWidget,QTableWidget, QTableWidgetItem,QHBoxLayout

from helpers.file_helpers import getParsedAverageParamsDict

class CompareAverageParamsTab(QWidget):
    def __init__(self):
        super().__init__()
        
        self.paths = ''

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

        self.parse_button = QPushButton("Compare average params", self)
        self.parse_button.clicked.connect(self.parse_excel)
        self.layout.addWidget(self.parse_button)
        
        self.tables_layout = QHBoxLayout()
        self.layout.addLayout(self.tables_layout)
    
        self.signal_params_table = QTableWidget(self)
        self.signal_params_table.setMinimumHeight(200)
        self.tables_layout.addWidget(self.signal_params_table)

    def browse_file(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Open Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)

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
            
            # params_df = pd.DataFrame(self.avarage_params.items(), columns = ['Parameter', 'Value'])
            
            # file_name = generateUniqueFileName(getFileNames('results'))
            # params_df.to_excel(f"results/compared_average_params/{file_name}.xlsx", index=False)
        else:
            self.file_path_edit.setText('Place path here')
    
    def init_table(self, data: list[dict]):
        self.signal_params_table.setRowCount(len(data[0]))
        self.signal_params_table.setColumnCount(len(data) + 1)
        self.signal_params_table.setHorizontalHeaderLabels(['Parameter', 'Value'])
        
        header_labels = ['Parameter']
        
        for counter, signal_params_dict in enumerate(data):
            header_labels.append(f"Value {counter + 1}")
            for row, (key, value) in enumerate(signal_params_dict.items()):
                item_key = QTableWidgetItem(str(key))
                item_value = QTableWidgetItem('{:.5f}'.format(value))

                self.signal_params_table.verticalHeader().setVisible(False)

                item_key.setFlags(item_key.flags() & ~Qt.ItemIsEditable)
                item_value.setFlags(item_value.flags() & ~Qt.ItemIsEditable)

                self.signal_params_table.setItem(row, 0, item_key)
                self.signal_params_table.setItem(row, counter + 1, item_value)
        
        self.signal_params_table.setHorizontalHeaderLabels(header_labels)