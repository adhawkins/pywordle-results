from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, fields, marshal, reqparse, inputs
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

from Database import *

API_BASE = "/wordle-results/api/v1"

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pywordle-results.db"
db = SQLAlchemy(model_class=Database.Base)
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
auth = HTTPBasicAuth()

# with app.app_context():
#     db.create_all()


@auth.verify_password
def verifyPassword(username, password):
    return username == "andy" and password == "testing"


userInfoArgs = reqparse.RequestParser()
userInfoArgs.add_argument(
    "username",
    type=str,
    required=True,
    help="No user name provided",
    location="json",
)
userInfoArgs.add_argument(
    "fullname",
    type=str,
    required=True,
    help="No full name provided",
    location="json",
)
userInfoArgs.add_argument(
    "telegram_id",
    type=int,
    required=False,
    help="No telegram ID provided",
    location="json",
)

user_fields = {
    "username": fields.String,
    "fullname": fields.String,
    "id": fields.Integer,
    "telegram_id": fields.Integer,
    "uri": fields.Url("user_info", absolute=True),
}


class UsersListAPI(Resource):
    @auth.login_required
    def get(self):
        telegramID = request.args.get("telegramid", default=None, type=int)
        fullName = request.args.get("fullname", default=None, type=str)

        query = db.select(Database.Users).order_by(Database.Users.id)
        if telegramID:
            query = query.where(Database.Users.telegram_id == telegramID)
        if fullName:
            query = query.where(Database.Users.fullname == fullName)

        users = db.session.execute(query).scalars()
        return {"users": [marshal(user, user_fields) for user in users]}

    @auth.login_required
    def post(self):
        try:
            args = userInfoArgs.parse_args()

            user = Database.Users(
                username=args["username"],
                fullname=args["fullname"],
            )

            if "telegram_id" in args:
                user.telegram_id = args["telegram_id"]

            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user_info", id=user.id))
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


class UserAPI(Resource):
    @auth.login_required
    def get(self, id):
        user = db.get_or_404(Database.Users, id)
        return {"user": marshal(user, user_fields)}

    @auth.login_required
    def delete(self, id):
        user = db.get_or_404(Database.Users, id)
        db.session.delete(user)
        db.session.commit()

        return redirect(url_for("users_list"))

    @auth.login_required
    def patch(self, id):
        try:
            args = userInfoArgs.parse_args()

            user = db.get_or_404(Database.Users, id)
            user.username = args["username"]
            user.fullname = args["fullname"]

            if "telegram_id" in args:
                user.telegram_id = args["telegram_id"]

            db.session.add(user)
            db.session.commit()

            return redirect(url_for("user_info", id=user.id))
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


gameInfoArgs = reqparse.RequestParser()
gameInfoArgs.add_argument(
    "id",
    type=int,
    required=True,
    help="No game ID provided",
    location="json",
)
gameInfoArgs.add_argument(
    "date",
    type=inputs.date,
    required=True,
    help="No game date provided",
    location="json",
)
gameInfoArgs.add_argument(
    "solution",
    type=str,
    required=True,
    help="No game solution provided",
    location="json",
)

game_fields = {
    "id": fields.Integer,
    "date": fields.String,
    "solution": fields.String,
    "uri": fields.Url("game_info", absolute=True),
}


class GamesListAPI(Resource):
    @auth.login_required
    def get(self):
        games = db.session.execute(
            db.select(Database.Games).order_by(Database.Games.id)
        ).scalars()
        return {"games": [marshal(game, game_fields) for game in games]}

    @auth.login_required
    def post(self):
        try:
            args = gameInfoArgs.parse_args()
            game = Database.Games(
                id=args["id"], date=args["date"], solution=args["solution"]
            )
            db.session.add(game)
            db.session.commit()
            return redirect(url_for("game_info", id=game.id))
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


class GameAPI(Resource):
    @auth.login_required
    def get(self, id):
        game = db.get_or_404(Database.Games, id)
        return {"game": marshal(game, game_fields)}

    @auth.login_required
    def delete(self, id):
        game = db.get_or_404(Database.Games, id)
        db.session.delete(game)
        db.session.commit()

        return redirect(url_for("games_list"))

    @auth.login_required
    def patch(self, id):
        try:
            args = gameInfoArgs.parse_args()

            game = db.get_or_404(Database.Games, id)
            game.id = args["id"]
            game.date = args["date"]
            game.solution = args["solution"]
            db.session.add(game)
            db.session.commit()

            return redirect(url_for("user_info", id=game.id))
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


gameResultInfoArgs = reqparse.RequestParser()
gameResultInfoArgs.add_argument(
    "user",
    type=int,
    required=True,
    help="No user ID provided",
    location="json",
)
gameResultInfoArgs.add_argument(
    "guesses",
    type=int,
    required=True,
    help="No num guesses provided",
    location="json",
)
gameResultInfoArgs.add_argument(
    "success",
    type=int,
    required=True,
    help="No success parameter provided",
    location="json",
)

game_result_fields = {
    "id": fields.Integer,
    "user": fields.Integer,
    "userdetails.username": fields.String,
    "userdetails.fullname": fields.String,
    "game": fields.Integer,
    "gamedetails.date": fields.String,
    "gamedetails.solution": fields.String,
    "guesses": fields.Integer,
    "success": fields.Integer,
    "uri": fields.Url("game_result_info", absolute=True),
}


class GameResultsListAPI(Resource):
    @auth.login_required
    def get(self, game):
        results = db.session.execute(
            db.select(Database.GameResults)
            .where(Database.GameResults.game == game)
            .order_by(Database.GameResults.id)
        ).scalars()
        return {
            "gameresults": [marshal(result, game_result_fields) for result in results]
        }

    @auth.login_required
    def post(self, game):
        try:
            args = gameResultInfoArgs.parse_args()
            result = Database.GameResults(
                user=args["user"],
                game=game,
                guesses=args["guesses"],
                success=args["success"],
            )
            db.session.add(result)
            db.session.commit()
            return redirect(url_for("game_result_info", game=game, id=result.id))
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


class GameResultAPI(Resource):
    @auth.login_required
    def get(self, game, id):
        gameresult = db.get_or_404(Database.GameResults, id)
        return {"gameresult": marshal(gameresult, game_result_fields)}


result_fields = {
    "id": fields.Integer,
    "user": fields.Integer,
    "userdetails.username": fields.String,
    "userdetails.fullname": fields.String,
    "game": fields.Integer,
    "gamedetails.date": fields.String,
    "gamedetails.solution": fields.String,
    "guesses": fields.Integer,
    "success": fields.Integer,
    "uri": fields.Url("result_info", absolute=True),
}


class ResultsListAPI(Resource):
    @auth.login_required
    def get(self):
        results = db.session.execute(db.select(Database.GameResults)).scalars()
        return {"results": [marshal(result, result_fields) for result in results]}


class ResultAPI(Resource):
    @auth.login_required
    def get(self, id):
        result = db.get_or_404(Database.GameResults, id)
        return {"result": marshal(result, result_fields)}


guessInfoArgs = reqparse.RequestParser()
guessInfoArgs.add_argument(
    "guess_num",
    type=int,
    required=True,
    help="No guess number provided",
    location="json",
)
guessInfoArgs.add_argument(
    "num_words",
    type=int,
    required=True,
    help="No number of words provided",
    location="json",
)
guessInfoArgs.add_argument(
    "guess",
    type=str,
    required=True,
    help="No guess provided",
    location="json",
)
guessInfoArgs.add_argument(
    "result1",
    type=str,
    required=True,
    help="No result1 parameter provided",
    location="json",
)
guessInfoArgs.add_argument(
    "result2",
    type=str,
    required=True,
    help="No result1 parameter provided",
    location="json",
)
guessInfoArgs.add_argument(
    "result3",
    type=str,
    required=True,
    help="No result1 parameter provided",
    location="json",
)
guessInfoArgs.add_argument(
    "result4",
    type=str,
    required=True,
    help="No result1 parameter provided",
    location="json",
)
guessInfoArgs.add_argument(
    "result5",
    type=str,
    required=True,
    help="No result1 parameter provided",
    location="json",
)

guess_fields = {
    "id": fields.Integer,
    "result": fields.Integer,
    "game": fields.Integer,
    "guess_num": fields.Integer,
    "num_words": fields.Integer,
    "guess": fields.String,
    "result1": fields.String,
    "result2": fields.String,
    "result3": fields.String,
    "result4": fields.String,
    "result5": fields.String,
    "uri": fields.Url("guess_info", absolute=True),
    "gamedetails.solution": fields.String,
}


class GuessListAPI(Resource):
    @auth.login_required
    def get(self, game, result):
        guesses = db.session.execute(
            db.select(Database.Guesses)
            .where(Database.Guesses.result == result)
            .order_by(Database.Guesses.id)
        ).scalars()
        return {"guesses": [marshal(guess, guess_fields) for guess in guesses]}

    @auth.login_required
    def post(self, game, result):
        try:
            args = guessInfoArgs.parse_args()
            guess = Database.Guesses(
                result=result,
                game=game,
                guess_num=args["guess_num"],
                num_words=args["num_words"],
                guess=args["guess"],
                result1=args["result1"],
                result2=args["result2"],
                result3=args["result3"],
                result4=args["result4"],
                result5=args["result5"],
            )
            db.session.add(guess)
            db.session.commit()

            return redirect(
                url_for("guess_info", game=game, result=result, id=guess.id)
            )
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


class GuessAPI(Resource):
    @auth.login_required
    def get(self, game, result, id):
        guess = db.get_or_404(Database.Guesses, id)
        return {"guess": marshal(guess, guess_fields)}


telegram_group_fields = {
    "id": fields.Integer,
    "group": fields.Integer,
    "title": fields.String,
    "uri": fields.Url("telegram_group_info", absolute=True),
}

telegramGroupInfoArgs = reqparse.RequestParser()
telegramGroupInfoArgs.add_argument(
    "group",
    type=int,
    required=True,
    help="No telegram group ID provided",
    location="json",
)
telegramGroupInfoArgs.add_argument(
    "title",
    type=str,
    required=True,
    help="No telegram group title provided",
    location="json",
)


class TelegramGroupListAPI(Resource):
    @auth.login_required
    def get(self):
        groupID = request.args.get("groupid", default=None, type=int)

        query = db.select(Database.TelegramGroups).order_by(Database.TelegramGroups.id)
        if groupID:
            query = query.where(Database.TelegramGroups.group == groupID)

        groups = db.session.execute(query).scalars()
        return {
            "telegram_groups": [
                marshal(group, telegram_group_fields) for group in groups
            ]
        }

    @auth.login_required
    def post(self):
        try:
            args = telegramGroupInfoArgs.parse_args()
            telegramGroup = Database.TelegramGroups(
                group=args["group"], title=args["title"]
            )
            db.session.add(telegramGroup)
            db.session.commit()
            return redirect(url_for("telegram_group_info", id=telegramGroup.id))
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


class TelegramGroupAPI(Resource):
    @auth.login_required
    def get(self, id):
        user = db.get_or_404(Database.TelegramGroups, id)
        return {"user": marshal(user, telegram_group_fields)}

    @auth.login_required
    def delete(self, id):
        telegramGroup = db.get_or_404(Database.TelegramGroups, id)
        db.session.delete(telegramGroup)
        db.session.commit()

        return redirect(url_for("telegram_groups_list"))

    @auth.login_required
    def patch(self, id):
        try:
            args = telegramGroupInfoArgs.parse_args()

            telegramGroup = db.get_or_404(Database.TelegramGroups, id)
            telegramGroup.title = args["title"]

            db.session.add(telegramGroup)
            db.session.commit()

            return redirect(url_for("telegram_group_info", id=telegramGroup.id))
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


telegram_group_member_fields = {
    "id": fields.Integer,
    "group": fields.Integer,
    "user": fields.Integer,
    "uri": fields.Url("telegram_group_members_info", absolute=True),
    "userdetails.username": fields.String,
    "userdetails.fullname": fields.String,
    "telegramgroupdetails.title": fields.String,
}

telegramGroupMemberInfoArgs = reqparse.RequestParser()
telegramGroupMemberInfoArgs.add_argument(
    "user",
    type=int,
    required=True,
    help="No user ID provided",
    location="json",
)


class TelegramGroupMembersListAPI(Resource):
    @auth.login_required
    def get(self, group):
        userID = request.args.get("userid", default=None, type=int)

        query = db.select(Database.TelegramGroupMembers).where(
            Database.TelegramGroupMembers.group == group
        )

        if userID:
            query = query.where(Database.TelegramGroupMembers.user == userID)

        members = db.session.execute(
            query.order_by(Database.TelegramGroupMembers.id)
        ).scalars()
        return {
            "telegram_group_members": [
                marshal(member, telegram_group_member_fields) for member in members
            ]
        }

    @auth.login_required
    def post(self, group):
        try:
            args = telegramGroupMemberInfoArgs.parse_args()
            telegramGroupMember = Database.TelegramGroupMembers(
                group=group, user=args["user"]
            )
            db.session.add(telegramGroupMember)
            db.session.commit()
            return redirect(
                url_for(
                    "telegram_group_members_info",
                    group=group,
                    id=telegramGroupMember.id,
                )
            )
        except IntegrityError as e:
            return {"error": str(e.orig)}, 409


class TelegramGroupMembersAPI(Resource):
    @auth.login_required
    def get(self, group, id):
        user = db.get_or_404(Database.TelegramGroupMembers, id)
        return {"user": marshal(user, telegram_group_member_fields)}

    @auth.login_required
    def delete(self, group, id):
        telegramGroupMember = db.get_or_404(Database.TelegramGroupMembers, id)
        db.session.delete(telegramGroupMember)
        db.session.commit()

        return redirect(url_for("telegram_group_members_list", group=group))


api.add_resource(UsersListAPI, f"{API_BASE}/users", endpoint="users_list")
api.add_resource(UserAPI, f"{API_BASE}/users/<int:id>", endpoint="user_info")

api.add_resource(GamesListAPI, f"{API_BASE}/games", endpoint="games_list")
api.add_resource(GameAPI, f"{API_BASE}/games/<int:id>", endpoint="game_info")

api.add_resource(
    GameResultsListAPI,
    f"{API_BASE}/games/<int:game>/results",
    endpoint="game_results_list",
)
api.add_resource(
    GameResultAPI,
    f"{API_BASE}/games/<int:game>/results/<int:id>",
    endpoint="game_result_info",
)

api.add_resource(
    ResultsListAPI,
    f"{API_BASE}/results",
    endpoint="results_list",
)
api.add_resource(
    ResultAPI,
    f"{API_BASE}/results/<int:id>",
    endpoint="result_info",
)

api.add_resource(
    GuessListAPI,
    f"{API_BASE}/games/<int:game>/results/<int:result>/guesses",
    endpoint="guess_list",
)
api.add_resource(
    GuessAPI,
    f"{API_BASE}/games/<int:game>/results/<int:result>/guesses/<int:id>",
    endpoint="guess_info",
)

api.add_resource(
    TelegramGroupListAPI, f"{API_BASE}/telegram_groups", endpoint="telegram_groups_list"
)
api.add_resource(
    TelegramGroupAPI,
    f"{API_BASE}/telegram_groups/<int:id>",
    endpoint="telegram_group_info",
)

api.add_resource(
    TelegramGroupMembersListAPI,
    f"{API_BASE}/telegram_groups/<int:group>/members",
    endpoint="telegram_group_members_list",
)
api.add_resource(
    TelegramGroupMembersAPI,
    f"{API_BASE}/telegram_groups/<int:group>/members/<int:id>",
    endpoint="telegram_group_members_info",
)
