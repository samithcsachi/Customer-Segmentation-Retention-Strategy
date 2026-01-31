from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Dict



@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    local_data_file_reading: Path
    local_data_file_users: Path