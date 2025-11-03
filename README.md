# Netlib.re 单账号登录保活脚本

## 项目简介

本项目用于自动登录 [Netlib.re](https://www.netlib.re/) 网站，实现账号保活。适用于需要每隔一段时间（如 30 天）登录一次的网站场景。支持登录失败判定、延迟和网页加载等待，防止被风控。支持 GitHub Actions 自动运行（无头模式），成功登录后停留 5 秒，用于保活或刷新 Cookie。仅用于登录保活，不涉及敏感操作。

## 功能说明

1. **登录成功判断**：

   * 成功条件：页面出现 `You are the exclusive owner of the following domains.`
   * 失败条件：出现以下提示之一：

     * `Invalid credentials.`
     * `Not connected to server.`
     * `Error with the login: login size should be between 2 and 50 (currently: 1)`
   * 其他情况判定为失败。
2. **延迟与等待**：

   * 打开网页等待 5 秒
   * 每个操作步骤间隔 2 秒
   * 登录成功后停留 5 秒
3. **GitHub Actions 自动运行**：

   * 支持定时任务（如每月 1 号和 31 号）
   * 支持手动触发

## 使用方式（Fork 部署）

1. **Fork 仓库**

   * 点击 GitHub 仓库页面右上角 `Fork` 将本项目复制到自己的账户。

2. **配置 Secrets**

   * 在仓库 `Settings` → `Secrets and variables` → `Actions` → `New repository secret` 中为单个账号添加用户名和密码，例如：

`UZANTONOMO`填入：你的用户名  
`PASVORTO`填入：你的密码  
`TELEGRAM_SIGNALO`填入：你的机器人token  
`TELEGRAM_BABILO_ID`填入：你的id  

6. **GitHub Actions 自动运行**

* `.github/workflows/keepalive.yml` 已包含 workflow 配置
* 默认自动执行：每月 1 号和 31 号
* 手动触发：Actions 页面点击 Run workflow
* Actions 日志显示每个账号的登录结果

## 注意事项

1. 确保账号密码正确，否则登录会判定失败。
2. 本项目仅用于登录保活，不支持操作其他敏感功能。
3. 如果网站增加防刷机制或修改页面元素，脚本可能需要更新。
4. GitHub Actions 免费账户有执行时长限制，适合少量账号保活。

## 项目结构

```
netlib-keepalive/
├─ login.py               # 单账号登录脚本
├─ .github/
│  └─ workflows/
│     └─ keepalive.yml   # GitHub Actions 工作流
└─ README.md              # 项目介绍与使用说明
```
## 许可证

MIT License
