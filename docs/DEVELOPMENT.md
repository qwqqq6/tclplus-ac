# 开发说明

## 项目结构

```text
custom_components/tclplus_ac/
  __init__.py
  api.py
  climate.py
  config_flow.py
  const.py
  coordinator.py
  entity.py
  number.py
  select.py
  sensor.py
  switch.py
  manifest.json
  strings.json
  translations/
```

## 设计概要

- `api.py`：同步 TCL+ 云 API 客户端，使用 Python 标准库 `urllib`，不引入第三方运行时依赖。
- `coordinator.py`：Home Assistant `DataUpdateCoordinator`，负责轮询设备状态和集中控制。
- `config_flow.py`：配置流登录。
- `climate.py`：主空调实体。
- `switch.py`、`select.py`、`number.py`、`sensor.py`：按 TCL+ 属性拆分的辅助实体。
- `const.py`：属性名、枚举、禁用规则、联动规则。

## 本地检查

本项目运行时不需要第三方 Python 包。

可以用 Python 编译检查语法：

```bash
python -m compileall custom_components/tclplus_ac
```

在 Windows PowerShell 中：

```powershell
python -m compileall custom_components\tclplus_ac
```

## Home Assistant 中测试

将集成复制到：

```text
/config/custom_components/tclplus_ac
```

然后运行：

```bash
ha core check
ha core restart
```

重启后到“设备与服务”添加 `TCL+ AC`。

## 代码原则

- 尽量保持运行时零第三方依赖。
- 控制命令尽量模拟 TCL+ App 面板的参数和联动规则。
- 新增设备能力前，优先验证 App 行为和云端返回状态。
- 不要在日志中输出账号、密码、token、完整设备 ID。
- 避免提交个人抓包、逆向分析缓存和 `.secrets` 目录。

## 提交兼容性反馈

请尽量提供：

- Home Assistant 版本。
- TCL+ App 版本。
- 空调型号。
- 产品 key。
- 控制项是否可用。
- 脱敏后的错误日志。

请不要提供：

- 账号。
- 密码。
- access token。
- refresh token。
- 完整设备 ID。
- 家庭地址或公网地址。
