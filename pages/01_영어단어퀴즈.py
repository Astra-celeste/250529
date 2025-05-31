import streamlit as st
import random

st.set_page_config(page_title="고급 영어 단어 퀴즈", page_icon="🏆")
st.title("🏆 고급 영어 단어 퀴즈")
st.subheader("뜻을 보고 알맞은 영어 단어를 골라보세요!")

# 사용자 이름 받기
if "user_name" not in st.session_state:
    user_name = st.text_input("🙋‍♂️ 이름을 입력해주세요:")
    if user_name:
        st.session_state.user_name = user_name
        st.session_state.correct_count = 0
        st.session_state.wrong_count = 0
        st.session_state.answered = False
        st.session_state.leaderboard = {}
        st.experimental_rerun()
    else:
        st.stop()

st.markdown(f"### 👋 안녕하세요, **{st.session_state.user_name}** 님!")

# 고급 단어 리스트 (고2~수능 수준, 약 60개)
quiz_data = [
    {"word": "allocate", "meaning": "할당하다"},
    {"word": "ambiguous", "meaning": "모호한"},
    {"word": "artificial", "meaning": "인공적인"},
    {"word": "contradict", "meaning": "모순되다"},
    {"word": "contemplate", "meaning": "심사숙고하다"},
    {"word": "conventional", "meaning": "전통적인"},
    {"word": "correspond", "meaning": "일치하다"},
    {"word": "deficiency", "meaning": "결핍"},
    {"word": "deteriorate", "meaning": "악화되다"},
    {"word": "diversify", "meaning": "다양화하다"},
    {"word": "elaborate", "meaning": "정교한"},
    {"word": "enormous", "meaning": "거대한"},
    {"word": "entitle", "meaning": "자격을 주다"},
    {"word": "exaggerate", "meaning": "과장하다"},
    {"word": "formulate", "meaning": "공식화하다"},
    {"word": "hypothesis", "meaning": "가설"},
    {"word": "implication", "meaning": "함축, 암시"},
    {"word": "indispensable", "meaning": "없어서는 안 되는"},
    {"word": "infer", "meaning": "추론하다"},
    {"word": "integrate", "meaning": "통합하다"},
    {"word": "interpret", "meaning": "해석하다"},
    {"word": "legitimate", "meaning": "합법적인"},
    {"word": "notorious", "meaning": "악명 높은"},
    {"word": "plausible", "meaning": "그럴듯한"},
    {"word": "prohibit", "meaning": "금지하다"},
    {"word": "reluctant", "meaning": "꺼리는"},
    {"word": "resemble", "meaning": "닮다"},
    {"word": "simultaneous", "meaning": "동시의"},
    {"word": "sophisticated", "meaning": "세련된, 정교한"},
    {"word": "subsequent", "meaning": "그 이후의"},
    {"word": "substitute", "meaning": "대체하다"},
    {"word": "sufficient", "meaning": "충분한"},
    {"word": "suppress", "meaning": "억압하다"},
    {"word": "sustain", "meaning": "지속하다"},
    {"word": "terminate", "meaning": "종결시키다"},
    {"word": "transmit", "meaning": "전송하다"},
    {"word": "undergo", "meaning": "겪다"},
    {"word": "utilize", "meaning": "활용하다"},
    {"word": "validate", "meaning": "입증하다"},
    {"word": "violate", "meaning": "위반하다"},
    {"word": "allocate", "meaning": "할당하다"},
    {"word": "dedicate", "meaning": "헌신하다"},
    {"word": "justify", "meaning": "정당화하다"},
    {"word": "manipulate", "meaning": "조종하다"},
    {"word": "modify", "meaning": "수정하다"},
    {"word": "retain", "meaning": "유지하다"},
    {"word": "retrieve", "meaning": "되찾다"},
    {"word": "revise", "meaning": "수정하다"},
    {"word": "speculate", "meaning": "추측하다"},
    {"word": "strive", "meaning": "노력하다"},
    {"word": "tremendous", "meaning": "엄청난"},
    {"word": "verify", "meaning": "검증하다"},
]

# 문제 생성
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

try:
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
            st.success("🎉 정답입니다!")
            st.session_state.correct_count += 1
            st.balloons()
        else:
            st.error(f"❌ 오답입니다. 정답은 **{st.session_state.correct_word}** 입니다.")
            st.session_state.wrong_count += 1

    if st.session_state.answered and st.button("🔄 다음 문제"):
        st.session_state.answered = False
        meaning, correct_word, options = get_new_quiz()
        st.session_state.current_meaning = meaning
        st.session_state.correct_word = correct_word
        st.session_state.options = options
        st.experimental_rerun()

    st.info(f"✅ 맞힌 문제 수: {st.session_state.correct_count}  \n❌ 틀린 문제 수: {st.session_state.wrong_count}")

    if "leaderboard" not in st.session_state:
        st.session_state.leaderboard = {}

    st.session_state.leaderboard[st.session_state.user_name] = {
        "correct": st.session_state.correct_count,
        "wrong": st.session_state.wrong_count,
        "score": st.session_state.correct_count - st.session_state.wrong_count
    }

    st.markdown("### 🏅 실시간 사용자 랭킹")
    sorted_users = sorted(
        st.session_state.leaderboard.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    for i, (name, data) in enumerate(sorted_users, 1):
        st.write(
            f"{i}위 🧑‍🎓 **{name}**: "
            f"✅ {data['correct']} / ❌ {data['wrong']} "
            f"(점수: {data['score']})"
        )

except Exception:
    st.warning("⚠️ 오류가 발생했지만 앱은 계속 작동 중입니다.")
