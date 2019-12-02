from dagster import execute_pipeline, pipeline, as_dagster_type, lambda_solid, dagster_type
from dagit import *
from graphql import  *
from dagster_graphql import *
import pandas as pd

# Data Validations which check that source and destination files should be in #PandasDataFrame format in all the nodes.
DataFrame = as_dagster_type(
    pd.pandas.core.frame.DataFrame,
    name='PandasDataFrame',
)

@lambda_solid #Defines a node in the workflow.
def Input1() -> DataFrame:# first node which reads input file -> file1.csv
    r = pd.read_csv('file1.csv')
    return r

@lambda_solid
def Input2() -> DataFrame:# second node which reads input file ->file2.csv
    r2 = pd.read_csv('file2.csv')
    return r2

@lambda_solid  #Represents third node which merges input from file1 and file2
def Merge(r:DataFrame,r2:DataFrame) -> DataFrame:
    r3 = pd.concat([r, r2], axis=1)
    return r3

@lambda_solid # Fourth node which contains the output merged file.
def Result_output(y:DataFrame) -> DataFrame:
    y3 = y
    y3.to_csv(r'merged_output.csv')
    return y3

@pipeline # definition for pipeline execution
def actual_dag_pipeline() -> DataFrame:
    y=Merge(Input1(),Input2())
    Result_output(y)


