import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator

from config import *
from gui_config import tab_config, QLineEdit, QComboBox, QLabel, tab_data, set_cale, update_tab_data, QPlainTextEdit, \
    MultiTextEdit
from gui_data_check import ct_calc, ct_check, per_calc, is_must_check


def buttonLayoutGen():
    button_layout = QtWidgets.QHBoxLayout()

    # button_wd_left = QtWidgets.QWidget()
    button_layout_left = QtWidgets.QHBoxLayout()
    # 添加伸缩
    # button_wd_left.setLayout(button_layout_left)

    button_reset = QtWidgets.QPushButton('重 置')
    button_reset.setFixedWidth(69)
    button_layout_left.setSpacing(10)
    button_layout_left.addWidget(button_reset)
    button_layout_left.addStretch()

    # button_wd_right = QtWidgets.QWidget()
    button_layout_right = QtWidgets.QHBoxLayout()
    # 添加伸缩
    # button_wd_right.setLayout(button_layout_right)
    button_layout_right.addStretch()

    button_prov = QtWidgets.QPushButton('上一页')
    button_prov.setFixedWidth(75)
    button_next = QtWidgets.QPushButton('下一页')
    button_next.setFixedWidth(75)

    blank_wdt = QtWidgets.QWidget()
    blank_wdt.setFixedWidth(60)

    button_submit = QtWidgets.QPushButton('导 出')
    button_submit.setFixedWidth(85)

    button_layout_right.setSpacing(10)
    button_layout_right.addWidget(button_prov)
    button_layout_right.addWidget(button_next)
    button_layout_right.addWidget(blank_wdt)
    button_layout_right.addWidget(button_submit)

    button_layout.addLayout(button_layout_left)
    button_layout.addLayout(button_layout_right)

    return button_layout, [button_prov, button_next, button_submit, button_reset]


def get_d(tab_data, obj_name, type_wd, type_msg, type_btn, level_data):
    """
    绑定匹配按钮
    """
    p_name = type_wd.text()
    if p_name != '':
        level_set = level_data[level_data['客户名称'] == p_name]['客户服务等级'].values
        if len(level_set) != 0:
            set_border(type_msg)
            type_msg.setText(level_set[0])
            type_msg.setEnabled(False)
            type_msg.setPlaceholderText('')
            tab_data.data['rec_info'][obj_name].update({'客户服务等级': [p_name, level_set[0]]})
        else:
            type_btn.setText('未找到匹配项')
            type_msg.setEnabled(True)
            type_msg.setPlaceholderText('请在此处手动输入等级')


def set_border(type_msg):
    """
    设置边框
    """
    if not isinstance(type_msg, QLineEdit):
        type_msg.setFrameShape(QtWidgets.QFrame.Box)
        type_msg.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        type_msg.setFrameShape(QtWidgets.QFrame.Box)
    # 设置边框样式
    # 设置背景填充颜色 'background-color: rgb(0, 0, 0)'
    # 设置边框颜色border-color: rgb(255, 170, 0);
    type_msg.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgba(255, 170, 170, 0.4);')
    # 调整文字与边框的对齐，可以多试几个参数，比如AlignTop
    type_msg.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
    return type_msg


def set_base_widget(type_name, self=None):
    """
    设置基本三列控件
    | 类型 | 内容1 | 内容2 |
    | QLabel | QWidgets1 | QWidgets2 |
    三列框类型
    """

    type_label = QtWidgets.QLabel(type_name)
    type_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    type_label.setFixedWidth(180)

    type_wd = None

    type_msg = QtWidgets.QLabel('')
    # if self is None:
    #     # type_msg.setFixedWidth(self.tabWidget.width()//3)
    #     type_msg.setFixedWidth(320)
    # if self is not None:
    #     type_msg.setFixedWidth(self.tabWidget.width()//3)
    #     # type_msg.setFixedWidth(320)
    # else:
    #     type_msg.setFixedWidth(320)

    type_msg.setFixedWidth(320)
    type_msg.setFixedHeight(27)

    set_border(type_msg)
    return type_label, type_wd, type_msg


def tabLayoutGenerate(self, obj_name):
    """

    :param self:
    :param obj_name:
    :return:
    """
    input_list = []
    msg_dict = {}
    # 创建tab中的布局
    tab_layout = QtWidgets.QGridLayout()
    tab_layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    tab_layout.setSpacing(8)
    # 读取表格配置
    obj_config = tab_config.get('tab_info').get(obj_name)

    for index, data_type_dict in enumerate(obj_config):
        type_name = data_type_dict.get('name')
        wd_type = data_type_dict.get('type')
        wd_data = data_type_dict.get('data')
        wd_must = data_type_dict.get('is_must')
        if wd_must:
            type_name = type_name + '*'

        # 三列显示类型
        type_label, type_wd, type_msg = set_base_widget(type_name, self)

        if wd_type == 0:
            type_wd = QLineEdit()
            type_wd.setObjectName(type_name)
        elif wd_type == 1:
            type_wd = QComboBox()
            type_wd.setObjectName(type_name)
            type_wd.addItems(wd_data)
        elif wd_type == 5:
            tab_layout.addWidget(type_label, index, 0)
            # cale_msg = QLabel()
            # cale_msg.setObjectName(type_name)
            cale_wd = QtWidgets.QDateTimeEdit(QtCore.QDate.currentDate())
            cale_wd.setDisplayFormat('yyyy-MM-dd')
            cale_wd.setCalendarPopup(True)
            cale_wd.setObjectName(type_name)
            # tab_layout.addWidget(QtWidgets.QLabel(), index + 1, 0)
            # tab_layout.addWidget(cale_msg, index, 1, 1, 2)
            tab_layout.addWidget(cale_wd, index, 1)
            tab_layout.addWidget(type_msg, index, 2)
            set_cale(tab_data, obj_name, cale_wd)

            cale_wd.dateChanged.connect(lambda date: set_cale(tab_data, obj_name, cale_wd))
            type_msg = None

        elif wd_type == 30:
            type_wd_l = MultiTextEdit(type_name, obj_name, wd_data)
            type_wd = type_wd_l.type_wd

        if wd_data == 'compare':
            type_wd.setPlaceholderText("请输入客户名称")
            file_path = os.path.join(cur_path, '客户服务等级.xls')

            type_btn = QtWidgets.QPushButton()
            type_btn.setText('点击查找')
            type_btn.setStyleSheet('border-width: 2px;border-style: solid;border-color: rgb(255, 170, 170);')
            type_msg = QLineEdit()
            type_msg.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
            type_btn.setFixedWidth(125)
            type_btn.setFixedHeight(25)

            # 按钮控件
            type_wdl = QtWidgets.QHBoxLayout()
            # type_wd = QtWidgets.QWidget(wd_layout)
            type_wdl.addWidget(type_msg)
            type_wdl.addWidget(type_btn)
            type_wdl.setContentsMargins(0, 0, 0, 0)
            # 创建控件并设置布局
            type_wd2 = QtWidgets.QWidget()
            type_wd2.setObjectName(obj_name)
            type_wd2.setLayout(type_wdl)
            type_wd2.setFixedHeight(25)

            if not os.path.exists(file_path):
                file_path = os.path.join(base_path, 'img', '客户服务等级.xls')

            if os.path.exists(file_path):
                level_data = pd.read_excel(file_path, engine='xlrd')
                level_data = level_data[['客户名称', '客户服务等级']]
                completer = QtWidgets.QCompleter(level_data['客户名称'].to_list())
                type_wd.setCompleter(completer)

                type_msg.setEnabled(False)
                set_border(type_msg)
                type_msg.textChanged.connect(lambda: update_tab_data(tab_data, obj_name, type_name, type_msg.text(), 1))
                # type_wd2.setFixedWidth(200)

                type_btn.clicked.connect(lambda clicked: get_d(tab_data, obj_name, type_wd, type_msg, type_btn, level_data))

            else:
                type_btn.setText('未找到等级数据')
                type_msg.setEnabled(True)

            tab_layout.addWidget(type_label, index, 0)  # i行 0列
            tab_layout.addWidget(type_wd, index, 1)
            tab_layout.addWidget(type_wd2, index, 2)
            input_list.append(type_wd)
            msg_dict.update({type_name: type_msg})

            # type_msg = None
            continue

        if wd_data == 'phone':
            reg_exp = QtCore.QRegExp(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$')
            # 实例化自定义校验器
            phone_validator = QRegExpValidator(reg_exp)
            type_wd.setValidator(phone_validator)

        if type_wd is None:
            continue

        if type_msg is not None:
            tab_layout.addWidget(type_label, index, 0)  # i行 0列
            tab_layout.addWidget(type_wd, index, 1)
            type_msg.setObjectName(type_name)
            tab_layout.addWidget(type_msg, index, 2)
            input_list.append(type_wd)
            msg_dict.update({type_name: type_msg})

    return tab_layout, input_list, msg_dict


def tabLayoutGenerate_2(self, obj_name):
    """
    tab2控件
    :param obj_name:
    :return:
    """
    yes_btn = None
    input_list = []
    is_able_label = []
    msg_dict = {}
    # 创建tab中的布局
    tab_layout = QtWidgets.QGridLayout()
    tab_layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    tab_layout.setSpacing(8)
    # 读取表格配置
    obj_config = tab_config.get('tab_info').get(obj_name)

    for index, data_type_dict in enumerate(obj_config):
        type_name = data_type_dict.get('name')
        wd_type = data_type_dict.get('type')
        wd_data = data_type_dict.get('data')
        wd_must = data_type_dict.get('is_must')
        if wd_must:
            type_name = type_name + '*'

        type_label, type_wd, type_msg = set_base_widget(type_name)

        if wd_type == 0:
            type_wd = QLineEdit()
            type_wd.setObjectName(type_name)
            type_wd.setDisabled(True)
            input_list.append(type_wd)
        elif wd_type == 1:
            type_wd = QComboBox()
            type_wd.setObjectName(type_name)
            type_wd.addItems(wd_data)
        elif wd_type == 3:
            type_wd = QtWidgets.QWidget()
            type_wdl = QtWidgets.QHBoxLayout()

            type_wd.setLayout(type_wdl)
            btn_g = QtWidgets.QButtonGroup()
            yes_btn = QtWidgets.QRadioButton('是')
            no_btn = QtWidgets.QRadioButton('否')
            no_btn.setChecked(True)
            btn_g.addButton(yes_btn, 1)
            btn_g.addButton(no_btn, 2)
            type_wdl.addWidget(yes_btn)
            type_wdl.addWidget(no_btn)
            type_wdl.addStretch()
            tab_layout.addWidget(type_wd, index, 1)

            type_wd = None
            type_msg = None

        elif wd_type == 4:
            type_wd = QPlainTextEdit()
            type_wd.setObjectName(type_name)
            # type_wd.setVisible(False)
            # type_wd.setWordWrap(True)
            type_wd.setFixedHeight(55)
            input_list.append(type_wd)
            tab_layout.addWidget(type_label, index, 0)  # i行 0列
            tab_layout.addWidget(type_wd, index, 1, 2, 2)
            continue

        elif wd_type == 30:
            # 创建输入框
            m_edit = MultiTextEdit(type_name, obj_name, wd_data)
            m_edit.setDisabled(True)
            is_able_label.append(m_edit)
            type_wd = m_edit.type_wd
            if wd_data == '元':
                double_validator = QDoubleValidator(0, 100000000000, 2)
                double_validator.setNotation(QDoubleValidator.StandardNotation)
                m_edit.setValidator(double_validator)

        elif wd_type == 31:
            type_wd = QLabel()
            set_border(type_wd)
            # type_wd.setDisabled(True)
            type_wd.setObjectName(type_name)
            is_able_label.append(type_wd)

        # if type_wd is None:
        #     continue

        tab_layout.addWidget(type_label, index, 0)  # i行 0列
        tab_layout.addWidget(type_wd, index, 1)
        tab_layout.addWidget(type_msg, index, 2)

        # input_list.append(type_wd)
        msg_dict.update({type_name: type_msg})

    for i in is_able_label:
        i.in_signal.connect(lambda in_dict: ct_calc(is_able_label, tab_data, in_dict, {obj_name: msg_dict}))
        i.in_signal.connect(lambda in_dict: is_must_check(tab_data, in_dict, {obj_name: msg_dict}))

    ct_check(btn_g, tab_data, input_list + is_able_label, {obj_name: msg_dict})
    yes_btn.toggled.connect(lambda: ct_check(btn_g, tab_data, input_list + is_able_label, {obj_name: msg_dict}))
    # no_btn.toggled.connect(lambda : ct_check(btn_g, tab_data, input_list + is_able_label, {obj_name: msg_dict}))
    return tab_layout, input_list, msg_dict


def tabLayoutGenerate_3(self, obj_name):
    """
    tab3控件
    """
    input_list = []
    pay_dict = {}
    msg_dict = {}
    # 创建tab中的布局
    tab_layout = QtWidgets.QGridLayout()
    tab_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    tab_layout.setSpacing(8)
    # 读取表格配置
    obj_config = tab_config.get('tab_info').get(obj_name)

    for index, data_type_dict in enumerate(obj_config):
        type_name = data_type_dict.get('name')
        wd_type = data_type_dict.get('type')
        wd_data = data_type_dict.get('data')
        wd_must = data_type_dict.get('is_must')
        if wd_must:
            type_name = type_name + '*'

        type_label, type_wd, type_msg = set_base_widget(type_name)
        # type_msg.setFixedWidth(380)

        if wd_type == 0:
            type_wd = QLineEdit()
            type_wd.setObjectName(type_name)
            input_list.append(type_wd)

        elif wd_type == 30:
            # 创建输入框
            m_edit = MultiTextEdit(type_name, obj_name, wd_data)
            pay_dict.update({type_name: m_edit})
            m_edit.textChanged.connect(lambda: per_calc(pay_dict, tab_data, obj_name, msg_dict))
            m_edit.in_signal.connect(lambda in_dict: is_must_check(tab_data, in_dict, {obj_name: msg_dict}))
            type_wd = m_edit.type_wd
            if wd_data == '元':
                double_validator = QDoubleValidator(0, 100000000000, 2)
                double_validator.setNotation(QDoubleValidator.StandardNotation)
                m_edit.setValidator(double_validator)

        elif wd_type == 31:
            type_wd = QLabel()
            set_border(type_wd)
            type_msg.setFixedHeight(self.width//11)
            type_wd.setObjectName(type_name)

            msg_dict.update({'{}1'.format(type_name): type_wd})
            pay_dict.update({type_name.strip('*'): m_edit})
            type_msg.setWordWrap(True)  # 自动换行

        tab_layout.addWidget(type_label, index, 0)  # i行 0列
        tab_layout.addWidget(type_wd, index, 1)
        tab_layout.addWidget(type_msg, index, 2)

        msg_dict.update({type_name: type_msg})

    return tab_layout, input_list, msg_dict
