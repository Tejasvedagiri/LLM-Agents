from typing import Union, List

from dotenv import load_dotenv
from langchain.output_parsers import YamlOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool, tool
from langchain.tools.render import render_text_description
from langchain.agents.format_scratchpad import format_log_to_str

from model.etl_model import ETLModel
from model.gcs_writer_model import GCSWriterModel
from model.bigquey_reader_model import BigQueryReaderModel
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser


load_dotenv()
import os


@tool
def get_etl_config_template(component_name: str) -> str:
    """Returns the ETL configuration template for a given component name."""
    print(component_name)
    if component_name == "BigQueryReader":
        comp_mode = BigQueryReaderModel
    # if component_name == "AggregateTransformer":
    #     return "id: <REPLACE_WITH_UNIQUE_ID>\n" \
    #             "type: AggregateTransformer\n" \
    #            "group_by: <REPLACE_ME_WITH_GROUP_BY_COLUMNS>\n" \
    #            "aggregate_columns: <REPLACE_ME_WITH_AGGREGATE_COLUMNS>\n" \
    #            "aggregate_function: <REPLACE_ME_WITH_FUNCTION>\n"
    if component_name == "GCSWriter":
        comp_mode =  GCSWriterModel
    return PydanticOutputParser(pydantic_object=comp_mode).get_format_instructions()


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")


if __name__ == "__main__":
    print("Hello ReAct LangChain!")
    tools = [get_etl_config_template]
    components = ["BigQueryReader", "AggregateTransformer", "GCSWriter"]
    agent_scratchpad = []

    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    You also have access to following ETL components and no custom components or properties are allowed:
    
    {components}
    
    One sample ETL flow is:
    
    {etl_flow_sample}
    
    Use the following format:

    Question: the input question you must answer as an ETL config
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the question must follow the example format below
    
   {format_instructions}

    Begin!

    Question: {input}
    Thought:
    agent_scratchpad: {agent_scratchpad}
    """

    parser = YamlOutputParser(pydantic_object=ETLModel)
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        components= ", ".join(components),
        tool_names=", ".join([t.name for t in tools]),
        format_instructions= parser.get_format_instructions(),
        etl_flow_sample = """
        flow=
          - id: READ_BQ_1
            type: BigQueryReader
            dataset: sales
            project: tejas
            table: sales
          - id: WRITE_GCS_1
            type: GCSWriter
            path: gs://tejas/temp/sales.csv
            format: csv
        """

    )

    llm = ChatOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_API_BASE_URL"],
        model=os.environ["MODEL"],
        temperature=0,
        max_tokens=1500,
        verbose=True,
        stop_sequences=["/nObservation:"]  # Ensure to stop at the right place
    )
    intermediate_steps = []

    agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"])
            }
            | prompt
            | llm
           # | parser.get_format_instructions()
    )

    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        {
            "input": "Read from Bigquery table project is project_op, dataset is temp and table name is newtable and write it to GCS as csv file path gs://tejas/backup/sales.csv",
            "agent_scratchpad": "\n".join(agent_scratchpad)
        }
    )
    print(agent_step)