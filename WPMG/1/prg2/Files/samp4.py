import streamlit as st
from streamlit_tree_select import tree_select

nodes = [
    {
        "label": "test",
        "value": "test",
        "children": [
            {
                "label": "file.txt",
                "value": "file.txt"
            }
        ]
    }
]

result = tree_select(nodes=nodes)
st.write(result)