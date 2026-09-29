# 协议模型自动更新

游戏返回 HTTP 428 时，原有版本更新入口会在工作线程中完成：

```text
APKPure StreamZip 下载入口
  → 提取 ARM64 libil2cpp.so / global-metadata.dat
  → Python 解码保护层、恢复 ELF 和重定位
  → Python 读取 IL2CPP 类型注册、字段、属性、泛型、枚举和 URL
  → 直接生成 Python 协议模型
  → 独立加载并校验全部模型
  → 原子保存版本信息及模型指针，切换注册表
  → 重新登录、重试请求
```

整个生成流程在当前 Python 进程中执行，不启动外部命令。不需要 .NET、C# 编译器、Il2CppDumper 程序、DummyDll、Unicorn 或 ARM 解码二进制。ELF 解析使用 `pyelftools`，AES 使用项目已有的 `pycryptodome`；其余解码及模型生成逻辑由 Python 实现。这些是 Python 包依赖，不要求所有依赖自身都由 Python 编写。

## 使用

安装 `requirements.txt` 即可，使用 64 位 Python。完整恢复需要读取数百 MB 的二进制，并保留中间结果；运行时应预留数 GB 内存和磁盘空间，本机两版样本每次完整生成约两分钟。

```powershell
pip install -r requirements.txt

# 检查 APKPure 最新版本，生成模型并激活
python _version_update.py

# 使用本地 XAPK，完整生成并激活
python _version_update.py --apk 'D:\path\game.xapk'

# 仅生成、校验，不改变当前版本
python _version_update.py --apk 'D:\path\game.xapk' --prepare-only

# 在独立缓存中验证整个更新流程
python _version_update.py --apk 'D:\path\game.xapk' --cache-dir cache\protocol-test-run
```

服务内的 HTTP 428 路径会直接更新当前进程。单独运行 CLI 会更新磁盘状态；其他已运行进程需要重启，或在它自己的 428 更新流程中加载新版。服务重启时按 `version.json` 的模型指针直接加载，不重新 Dump。`AUTOPCR_CACHE_DIR` 可配置缓存目录。

## 动态类代理

原有 `autopcr.model.requests/responses/common/enums` 导入路径保持可用。公开名称是稳定的类代理，构造、`parse_obj` 等类方法以及枚举访问在调用时查找实际类。生成结果写入缓存，源码 `_bundled/` 保存首次运行的模型。

```python
from autopcr.model.requests import LoginApiLoginRequest
from autopcr.model.responses import LoginApiLoginResponse

# 即使这些名称在更新前已被导入，以下调用仍使用当前注册表。
request = LoginApiLoginRequest(appVersion="3.19.1")
response = LoginApiLoginResponse.parse_obj({"userId": 123})
```

注册表按 requests/responses/common/enums 分组，整套替换，避免嵌套类型和响应泛型混用版本。需要实际 Pydantic 类做继承或复杂反射时可调用：

```python
from autopcr.model.registry import resolve
actual_class = resolve("requests", "LoginApiLoginRequest")
```

`handlers.py` 的业务处理函数按响应名称注册，并附加到每代实际响应类。发送前会把排队的旧请求转换成当前类；发送时固定该请求的签名和版本，响应按该请求对应的实际类型解析。旧实例不会被原地改写。

所有模型加载成功且处理函数目标存在后，才替换当前注册表。版本号、签名、库数量、模型路径及校验值在同一个 `version.json` 中，通过临时文件和 `os.replace` 保存。解码、生成、校验或持久化失败时不激活新版；进程内并发更新合并执行。APKPure 尚无新版时返回明确错误，避免无限重试。

## 实现与产物

- `autopcr/model/il2cpp/decoder.py`：保护格式的整数变换、AES 包解码、前缀码及重复/回溯解压。
- `recovery.py`：定位保护层、恢复分层模块、重建 ELF 和重定位。
- `metadata.py`：定位 IL2CPP metadata registration，解析元数据、泛型和常量。
- `protocol.py`：提取协议结构并生成四个模型模块。
- `autopcr/model/update.py`：复用下载入口，管理缓存、日志和模型校验。

缓存目录 `cache/protocol/<版本>-<指纹>/` 保存 `input.json`（输入及实现校验值）、`pipeline.log`、`analysis/`（恢复中间结果）、`extracted/il2cpp/libil2cpp.restored.so`、`models/`（四个 Python 模块、`protocol.json` 计数、`protocol.schema.json` 协议结构）及 `complete.json`（模型校验值）。实现代码改变会影响缓存指纹。

这个实现覆盖自动协议更新所需的 IL2CPP 内容，直接生成模型，不导出完整 DummyDll、方法反汇编或 IDA 脚本。元数据布局和压缩常量参考 Il2CppDumper 的 MIT 源码，许可保存在 `autopcr/model/il2cpp/LICENSE.Il2CppDumper`；协议映射规则移植自现有 `MagiaExedra/ProtocolGen`。本工作区的旧工具已归档到 `cache/legacy-protocol-tools/`，不参与运行、版本管理或 Docker 构建。

## 兼容范围与验证

支持 little-endian ARM64 ELF、metadata 29/31 的已实现布局，以及本次验证的保护格式。已用 3.16.1、3.19.1 实际安装包验证。识别到保护加载器改变、未知类型或非法结构时会停止，保留当前活动版本，后续需要适配。普通未保护 ELF 可直接进入元数据解析，但并非所有 Unity 版本都已验证。

接口删除、新增必填业务参数或业务含义改变仍可能需要修改调用代码。自动生成模型不能代替业务适配。

```powershell
python -m unittest discover -s tests -p 'test_protocol*.py' -v

# 使用真实两版生成结果验证热切换
$env:AUTOPCR_PROTOCOL_TEST_RUNS = 'cache\protocol-python-e2e\protocol'

# 可选：与旧 C# 生成结果逐项比较字段、泛型、枚举、URL
$env:AUTOPCR_PROTOCOL_BASELINE = 'cache\protocol-test'
python -m unittest discover -s tests -p 'test_protocol*.py' -v

# 可选：从 XAPK 重跑完整流程，测试期间禁止启动子进程；使用独立临时缓存
$env:AUTOPCR_PROTOCOL_TEST_APKS = 'D:\path\xapks'
python -m unittest discover -s tests -p 'test_protocol_python.py' -v
```

XAPK 完整测试需要目录中有 `Madoka+Magica+Magia+Exedra_3.16.1_APKPure.xapk` 和 `Madoka+Magica+Magia+Exedra_3.19.1_APKPure.xapk`，会占用约数 GB 临时磁盘空间，测试结束后清理。
