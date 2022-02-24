import re
from copy import copy

from PyQt5 import QtCore, QtWidgets


def set_msg(msg_label, text_in='必填项未填写'):
    """
    设置提示
    :param msg_label:
    :param text_in:
    :return:
    """
    msg_label.setText(text_in)
    if type(msg_label) is QtWidgets.QLabel:
        msg_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
        msg_label.setStyleSheet("color:red")


def clear_msg(msg_label):
    """
    清除提示
    :param msg_label:
    :return:
    """
    msg_label.setText('')
    msg_label.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgba(255, 170, 170, 0.3);')


def is_must_check(tab_data, in_dict: dict, text_label_dict: dict, is_disable=False):
    """
    必选检查
    :param tab_data: 数据保存的dict
    :param in_dict: {obj_name:{label:内容1}}
    :param text_label_dict: {obj_name:{label:内容2}}
    :param is_disable:
    """
    # 模块名称
    obj_name = list(in_dict.keys())[0]
    # 子类数据
    val_data = list(in_dict.values())[0]
    labal_name = list(val_data.keys())[0]
    labal_val = list(val_data.values())[0]

    # 保存的数据
    rec_dict = tab_data.data['rec_info']
    val_dict = rec_dict.get(obj_name, {})

    msg_label_dict = text_label_dict.get(obj_name)
    if msg_label_dict is None:
        msg_value = ''
    else:
        msg_label = msg_label_dict.get(labal_name)
        if msg_label is None:
            msg_value = ''
        else:
            msg_value = msg_label.text()

        # if msg_label is QtWidgets.QLabel:
        #     msg_value = msg_label.text()
        # elif msg_label is QtWidgets.QPushButton:
        #     msg_value = msg_label.text()
    if is_disable:
        # if isinstance(msg_label, QtWidgets.QLineEdit) or isinstance(msg_label, QtWidgets.QListView):
        msg_val_save = val_dict.get(labal_name.strip('*'))
        if msg_val_save is not None:
            labal_val = msg_val_save[0]
        # print(labal_val)
    else:
        if '*' in labal_name:
            if labal_val == '' or labal_val == '元' or ('签约期' in labal_name and labal_val in ('年', '季度', '月')):
                set_msg(msg_label, '必填项未填写')

            elif '必填项未填写' in msg_value:
                clear_msg(msg_label)
                msg_value = ''
            elif '联系方式' in labal_name:
                if len(labal_val) < 11:
                    set_msg(msg_label, '号码不足11位，请检查')
                else:
                    set_msg(msg_label, '')

    if '项目名称' in labal_name:
        re_rule = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        labal_val = re.sub(re_rule, "_", labal_val.replace('\n', ''))  # 替换为下划线

    val_dict.update({labal_name.strip('*'): [labal_val, msg_value]})
    rec_dict.update({obj_name: val_dict})
    # tab_data.save()  # 历史记录

    # print(rec_dict)


def number_clear(s: str):
    o = ''
    for index, c in enumerate(s):
        if index == 0:
            if c == '.':
                o += '0'
        if c.isdigit() or c == '.':
            o += c
    return o


def ct_calc(is_able_label, tab_data, in_dict, msg_dict):
    """
    ct部分计算
    :param is_able_label: 需要禁止输入的label
    :param tab_data: 数据dict
    :param in_dict: {obj_name:{label:内容1}}
    :param msg_dict: {obj_name:{label:内容2}}
    """
    # 模块名称
    is_must_check(tab_data, in_dict, msg_dict)
    obj_name = list(in_dict.keys())[0]
    rec_dict = tab_data.data['rec_info']
    val_dict = rec_dict.get(obj_name, {})
    # 内容2 CT收入≥CT成本是否满足的控件
    msg_dict_last = list(msg_dict.values())[0]
    data_key = list(msg_dict_last.keys())[-1]
    msg_label = msg_dict.get(obj_name).get(data_key)
    # msg_value = msg_label.text()

    ct_cb_c = val_dict.get('CT成本', [False])[0]
    ct_sr_c = val_dict.get('CT收入', [False])[0]
    ct_cb = copy(ct_cb_c)
    ct_sr = copy(ct_sr_c)

    if not ct_cb or not ct_sr:
        ct_msg = ''
        ct_msg_2 = ''
    else:
        ct_cb = number_clear(ct_cb)
        ct_sr = number_clear(ct_sr)
        try:
            compare = float(ct_cb) <= float(ct_sr)
        except Exception as e:
            print(e)
            compare = False
        if compare:
            ct_msg = '是'
            ct_msg_2 = 'CT建设符合要求'
        else:
            ct_msg = '否'
            ct_msg_2 = 'CT建设不符合要求，该项目无法上会'
        val_dict.update({'CT成本': [ct_cb_c, '']})
        val_dict.update({'CT收入': [ct_sr_c, '']})

    if msg_label is not None or ct_msg_2 != '':
        is_able_label[-1].setText(ct_msg)
        msg_label.setText(ct_msg_2)
        val_dict.update({data_key.strip('*'): [ct_msg, ct_msg_2]})
        rec_dict.update({obj_name: val_dict})

    return tab_data


def ct_check(btn, tab_data, label_list, msg_dict):
    """
    CT选择check
    """
    checked_btn = btn.checkedButton()
    # 模块名称
    obj_name = list(msg_dict.keys())[0]
    # 子类数据
    val_data = list(msg_dict.values())[0]
    data_key = list(val_data.keys())[0]
    msg_val = list(val_data.values())
    data_val = checked_btn.text()

    # 获取保存的数据
    rec_dict = tab_data.data['rec_info']
    val_dict = rec_dict.get(obj_name, {})

    if data_val == '是':
        for i in label_list:
            i.setDisabled(False)
            # i.in_signal.connect(lambda in_dict: is_must_check(tab_data, in_dict, msg_dict))

    if checked_btn.text() == '否':
        for i in label_list:
            i.setDisabled(True)
            # 清除保存的数据
            val_dict = {}
            i.setText('')
            for msg_l in msg_val:
                if msg_l is not None:
                    clear_msg(msg_l)
            # i.in_signal.disconnect(lambda in_dict: is_must_check(tab_data, in_dict, msg_dict))
            # try:
            #     i.in_signal.disconnect()
            # except Exception as e:
            #     print(e)

    val_dict.update({data_key.strip('*'): [data_val, '']})
    rec_dict.update({obj_name: val_dict})


def per_calc(pay_dict, tab_data, obj_name, t_msg_dict):
    """
    维护费信息计算
        1.若维护费占比≥10%，自动提示：符合维护费用比例要求；
        2.若10%>维护费占比≥5%，自动提示：不符合维护费用比例要求，建议提高维护费比例至10%，增强对维护单位的约束力；
        3.若5%>维护费占比>0%，自动提示：维护费用严重不足，建议提高维护费比例至10%，增强对维护单位的约束力；
        4.若维护费占比=0%，自动提示：本项目无维护无质保，建议该项目无需交维；
    :param is_able_label:
    :param tab_data:
    :param in_dict: {obj_name:{label:内容1}}
    :param msg_dict: {obj_name:{label:内容2}}
    """
    # 模块名称
    msg_dict = {obj_name: t_msg_dict}
    # print(t_msg_dict)
    for lb_name, lb_wd in pay_dict.items():
        if lb_wd.text() != '':
            is_must_check(tab_data, {obj_name: {lb_name: lb_wd.text()}}, msg_dict)
        elif lb_name != '维护费占比':
            set_msg(t_msg_dict[lb_name])
    rec_dict = tab_data.data['rec_info']
    val_dict = rec_dict.get(obj_name, {})
    # 内容2的控件
    data_key1 = '维护费占比1'
    data_key = '维护费占比'
    msg_label1 = msg_dict.get(obj_name, {}).get(data_key1, {})
    msg_label = msg_dict.get(obj_name, {}).get(data_key, {})
    msg_value = msg_label.text()
    msg_value_2 = ''

    it_all = pay_dict.get('IT总投入*', False).text().strip('元')
    it_tetention = pay_dict.get('质保金*', False).text().strip('元')
    it_repairs = pay_dict.get('维护费*', False).text().strip('元')
    # print(it_all, it_tetention, it_repairs)
    if not it_all or not it_repairs or not it_tetention:
        it_repairs_persent = ''
        msg_value_2 = ''
        clear_msg(msg_label)
        clear_msg(msg_label1)

    else:
        it_repairs = number_clear(it_repairs)
        it_tetention = number_clear(it_tetention)
        it_all = number_clear(it_all)
        try:
            it_repairs_persent = (float(it_repairs) + float(it_tetention)) / float(it_all)
        except Exception as e:
            msg_value_2 = '数据异常：{}'.format(e)
            it_repairs_persent = -1
        if it_repairs_persent >= 0.1:
            msg_value_2 = '符合维护费用比例要求'
        elif 0.1 > it_repairs_persent >= 0.05:
            msg_value_2 = '不符合维护费用比例要求，建议提高维护费比例至10%，增强对维护单位的约束力'
        elif 0.05 > it_repairs_persent > 0:
            msg_value_2 = '维护费用严重不足，建议提高维护费比例至10%，增强对维护单位的约束力'
        elif it_repairs_persent == 0:
            msg_value_2 = '本项目无维护无质保，建议该项目无需交维'

    if msg_value is not None and msg_value_2 != '':
        # 得出结果后填入
        msg_label1.setText('{:.2%}'.format(it_repairs_persent))
        msg_label.setText(msg_value_2)
        val_dict.update({data_key.strip('*'): ['{:.2%}'.format(it_repairs_persent), msg_value_2]})
        rec_dict.update({obj_name: val_dict})

    return tab_data


def four_box_check(tab_data, obj_name, able_check_list, msg_dict):
    """
    CT选择check
    """
    tab_info_dict = tab_data.data['tab_info']

    # 模块名称
    for type_name, type_wd, type_msg in able_check_list:
        labal_val = type_wd.text()
        msg_value = type_msg.text()
        if '否' == labal_val or '无' == labal_val:
            # msg_label.setDisabled(False)
            msg_value = ''
            if isinstance(type_msg, QtWidgets.QComboBox):
                type_msg.clear()
            elif isinstance(type_msg, QtWidgets.QLineEdit):
                type_msg.setDisabled(True)
                type_msg.setText('')
        elif '有' == labal_val or '是' == labal_val:
            if msg_value == '':
                if isinstance(type_msg, QtWidgets.QComboBox):
                    for i in tab_info_dict[obj_name]:
                        if i['name'] == type_name.strip('*'):
                            type_msg.addItems(i['data'][1])
                            break
                elif isinstance(type_msg, QtWidgets.QLineEdit):
                    type_msg.setDisabled(False)
                    type_msg.setPlaceholderText('请填写必填项')
            # type_msg.setDisabled(True)

        is_must_check(tab_data, {obj_name: {type_name: labal_val}}, msg_dict)


def check_all(tab_data):
    """
    校验保存的数据
    :param tab_data: 保存的数据结构
    :return: [bool, text]: [是否通过, 校验报告]
    """
    save_data = tab_data.data
    save_name_list = save_data.tab_name
    save_check_dict = save_data.tab_info
    save_data_dict = save_data.rec_info
    data_list = []
    text_msg = []
    check_pass_flag = True

    for index, type_name in enumerate(save_name_list):
        check_list = save_check_dict.get(type_name)
        sub_msg = []
        # print(type_name, check_list)
        first_data = ''
        for c_index, check_data in enumerate(check_list):
            c_name = check_data['name']
            c_must = check_data.get('is_must')
            c_data = check_data.get('data')
            data = save_data_dict.get(type_name, {}).get(c_name, ['', ''])
            if c_index == 0:
                first_data = data[0]
                # print(first_data)
            # print(type_name, c_must, c_name, data)

            if c_must is None:
                c_name = list(save_data_dict.get(type_name, {}).keys())
                data = list(save_data_dict.get(type_name, {}).values())
                # print(type_name, c_must, c_name, data)
                if len(data) == 0:
                    sub_msg = ['统一审核建议']
                    data = [[], []]
                else:
                    c_name = c_name[0]
                    data = data[0]
                l1 = []
                data1 = save_data_dict.get('CT成本确认', {}).get('CT收入≥CT成本是否满足', ['', ''])[1]
                data2 = save_data_dict.get('维护费信息', {}).get('维护费占比', ['', ''])[1]
                if data1 != '':
                    l1.append(data1)
                if data2 != '':
                    l1.append(data2)
                data = [l1 + data[0], data[1]]
                # 同单元格输出全部
                if data[0] != '':
                    d = ['{}、{}'.format(i + 1, data[0][i]) for i in range(len(data[0]))]
                    data_list.append([index + 1, type_name, c_name, '\r\n'.join(d), ''])
                # for d in data[0]:  # 分单元格操作
                #     data_list.append([index + 1, type_name, c_name, d, ''])
                if data[1] != '':
                    data_list.append([index + 1, type_name, c_name, data[1], ''])
                break

            data_list.append([index + 1, type_name, c_name] + data)
            if isinstance(c_must, list):
                for index_2, must_flag in enumerate(c_must):
                    if must_flag:
                        if data[index_2] == '' and (data[0] != '否' and data[0] != '无'):
                            sub_msg.append(c_name)
            else:
                if c_must:
                    if c_data == 'phone':
                        if len(data[0]) != 11:
                            sub_msg.append('{}: 号码不足11位，请检查'.format(c_name))
                            continue
                    if data[0] == '' and (first_data != '否' and first_data != '无'):
                        sub_msg.append(c_name)
        text_msg.append([type_name, sub_msg])
    res_text = '以下项目未填写，请检查：'
    index = 1
    for type_name, type_sub in text_msg:
        if len(type_sub) > 0:
            res_text += '\r\n{}:{}\r\n\t'.format(index, type_name)
            res_text += '\r\n\t'.join(type_sub)
            check_pass_flag = False
        index += 1
    if check_pass_flag:
        res_text = ''
    return check_pass_flag, res_text, data_list
