import streamlit as st
import random
import re
import time
from PyKorean import korean

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

# 사전 단어 불러오기 (공식 사전 기반 체크)
def is_valid_korean_word(word):
    return korean.check_word(word)

# 모든 가능한 2글자 초성 조합 생성 (임의 단어를 위한)
def generate_all_chosungs():
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ',
                    'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ',
                    'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    return [c1 + c2 for c1 in CHOSUNG_LIST for c2 in CHOSUNG_LIST]

all_chosungs = generate_all_chosungs()

# 상태 초기화
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "used_words" not in st.session_state:
    st.session_state.used_words = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner" not in st.session_state:
    st.session_state.winner = ""
if "current_chosung" not in st.session_state:
    st.session_state.current_chosung = random.choice(all_chosungs)
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# UI 타이틀
st.title("훈민정음 초성 게임 (공식 사전 기반)")
st.markdown("2글자 한국어 단어를 맞히면 점수 획득! 예: 'ㅂㅈ' → '바지'.\n10초 안에 제출하지 못하면 패배합니다.")

col1, col2 = st.columns(2)
col1.metric("사용자 점수", st.session_state.user_score)
col2.metric("컴퓨터 점수", st.session_state.computer_score)

chosung = st.session_state.current_chosung
st.markdown(f"### 현재 초성: `{chosung}`")

# 타이머 표시
elapsed = time.time() - st.session_state.start_time
remaining = max(0, 10 - int(elapsed))
st.markdown(f"### 남은 시간: {remaining}초")

if remaining <= 0 and not st.session_state.game_over:
    st.warning("⏰ 시간 초과! 아무도 답을 제출하지 못했습니다.")
    st.session_state.computer_score += 100
    st.session_state.winner = "컴퓨터"
    st.session_state.game_over = True

if st.session_state.game_over:
    st.success(f"게임 종료: **{st.session_state.winner}** 승리!")
    if st.button("다음 라운드 시작"):
        st.session_state.current_chosung = random.choice(all_chosungs)
        st.session_state.used_words = []
        st.session_state.game_over = False
        st.session_state.winner = ""
        st.session_state.user_input = ""
        st.session_state.start_time = time.time()
    st.stop()

# 사용자 입력 처리
st.session_state.user_input = st.text_input("단어 입력 (Enter로 제출)", value=st.session_state.user_input, max_chars=10)

if st.session_state.user_input and not st.session_state.game_over:
    user_input = st.session_state.user_input.strip()
    user_chosung = get_chosung(user_input)

    if not re.fullmatch(r'[\uac00-\ud7a3]{2}', user_input):
        st.error("❌ 정확한 2글자 한글 단어를 입력해주세요.")
        st.session_state.user_score -= 50
    elif user_input in st.session_state.used_words:
        st.error("❌ 이미 사용된 단어입니다.")
        st.session_state.user_score -= 50
    elif user_chosung != chosung:
        st.error(f"❌ 초성이 맞지 않습니다. 입력된 초성: `{user_chosung}`")
        st.session_state.user_score -= 50
        st.session_state.computer_score += 100
        st.session_state.game_over = True
        st.session_state.winner = "컴퓨터"
    elif not is_valid_korean_word(user_input):
        st.error(f"❌ '{user_input}'는 사전에 없는 단어입니다.")
        st.session_state.user_score -= 50
    else:
        st.success(f"✅ 정답: `{user_input}` (+100점)")
        st.session_state.user_score += 100
        st.session_state.used_words.append(user_input)

        # 컴퓨터 응답 (랜덤 2글자 단어 생성)
        from random_word import RandomWords
        rw = RandomWords()
        attempts = 0
        while attempts < 20:
            try:
                comp_word = rw.get_random_word()
                if comp_word and len(comp_word) == 2 and get_chosung(comp_word) == chosung and comp_word not in st.session_state.used_words and is_valid_korean_word(comp_word):
                    st.info(f"💻 컴퓨터 단어: `{comp_word}`")
                    st.session_state.used_words.append(comp_word)
                    break
            except:
                pass
            attempts += 1
        else:
            st.warning("💻 컴퓨터가 더 이상 단어를 내지 못합니다.")
            st.session_state.user_score += 100
            st.session_state.winner = "사용자"

        st.session_state.game_over = True

    # 입력 초기화
    st.session_state.user_input = ""

if st.session_state.used_words:
    st.markdown("### 사용된 단어 목록")
    st.write(", ".join(st.session_state.used_words))

# 실시간 새로고침 유지 조건에 따라 rerun
if "start_time" in st.session_state and not st.session_state.game_over and remaining > 0:
    time.sleep(1)
    st.experimental_rerun()
