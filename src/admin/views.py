from src.models import Plant, Question
from src.ext import db, admin  # or pass these as arguments if you prefer decoupling
from src.models import User
from src.config import Config

from flask_admin import AdminIndexView, expose
from flask_admin.form.upload import ImageUploadField
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user
from flask import redirect, url_for, request, render_template
from wtforms import TextAreaField
from markupsafe import Markup


class MyAdminIndexView(AdminIndexView):
    def is_visible(self):
        return False

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super().index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('admin.index'))
        return render_template('admin_login.html')

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.login_view'))



class AuthModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class PlantAdmin(AuthModelView):
    form_extra_fields = {
        'image': ImageUploadField(
            label='Image',
            base_path=Config.UPLOAD_PATH,
            relative_path='',
            url_relative_path='/static/',
            allowed_extensions=['jpg', 'png', 'jpeg']
        )
    }

    column_formatters = {
        'image': lambda v, c, m, p: Markup(f'<img src="/static/{m.image}" style="height: 100px;">') if m.image else '',
        'description': lambda v, c, m, p: (m.description[:100] + '...') if m.description and len(
            m.description) > 100 else m.description
    }
    form_overrides = {'description': TextAreaField}
    form_widget_args = {
        'description': {'rows': 10, 'style': 'width: 100%; font-size: 16px;'}
    }

    form_columns = ['name', 'eng_name', 'family_name', 'family_name_geo', 'description', 'image']
    column_searchable_list = ['name', 'eng_name', 'family_name', 'family_name_geo', ]


class QuestionAdmin(AuthModelView):
    form_extra_fields = {
        'image': ImageUploadField(
            label='Image',
            base_path=Config.UPLOAD_PATH,
            relative_path='',
            url_relative_path='/static/',
            allowed_extensions=['jpg', 'png', 'jpeg'],
        )
    }

    form_ajax_refs = {
        'plant': {
            'fields': ('name', 'eng_name', 'family_name'),
            'page_size': 10
        }
    }

    column_formatters = {
        'plant': lambda v, c, m, p: m.plant.family_name if m.plant else '',
        'image': lambda v, c, m, p: Markup(f'<img src="/static/{m.image}" style="height: 100px;">') if m.image else '',
        'text': lambda v, c, m, p: (m.text[:100] + '...') if m.text and len(
            m.text) > 100 else m.text
    }
    form_widget_args = {
        'text': {'rows': 10, 'style': 'width: 100%; font-size: 16px;'}
    }

    column_list = ['pair_number', 'text', 'next_pair_number', 'plant', 'image']
    column_searchable_list = ['text', 'pair_number', 'next_pair_number', 'plant_id']
    form_columns = ['pair_number', 'text', 'next_pair_number', 'plant', 'image']

def register_admin_views():
    admin.add_view(PlantAdmin(Plant, db.session))
    admin.add_view(QuestionAdmin(Question, db.session))
