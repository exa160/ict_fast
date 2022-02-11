from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QCheckBox, QListWidgetItem

from gui_config import QLineEdit, QComboBox, QListWidget, get_check_box, QPlainTextEdit, set_check_box, set_add_data
from gui_data_check import four_box_check, is_must_check
from gui_subtable import tab_config, tab_data, set_base_widget, set_border


def tabLayoutGenerate_4(self, obj_name):
    """
    tab4控件
    """
    input_list = []
    is_able_label = []
    msg_dict = {}
    # 创建tab中的布局
    tab_layout = QtWidgets.QGridLayout()
    tab_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    tab_layout.setSpacing(8)
    # 读取表格配置
    obj_config = tab_config.get('tab_info').get(obj_name)

    able_check_list = []  # 单独传入函数判断
    for index, data_type_dict in enumerate(obj_config):
        type_name = data_type_dict.get('name')
        wd_type_list = data_type_dict.get('type')
        wd_data_list = data_type_dict.get('data')
        wd_must_list = data_type_dict.get('is_must')

        if True in wd_must_list:
            type_name = type_name + '*'

        type_label, type_wd, type_msg = set_base_widget(type_name)

        wd_list = []
        for wd_type, wd_data, wd_must in list(zip(*[wd_type_list, wd_data_list, wd_must_list])):

            # type_msg.setFixedWidth(380)

            if wd_type == 0:
                type_wd = QLineEdit()
                type_wd.setObjectName(type_name)
                if wd_must:
                    type_wd.setPlaceholderText('请填写必填项')
                # input_list.append(type_wd)
                if wd_data != '':
                    completer = QtWidgets.QCompleter([wd_data])
                    type_wd.setCompleter(completer)

            elif wd_type == 1:
                type_wd = QComboBox()
                type_wd.setObjectName(type_name)
                if not wd_must:
                    wd_data = [''] + wd_data
                type_wd.addItems(wd_data)

                # type_wd.setVisible()

            elif wd_type == 2:
                type_wd = QLineEdit()
                type_wd.setObjectName(type_name)
                type_wd.setVisible(False)
                wd_list.append(type_wd)

                # type_wd.textChanged.connect(lambda: type_wd.clearFocus())
                continue
                # input_list.append(type_wd)

            elif wd_type == 4:
                type_wd = QPlainTextEdit()
                type_wd.setObjectName(type_name)
                # type_wd.setVisible(False)
                # type_wd.setWordWrap(True)
                type_wd.setFixedHeight(55)
                # type_wd.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

            wd_list.append(type_wd)

        tab_layout.addWidget(type_label, index, 0)  # i行 0列
        if len(wd_list) == 1:
            # continue
            tab_layout.addWidget(wd_list[0], index, 1, 2, 2)
            input_list.append(wd_list[0])
        elif len(wd_list) == 2:
            type_wd = wd_list[0]
            type_msg = wd_list[1]
            tab_layout.addWidget(type_wd, index, 1)
            tab_layout.addWidget(type_msg, index, 2)
            msg_dict.update({type_name: type_msg})
            able_check_list.append([type_name] + wd_list)
            if len(wd_data_list[0]) == 2:
                type_wd.currentTextChanged.connect(
                    lambda in_dict: four_box_check(tab_data, obj_name, able_check_list, {obj_name: msg_dict}))
                type_wd.in_signal.connect(
                    lambda in_dict: is_must_check(tab_data, in_dict, {obj_name: msg_dict}, is_disable=True))
                type_msg.in_signal.connect(
                    lambda in_dict: is_must_check(tab_data, in_dict, {obj_name: msg_dict}, is_disable=True))

            else:
                # type_wd.setDisabled(False)
                input_list.append(type_wd)
            # input_list.append(type_msg)
    # for i in input_list:
    #     i.in_signal.connect(lambda in_dict: per_calc(is_able_label, tab_data, in_dict, {obj_name: msg_dict}))

    return tab_layout, input_list, msg_dict


def tabLayoutGenerate_5(self, obj_name):
    """
    tab5控件
    """
    input_list = []
    msg_dict = {}
    # 创建tab中的布局
    tab_layout = QtWidgets.QGridLayout()
    tab_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    tab_layout.setSpacing(8)
    # 读取表格配置
    obj_config = tab_config.get('tab_info').get(obj_name)

    title_label = QtWidgets.QLabel('项目类型*')
    # check_label = QtWidgets.QLabel('统一审核建议*')
    tab_layout.addWidget(title_label, 0, 0)
    # tab_layout.addWidget(check_label, 0, 1)

    list_wd = QListWidget()
    list_msg = QListWidget()
    list_msg2 = QPlainTextEdit()

    project_dict = {}

    for index, data_type_dict in enumerate(obj_config):
        type_name = data_type_dict.get('name')
        wd_type = data_type_dict.get('type')
        wd_data = data_type_dict.get('data')
        # wd_must = data_type_dict.get('is_must')
        # if wd_type
        project_dict.update({type_name: wd_data})

    box_list = []
    for i in project_dict.keys():
        box = QCheckBox('{}'.format(i))  # 实例化一个QCheckBox
        box.setObjectName(i)
        item = QListWidgetItem()  # 实例化一个Item，QListWidget，不能直接加入QCheckBox
        list_wd.addItem(item)  # 把QListWidgetItem加入QListWidget
        list_wd.setItemWidget(item, box)  # 再把QCheckBox加入Q
        box_list.append(box)
        box.stateChanged.connect(lambda iw: get_check_box(tab_data, obj_name, list_msg, list_msg2, box_list, project_dict))
    # list_wd.itemClicked.connect(lambda iw: getChoose(list_wd))

    msg_tab = QtWidgets.QTabWidget()
    msg_tab.addTab(list_msg, '统一审核建议*')

    msg_tab.addTab(list_msg2, '补充审核建议')
    list_wd.itemClicked.connect(lambda: set_check_box(list_wd, box_list))
    list_msg2.in_signal.connect(lambda: set_add_data(tab_data, list_msg2, obj_name, ''))
    list_msg.itemClicked.connect(lambda l: print(l))
    tab_layout.addWidget(list_wd, 1, 0, 1, 1)
    tab_layout.addWidget(msg_tab, 0, 1, 2, 3)
    tab_layout.setColumnStretch(1, 3)  # 前后1：2
    # for i in input_list:
    #     i.in_signal.connect(lambda in_dict: per_calc(is_able_label, tab_data, in_dict, {obj_name: msg_dict}))

    return tab_layout, input_list, msg_dict
