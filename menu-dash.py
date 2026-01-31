import marimo

__generated_with = "0.16.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import altair as alt
    return alt, mo, pl


@app.cell
def _(pl):
    df = pl.read_csv("metadata.csv")
    return (df,)


@app.cell
def _(mo):
    mo.md(
        """
    # Datenset historische Menükarten
    **Datenset auf Zenodo:** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17245334.svg)](https://doi.org/10.5281/zenodo.17245334)
    """
    )
    return


@app.cell
def _(mo):
    mo.md("""## Übersicht gesamtes Datenset""")
    return


@app.cell
def _(df):
    places = df["Place"].unique()
    subtitles = df["Subtitle"].unique()
    min_year, max_year = int(df["Date"].min()), int(df["Date"].max())
    return max_year, min_year, places


@app.cell
def _(df, max_year, min_year, mo, places):
    mo.hstack([
        mo.stat(label="Anzahl der Menukarten", value=len(df)),
        mo.stat(label="Anzahl der Orte", value=len(places)),
        mo.stat(label="Frühestes Datum", value=min_year),
        mo.stat(label="Spätestes Datum", value=max_year)
    ])
    return


@app.cell
def _(df):
    df
    return


@app.cell
def _(alt, df):
    years = (
        alt.Chart(df)
        # Aggregate counts per year
        .transform_aggregate(
            count='count()',
            groupby=['Date']
        )
        # Impute missing years → fill them with 0
        .transform_impute(
            impute='count',
            key='year',
            value=0
        )
        .mark_bar()
        .encode(
            x=alt.X('Date:O', title='Jahr'),
            y=alt.Y('count:Q', title='Häufigkeit'),
            tooltip=[
                alt.Tooltip('Date:O', title='Jahr'),
                alt.Tooltip('count:Q', title='Häufigkeit')
            ]
        )
        .properties(
            title='Menükarten pro Jahr',
        )
    )

    years
    return


@app.cell
def _(alt, df, max_year, min_year, pl):
    counts = df.group_by('Date').len().rename({'len': 'count'})

    year_range = pl.DataFrame({'Date': list(range(min_year, max_year + 1))})

    year_counts = (
        year_range.join(counts, on='Date', how='left')
        .with_columns(pl.col('count').fill_null(0))
    )



    # --- Altair bar chart ---
    year_dist = (
        alt.Chart(year_counts)
        .mark_bar()
        .encode(
            x=alt.X('Date:O', title='Jahr'),
            y=alt.Y('count:Q', title='Anzahl'),
            tooltip=[
                alt.Tooltip('Date:O', title='Jahr'),
                alt.Tooltip('count:Q', title='Anzahl')
            ]
        )
        .properties(
            title='Menükarten pro Jahr (inkl. leere Jahre)',

        )
    )

    year_dist
    return


@app.cell
def _(mo):
    mo.md("""## Auswahl aus dem Datenset""")
    return


@app.cell
def _(max_year, min_year, mo, places):
    year_range_slider = mo.ui.range_slider(min_year, max_year, value=[min_year, max_year], label="Jahre auswählen", full_width=True)
    place_filter_multiselect = mo.ui.multiselect(options=list(places), label="Orte auswählen", value=list(places), full_width=True)
    return place_filter_multiselect, year_range_slider


@app.cell
def _(mo, place_filter_multiselect, year_range_slider):
    mo.hstack([year_range_slider,
               place_filter_multiselect])
    return


@app.cell
def _(df, pl, place_filter_multiselect, year_range_slider):
    # Reactive filtering based on year range and subtitle selection
    filtered_df = df.lazy()
    filtered_df = filtered_df.filter(
        (pl.col("Date") >= year_range_slider.value[0]) & (pl.col("Date") <= year_range_slider.value[1])
    )
    if place_filter_multiselect.value != None:
        filtered_df = filtered_df.filter(pl.col("Place").is_in(place_filter_multiselect.value))


    filtered_df = filtered_df.collect()
    return (filtered_df,)


@app.cell
def _():
    return


@app.cell
def _(filtered_df, mo):
    mo.hstack([
        mo.stat(label="Anzahl der Menukarten", value=len(filtered_df)),
        mo.stat(label="Anzahl der Orte", value=len(filtered_df["Place"].unique())),
        mo.stat(label="Frühestes Datum", value=int(filtered_df["Date"].min())),
        mo.stat(label="Spätestes Datum", value=int(filtered_df["Date"].max()))
                ])
    return


@app.cell
def _(filtered_df):
    filtered_df
    return


@app.cell
def _(alt, filtered_df, mo):
    place_chart = (
        alt.Chart(filtered_df)
        .mark_bar()
        .encode(
            y=alt.Y('Place:N', sort='-x', title='Ort'),
            x=alt.X('count():Q', title='Häufigkeit'),
            tooltip=['Place', alt.Tooltip('count():Q', title='Count')]
        )
        .properties(
            title='Häufigste Ortsnamen'
        )
    )

    place_chart_mo = mo.ui.altair_chart(place_chart)
    place_chart_mo
    return (place_chart_mo,)


@app.cell
def _(place_chart_mo):
    place_chart_mo.value
    return


@app.cell
def _(alt, filtered_df, mo):
    scatter = (
        alt.Chart(filtered_df)
        # Aggregate counts per (place, date)
        .transform_aggregate(
            count='count()',
            groupby=['Place', 'Date']
        )
        .transform_joinaggregate(
            total='sum(count)',
            groupby=['Place']
        )
        .mark_circle(stroke='black', strokeOpacity=0.2)
        .encode(
            x=alt.X(
                'Place:N',
                sort=alt.EncodingSortField(field='total', order='descending'),
                title='Ort'
            ),
            y=alt.Y('Date:O', title='Jahr'),
            color=alt.Color(
                'count:Q',
                scale=alt.Scale(scheme='viridis'),
                title='Häufigkeit'
            ),
            size=alt.Size('count:Q', title='Häufigkeit', scale=alt.Scale(range=[30, 400])),
            tooltip=[
                alt.Tooltip('Place:N', title='Place'),
                alt.Tooltip('Date:O', title='Year'),
                alt.Tooltip('count:Q', title='Occurrences')
            ]
        )

        .properties(

            title='Verteilung Ortsnamen/Jahr'
        )
    )

    scatter_chart = mo.ui.altair_chart(scatter)
    scatter_chart

    return


if __name__ == "__main__":
    app.run()
