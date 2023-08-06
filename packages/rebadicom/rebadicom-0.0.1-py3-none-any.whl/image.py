# authors : Frank Kwizera <frankpmn@gmail.com>
# license : MIT

from src.utils.utils import Utils
from pydicom.dataset import FileDataset
from pydicom.dataelem import DataElement
from pydicom.pixel_data_handlers.util import convert_color_space
from typing import Dict, Union, List, Tuple
import matplotlib.pyplot as plt
import cv2
import json


class Image:
    def __init__(self, dicom_file_path: str, convert_ybr_to_rgb: bool = True):
        self.convert_ybr_to_rgb: bool = convert_ybr_to_rgb
        self.image_dataset: FileDataset = Utils.read_dicom_file(dicom_file_path=dicom_file_path)

    def show(self):
        """
        Visualizes dicom pixel array.
        """
        pixel_array = self.image_dataset.pixel_array
        if self.image_dataset.PhotometricInterpretation in ['YBR_FULL', 'YBR_FULL_422']:
            pixel_array = self.convert_color_space_to_rgb()

        plt.imshow(pixel_array)
        plt.show()

    def convert_color_space_to_rgb(self):
        """
        Convert color space to RGB
        """
        converted_pixel_array = \
            convert_color_space(
                arr=self.image_dataset.pixel_array,
                current=self.image_dataset.PhotometricInterpretation, desired="RGB")
        return converted_pixel_array

    def save(self, file_path: str = None) -> str:
        """
        Saves dicom pixel array on a file system.
        Inputs:
            - file_path: Desired file path, If it is not present the default file path is of the following format
                         ``series.{self.image_dataset.SeriesInstanceUID}.instance.{self.image_dataset.InstanceNumber}.png``
        Returns:
            - File path where the png is saved.
        """
        pixel_array = self.image_dataset.pixel_array
        if self.image_dataset.PhotometricInterpretation in ['YBR_FULL', 'YBR_FULL_422']:
            pixel_array = self.convert_color_space_to_rgb()

        if file_path:
            cv2.imwrite(file_path, pixel_array)

        else:
            file_path: str = f"series.{self.image_dataset.SeriesInstanceUID}.instance.{self.image_dataset.InstanceNumber}.png"
            cv2.imwrite(file_path, pixel_array)

        return file_path

    def to_json(self, json_file_path: str = None) -> List[Dict[str, Union[str, int, float]]]:
        """
        Converts dicom dataset into a list of dictionary and saves the JSON file on the file system.
        Inputs:
            - json_file_path: Desired json file path to dump the JSON list in.
        Returns:
            - JSON file path if the json was save on the file system, Otherwise a list of dataset elements
              dictionaries.
        """
        dataset_keys: List[Tuple[int, int]] = list(self.image_dataset.keys())
        dataset_keys.remove(('7fe0', '0010'))  # Remove pixel_array tag

        elements: List[Dict[str, Union[str, int, float]]] = []
        for dataset_key in dataset_keys:
            data_element: DataElement = self.image_dataset[dataset_key]
            data_element_dict: Dict[str, Union[str, int, float]] = {
                "value": str(data_element.value),
                "name": str(data_element.name)
            }
            elements.append(data_element_dict)

        if not json_file_path:
            return elements

        with open(json_file_path, 'w') as json_file:
            json.dump(elements, json_file)

        return json_file_path

    def anonymize(self):
        pass
