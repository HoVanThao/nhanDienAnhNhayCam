from flask import Flask
from flaskr.utils.json_helper import CustomJSONProvider
from flaskr.errorHandlers.default_handler import default_handler
from flaskr.errorHandlers.default_http_handler import default_http_handler
from flaskr.errorHandlers.my_handler import my_handler
from flaskr.errors.bad_request import BadRequestError
from flaskr.errors.not_found import NotFoundError
from flaskr.errors.unauthenticated import UnauthenticatedError
from flaskr.errors.forbidden import ForbiddenError
from flaskr.controllers.image_recognition_controller import imageRecognitionBP
from werkzeug.exceptions import HTTPException

def create_app():

    #Tạo ứng dụng Flask.
    app = Flask(__name__, instance_relative_config=True)

    #Sử dụng để cấu hình JSON encoder cho ứng dụng.
    app.json = CustomJSONProvider(app)

    # error handler

    # máy chủ không thể hiểu hoặc xử lý yêu cầu mà bạn gửi đi do cú pháp không hợp lệ hoặc thiếu thông tin cần thiết. 
    app.register_error_handler(BadRequestError, my_handler)
    # máy chủ không thể tìm thấy tài nguyên hoặc trang web mà bạn yêu cầu
    app.register_error_handler(NotFoundError, my_handler)
    # xảy ra khi bạn không có quyền truy cập vào tài nguyên yêu cầu
    app.register_error_handler(UnauthenticatedError, my_handler)

    # máy chủ từ chối yêu cầu do thiếu quyền truy cập hoặc có hạn chế đối với yêu cầu đó
    app.register_error_handler(ForbiddenError, my_handler)
    app.register_error_handler(HTTPException, default_http_handler)
    app.register_error_handler(Exception, default_handler)

    # api/v1/image
    app.register_blueprint(imageRecognitionBP)

    return app