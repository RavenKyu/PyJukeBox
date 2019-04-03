from flask import jsonify
from flask_restplus import Namespace, Resource
from models import User


api = Namespace('users', description='Cats related operations')


################################################################################
@api.route('/')
class UserDetail(Resource):
    # ==========================================================================
    def get(self):
        # DB 검색
        users = [user.to_dict() for user in User.query.all()]
        if not users:
            api.abort(404)
        return jsonify(users)



################################################################################
@api.route('/<nickname>')
@api.param('nickname')
class UserDetail(Resource):
    # ==========================================================================
    def get(self, nickname):
        user = User.query.filter(User.name == nickname).first()
        if not user:
            api.abort(404)
        return jsonify(user.to_dict())



