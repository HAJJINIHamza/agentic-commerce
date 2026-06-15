import os 
from src.logger import get_logger
from datetime import datetime

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
