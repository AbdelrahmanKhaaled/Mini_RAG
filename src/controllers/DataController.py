from fastapi import UploadFile
from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ResponseSignal
import re
import os

class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.size_scale = 1024*1024

    def validate_file_type(self, file: UploadFile):
        if (file.content_type not in self.app_settings.FILE_ALLOW_TYPE):
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if (file.size > self.app_settings.FILE_ALLOW_SIZE * self.size_scale):
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value
    
    def generate_unique_filepath(self, original_filename: str, project_id: str):

        project_dir = ProjectController().get_project_path(project_id=project_id)

        random_key = self.generate_random_string()
        cleaned_file_name = self.get_clean_file_name(original_filename=original_filename)

        unique_file_path = project_dir + "/" + random_key + "_" + cleaned_file_name

        while os.path.exists(unique_file_path):
            random_key = self.generate_random_string()
            unique_file_path = project_dir + "/" + random_key + "_" + cleaned_file_name

        return unique_file_path, random_key + "_" + cleaned_file_name

    def get_clean_file_name(self, original_filename: str):
        cleaned_file_name = re.sub(r"[^\w.]", "", original_filename.strip())
        # cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
