import os
from file_processing import FileProcessor

class Main:
    def main(self):
        filePath = input("Enter File Path : ")
        storage_type = input("Enter the storage type (sql or file): ")

        # Extract the file extension
        file_type = os.path.splitext(filePath)[1][1:]  # Extracts the file extension
        print(file_type)

        FileProcessor.process_file(
            file_type=file_type, 
            file_path=filePath, 
            storage_type=storage_type, 
            storage_path=f'./output/{os.path.basename(filePath)}_files'
        )

if __name__ == "__main__":
    instance = Main()
    instance.main()
