# images_in_zip_to_single_pdf.py

This Python script converts images into PDF files. When you run it, you choose one of two processing modes:

1. **ZIP mode** — processes all `.zip` files in a selected folder, converts the contained images into a single PDF file for each `.zip`.
2. **Subfolder mode** — processes each subfolder in a selected folder, converting the images directly inside each subfolder into a single PDF per subfolder.

Supported image formats: `.jpg`, `.jpeg`, `.bmp`, `.png`, `.webp`.

## Features

- **Two selectable modes** (chosen via a dialog on startup).
- **Batch Processing**: Automatically processes all `.zip` files or all subfolders in the specified folder.
- **Folder Organization**:
  - Saves the generated PDF files in a `pdf` folder within the specified folder.
  - In ZIP mode, moves processed `.zip` files to a `zip` folder.

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `Pillow` (for handling images)
  - `tkinter` (built-in with most Python distributions)

### Install Required Libraries

Install `Pillow` using pip if it is not already installed:

```bash
pip install pillow
```

## Usage

1. Run the script using Python:
```
python images_in_zip_to_single_pdf.py
```
1. A mode-selection dialog appears. Choose:
   - **Yes / 是** — process subfolders (each subfolder → one PDF).
   - **No / 否** — process ZIP files (each ZIP → one PDF).
   - **Cancel / 取消** — exit.
1. A folder selection dialog will appear. Select the folder to process.
1. The script will:
   - **ZIP mode**: convert each `.zip` file's images into a PDF and move processed `.zip` files to a `zip` folder.
   - **Subfolder mode**: convert each subfolder's images into a PDF named after that subfolder.
   - Save all generated PDFs in a `pdf` folder.
1. Progress updates will be displayed in the terminal.

## File Structure After Execution

Suppose the selected folder is `/path/to/folder`. After execution, the structure will look like this:

```plain
/path/to/folder/
├── pdf/
│   ├── file1.pdf
│   ├── file2.pdf
│   └── ...
├── zip/
│   ├── file1.zip
│   ├── file2.zip
│   └── ...
├── file3.zip
├── ...
```

## Example Output

```bash
Processing ZIP file: sample1.zip
  - Image file in process: 100/100
  -> PDF created: /path/to/folder/pdf/sample1.pdf
  -> ZIP file moved to: /path/to/folder/zip/sample1.zip
```

## Notes

- In ZIP mode, the generated PDFs will have the same base name as the `.zip` files.
- In subfolder mode, the generated PDFs will have the same base name as the subfolders.
- Images are sorted numerically when their names are numbers (e.g., `000.jpg`, `001.jpg`, ...); otherwise they are sorted alphabetically.
