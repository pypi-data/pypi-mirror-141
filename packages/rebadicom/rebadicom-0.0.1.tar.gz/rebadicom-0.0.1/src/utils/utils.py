__author__ = "Frank Kwizera"

import pydicom


class Utils:
    @staticmethod
    def read_dicom_file(dicom_file_path: str) -> pydicom.dataset.FileDataset:
        """
        Reads dicom file from a given file path.
        Inputs:
            - dicom_file_path: File path.
        Returns:
            - Dicom file dataset.
        """
        return pydicom.dcmread(dicom_file_path)
