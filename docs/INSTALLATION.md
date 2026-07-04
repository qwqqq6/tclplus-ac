# 安装说明

本文档说明如何安装 `TCL+ AC` Home Assistant 自定义集成。

## 前提条件

- 一台可正常运行的 Home Assistant。
- 一个可以在 TCL+ 国内 App 登录的账号。
- 账号下已经绑定 TCL 空调设备。
- Home Assistant 可以访问公网 TCL+ 云接口。

## HACS 安装

可以通过 HACS 自定义仓库安装：

1. 打开 Home Assistant。
2. 打开 HACS。
3. 添加自定义仓库。
4. 仓库地址填写 `https://github.com/qwqqq6/tclplus-ac`。
5. 仓库类型选择 `Integration`。
6. 搜索并安装 `TCL+ AC`。
7. 重启 Home Assistant。

如果 HACS 中搜索不到，请确认：

- 仓库根目录存在 `hacs.json`。
- 仓库根目录存在 `custom_components/tclplus_ac/manifest.json`。
- `manifest.json` 中包含 `version` 字段。

## 手动安装

将 `custom_components/tclplus_ac` 复制到 Home Assistant 配置目录。

Home Assistant OS 或 Container 常见路径：

```text
/config/custom_components/tclplus_ac
```

安装后重启 Home Assistant。

## 添加集成

重启后进入：

```text
设置 -> 设备与服务 -> 添加集成 -> TCL+ AC
```

输入 TCL+ 国内 App 的账号和密码。

如果登录成功，集成会自动读取账号下的空调设备并创建实体。

## 手机 App 可能退出登录

TCL+ 云端可能只允许同一账号保持有限数量的有效登录会话。使用本集成登录后，手机 TCL+ App 可能会被挤下线，需要在手机 App 中重新登录。

建议安装前确认你知道 TCL+ App 的账号密码，并能正常重新登录手机 App。

## 更新

### HACS 更新

在 HACS 中更新后重启 Home Assistant。

### 手动更新

替换 `custom_components/tclplus_ac` 目录后重启 Home Assistant。

## 卸载

1. 在 Home Assistant 的“设备与服务”中删除 `TCL+ AC` 集成条目。
2. 删除 `custom_components/tclplus_ac` 目录。
3. 重启 Home Assistant。
