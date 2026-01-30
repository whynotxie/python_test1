# Simple Kivy Android App

这是一个最小的 Kivy 应用示例，包含一个按钮和标签，按下按钮会增加计数并显示时间。

本地运行（Windows/桌面）:

```powershell
python python_test1\kivy_app\main.py
```

在 Android 上打包（建议在 WSL 或 Linux 环境中使用 Buildozer）：

1. 安装 buildozer 环境（在 Linux/WSL）：

```bash
sudo apt update
sudo apt install -y python3-pip build-essential git python3-setuptools
pip3 install --user buildozer
```

2. 进入项目目录并初始化（可选）：

```bash
cd python_test1/kivy_app
buildozer init
```

3. 编辑 `buildozer.spec`（本目录已有示例），然后运行：

```bash
buildozer -v android debug
```

这会生成一个可安装的 APK（需要 Android SDK/NDK，参见 Buildozer 文档）。

注意事项：
- 建议在 WSL2 或 Linux 环境中运行 `buildozer`，Windows 原生打包支持性差。
- 在 `buildozer.spec` 中把 `icon.filename` 指向一个 512x512 的 PNG（例如 `icon.png`），否则会使用默认图标。
- `android.api` 和 `android.ndk` 需要与 Buildozer 文档推荐值匹配（上面示例使用 `android.api = 33` 和 `android.ndk = 25b`）。

示例完整打包流程（WSL/Ubuntu）：

```bash
# 安装依赖（仅示例）
sudo apt update
sudo apt install -y python3-pip build-essential git zlib1g-dev libssl-dev libffi-dev
pip3 install --user buildozer

# 初始化并打包
cd python_test1/kivy_app
buildozer init            # 可选，生成/更新 buildozer.spec
buildozer android debug
```

运行时权限说明：

- `buildozer.spec` 中的 `android.permissions` 会把相应权限写入 AndroidManifest，但从 Android 6.0 开始，敏感权限必须在运行时请求（runtime permission）。
- 常见需要在运行时请求的权限包括：`CAMERA`（摄像头）、`RECORD_AUDIO`（麦克风）、`ACCESS_FINE_LOCATION`（精确定位）、`READ_EXTERNAL_STORAGE` / `WRITE_EXTERNAL_STORAGE`（存储）。
- 在 Kivy 中可使用 `android.permissions` 模块或第三方库（如 `plyer`）来请求运行时权限；打包后在设备上首次使用相关功能时应询问用户授权。

示例（请求权限的思路，非完整代码）：

```python
from android.permissions import request_permissions, Permission

def ask_perms():
	request_permissions([Permission.CAMERA, Permission.RECORD_AUDIO])
```

如果你希望我把示例运行时权限请求代码加入 `main.py`，我可以把简单的请求逻辑和说明一并添加。

签名与发布说明：

- 本地调试（`buildozer android debug`）会使用默认的调试签名，直接生成可安装的调试 APK。
- 发布到 Google Play 前，必须对 APK 进行签名并使用合适的 `version_code`（在 `buildozer.spec` 中为 `android.version_code`）。
- 在 `buildozer.spec` 中填写签名相关字段（示例已包含注释）：
	- `android.keystore` — 指向你的 keystore 文件路径
	- `android.keystore_password` — keystore 密码
	- `android.keyalias` — key alias
	- `android.keyalias_password` — alias 密码
	- `android.release = 1` — 启用 release 打包
- 推荐在安全的环境（例如 CI 或受控机器）中保存和使用 keystore 密码，避免将明文密码提交到仓库。可以使用环境变量或 CI secret 注入。

示例：在 Linux/WSL 下使用 release 签名打包的基本流程：

```bash
cd python_test1/kivy_app
# 在 buildozer.spec 中填写 android.keystore 等签名字段，或把密码通过环境变量注入
# 运行 release 打包（可能需要更长时间并下载依赖）
buildozer android release
```

完成后，生成的签名 APK 位于 `bin/` 目录，可以进一步使用 `jarsigner` 或 `apksigner` 验证签名。

---

Android 验证步骤（在真实设备上测试运行时权限）

1) 先决条件
- 在开发机安装 Buildozer（建议 WSL2/Ubuntu）并准备 Android SDK/NDK。
- 设备开启 USB 调试并连接到电脑；确认能用 `adb devices` 看到设备。
- 确认 `buildozer.spec` 中的 `package.name` 与 `package.domain` 配置正确（示例：`org.example.simplekivyapp`）。

2) 打包、部署并运行（在项目目录）
```bash
cd python_test1/kivy_app
# 构建、部署并运行调试 APK（需要较长时间，且需网络）
buildozer android debug deploy run
```
或者使用 adb 手动安装并启动：
```bash
adb install -r bin/org.example.simplekivyapp-0.1-debug.apk
adb shell am start -n org.example.simplekivyapp/org.kivy.android.PythonActivity
```

3) 在设备上验证交互
- 打开应用，点击 `Request Permissions` 按钮。系统会弹出权限请求对话框（一次或逐项，取决于 Android 版本）。
- 允许或拒绝后，应用界面应更新为类似：
	`Permissions: CAMERA:GRANTED, RECORD_AUDIO:GRANTED, ...`（由回调写入）。

4) 通过 ADB 检查权限状态
- 检查单个权限：
```bash
adb shell pm check-permission org.example.simplekivyapp android.permission.CAMERA
# 返回: granted 或 denied
```
- 查包信息并筛选已授予权限：
```bash
adb shell dumpsys package org.example.simplekivyapp | grep granted=true
```

5) 收集运行时日志（若需要排查）
```bash
adb logcat | grep python
# 或查看 Kivy/log 输出以调试回调行为
```

6) 卸载测试 APK
```bash
adb uninstall org.example.simplekivyapp
```

预期结果
- 系统权限对话框应出现并允许用户授权。
- 授权后，应用标签显示每个权限的 GRANTED/DENIED 状态（由 `_permission_callback` 写入 `label_text`）。

如果你希望，我可以把上述验证步骤加入到一个可执行的 shell 脚本中来自动化安装、运行与日志收集。

自动化脚本说明

本目录包含 `android_test.sh`，用于在 WSL/Linux 环境下自动化构建、部署、运行和收集日志（依赖 `buildozer` 和可选的 `adb`）：

使用方法：

```bash
cd python_test1/kivy_app
chmod +x android_test.sh
./android_test.sh        # 构建、部署并收集日志（如果有 adb）
./android_test.sh clean  # 清理 buildozer 后再构建
```

脚本功能：
- 使用 `buildozer -v android debug` 构建调试 APK（需要网络和较长时间）。
- 如果 `adb` 可用，脚本会尝试安装 APK、启动应用并收集 `logcat`（保存为 `android_test_log.txt`）。
- 若 `adb` 不可用，脚本仅构建 APK 并提示你手动部署。

注意：在 Windows 主机上请在 WSL2/Ubuntu 中运行此脚本以获得最佳兼容性。
