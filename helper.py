#!/usr/bin/env python3

import altair as alt
import numpy as np
import pandas as pd
import plotly
import plotly.express as px


def create_pie_chart(df):
    # Modify data frame to keep only positive significant moments
    df = df[df["PANAS Score"] > 0]

    # Create data frame for sources of significant moments and their counts
    df_source_count = pd.DataFrame(
        df["Who/what caused this significant moment (e.g. Self, someone, something)?"]
        .value_counts()
        .reset_index()
    )

    # Rename columns of data frame
    df_source_count = df_source_count.rename(
        columns={
            "index": "source",
            "Who/what caused this significant moment (e.g. Self, someone, something)?": "count",
        }
    )

    # Combine all external sources
    df_source_count["internal/external"] = np.where(
        df_source_count["source"] == "Self", "internal", "external"
    )
    df_source_count = df_source_count.groupby("internal/external").sum().reset_index()

    # Rename columns of data frame
    df_source_count = df_source_count.rename(
        columns={
            "internal/external": "source",
        }
    )

    # Create and show a pie chart that shows more details on mouse hover
    pie_source_count = px.pie(
        data_frame=df_source_count,
        values="count",
        names="source",
        color="source",
        title="Internal versus external sources",
    )
    pie_source_count.show()


def create_h_bar_chart(df):
    # Create data frame for daily net PANAS scores
    df_daily_score = df[["Date (dd/mm/yy)"] + ["PANAS Score"]]
    df_daily_score = df_daily_score.groupby("Date (dd/mm/yy)").sum().reset_index()

    # Create and show a bar graph with a drop-down box for filtering dates
    dropdown_box = alt.binding_select(
        options=list(df_daily_score["Date (dd/mm/yy)"]), name="Date (dd/mm/yy)"
    )
    selection = alt.selection_single(fields=["Date (dd/mm/yy)"], bind=dropdown_box)
    return (
        alt.Chart(df_daily_score)
        .mark_bar()
        .encode(
            x="PANAS Score",
            y="Date (dd/mm/yy)",
            color=alt.condition(selection, "Date (dd/mm/yy)", alt.value("lightgray")),
        )
        .add_selection(selection)
    )


def create_v_bar_chart(df):
    # Create data frame that splits "Why did this situation cause a significant moment?, Relevant PANAS word" into two columns
    df_split = df[
        "Why did this situation cause a significant moment?, Relevant PANAS word"
    ].str.split(",", expand=True)

    # Create data frame of PANAS words and their counts
    df_word_count = pd.DataFrame(df_split[1].value_counts().reset_index())

    # Rename columns of data frame
    df_word_count = df_word_count.rename(columns={"index": "panas word", 1: "count"})

    # Create and show a scatter plot with multi-selectable points
    multi_sel = alt.selection_multi()
    return (
        alt.Chart(df_word_count)
        .mark_bar()
        .encode(
            x=alt.X("panas word", sort="-y"),
            y="count",
            color=alt.condition(multi_sel, "panas word", alt.value("lightgray")),
        )
        .add_selection(multi_sel)
    )
