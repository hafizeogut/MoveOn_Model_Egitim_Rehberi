import cv2
import os
import numpy as np
import glob

def crop_center(image, crop_size):
    height, width = image.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    crop_w, crop_h = crop_size
    x1 = max(center_x - crop_w // 2, 0)
    y1 = max(center_y - crop_h // 2, 0)
    x2 = min(center_x + crop_w // 2, width)
    y2 = min(center_y + crop_h // 2, height)
    
    cropped_image = image[y1:y2, x1:x2]
    return cropped_image

def crop_and_save_images(input_folder, output_folder, crop_size=(830, 470)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Klasördeki tüm resimleri al
    image_files = glob.glob(os.path.join(input_folder, '*.jpg'))
    image_files.sort()  # Dosyaları sıralayarak işleme koy

    for i, image_file in enumerate(image_files):
        # Görüntüyü oku
        image = cv2.imread(image_file)

        # Merkezden kırp
        cropped_image = crop_center(image, crop_size)

        # Çözünürlüğü korumak için yeniden boyutlandırma
        height, width = image.shape[:2]
        resized_image = cv2.resize(cropped_image, (width, height), interpolation=cv2.INTER_LINEAR)

        # Yeni dosya adı oluştur
        new_file_name = f'imagee_{i+1:05d}.jpg'  # Örneğin: image_0001.jpg, image_0002.jpg, ...
        new_file_path = os.path.join(output_folder, new_file_name)

        # Yeni görüntüyü kaydet
        cv2.imwrite(new_file_path, resized_image)
         

    print("Tüm görüntüler işlenip kaydedildi.")

# Ana fonksiyon
if __name__ == "__main__":
    input_folder = "/home/hafizeogut/Desktop/images"  # Girdi görüntülerinin olduğu klasör
    output_folder = "/home/hafizeogut/Desktop/images"  # Çıktı görüntülerinin kaydedileceği klasör
    crop_and_save_images(input_folder, output_folder)

