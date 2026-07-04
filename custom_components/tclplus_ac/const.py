"""Constants for the TCL+ AC integration."""

from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "tclplus_ac"

CONF_ACCESS_TOKEN = "access_token"
CONF_ACCOUNT_ID = "account_id"
CONF_CLIENT_DEVICE_ID = "client_device_id"
CONF_REFRESH_TOKEN = "refresh_token"

DEFAULT_SCAN_INTERVAL_SECONDS = 30

PLATFORMS: list[Platform] = [
    Platform.CLIMATE,
    Platform.SWITCH,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.NUMBER,
]

ACCOUNT_BASE = "https://cn.account.tcl.com"
IOT_BASE = "https://io.zx.tcljd.com"

APP_ID = "55271606743758954"
APP_SECRET = "431dba39e008c3fb2c6c1fadf44a7a6b102d016fae83b921cee79205023b1ff6"
TENANT_ID = "TCLPLUS"

APP_VERSION = "4.1.4"
APP_VERSION_NAME = "4.1.4.0"
SDK_VERSION = "6.0.4"
APP_PACKAGE_NAME = "com.tcl.tclplus"

ATTR_DEVICE_ID = "device_id"
ATTR_PRODUCT_KEY = "product_key"

TARGET_TEMPERATURE_MIN = 16
TARGET_TEMPERATURE_MAX = 31
TARGET_TEMPERATURE_STEP = 0.5

PROP_POWER = "powerSwitch"
PROP_TARGET_TEMPERATURE = "targetTemperature"
PROP_CURRENT_TEMPERATURE = "currentTemperature"
PROP_WORK_MODE = "workMode"
PROP_FAN_AUTO = "windSpeedAutoSwitch"
PROP_FAN_PERCENTAGE = "windSpeedPercentage"
PROP_VERTICAL_DIRECTION = "verticalDirection"
PROP_HORIZONTAL_DIRECTION = "horizontalDirection"
PROP_VERTICAL_WIND = "verticalWind"
PROP_HORIZONTAL_WIND = "horizontalWind"

WORK_MODE_TO_HVAC = {
    0: "auto",
    1: "cool",
    2: "dry",
    3: "fan_only",
    4: "heat",
    5: "auto",
}

HVAC_TO_WORK_MODE = {
    "auto": 0,
    "cool": 1,
    "dry": 2,
    "fan_only": 3,
    "heat": 4,
}

WORK_MODE_OPTIONS = {
    0: "自动",
    1: "制冷",
    2: "除湿",
    3: "送风",
    4: "制热",
    5: "AI",
}

SLEEP_OPTIONS = {
    0: "关",
    1: "标准",
}

VERTICAL_DIRECTION_OPTIONS = {
    1: "上下扫风",
    2: "上中扫风",
    3: "中下扫风",
    8: "停止扫风",
    9: "上风",
    10: "偏上风",
    11: "中风",
    12: "偏下风",
    13: "下风",
}

HORIZONTAL_DIRECTION_OPTIONS = {
    1: "左右扫风",
    2: "左中扫风",
    3: "中扫风",
    4: "右中扫风",
    8: "停止扫风",
    9: "左风",
    10: "偏左风",
    11: "中风",
    12: "偏右风",
    13: "右风",
}

SELF_CLEAN_STATUS_OPTIONS = {
    0: "凝露",
    1: "结霜",
    2: "除霜",
    3: "风干",
    4: "失败",
    5: "成功",
    6: "未启动",
}

SWING_OFF_VALUE = 11
SWING_VERTICAL_VALUE = 1
SWING_HORIZONTAL_VALUE = 1

SWING_OFF = "关闭"
SWING_VERTICAL = "上下扫风"
SWING_HORIZONTAL = "左右扫风"
SWING_BOTH = "上下+左右扫风"

FAN_AUTO = "自动"
FAN_MANUAL = "手动"

SWITCH_DESCRIPTIONS = {
    "powerSwitch": "电源",
    "windSpeedAutoSwitch": "自动风",
    "softWind": "柔风",
    "ECO": "节能",
    "PTC": "电辅热",
    "beepSwitch": "提示音",
    "screen": "灯光",
    "antiMoldew": "干燥",
    "selfLearn": "自学习",
    "selfClean": "蒸发器清洁",
}

SELECT_DESCRIPTIONS = {
    "sleep": ("睡眠模式", SLEEP_OPTIONS),
    "verticalDirection": ("上下送风", VERTICAL_DIRECTION_OPTIONS),
    "horizontalDirection": ("左右送风", HORIZONTAL_DIRECTION_OPTIONS),
}

NUMBER_DESCRIPTIONS = {
    "windSpeedPercentage": ("风速百分比", 1, 100, 1, "%"),
}

SENSOR_DESCRIPTIONS = {
    "sleepTime": "睡眠时间",
    "selfCleanStatus": "蒸发器清洁状态",
    "verticalWind": "上下扫风状态",
    "horizontalWind": "左右扫风状态",
    "windSpeed7Gear": "七档风速",
    "PTCStatus": "电辅热状态",
    "currentTemperature": "当前温度",
    "internalUnitCoilTemperature": "内机盘管温度",
    "externalUnitCoilTemperature": "外机盘管温度",
    "externalUnitTemperature": "外机环境温度",
    "externalUnitExhaustTemperature": "外机排气温度",
    "internalUnitFanSpeed": "内机风机转速",
    "externalUnitFanSpeed": "外机风机转速",
    "externalUnitFanGear": "外机风档",
    "compressorFrequency": "压缩机频率",
    "externalUnitElectricCurrent": "外机电流",
    "externalUnitVoltage": "外机电压",
    "fourWayValveStatus": "四通阀状态",
    "expansionValve ": "电子膨胀阀",
    "errorCode": "故障码",
    "aiSmartControlSource": "AI 控制来源",
    "tslLatestVersion": "TSL 最新版本",
    "tslReqVersion": "TSL 请求版本",
    "tslQueryTime": "TSL 查询时间",
}

DISABLE_RULES = [
    (("powerSwitch", "==", 0), "targetTemperature"),
    (("powerSwitch", "==", 0), "workMode"),
    (("workMode", "==", 2), "windSpeedAutoSwitch"),
    (("workMode", "==", 2), "windSpeedPercentage"),
    (("workMode", "!=", 1), "softWind"),
    (("powerSwitch", "==", 0), "softWind"),
    ((("workMode", "!=", 1), ("workMode", "!=", 4)), "ECO"),
    (("powerSwitch", "==", 0), "ECO"),
    (("powerSwitch", "==", 0), "PTC"),
    (("powerSwitch", "==", 0), "sleep"),
    (("workMode", "!=", 4), "PTC"),
    (("powerSwitch", "==", 0), "antiMoldew"),
    (("workMode", "==", 0), "antiMoldew"),
    (("workMode", "==", 3), "antiMoldew"),
    (("workMode", "==", 4), "antiMoldew"),
    (("workMode", "==", 5), "antiMoldew"),
    (("workMode", "==", 0), "sleep"),
    (("workMode", "==", 2), "sleep"),
    (("workMode", "==", 3), "sleep"),
]

LINK_RULES = [
    {"main": ("powerSwitch", "==", 0), "when": [], "actions": [{"softWind": 0}]},
    {"main": ("powerSwitch", "==", 1), "when": [("workMode", "==", 2)], "actions": [{"antiMoldew": 0}]},
    {"main": ("powerSwitch", "==", 1), "when": [("workMode", "!=", 2)], "actions": [{"antiMoldew": 0}]},
    {"main": ("targetTemperature", "<", 26), "when": [("workMode", "==", 1)], "actions": [{"ECO": 0}]},
    {"main": ("targetTemperature", ">", 25), "when": [("workMode", "==", 4)], "actions": [{"ECO": 0}]},
    {"main": ("targetTemperature", "==", "any"), "when": [], "actions": [{"selfLearn": 0}]},
    {
        "main": ("workMode", "==", "any"),
        "when": [],
        "actions": [
            {"ECO": 0},
            {"sleep": 0},
            {"sleepTime": 0},
            {"antiMoldew": 0},
            {"PTC": 0},
            {"selfLearn": 0},
            {"softWind": 0},
        ],
    },
    {"main": ("windSpeedAutoSwitch", "==", 1), "when": [], "actions": [{"selfLearn": 0}]},
    {"main": ("windSpeedPercentage", "==", "any"), "when": [], "actions": [{"selfLearn": 0}]},
    {"main": ("windSpeedPercentage", "!=", 0), "when": [], "actions": [{"windSpeedAutoSwitch": 0}]},
    {"main": ("horizontalDirection", "==", "any"), "when": [], "actions": [{"selfLearn": 0}]},
    {"main": ("verticalDirection", "==", "any"), "when": [], "actions": [{"selfLearn": 0}]},
    {"main": ("sleep", "==", "any"), "when": [], "actions": [{"selfLearn": 0}]},
    {
        "main": ("ECO", "==", 1),
        "when": [("workMode", "==", 1), ("targetTemperature", "<", 26)],
        "actions": [{"targetTemperature": 26}],
    },
    {
        "main": ("ECO", "==", 1),
        "when": [("workMode", "==", 4), ("targetTemperature", ">", 25)],
        "actions": [{"targetTemperature": 25}],
    },
    {"main": ("ECO", "==", 1), "when": [], "actions": [{"PTC": 0}]},
    {"main": ("PTC", "==", 1), "when": [], "actions": [{"ECO": 0}]},
    {"main": ("selfClean", "==", 1), "when": [], "actions": [{"powerSwitch": 0}]},
]
