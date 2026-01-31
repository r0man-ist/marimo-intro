import marimo

__generated_with = "0.16.4"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
    # Eine kurze Einführung in Marimo

    https://docs.marimo.io/

    """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    print("Hello from the Staatsbibliothek")
    return


@app.cell
def _(mo):
    mo.md(
        """
    # Überschrift
    - Text, der auch in der App-View angezeigt wird
    """
    )
    return


@app.cell
def _():
    a = 6
    b = 2
    return a, b


@app.cell
def _(mo):
    mo.md(r"""## Eine erste reaktive Zelle""")
    return


@app.cell
def _(a, b):
    a+b
    return


@app.cell
def _(mo):
    mo.md(r"""## UI-Elemente, die auf reaktive Zellen wirken""")
    return


@app.cell
def _(mo):
    slider = mo.ui.slider(start=1, stop=10, step=1)
    slider
    return (slider,)


@app.cell
def _(b, slider):
    slider.value+b
    return


@app.cell
def _(mo):
    mo.md(r"""## Text-Element und Kontrolle über Ausführung reaktiver Zellen""")
    return


@app.cell
def _(mo):
    text = mo.ui.text(placeholder="Wie heißt du?")
    text
    return (text,)


@app.cell
def _(mo, text):
    mo.stop (not text.value)
    mo.md(f"""Hello from {text.value}!""")
    return


@app.cell
def _(mo):
    switch = mo.ui.switch(label="Schalte mich!")
    return (switch,)


@app.cell
def _(mo, switch):
    mo.hstack([switch, mo.md(f"Schalter umgelegt = {switch.value}")])
    return


@app.cell
def _(mo):
    button = mo.ui.button(
        value="", on_click=lambda value: value + "🐻", label="Drück mich!", kind="warn"
    )
    button
    return (button,)


@app.cell
def _(button, mo):
    mo.stop (not button.value == "🐻🐻🐻")
    button.value  
    return


@app.cell
def _(mo):
    callout_kind = mo.ui.dropdown(
        label="Farbe",
        options=["info", "neutral", "danger", "warn", "success"],
        value="neutral",
    )
    return (callout_kind,)


@app.cell
def _(callout_kind, mo):
    callout = mo.callout("Callout-Box", kind=callout_kind.value)
    return (callout,)


@app.cell
def _(callout, callout_kind, mo):
    mo.vstack([callout_kind, callout], align="stretch", gap=0)
    return


@app.cell
def _(mo):
    mo.md(r"""## Umgang mit Daten und Dataframes""")
    return


@app.cell
def _():
    import pandas as pd
    import altair as alt
    return alt, pd


@app.cell
def _(pd):
    data = {
        "Monat": ["Januar", "Februar", "März", "April", "Mai", "Juni"],
        "Besucherzahlen": [120, 150, 180, 80, 95, 110]
    }

    df = pd.DataFrame(data)
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _(mo):
    mo.md(r"""### UI-Elemente zur Manipulation von Daten""")
    return


@app.cell
def _(df, mo):
    editor = mo.ui.data_editor(df)

    editor
    return (editor,)


@app.cell
def _(editor, pd):
    df_edited = pd.DataFrame(editor.value)
    df_edited
    return (df_edited,)


@app.cell
def _(df_edited, mo):
    import plotly.express as px

    # Create a bar chart
    fig = plot = mo.ui.plotly(px.bar(df_edited, x='Monat', y='Besucherzahlen', title='Besucherzahlen pro Monat',
                 labels={'Monat':'Monat', 'Besucherzahlen':'Besucherzahlen'},
                 color='Monat', color_discrete_sequence=px.colors.qualitative.Plotly))

    # Show the plot
    fig
    return (fig,)


@app.cell
def _(fig):
    fig.value
    return


@app.cell
def _(fig, pd):
    df_select =pd.DataFrame(fig.value)
    df_select
    return


@app.cell
def _(mo):
    mo.md(
        """
    ### Interaktive Widgets

          siehe: https://koaning.github.io/drawdata/
    """
    )
    return


@app.cell
def _():
    from drawdata import ScatterWidget
    return (ScatterWidget,)


@app.cell
def _(ScatterWidget, mo):
    widget = mo.ui.anywidget(ScatterWidget(height=400, width=400))
    widget
    return (widget,)


@app.cell
def _(alt, mo, widget):
    out = mo.md("Draw some data to see the effect here.")

    if widget.value["data"]:
        base = alt.Chart(widget.data_as_pandas)
        base_bar = base.mark_bar(opacity=0.3, binSpacing=0)
        color_domain = widget.data_as_pandas["color"].unique()

        xscale = alt.Scale(domain=(0, widget.value["width"]))
        yscale = alt.Scale(domain=(0, widget.value["height"]))
        colscale = alt.Scale(domain=color_domain, range=color_domain)

        points = base.mark_circle().encode(
            alt.X("x").scale(xscale),
            alt.Y("y").scale(yscale),
            color="color",
        )

        top_hist = base_bar.encode(
            alt.X("x:Q")
            # when using bins, the axis scale is set through
            # the bin extent, so we do not specify the scale here
            # (which would be ignored anyway)
            .bin(maxbins=30, extent=xscale.domain)
            .stack(None)
            .title(""),
            alt.Y("count()").stack(None).title(""),
            alt.Color("color:N", scale=colscale),
        ).properties(height=60)

        right_hist = base_bar.encode(
            alt.Y("y:Q").bin(maxbins=30, extent=yscale.domain).stack(None).title(""),
            alt.X("count()").stack(None).title(""),
            alt.Color("color:N"),
        ).properties(width=60)

        out = top_hist & (points | right_hist)

    out
    return


@app.cell
def _(mo):
    mo.md(r"""### Datenbankunterstützung""")
    return


@app.cell
def _(df, mo):
    _df = mo.sql(
        f"""
        SELECT Monat, Besucherzahlen
        FROM df
        ORDER BY (Besucherzahlen) DESC
        LIMIT 1;
        """
    )
    return


if __name__ == "__main__":
    app.run()
