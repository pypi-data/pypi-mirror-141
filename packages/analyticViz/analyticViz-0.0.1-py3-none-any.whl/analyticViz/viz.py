import plotly.express as px
import plotly.figure_factory as ff


"""
This is a script that contains functions needed for plotting various visualizations using plotly

The various viz includes;
* Bar Chart (Horizontal)
* Bar Chart (Vertical)
* Stacked bar chart
* Clustered bar chart
* Pie Chart 
* Histogram
* Box plots
* Facet row plots
* Sunburst
* Violin Plot
"""


def Vbar(data, x_col, y_col, text, title=None, x_title=None, y_title=None, color=None, mode=None):
    """
    Function that plots a vertical bar chart
    
    Args:
        data: dataframe - pandas dataframe 
        x_col: str - column in the dataframe to be plotted on the x-axis
        y_col: str - column in the dataframe to be plotted on the y-axis
        text: str - column name to be used as text display on the bar chart
        title: str - text to be displyed as title for the plot
        x_title: str - text to be displayed on the x-axis
        y_title: str - text to be displayed on the y-axis
        color: str - column name that you want stacked
        mode: str - indicate whether stacked or group(side by side plot)
    
    Returns:
        fig: plot - bar plot to be displayed
    """
    
    # plot bar chart
    fig = px.bar(data, x=x_col, y=y_col, text=text, color=color, barmode=mode, color_discrete_sequence=px.colors.qualitative.D3)
    
    # edit contents of bar chart
    fig.update_traces(texttemplate='%{text:.1s}', textposition='outside', cliponaxis=False, 
                      textfont={'family':"Arial",'size': 13,'color': "black"})
    
    # edit outline of bar chart
    fig.update_xaxes(title_text=x_title, automargin=True, categoryorder='total ascending', type='category')
    fig.update_yaxes(title_text=y_title, automargin=True)
    fig.update_layout(title_text=title, yaxis=dict(visible=False), autosize=False, plot_bgcolor='rgba(0,0,0,0)',
                      title_x=0.5,uniformtext_minsize=5)
    
    return fig.show()


def Hbar(data, x_col, y_col, text, title=None, x_title=None, y_title=None, color=None, f_col=None, f_row=None):
    """
    Function that plots a horizontal bar chart
    
    Args:
        data: dataframe - pandas dataframe 
        x_col: str - column in the dataframe to be plotted on the x-axis
        y_col: str - column in the dataframe to be plotted on the y-axis
        text: str - column name to be used as text display on the bar chart
        title: str - text to be displyed as title for the plot
        x_title: str - text to be displayed on the x-axis
        y_title: str - text to be displayed on the y-axis
        color: str - column name that you want stacked
    
    Returns:
        fig: plot - bar plot to be displayed
    """
    
    # plot bar chart
    fig = px.bar(data, x=x_col, y=y_col, text=text, orientation='h', color=color, 
                facet_col=f_col, facet_row=f_row, color_discrete_sequence=px.colors.qualitative.D3)
    
    # edit contents of bar chart
    fig.update_traces(texttemplate='%{text:.1s}', textposition='outside', cliponaxis=False, 
                      textfont={'family':"Arial",'size': 13,'color': "black"})
    
    # edit outline of bar chart
    fig.update_xaxes(title_text=x_title, automargin=True)
    fig.update_yaxes(title_text=y_title, automargin=True, categoryorder='total ascending', type='category')
    fig.update_layout(title_text=title, xaxis=dict(visible=False), autosize=False, plot_bgcolor='rgba(0,0,0,0)',
                      title_x=0.5, uniformtext_minsize=5)
    
    return fig.show()


def pie(data, values, labels, title=None):
    """
    Function that plots a pie chart
    
    Args:
        data: dataframe - pandas dataframe 
        values: str - column in the dataframe representing numeric values
        labels: str - column in the dataframe representing categorical values
        title: str - text to be displyed as title for the plot
    
    Returns:
        fig: plot - pie chart to be displayed
    """
    # plot pie chart
    fig = px.pie(data, values=values, names=labels, title=title, hole=0.6, color_discrete_sequence=px.colors.qualitative.D3)
    
    # edit pie chart
    fig.update_traces(hoverinfo='label+value', textfont_size=12, marker=dict(line=dict(color='#000000', width=0.5)))
    fig.update_layout(autosize=False, plot_bgcolor='rgba(0,0,0,0)', title_x=0.46, uniformtext_minsize=5)
    
    return fig.show()


def hist(data, x_col, title, plot_type, color=None, f_col=None, f_row=None):
    """
    Function that plots a histogram
    
    Args:
        data: dataframe - pandas dataframe 
        x_col: str - column in the dataframe representing numeric values
        title: str - text to be displyed as title for the plot
        plot_type: str - indcates which additional plot you need (box, violin, rug)
        color: str - column name to be used for multiple histograms
    
    Returns:
        fig: plot - histogram to be displayed
    """
    # plot graph
    fig = px.histogram(data, x=x_col, marginal=plot_type, color=color, hover_data=data.columns,
                       facet_col=f_col, facet_row=f_row, color_discrete_sequence=px.colors.qualitative.D3)
    
    # update or edit graph
    fig.update_layout(autosize=False, plot_bgcolor='rgba(0,0,0,0)', title_x=0.46, uniformtext_minsize=5,
                     yaxis=dict(visible=False), title_text = title)

    return fig.show()


def scatter(data, x_col, y_col, title=None, x_title=None, y_title=None, color=None, size=None, render=None, f_col=None, f_row=None):
    """
    Function that plots a scatter plot
    
    Args:
        data: dataframe - pandas dataframe 
        x_col: str - column in the dataframe representing numeric values
        y_col: str - column in the dataframe representing numeric values
        title: str - text to be displyed as title for the plot
        x_title: str - text to be displayed on the x-axis
        y_title: str - text to be displayed on the y-axis
        size: str - column name to size points with 
        color: str - column name to be used for multiple histograms
        render: str - how to render the viz (webgl or svg)
    
    Returns:
        fig: plot - histogram to be displayed
    """
    # plot graph
    fig = px.scatter(data, x=x_col, y=y_col, color=color, size=size, render_mode=render, 
                    facet_col=f_col, facet_row=f_row, color_discrete_sequence=px.colors.qualitative.D3)

    # edit graph
    fig.update_xaxes(title_text=x_title, automargin=True)
    fig.update_yaxes(title_text=y_title, automargin=True)
    fig.update_traces(marker=dict(line=dict(width=1.5, color='DarkSlateGrey')), selector=dict(mode='markers'))
    fig.update_layout(title_text=title, autosize=False, plot_bgcolor='rgba(0,0,0,0)',
                      title_x=0.5, uniformtext_minsize=5)
    
    return fig.show()


def line(data, x_col, y_col, x_title=None, y_title=None, title=None, color=None, f_col=None, f_row=None):
    """
    Function that plots a line charts
    
    Args:
        data: dataframe - pandas dataframe 
        x_col: str - column in the dataframe representing date values(year, month, day, week, date, datetime)
        y_col: str - column in the dataframe representing numeric values
        title: str - text to be displyed as title for the plot
        x_title: str - text to be displayed on the x-axis
        y_title: str - text to be displayed on the y-axis
        color: str - column name to be used for multiple line plots
    
    Returns:
        fig: plot - line plot to be displayed
    """
    # plot line chart
    fig = px.line(data, x=x_col, y=y_col, color=color, markers=True, facet_col=f_col, facet_row=f_row,
                  color_discrete_sequence=px.colors.qualitative.D3)

    # edit line chart
    fig.update_layout(title_text=title,  yaxis=dict(visible=False), autosize=False, plot_bgcolor='rgba(0,0,0,0)', title_x=0.5, uniformtext_minsize=5)
    
    return fig.show()


def sun(data, path, value, title=None):
    """
    Function that plots a sunburst chart(pie)
    
    Args:
        data: dataframe - pandas dataframe 
        value: str - column in the dataframe representing numeric values
        path: list - list of column names in the dataframe representing categorical values
        title: str - text to be displyed as title for the plot
    
    Returns:
        fig: plot - sunburst chart to be displayed
    """
    # plot chart
    fig = px.sunburst(data, path=path, values=value, color_discrete_sequence=px.colors.qualitative.D3)

    #edit chart
    fig.update_traces(hoverinfo='label+value', textfont_size=12, marker=dict(line=dict(color='#000000', width=0.5)))
    fig.update_layout(title_text=title, autosize=False, plot_bgcolor='rgba(0,0,0,0)', title_x=0.46, uniformtext_minsize=5)
    
    return fig.show()


def table(data, index=None):
    """
    Function that converts pandas dataframe to plotly dataframe
    
    Args:
        data: dataframe - pandas dataframe 
        index: bool - indicates if you want index to show or not
    
    Returns:
        fig: plot - formatted plotly table
    """
    # plot table
    colorscale = [[0, '#1779bd'],[.5, '#d2e8f7'],[1, '#ffffff']]
    fig = ff.create_table(data, index=index, colorscale=colorscale)

    return fig.show()


def box(data, x_col, y_col, title=None, x_title=None, y_title=None, color=None, f_col=None, f_row=None):
    """
    Function that plots a box plot
    
    Args:
        data: dataframe - pandas dataframe 
        x_col: str - column in the dataframe representing categorical values
        y_col: str - column in the dataframe representing numerical values
        title: str - text to be displyed as title for the plot
        x_title: str - text to be displayed on the x-axis
        y_title: str - text to be displayed on the y-axis
        color: str - column name to be used for multiple box plots
    
    Returns:
        fig: plot - box plot to be displayed
    """
    # plot box plot
    fig = px.box(data, x=x_col, y=y_col, color=color, color_discrete_sequence=px.colors.qualitative.D3, notched=True,
                facet_col=f_col, facet_row=f_row)

    # edit plot
    fig.update_xaxes(title_text=x_title, automargin=True)
    fig.update_yaxes(title_text=y_title, automargin=True)
    fig.update_layout(title_text=title, yaxis=dict(visible=False), autosize=False, plot_bgcolor='rgba(0,0,0,0)', 
                      title_x=0.46, uniformtext_minsize=5)
    
    return fig.show()


def violin(data, x_col, y_col, title=None, x_title=None, y_title=None, color=None, f_col=None, f_row=None):
    """
    Function that plots a violin plot
    
    Args:
        data: dataframe - pandas dataframe 
        x_col: str - column in the dataframe representing categorical values
        y_col: str - column in the dataframe representing numerical values
        title: str - text to be displyed as title for the plot
        x_title: str - text to be displayed on the x-axis
        y_title: str - text to be displayed on the y-axis
        color: str - column name to be used for multiple box plots
    
    Returns:
        fig: plot - violin plot to be displayed
    """
    # plot box plot
    fig = px.violin(data, x=x_col, y=y_col, color=color, color_discrete_sequence=px.colors.qualitative.D3, box=True,
                facet_col=f_col, facet_row=f_row)

    # edit plot
    fig.update_xaxes(title_text=x_title, automargin=True)
    fig.update_yaxes(title_text=y_title, automargin=True)
    fig.update_layout(title_text=title, yaxis=dict(visible=False), autosize=False, plot_bgcolor='rgba(0,0,0,0)', 
                      title_x=0.46, uniformtext_minsize=5)
    
    return fig.show()