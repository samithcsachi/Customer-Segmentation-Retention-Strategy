from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Dict



@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    local_data_file: Path



@dataclass(frozen=True)
class DataTransformationConfig:
    source_file_path: str
    root_dir: Path
    data_path: Path


