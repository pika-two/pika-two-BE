from flask import jsonify, request
from flask_restx import Resource, Namespace
from src.service.user import *

User = Namespace('User')


@User.route('/signup')
class Signup(Resource):
    # 사용자 기본정보 등록
    def post(self):
        user_data = signup(dict(request.get_json()))
        return jsonify({
            "code": 200,
            "data": user_data,
            "message": "사용자가 등록되었습니다"
        })


@User.route('/mypage/<int:user_id>')
class MyPage(Resource):

    # 마이페이지 정보 조회
    def get(self, user_id):
        print(user_id)
        response = get_my_page(user_id)
        return jsonify({"code": 200, "data": response})


@User.route('/<int:user_id>/favor')
class FavList(Resource):

    # 찜목록    
    def get(self, user_id):
        print(user_id)
        response = get_fav_list(user_id)
        return jsonify({"code": 200, "data": response})

    # 찜등록/해제
    def post(self, user_id):
        result = post_fav_list(user_id, request.get_json()['company_id'])
        return jsonify({"code": 200, "data": result})


@User.route('/<int:user_id>/favor/<int:fav_company_id>')
class FavDetail(Resource):

    # 찜삭제
    def delete(self, user_id, fav_company_id):
        print(user_id)
        delete_fav_list(fav_company_id)
        return jsonify({"code": 200})


@User.route('/<int:user_id>/applied-posts')
class AppliedPosts(Resource):

    # 지원회사 목록
    def get(self, user_id):
        print(user_id)
        res = get_applied_posts(user_id)
        return jsonify({"code": 200, "data": res})

    #지원하기
    def post(self, user_id):
        print(user_id)
        post_applied_posts(user_id, request.get_json()['post_id'])
        return jsonify({"code": 200})

    #상태 변경
    def put(self, user_id):
        print(user_id)
        req = request.get_json()
        update_applied_posts(user_id, req['apply_id'], req['status'])
        return jsonify({"code": 200})

@User.route('/<int:user_id>/applied-posts/<int:apply_id>')
class AppliedPostsDetail(Resource):
    #지원현황 삭제
    def delete(self, user_id, apply_id):
        logging.info(f"{request.form}")
        delete_applied_posts(apply_id)
        return jsonify({"code": 200})



