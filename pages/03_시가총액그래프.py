import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Top 10 시가총액 기업의 변화", layout="wide")
st.title("전 세계 시가총액 TOP 10 기업의 지난 3년간 변화")

# 시가총액 기준 상위 10개 기업 (2025년 기준 가정)
companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",  # 사우디 증권거래소
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta (Facebook)": "META",
    "TSMC": "TSM",
    "Tesla": "TSLA"
}

start_date = datetime.today() - timedelta(days=3*365)
end_date = datetime.today()

@st.cache_data
def get_market_caps(ticker):
    data = yf.Ticker(ticker).history(start=start_date, end=end_date)
    info = yf.Ticker(ticker).info
    shares = info.get('sharesOutstanding', 0)
    data["Market Cap"] = data["Close"] * shares
    return data[["Market Cap"]]

fig = go.Figure()
for name, symbol in companies.items():
    try:
        cap_data = get_market_caps(symbol)
        fig.add_trace(go.Scatter(x=cap_data.index, y=cap_data["Market Cap"] / 1e12,
                                 mode='lines', name=name))
    except Exception as e:
        st.warning(f"{name} ({symbol}) 데이터를 불러오는 중 오류 발생: {e}")

fig.update_layout(
    title="전 세계 TOP 10 시가총액 기업의 시가총액 변화 (단위: 조 USD)",
    xaxis_title="날짜",
    yaxis_title="시가총액 (조 USD)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
