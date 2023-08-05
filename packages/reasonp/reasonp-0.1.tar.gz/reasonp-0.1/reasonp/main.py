import pandas as pd
import ipdb


def find_reason(
    df: pd.DataFrame,
    compare_column: str,
    compare_values: tuple,
    compare_metric: tuple = None,
    limit=20,
) -> pd.DataFrame:
    """
    find reason for diffrence
    """
    search_columns = [col for col in df.columns if df.dtypes[col].name in ["object"]]
    reason_data_map = {}
    for search_column in search_columns:
        sub_reason_data = get_sub_reason_data(
            df,
            search_column,
            compare_column,
            compare_values,
            compare_metric,
        )
        reason_data_map[search_column] = sub_reason_data
    total_diffrence_data = reason_data_map.pop(compare_column)
    total_diffrence = (
        total_diffrence_data["target_metric_value"].sum()
        - total_diffrence_data["compare_metric_value"].sum()
    )
    reason_df = pd.concat(reason_data_map.values())
    reason_df["reason_coef"] = reason_df["metric_change"] / total_diffrence
    ordered_columns = [
        "search_column",
        "target_column_value",
        "compare_column_value",
        "target_metric_value",
        "compare_metric_value",
        "metric_change",
        "reason_coef",
    ]
    return (
        reason_df[ordered_columns]
        .sort_values("reason_coef", ascending=False)
        .head(limit)
    )


def get_sub_reason_data(
    df: pd.DataFrame,
    search_column: str,
    compare_column: str,
    compare_values: tuple,
    compare_metric: tuple = None,
):
    """
    find reason from single search column
    """
    assert len(compare_values) == 2, "Length of compare_values should be 2. "
    target_column_value, compare_column_value = compare_values
    left_df = df[df[compare_column] == target_column_value].groupby(search_column)
    right_df = df[df[compare_column] == compare_column_value].groupby(search_column)

    if isinstance(compare_metric, tuple):
        left_df = left_df.agg(target_metric_value=compare_metric)
        right_df = right_df.agg(compare_metric_value=compare_metric)
    elif isinstance(compare_metric, dict):

        compare_metric_name = list(compare_metric.keys())[0]
        # ipdb.set_trace()
        left_df = left_df.agg(compare_metric).rename(
            {compare_metric_name: "target_metric_value"}, axis=1
        )
        right_df = right_df.agg(compare_metric).rename(
            {compare_metric_name: "compare_metric_value"}, axis=1
        )
    elif isinstance(compare_metric, dict):
        left_df = left_df.agg(target_metric_value=(compare_metric, "count"))
        right_df = right_df.agg(compare_metric_value=(compare_metric, "count"))
    else:
        left_df = left_df.agg(target_metric_value=(compare_column, "count"))
        right_df = right_df.agg(compare_metric_value=(compare_column, "count"))

    left_df.index.name = "target_column_value"
    right_df.index.name = "compare_column_value"

    merge_df = pd.merge(
        left_df.reset_index(),
        right_df.reset_index(),
        how="outer",
        left_on="target_column_value",
        right_on="compare_column_value",
    )
    fill_na_columns = ["target_metric_value", "compare_metric_value"]
    merge_df[fill_na_columns] = merge_df[fill_na_columns].fillna(0)
    sub_reason_data = merge_df.assign(
        search_column=search_column,
        metric_change=merge_df["target_metric_value"]
        - merge_df["compare_metric_value"],
    )
    return sub_reason_data


def find_insight(df, metric):
    raise NotImplementedError()
