import os
import time

from das_emitter.exceptions import DownloadPDFTimeoutException


class DownloadManager:
    def __init__(self, download_path: str) -> None:
        self.download_path = download_path
    
    def file_exists(self, filename: str) -> bool:
        files = os.listdir(self.download_path)
        for file in files:
            if(file == filename):
                return True
        return False
    
    def __get_file_content(self, filename: str) -> bytes:
        path = os.path.join(self.download_path, filename)
        with open(path, mode='br') as file:
            return file.read()
        
    def await_download_file(self, filename: str, timeout: int = 10) -> bytes:
        t0 = time.time()
        while(time.time() - t0 < timeout):
            if(self.file_exists(filename)):
                return self.__get_file_content(filename)
            time.sleep(1)
        raise DownloadPDFTimeoutException(f'Download excedeu o limite de {timeout}s')

    def delete_file(self, filename: str):
        if(self.file_exists(filename)):
            path = os.path.join(self.download_path, filename)
            os.remove(path)