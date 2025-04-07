content='```yml
flow:
  - id: READ_BQ_1
    type: BigQueryReader
    dataset: project_op
    project: tejas
    table: newtable
  - id: WRITE_GCS_1
    type: GCSWriter
    path: gs://tejas/backup/sales.csv
    format: csv
```' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 77, 'prompt_tokens': 889, 'total_tokens': 966, 'completion_tokens_details': None, 'prompt_tokens_details': None}, 'model_name': 'llama-3.2-8x3b-moe-dark-champion-instruct-uncensored-abliterated-18.4b', 'system_fingerprint': 'llama-3.2-8x3b-moe-dark-champion-instruct-uncensored-abliterated-18.4b', 'id': 'chatcmpl-qp0eevolj1dkwbrxtef2g', 'finish_reason': 'stop', 'logprobs': None} id='run-099109ba-ec26-43b8-b974-9a84eaab6cfe-0' usage_metadata={'input_tokens': 889, 'output_tokens': 77, 'total_tokens': 966, 'input_token_details': {}, 'output_token_details': {}}
