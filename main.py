import sys
import scan
import shutil
import normalize
from pathlib import Path

def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

extensions_to_remove = [".zip", ".gz", ".tar"]
for extension_to_remove in extensions_to_remove: 
    new_name = normalize.normalize(path.name.replace(extension_to_remove, ''))


    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return 
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def main(folder_path):
    print(folder_path)
    scan.scan(folder_path)

    for file in scan.jpeg_files:
        handle_file(file, folder_path, 'images')
    for file in scan.jpg_files:
        handle_file(file, folder_path, 'images')
    for file in scan.png_files:
        handle_file(file, folder_path, 'images')  
    for file in scan.svg_files:
        handle_file(file, folder_path, 'images')
    for file in scan.mp3_files:
        handle_file(file, folder_path, 'audio')
    for file in scan.ogg_files:
        handle_file(file, folder_path, 'audio')
    for file in scan.wav_files:
        handle_file(file, folder_path, 'audio')
    for file in scan.amr_files:
        handle_file(file, folder_path, 'audio')
    for file in scan.avi_files:
        handle_file(file, folder_path, 'video')
    for file in scan.mp4_files:
        handle_file(file, folder_path, 'video')
    for file in scan.mov_files:
        handle_file(file, folder_path, 'video')
    for file in scan.mkv_files:
        handle_file(file, folder_path, 'video')
    for file in scan.txt_files:
        handle_file(file, folder_path, 'documents')
    for file in scan.docx_files:
        handle_file(file, folder_path, 'documents')
    for file in scan.doc_files:
        handle_file(file, folder_path, 'documents')
    for file in scan.pdf_files:
        handle_file(file, folder_path, 'documents')
    for file in scan.pptx_files:
        handle_file(file, folder_path, 'documents')
    for file in scan.xlsx_files:
        handle_file(file, folder_path, 'documents')
    for file in scan.others:
        handle_file(file, folder_path, 'other')
    for file in scan.zip_files:
        handle_archive(file, folder_path, 'archives')
    for file in scan.gz_files:
        handle_archive(file, folder_path, 'archives')
    for file in scan.tar_files:
        handle_archive(file, folder_path, 'archives')

remove_empty_folders(folder_path)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
    main(folder.resolve())