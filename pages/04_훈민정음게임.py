import streamlit as st
import random
import re

# 초성 추출 함수
def get_chosung(word):
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ',
                    'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ',
                    'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    def is_korean_char(char):
        return '가' <= char <= '힣'

    chosung = ''
    for char in word:
        if is_korean_char(char):
            code = ord(char) - ord('가')
            chosung += CHOSUNG_LIST[code // 588]
    return chosung

# 랜덤 초성 리스트
all_chosungs = ["ㅂㅈ", "ㅇㅇ", "ㄱㅅ", "ㅈㅂ", "ㅅㅈ", "ㅁㄴ", "ㄷㅂ", "ㅊㄱ", "ㅍㄹ", "ㅎㅅ"]

# 초기 상태 설정
if "round" not in st.session_state:
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.current_chosung = random.choice(all_chosungs)
    st.session_state.used_words = []

# 제목 및 설명
st.title("🟠 훈민정음 초성 게임")
st.write("사용자와 컴퓨터가 번갈아가며 초성에 맞는 단어를 말하는 게임입니다.")

st.markdown(f"### 🕹️ 라운드 {st.session_state.round}")
st.markdown(f"**초성:** `{st.session_state.current_chosung}`")

# 🔽 폼을 사용해 Enter 키 제출 가능하게 함
with st.form("word_form", clear_on_submit=True):
    user_input = st.text_input("당신의 단어 입력:")
    submitted = st.form_submit_button("제출")

if submitted:
    user_input = user_input.strip()
    chosung = st.session_state.current_chosung
    user_chosung = get_chosung(user_input)

    if not re.fullmatch(r'[가-힣]+', user_input):
        st.error("⚠️ 한글 단어만 입력해주세요.")
    elif user_input in st.session_state.used_words:
        st.error("⚠️ 이미 사용된 단어입니다!")
    elif user_chosung != chosung:
        st.error(f"❌ 초성이 일치하지 않아요! 입력한 초성: `{user_chosung}`")
    else:
        st.success(f"✅ '{user_input}' 정답입니다!")
        st.session_state.score += 1
        st.session_state.used_words.append(user_input)

        # 컴퓨터 차례 (가상의 단어 생성)
        fake_word = f"{chosung}단어{random.randint(1, 999)}"
        st.info(f"🤖 컴퓨터의 단어: `{fake_word}`")
        st.session_state.used_words.append(fake_word)

        # 다음 라운드로 진행
        st.session_state.round += 1
        st.session_state.current_chosung = random.choice(all_chosungs)

# 점수 출력
st.markdown(f"### 🔢 현재 점수: {st.session_state.score}")
