from flask import request, Blueprint, jsonify
from flaskr.errors.bad_request import BadRequestError
from flaskr.utils.model import model, class_names, preprocess_image
from PIL import Image
import numpy as np

imageRecognitionBP = Blueprint("image_recognition", __name__, url_prefix="/api/v1/image")

@imageRecognitionBP.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        raise BadRequestError('Không tìm thấy tệp trong yêu cầu')

    file = request.files['file']
    if file.filename == '':
        raise BadRequestError('Chưa chọn tệp')

    try:
        # Mở ảnh từ file upload và tiền xử lý
        image = Image.open(file.stream)
        processed_image = preprocess_image(image)

        # Dự đoán với model
        predictions = model.predict(processed_image)
        predicted_class = np.argmax(predictions[0])  # Lấy class có xác suất cao nhất
        predicted_label = class_names[predicted_class]  # Tên class tương ứng

        # Xác định loại ảnh
        result = "Ảnh bình thường" if predicted_label in ['safe'] else "Ảnh nhạy cảm"

        response = {
            'EC': 0,  # Error code 0: Thành công
            'EM': 'Dự đoán thành công',
            'DT': {
                'result': result,
                'predicted_label': predicted_label,
                'confidence': float(np.max(predictions[0])),
                'class_probabilities': {
                    class_names[i]: float(predictions[0][i]) for i in range(len(class_names))
                }
            }
        }

        print(f'Predicted label: {predicted_label}, Result: {result}')
        return jsonify(response), 200

    except ValueError as ve:
        raise BadRequestError(str(ve))
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise

@imageRecognitionBP.route("/", methods=["GET"])
def ping():
    return jsonify({
        'EC': 0,
        'EM': 'Server is running...',
        'DT': None
    }), 200