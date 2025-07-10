import os
from typing import List

class LogDiscovery:
    def __init__(self, config):
        self.config = config
        self.extensions = config.log_extensions
        self.base_dir = config.log_base_dir
        self.priority_logs = config.priority_logs


    def discover_all_logs(self) -> List[str]:
        log_files = []

        try:
            for root, dirs, files in os.walk(self.base_dir):
                for file in files:
                    if self._is_log_file(file):
                        filepath = os.path.join(root,file)
                        if self._is_readable(filepath):
                            log_files.append(filepath)

        except Exception as e:  
            print(f"Error in accessing {self.base_dir}: {e}")

        return sorted(log_files)
    

    def get_priority_logs(self) -> List[str]:
        """gets the priority logs"""
        all_logs = self.discover_all_logs()
        priority_logs = []

        for log_file in all_logs:
           for priority in self.priority_logs:
               if priority in os.path.basename(log_file):
                   priority_logs.append(log_file)
                   break
        
        return priority_logs
    
    def find_app_logs(self, appname:str) -> List[str]:
        "find all logs related to the app"

        app_logs = []
        appname_lower = appname.lower()
        


    
    def _is_log_file(self,filename: str) -> bool:
        """checking whether the files ends with a particular type of extension"""
        return any(filename.endswith(ext) for ext in self.extensions)
    
    def _is_readable(self,filepath: str) -> bool:
        """checking whether the file is readable"""
        try:
            with open(filepath,"r") as f:
                f.read(1)
            return True
        except Exception:
            return False
        
    



