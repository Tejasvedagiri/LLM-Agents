from pydantic import BaseModel, Field
from enum import Enum
from model.bigquey_reader_model import BigQueryReaderModel
from model.gcs_writer_model import GCSWriterModel
class ETLComponents(str, Enum):
    GCS_WRITER = GCSWriterModel
    BIGQUERY_READER = BigQueryReaderModel

class ETLModel(BaseModel):
    """
    Model for ETL configuration.

    :param flow: List of ETL components in the flow. Each component should be a dictionary with 'id', 'type', and other necessary fields.
    :type flow: list[ETLComponents]
    """
    flow: list[ETLComponents] = Field(
        ...,
        description="List of ETL components in the flow. Each component should be a dictionary with 'id', 'type', and other necessary fields."
    )