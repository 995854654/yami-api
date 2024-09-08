# yami-api

## 版本依赖

-   python3.9



## 技术栈

|       name       | version |      remark      |
| :--------------: |:-------:| :--------------: |
|     fastAPI      | 0.110.2 |  python Web框架  |
|      loguru      |  0.7.2  |   异步日志模块   |
|     pydantic     |  2.7.0  |  python对象模型  |
|      pyjwt       |  2.8.0  |     安全模块     |
|      pytest      |  8.1.1  |     单元测试     |
|     uvicorn      | 0.29.0  | 运行fastAPI工具  |
|    sqlalchemy    | 2.0.21  |     ORM模型      |
|      Pyyaml      |  6.0.1  | 读取yaml配置文件 |
| python-multipart |  0.0.9  |   接收表单数据   |
|     passlib      |  1.7.4  |      加密库      |
|      bcrypt      |  4.0.1  |    加密算法包    |


## 项目进度

- infrastructure
    - [X] logging
    - [X] security - JWT
- function requirement
- non-function requirement
- LLM
    - [ ] GPT3
    - [ ] GPT3.5
    - [X] moonshot
- data transmission
    - [X] http
    - [ ] websocket

## 部署
1. 安装ffmpeg, `https://ffmpeg.org/`

cicd: continue integrate continue deploy
1. 在项目根目录运行:`./cicd/build.sh`

