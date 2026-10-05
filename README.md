# autopcr

[![License](https://img.shields.io/github/license/cc004/autopcr)](LICENSE)

自动清日常
bug反馈/意见/交流群: 885228564

请先运行一次`python3 _download_web.py`下载前端资源。脚本会选择与后端 API 主版本、次版本匹配的最新前端补丁版本，而不是直接安装上游最新版本。

如果网络不好，可从[前端发布列表](https://github.com/Lanly109/AutoPCR_Web/releases)下载与 `autopcr/http_server/version.py` 中版本匹配的 `web.zip`（当前为 **1.7.x**），然后`python3 _download_web.py /path/to/zip`安装。不要直接下载 `latest`，它可能与本后端不兼容。

如果登录或注册提示“后端期望前端版本为…”，重新运行 `python3 _download_web.py` 安装匹配的前端，再刷新网页。无需关闭后端版本校验，也无需修改游戏安装包或版本指纹。

## Docker 构建

镜像构建过程中会执行 `_download_web.py`，这一步要访问 GitHub API。匿名请求限额只有 **60 次/小时**，在 Docker 构建、共享出口 IP 或代理环境下很容易报 `403 rate limit exceeded`。两个可选构建参数可以规避：

| 构建参数           | 说明                                                        |
|----------------|-----------------------------------------------------------|
| `GITHUB_TOKEN` | 走认证请求，限额提升到 5000 次/小时。只读公开仓库无需任何 scope，传一个最小权限 token 即可 |
| `WEB_ZIP`      | 完全跳过网络：把与后端匹配的 `web.zip` 放进构建上下文，构建时直接解压安装                 |

```bash
# 方式一：带 token 构建（推荐）
docker build --build-arg GITHUB_TOKEN=ghp_xxx -t automadoka .

# 方式二：离线，先把 web.zip 放到项目根目录
docker build --build-arg WEB_ZIP=web.zip -t automadoka .
```

注意 `--build-arg` 的值会留在镜像历史里，别传长期有效的个人 token；建议用只读的 fine-grained token。

## HTTP 服务器模式

```bash
python3 _httpserver_test.py
```

访问`/daily/login`

## Hoshino插件模式

使用前请更新Hoshino到最新版，并**更新Hoshino的配置文件`__bot__.py`**

## 渠道服支持

渠道服需要自抓`uid`和`access_key`，作为用户名和密码。

## 配置

| 环境变量                          | 描述            | 默认值（留空则表示必填）     |
|-------------------------------|---------------|------------------|
| AUTOPCR_SERVER_PORT           | 自定义服务器启动端口    | 13200            |
| AUTOPCR_SERVER_DEBUG_LOG      | 是否输出 Debug 日志 | False            |
| AUTOPCR_SERVER_ALLOW_REGISTER | 是否允许注册        | True             |
| AUTOPCR_SERVER_SUPERUSER      | 设置无条件拥有管理员的用户 | （可选，设置为登录使用的 QQ） |

## Credits
- aiorequests 来自 [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)
- 图片绘制改自 [convert2img](https://github.com/SonderXiaoming/convert2img)
- 前端html来自 [AutoPCR_Web](https://github.com/Lanly109/AutoPCR_Web)
- ~~前端html来自 [autopcr_web](https://github.com/cca2878/autopcr_web)~~
- ~~前端html来自 [AutoPCR_Archived](https://github.com/watermellye/AutoPCR_Archived)~~
- ~~模型生成来自 [PcrotoGen](https://github.com/cc004/PcrotoGen)~~

## Github Action（打包镜像仅适用于HTTP服务器模式）
打包镜像默认推送到[ghcr](https://ghcr.io),如需推送到[dockerhub](https://hub.docker.com)需要执行以下步骤
- 添加变量`DOKCKERHUB_IMAGE_NAME`用于推送到dockerhub镜像名称,例如autopcr/autopcr
- 添加机密`DOCKERHUB_USERNAME`和`DOCKERHUB_TOKEN`用于推送到dockerhub的身份验证

## Protocol model updates

APK version updates now recover IL2CPP and generate protocol models directly in Python, then atomically activate them. No external commands or .NET tools are needed. See [setup, offline updates and verification](docs/protocol-model-updates.md).
