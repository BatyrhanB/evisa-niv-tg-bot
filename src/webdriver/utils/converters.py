import base64
import tempfile


class Base64ToPngConverter:
    def __init__(self, base64_string):
        self.base64_string = base64_string
        self.temp_file_path = None

    def convert_and_save_temp(self):
        binary_data = base64.b64decode(self.base64_string)

        _, temp_file_path = tempfile.mkstemp(suffix=".png")
        self.temp_file_path = temp_file_path

        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(binary_data)

        return temp_file_path
