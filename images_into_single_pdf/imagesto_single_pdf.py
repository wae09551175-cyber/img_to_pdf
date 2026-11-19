import os
import shutil
from tkinter import Tk, filedialog, messagebox
from PIL import Image
from zipfile import ZipFile


SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.bmp', '.png', '.webp')


def sort_key(name):
    """Sort image files numerically when possible, otherwise by name."""
    base = os.path.splitext(os.path.basename(name))[0]
    try:
        return (0, int(base))
    except ValueError:
        return (1, base.lower())


def combine_images_to_pdf(images, output_pdf_path):
    """Combine a list of PIL Images into a single PDF."""
    if not images:
        return False
    first_image = images[0]
    first_image.save(output_pdf_path, save_all=True, append_images=images[1:])
    return True


def convert_img_to_pdf_in_folder(folder_path):
    """Convert images inside each ZIP file into a single PDF per ZIP."""
    output_folder = os.path.join(folder_path, "pdf")
    done_folder = os.path.join(folder_path, "zip")
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(done_folder, exist_ok=True)

    zip_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.zip')]

    if not zip_files:
        print("There are no ZIP files in the specified folder.")
        return

    for zip_file_name in zip_files:
        zip_file_path = os.path.join(folder_path, zip_file_name)
        base_name = os.path.splitext(zip_file_name)[0]
        output_pdf_path = os.path.join(output_folder, f"{base_name}.pdf")

        print(f"ZIP file in process: {zip_file_name}")

        try:
            with ZipFile(zip_file_path, 'r') as zip_file:
                img_files = sorted(
                    [f for f in zip_file.namelist()
                     if f.lower().endswith(SUPPORTED_EXTENSIONS)],
                    key=sort_key
                )

                images = []
                total_files = len(img_files)
                for idx, img_file in enumerate(img_files, start=1):
                    print(
                        f"  - Image file in process: {idx:03}/{total_files:03}\r",
                        end="")
                    with zip_file.open(img_file) as file:
                        img = Image.open(file)
                        images.append(img.convert("RGB"))
                print("")

                if combine_images_to_pdf(images, output_pdf_path):
                    print(f"  -> Created PDF: {output_pdf_path}")
                else:
                    print("  -> Image files not found. Skipping.")
                    continue

            shutil.move(zip_file_path, os.path.join(
                done_folder, zip_file_name))
            print(
                f"  -> ZIP file has been moved: "
                f"{os.path.join(done_folder, zip_file_name)}")

        except Exception as e:
            print(f"  -> An error has occurred: {e}")
            continue


def convert_subfolders_to_pdf(folder_path):
    """Convert images inside each subfolder into a single PDF per subfolder."""
    output_folder = os.path.join(folder_path, "pdf")
    os.makedirs(output_folder, exist_ok=True)

    subfolders = [
        d for d in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, d))
        and d.lower() not in ("pdf", "zip")
    ]

    if not subfolders:
        print("There are no subfolders in the specified folder.")
        return

    for subfolder_name in sorted(subfolders):
        subfolder_path = os.path.join(folder_path, subfolder_name)
        image_files = sorted(
            [f for f in os.listdir(subfolder_path)
             if f.lower().endswith(SUPPORTED_EXTENSIONS)],
            key=sort_key
        )

        if not image_files:
            print(f"Subfolder in process: {subfolder_name} "
                  f"(no images found. Skipping.)")
            continue

        output_pdf_path = os.path.join(output_folder, f"{subfolder_name}.pdf")
        print(f"Subfolder in process: {subfolder_name}")

        images = []
        total_files = len(image_files)
        for idx, image_file in enumerate(image_files, start=1):
            print(
                f"  - Image file in process: {idx:03}/{total_files:03}\r",
                end="")
            img_path = os.path.join(subfolder_path, image_file)
            img = Image.open(img_path)
            images.append(img.convert("RGB"))
        print("")

        if combine_images_to_pdf(images, output_pdf_path):
            print(f"  -> Created PDF: {output_pdf_path}")
        else:
            print("  -> Image files not found. Skipping.")


def main():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    mode = messagebox.askyesnocancel(
        "请选择处理模式 / Choose a mode",
        "是否处理子文件夹？\n"
        "Process subfolders?\n\n"
        "是 / Yes —— 把每个子文件夹里的图片分别合成 PDF\n"
        "    (Combine images in each subfolder into one PDF each)\n\n"
        "否 / No —— 处理文件夹里的 ZIP 文件\n"
        "    (Combine images inside each ZIP into one PDF)\n\n"
        "取消 / Cancel —— 退出 (Exit)"
    )

    if mode is None:
        print("Cancelled.")
        return

    if mode:
        folder_path = filedialog.askdirectory(
            title="请选择包含子文件夹的目录 / Select a folder with subfolders.")
        if folder_path:
            try:
                convert_subfolders_to_pdf(folder_path)
            except Exception as e:
                print(f"An error has occurred: {e}")
        else:
            print("Directory not selected.")
    else:
        folder_path = filedialog.askdirectory(
            title="请选择包含 ZIP 文件的目录 / Select a folder with ZIP files.")
        if folder_path:
            try:
                convert_img_to_pdf_in_folder(folder_path)
            except Exception as e:
                print(f"An error has occurred: {e}")
        else:
            print("Directory not selected.")


if __name__ == "__main__":
    main()
