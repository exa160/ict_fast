"""
type:
0 QLineEdit
1 QComboBox
"""
import os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QCheckBox, QListWidgetItem

from config import cur_path, ConfigAttrDict
from gui_data_check import is_must_check

"""
'type': 0 : QLineEdit
'type': 1 : QComboBox
'type': 2 : QLineEdit divisible
'type': 3 : RedioButton
'type': 4 : QLineEdit large
'type': 5 : QCalendarWidget
'type': 30: lineedit+label
'type': 31: msg label
"""
tab_config = {
    "tab_name": ['项目基础信息', 'CT成本确认', '维护费信息', '业主侧维护及考核要求', '项目类型', '审核留痕'],
    'tab_info': {
        '项目基础信息': [
            {'name': '项目编号', 'is_must': False, 'type': 0, 'data': ''},
            {'name': '项目名称', 'is_must': True, 'type': 0, 'data': ''},
            {'name': '县市', 'is_must': True, 'type': 1,
             'data': ['市本级', '婺城', '金东', '义乌', '东阳', '永康', '武义', '浦江', '兰溪', '磐安']},
            {'name': '县市政企项目经理', 'is_must': True, 'type': 0, 'data': ''},
            {'name': '项目经理联系方式', 'is_must': True, 'type': 0, 'data': 'phone'},
            {'name': '签约期', 'is_must': True, 'type': 0, 'data': ''},
            {'name': '客户服务等级', 'is_must': [True, True], 'type': 0, 'data': 'compare'},
        ],
        'CT成本确认': [
            {'name': '项目是否含CT', 'is_must': True, 'type': 3, 'data': ['是', '否']},
            {'name': 'CT成本', 'is_must': True, 'type': 30, 'data': 'yuan'},
            {'name': 'CT收入', 'is_must': True, 'type': 30, 'data': 'yuan'},
            {'name': 'CT成本签字人员', 'is_must': True, 'type': 0, 'data': ''},
            {'name': 'CT收入≥CT成本是否满足', 'is_must': False, 'type': 31, 'data': ''},
            {'name': '备注', 'is_must': False, 'type': 4, 'data': ''},
        ],
        '维护费信息': [
            {'name': 'IT总投入', 'is_must': True, 'type': 30, 'data': 'yuan'},
            {'name': '质保金', 'is_must': True, 'type': 30, 'data': 'yuan'},
            {'name': '维护费', 'is_must': True, 'type': 30, 'data': 'yuan'},
            {'name': '维护费占比', 'is_must': False, 'type': 31, 'data': ''},
        ],
        '业主侧维护及考核要求': [
            {'name': '服务承诺', 'is_must': [True, True], 'type': [1, 0], 'data': [['有', '无'], '7*24小时热线服务']},
            {'name': '故障处理时限是否明确', 'is_must': [True, True], 'type': [1, 1], 'data': [['是', '否'],
                                                                                     ['故障于2小时内解决',
                                                                                      '故障于4小时内解决',
                                                                                      '故障于6小时内解决',
                                                                                      '故障于8小时内解决',
                                                                                      '故障于12小时内解决',
                                                                                      '故障于18小时内解决',
                                                                                      '故障于24小时内解决',
                                                                                      '故障于48小时内解决']]},
            {'name': '故障处理书面报告是否需要提供', 'is_must': [True, True], 'type': [1, 1], 'data': [['是', '否'],
                                                                                         ['1个工作日',
                                                                                          '2个工作日',
                                                                                          '3个工作日',
                                                                                          '4个工作日',
                                                                                          '5个工作日',
                                                                                          '6个工作日',
                                                                                          '7个工作日']]},
            {'name': '日常巡检是否需要提供', 'is_must': [True, True], 'type': [1, 1], 'data': [['是', '否'], ['每日一次',
                                                                                                  '每周一次',
                                                                                                  '每半月一次',
                                                                                                  '每月一次',
                                                                                                  '每季度一次',
                                                                                                  '每半年一次',
                                                                                                  '每年一次']]},
            {'name': '设备/点位在线率要求', 'is_must': [False, False], 'type': [1, 2], 'data': [['100%', '98%',
                                                                                        '95%', '90%',
                                                                                        '85%', '80%'], []]},
            {'name': '备品备件需求是否明确', 'is_must': [True, True], 'type': [1, 0], 'data': [['是', '否'], '摄像头备件']},
            {'name': '维护界面是否清晰', 'is_must': [True, True], 'type': [1, 0], 'data': [['是', '否'], '取电问题由客户负责，其他维护全部由乙方负责']},
            {'name': '考核方式是否明确', 'is_must': [True, True], 'type': [1, 0], 'data': [['是', '否'], '每年12月底取数，在线率低于95%，每低于1个百分点，扣除本年底1/45的维护款']},
            {'name': '补充说明', 'is_must': [False], 'type': [4], 'data': ['']},
        ],
        '项目类型': [{'name': '视频监控',
                  'data': ['建议在前后向合同中写明取电、道路改造、设备拆移机等非自身原因造成的维护责任归属问题',
                           '项目建设摄像头、交换机、硬盘、光收发器等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                           '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责',
                           '若项目为监管类项目（透明药房、阳光厨房等），容易受到人为或不可控原因导致业务中断（离线、损坏等），建议项目预留10~20%的风险金',
                           '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '视频监控（公安）',
                  'data': [
                      '若项目内建设点位纳入公安健康度考核，建议在后向合同的维护条款和考核内容中写明维护单位每日线上巡检、及时修复，并将扣分原因反馈给区县公安视频监控负责人，非维护不力造成的考核扣分需及时向公安报备',
                      '若项目建设点位有破路取电、老旧小区改造、设备拆移机等风险，建议项目预留10~20%的风险金',
                      '公安视频监控有较高的健康度考核指标（要求：99%以上），建议项目内提供不低于3%的备品备件（摄像头、交换机、光收发器、硬盘等），在前后向合同中写明备品备件需求说明',
                      '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）',
                      '项目有驻点人员要求，建议前后向合同中明确驻点人员的数量及工作职责，若驻点人员的工作内容与项目无关，其驻点人员费用不能计入IT维护费用中',
                      '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责',
                      '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                      '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                      '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': 'WLAN',
                  'data': ['建议项目建设AP上线后，AP名称修改为其覆盖楼层，同时做好三层拓扑、IP规划、项目建设详单、CAD图纸等资料整理归档工作',
                           '项目建设AP、交换机、外置天线等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                           '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）',
                           '为便于后期设备的检修，建议项目施工建设过程中预留充足的检修口',
                           '建议在前后向合同中写明设备拆移机等非自身原因造成的维护责任归属问题',
                           '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '软件开发',
                  'data': ['若项目的软件开发有公网出口，建议在售中阶段公网出口及时进行ICP备案和定级备案',
                           '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                           '该项目为软件开发类项目，在验收合格后需与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等的问题',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '5G',
                  'data': ['若项目为5GToB业务项目，需政企项目经理提供各专业签字版《5G项目组网需求确认表》，项目方可上会',
                           '项目建设摄像头、交换机、硬盘、光收发器等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                           '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）',
                           '项目有驻点人员要求，建议前后向合同中明确驻点人员的数量及工作职责，若驻点人员的工作内容与项目无关，其驻点人员费用不能计入IT维护费用中',
                           '若项目建设内容包含软件开发，建议在验收合格后与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等问题',
                           '若项目的软件开发有公网出口，建议在售中阶段公网出口及时进行ICP备案和定级备案',
                           '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责',
                           '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '大屏',
                  'data': ['若业主有除尘、防鼠虫咬隐患等要求，建议在前后向合同写明需求内容并明确责任人',
                           '若项目建设大屏布于室外，有电路/网络线路挖断的风险，建议在前后向合同中明确该部分维护职责的归属问题',
                           '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '一卡通',
                  'data': ['项目建设白卡、交换机等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                           '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）',
                           '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '智慧楼宇',
                  'data': ['项目建设摄像头、交换机、电子会议门牌、巡更设备、广播等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                           '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）',
                           '项目内门禁安防设备涉及破路施工、地下埋线，有电路/网络线路挖断的风险，建议在前后向合同中明确该部分维护职责的归属问题',
                           '项目建设若涉及物联网和云相关的业务，需网络部相关专业审核确认',
                           '项目有驻点人员要求，建议前后向合同中明确驻点人员的数量及工作职责，若驻点人员的工作内容与项目无关，其驻点人员费用不能计入IT维护费用中',
                           '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等',
                           '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责',
                           '若项目建设内容包含软件开发，建议在验收合格后与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等问题',
                           '若项目的软件开发有公网出口，建议在售中阶段，针对公网出口暴露面及时进行ICP备案和定级备案',
                           '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '云平台',
                  'data': ['若项目的软件开发有公网出口，建议在售中阶段公网出口及时进行ICP备案和定级备案',
                           '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                           '该项目为软件开发类项目，在验收合格后需与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等的问题',
                           '项目建设涉及物联网和云相关的业务，需网络部相关专业进行审核确认',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '设备采购',
                  'data': ['若业主有上门拆机、返修寄件等要求，建议在前后向合同写明需求内容并明确责任人',
                           '前后向合同需明确质保期从签署到货单之日起算，还是从签署验收合格文件之日起算',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '会议室改造',
                  'data': ['软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责',
                           '项目建设摄像头、交换机等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                           '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '综合布线',
                  'data': ['项目有线路标签脱落、扎带老化等风险，建议在后向合同维护内容中增加线路溯源、标签维护和扎带老化处理等',
                           '项目建设交换机、理线器、插线板、PDU等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                           '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）',
                           '硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '续维保',
                  'data': ['首先确认软硬件质保是否已到期，若到期或软硬件质保期不足项目维护期，需在前后向合同中明确脱保部分的维护职责',
                           '建议在前后向合同中写明取电、道路改造、设备拆移机等非自身原因造成的维护责任归属问题',
                           '项目建设摄像头、交换机、硬盘、光收发器等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                           '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '若项目为监管类项目（透明药房、阳光厨房等），容易受到人为或不可控原因导致业务中断（离线、损坏等），建议项目预留10~20%的风险金',
                           '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': 'IDC',
                  'data': [
                      '项目内设备服务器上架，禁止放于县市的骨干机房；目前服务器托管机房只有金华第一枢纽楼机房、政和路IDC机房和浙中IDC机房，按《金华IDC成本测试表》进行托管费用的测算，同时明确托管的机房',
                      '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                      '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                      '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '系统集成',
                  'data': ['项目建设摄像头、交换机、硬盘、光收发器等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                           '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）',
                           '项目有驻点人员要求，建议前后向合同中明确驻点人员的数量及工作职责，若驻点人员的工作内容与项目无关，其驻点人员费用不能计入IT维护费用中',
                           '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责',
                           '若项目建设内容包含软件开发，建议在验收合格后与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等问题',
                           '若项目的软件开发有公网出口，建议在售中阶段公网出口及时进行ICP备案和定级备案',
                           '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                           '项目内设备服务器上架，禁止放于县市的骨干机房；目前服务器托管机房只有金华第一枢纽楼机房、政和路IDC机房和浙中IDC机房，按《金华IDC成本测试表》进行托管费用的测算，同时明确托管的机房',
                           '项目建设涉及物联网和云相关的业务，需网络部相关专业审核确认',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '若项目为监管类项目（透明药房、阳光厨房等），容易受到人为或不可控原因导致业务中断（离线、损坏等），建议项目预留10~20%的风险金',
                           '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']},
                 {'name': '其他',
                  'data': ['项目建设摄像头、交换机、硬盘、光收发器等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                           '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）',
                           '项目有驻点人员要求，建议前后向合同中明确驻点人员的数量及工作职责，若驻点人员的工作内容与项目无关，其驻点人员费用不能计入IT维护费用中',
                           '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责',
                           '若项目建设内容包含软件开发，建议在验收合格后与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等问题',
                           '若项目的软件开发有公网出口，建议在售中阶段公网出口及时进行ICP备案和定级备案',
                           '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                           '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                           '若项目为监管类项目（透明药房、阳光厨房等），容易受到人为或不可控原因导致业务中断（离线、损坏等），建议项目预留10~20%的风险金',
                           '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等',
                           '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》',
                           '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']}],
        '审核留痕': [
            {'name': '审核人', 'is_must': True, 'type': 0, 'data': ''},
            {'name': '审核日期', 'is_must': True, 'type': 5, 'data': ''},
        ]
    },
    'rec_info': {}
}

gui_path = os.path.join(cur_path, 'module.cfg')
if os.path.exists(gui_path):
    os.remove(gui_path)
config = ConfigAttrDict(gui_path, tab_config)


class TabDataGui:
    def __init__(self) -> None:
        self.data = config

    def __del__(self):
        self.data.save()

    def save(self):
        self.data.save()


tab_data = TabDataGui()


class QTabWidget(QtWidgets.QTabWidget):
    in_signal = QtCore.pyqtSignal(dict)  # 定义信号

    def __init__(self, parent=None):
        super(QTabWidget, self).__init__(parent)

    def mousePressEvent(self, e):
        self.in_signal.emit({})  # 发送信号
        return super(QTabWidget, self).mousePressEvent(e)


class QComboBox(QtWidgets.QComboBox):
    in_signal = QtCore.pyqtSignal(dict)  # 定义信号

    def __init__(self, parent=None):
        super(QComboBox, self).__init__(parent)

    def focusOutEvent(self, e):
        obj_name = self.parentWidget().objectName()
        self.in_signal.emit({obj_name: {self.objectName(): self.currentText()}})  # 发送信号
        return super(QComboBox, self).focusOutEvent(e)

    def text(self):
        return self.currentText()

    def changeEvent(self, e: str) -> None:
        obj_name = self.parentWidget().objectName()
        self.in_signal.emit({obj_name: {self.objectName(): self.currentText()}})  # 发送信号
        return super(QComboBox, self).changeEvent(e)


class QLabel(QtWidgets.QLabel):
    in_signal = QtCore.pyqtSignal(dict)  # 定义信号

    def __init__(self, parent=None):
        super(QLabel, self).__init__(parent)

    def focusOutEvent(self, e):
        obj_name = self.parentWidget().objectName()
        self.in_signal.emit({obj_name: {self.objectName(): self.text()}})  # 发送信号
        return super(QLabel, self).focusOutEvent(e)


class QLineEdit(QtWidgets.QLineEdit):
    in_signal = QtCore.pyqtSignal(dict)  # 定义信号

    # def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
    #         if QStyleOptionViewItem.state & QtWidgets.QStyle.State_HasFocus:
    #             QStyleOptionViewItem.state = QStyleOptionViewItem.state ^ QtWidgets.QStyle.State_HasFocus
    #         super().paint(QPainter, QStyleOptionViewItem, QModelIndex)

    def __init__(self, parent=None):
        super(QLineEdit, self).__init__(parent)
        # self.setAttribute(QtCore.Qt.WA_MacShowFocusRect)

    def focusOutEvent(self, e):
        obj_name = self.parentWidget().objectName()
        self.in_signal.emit({obj_name: {self.objectName(): self.text()}})  # 发送信号
        return super(QLineEdit, self).focusOutEvent(e)


class QPlainTextEdit(QtWidgets.QPlainTextEdit):
    in_signal = QtCore.pyqtSignal(dict)  # 定义信号

    # def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
    #         if QStyleOptionViewItem.state & QtWidgets.QStyle.State_HasFocus:
    #             QStyleOptionViewItem.state = QStyleOptionViewItem.state ^ QtWidgets.QStyle.State_HasFocus
    #         super().paint(QPainter, QStyleOptionViewItem, QModelIndex)

    def __init__(self, parent=None):
        super(QPlainTextEdit, self).__init__(parent)

    def text(self):
        return self.toPlainText()

    def setText(self, str_data: str):
        return self.setPlainText(str_data)

    def focusOutEvent(self, e):
        obj_name = self.parentWidget().objectName()
        self.in_signal.emit({obj_name: {self.objectName(): self.text()}})  # 发送信号
        return super(QPlainTextEdit, self).focusOutEvent(e)


class QListWidget(QtWidgets.QListWidget):
    # in_signal = QtCore.pyqtSignal(dict)  # 定义信号

    # def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
    #         if QStyleOptionViewItem.state & QtWidgets.QStyle.State_HasFocus:
    #             QStyleOptionViewItem.state = QStyleOptionViewItem.state ^ QtWidgets.QStyle.State_HasFocus
    #         super().paint(QPainter, QStyleOptionViewItem, QModelIndex)

    def __init__(self, parent=None):
        super(QListWidget, self).__init__(parent)
        # self.setAttribute(QtCore.Qt.WA_MacShowFocusRect)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Resize:
            count = self.count()  # 得到QListWidget的总个数
            if count > 0:
                cb_list = [self.itemWidget(self.item(i))
                           for i in range(count)]  # 得到QListWidget里面所有QListWidgetItem中的QCheckBox
                c = cb_list[0].children()
                if len(c) == 3:
                    if c[2].width() > 200:
                        height = self.height() // 5
                        if height > 60:
                            height = 60
                        for cb in cb_list:  # type:QtWidgets.QCheckBox
                            if cb is None:
                                continue
                            cb.children()[2].setFixedSize(self.width() - 42, height)
                            # cb.setSizeHint(QtCore.QSize(self.width() - 42, height))

        return super().eventFilter(obj, event)
    # def mousePressEvent(self, e):
    #     # self.setDisabled(False)
    # #     QListWidgetItem.setDisabled(False)
    # #     # self.in_signal.emit({obj_name: {self.objectName(): self.text()}})  # 发送信号
    #     return super(QListWidget, self).mousePressEvent(e)


class MultiQComBoxConfig:
    def __init__(self, info_dict):
        pass


def boxChoose(list_wd):
    """
    得到备选统计项的字段
    :return: list[str]
    """
    count = list_wd.count()  # 得到QListWidget的总个数
    cb_list = [list_wd.itemWidget(list_wd.item(i))
               for i in range(count)]  # 得到QListWidget里面所有QListWidgetItem中的QCheckBox
    chooses = []  # 存放被选择的数据
    for cb in cb_list:  # type:QtWidgets.QCheckBox
        cd = cb.children()
        cb = cd[1]
        label = cd[2]
        if cb.isChecked():
            chooses.append(label.text())
    # print(chooses)
    return chooses


def get_check_box_2(_tab_data, obj_name, c_name, box_list, label_list):
    """
    得到备选统计项的字段
    :return: list[str]
    """
    chooses = []  # 存放被选择的数据
    for cb, dt in zip(*(box_list, label_list)):  # type:QtWidgets.QCheckBox
        if cb.isChecked():
            val = dt.text()
            chooses.append(val)

    # _tab_data.data['rec_info'].update({obj_name: {}})
    is_must_check(_tab_data, {obj_name: {c_name: chooses}}, {})


def get_check_box(_tab_data, obj_name, list_msg, list_msg2, box_list, project_dict):
    """
    得到备选统计项的字段
    :return: list[str]
    """
    chooses = []  # 存放被选择的数据
    chooses_value = []
    for cb in box_list:  # type:QtWidgets.QCheckBox
        if cb.isChecked():
            val = cb.text()
            chooses.append(val)
            for i in project_dict[val]:
                if i not in set(chooses_value):
                    chooses_value.append(i)

    box_list = []  # 统一审核建议的选择box
    label_list = []  # 同一行文本的label
    choose_save_list = []  # 默认选中的项
    last_data_list = boxChoose(list_msg)
    list_msg.clear()
    list_msg.itemClicked.disconnect()
    # print(list_msg.width() - 42, list_msg.height() // 5)
    height = list_msg.height() // 5
    if height > 60:
        height = 60
    for i in chooses_value:
        wd_box = QtWidgets.QWidget()
        hly = QtWidgets.QHBoxLayout()
        # box = QCheckBox('{:<40}'.format(i))  # 实例化一个QCheckBox，吧文字传进去
        box = QCheckBox()  # 实例化一个QCheckBox，吧文字传进去
        # label = QtWidgets.QTextBrowser()
        label = QLabel()
        label.setText('{}'.format(i))
        label.setFixedSize(list_msg.width() - 42, height)
        hly.setContentsMargins(0, 0, 0, 0)
        hly.addWidget(box)
        hly.addWidget(label)
        hly.addStretch()
        wd_box.setLayout(hly)
        box.setObjectName(i)
        item = QListWidgetItem()  # 实例化一个Item，QListWidget，不能直接加入QCheckBox

        item.setSizeHint(QtCore.QSize(list_msg.width() - 42, height))
        label.setWordWrap(True)
        wd_box.setToolTip(i)
        list_msg.addItem(item)  # 把QListWidgetItem加入QListWidget

        list_msg.setItemWidget(item, wd_box)  # 再把QCheckBox加入Q
        if i in last_data_list:
            box.setCheckState(2)  # 设置默认选中值
            choose_save_list.append(i)
        else:
            box.setCheckState(0)
        box_list.append(box)
        label_list.append(label)
        box.stateChanged.connect(lambda iw: get_check_box_2(tab_data, obj_name, '\r\n'.join(chooses), box_list, label_list))

    list_msg.itemClicked.connect(lambda: set_check_box(list_msg, box_list))
    list_msg2.in_signal.disconnect()
    list_msg2.in_signal.connect(lambda: set_add_data(tab_data, list_msg2, obj_name, '\r\n'.join(chooses)))
    _tab_data.data['rec_info'].update({obj_name: {}})
    is_must_check(_tab_data, {obj_name: {'\r\n'.join(chooses): choose_save_list}}, {obj_name: {'\r\n'.join(chooses): list_msg2}})


def set_check_box(list_msg, box_list):
    """
    设置点击item触发box
    """
    row_index = list_msg.currentIndex().row()
    box = box_list[row_index]
    status = box.checkState()
    box.setCheckState(abs(status - 2))
    list_msg.clearSelection()


def set_cale(_tab_data, obj_name, cale_wd):
    _tab_data.data['rec_info'].update({obj_name: {}})
    date = cale_wd.text()
    _tab_data.data['rec_info'].update({obj_name: {cale_wd.objectName().strip('*'): [date, '']}})


def set_add_data(_tab_data, list_msg2, obj_name, wd_name):
    if wd_name == '':
        return
    in_list = _tab_data.data['rec_info'].get(obj_name, {}).get(wd_name, [])
    if len(in_list) == 0:
        in_list_data = ''
    else:
        in_list_data = in_list[0]
    data = list_msg2.text()
    _tab_data.data['rec_info'].update({obj_name: {wd_name: [in_list_data, data]}})


def update_tab_data(_tab_data, obj_name, type_name, change_data, label_index=0):
    # print(change_data)
    rec_info = _tab_data.data.rec_info
    obj_data_dict = rec_info.get(obj_name, {})
    type_data_list = obj_data_dict.get(type_name.strip('*'), ['', ''])
    type_data_list[label_index] = change_data
    obj_data_dict.update({type_name.strip('*'):type_data_list})
    rec_info.update(obj_data_dict)
    # print(rec_info)

