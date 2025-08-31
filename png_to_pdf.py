import os
from PIL import Image

SOURCE_FOLDER = "png_folder"
OUTPUT_FILE = "combined_document.pdf"

def create_pdf_from_images(folder_path: str, output_pdf_name: str):
    if not os.path.isdir(folder_path):
        print(f"[エラー] フォルダが見つかりません: {folder_path}")
        return

    try:
        # PNG、JPEG、JPGファイルを処理対象とする
        image_files = [f for f in os.listdir(folder_path) 
                      if f.lower().endswith(('.png', '.jpeg', '.jpg'))]
        
        if not image_files:
            print(f"[情報] フォルダ内に画像ファイル（PNG/JPEG/JPG）が見つかりませんでした: {folder_path}")
            return

        image_files.sort()
        print(f"[情報] {len(image_files)}個の画像ファイルを処理します:")
        for f in image_files:
            print(f"  - {f}")

        image_objects = []
        for file_name in image_files:
            file_path = os.path.join(folder_path, file_name)
            img = Image.open(file_path)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            image_objects.append(img)

        if image_objects:
            first_image = image_objects[0]
            remaining_images = image_objects[1:]
            first_image.save(
                output_pdf_name, 
                "PDF", 
                resolution=100.0, 
                save_all=True, 
                append_images=remaining_images
            )
            print(f"\n[成功] PDFファイルが作成されました: {output_pdf_name}")
            print(f"      フルパス: {os.path.abspath(output_pdf_name)}")

    except Exception as e:
        print(f"[エラー] 処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    create_pdf_from_images(SOURCE_FOLDER, OUTPUT_FILE)

