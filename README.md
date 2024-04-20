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


## FAQ

### fastAPI文档加载异常
原因：因为fastAPI文档使用了外网CDN的资源，所以需要将资源保存到本地

解决链接：`https://blog.csdn.net/m0_52726759/article/details/124854070?spm=1001.2014.3001.5502`

1. 在`Lib/site-package/fastapi/openapi/docs.py`修改swagger url
    ```python
      
   def get_swagger_ui_html():
        ...
        swagger_js_url: str = "/static/swagger-ui/swagger-ui-bundle.js"
        swagger_css_url: str = "/static/swagger-ui/swagger-ui.css"
        swagger_favicon_url: str = "/static/swagger-ui/favicon.png"
   
   def get_redoc_html():
        ...
        redoc_js_url:str = "/static/bundles/redoc.standalone.js"
   ```
2. 在fastAPI应用中添加以下代码：
    ```python
    from fastapi import FastAPI
    from starlette.staticfiles import StaticFiles
    app = FastAPI()
    # 将OpenAI docs代码接管到本地中
    app.mount("/static", StaticFiles(directory="static"), name="static")
    ```