from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTabWidget
from PyQt5.QtGui import QFont

from UI.Tabs.AverageParamsTab import AverageParamsTab
from UI.Tabs.CompareAverageParamsTab import CompareAverageParamsTab

class ExcelParserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PPG monitoring system")
        self.setMinimumWidth(800)

        self.central_widget = QTabWidget(self)
        self.setCentralWidget(self.central_widget)
        
        font = QFont()
        font.setPointSize(12)
        self.central_widget.tabBar().setFont(font)
        
        self.tab1 = AverageParamsTab()
        self.tab2 = CompareAverageParamsTab()
        self.tab3 = QTableWidget()

        self.central_widget.addTab(self.tab1, "Calculate average params")
        self.central_widget.addTab(self.tab2, "Compare average params")
        self.central_widget.addTab(self.tab3, "Tab 3")