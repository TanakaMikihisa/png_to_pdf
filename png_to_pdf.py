import os
from PIL import Image

def create_pdf_from_pngs(folder_path: str, output_pdf_name: str):
    """
    指定されたフォルダ内のPNG画像を名前順に結合し、単一のPDFとして保存する関数。

    Args:
        folder_path (str): PNG画像が保存されているフォルダのパス。
        output_pdf_name (str): 出力するPDFファイルの名前。
    """
    # 1. 指定されたフォルダが存在するか確認
    if not os.path.isdir(folder_path):
        print(f"[エラー] フォルダが見つかりません: {folder_path}")
        return

    # 2. フォルダ内のPNGファイルを取得
    try:
        # フォルダ内の全ファイルを取得し、末尾が.pngのファイルのみをリストアップ
        png_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]

        if not png_files:
            print(f"[情報] フォルダ内にPNGファイルが見つかりませんでした: {folder_path}")
            return

        # 3. ファイル名を名前順（昇順）にソート
        png_files.sort()
        print(f"[情報] {len(png_files)}個のPNGファイルを以下の順序で処理します:")
        for f in png_files:
            print(f"  - {f}")

    except Exception as e:
        print(f"[エラー] ファイルリストの取得中にエラーが発生しました: {e}")
        return

    # 4. 画像を読み込み、PDF化の準備
    image_objects = []
    try:
        for file_name in png_files:
            # 画像ファイルのフルパスを作成
            file_path = os.path.join(folder_path, file_name)
            
            # 画像を開く
            img = Image.open(file_path)
            
            # PNGの透過チャンネル(A)が原因でエラーになることがあるため、RGBに変換
            if img.mode == 'RGBA':
                img = img.convert('RGB')
                
            image_objects.append(img)
            
    except Exception as e:
        print(f"[エラー] 画像ファイルの読み込み中にエラーが発生しました: {e}")
        return

    # 5. 最初の画像と残りの画像のリストを使ってPDFを保存
    # PDF化する画像がない場合は処理を中断
    if not image_objects:
        return
        
    first_image = image_objects[0]
    remaining_images = image_objects[1:]

    try:
        # save_all=True と append_images を使うと複数画像を1つのPDFにできる
        first_image.save(
            output_pdf_name, 
            "PDF", 
            resolution=100.0, 
            save_all=True, 
            append_images=remaining_images
        )
        # --- 変更点 ---
        # フルパスを取得
        full_path = os.path.abspath(output_pdf_name)
        print(f"\n[成功] PDFファイルが正常に作成されました: {output_pdf_name}")
        print(f"      フルパス: {full_path}") # フルパスを表示
        # --- 変更ここまで ---
        
    except Exception as e:
        print(f"[エラー] PDFファイルの保存中にエラーが発生しました: {e}")


if __name__ == '__main__':
    # --- 設定項目 ---

    # PNG画像が入っているフォルダの名前を指定
    # このスクリプトと同じ階層にフォルダを置いてください
    sourceFolder = "png_folder"

    # 出力するPDFファイルの名前を指定
    outputFile = "combined_document.pdf"

    # --- 実行 ---
    create_pdf_from_pngs(sourceFolder, outputFile)


