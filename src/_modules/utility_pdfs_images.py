import os,re, io, base64
from pathlib import Path
from PIL import Image as PImage
import pymupdf as pdfutil


def _validate_path_safety(file_path, base_dir=None):
    """
    Validates that a file path is safe and doesn't contain path traversal attempts.
    
    Args:
        file_path (str): The file path to validate
        base_dir (str, optional): The base directory to check against. If provided,
                                 ensures the resolved path is within this directory.
    
    Returns:
        Path: The validated, resolved Path object
        
    Raises:
        ValueError: If the path contains potentially dangerous sequences or 
                   resolves outside the base directory
    """
    # Convert to Path object and resolve to absolute path
    path = Path(file_path).resolve()
    
    # Check for suspicious patterns (though resolve() should handle these)
    path_str = str(path)
    if '..' in Path(file_path).parts:
        raise ValueError(f"Path traversal detected in path: {file_path}")
    
    # If base_dir is provided, ensure the path is within it
    if base_dir:
        base_path = Path(base_dir).resolve()
        try:
            # This will raise ValueError if path is not relative to base_path
            path.relative_to(base_path)
        except ValueError:
            raise ValueError(f"Path {file_path} is outside the allowed directory {base_dir}")
    
    return path


# Create a single image from all pages of a PDF document
def convert_pdf_docs_in_folder_to_images(source_dir, output_dir,from_page = 1, to_page = 0, dpi=300, file_name_pattern=None):
    # Validate base directories
    source_path = _validate_path_safety(source_dir)
    output_path = _validate_path_safety(output_dir)
    
    # Ensure directories exist
    if not source_path.is_dir():
        raise ValueError(f"Source directory does not exist: {source_dir}")
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
    
    for filename in os.listdir(source_path):
        if file_name_pattern and not re.search(file_name_pattern,filename):
            continue
        if filename.lower().endswith(".pdf"):
            # Use Path for secure path joining - prevents traversal
            pdf_path = source_path / filename
            # Validate the constructed path is still within source_dir
            _validate_path_safety(pdf_path, source_path)
            
            output_image_path = output_path / f"{pdf_path.stem}.png"
            # Validate the output path is still within output_dir
            _validate_path_safety(output_image_path, output_path)
            
            convert_pdf_doc_to_image(str(pdf_path), str(output_image_path),from_page, to_page, dpi)
    print("Created single image from all PDF pages.")
    
    # convert_pdf_to_images("DBS_POSB Consolidated Statement_Dec2018.pdf")
    # print("Converted PDF to images.")


# Create a single image from all pages of a PDF document
def convert_pdf_doc_to_image(pdf_path, output_image_path, from_page = 1, to_page = 0, dpi=300, match_content=None):
    # Validate input paths
    pdf_path_obj = _validate_path_safety(pdf_path)
    if not pdf_path_obj.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    if not pdf_path_obj.suffix.lower() == '.pdf':
        raise ValueError(f"File is not a PDF: {pdf_path}")
    
    # Validate output path (directory must exist or be creatable)
    output_path_obj = _validate_path_safety(output_image_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    doc = pdfutil.open(str(pdf_path_obj))
    page_images = []
    total_height = 0
    max_width = 0

    
    if from_page > 0 and to_page>0:
        start_index = from_page-1
        end_index = doc.page_count if doc.page_count<to_page else to_page
    elif from_page > 0 and to_page == 0:
        start_index = from_page-1
        end_index = doc.page_count
    elif from_page < 0 and to_page < 0 and to_page > from_page:
        start_index = doc.page_count + from_page 
        end_index = doc.page_count + to_page 
    else:
         raise Exception("Negative values for pages from last, but has to consistent.")

    
    
    print(f"---Converting pages (ask:'{from_page} {to_page}') '{pdf_path}' pages {start_index+1}-{end_index}/{doc.page_count}")
    print(f'{match_content}')

    # Render each page to a Pixmap and store them
    for page_num in range(start_index, end_index):
        page = doc[page_num]
        if match_content:
            text = page.get_text()
            if match_content not in text:
                print(f'\t page {page_num+1}: . ')
                continue
            print(f'\t page {page_num+1}: \u2714 ')
        
        pix = page.get_pixmap(dpi=dpi)
        page_images.append(pix)
        total_height += pix.height
        if pix.width > max_width:
            max_width = pix.width

    if match_content and not page_images:
        raise Exception(f"Content '{match_content}' not found in any of the specified pages.")

    # Create a new blank image with Pillow
    combined_image = PImage.new("RGB", (max_width, total_height), (255, 255, 255)) # White background

    # Paste individual page images onto the combined image
    current_height = 0
    for pix in page_images:
        img = PImage.frombytes("RGB", [pix.width, pix.height], pix.samples)
        combined_image.paste(img, (0, current_height))
        current_height += pix.height

    # Save the combined image
    combined_image.save(output_image_path)
    doc.close()

# Example usage:
# create_single_image_from_pdf("your_document.pdf", "all_pages_combined.png")


def encode_image_to_base64(image_path):
    """Encodes an image file to a base64 string."""
    try:
        # Validate image path
        image_path_obj = _validate_path_safety(image_path)
        if not image_path_obj.exists():
            print(f"Error: The file '{image_path}' was not found.")
            return None
        
        with PImage.open(image_path_obj) as img:
            if img.format != 'PNG':
                print("Warning: Image is not in PNG format. Converting to PNG.")
                # Convert to PNG in memory
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)
                return base64.b64encode(buffer.getvalue()).decode('utf-8')
            else:
                with open(image_path_obj, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while processing the image: {e}")
        return None