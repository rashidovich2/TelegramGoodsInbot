from flask import Flask, render_template, jsonify
from flask.views import MethodView
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker
from models import User, db
from app import app

app = Flask(__name__) #__name__
db_uri = os.getenv('SQLALCHEMY_DATABASE_FULL_URI')
db = SQLAlchemy(app, session_options={"expire_on_commit": False})
engine = create_async_engine(db_uri, echo=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

'''@app.route('/')
def index():
    return render_template('templates/index.html')

@app.route('/about')
def about():
    return render_template('templates/about.html')

@app.route('/users')
async def user_list():
    #users = User.query.all()
    engine = create_async_engine(
        "mysql+asyncmy://u95430_telegram_port:Aa876024311abc@46.23.98.123/u95430_telegram_port",
        echo=True,
    )
    try:
        async with AsyncSession(engine) as session:
            async with session.begin():
                result = await session.execute(db.select(
                    User.user_id,
                    User.user_login,
                    User.user_name))
                data = result.all()
                user_list = []
                for user in data:
                    user_data = {
                        'user_id': user.user_id,
                        'user_login': user.user_login,
                        'user_name': user.user_name
                    }
                    user_list.append(user_data)
                return jsonify(user_list)


    except exc.SQLAlchemyError as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500


    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500

    return jsonify([])
    #return render_template('templates/users.html', users=users)

@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("templates/404.html")'''

class IndexView(MethodView):
    def get(self):
        return render_template('index.html')

class AboutView(MethodView):
    def get(self):
        return render_template('about.html')

class UserListView(MethodView):
    async def get(self):
        #users = User.query.all()
        engine = create_async_engine(
        "mysql+asyncmy://u95430_telegram_port:Aa876024311abc@46.23.98.123/u95430_telegram_port",
        echo=True,
        )
        try:
            async with AsyncSession(engine) as session:
                async with session.begin():
                    result = await session.execute(db.select(
                        User.user_id,
                        User.user_login,
                        User.user_name))
                    data = result.all()
                    users = []
                    for user in data:
                        user_data = {
                            'user_id': user.user_id,
                            'user_login': user.user_login,
                            'user_name': user.user_name
                        }
                        users.append(user_data)
                    return jsonify(users)


        except exc.SQLAlchemyError as e:
            error_message = f"An error occurred: {str(e)}"
            return jsonify({'error': error_message}), 500


        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return jsonify({'error': error_message}), 500

        #return jsonify([])
        return render_template('templates/users.html', users=users)

# Класс для отображения карточки одного пользователя
class UserCardView(MethodView):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return render_template('user_card.html', user=user)
        else:
            return jsonify({'message': 'User not found'}), 404

# Добавляем URL-маршруты для классов представлений
app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/about', view_func=AboutView.as_view('about'))
app.add_url_rule('/users', view_func=UserListView.as_view('users'), methods=['GET'])
app.add_url_rule('/users/<int:user_id>', view_func=UserCardView.as_view('user_card'))

'''app.add_url_rule('/', view_func=index)
app.add_url_rule('/about', view_func=about)
app.add_url_rule('/users', view_func=users_list, methods=['GET'])
#app.add_url_rule('/users/<int:user_id>', view_func=UserCardView.as_view('user_card'))'''

