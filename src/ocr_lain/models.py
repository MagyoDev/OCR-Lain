from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ExtractedBlock:

    source_file: str
    source_type: str
    location: str
    method: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractResult:

    file_path: Path
    blocks: list[ExtractedBlock]
    errors: list[str] = field(default_factory=list)

    @property
    def full_text(self) -> str:
        return "\n\n".join(block.text for block in self.blocks if block.text.strip())