from . import data
locs = data.locations

def reshaper(df):
    temp = df.groupby(["år"], as_index=True)["value"].sum().reset_index()
    temp["type"] = "historisk"
    temp = temp[["value", "type"]].merge(df[df["alder"]=="65 år eller eldre"].groupby(["år"], as_index=True)["value"].sum().reset_index().rename(columns={"value":"Personer over 65"}),
                  how="left", left_index=True, right_index=True)
    temp = temp[["value", "type", "Personer over 65"]].merge(df[df["alder"]=="0-19 år"].groupby(["år"], as_index=True)["value"].sum().reset_index().rename(columns={"value":"Personer under 19"}),
                  how="left", left_index=True, right_index=True)
    temp.rename(columns={"value": "Antall innbyggere"}, inplace=True)
    return temp

class InputFormater:
    def __init__(self, inntastet_verdi):
        self.input = inntastet_verdi
        # returner kommunenummer
        try:
            self.id_nr = int(self.input[0])
        except:
            self.id_nr = locs[self.input[0].title()]
        # return med K-foran
        self.idnr_K = ["K-" + i for i in [str(self.id_nr)]]
        # returner kommunenavn
        self.navn = list(locs.keys())[list(locs.values()).index(self.id_nr)]

def graph(df, variabel, område):
    import plotly.graph_objects as go

    x_data = df["år"]
    y_data = df[variabel]
    title = f"Innbyggere i {område}"
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines',
                             name="Antall innbyggere",
                             line=dict(color='rgb(67,67,67)', width=2),
                             connectgaps=True,
                             ))

    # endpoints
    fig.add_trace(go.Scatter(
        x=[x_data.iloc[0], x_data.iloc[-1]],
        y=[y_data.iloc[0], y_data.iloc[-1]],
        mode='markers',
        marker=dict(color='rgb(67,67,67)', size=8)
    ))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=20,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []

    # Adding labels

    # labeling the left_side of the plot
    annotations.append(dict(xref='paper', x=13 / x_data.count(), y=y_data[15],
                            xanchor='right', yanchor='middle',
                            text="Antall innbyggere",
                            font=dict(family='Arial',
                                      size=14,
                                      color='rgb(67,67,67)', ),
                            showarrow=False))

    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                            xanchor='left', yanchor='bottom',
                            text=title,
                            font=dict(family='Arial',
                                      size=24,
                                      color='rgb(37,37,37)'),
                            showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=1, y=-0.2,
                            xanchor='right', yanchor='top',
                            text='Source: ssb.no tabell 07459: Befolkning, etter region, alder, år og statistikkvariabel & ' +
                                 'www.trifektum.no',
                            font=dict(family='Arial',
                                      size=12,
                                      color='rgb(150,150,150)'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)

    graph = fig.to_html(full_html=False)
    return graph