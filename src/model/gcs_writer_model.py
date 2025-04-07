from pydantic import BaseModel, Field
from enum import Enum

class GCSFormatEnum(str, Enum):
    """
    Enumeration for GCS file formats.

    :cvar CSV: CSV file format.
    :cvar ORC: ORC file format.
    """
    CSV = 'csv'
    ORC = 'orc'

class GCSWriterModel(BaseModel):
    """
    Model for GCS Writer configuration.

    :param id: Unique identifier for the GCS Writer.
    :type id: str
    :param type: Type of the writer, defaults to "GCSWriter".
    :type type: str
    :param format: Format of the file to be written.
    :type format: GCSFormatEnum
    :param path: Path to the GCS location, must start with 'gs://'.
    :type path: str
    """
    id: str
    type: str = "GCSWriter"
    format: GCSFormatEnum
    path: str = Field(pattern=r"^gs://")