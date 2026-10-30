import os 
from pathlib import Path
from src.logger import get_logger
from datetime import datetime
from pypdf import PdfReader, PdfWriter

logger = get_logger(__name__)

def save_csv_file(file, file_name, directory):
    """
    Save a file (dataframe) into a csv file in directory

    Params:

    file : dataframe to save
    file_name : Name of the file without the extension (.csv) ex: output not output.csv
    directory : directory, example : "Documents/my_folder/"
    """

    current_date = datetime.now().strftime("%d-%m-%Y_%H-%M")
    try :
        os.makedirs(directory, exist_ok=True)
        file_name = f"{file_name}_{current_date}.csv"
        file_directory = os.path.join(directory, file_name)
        file.to_csv(file_directory, index=False)
        logger.info(f"Saved file {file_name} on {directory}")

    except Exception as e :
        raise ValueError(f"Couldn't save file :{file_directory}. Error : {e} ")


def split_pdf_by_pages(pdf_path: str, num_of_pages: int) -> None:
    """Split a PDF into same-directory parts containing at most num_of_pages pages."""
    if num_of_pages <= 0:
        raise ValueError("num_of_pages must be a positive integer")

    pdf_path = Path(pdf_path)
    reader = PdfReader(str(pdf_path))
    output_stem = pdf_path.stem

    for part_number, start_page in enumerate(
        range(0, len(reader.pages), num_of_pages),
        start=1,
    ):
        writer = PdfWriter()
        end_page = min(start_page + num_of_pages, len(reader.pages))
        for page_number in range(start_page, end_page):
            writer.add_page(reader.pages[page_number])

        output_path = pdf_path.with_name(f"{output_stem}_part_{part_number}.pdf")
        with output_path.open("wb") as output_file:
            writer.write(output_file)

        logger.info(
            "Saved pages %s-%s to %s",
            start_page + 1,
            end_page,
            output_path,
        )

if __name__ == "__main__":
    # Example usage
    pdf_path = "ressources/rag_documents/principles_of_marketing_book.pdf"
    split_pdf_by_pages(pdf_path, 238)
