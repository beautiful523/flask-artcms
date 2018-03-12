# coding:utf8
import os
import uuid

from flask import Flask, render_template, redirect, flash, session, Response, request, url_for
from werkzeug.security import generate_password_hash
from functools import wraps

from werkzeug.utils import secure_filename

from forms import LoginForm, RegisterForm, ArtForm, ArtEditForm
from models import User, db, Art
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
app.config["UP"] = os.path.join(os.path.dirname(__file__), "static/uploads")


# 登录装饰器
def user_login_req(f):
    @wraps(f)
    def login_req(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return login_req


# 登录
@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        session["user"] = data["name"]
        flash("登录成功", "ok")
        return redirect("/art/list/1/")
    return render_template("login.html", title=u"登录", form=form)


# 注册
@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            addtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(user)
        db.session.commit()
        # 定义一个会话闪现
        flash(u"注册成功，请登录", "ok")
        return redirect("/login/")
    else:
        flash(u"输入正确信息注册", "err")
    return render_template("register.html", title=u"注册", form=form)


# 退出(302跳转到登录页面)
@app.route("/logout/", methods=["GET"])
@user_login_req
def logout():
    session.pop("user", None)
    # return redirect(url_for("app.login"))
    return redirect("/login/")


# 修改文件名称
def change_name(name):
    # name = 2431424aa05068432cdb5e8f7d73518a.jpg
    info = os.path.splitext(name)
    # info = ('2431424aa05068432cdb5e8f7d73518a', '.jpg')
    # info[-1]是文件名的后缀
    name = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + info[-1]
    # name = 20180307155439 4f41caa69d604ff08b61170c20022900 .jpg
    return name


# 发布文章
@app.route("/art/add/", methods=["GET", "POST"])
@user_login_req
def art_add():
    form = ArtForm()
    if form.validate_on_submit():
        data = form.data
        # 上传logo
        # uploads里面存的是图片文件
        # 数据库里存的是uploads里面的图片的文件名
        file = secure_filename(form.logo.data.filename)
        logo = change_name(file)
        # logo是时间加唯一标志服加图片文件后缀
        if not os.path.exists(app.config["UP"]):
            os.makedirs(app.config["UP"])
        form.logo.data.save(app.config["UP"] + "/" + logo)

        # 获取用户ID
        user = User.query.filter_by(name=session["user"]).first()
        user_id = user.id

        # 保存数据
        art = Art(
            title=data["title"],
            cate=data["cate"],
            user_id=user_id,
            logo=logo,
            content=data["content"],
            addtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(art)
        db.session.commit()
        flash(u"发布文章成功", "ok")

    return render_template("art_add.html", title=u"发布文章", form=form)


# 编辑文章
@app.route("/art/edit/<int:id>/", methods=["GET", "POST"])
@user_login_req
def art_edit(id):
    art = Art.query.get_or_404(int(id))
    form = ArtEditForm()
    if request.method == "GET":
        form.content.data = art.content
        form.cate.data = art.cate
        form.title.data = art.title
        # logo不能传默认文件，因为这个字段是在本地选择图片，数据库里的图片本地不一定有
        # 封面下的图怎样跟随选取的文件变化 todo

    if form.validate_on_submit():
        data = form.data
        if form.logo.data:
            file = secure_filename(form.logo.data.filename)
            logo = change_name(file)
            # logo是时间加唯一标志服加图片文件后缀
            if not os.path.exists(app.config["UP"]):
                os.makedirs(app.config["UP"])
            # 将图存到这个文件地址：
            form.logo.data.save(app.config["UP"] + "/" + logo)
            art.logo = logo
        art.title = data["title"]
        art.content = data["content"]
        art.cate = data["cate"]
        # db.session.add(art)
        db.session.commit()
        flash(u"编辑文章成功", "ok")
        # 存数据为什么会存之前的：
        # 因为不判断get的话，在post时也会执行form赋值，且在数据库更新之前，所以存的是之前的。
    return render_template("art_edit.html", form=form, title="编辑文章", art=art)


# 删除文章
@app.route("/art/del/<int:id>/", methods=["GET"])
@user_login_req
def art_del(id):
    art = Art.query.get_or_404(int(id))
    db.session.delete(art)
    db.session.commit()
    flash(u"删除《%s》成功" % art.title, "ok")
    return redirect("/art/list/1/")


# 文章列表
@app.route("/art/list/<int:page>/", methods=["GET"])
@user_login_req
def art_list(page=None):
    # 什么时候可以不传页码？TODO
    if page is None:
        page = 1
    user = User.query.filter_by(name=session["user"]).first()
    page_data = Art.query.filter_by(
        user_id=user.id
    ).order_by(
        Art.addtime.desc()
    ).paginate(
        page=page, per_page=3
    )  # 获得我的所有文章并分页显示当前页
    cate = [(1, u"科技"), (2, "搞笑"), (3, "军事")]
    return render_template("art_list.html", title=u"文章列表", page_data=page_data, cate=cate)


# 验证码

@app.route("/codes/", methods=["GET"])
def codes():
    from codes import Codes
    c = Codes()
    info = c.create_code()  # 创建了验证码的同时返回了图片名和字符串
    image = os.path.join(os.path.dirname(__file__), "static/code") + "/" + info["img_name"]
    i = open(image, 'rb')
    session["code"] = info["code"]
    return Response(i, mimetype="jpeg")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8888)
