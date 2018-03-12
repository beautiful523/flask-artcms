# flask_artcms
### 实战小项目
#### 1.搭建开发环境
创建项目
interpreter添加flask
#### 2.构建项目目录
#### 3.开发前端模板
#### 4.设计数据模型
操作mysql, mariadb和MySQL的操作是一样的
\s查看当前状态
若不是则将数据库的字符集改为utf-8
对比原生语句创建数据表和model的方法创建数据表
原生的缺点，查询也要原生语句，换数据库会有迁移的问题
原生修改表字段：
alter table art modify logo varchar(100) not null;

#### 5.wtforms定义表单
pip3 install flask-wtf
#### 6.验证码
pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com pillow
#### 6.编写后端逻辑
#### 7.测试部署上线
- 入口：127.0.0.1:8080/login/
- 数据库：mysql数据库名 artcms
- 软件如下图

![Aaron Swartz](https://github.com/beautiful523/flask_artcms/blob/master/1520502564892.jpg)
![avatar](/Users/admin/Documents/1520502564892.jpg)