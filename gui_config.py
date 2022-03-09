"""
type:
0 QLineEdit
1 QComboBox
"""
import os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QCheckBox, QListWidgetItem

from config import cur_path, ConfigAttrDict

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
            {'name': '签约期', 'is_must': True, 'type': 30, 'data': '年/季度/月'},
            {'name': '客户服务等级', 'is_must': [
                True, True], 'type': 0, 'data': 'compare'},
        ],
        'CT成本确认': [
            {'name': '项目是否含CT', 'is_must': True,
             'type': 3, 'data': ['是', '否']},
            {'name': 'CT成本', 'is_must': True, 'type': 30, 'data': '元'},
            {'name': 'CT收入', 'is_must': True, 'type': 30, 'data': '元'},
            {'name': 'CT成本签字人员', 'is_must': True, 'type': 0, 'data': ''},
            {'name': 'CT收入≥CT成本是否满足', 'is_must': False, 'type': 31, 'data': ''},
            {'name': '备注', 'is_must': False, 'type': 4, 'data': ''},
        ],
        '维护费信息': [
            {'name': 'IT总投入', 'is_must': True, 'type': 30, 'data': '元'},
            {'name': '质保金', 'is_must': True, 'type': 30, 'data': '元'},
            {'name': '维护费', 'is_must': True, 'type': 30, 'data': '元'},
            {'name': '维护费占比', 'is_must': False, 'type': 31, 'data': ''},
        ],
        '业主侧维护及考核要求': [
            {'name': '服务承诺', 'is_must': [True, True], 'type': [
                1, 0], 'data': [['有', '无'], '7*24小时热线服务']},
            {'name': '故障处理时限是否明确', 'is_must': [True, True], 'type': [1, 1], 'data': [['是', '否'],
                                                                                     ['故障于2小时内解决',
                                                                                      '故障于4小时内解决',
                                                                                      '故障于6小时内解决',
                                                                                      '故障于8小时内解决',
                                                                                      '故障于12小时内解决',
                                                                                      '故障于18小时内解决',
                                                                                      '故障于24小时内解决',
                                                                                      '故障于36小时内解决',
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
            {'name': '备品备件需求是否明确', 'is_must': [True, True], 'type': [
                1, 0], 'data': [['是', '否'], '摄像头备件']},
            {'name': '维护界面是否清晰', 'is_must': [True, True], 'type': [1, 0],
             'data': [['是', '否'], '取电问题由客户负责，其他维护全部由乙方负责']},
            {'name': '考核方式是否明确', 'is_must': [True, True], 'type': [1, 0],
             'data': [['是', '否'], '每年12月底取数，在线率低于95%，每低于1个百分点，扣除本年底1/45的维护款']},
            {'name': '补充说明', 'is_must': [False], 'type': [4], 'data': ['']},
        ],
        '项目类型': [{'name': '视频监控',
                  'data': [[0,
                            '【备品备件】',
                            '项目建设摄像头、交换机、硬盘、光收发器等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                            '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）'],
                           [1, '【脱保风险】', '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责'],
                           [2, '【维护职责】', '建议在前后向合同中写明取电、道路改造、设备拆移机等非自身原因造成的维护责任归属问题'],
                           [3, '【信息安全】', '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [5,
                            '【预留风险金】',
                            '若项目为监管类项目（透明药房、阳光厨房等），容易受到人为或不可控原因导致业务中断（离线、损坏等），建议项目预留10~20%的风险金'],
                           [9,
                            '【提升维护等级】',
                            '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '视频监控（公安）',
                  'data': [[0, '【备品备件】', '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）'],
                           [1, '【脱保风险】', '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责'],
                           [3, '【信息安全】', '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [4,
                            '【其他】',
                            '项目有驻点人员要求，建议前后向合同中明确驻点人员的数量及工作职责，若驻点人员的工作内容与项目无关，其驻点人员费用不能计入IT维护费用中'],
                           [5, '【预留风险金】', '若项目建设点位有破路取电、老旧小区改造、设备拆移机等风险，建议项目预留10~20%的风险金'],
                           [11,
                            '【考核支付】',
                            '若项目内建设点位纳入公安健康度考核，建议在后向合同的维护条款和考核内容中写明维护单位每日线上巡检、及时修复，并将扣分原因反馈给区县公安视频监控负责人，非维护不力造成的考核扣分需及时向公安报备',
                            '公安视频监控有较高的健康度考核指标（要求：99%以上），建议项目内提供不低于3%的备品备件（摄像头、交换机、光收发器、硬盘等），在前后向合同中写明备品备件需求说明',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': 'WLAN',
                  'data': [[0,
                            '【备品备件】',
                            '项目建设AP、交换机、外置天线等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                            '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）'],
                           [1, '【脱保风险】', '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责'],
                           [2, '【维护职责】', '建议在前后向合同中写明设备拆移机等非自身原因造成的维护责任归属问题'],
                           [3, '【信息安全】', '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [8,
                            '【售中实施建议】',
                            '建议项目建设AP上线后，AP名称修改为其覆盖楼层，同时做好三层拓扑、IP规划、项目建设详单、CAD图纸等资料整理归档工作',
                            '为便于后期设备的检修，建议项目施工建设过程中预留充足的检修口'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '软件开发',
                  'data': [[3,
                            '【信息安全】',
                            '若项目的软件开发有公网出口，建议在售中阶段及时完成ICP备案和漏洞扫描修复',
                            '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                            '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [9,
                            '【提升维护等级】',
                            '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等'],
                           [10,
                            '【规范验收】',
                            '该项目为软件开发类项目，在验收合格后需与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等的问题'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '5G',
                  'data': [[0,
                            '【备品备件】',
                            '项目建设摄像头、交换机、硬盘、光收发器等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                            '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）'],
                           [1, '【脱保风险】', '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责'],
                           [3,
                            '【信息安全】',
                            '若项目的软件开发有公网出口，建议在售中阶段及时完成ICP备案和漏洞扫描修复',
                            '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                            '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [4,
                            '【其他】',
                            '项目有驻点人员要求，建议前后向合同中明确驻点人员的数量及工作职责，若驻点人员的工作内容与项目无关，其驻点人员费用不能计入IT维护费用中'],
                           [6, '【专业口审核】', '若项目为5GToB业务项目，需政企项目经理提供各专业签字版《5G项目组网需求确认表》，项目方可上会'],
                           [9,
                            '【提升维护等级】',
                            '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等'],
                           [10,
                            '【规范验收】',
                            '若项目建设内容包含软件开发，建议在验收合格后与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等问题'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '大屏',
                  'data': [[1, '【脱保风险】', '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责'],
                           [2,
                            '【维护职责】',
                            '若业主有除尘、防鼠虫咬隐患等要求，建议在前后向合同写明需求内容并明确责任人',
                            '若项目建设大屏布于室外，有电路/网络线路挖断的风险，建议在前后向合同中明确该部分维护职责的归属问题'],
                           [3, '【信息安全】', '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '一卡通',
                  'data': [[0,
                            '【备品备件】',
                            '项目建设白卡、交换机等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                            '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）'],
                           [1, '【脱保风险】', '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责'],
                           [3, '【信息安全】', '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '智慧楼宇',
                  'data': [[0,
                            '【备品备件】',
                            '项目建设摄像头、交换机、电子会议门牌、巡更设备、广播等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                            '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）'],
                           [1, '【脱保风险】', '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责'],
                           [2, '【维护职责】', '项目内门禁安防设备涉及破路施工、地下埋线，有电路/网络线路挖断的风险，建议在前后向合同中明确该部分维护职责的归属问题'],
                           [3,
                            '【信息安全】',
                            '若项目的软件开发有公网出口，建议在售中阶段及时完成ICP备案和漏洞扫描修复',
                            '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                            '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [4,
                            '【其他】',
                            '项目有驻点人员要求，建议前后向合同中明确驻点人员的数量及工作职责，若驻点人员的工作内容与项目无关，其驻点人员费用不能计入IT维护费用中'],
                           [6, '【专业口审核】', '项目建设若涉及物联网和云相关的业务，需网络部相关专业审核确认'],
                           [9,
                            '【提升维护等级】',
                            '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等'],
                           [10,
                            '【规范验收】',
                            '若项目建设内容包含软件开发，建议在验收合格后与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等问题'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '云平台',
                  'data': [[3,
                            '【信息安全】',
                            '若项目的软件开发有公网出口，建议在售中阶段及时完成ICP备案和漏洞扫描修复',
                            '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                            '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [6, '【专业口审核】', '项目建设若涉及物联网和云相关的业务，需网络部相关专业审核确认'],
                           [9,
                            '【提升维护等级】',
                            '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等'],
                           [10,
                            '【规范验收】',
                            '该项目为软件开发类项目，在验收合格后需与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等的问题'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '设备采购',
                  'data': [[3,
                            '【信息安全】',
                            '若项目的软件开发有公网出口，建议在售中阶段及时完成ICP备案和漏洞扫描修复',
                            '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                            '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [6, '【专业口审核】', '项目建设若涉及物联网和云相关的业务，需网络部相关专业审核确认'],
                           [9,
                            '【提升维护等级】',
                            '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等'],
                           [10,
                            '【规范验收】',
                            '该项目为软件开发类项目，在验收合格后需与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等的问题'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '会议室改造',
                  'data': [[0,
                            '【备品备件】',
                            '项目建设摄像头、交换机等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                            '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）'],
                           [1, '【脱保风险】', '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责'],
                           [3, '【信息安全】', '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [9,
                            '【提升维护等级】',
                            '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '综合布线',
                  'data': [[0,
                            '【备品备件】',
                            '项目建设交换机、理线器、插线板、PDU等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                            '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）'],
                           [1, '【脱保风险】', '硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责'],
                           [2, '【维护职责】', '项目有线路标签脱落、扎带老化等风险，建议在后向合同维护内容中增加线路溯源、标签维护和扎带老化处理等'],
                           [3, '【信息安全】', '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '续维保',
                  'data': [[0,
                            '【备品备件】',
                            '项目建设摄像头、交换机、硬盘、光收发器等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                            '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）'],
                           [1, '【脱保风险】', '首先确认软硬件质保是否已到期，若到期或软硬件质保期不足项目维护期，需在前后向合同中明确脱保部分的维护职责'],
                           [2, '【维护职责】', '建议在前后向合同中写明取电、道路改造、设备拆移机等非自身原因造成的维护责任归属问题'],
                           [3, '【信息安全】', '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [5,
                            '【预留风险金】',
                            '若项目为监管类项目（透明药房、阳光厨房等），容易受到人为或不可控原因导致业务中断（离线、损坏等），建议项目预留10~20%的风险金'],
                           [9,
                            '【提升维护等级】',
                            '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': 'IDC',
                  'data': [[3, '【信息安全】', '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [7,
                            '【设备托管】',
                            '项目内设备服务器上架，禁止放于县市的骨干机房；目前服务器托管机房只有金华第一枢纽楼机房、政和路IDC机房和浙中IDC机房，按《金华IDC成本测试表》进行托管费用的测算，同时明确托管的机房'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '系统集成',
                  'data': [[0,
                            '【备品备件】',
                            '项目建设摄像头、交换机、硬盘、光收发器等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                            '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）'],
                           [1, '【脱保风险】', '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责'],
                           [3,
                            '【信息安全】',
                            '若项目的软件开发有公网出口，建议在售中阶段及时完成ICP备案和漏洞扫描修复',
                            '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                            '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [4,
                            '【其他】',
                            '项目有驻点人员要求，建议前后向合同中明确驻点人员的数量及工作职责，若驻点人员的工作内容与项目无关，其驻点人员费用不能计入IT维护费用中'],
                           [5,
                            '【预留风险金】',
                            '若项目为监管类项目（透明药房、阳光厨房等），容易受到人为或不可控原因导致业务中断（离线、损坏等），建议项目预留10~20%的风险金'],
                           [6, '【专业口审核】', '项目建设若涉及物联网和云相关的业务，需网络部相关专业审核确认'],
                           [7,
                            '【设备托管】',
                            '项目内设备服务器上架，禁止放于县市的骨干机房；目前服务器托管机房只有金华第一枢纽楼机房、政和路IDC机房和浙中IDC机房，按《金华IDC成本测试表》进行托管费用的测算，同时明确托管的机房'],
                           [9,
                            '【提升维护等级】',
                            '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等'],
                           [10,
                            '【规范验收】',
                            '若项目建设内容包含软件开发，建议在验收合格后与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等问题'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]},
                 {'name': '其他',
                  'data': [[0,
                            '【备品备件】',
                            '项目建设摄像头、交换机、硬盘、光收发器等易损件数量超30个，建议项目内提供不低于3%的备品备件，在后向合同中写明备品备件需求说明',
                            '建议在前后向合同中明确备品备件保管方及归属责任（含：备件遗失问题）'],
                           [1, '【脱保风险】', '软硬件质保期与项目维护期是否一致，若不一致，需在前后向合同中明确脱保部分的维护职责'],
                           [3,
                            '【信息安全】',
                            '若项目的软件开发有公网出口，建议在售中阶段及时完成ICP备案和漏洞扫描修复',
                            '若项目建设平台/软件存在公网暴露面，售中阶段需完成漏洞扫描和修复工作',
                            '建议项目售前售中阶段与客户签订《ICT项目网络与信息安全责任书》'],
                           [4,
                            '【其他】',
                            '项目有驻点人员要求，建议前后向合同中明确驻点人员的数量及工作职责，若驻点人员的工作内容与项目无关，其驻点人员费用不能计入IT维护费用中'],
                           [5,
                            '【预留风险金】',
                            '若项目为监管类项目（透明药房、阳光厨房等），容易受到人为或不可控原因导致业务中断（离线、损坏等），建议项目预留10~20%的风险金'],
                           [9,
                            '【提升维护等级】',
                            '若项目为防疫类、重要场所保障、关乎大规模民生民事等类型项目，建议提高项目整体维护等级（含IT、CT），如：增设驻点人员（不低于8万元/人/年）、提高巡检频次等'],
                           [10,
                            '【规范验收】',
                            '若项目建设内容包含软件开发，建议在验收合格后与业主签一个软件功能满足客户需求的书面说明，避免软件验收后客户提出功能缺失等问题'],
                           [11,
                            '【考核支付】',
                            '项目支付方式背靠背，要求集成公司/铁通公司与集成商后向合同的质保金/维护费需可维护考核（扣罚），建议在政企项目委托的材料中写明',
                            '客户未明确要求的维护内容和考核方式，建议后向合同按照SLA标准写明']]}],
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

    def send_signal(self):
        obj_name = self.parentWidget().objectName()
        self.in_signal.emit({obj_name: {self.objectName(): self.text()}})  # 发送信号

    def focusOutEvent(self, e):
        self.send_signal()
        return super(QLineEdit, self).focusOutEvent(e)


class MultiTextEdit(QLineEdit):
    def __init__(self, type_name, obj_name, wd_data):
        super(MultiTextEdit, self).__init__()
        # type_wd_l = QLineEdit()
        # self.type_wd_l = type_wd_l
        # self.textChanged = type_wd_l.textChanged
        # self.in_signal = type_wd_l.in_signal
        # self.setValidator = type_wd_l.setValidator
        type_wd_l = self
        type_wd_l.setObjectName(type_name)
        # 输入框布局
        type_wdl = QtWidgets.QHBoxLayout()
        # type_wd = QtWidgets.QWidget(wd_layout)
        # type_wdl.addStretch()
        type_wdl.addWidget(type_wd_l)
        # type_wdl.addStretch()
        if '/' in wd_data:
            self.unit_d = QComboBox()
            self.unit_d.addItems(wd_data.split('/'))
            self.unit_d.in_signal.connect(lambda: self.send_signal())
        else:
            self.unit_d = QtWidgets.QLabel(wd_data)
        type_wdl.addWidget(self.unit_d)
        type_wdl.addStretch()
        type_wdl.setContentsMargins(0, 0, 0, 0)
        # 创建控件并设置布局
        type_wd = QtWidgets.QWidget()
        type_wd.setObjectName(obj_name)
        type_wd.setLayout(type_wdl)
        type_wd.setFixedHeight(25)
        type_wd.in_signal = self.in_signal
        self.type_wd = type_wd

    def text(self):
        t = super(QLineEdit, self).text()
        text = t + self.unit_d.text()
        return text


class QPlainTextEdit(QtWidgets.QPlainTextEdit):
    in_signal = QtCore.pyqtSignal(dict)  # 定义信号

    # def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
    #         if QStyleOptionViewItem.state & QtWidgets.QStyle.State_HasFocus:
    #             QStyleOptionViewItem.state = QStyleOptionViewItem.state ^ QtWidgets.QStyle.State_HasFocus
    #         super().paint(QPainter, QStyleOptionViewItem, QModelIndex)

    def __init__(self, parent=None, is_now=False):
        super(QPlainTextEdit, self).__init__(parent)
        self.is_now = is_now

    def textChanged(self) -> None:
        if self.is_now:
            obj_name = self.parentWidget().objectName()
            self.in_signal.emit({obj_name: {self.objectName(): self.text()}})  # 发送信号
        return super(QPlainTextEdit, self).textChanged()

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
        if len(cd) < 3:
            continue
        cb = cd[1]
        label = cd[2]
        if isinstance(cb, QCheckBox) and cb.isChecked():
            chooses.append(label.text())
    # print(chooses)
    return chooses


def get_check_box_2(_tab_data, obj_name, c_name, box_list, label_list):
    """
    得到备选统计项的字段
    :return: list[str]
    """
    chooses = []  # 存放被选择的数据
    last_group = ''
    now_group = ''
    for cb, dt in zip(*(box_list, label_list)):  # type:QtWidgets.QCheckBox
        text_data = dt.text()
        # 添加标题
        if text_data[0] == '【':
            now_group = text_data
            continue
        if cb.isChecked():
            if last_group != now_group:
                chooses.append(now_group)
                last_group = now_group
            val = text_data
            chooses.append(val)

    # _tab_data.data['rec_info'].update({obj_name: {}})
    set_add_data(_tab_data, chooses, obj_name, c_name, is_first=True)
    # is_must_check(_tab_data, {obj_name: {c_name: chooses}}, {})


def get_select_data(suggest_list):
    """
    建议数据转换
    :param suggest_list: 建议数据列表 data[0]为排序 data[1]为标题
    :return:
    """
    print(suggest_list)
    suggest_list.sort(key=lambda x: x[0])
    last_index = -1
    out_list = []
    for line_data in suggest_list:
        start_num = 1
        if line_data[0] == last_index:
            start_num = 2
        out_list += line_data[start_num:]

    return out_list


def get_check_box(_tab_data, obj_name, list_msg, list_msg2, box_list, project_dict):
    """
    得到备选统计项的字段
    :return: list[str]
    """
    chooses = []  # 存放被选择的数据
    suggest_list = []  # 建议数据暂存
    for cb in box_list:  # type:QtWidgets.QCheckBox
        if isinstance(cb, QCheckBox) and cb.isChecked():
            # 获取选中的项目类型
            val = cb.text()
            chooses.append(val)
            for i in project_dict[val]:
                # 获取对应的数据
                suggest_list.append(i)

    chooses_value = get_select_data(suggest_list)  # 统一审核建议的内容list

    box_list = []  # 统一审核建议的选择box
    label_list = []  # 同一行文本的label
    choose_save_list = []  # 默认选中的项
    last_data_list = boxChoose(list_msg)
    list_msg.clear()
    list_msg.itemClicked.disconnect()
    # print(list_msg.width() - 42, list_msg.height() // 5)
    height_f = list_msg.height() // 5
    if height_f > 60:
        height_f = 60
    for i in chooses_value:
        wd_box = QtWidgets.QWidget()
        hly = QtWidgets.QHBoxLayout()
        # box = QCheckBox('{:<40}'.format(i))  # 实例化一个QCheckBox，吧文字传进去
        box = QCheckBox()  # 实例化一个QCheckBox，吧文字传进去
        # label = QtWidgets.QTextBrowser()
        label = QLabel()
        label.setText('{}'.format(i))

        hly.setContentsMargins(0, 0, 0, 0)  # 边距

        wd_box.setLayout(hly)
        box.setObjectName(i)
        item = QListWidgetItem()  # 实例化一个Item，QListWidget，不能直接加入QCheckBox
        if i[0] == '【':
            height = height_f // 2.2
            box_list.append(None)
            # hly.addWidget(None)
            label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
            label.setStyleSheet("font-weight:bold;border-width: 1px;border-style: solid;border-color: rgba("
                                "255, 170, 170, 0.3);")
        else:
            hly.addWidget(box)
            box_list.append(box)
            height = height_f
        hly.addWidget(label)
        hly.addStretch()

        label_list.append(label)

        label.setFixedSize(list_msg.width() - 42, height)
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

        box.stateChanged.connect(
            lambda iw: get_check_box_2(tab_data, obj_name, '\r\n'.join(chooses), box_list, label_list))

    list_msg.itemClicked.connect(lambda: set_check_box(list_msg, box_list))
    list_msg2.in_signal.disconnect()
    list_msg2.in_signal.connect(lambda: set_add_data(tab_data, list_msg2, obj_name, '\r\n'.join(chooses)))
    _tab_data.data['rec_info'].update({obj_name: {'\r\n'.join(chooses): [choose_save_list, list_msg2.text()]}})
    # set_add_data(_tab_data, choose_save_list, obj_name, '\r\n'.join(chooses), is_first=True)
    # is_must_check(_tab_data, {obj_name: {'\r\n'.join(chooses): choose_save_list}},
    #               {obj_name: {'\r\n'.join(chooses): list_msg2}})


def set_check_box(list_msg, box_list):
    """
    设置点击item触发box
    """
    row_index = list_msg.currentIndex().row()
    box = box_list[row_index]
    if box is not None:
        status = box.checkState()
        box.setCheckState(abs(status - 2))
    list_msg.clearSelection()


def set_cale(_tab_data, obj_name, cale_wd):
    _tab_data.data['rec_info'].update({obj_name: {}})
    date = cale_wd.text()
    _tab_data.data['rec_info'].update({obj_name: {cale_wd.objectName().strip('*'): [date, '']}})


def set_first_data(_tab_data, list_msg, obj_name, wd_name):
    """
    添加第一列数据接口
    :param _tab_data:
    :param list_msg2:
    :param obj_name:
    :param param:
    :return:
    """
    pass


def set_add_data(_tab_data, list_msg2, obj_name, wd_name, is_first=False):
    """
    添加第二列数据，选填项可用
    :param _tab_data: 保存的数据
    :param list_msg2: 信息组件
    :param obj_name:
    :param wd_name:
    :param is_first: 是否第一列
    :return:
    """
    if wd_name == '':
        wd_name = '项目未选择'
    in_list = _tab_data.data['rec_info'].get(obj_name, {}).get(wd_name, ['', ''])
    if isinstance(list_msg2, list):
        data = list_msg2
    else:
        data = list_msg2.text()
    if is_first:
        out_list = [data, in_list[1]]
    else:
        out_list = [in_list[0], data]
    _tab_data.data['rec_info'].update({obj_name: {wd_name: out_list}})


def update_tab_data(_tab_data, obj_name, type_name, change_data, label_index=0):
    # print(change_data)
    rec_info = _tab_data.data.rec_info
    obj_data_dict = rec_info.get(obj_name, {})
    type_data_list = obj_data_dict.get(type_name.strip('*'), ['', ''])
    type_data_list[label_index] = change_data
    obj_data_dict.update({type_name.strip('*'): type_data_list})
    rec_info.update(obj_data_dict)
    # print(rec_info)
