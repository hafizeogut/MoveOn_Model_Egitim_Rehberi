import os
import shutil
from datetime import datetime

# Kaynak ve hedef klasör yolları
source_folder = '../00_tassel'
destination_folder = '../tassel'
# Mevcut tarih ve saat formatı
current_time = datetime.today().strftime('%Y_%m_%d')

# Kaynak klasördeki tüm dosyaları al
files = os.listdir(source_folder)

# Dosyaları yeniden isimlendirip hedef klasöre taşı
for index, file in enumerate(files):
    # Dosya uzantısını ayır
    file_name, file_ext = os.path.splitext(file)
    
    # Uzantıyı jpg olarak değiştirme
    new_ext = '.jpg'
    
    # Yeni isim oluştur
    new_name = f'{current_time}_frame_{index:04d}{new_ext}'
    
    # Kaynak ve hedef dosya yollarını oluştur
    source_file = os.path.join(source_folder, file)
    destination_file = os.path.join(destination_folder, new_name)
    
    # Dosyayı yeniden adlandır ve hedef klasöre taşı
    # .jpg uzantısına dönüştürme ve kopyalama
    with open(source_file, 'rb') as fsrc:
        with open(destination_file, 'wb') as fdst:
            fdst.write(fsrc.read())
    
    print(f'{file} dosyası {new_name} olarak yeniden adlandırıldı ve {destination_folder} klasörüne taşındı.')

