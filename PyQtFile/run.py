import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from rebuild2 import Ui_MainWindow
import random
import shutil
import sys
import subprocess
import os
from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        
def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'Images (*.png *.xpm *.jpg)')
        if file_name:
            try:
                item5 = QtWidgets.QTableWidgetItem(file_name)
                self.table.setItem(0, 1, item5)
                # 获取图片长宽
                img = Image.open(file_name)
                width, height = img.size
                item6 = QtWidgets.QTableWidgetItem(str(width))
                item7 = QtWidgets.QTableWidgetItem(str(height))
                self.table.setItem(1, 1, item6)
                self.table.setItem(2, 1, item7)
                # 获取图片树种 如果包含apple则为苹果，包含grape则为葡萄 否则为未知
                if 'apple' in file_name:
                    item8 = QtWidgets.QTableWidgetItem('苹果')
                    self.table.setItem(3, 1, item8)
                elif 'grape' in file_name:
                    item8 = QtWidgets.QTableWidgetItem('葡萄')
                    self.table.setItem(3, 1, item8)
                else:
                    item8 = QtWidgets.QTableWidgetItem('Unknown')
                    self.table.setItem(3, 1, item8)
                    
                # 获取病害名称
                if 'rot' in file_name:
                    item9 = QtWidgets.QTableWidgetItem('黑斑病')
                    self.table.setItem(4, 1, item9)
                else:
                    item9 = QtWidgets.QTableWidgetItem('Unknown')
                    self.table.setItem(4, 1, item9)
                


                # Generate a new random file name with a 6-digit suffix
                random_suffix = str(random.randint(100000, 999999))
                file_ext = os.path.splitext(file_name)[-1]
                new_file_name = "imgs/input/" + "input_" + random_suffix + file_ext
                self.file_name = new_file_name
                print(new_file_name+" "+self.file_name)

                # Copy the selected file to the input folder
                shutil.copy2(file_name, new_file_name)

                # Load the image and display it in the left label
                pixmap = QPixmap(new_file_name)
                self.left_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio)) # type: ignore

            except Exception as e:
                messagebox.warning(self, 'Error', str(e)) # type: ignore
                



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyMainForm()
    mainWindow.show()
    sys.exit(app.exec_())