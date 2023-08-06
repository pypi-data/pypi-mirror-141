# dvadmin-upgrade-center

#### 介绍
dvadmin-upgrade-center 是一款升级中心后端插件。

## 安装包

使用pip安装软件包：

~~~python
pip install dvadmin-upgrade-center
~~~

在INSTALLED_APPS 中注册app

~~~python
INSTALLED_APPS = [
    ...
    'dvadmin_upgrade_center',
]
~~~

在 application / urls.py 中注册url地址

~~~python
urlpatterns = [
    ...
    re_path(r'api/dvadmin_upgrade_center/', include('dvadmin_upgrade_center.urls')),
]
~~~

进行迁移及初始化
```python
python3 manage.py makemigrations 
python3 manage.py migrate 
# 注意备份初始化信息
python3 manage.py init -y 
```
