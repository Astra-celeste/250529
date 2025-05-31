import streamlit as st
import random

st.set_page_config(page_title="고1 영어 단어 퀴즈", page_icon="📚")

st.title("📚 고1 영어 단어 퀴즈")
st.subheader("뜻을 보고 알맞은 영어 단어를 골라보세요!")

# 고1 수준 영어 단어 데이터
quiz_data = [
    {"word": "analyze", "meaning": "분석하다"},
    {"word": "culture", "meaning": "문화"},
    {"word": "confident", "meaning": "자신감 있는"},
    {"word": "effort", "meaning": "노력"},
    {"word": "explain", "meaning": "설명하다"},
    {"word": "solution", "meaning": "해결책"},
    {"word": "variety", "meaning": "다양성"},
    {"word": "opinion", "meaning": "의견"},
    {"word": "curious", "meaning": "호기심 많은"},
    {"word": "develop", "meaning": "발전시키다"},
    {"word": "behavior", "meaning": "행동"},
    {"word": "opportunity", "meaning": "기회"},
    {"word": "responsibility", "meaning": "책임"},
    {"word": "technology", "meaning": "기술"},
    {"word": "environment", "meaning": "환경"}
]

# 새로운 문제 불러오기
def get_new_quiz():
    question = random.choice(quiz_data)
    correct_word = question["word"]
    meaning = question["meaning"]
    
    options = [correct_word]
    while len(options) < 4:
        choice = random.choice(quiz_data)["word"]
        if choice not in options:
            options.append(choice)
    random.shuffle(options)
    
    return meaning, correct_word, options

# 세션 상태 초기화
if "answered" not in st.session_state:
    st.session_state.answered = False
if "current_meaning" not in st.session_state:
    meaning, correct_word, options = get_new_quiz()
    st.session_state.current_meaning = meaning
    st.session_state.correct_word = correct_word
    st.session_state.options = options

# 문제 표시
st.markdown(f"### ❓ 단어의 뜻: `{st.session_state.current_meaning}`")
answer = st.radio("정답을 골라보세요:", st.session_state.options)

# 정답 확인 버튼
if st.button("✅ 정답 확인") and not st.session_state.answered:
    st.session_state.answered = True
    if answer == st.session_state.correct_word:
        st.success("🎉 정답입니다! 잘했어요!")
        st.balloons()
    else:
        st.error(f"❌ 오답입니다. 정답은 **{st.session_state.correct_word}** 입니다.")

# 다음 문제 버튼
if st.session_state.answered and st.button("🔄 다음 문제"):
    st.session_state.answered = False
    meaning, correct_word, options = get_new_quiz()
    st.session_state.current_meaning = meaning
    st.session_state.correct_word = correct_word
    st.session_state.options = options
    st.experimental_rerun()
