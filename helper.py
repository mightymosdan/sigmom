#!/usr/bin/env python3

import altair as alt
import numpy as np
import pandas as pd
import plotly
import plotly.express as px


def sig_mom_source_pie_chart(df, positive_only=True):
    # If positive_only, modify data frame to keep only positive significant moments
    if positive_only:
        df = df[df["PANAS Score"] > 0]

    # Create data frame for sources of significant moments and their counts
    df = pd.DataFrame(
        df["Who/what caused this significant moment (e.g. Self, someone, something)?"]
        .value_counts()
        .reset_index()
    )

    # Rename columns of data frame
    df = df.rename(
        columns={
            "index": "source",
            "Who/what caused this significant moment (e.g. Self, someone, something)?": "count",
        }
    )

    # Combine all external sources
    df["internal/external"] = np.where(df["source"] == "Self", "internal", "external")
    df = df.groupby("internal/external").sum().reset_index()

    # Rename columns of data frame
    df = df.rename(
        columns={
            "internal/external": "source",
        }
    )

    # Create and show a pie chart that shows more details on mouse hover
    pie_source_count = px.pie(
        data_frame=df,
        values="count",
        names="source",
        color="source",
        title="Sources of Positive Significant Moments",
    )
    pie_source_count.show()


def sig_mom_panas_score_bar_chart(df, positive_only=True):
    # Add a new column to specify whether the cause is internal or external
    df["source"] = np.where(
        df["Who/what caused this significant moment (e.g. Self, someone, something)?"]
        == "Self",
        "internal",
        "external",
    )

    # If positive_only, modify data frame to keep only positive significant moments
    if positive_only:
        df = df[df["PANAS Score"] > 0]

    # Get desired columns
    df = df[["Date (dd/mm/yy)"] + ["source"] + ["PANAS Score"]]

    # Sum up PANAS scores for each combination of day and source
    df = df.groupby(["Date (dd/mm/yy)", "source"]).sum().reset_index()

    # Create and show a bar graph with a drop-down box for filtering dates
    dropdown_box = alt.binding_select(
        options=list(dict.fromkeys(df["Date (dd/mm/yy)"])), name="Date (dd/mm/yy)"
    )
    selection = alt.selection_single(fields=["Date (dd/mm/yy)"], bind=dropdown_box)
    return (
        alt.Chart(df)
        .mark_bar()
        .encode(
            color=alt.condition(selection, "source", alt.value("lightgray")),
            column="Date (dd/mm/yy)",
            x="source",
            y="PANAS Score",
        )
        .add_selection(selection)
    )


def sig_mom_panas_word_bar_chart(df, positive_only=True):
    # Add a new column to specify whether the cause is internal or external
    df["source"] = np.where(
        df["Who/what caused this significant moment (e.g. Self, someone, something)?"]
        == "Self",
        "internal",
        "external",
    )

    # Split "Why did this situation cause a significant moment?, Relevant PANAS word" into two
    df[
        ["Why did this situation cause a significant moment?", "Relevant PANAS word"]
    ] = df[
        "Why did this situation cause a significant moment?, Relevant PANAS word"
    ].str.split(
        ",", expand=True
    )

    # If positive_only, modify data frame to keep only positive significant moments
    if positive_only:
        df = df[df["PANAS Score"] > 0]

    # Get desired columns
    df = df[["source"] + ["Relevant PANAS word"]]

    # Count instances of combination of source and relevant PANAS word
    df = df.groupby(["source", "Relevant PANAS word"]).size().reset_index()
    df = df.rename(columns={0: "count"})

    # Create and show a scatter plot with multi-selectable points
    multi_sel = alt.selection_multi()
    return (
        alt.Chart(df)
        .mark_bar()
        .encode(
            color=alt.condition(multi_sel, "source", alt.value("lightgray")),
            column="Relevant PANAS word",
            x="source",
            y="count",
        )
        .add_selection(multi_sel)
    )
