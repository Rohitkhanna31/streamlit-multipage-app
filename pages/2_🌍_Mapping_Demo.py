import streamlit as st
import pandas as pd
import pydeck as pdk

from urllib.error import URLError

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")
st.write(
    """This demo shows how to use `st.pydeck_chart` to display geospatial data."""
)

@st.cache_data
def from_data_file(filename):
    url = (
        "https://raw.githubusercontent.com/streamlit/"
        "demo-uber-nyc-pickups/main/data/"
        + filename
    )
    return pd.read_json(url)


try:
    ALL_LAYERS = {
        "Pickups": pdk.Layer(
            "HexagonLayer",
            data=from_data_file("uber-raw-data-sep14.json.gz"),
            get_position=["lon", "lat"],
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
        "Dropoffs": pdk.Layer(
            "HexagonLayer",
            data=from_data_file("uber-raw-data-sep14.json.gz"),
            get_position=["lon", "lat"],
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    }

    st.sidebar.markdown("### Map Layers")
    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)
    ]

    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style=None,
                initial_view_state={
                    "latitude": 40.7,
                    "longitude": -74,
                    "zoom": 11,
                    "pitch": 50,
                },
                layers=selected_layers,
            )
        )
    else:
        st.error("Please choose at least one layer above.")

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
        """
        % e.reason
    )
