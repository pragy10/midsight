import os
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List

class Config(BaseModel):
    api_provider: str = "google"
    api_key: Optional[str] = None
    model_name: str = "gemini-2.0-flash"
    max_tokens: int = 500
    
    log_base_dir: str = "/var/log"
    log_extensions: List[str] = [".log","log"]
    priority_logs: List[str] = ["syslog","auth.log","kern.log","user.log","boot.log",
                                "error.log","dpkg.log","cron.log","message","secure"]
    
    basic_check_enable: bool = True
    max_log_per_analysis: int = 10
    token_limit_per_log: int = 2000

    @classmethod
    def load_from_file(cls,config_path: str = "~/.midsight/config.yaml"):
        config_file = Path(config_file).expanduser()
        if config_file.exists():
            import yaml
            with open(config_file) as f:
                data = yaml.safe_load(f)
                return cls(**data)
        return cls
    
    def save_to_file(self,config_path: str = "~/.midsight/config.yaml"):
        config_file = Path(config_path).expanduser()
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        import yaml
        with open(config_file,'w') as f:
            yaml.dump(self.model_dump(),f)
    