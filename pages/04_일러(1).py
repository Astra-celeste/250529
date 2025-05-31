import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🐰 다채로운 토끼 그림")

# 도형을 추가하는 함수
def draw_bunny():
    fig = go.Figure()

    # 머리
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=2, y0=2, x1=6, y1=6,
                  fillcolor="lightpink", line_color="black")

    # 몸통
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=1.5, y0=-1, x1=6.5, y1=4,
                  fillcolor="lavender", line_color="black")

    # 눈 (왼쪽)
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=3.2, y0=4.2, x1=3.6, y1=4.6,
                  fillcolor="black", line_color="black")

    # 눈 (오른쪽)
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=4.4, y0=4.2, x1=4.8, y1=4.6,
                  fillcolor="black", line_color="black")

    # 귀 (왼쪽)
    fig.add_shape(type="rect",
                  xref="x", yref="y",
                  x0=2.8, y0=6, x1=3.4, y1=9,
                  fillcolor="pink", line_color="black")

    # 귀 (오른쪽)
    fig.add_shape(type="rect",
                  xref="x", yref="y",
                  x0=4.6, y0=6, x1=5.2, y1=9,
                  fillcolor="hotpink", line_color="black")

    # 코
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=3.8, y0=3.2, x1=4.2, y1=3.6,
                  fillcolor="deeppink", line_color="black")

    # 수염
    fig.add_shape(type="line", x0=3.5, y0=3.4, x1=2.5, y1=3.4,
                  line=dict(color="gray", width=2))
    fig.add_shape(type="line", x0=3.5, y0=3.2, x1=2.5, y1=3.0,
                  line=dict(color="gray", width=2))
    fig.add_shape(type="line", x0=4.5, y0=3.4, x1=5.5, y1=3.4,
                  line=dict(color="gray", width=2))
    fig.add_shape(type="line", x0=4.5, y0=3.2, x1=5.5, y1=3.0,
                  line=dict(color="gray", width=2))

    fig.update_layout(
        xaxis=dict(range=[0, 8], visible=False),
        yaxis=dict(range=[-2, 10], visible=False),
        width=600,
        height=800,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    return fig

fig = draw_bunny()
st.plotly_chart(fig, use_container_width=True)
