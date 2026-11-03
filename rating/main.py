"""Pipeline: throwaway-testing"""

import haute
import polars as pl

pipeline = haute.Pipeline("throwaway-testing")


@pipeline.api_input(config="config/quote_input/api_input.json")
def api_input(): ...


@pipeline.polars(selected_columns=["quote_id", "premium"])
def premium(quote_info: pl.LazyFrame) -> pl.LazyFrame:
    df = quote_info
    df = df.with_columns(pl.lit(500).alias("premium"))
    return df


@pipeline.output(config="config/quote_response/output.json")
def output(premium): ...


pipeline.connect("api_input", "premium", source_port="quote_info")
