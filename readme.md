# Speechless

一个普通的基于Nonebot的实现

<u>**注意：只支持Windows环境，不兼容Windows8.1及以下**</u>

![python](https://img.shields.io/badge/python-v3.10%2B-blue)![nonebot](https://img.shields.io/badge/nonebot-v2.3.3-yellow)![onebot](https://img.shields.io/badge/onebot-v11-black)

## 1.安装

#### 准备

自行安装python3.11+，git，在cmd中执行以下操作（# 后为注释无需执行）

#### 克隆

```
# 通过github安装
git clone https://github.com/yeqiu6080/Speechless.git
# 或通过github镜像安装
git clone https://ghproxy.net/https://github.com/yeqiu6080/Speechless.git
```
### 以下操作均在克隆的speechless目录下执行

#### 换源&创建虚拟环境&安装依赖

```
# 推荐阿里源，不限速
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
pip config set install.trusted-host mirrors.aliyun.com
# 创建虚拟环境
python -m venv .venv --prompt Speechless
# 激活虚拟环境
.venv\Scripts\activate
# 安装pipx
python -m pip install --user pipx
python -m pipx ensurepath

```

关闭当前窗口，然后重新打开一个cmd
```
# 安装poetry，nb脚手架
pipx install nb-cli
pipx install poetry
# 激活虚拟环境
.venv\Scripts\activate
# 安装依赖
poetry install

```

## 2.使用

```
# 运行
nb run

```

### 连接协议端

本项目符合 [OneBot11](https://github.com/howmanybots/onebot) 标准，可基于以下项目与机器人框架/平台进行交互

|                           项目地址                           |  平台  |         核心作者         | 状态 |
| :----------------------------------------------------------: | :----: | :----------------------: | ---- |
|    [👍推荐LLOneBot](https://github.com/LLOneBot/LLOneBot)     |  NTQQ  |        linyuchen         | 维护 |
|    [Shamrock](https://whitechi73.github.io/OpenShamrock)     | Xposed |        whitechi73        | 归档 |
|        [Napcat](https://github.com/NapNeko/NapCatQQ)         |  NTQQ  |         NapNeko          | 维护 |
| [Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core) |        | LagrangeDev/Linwenxuan04 | 维护 |
|      [Yunzai](https://gitee.com/xiaoye12123/ws-plugin)       |        |                          | 维护 |

反向 WebSocket 连接

> 配置 OneBot 实现的 ws reverse 相关配置，并将上报地址改为以下地址其一： 
>
> ws://127.0.0.1:1451/onebot/v11/ 
>
> ws://127.0.0.1:1451/onebot/v11/ws 
>
> ws://127.0.0.1:1451/onebot/v11/ws/

## 恭喜🎉🎉

到这里，你已经完成安装了
## 更新
```
# 放弃更改（注意备份）
git checkout .
# 更新
git pull
# 激活虚拟环境
.venv\Scripts\activate
# 安装依赖
poetry install

```