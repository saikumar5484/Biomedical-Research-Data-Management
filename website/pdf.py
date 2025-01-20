import os

# Define the directory path
directory = os.path.join('path', 'to', 'fake', 'documents')

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

from reportlab.pdfgen import canvas
import os

# Define the directory path
directory = os.path.join('path', 'to', 'fake', 'documents')

# Function to create a test PDF
def create_test_pdf(file_name):
    file_path = os.path.join(directory, file_name)
    c = canvas.Canvas(file_path)
    c.drawString(100, 750, f"This is a test PDF: {file_name}")
    c.drawString(100, 735, "Generated using ReportLab.")
    c.save()
    print(f"PDF created at: {file_path}")

# Generate multiple PDFs
for i in range(1, 1201):  # Create 1200 sample PDFs
    create_test_pdf(f'project_{i}.pdf')
