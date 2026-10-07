import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(
    page_title="DataFrame Demo",
    page_icon="📊"
)

st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")

st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames."""
)


@st.cache_data
def get_UN_data():
    url = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com/agri.csv.gz"
    df = pd.read_csv(url)
    return df.set_index("Region")


try:
    df = get_UN_data()

    countries = st.multiselect(
        "Choose countries",
        list(df.index),
        ["China", "United States of America"],
    )

    if not countries:
        st.error("Please select at least one country.")

    else:
        data = df.loc[countries].copy()

        data = data / 1000000.0

        st.write(
            "### Gross Agricultural Production ($B)",
            data.sort_index()
        )

        chart_data = data.T.reset_index()

        chart_data = chart_data.melt(
            id_vars=["index"],
            var_name="Region",
            value_name="Gross Agricultural Product ($B)"
        )

        chart_data = chart_data.rename(
            columns={"index": "Year"}
        )

        chart = (
            alt.Chart(chart_data)
            .mark_area(opacity=0.3)
            .encode(
                x=alt.X("Year:T", title="Year"),
                y=alt.Y(
                    "Gross Agricultural Product ($B):Q",
                    title="Gross Agricultural Product ($B)"
                ),
                color=alt.Color("Region:N", title="Region")
            )
        )

        st.altair_chart(chart, use_container_width=True)

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
        """
        % e.reason
    )
