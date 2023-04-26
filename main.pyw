from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
import json
import random

class main:
    def __init__(self):
        self.main_ui = QUiLoader().load("ui\\main.ui")
        self.vocabulary_dict = {}
        self.vocabulary_list_key = []
        self.vocabulary_list_value = []
        self.randint = None
        self.arguments = {}
        # 读取json数据文件
        with open("data.json", "r", encoding="utf-8") as file:
            self.vocabulary_dict = json.load(file)
        with open("data_1.json", "r", encoding="utf-8") as file:
            self.arguments = json.load(file)
        # 制作单词列表
        for key, value in self.vocabulary_dict.items():
            self.vocabulary_list_key.append(key)
            self.vocabulary_list_value.append(value)
        # 建立链接
        self.main_ui.pushButton.clicked.connect(self.choose_vocabulary)
        self.main_ui.pushButton_2.clicked.connect(self.getArguments)
        self.main_ui.spinBox.setRange(self.arguments["spinBox-min"], self.arguments["spinBox-max"])
        self.main_ui.spinBox_2.setRange(self.arguments["spinBox-min"], self.arguments["spinBox-max"])
        # 设置参数
        self.setArguments()

    def choose_vocabulary(self):
        # 随机选择单词
        self.randint = random.randint(0, len(self.vocabulary_list_key))
        self.main_ui.label.setText(self.vocabulary_list_key[self.randint - 1])
        self.main_ui.label_3.setText(self.vocabulary_list_value[self.randint - 1])

    def getArguments(self):
        # 获取并修改数据
        self.arguments["font-size-English"] = str(self.main_ui.spinBox.value()) + "px"
        self.arguments["font-size-Chinese"] = str(self.main_ui.spinBox_2.value()) + "px"
        # 储存数据
        with open("data_1.json", "w", encoding="utf-8") as file:
            json.dump(self.arguments, file, ensure_ascii=False)
        # 重新设置数据
        self.setArguments()

    def setArguments(self):
        # 设置数据
        self.main_ui.label.setStyleSheet(
            '''
            font-size: %s
            ''' % self.arguments["font-size-English"]
        )
        self.main_ui.label_3.setStyleSheet(
            '''
            font-size: %s
            ''' % self.arguments["font-size-Chinese"]
        )
        self.main_ui.spinBox.setValue(int(self.arguments["font-size-English"].replace("px", "")))
        self.main_ui.spinBox_2.setValue(int(self.arguments["font-size-Chinese"].replace("px", "")))

if __name__ == '__main__':
    app = QApplication()
    main = main()
    main.main_ui.show()
    app.exec_()