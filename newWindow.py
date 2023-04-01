import random
import shutil
import sys
from tkinter import messagebox
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QFileDialog,QMenu,QTableWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGroupBox, QGridLayout
from PyQt5 import QtWidgets


import subprocess
import os


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化界面
        self.initUI()

        self.file_name = None
        self.output_file = None


        # 初始化文件路径
        if not os.path.exists('imgs'):
            os.mkdir('imgs')
        if not os.path.exists('imgs/input'):
            os.mkdir('imgs/input')
        if not os.path.exists("imgs/output"):
            os.mkdir("imgs/output")

    def initUI(self):

        # 设置窗口大小和标题
        self.setGeometry(100, 100, 700, 600)
        self.setWindowTitle('My App~农作物病害区域分割与面积估算')

        # 创建加载模型button
        self.load_model_button = QPushButton('初始化模型', self)
        self.load_model_button.setGeometry(30, 30, 200, 50)
        self.load_model_button.clicked.connect(self.load_model)

        #创建320*120的图片框 用于显示图片 script/title.jpg
        self.title_label = QLabel(self)
        self.title_label.setGeometry(320, 30, 320, 120)
        self.title_label.setAlignment(Qt.AlignCenter) # type: ignore
        # self.title_label.setStyleSheet("border: 1px solid black")
        self.title_label.setPixmap(QPixmap('scripts/title.jpg'))


        # 创建模型选择框
        self.file_select = QComboBox(self)
        self.file_select.setGeometry(30, 90, 200, 50)
        # 设置内容“请加载模型”
        self.file_select.addItem("需加载模型")
        #self.file_select.currentIndexChanged.connect(self.file_selection_changed)

        # 创建图片框
        self.left_label = QLabel(self)
        self.left_label.setGeometry(350, 180, 256, 256)
        self.left_label.setAlignment(Qt.AlignCenter) # type: ignore
        self.left_label.setStyleSheet("border: 1px solid black")

        # 创建选择文件的按钮
        self.select_button = QPushButton('选择文件', self)
        self.select_button.setGeometry(30, 150, 200, 50)
        self.select_button.clicked.connect(self.select_file)

        # 创建生成图片的按钮
        self.generate_button = QPushButton('病害区域识别', self)
        self.generate_button.setGeometry(30, 210, 200, 50)
        self.generate_button.clicked.connect(self.generate_image)

        #创建计算按钮
        self.general_button = QPushButton('混合&计算', self)
        self.general_button.setGeometry(30, 270, 200, 50)
        self.general_button.clicked.connect(self.mix_image)
        # # 创建值标签
        # self.lbl = QLabel('病害面积占比：', self)
        # self.lbl.setGeometry(850, 370, 200, 30)
        # self.lbl.setAlignment(Qt.AlignLeft)

        #创建 五行两列的数据表格 不需要表头
        self.table = QTableWidget(6, 2, self)
        self.table.setGeometry(30, 330, 260, 230)
        self.table.verticalHeader().setVisible(False)  # 不显示行表头
        self.table.horizontalHeader().setVisible(False)  # 不显示列表头
        self.table.horizontalScrollBar().setVisible(False)  # 不显示水平滚动条
        self.table.verticalScrollBar().setVisible(False)  # 不显示垂直滚动条

        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        item1 = QtWidgets.QTableWidgetItem('图片路径')
        item2 = QtWidgets.QTableWidgetItem('图片长')
        item3 = QtWidgets.QTableWidgetItem('图片宽')
        item4 = QtWidgets.QTableWidgetItem('图片树种')
        itembh = QtWidgets.QTableWidgetItem('病害名称')
        itemjs = QtWidgets.QTableWidgetItem('病害面积占比')

        self.table.setItem(0, 0, item1)
        self.table.setItem(1, 0, item2)
        self.table.setItem(2, 0, item3)
        self.table.setItem(3, 0, item4)
        self.table.setItem(4, 0, itembh)
        self.table.setItem(5, 0, itemjs)

        # itemmj = QtWidgets.QTableWidgetItem('10%')
        # self.table.setItem(5, 1, itemmj)



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
                


    def show_about_dialog(self):
        about_dialog = QLabel(self)
        about_dialog.setFixedSize(400, 300)
        about_dialog.setWindowTitle("About")
        about_dialog.setText("This is the about dialog!")
        about_dialog.show()

    def load_model(self):
        # 删除file_select原有内容
        self.file_select.clear()
        self.file_select.addItems(os.listdir("checkpoints"))
               



    def generate_image(self):
        if not self.file_name:
            return
        input_file = os.path.join("Imgs", "input", os.path.basename(self.file_name))
        #output_file = os.path.join("Imgs", "output", f"gen{random.randint(0, 1000000)}.jpg")
        output_file = os.path.join("Imgs", "output", f"{os.path.splitext(os.path.basename(self.file_name))[0]}_{random.randint(10, 99)}.jpg")
        self.file_name = input_file
        self.output_file = output_file
        model_file = os.path.join("checkpoints", self.file_select.currentText())

        cmd = f"python predict.py -i {input_file} -o {output_file} --model {model_file}"
        try:
            result = subprocess.run(cmd, shell=True, check=True)
            if result.returncode == 0:
                pixmap = QPixmap(output_file)
                self.left_label.setPixmap(pixmap)
        except subprocess.CalledProcessError as e:
            print(f"Command {cmd} returned non-zero exit status {e.returncode}")

        print(input_file+" "+output_file+"" +model_file+"cuda 处理完成 等待处理gengellabel")


    def blend_two_images(self,img1, img2, alpha):
        print("blend_two_images")

        #input_file = "Imgs\input\input_204291.jpg"
        #output_file = "Imgs\output\input_204291_78.jpg"

        #img1 = Image.open(input_file)
        #img2 = Image.open(output_file)
        img1 = img1.convert('RGBA')
        img2 = img2.convert('RGBA')
        
        img = Image.blend(img1, img2, alpha)

        img.save("Imgs\general\etemp.png")

    def mix_image(self):
        if self.file_name == None:
            return
        else:
            print("mix_image")
            print(self.file_name)
            print(self.output_file)
            img1 = Image.open(self.file_name)
            img2 = Image.open(self.output_file) # type: ignore
            
            #Debug
            # input_file = "Imgs\input\input_204291.jpg"
            # output_file = "Imgs\output\input_204291_78.jpg"
            # img1 = Image.open(input_file)
            # img2 = Image.open(output_file)
            print("start")
            self.blend_two_images(img1, img2, 0.6)
            print("mixend")
            pixmap = QPixmap("Imgs\general\etemp.png")
            self.left_label.setPixmap(pixmap)
            print("放置完成")

            print("开始计算")
            self.calculate_precent()

            print("计算完成")

    def count_non_black_pixels(self,image_path):
        # 打开图片
        image = Image.open(image_path)

        # 将图片转换为 RGB 模式，以便读取每个像素的 RGB 值
        image = image.convert('RGB')

        # 计算非黑色像素点的数量
        count = 0
        width, height = image.size
        for x in range(width):
            for y in range(height):
                r, g, b = image.getpixel((x, y))
                if r != 0 or g != 0 or b != 0:
                    count += 1

        return count

    def calculate_precent(self):
        print(self.file_name)
        print(self.output_file)
        non_black_pixel_count = self.count_non_black_pixels(self.file_name)
        white_pixel_count = self.count_non_black_pixels(self.output_file)
        print("input 非黑色个数")
        print(non_black_pixel_count)
        print("output 白色个数")
        print(white_pixel_count)
        print("白色个数/非黑色个数")
        print(white_pixel_count/non_black_pixel_count)
        percent = white_pixel_count/non_black_pixel_count
        #self.lbl.setText('病害面积占比为: {:.2%}'.format(float(percent)))
        #percent保留两位小数换算为百分比
        itemmj = QtWidgets.QTableWidgetItem('{:.2%}'.format(float(percent)))
        self.table.setItem(5, 1, itemmj)


# def file_selection_changed(self, index):
#     selected_file = self.file_select.currentText()
#     print(f"Selected file: {selected_file}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
