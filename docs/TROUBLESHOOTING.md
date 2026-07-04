# 故障排查

## 搜索不到集成

确认文件路径为：

```text
/config/custom_components/tclplus_ac/manifest.json
```

然后重启 Home Assistant。

如果仍然搜索不到，检查 Home Assistant 日志中是否有 `custom_components.tclplus_ac` 或 `tclplus_ac` 相关错误。

## 登录失败

请确认：

- 使用的是 TCL+ 国内 App 账号。
- 账号和密码可以在手机 App 正常登录。
- Home Assistant 可以访问公网。
- 没有频繁重试触发账号风控。

本集成目前使用账号密码登录，首次配置时需要输入明文密码，但密码不会被保存。

## 手机 TCL+ App 被退出登录

这是已知副作用。

TCL+ 云端可能会让同一账号的新登录会话挤掉旧会话。Home Assistant 使用本集成登录后，手机 TCL+ App 可能会退出登录或提示需要重新登录。

如果发生这种情况：

- 在手机 TCL+ App 中重新登录。
- 确认 Home Assistant 中的空调实体仍可正常控制。
- 如果手机 App 和 Home Assistant 频繁互相挤下线，可以考虑只在 Home Assistant 中保持长期登录，手机 App 需要时再登录。

## 找不到空调设备

请确认：

- 空调已经绑定到同一个 TCL+ 账号。
- 设备在 TCL+ App 中在线。
- 设备类别为 `AC`。

如果账号下有多个设备，但集成没有创建实体，请提交 issue 并附上已脱敏的日志。

## 实体不可用

这通常不是错误，而是 TCL+ App 面板规则导致的禁用状态。

例如：

- 空调关闭时，温度和模式不可调。
- 除湿模式下，风速不可调。
- 非制热模式下，电辅热不可用。
- 非制冷模式下，柔风可能不可用。

## 控制成功但状态没有马上变化

集成默认云轮询间隔为 30 秒。控制命令发送后会主动刷新一次，但 TCL+ 云端状态仍可能有短暂延迟。

如果状态长期不更新，请检查：

- TCL+ App 中状态是否变化。
- Home Assistant 日志是否有连接错误。
- 设备是否离线。

## 风向或扫风行为不符合预期

本集成已验证：

- `verticalDirection=1` 开启上下扫风。
- `horizontalDirection=1` 开启左右扫风。
- `verticalDirection=11` 固定到中风位置。
- `horizontalDirection=11` 固定到中风位置。

不同型号的风向枚举可能存在差异。如果你的型号表现不同，请提交设备型号、产品 key 和脱敏日志。

## 查看日志

在 `configuration.yaml` 中临时加入：

```yaml
logger:
  default: info
  logs:
    custom_components.tclplus_ac: debug
```

重启 Home Assistant 后复现问题，再收集日志。

提交 issue 前请删除：

- 账号。
- 密码。
- access token。
- refresh token。
- 真实设备 ID。
- 家庭地址、公网地址、局域网地址。
