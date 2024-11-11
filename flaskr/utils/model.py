from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Tải mô hình đã lưu
model = load_model('./model/mobileNet_2class_v3_11_11.keras')  # Thay đổi đường dẫn nếu cần

# Xác định các lớp dự đoán
class_names = ['safe', 'unsafe']

# Tiền xử lý hình ảnh
def preprocess_image(image):
    try:
        image = image.resize((180, 180))  # Kích thước ảnh đầu vào
        image = np.array(image) / 255.0  # Chuẩn hóa giá trị ảnh
        image = np.expand_dims(image, axis=0)  # Thêm chiều batch
        return image
    except Exception as e:
        raise ValueError(f"Lỗi khi tiền xử lý ảnh: {str(e)}")