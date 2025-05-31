import json
import zipfile
from pathlib import Path
from typing import Union
from dataclasses import dataclass

from .showfile import ShowFile, showfile_from_dict, showfile_to_dict
from .settings import Settings


@dataclass
class LsfFile:
    """Handles ETC Colorsource LSF (Light Show File) format.

    LSF files are ZIP archives containing two JSON files:
    - showfile.json: Main show data (cues, palettes, patch, etc.)
    - settings.json: Console settings and configuration
    """

    showfile: ShowFile
    settings: Settings

    @classmethod
    def from_file(cls, filepath: Union[str, Path]) -> "LsfFile":
        """Load an LSF file from disk.

        Args:
            filepath: Path to the .lsf file

        Returns:
            LsfFile instance with parsed showfile and settings data

        Raises:
            FileNotFoundError: If the file doesn't exist
            zipfile.BadZipFile: If the file is not a valid ZIP
            KeyError: If required files are missing from the ZIP
            json.JSONDecodeError: If the JSON files are malformed
        """
        filepath = Path(filepath)

        with zipfile.ZipFile(filepath, "r") as zf:
            # Read showfile.json
            try:
                showfile_data = zf.read("showfile.json")
                showfile_dict = json.loads(showfile_data.decode("utf-8"))
                showfile = showfile_from_dict(showfile_dict)
            except KeyError:
                raise KeyError("showfile.json not found in LSF archive")

            # Read settings.json
            try:
                settings_data = zf.read("settings.json")
                settings_dict = json.loads(settings_data.decode("utf-8"))
                settings = Settings.from_dict(settings_dict)
            except KeyError:
                raise KeyError("settings.json not found in LSF archive")

        return cls(showfile=showfile, settings=settings)

    def to_file(self, filepath: Union[str, Path]) -> None:
        """Save the LSF file to disk.

        Args:
            filepath: Path where to save the .lsf file
        """
        filepath = Path(filepath)

        with zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED) as zf:
            # Write showfile.json
            showfile_dict = showfile_to_dict(self.showfile)
            showfile_json = json.dumps(showfile_dict, indent=2).encode("utf-8")
            zf.writestr("showfile.json", showfile_json)

            # Write settings.json
            settings_dict = self.settings.to_dict()
            settings_json = json.dumps(settings_dict, indent=2).encode("utf-8")
            zf.writestr("settings.json", settings_json)

    def extract_json_files(self, output_dir: Union[str, Path]) -> None:
        """Extract the JSON files to a directory for inspection.

        Args:
            output_dir: Directory where to extract the JSON files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Write showfile.json
        showfile_dict = showfile_to_dict(self.showfile)
        showfile_path = output_dir / "showfile.json"
        with open(showfile_path, "w", encoding="utf-8") as f:
            json.dump(showfile_dict, f, indent=2)

        # Write settings.json
        settings_dict = self.settings.to_dict()
        settings_path = output_dir / "settings.json"
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings_dict, f, indent=2)

    @property
    def show_name(self) -> str:
        """Get the show file name from the showfile data."""
        return self.showfile.play.show_file_name

    @property
    def software_version(self) -> str:
        """Get the software version from the showfile data."""
        return self.showfile.play.software_version

    @property
    def console_model(self) -> str:
        """Get the console model from the showfile data."""
        return self.showfile.play.console_model
