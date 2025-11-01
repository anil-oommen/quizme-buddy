import os,re, io, base64
from PIL import Image as PImage
import pymupdf as pdfutil

# Create a single image from all pages of a PDF document
def convert_pdf_docs_in_folder_to_images(source_dir, output_dir,from_page = 1, to_page = 0, dpi=300, file_name_pattern=None):
    for filename in os.listdir(source_dir):
        if file_name_pattern and not re.search(file_name_pattern,filename):
            continue
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(source_dir, filename)
            output_image_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.png')
            convert_pdf_doc_to_image(pdf_path, output_image_path,from_page, to_page, dpi)
    print("Created single image from all PDF pages.")
    
    # convert_pdf_to_images("DBS_POSB Consolidated Statement_Dec2018.pdf")
    # print("Converted PDF to images.")


# Create a single image from all pages of a PDF document
def convert_pdf_doc_to_image(pdf_path, output_image_path, from_page = 1, to_page = 0, dpi=300, match_content=None):
    doc = pdfutil.open(pdf_path)
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
        with PImage.open(image_path) as img:
            if img.format != 'PNG':
                print("Warning: Image is not in PNG format. Converting to PNG.")
                # Convert to PNG in memory
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)
                return base64.b64encode(buffer.getvalue()).decode('utf-8')
            else:
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while processing the image: {e}")
        return None