# 实体说明

本集成会为每台 TCL 空调创建一个主 `climate` 实体，并根据设备当前属性创建若干开关、下拉框、数字滑块和传感器。

## Climate

主实体用于 Home Assistant 标准空调控制。

| 功能 | TCL+ 属性 | 说明 |
| --- | --- | --- |
| 开关 | `powerSwitch` | `0=关`，`1=开` |
| 模式 | `workMode` | 自动、制冷、除湿、送风、制热 |
| 目标温度 | `targetTemperature` | 默认范围 `16..31`，步进 `0.5` |
| 当前温度 | `currentTemperature` | 室内当前温度 |
| 风模式 | `windSpeedAutoSwitch` | 自动风 / 手动风 |
| 扫风模式 | `verticalDirection`、`horizontalDirection` | 关闭、上下、左右、上下+左右 |

## Switch

| 实体 | TCL+ 属性 | 说明 |
| --- | --- | --- |
| 电源 | `powerSwitch` | 独立电源开关 |
| 自动风 | `windSpeedAutoSwitch` | 自动风速 |
| 柔风 | `softWind` | 通常仅制冷可用 |
| 节能 | `ECO` | 制冷/制热可用 |
| 电辅热 | `PTC` | 通常仅制热可用 |
| 提示音 | `beepSwitch` | 蜂鸣提示音 |
| 灯光 | `screen` | 面板/屏显灯光 |
| 干燥 | `antiMoldew` | 防霉干燥 |
| 自学习 | `selfLearn` | 设备自学习 |
| 蒸发器清洁 | `selfClean` | 启动清洁流程 |

## Select

| 实体 | TCL+ 属性 | 选项 |
| --- | --- | --- |
| 睡眠模式 | `sleep` | 关、标准 |
| 上下送风 | `verticalDirection` | 上下扫风、上中扫风、中下扫风、停止扫风、上风、偏上风、中风、偏下风、下风 |
| 左右送风 | `horizontalDirection` | 左右扫风、左中扫风、中扫风、右中扫风、停止扫风、左风、偏左风、中风、偏右风、右风 |

## Number

| 实体 | TCL+ 属性 | 范围 |
| --- | --- | --- |
| 风速百分比 | `windSpeedPercentage` | `1..100%` |

## Sensor

| 实体 | TCL+ 属性 | 说明 |
| --- | --- | --- |
| 睡眠时间 | `sleepTime` | 睡眠计时状态 |
| 蒸发器清洁状态 | `selfCleanStatus` | 凝露、结霜、除霜、风干、失败、成功、未启动 |
| 上下扫风状态 | `verticalWind` | 开启/关闭 |
| 左右扫风状态 | `horizontalWind` | 开启/关闭 |
| 七档风速 | `windSpeed7Gear` | 设备上报的风档状态 |
| 电辅热状态 | `PTCStatus` | 开启/关闭 |
| 当前温度 | `currentTemperature` | 室内温度 |
| 内机盘管温度 | `internalUnitCoilTemperature` | 诊断温度 |
| 外机盘管温度 | `externalUnitCoilTemperature` | 诊断温度 |
| 外机环境温度 | `externalUnitTemperature` | 诊断温度 |
| 外机排气温度 | `externalUnitExhaustTemperature` | 诊断温度 |
| 内机风机转速 | `internalUnitFanSpeed` | rpm |
| 外机风机转速 | `externalUnitFanSpeed` | rpm |
| 外机风档 | `externalUnitFanGear` | 设备风档 |
| 压缩机频率 | `compressorFrequency` | Hz |
| 外机电流 | `externalUnitElectricCurrent` | A |
| 外机电压 | `externalUnitVoltage` | V |
| 四通阀状态 | `fourWayValveStatus` | 开启/关闭 |
| 电子膨胀阀 | `expansionValve ` | 注意属性名包含尾随空格 |
| 故障码 | `errorCode` | 无故障时显示“无” |
| AI 控制来源 | `aiSmartControlSource` | 云端来源标记 |
| TSL 最新版本 | `tslLatestVersion` | 设备物模型版本 |
| TSL 请求版本 | `tslReqVersion` | 请求版本 |
| TSL 查询时间 | `tslQueryTime` | 云端查询时间 |

## 禁用规则

部分实体会在特定模式下显示不可用，这是按照 TCL+ App 面板规则处理的。

常见规则：

- 空调关闭时，温度、模式、柔风、ECO、电辅热、睡眠、干燥不可用。
- 除湿模式下，自动风和风速百分比不可用。
- 柔风通常只在制冷模式可用。
- 电辅热通常只在制热模式可用。
- 睡眠通常只在制冷或制热模式可用。

## 联动规则

为了模拟 App 行为，部分控制会附带额外属性：

- 关闭电源会同时关闭柔风。
- 切换模式会清理 ECO、睡眠、干燥、电辅热、自学习、柔风等状态。
- 手动设置风速会关闭自动风。
- 设置风向、睡眠、温度会关闭自学习。
- 开启 ECO 会关闭电辅热。
- 开启电辅热会关闭 ECO。
- 开启蒸发器清洁会关闭空调电源。
