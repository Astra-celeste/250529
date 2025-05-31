import streamlit as st
import random
import re
import time

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

# 단어 사전
word_dict = {
    "ㅂㅈ": ["바지", "보자", "벌집"],
    "ㅇㅇ": ["우유", "오이", "이유", "의의", "야유"],
    "ㄱㅅ": ["감사", "급식", "간식", "가슴"],
    "ㅈㅂ": ["자바", "지방", "제비"],
    "ㅅㅈ": ["사진", "소주", "시작"],
    "ㅁㄴ": ["마늘", "묵념", "미녀"],
    "ㄷㅂ": ["도박", "당분", "대박"],
    "ㅊㄱ": ["차갑", "청국", "축구"],
    "ㅍㄹ": ["포르", "팔로", "파랑"],
    "ㅎㅅ": ["항상", "한숨", "호수"]
}
all_chosungs = list(word_dict.keys())

# 상태 초기화
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.current_chosung = random.choice(all_chosungs)
    st.session_state.used_words = []
    st.session_state.game_over = False
    st.session_state.winner = ""
    st.session_state.start_time = time.time()

# 타이틀
st.title("🎯 훈민정음 초성 게임")
st.markdown("한글 초성에 맞는 두 글자 단어를 말하세요! 맞으면 +100, 틀리면 -50!")

# 점수판
col1, col2 = st.columns(2)
col1.metric("😊 사용자 점수", st.session_state.user_score)
col2.metric("🤖 컴퓨터 점수", st.session_state.computer_score)

# 현재 초성
chosung = st.session_state.current_chosung
st.markdown(f"### 🧩 현재 초성: `{chosung}`")

# 타이머
elapsed = time.time() - st.session_state.start_time
remaining = max(0, 10 - int(elapsed))
st.markdown(f"⏱️ 남은 시간: `{remaining}초`")

# 시간 초과 확인
if remaining <= 0 and not st.session_state.game_over:
    st.error("⏰ 시간 초과! 컴퓨터 승리입니다.")
    st.session_state.computer_score += 100
    st.session_state.game_over = True
    st.session_state.winner = "🤖 컴퓨터"
    st.stop()

# 라운드 종료
if st.session_state.game_over:
    st.success(f"🏁 이번 라운드 승자는 **{st.session_state.winner}**입니다!")
    if st.button("🔁 다음 초성으로 시작"):
        st.session_state.current_chosung = random.choice(all_chosungs)
        st.session_state.used_words = []
        st.session_state.game_over = False
        st.session_state.winner = ""
        st.session_state.start_time = time.time()
        st.experimental_rerun()
    st.stop()

# 사용자 입력
with st.form("word_form", clear_on_submit=True):
    user_input = st.text_input("단어 입력 (한글 두 글자):", max_chars=2)
    submitted = st.form_submit_button("제출")

if submitted and not st.session_state.game_over:
    user_input = user_input.strip()
    user_chosung = get_chosung(user_input)

    if not re.fullmatch(r'[가-힣]{2}', user_input):
        st.error("⚠️ 한글 두 글자만 입력해주세요.")
        st.session_state.user_score -= 50
    elif user_input in st.session_state.used_words:
        st.error("⚠️ 이미 사용된 단어입니다!")
        st.session_state.user_score -= 50
    elif user_chosung != chosung:
        st.error(f"❌ 초성이 일치하지 않아요! 입력한 초성: `{user_chosung}`")
        st.session_state.user_score -= 50
        st.session_state.computer_score += 100
        st.session_state.game_over = True
        st.session_state.winner = "🤖 컴퓨터"
    else:
        st.success(f"✅ '{user_input}' 정답입니다! +100점")
        st.session_state.user_score += 100
        st.session_state.used_words.append(user_input)

        # 컴퓨터 차례
        comp_candidates = [
            w for w in word_dict.get(chosung, [])
            if w not in st.session_state.used_words and len(w) == 2
        ]

        if comp_candidates:
            comp_word = random.choice(comp_candidates)
            st.info(f"🤖 컴퓨터의 단어: `{comp_word}`")
            st.session_state.used_words.append(comp_word)
        else:
            st.warning("🤖 컴퓨터는 더 이상 낼 단어가 없어요!")
            st.session_state.user_score += 100
            st.session_state.game_over = True
            st.session_state.winner = "😊 사용자"

# 사용된 단어 목록
if st.session_state.used_words:
    st.markdown("### 📚 사용된 단어 목록")
    st.write(", ".join(st.session_state.used_words))

# 자동 새로고침 (1초마다)
st.experimental_rerun()
