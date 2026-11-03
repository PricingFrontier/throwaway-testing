"""Pipeline: throwaway-testing"""

import haute
import polars as pl

pipeline = haute.Pipeline("throwaway-testing")


@pipeline.api_input(config="config/quote_input/api_input.json")
def api_input(): ...


@pipeline.edge_join(how="left", on=["quote_id"], maintain_order="left_right")
def edge_join(live_switch, data_input_2): ...


@pipeline.polars(selected_columns=["quote_id", "premium"])
def premium(edge_join: pl.LazyFrame) -> pl.LazyFrame:
    df = edge_join
    df = df.with_columns(pl.lit(500).alias("premium"))
    return df


@pipeline.output(config="config/quote_response/output.json")
def output(premium): ...


@pipeline.data_input(config="config/data_input/data_input.json")
def data_input(): ...


@pipeline.live_switch(config="config/source_switch/live_switch.json")
def live_switch(data_input, quote_info): ...


@pipeline.data_input(config="config/data_input/data_input_2.json")
def data_input_2(): ...


@pipeline.modelling(config="config/model_training/modelling.json")
def modelling(edge_join): ...


pipeline.connect("api_input", "live_switch", source_port="quote_info")
pipeline.connect("live_switch", "edge_join", target_port="base")
pipeline.connect("data_input_2", "edge_join", target_port="join")
