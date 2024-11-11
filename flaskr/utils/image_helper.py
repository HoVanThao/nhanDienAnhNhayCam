from PIL import Image
import numpy as np

def preprocess_image(image):
    try:
        image = image.resize((180, 180))  # Kích thước ảnh đầu vào
        image = np.array(image) / 255.0  # Chuẩn hóa giá trị ảnh
        image = np.expand_dims(image, axis=0)  # Thêm chiều batch
        return image
    except Exception as e:
        raise ValueError(f"Lỗi khi tiền xử lý ảnh: {str(e)}")