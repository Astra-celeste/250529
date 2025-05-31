import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🐰 예쁘고 귀여운 토끼")

# 예쁜 토끼 이미지 URL
bunny_url = "https://upload.wikimedia.org/wikipedia/commons/6/6e/Grey_rabbit.jpg"

fig = go.Figure()

# 토끼 이미지 삽입
fig.add_layout_image(
    dict(
        source=bunny_url,
        x=0, y=1,
        sizex=1, sizey=1,
        xref="paper", yref="paper",
        xanchor="left", yanchor="top",
        sizing="stretch",
        opacity=1,
        layer="below"
    )
)

fig.update_layout(
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    margin=dict(l=0, r=0, t=0, b=0),
    width=800,
    height=600
)

st.plotly_chart(fig, use_container_width=True)
