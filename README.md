# yami-api

## 版本依赖

-   python3.9



## 技术栈

|   name   | version |     remark      |
| :------: | :-----: | :-------------: |
| fastAPI  | 0.110.2 | python Web框架  |
|  loguru  |  0.7.2  |  异步日志模块   |
| pydantic |  2.7.0  |      模型       |
|  pyjwt   |  2.8.0  |    安全模块     |
|  pytest  |  8.1.1  |    单元测试     |
| uvicorn  | 0.29.0  | 运行fastAPI工具 |


## 项目进度

- [ ] infrastructure
    - [X] logging
    - [ ] security - JWT
- [ ] function requirement
- [ ] non-function requirement
- [ ] LLM
    - [ ] GPT3
    - [ ] GPT3.5
- [ ] data transmission
    - [X] http
    - [ ] websocket

## 部署
cicd: continue integrate continue deploy
1. 在项目根目录运行:`./cicd/build.sh`