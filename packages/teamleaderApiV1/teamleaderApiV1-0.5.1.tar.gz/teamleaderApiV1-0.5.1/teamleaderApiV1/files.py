import base64


class Files:
    def __init__(self, get_teamleader, post_teamleader) -> None:
        self.get = get_teamleader
        self.post = post_teamleader

    def upload(self, company_id, file_name, folder_name, file_path):
        with open(file_path, "rb") as binary_file:
            binary_file_data = binary_file.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            extra_data = {
                "object_type": "company",
                "object_id": company_id,
                "file_content": base64_encoded_data,
                "file_name": file_name,
                "folder_name": folder_name,
            }
            return self.post(url_addition="uploadFile", additional_data=extra_data)
        raise Exception("No file uploaded")
