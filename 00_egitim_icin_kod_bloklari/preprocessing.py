from sklearn.model_selection import train_test_split
import cv2
import os
import yaml

# Veri kümesi kök dizini
root_dir = "/home/hafizeogut/Desktop/tassel_label"  # Bu dizin altında resimler ve etiket dosyaları bulunur.
valid_formats = [".png", ".jpg", ".jpeg", ".txt"]  # Veri kümesinde yer almasına izin verilen formatlar belirleniyor.

def file_paths(root, valid_formats):
    file_paths = []
    # Dizin yolunun var olup olmadığını kontrol ediliyor
    if not os.path.exists(root):
        print(f"Verilen dizin mevcut değil: {root}")
        return []
    # Dizin içindeki dosyalar dolaşılıyor
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            # Dosya uzantısını al ve küçük harfe çevir
            extension = os.path.splitext(filename)[1].lower()

            # Geçerli formatlardan biriyle eşleşiyorsa:
            if extension in valid_formats:
                # dirpath ve filename değerlerini birleştirerek tam dosya yolunu oluştur
                file_path = os.path.join(dirpath, filename)
                file_paths.append(file_path)

    return file_paths

image_paths = file_paths(root_dir + "/images", valid_formats[:3])
label_paths = file_paths(root_dir + "/labels", [valid_formats[-1]])

# Dosya adlarına göre eşleşmeleri kontrol et
image_base_names = {os.path.basename(p).split('.')[0]: p for p in image_paths}
label_base_names = {os.path.basename(p).split('.')[0]: p for p in label_paths}

common_base_names = set(image_base_names.keys()).intersection(set(label_base_names.keys()))

# Ortak olan dosyaları seç
image_paths = [image_base_names[name] for name in common_base_names]
label_paths = [label_base_names[name] for name in common_base_names]

# Şimdi image_paths ve label_paths eşleşen dosyalar içerecek
print(f"Eşleşen dosya sayısı: {len(image_paths)}")

# Veri setinin %20 doğrulama ve %80 eğitim kümesi olarak ayarlanıyor
X_train, X_val_test, y_train, y_val_test = train_test_split(image_paths, label_paths, test_size=0.2, random_state=42)

X_valid, X_test, y_valid, y_test = train_test_split(X_val_test, y_val_test, test_size=0.7, random_state=42)

def write_to_file(image_dir, label_dir, X):
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)
    for image_path in X: 
        img_name = image_path.split("/")[-1].split(".")[0]  # Dosya adını al
        
        img_ext = image_path.split("/")[-1].split(".")[-1]  # Dosya uzantısını al

        image = cv2.imread(image_path)
        cv2.imwrite(f"{image_dir}/{img_name}.{img_ext}", image)

        with open(f"{label_dir}/{img_name}.txt", "w") as f:
            with open(f"{root_dir}/labels/{img_name}.txt", "r") as label_file:
                f.write(label_file.read())

write_to_file("tassel_data/train/images", "tassel_data/train/labels", X_train)
write_to_file("tassel_data/valid/images", "tassel_data/valid/labels", X_valid)
write_to_file("tassel_data/test/images", "tassel_data/test/labels", X_test)
