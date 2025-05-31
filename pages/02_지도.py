import streamlit as st
import folium
from streamlit.components.v1 import html
import os

# 여행지 데이터
travel_spots = [
    {"name": "서울", "lat": 37.5665, "lon": 126.9780, "desc": "역사와 현대가 공존하는 대한민국의 수도"},
    {"name": "제주도", "lat": 33.4996, "lon": 126.5312, "desc": "자연 경관과 독특한 문화가 어우러진 섬"},
    {"name": "부산", "lat": 35.1796, "lon": 129.0756, "desc": "해변과 도시의 매력을 동시에 느낄 수 있는 항구도시"},
    {"name": "경주", "lat": 35.8562, "lon": 129.2247, "desc": "천년고도 신라의 숨결이 살아있는 역사도시"},
    {"name": "강릉", "lat": 37.7519, "lon": 128.8761, "desc": "동해안의 아름다운 바다와 커피 거리로 유명한 도시"},
    {"name": "속초", "lat": 38.2048, "lon": 128.5912, "desc": "설악산과 바다, 수산시장으로 유명한 도시"},
    {"name": "전주", "lat": 35.8242, "lon": 127.1480, "desc": "한옥마을과 전통음식의 본고장"},
    {"name": "여수", "lat": 34.7604, "lon": 127.6622, "desc": "밤바다와 낭만이 넘치는 남해안 도시"},
    {"name": "인천", "lat": 37.4563, "lon": 126.7052, "desc": "국제공항과 차이나타운, 송도국제도시로 유명"},
    {"name": "남해", "lat": 34.8372, "lon": 127.8926, "desc": "섬과 해안도로, 힐링 여행지로 주목받는 곳"}
]

# Streamlit 페이지 설정
st.set_page_config(page_title="TOP 10 한국 여행지", layout="wide")

st.title("🇰🇷 한국인이 사랑하는 TOP 10 여행지")
st.markdown("아래 지도에서 여행지를 클릭하면 간단한 설명을 확인할 수 있습니다.")

# 사이드바 선택
selected_spot = st.sidebar.selectbox("여행지 선택", ["전체 보기"] + [spot["name"] for spot in travel_spots])

# 중심 좌표 계산
center_lat = sum(spot["lat"] for spot in travel_spots) / len(travel_spots)
center_lon = sum(spot["lon"] for spot in travel_spots) / len(travel_spots)

# 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

for spot in travel_spots:
    if selected_spot == "전체 보기" or spot["name"] == selected_spot:
        folium.Marker(
            [spot["lat"], spot["lon"]],
            popup=f"<b>{spot['name']}</b><br>{spot['desc']}",
            tooltip=spot["name"],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

# HTML 파일로 저장 후 읽기
map_file = "map.html"
m.save(map_file)

with open(map_file, "r", encoding="utf-8") as f:
    map_html = f.read()

html(map_html, height=600)

# 설명 출력
if selected_spot != "전체 보기":
    spot_info = next(item for item in travel_spots if item["name"] == selected_spot)
    st.subheader(f"📍 {spot_info['name']}")
    st.write(spot_info["desc"])

# 파일 삭제는 선택사항
os.remove(map_file)
