# dvadmin_celery_backend

#### 介绍
dvadmin用来全局拦截指定请求方式及请求插件

## 安装包

使用pip安装软件包：

~~~python
pip install dvadmin-request-intercept
~~~
在INSTALLED_APPS 中注册app

~~~python
INSTALLED_APPS = [
    ...
    'dvadmin_request_intercept',
]
~~~

在 application / settings.py 下添加配置

~~~python
MIDDLEWARE = [
    ...
    'dvadmin_request_intercept.middleware.RequestInterceptMiddleware',
]
~~~

在 application / settings.py 下注册插件

```python
# dvadmin 插件
REGISTER_PLUGINS = (
    ...
    "dvadmin_request_intercept"
)
```
