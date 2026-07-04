# TCL+ AC for Home Assistant

TCL+ AC 是一个非官方 Home Assistant 自定义集成，用于接入 TCL+ 国内 App 账号下的 TCL 空调设备。

这个集成基于 TCL+ 国内 App 云接口实现，目标是补齐小程序接口缺失的能力，例如上下/左右风向、扫风、柔风、ECO、电辅热、灯光、提示音等控制。

> 非官方项目：本项目与 TCL、TCL+、Home Assistant 官方均无隶属关系。云接口可能随 App 更新而变化，请自行评估使用风险。

> 账号登录提示：TCL+ 云端可能只允许同一账号保持有限数量的有效登录会话。使用本集成登录后，手机 TCL+ App 可能会被挤下线，需要在手机 App 中重新登录。建议使用前确认你可以正常找回或重新登录 TCL+ 账号。

## 功能

- 通过 Home Assistant 配置流登录 TCL+ 国内 App 账号。
- 不保存明文密码，仅保存访问令牌和刷新令牌。
- 自动刷新令牌。
- 读取账号下的 TCL 空调设备。
- 暴露标准 `climate` 实体：开关、模式、目标温度、当前温度、风模式、扫风模式。
- 暴露独立控制实体：柔风、ECO、电辅热、提示音、灯光、干燥、自学习、蒸发器清洁、睡眠模式、风向位置、风速百分比。
- 暴露诊断传感器：扫风状态、清洁状态、盘管温度、外机温度、风机转速、电压、电流、压缩机频率、故障码等。
- 模拟 TCL+ App 面板的联动和禁用规则，减少无效控制命令。

## 兼容性

- Home Assistant：建议 `2024.6.0` 或更新版本。
- 已验证环境：Home Assistant OS `17.3`，Home Assistant Core `2026.5.4`。
- 已验证 App：TCL+ 国内 Android App `4.1.4.0`。
- 已验证设备类别：`AC`。
- 已验证型号：`KFRd-72L/D-ME21Bp(B1)`。

其他型号可能也能工作，但需要实际测试。欢迎提交兼容性反馈。

## 安装

### HACS 自定义仓库

可在 HACS 中添加自定义仓库：

1. 打开 HACS。
2. 进入自定义仓库。
3. 输入仓库地址：`https://github.com/qwqqq6/tclplus-ac`。
4. 类别选择 `Integration`。
5. 安装 `TCL+ AC`。
6. 重启 Home Assistant。

### 手动安装

将目录复制到 Home Assistant 配置目录：

```text
custom_components/tclplus_ac
```

最终结构应类似：

```text
config/
  custom_components/
    tclplus_ac/
      manifest.json
      __init__.py
      config_flow.py
      ...
```

然后重启 Home Assistant。

## 配置

重启后进入：

```text
设置 -> 设备与服务 -> 添加集成 -> TCL+ AC
```

输入 TCL+ 国内 App 使用的账号和密码。

密码只用于首次登录；集成会保存 TCL+ 返回的 token，不会保存明文密码。

### 手机 App 登录状态

TCL+ 云端可能会让同一账号的新登录会话挤掉旧会话。因此，首次在 Home Assistant 中配置本集成，或者 token 刷新后，手机 TCL+ App 可能会退出登录或提示需要重新登录。

这是 TCL+ 账号会话策略导致的副作用，不代表空调控制失败。建议使用前确认你知道 TCL+ App 的账号密码，并能在手机上重新登录。

## 文档

- [安装说明](docs/INSTALLATION.md)
- [实体说明](docs/ENTITIES.md)
- [故障排查](docs/TROUBLESHOOTING.md)
- [开发说明](docs/DEVELOPMENT.md)
- [贡献指南](CONTRIBUTING.md)
- [安全策略](SECURITY.md)
- [更新日志](CHANGELOG.md)

## 免责声明

本项目仅供学习、研究和个人自动化使用。TCL+ 云服务、App 接口、设备能力可能随时变化。使用本项目造成的账号、设备、云服务、网络或自动化风险由使用者自行承担。
