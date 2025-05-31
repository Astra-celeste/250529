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

# 컴퓨터용 단어 사전 (예시)
word_dict = {
    "ㅂㅈ": ["바지", "보자기", "벌집", "배지"],
    "ㅇㅇ": ["우유", "오이", "이유", "의의", "야유"],
    "ㄱㅅ": ["감사", "급식", "간식", "가슴"],
    "ㅈㅂ": ["자바", "지방", "준비", "제비"],
    "ㅅㅈ": ["사진", "소주", "시작", "신전"],
    "ㅁㄴ": ["마늘", "묵념", "만남", "미녀"],
    "ㄷㅂ": ["도박", "당분", "덧붙", "대박"],
    "ㅊㄱ": ["차갑", "청국", "축구", "참견"],
    "ㅍㄹ": ["포르", "팔로", "파랑", "피뢰"],
    "ㅎㅅ": ["항상", "한숨", "호수", "행성"]
}
all_chosungs = list(word_dict.keys())

# 초기화
if "round" not in st.session_state:
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.current_chosung = random.choice(all_chosungs)
    st.session_state.used_words = []

# 타이틀
st.title("🟠 훈민정음 초성 게임")
st.write("사용자와 컴퓨터가 번갈아가며 초성에 맞는 단어를 말하는 게임입니다.")

st.markdown(f"### 🕹️ 라운드 {st.session_state.round}")
st.markdown(f"**초성:** `{st.session_state.current_chosung}`")

# 입력 폼
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

        # 컴퓨터 응답
        comp_candidates = [
            w for w in word_dict.get(chosung, [])
            if w not in st.session_state.used_words
        ]

        if comp_candidates:
            comp_word = random.choice(comp_candidates)
            st.info(f"🤖 컴퓨터의 단어: `{comp_word}`")
            st.session_state.used_words.append(comp_word)
        else:
            st.info("🤖 컴퓨터는 더 이상 낼 단어가 없어요!")

        # 다음 라운드로
        st.session_state.round += 1
        st.session_state.current_chosung = random.choice(all_chosungs)
        st.session_state.used_words = []

st.markdown(f"### 🔢 현재 점수: {st.session_state.score}")
