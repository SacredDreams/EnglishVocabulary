from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from PySide2.QtGui import *
import json
import random
import traceback
import time

class main:
    def __init__(self):
        self.main_ui = QUiLoader().load("ui\\main.ui")
        self.vocabulary_dict = {}
        self.vocabulary_list_key = []
        self.vocabulary_list_value = []
        self.arguments = {}
        self.randint = None
        self.temp_vocabulary_list = []
        self.screen_size = QGuiApplication.primaryScreen().geometry()
        # 读取json数据文件
        with open("data\\words.json", "r", encoding="utf-8") as file:
            self.vocabulary_dict = json.load(file)
        with open("data\\arguments.json", "r", encoding="utf-8") as file:
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
        self.setArguments(
            ui_width=self.arguments["UI-width"],
            ui_height=self.arguments["UI-height"],
            all_pushbutton_width=self.arguments["ALL_PushButton-width"],
            pushbutton_height=self.arguments["PushButton_2-height"],
            pushbutton_2_height=self.arguments["ALL_PushButton-height"]
        )

    def choose_vocabulary(self):
        """随机选择单词"""
        while True:
            if len(self.temp_vocabulary_list) == len(self.vocabulary_list_key):
                self.temp_vocabulary_list = []

            if self.main_ui.checkBox_3.isChecked() is True:
                self.temp_vocabulary_list = []

            self.randint = random.randint(0, len(self.vocabulary_list_key) - 1)

            if self.randint not in self.temp_vocabulary_list:
                if self.main_ui.checkBox.isChecked() is True:
                    self.main_ui.label.setText("")
                else:
                    self.main_ui.label.setText(self.vocabulary_list_key[self.randint])
                if self.main_ui.checkBox_2.isChecked() is True:
                    self.main_ui.label_3.setText("")
                else:
                    self.main_ui.label_3.setText(self.vocabulary_list_value[self.randint])

                self.temp_vocabulary_list.append(self.randint)
                break

    def getArguments(self):
        """获取并修改数据"""
        self.arguments["font-size-English"] = str(self.main_ui.spinBox.value()) + "px"
        self.arguments["font-size-Chinese"] = str(self.main_ui.spinBox_2.value()) + "px"
        self.arguments["checkBox"] = int(self.main_ui.checkBox.isChecked())
        self.arguments["checkBox_2"] = int(self.main_ui.checkBox_2.isChecked())
        self.arguments["checkBox_3"] = int(self.main_ui.checkBox_3.isChecked())
        # 储存数据
        with open("data\\arguments.json", "w", encoding="utf-8") as file:
            json.dump(self.arguments, file, ensure_ascii=False)
        # 重新设置数据
        self.setArguments()

    def setArguments(
            self,
            ui_width=1.0,
            ui_height=1.0,
            all_pushbutton_width=1.0,
            pushbutton_height=1.0,
            pushbutton_2_height=1.0
    ):
        """设置数据"""
        # 设置self.main_ui大小
        if ui_width < 1.0 and ui_height < 1.0:
            # 根据百分比计算数值
            self.main_ui.resize(
                int(self.screen_size.width() * ui_width), int(self.screen_size.height() * ui_height)
            )

        # 设置button
        if all_pushbutton_width < 1.0 and pushbutton_height < 1.0 and pushbutton_2_height < 1.0:
            # 根据百分比计算数值
            self.main_ui.pushButton.setStyleSheet(
                '''
                width: %d;
                height: %d;
                ''' % (
                    self.screen_size.width() * all_pushbutton_width,
                    self.screen_size.height() * pushbutton_height
                )
            )
            self.main_ui.pushButton_2.setStyleSheet(
                '''
                width: %d;
                height: %d;
                ''' % (
                    self.screen_size.width() * all_pushbutton_width,
                    self.screen_size.height() * pushbutton_2_height
                )
            )

        # 设置label
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

        # 设置spinBox
        self.main_ui.spinBox.setValue(int(self.arguments["font-size-English"].replace("px", "")))
        self.main_ui.spinBox_2.setValue(int(self.arguments["font-size-Chinese"].replace("px", "")))

        # 设置checkBox
        self.main_ui.checkBox.setChecked(bool(self.arguments["checkBox"]))
        self.main_ui.checkBox_2.setChecked(bool(self.arguments["checkBox_2"]))
        self.main_ui.checkBox_3.setChecked(bool(self.arguments["checkBox_3"]))

if __name__ == '__main__':
    app = QApplication()
    try:
        main = main()
        main.main_ui.show()
    except:
        # 输出错误信息
        logs_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        error_messages = traceback.format_exc()
        error_ui = QUiLoader().load("ui\\error.ui")
        error_ui.show()
        error_ui.textEdit.setMarkdown("```python\n%s" % error_messages)
        error_ui.setWindowTitle("Error - " + logs_time)
        with open("error_logs\\%s.log" % logs_time, "a") as file:
            file.write(error_messages)
    app.exec_()
