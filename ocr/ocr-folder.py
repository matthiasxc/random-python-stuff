import cv2
import os
from PIL import Image
import pytesseract
import pillow_heif

# this didn't really work
def heic_to_png(folder_path):
    if not os.path.exists(folder_path):
        print (f"Error: Folder '{folder_path}' does not exist.")
        return
    count = 0
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.heic'):
            # convert HEIC to png
            heif_file_path = os.path.join(folder_path, filename)
            heif_file = pillow_heif.read_heif(heif_file_path)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
            )

            png_path = heif_file_path.replace('.heif', '.png')
            print(f"Saving {png_path}")
            image.save(png_path, format("png"))
            count = count + 1
    print(f"{count} files in {folder_path} converted")

def ocr_images(folder_path, output_file_suffix="_text.txt"):
    # Set the path to the Tesseract executable if it's not in your PATH
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe" 

    supported_extensions = ('.jpg', '.jpeg', '.png', '.tiff')

    if not os.path.exists(folder_path):
        print (f"Error: Folder '{folder_path}' does not exist.")
        return
    
    for filename in os.listdir(folder_path):
       if filename.lower().endswith(supported_extensions):
            file_path = os.path.join(folder_path, filename)
            try:
                
                # print(f"Read the image using OpenCV")
                raw_image = cv2.imread(file_path)

                #print(f"Convert to grayscale")
                gray = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)

                # print(f"Apply thresholding")
                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                processed_path = os.path.splitext(os.path.basename(file_path))[0] + "_processed.jpg"

                # print(f"Save the preprocessed image temporarily")
                cv2.imwrite(processed_path, thresh)

                print(f"opening image")
                image = Image.open(processed_path)
                print(f"image to string")
                text = pytesseract.image_to_string(image)
                if not text:
                    print(f"Text could not be extracte from {filename}")
                else:
                    print(f"got text, creating file")                
                    output_file_name = os.path.splitext(os.path.basename(file_path))[0] + output_file_suffix
                    print(f"opening file {output_file_name}") 
                    with open(output_file_name, 'w', encoding='utf-8') as f:
                        f.write(f"---- Text from {filename} ----\n")
                        f.write(text + "\n\n")
            except Exception as e:
                print(f"Error processing file {filename} - {e.__cause__}")
            

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)  # Directory of the current script
    folder_path = os.path.join(base_dir, "source", "test-output")
    ocr_images(folder_path)