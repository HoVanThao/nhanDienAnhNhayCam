from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Tải mô hình đã lưu
model = load_model('./model/mobileNet_2class_v3_11_11.keras')  # Thay đổi đường dẫn nếu cần

# Xác định các lớp dự đoán
class_names = ['safe', 'unsafe']

def preprocess_image(image):
    try:
        # Chuyển đổi hình ảnh sang chế độ RGB nếu cần
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Thay đổi kích thước ảnh
        image = image.resize((180, 180))  # Kích thước ảnh đầu vào
        
        # Chuyển đổi ảnh sang mảng numpy và chuẩn hóa giá trị
        image = np.array(image) / 255.0
        
        # Thêm chiều batch để phù hợp với đầu vào của mô hình
        image = np.expand_dims(image, axis=0)
        
        return image
    except Exception as e:
        raise ValueError(f"Lỗi khi tiền xử lý ảnh: {str(e)}")
