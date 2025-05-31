import streamlit as st
import random

st.set_page_config(page_title="고급 영어 단어 퀴즈", page_icon="📖")

st.title("📖 고급 영어 단어 퀴즈")
st.subheader("뜻을 보고 알맞은 영어 단어를 골라보세요!")

# 고2~고3 수준 영어 단어 데이터
quiz_data = [
    {"word": "allocate", "meaning": "할당하다"},
    {"word": "comprehensive", "meaning": "포괄적인"},
    {"word": "consequence", "meaning": "결과"},
    {"word": "contradict", "meaning": "모순되다"},
    {"word": "credible", "meaning": "믿을 수 있는"},
    {"word": "deficiency", "meaning": "결핍"},
    {"word": "emphasize", "meaning": "강조하다"},
    {"word": "hypothesis", "meaning": "가설"},
    {"word": "interpret", "meaning": "해석하다"},
    {"word": "negotiate", "meaning": "협상하다"},
    {"word": "plausible", "meaning": "그럴듯한"},
    {"word": "substantial", "meaning": "상당한"},
    {"word": "sustainable", "meaning": "지속 가능한"},
    {"word": "terminate", "meaning": "종결시키다"},
    {"word": "utilize", "meaning": "활용하다"}
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

# 에러 방지용 try-except로 감싸기
try:
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
            st.success("🎉 정답입니다! 단어 실력이 대단하네요!")
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

except Exception as e:
    st.warning("⚠️ 문제가 발생했지만 앱은 계속 작동 중입니다.")
    # 개발 중에는 아래 주석을 풀면 콘솔에 에러 내용 확인 가능
    # st.text(f"디버그용 에러 내용: {e}")
