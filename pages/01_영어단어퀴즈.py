import streamlit as st
import random

st.set_page_config(page_title="중3 영어 단어 퀴즈", page_icon="📝")

st.title("📝 중3 영어 단어 퀴즈")
st.subheader("뜻을 보고 알맞은 영어 단어를 골라보세요!")

# 중3 수준 영어 단어 데이터
quiz_data = [
    {"word": "environment", "meaning": "환경"},
    {"word": "experiment", "meaning": "실험"},
    {"word": "volunteer", "meaning": "자원봉사자"},
    {"word": "success", "meaning": "성공"},
    {"word": "disease", "meaning": "질병"},
    {"word": "history", "meaning": "역사"},
    {"word": "temperature", "meaning": "온도"},
    {"word": "education", "meaning": "교육"},
    {"word": "invention", "meaning": "발명"},
    {"word": "celebration", "meaning": "축하"},
    {"word": "pollution", "meaning": "오염"},
    {"word": "energy", "meaning": "에너지"},
    {"word": "accident", "meaning": "사고"},
    {"word": "direction", "meaning": "방향"},
    {"word": "population", "meaning": "인구"}
]

# 퀴즈 인덱스 초기화
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = random.randint(0, len(quiz_data)-1)

# 퀴즈 출제
current = quiz_data[st.session_state.quiz_index]
correct_word = current["word"]
meaning = current["meaning"]

# 보기 구성
options = [correct_word]
while len(options) < 4:
    choice = random.choice(quiz_data)["word"]
    if choice not in options:
        options.append(choice)
random.shuffle(options)

# 문제 표시
st.markdown(f"### ❓ 단어의 뜻: `{meaning}`")
answer = st.radio("정답을 골라보세요:", options)

# 정답 확인
if st.button("✅ 정답 확인"):
    if answer == correct_word:
        st.success("🎉 정답입니다! 잘했어요!")
        st.balloons()
    else:
        st.error(f"❌ 아쉬워요! 정답은 **{correct_word}** 입니다.")

    # 다음 문제 버튼
    if st.button("🔄 다음 문제"):
        st.session_state.quiz_index = random.randint(0, len(quiz_data)-1)
        st.experimental_rerun()
