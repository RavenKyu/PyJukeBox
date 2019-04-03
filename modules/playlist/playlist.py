from flask import jsonify
from flask_restplus import Namespace, Resource
from models import UserPlayListIndex, User


api = Namespace('categories', description='Cats related operations')


################################################################################
@api.route('/<string:nickname>/categories/')
class UserPlayList(Resource):
    # ==========================================================================
    def get(self, nickname):
        # DB 검색

        print(UserPlayListIndex.query.all())
        # categories = [categories.to_dict() for categories in
        #               UserPlayListIndex.query.filter_by(user=User.nickname)]
        #          UserPlayListIndex.query.filter_by(User.name == nickname)]
        # print(categories)
        # if not categories:
        #     api.abort(404)
        # return jsonify(categories)


#
# ################################################################################
# @api.route('/<nickname>')
# @api.param('nickname')
# class UserDetail(Resource):
#     # ==========================================================================
#     def get(self, nickname):
#         user = User.query.filter(User.name == nickname).first()
#         if not user:
#             api.abort(404)
#         return jsonify(user.to_dict())