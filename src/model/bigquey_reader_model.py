from pydantic import BaseModel

class BigQueryReaderModel(BaseModel):
    """
    Model for BigQuery Reader configuration.

    :param id: Unique identifier for the BigQuery Reader.
    :type id: str
    :param type: Type of the reader, defaults to "BigQueryReader".
    :type type: str
    :param project: Project ID for the BigQuery dataset.
    :type project: str
    :param dataset: Dataset ID for the BigQuery dataset.
    :type dataset: str
    :param table: Table ID for the BigQuery table.
    :type table: str
    """
    id: str
    type: str = "BigQueryReader"
    project: str
    dataset: str
    table: str