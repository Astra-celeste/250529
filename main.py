import streamlit as st

st.set_page_config(page_title="MBTI 여행 추천", page_icon="🌍", layout="centered")

st.title("✈️ MBTI 여행 추천 서비스")
st.subheader("당신의 성격 유형으로 딱 맞는 여행지를 추천해드릴게요! 😎")

mbti = st.selectbox(
    "당신의 MBTI는 무엇인가요?",
    [
        "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP"
    ]
)

if st.button("🧳 여행지 추천 받기!"):
    st.balloons()
    
    recommendations = {
        "INTJ": ("📚 오슬로, 노르웨이", "조용하고 지적인 분위기를 좋아하는 당신에게 북유럽 도시가 딱!"),
        "INTP": ("🧠 도쿄, 일본", "창의성과 독립심을 충전할 수 있는 도시!"),
        "ENTJ": ("🌆 뉴욕, 미국", "빠르게 움직이는 대도시에서 에너지를 얻는 타입!"),
        "ENTP": ("🌋 레이캬비크, 아이슬란드", "자연과 아이디어의 폭발 💥"),
        "INFJ": ("🌲 밴프, 캐나다", "깊은 성찰과 평화를 주는 대자연 여행지"),
        "INFP": ("🎨 피렌체, 이탈리아", "예술과 감성의 도시에서 힐링 타임"),
        "ENFJ": ("🎡 런던, 영국", "문화와 사람을 동시에 만날 수 있는 다채로운 도시"),
        "ENFP": ("🎉 바르셀로나, 스페인", "열정과 자유를 마음껏 즐기세요!"),
        "ISTJ": ("🏯 교토, 일본", "전통과 질서를 중시하는 당신에게 완벽한 선택"),
        "ISFJ": ("🏞️ 잘츠부르크, 오스트리아", "조용한 자연과 따뜻한 문화가 어우러진 장소"),
        "ESTJ": ("🏙️ 시카고, 미국", "조직적이고 실용적인 당신에게 어울리는 도시"),
        "ESFJ": ("🎭 파리, 프랑스", "사람들과의 교류와 로맨틱한 감성을 동시에!"),
        "ISTP": ("🏜️ 그랜드 캐니언, 미국", "탐험심 가득한 당신에게 최고의 모험!"),
        "ISFP": ("🌅 발리, 인도네시아", "자연과 예술을 사랑하는 당신에게 이상적인 곳"),
        "ESTP": ("🏄 시드니, 호주", "모험과 액션을 즐길 수 있는 다이나믹한 도시"),
        "ESFP": ("🎶 리우데자네이루, 브라질", "음악과 춤, 자유를 만끽하세요!")
    }

    if mbti in recommendations:
        place, desc = recommendations[mbti]
        st.success(f"당신에게 추천하는 여행지는... **{place}** 🌟")
        st.write(desc)
        st.image("https://source.unsplash.com/800x400/?" + place.split(",")[0])
