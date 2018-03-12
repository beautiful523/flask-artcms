# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from models import User
from flask import session


class LoginForm(FlaskForm):
    name = StringField(
        label=u"账号",
        validators=[
            DataRequired(u"账号不能为空")
        ],
        description=u"账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号"
        }
    )
    pwd = PasswordField(
        label=u"密码",
        validators=[
            DataRequired(u"密码不能为空")
        ],
        description=u"密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码"
        }
    )
    submit = SubmitField(
        u"登录",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_pwd(self, field):
        pwd = field.data
        user = User.query.filter_by(name=self.name.data).first()
        if not user.check_pwd(pwd):
            raise ValidationError(u"密码不正确")


class RegisterForm(FlaskForm):
    name = StringField(
        label=u"账号",
        validators=[
            DataRequired(u"账号不能为空")
        ],
        description=u"账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号"
        }
    )
    pwd = PasswordField(
        label=u"密码",
        validators=[
            DataRequired(u"密码不能为空")
        ],
        description=u"密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码"
        }
    )
    repwd = PasswordField(
        label=u"确认密码",
        validators=[
            DataRequired(u"确认密码不能为空"),
            EqualTo('pwd', message=u"两次输入密码不一致")
        ],
        description=u"确认密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入确认密码"
        }
    )
    code = StringField(
        label=u"验证码",
        validators=[
            DataRequired(u"验证码不能为空")
        ],
        description=u"验证码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入验证码"
        }
    )
    submit = SubmitField(
        u"注册",
        render_kw={
            "class": "btn btn-success"
        }
    )

    def validate_name(self, field):  # validate_name就指定了验证的是name那一栏
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user > 0:
            raise ValidationError(u"账号已存在，不能重复注册")

    # 自定义验证码验证功能
    def validate_code(self, field):
        code = field.data
        # if not session.has_key("code"):
        #     raise ValidationError(u"没有验证码")
        if session["code"].lower() != code.lower():
            raise ValidationError(u"验证码不正确")


class ArtForm(FlaskForm):
    title = StringField(
        label=u"标题",
        validators=[
            DataRequired(u"标题不能为空")
        ],
        description=u"标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入标题"
        }
    )
    cate = SelectField(
        label=u"分类",
        validators=[
            DataRequired(u"分类不能为空")
        ],
        description=u"分类",
        choices=[(1, u"科技"), (2, "搞笑"), (3, "军事")],
        default=3,
        coerce=int,
        render_kw={
            "class": "form-control",
        }
    )
    logo = FileField(
        label=u"封面",
        validators=[
            DataRequired(u"封面不能为空")
        ],
        description=u"封面",
        render_kw={
            "class": "form-control-file",
        }
    )
    content = TextAreaField(
        label=u"内容",
        validators=[
            DataRequired(u"内容不能为空")
        ],
        description=u"内容",
        render_kw={
            "style": "height:300px",
            "id": "content"
        }
    )
    submit = SubmitField(
        u"发布文章",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class ArtEditForm(FlaskForm):
    id = IntegerField(
        label=u"编号",
        validators=[
            DataRequired(u"编号不能为空")
        ],

    )
    title = StringField(
        label=u"标题",
        validators=[
            DataRequired(u"标题不能为空")
        ],
        description=u"标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入标题"
        }
    )
    cate = SelectField(
        label=u"分类",
        validators=[
            DataRequired(u"分类不能为空")
        ],
        description=u"分类",
        choices=[(1, u"科技"), (2, "搞笑"), (3, "军事")],
        coerce=int,
        render_kw={
            "class": "form-control",
        }
    )
    logo = FileField(
        label=u"封面",
        # validators=[
        #     DataRequired(u"封面不能为空")
        # ],
        # 编辑文章的时候可以不选取封面，封面保留为原封面
        description=u"封面",
        render_kw={
            "class": "form-control-file",
            "style": "display:None;",
            "id": "logo"
        }
    )
    content = TextAreaField(
        label=u"内容",
        validators=[
            DataRequired(u"内容不能为空")
        ],
        description=u"内容",
        render_kw={
            "style": "height:300px",
            "id": "content"
        }
    )
    submit = SubmitField(
        u"文编辑章",
        render_kw={
            "class": "btn btn-primary"
        }
    )
