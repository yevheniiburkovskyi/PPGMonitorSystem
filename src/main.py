import sys
from PyQt5.QtWidgets import QApplication

from UI.UI import ExcelParserApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelParserApp()
    window.show()
    sys.exit(app.exec_())