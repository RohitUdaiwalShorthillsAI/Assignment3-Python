import os
from file_processing import FileProcessor

class Main:
    def main(self):
        filePath = input("Enter File Path : ")
        storage_type = input("Enter the storage type (sql or file): ")

        # Extract the file extension
        file_type = os.path.splitext(filePath)[1][1:]  # Extracts the file extension
        print(file_type)
        if not os.path.exists(filePath):
            print("File does not exist.")  # File doesn't exist
        # Check file extension and validate type
        if file_type in ['pdf', 'docx', 'pptx']:
            print("File is valid.")  # File exists and is valid
        else:
            print("Unsupported file type. Only PDF, DOCX, and PPTX files are supported.")

        FileProcessor.process_file(
            file_type=file_type, 
            file_path=filePath, 
            storage_type=storage_type, 
            storage_path=f'./output/{os.path.basename(filePath)}_files'
        )

if __name__ == "__main__":
    instance = Main()
    instance.main()
