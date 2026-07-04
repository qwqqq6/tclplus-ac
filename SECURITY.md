# Security Policy

## 支持版本

当前项目处于早期阶段，仅维护最新版本。

| Version | Supported |
| --- | --- |
| 0.1.x | Yes |

## 报告安全问题

如果你发现安全问题，请不要在公开 issue 中贴出敏感内容。

敏感内容包括：

- TCL+ 账号。
- 密码。
- access token。
- refresh token。
- 真实设备 ID。
- 家庭地址。
- 公网 IP。
- 抓包原始数据。

在公开 issue 中可以描述问题类型和影响范围，但请先删除所有敏感字段。

## 数据存储说明

本集成不会保存明文密码。

Home Assistant 配置条目中会保存：

- TCL+ access token。
- TCL+ refresh token。
- TCL+ account id。
- 本集成生成的客户端 device id。

这些数据由 Home Assistant 存储在配置目录中。请保护你的 Home Assistant 配置目录、备份和日志。

## 手机 App 会话

TCL+ 云端可能会让同一账号的新登录会话挤掉旧会话。使用本集成登录后，手机 TCL+ App 可能会退出登录或要求重新登录。

这不是本集成主动注销手机 App，而是云端账号会话策略的结果。请确保你可以重新登录 TCL+ App，并妥善保管账号凭据。

## 网络说明

本集成需要访问 TCL+ 国内云接口：

- `cn.account.tcl.com`
- `io.zx.tcljd.com`

设备控制依赖云端接口，不是本地局域网控制。
