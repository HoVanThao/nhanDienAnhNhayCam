from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

app = Flask(__name__)

# Tải mô hình đã lưu
model = load_model('./model/model_mobileNet.h5')  # Thay đổi đường dẫn nếu cần

# Xác định các lớp dự đoán
class_names = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

# Tiền xử lý hình ảnh
def preprocess_image(image):
    # Chuyển đổi ảnh thành định dạng phù hợp với mô hình
    image = image.resize((180, 180))  # Kích thước ảnh đầu vào
    image = np.array(image) / 255.0  # Chia cho 255 để chuẩn hóa
    image = np.expand_dims(image, axis=0)  # Thêm một chiều
    return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        image = Image.open(file.stream)  # Mở ảnh từ file upload
        processed_image = preprocess_image(image)  # Tiền xử lý ảnh

        # Dự đoán với model
        predictions = model.predict(processed_image)
        predicted_class = np.argmax(predictions[0])  # Lấy class có xác suất cao nhất
        predicted_label = class_names[predicted_class]  # Lấy tên class tương ứng

        # Xác định loại ảnh dựa trên class
        if predicted_label in ['neutral', 'drawings']:
            print('class: ', predicted_label)
            return jsonify({"result": "Ảnh bình thường"})
        else:
            print('class: ', predicted_label)
            return jsonify({"result": "Ảnh nhạy cảm"})
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")  
        return jsonify({'error': str(e)}), 500

@app.route("/", methods=["GET"])
def ping():
    return "server running..."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

