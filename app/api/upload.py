import os
from flask import request, jsonify
from termcolor import colored
from app import app

from app.utils.auth import verify_token
from app.utils.upload import save_base64, save_image


@app.route("/api/uploadByBase64", methods=["POST"])
def upload_from_base64():
    try:
        data = request.get_json()
        image_base64 = data["imageBase64"]
        filename = data["filename"]

        # 验证文件格式
        file_extension = os.path.splitext(filename)[1].lower()
        if (
            (file_extension != ".jpg")
            & (file_extension != ".png")
            & (file_extension != ".gif")
        ):
            response = {"message": "图片格式不正确"}
            return jsonify(response), 500

        # 验证token
        token = request.headers.get("Authorization")
        if not token:
            response = {"message": "缺少认证Token"}
            return jsonify(response), 401

        # 分割 Authorization 头部，获取实际的 token 部分
        token_parts = token.split()
        if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
            response = {"message": "Token格式不正确"}
            return jsonify(response), 401

        # 获取实际的 token
        actual_token = token_parts[1]

        decoded_payload = verify_token(actual_token)
        if (
            not decoded_payload
            or decoded_payload["username"] != app.config["ADMIN_USERNAME"]
        ):
            response = {"message": "Token无效或与用户不匹配"}
            return jsonify(response), 401

        # 保存图片
        filename = save_base64(image_base64, filename)
        if filename:
            colored_filename = colored(filename, "yellow")
            app.logger.info("upload: %s", colored_filename)
            response = {
                "message": "图片上传成功",
                "file_url": f"{request.url_root}images/{filename}",
            }
            return jsonify(response), 201
        else:
            response = {"message": "图片上传失败"}
            return jsonify(response), 500

    except Exception as e:
        print("Error:", e)
        response = {"message": "图片上传失败"}
        return jsonify(response), 500


@app.route("/api/upload", methods=["POST"])
def upload_image():
    try:
        uploaded_image = request.files.get("image")

        # 验证文件格式
        file_extension = os.path.splitext(uploaded_image.filename)[1].lower()
        if (
            (file_extension != ".jpg")
            & (file_extension != ".png")
            & (file_extension != ".gif")
        ):
            response = {"message": "图片格式不正确"}
            return jsonify(response), 500

        # 验证token
        token = request.headers.get("Authorization")
        if not token:
            response = {"message": "缺少认证Token"}
            return jsonify(response), 401

        # 分割 Authorization 头部，获取实际的 token 部分
        token_parts = token.split()
        if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
            response = {"message": "Token格式不正确"}
            return jsonify(response), 401

        # 获取实际的 token
        actual_token = token_parts[1]

        decoded_payload = verify_token(actual_token)
        if (
            not decoded_payload
            or decoded_payload["username"] != app.config["ADMIN_USERNAME"]
        ):
            response = {"message": "Token无效或与用户不匹配"}
            return jsonify(response), 401

        # 保存图片
        if uploaded_image:
            # 保存文件到文件系统
            file_path = uploaded_image.filename
            filename = save_image(uploaded_image, file_path)
            if filename is not None:
                colored_filename = colored(filename, "yellow")
                app.logger.info("upload: %s", colored_filename)
                return jsonify(
                    {
                        "message": "图片上传成功",
                        "file_url": f"{request.url_root}images/{filename}",
                    }
                )
        response = {"message": "图片上传失败"}
        return jsonify(response), 500

    except Exception as e:
        print("Error:", e)
        response = {"message": "图片上传失败"}
        return jsonify(response), 500
