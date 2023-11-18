from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTabWidget

from UI.Tabs.AverageParamsTab import AverageParamsTab

class ExcelParserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PPG monitoring system")

        self.central_widget = QTabWidget(self)
        self.setCentralWidget(self.central_widget)

        self.tab1 = AverageParamsTab()
        self.tab2 = QTableWidget()
        self.tab3 = QTableWidget()

        self.central_widget.addTab(self.tab1, "Tab 1")
        self.central_widget.addTab(self.tab2, "Tab 2")
        self.central_widget.addTab(self.tab3, "Tab 3")