import streamlit as st
import random

st.set_page_config(page_title="고급 영어 단어 퀴즈", page_icon="🧠")
st.title("🧠 고급 영어 단어 퀴즈")
st.subheader("뜻을 보고 알맞은 영어 단어를 골라보세요!")

# 다양한 고급 영어 단어 목록
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
    {"word": "utilize", "meaning": "활용하다"},
    {"word": "implement", "meaning": "실행하다"},
    {"word": "suppress", "meaning": "억압하다"},
    {"word": "retain", "meaning": "유지하다"},
    {"word": "evaluate", "meaning": "평가하다"},
    {"word": "distinguish", "meaning": "구별하다"},
    {"word": "illustrate", "meaning": "설명하다"},
    {"word": "influence", "meaning": "영향을 미치다"},
    {"word": "prioritize", "meaning": "우선순위를 정하다"},
    {"word": "reinforce", "meaning": "강화하다"},
    {"word": "acquire", "meaning": "획득하다"},
    {"word": "anticipate", "meaning": "예상하다"},
    {"word": "enhance", "meaning": "향상시키다"},
    {"word": "adapt", "meaning": "적응하다"},
    {"word": "indicate", "meaning": "나타내다"},
    {"word": "acknowledge", "meaning": "인정하다"},
    {"word": "justify", "meaning": "정당화하다"},
    {"word": "perceive", "meaning": "인지하다"},
    {"word": "dedicate", "meaning": "헌신하다"},
    {"word": "devote", "meaning": "바치다"},
    {"word": "resolve", "meaning": "해결하다"},
    {"word": "distribute", "meaning": "분배하다"},
    {"word": "generate", "meaning": "생성하다"},
    {"word": "initiate", "meaning": "시작하다"},
    {"word": "inspire", "meaning": "영감을 주다"},
    {"word": "persuade", "meaning": "설득하다"},
    {"word": "regulate", "meaning": "규제하다"},
    {"word": "speculate", "meaning": "추측하다"},
    {"word": "strive", "meaning": "노력하다"},
    {"word": "undergo", "meaning": "겪다"},
    {"word": "validate", "meaning": "입증하다"},
    {"word": "violate", "meaning": "위반하다"},
    {"word": "withdraw", "meaning": "철회하다"},
    {"word": "accommodate", "meaning": "수용하다"},
    {"word": "accelerate", "meaning": "가속하다"},
    {"word": "collaborate", "meaning": "협력하다"},
]

# 문제 생성 함수
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

# 앱 본문 실행 (에러 숨김 처리)
try:
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "current_meaning" not in st.session_state:
        meaning, correct_word, options = get_new_quiz()
        st.session_state.current_meaning = meaning
        st.session_state.correct_word = correct_word
        st.session_state.options = options

    st.markdown(f"### ❓ 단어의 뜻: `{st.session_state.current_meaning}`")
    answer = st.radio("정답을 골라보세요:", st.session_state.options)

    if st.button("✅ 정답 확인") and not st.session_state.answered:
        st.session_state.answered = True
        if answer == st.session_state.correct_word:
            st.success("🎉 정답입니다! 단어 실력이 대단해요!")
            st.balloons()
        else:
            st.error(f"❌ 오답입니다. 정답은 **{st.session_state.correct_word}** 입니다.")

    if st.session_state.answered and st.button("🔄 다음 문제"):
        st.session_state.answered = False
        meaning, correct_word, options = get_new_quiz()
        st.session_state.current_meaning = meaning
        st.session_state.correct_word = correct_word
        st.session_state.options = options
        st.experimental_rerun()

except Exception:
    st.warning("⚠️ 오류가 발생했지만 앱은 계속 작동 중입니다.")
