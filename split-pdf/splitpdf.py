from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_file, output_dir, pages_per_file):
    reader = PdfReader(input_file)
    total_pages = len(reader.pages)
    for start in range(0, total_pages, pages_per_file):
        writer = PdfWriter()
        for i in range(start, min(start + pages_per_file, total_pages)):
            writer.add_page(reader.pages[i])
        output_file = f"{output_dir}/split_{start // pages_per_file + 1}.pdf"
        with open(output_file, "wb") as f:
            writer.write(f)
        print(f"Created: {output_file}")

# Example Usage
split_pdf("source/my-pdf.pdf", "split-output", 10)  

# Adjust pages_per_file as needed