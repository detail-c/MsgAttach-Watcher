import sys
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QFileDialog,
    QLabel,
    QFormLayout,
)

from config import Config
from views.add_whitelist_dialog import AddWhitelistDialog


class MainWindow(QWidget):
    def __init__(self, config: Config, save_config: callable):
        super().__init__()

        self.config = config
        self.save_config = save_config

        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle("MsgAttach Watcher")
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 表单
        self.form_layout = QFormLayout()
        self.form_layout.setHorizontalSpacing(10)

        # 保存的根路径
        self.base_path_label = QLabel("路径:")

        self.base_path_layout = QHBoxLayout()

        self.base_path_input = QLineEdit()
        self.base_path_input.setText(self.config.base_path)

        self.base_path_button = QPushButton("选择路径")
        self.base_path_button.setToolTip("选择要转换的图片文件夹")
        self.base_path_button.clicked.connect(self.choose_folder)

        self.base_path_layout.addWidget(self.base_path_input)
        self.base_path_layout.addWidget(self.base_path_button)
        self.form_layout.addRow(self.base_path_label, self.base_path_layout)

        # 保存路径模板
        self.path_template_label = QLabel("模板:")
        self.path_template_input = QLineEdit()
        self.path_template_input.setText(self.config.path_template)
        self.path_template_input.textChanged.connect(self.set_path_template)
        self.form_layout.addRow(self.path_template_label, self.path_template_input)

        # 日期格式
        self.date_format_label = QLabel("日期格式:")
        self.date_format_input = QLineEdit()
        self.date_format_input.setText(self.config.date_format)
        self.date_format_input.textChanged.connect(self.set_date_format)
        self.form_layout.addRow(self.date_format_label, self.date_format_input)

        # 白名单
        self.whitelist_label = QLabel("白名单:")

        self.whitelist_layout = QVBoxLayout()
        self.whitelist = QListWidget()
        self.whitelist.addItems([user.nickname for user in self.config.whitelist])
        self.whitelist.itemDoubleClicked.connect(self.remove_whitelist_item)

        self.add_whitelist_button = QPushButton("添加白名单")
        self.add_whitelist_button.clicked.connect(self.show_add_whitelist_dialog)

        self.whitelist_layout.addWidget(self.whitelist)
        self.whitelist_layout.addWidget(self.add_whitelist_button)
        self.form_layout.addRow(self.whitelist_label, self.whitelist_layout)

        # 保存按钮
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_config)
        self.form_layout.addRow(self.save_button)

        # 设置标签最小宽度
        self.base_path_label.setMinimumWidth(50)
        self.path_template_label.setMinimumWidth(50)
        self.date_format_label.setMinimumWidth(50)
        self.whitelist_label.setMinimumWidth(50)

        self.layout.addLayout(self.form_layout)

    def choose_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "选择文件夹", self.base_path_input.text()
        )
        if folder_path:
            self.config.base_path = folder_path
            self.base_path_input.setText(folder_path)

    def set_path_template(self, text):
        self.config.path_template = text

    def set_date_format(self, text):
        self.config.date_format = text

    def remove_whitelist_item(self, item):
        self.config.whitelist.remove(self.config.whitelist[self.whitelist.row(item)])
        self.whitelist.takeItem(self.whitelist.row(item))

    def show_add_whitelist_dialog(self):
        dialog = AddWhitelistDialog(self)
        dialog.show()

    def add_whitelist_item(self, user):
        self.config.whitelist.append(user)
        self.whitelist.addItem(user.get("nickname", "未知用户"))

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "提示",
            "确认退出吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()