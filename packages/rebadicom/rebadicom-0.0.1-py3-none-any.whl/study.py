# authors : Frank Kwizera <frankpmn@gmail.com>
# license : MIT

from src.image import Image
import os
from typing import List


class Study:
    def __init__(self, dicom_study_directory_path: str):
        self.dicom_study_directory_path: str = dicom_study_directory_path
        self.all_file_paths: List[str] = \
            [os.path.join(self.dicom_study_directory_path, filename) for filename in
             os.listdir(self.dicom_study_directory_path) if
             os.path.isfile(os.path.join(self.dicom_study_directory_path, filename))]

        self.all_study_images: List[Image] = []
        self.read_all_dicom_images()

    def read_all_dicom_images(self):
        """
        Reads all study dicom images.
        """
        for file_path in self.all_file_paths:
            self.all_study_images.append(Image(dicom_file_path=file_path))

    def save(self):
        """
        Saves all study dicom images.
        """
        for study_image in self.all_study_images:
            study_image.save()



dicom_study_directory_path: str = '/Users/frankwizera/Downloads/series-00000 5'
study: Study = Study(dicom_study_directory_path=dicom_study_directory_path)
study.save()

