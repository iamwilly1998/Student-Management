from flask import Flask
from urllib.parse import quote
from .extensions import db, login_manager
from .models import User, Semester
from .index import main
from flask_admin import Admin
from .admin import MyAdminIndex
import cloudinary

administrator = Admin(name = 'QUẢN TRỊ VIÊN', template_mode = 'bootstrap4', index_view = MyAdminIndex())

cloudinary.config(
        cloud_name = 'dzm6ikgbo',
        api_key = '539987548171822',
        api_secret = 'FfePKpjetbSwFufRAnuWoDMeaIA'
    )


def create_app():
    database_uri = "mysql+pymysql://root:%s@localhost/student_management?charset=utf8mb4" % quote('Admin@123')
    app = Flask(__name__)
    app.secret_key = "hjasgdikuhqhjkgavsasudmnxbzcjyatwakjhsh"
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    db.init_app(app)
    login_manager.init_app(app)
    administrator.init_app(app)

    from .admin import EditPrincipleView, ManageSubjectView, MyStatsView, MyLogoutView
    from .models import Principle, Subject
    administrator.add_view(EditPrincipleView(Principle, db.session, name = "Chỉnh sửa quy định"))
    administrator.add_view(ManageSubjectView(Subject, db.session, name = "Quản lý môn học"))
    administrator.add_view(MyStatsView(name = 'Thống kê báo cáo'))
    administrator.add_view(MyLogoutView(name = 'Đăng xuất'))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(main, name="main")

    return app

# app = Flask(__name__)
# app.secret_key = "hjasgdikuhqhjkgavsasudmnxbzcjyatwakjhsh"
# database_uri = "mysql+pymysql://root:%s@localhost/student_management?charset=utf8mb4" % quote('Admin@123')
# app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config["CN_PAGE_SIZE"] = 9
#
#
# db = SQLAlchemy(app= app)
# login = LoginManager(app)
#
# cloudinary.config(
#     cloud_name = 'dzm6ikgbo',
#     api_key = '539987548171822',
#     api_secret = 'FfePKpjetbSwFufRAnuWoDMeaIA'
# )