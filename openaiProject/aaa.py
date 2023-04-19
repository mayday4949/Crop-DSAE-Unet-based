import sys
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

import jieba
import math
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建界面控件
        self.label1 = QLabel("输入1:")
        #控件大小
        self.label1.setFixedSize(100, 60)
        #控件高度

        self.label2 = QLabel("输入2:")
        self.label2.setFixedSize(100, 60)
        self.edit1 = QLineEdit()
        self.edit2 = QLineEdit()
        self.button = QPushButton("计算")
        self.textbox = QTextEdit()

        # 绑定按钮点击事件
        self.button.clicked.connect(self.calculate)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.edit1)
        layout.addWidget(self.label2)
        layout.addWidget(self.edit2)
        layout.addWidget(self.button)
        layout.addWidget(self.textbox)

        # 设置窗口布局
        self.setLayout(layout)

    def cosine_similarity(self,s1, s2):
        # 将字符串分词并转换为向量
        vec1 = list(jieba.cut(s1))
        vec2 = list(jieba.cut(s2))
        
        # 将所有的单词存储到set中
        words = set(vec1 + vec2)
        
        # 计算每个向量中每个单词的出现次数
        vec1 = [vec1.count(w) for w in words]
        vec2 = [vec2.count(w) for w in words]
        
        # 计算余弦相似度
        dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(v1 ** 2 for v1 in vec1))
        magnitude2 = math.sqrt(sum(v2 ** 2 for v2 in vec2))
        
        # 处理分母为0的情况
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity


    def calculate_similarity(json_data, target_str):
        # 读取JSON数据
        data = json.loads(json_data)
        
        # 创建CountVectorizer对象，并使用fit_transform()函数将文本转换为向量
        vectorizer = CountVectorizer()
        vectors = vectorizer.fit_transform([data['str0'], data['str1'], data['str2'], data['str3'], data['str4'], data['str5']])
        
        # 计算相似度
        target_vector = vectors[0]
        text_vectors = vectors[1:]
        similarities = cosine_similarity(target_vector, text_vectors)
        
        # 返回相似度列表
        return similarities[0].tolist()


    def calculate(self):
        # 定义函数a，此处为示例函数
        # 调用函数a并将结果显示在文本框中
        s1 = self.edit1.text()
        s2 = self.edit2.text()
        # result = self.cosine_similarity(s1, s2)
        # self.textbox.setText(str(result))
        result = self.cosine_similarity(s1, s2) * 100
        percent_str = "{:.2f}%".format(result)
        self.textbox.setText(percent_str)

if __name__ == '__main__':
    # 创建应用程序和窗口
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()

    # 运行应用程序
    sys.exit(app.exec_())