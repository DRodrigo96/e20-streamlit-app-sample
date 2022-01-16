

# streamlit_app.py
# ==================================================
# requirements
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
# common
import os
import time
# user defined
from utils.utils import get_dependencies
from utils.utils import get_properties
from utils.utils import get_options
# --------------------------------------------------

# => data
db_dep = pd.read_csv('./data/db_dependencies.csv', delimiter=';')
db_prop = pd.read_csv('./data/db_properties.csv', delimiter=';')

# => streamlit components
# -> header title
st.title('Table dependencies network')

# -> selection options
table_list = db_prop['table_name'].tolist()
table_list.sort()

# -> multiselect dropdown menu for selections
selected_tables = st.multiselect('Tablas a visualizar', table_list)

# -> set info message on initial site load
if len(selected_tables) == 0:
    st.text('Escoger al menos una tabla...')
# -> network graph when user selects at least 1 item
else:
    df_select = db_dep.loc[db_dep['source'].isin(selected_tables) | db_dep['target'].isin(selected_tables)]
    df_select = df_select.reset_index(drop=True)
    nb_select = set(df_select['source'].unique()).union(set(df_select['target'].unique()))
    df_prop_select = db_prop.loc[db_prop['table_name'].isin(nb_select)]

    # > initiate pyvis network object
    db_net = Network(
        height='750px', 
        width="100%", 
        bgcolor='#F0F0F0', 
        font_color='#000000'
    )

    # > network series
    sources = df_select['source']
    targets = df_select['target']

    # > network dependencies mapper
    edge_data = zip(sources, targets)
    for e in edge_data:
        src = e[0]
        trg = e[1]
        db_net.add_node(src, src, title=src)
        db_net.add_node(trg, trg, title=trg)
        db_net.add_edge(source=src, to=trg)
    neighbor_map = db_net.get_adj_list()

    # > node properties
    for node in db_net.nodes:
        table_name = node['title']
        table_dependencies = get_dependencies(db_dep, table_name)
        table_properties = get_properties(df_prop_select, table_name)
        
        # >> tooltips
        prop_str = (
            f"""
            - Table name: {table_name}
            <br>
            - Dependencies:
            <br>
            {table_dependencies}
            <br>
            - Propiedades:
            <br>
            Rows: {table_properties['nro_rows']}
            <br>
            Columns: {table_properties['nro_cols']}
            <br>
            Schema: {table_properties['schema']}
            """
        )

        # >> network labels
        node['title'] = prop_str
        node['value'] = len(neighbor_map[node['id']])

    # > added graph properties
    var_options = get_options()
    db_net.set_options(var_options)

    # > save and read graph as HTML file (on Streamlit Sharing)
    path = './public/resources'
    db_net.save_graph(f'{path}/pyvis-graph.html')
    HtmlFile = open(f'{path}/pyvis-graph.html', 'r', encoding='utf-8')

    # > HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=750)