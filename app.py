from flask import Flask, request, Response, jsonify
import requests
import json

app = Flask(__name__)


API_SUB_URL = "http://160.250.137.144:5001/like"
API_KEY = "qqwweerrb"

@app.route('/like', methods=['GET'])
def like_proxy():
    uid = request.args.get('uid')
    region = request.args.get('server_name') or request.args.get('region')

    if not uid or not region:
        return jsonify({"error": "Thiếu uid hoặc server_name"}), 400

    try:
        response = requests.get(API_SUB_URL, params={
            "uid": uid,
            "server_name": region,
            "key": API_KEY
        }, timeout=10)

        # Nếu API phụ trả về lỗi 5xx thì không để lộ chi tiết
        if response.status_code >= 500:
            return jsonify({"error": "Hệ thống hiện đang bảo trì. Vui lòng thử lại sau."}), 503

        data = response.json()

        # Xóa trường "owner" nếu có
        data.pop("owner", None)

        # Kiểm tra các trường cần thiết
        required_keys = ["likes_given", "likes_before", "likes_after", "nickname", "status", "uid"]
        if not all(k in data for k in required_keys):
            return jsonify({"error": "Không thể xử lý dữ liệu. Vui lòng thử lại sau."}), 500

        return jsonify({
            "LikesGivenByAPI": data["likes_given"],
            "Credit": "@tranhao116",
            "LikesafterCommand": data["likes_after"],
            "LikesbeforeCommand": data["likes_before"],
            "PlayerNickname": data["nickname"],
            "UID": data["uid"],
            "status": data["status"]
        })

    except requests.exceptions.RequestException:
        return jsonify({"error": "Không thể kết nối đến hệ thống. Vui lòng thử lại sau."}), 502

    except Exception:
        return jsonify({"error": "Đã xảy ra lỗi không xác định. Vui lòng thử lại sau."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
