import streamlit as st
import random
import re
import os

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

# 사전 단어 불러오기
def load_dictionary():
    if not os.path.exists("dictionary.txt"):
        return []
    with open("dictionary.txt", "r", encoding="utf-8") as file:
        words = [line.strip() for line in file.readlines() if len(line.strip()) == 2]
    return words

# 초성별 사전 만들기
def make_word_dict(dictionary):
    word_dict = {}
    for word in dictionary:
        chosung = get_chosung(word)
        if chosung not in word_dict:
            word_dict[chosung] = []
        word_dict[chosung].append(word)
    return word_dict

# 단어 사전 준비
dictionary = load_dictionary()
word_dict = make_word_dict(dictionary)
all_chosungs = list(word_dict.keys())

if not all_chosungs:
    st.error("⚠️ 사전에 유효한 단어가 없습니다. dictionary.txt 파일에 2글자 한글 단어를 추가해주세요.")
    st.stop()

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

# UI 타이틀
st.title("훈민정음 초성 게임")
st.markdown("2글자 한국어 단어를 들어맞추면 점수 획득! 예: 'ㅂㅈ' → '바지'")

col1, col2 = st.columns(2)
col1.metric("사용자 점수", st.session_state.user_score)
col2.metric("컴퓨터 점수", st.session_state.computer_score)

chosung = st.session_state.current_chosung
st.markdown(f"### 현재 초성: `{chosung}`")

if st.session_state.game_over:
    st.success(f"게임 종료: **{st.session_state.winner}** 승리!")
    if st.button("다음 라운드 시작"):
        st.session_state.current_chosung = random.choice(all_chosungs)
        st.session_state.used_words = []
        st.session_state.game_over = False
        st.session_state.winner = ""
    st.stop()

# 사용자 입력 처리
user_input = st.text_input("단어 입력 (Enter로 제출)", max_chars=10)

if user_input:
    user_input = user_input.strip()
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
    elif user_input not in dictionary:
        st.error(f"❌ '{user_input}'는 사전에 없는 단어입니다.")
        st.session_state.user_score -= 50
    else:
        st.success(f"✅ 정답: `{user_input}` (+100점)")
        st.session_state.user_score += 100
        st.session_state.used_words.append(user_input)

        # 컴퓨터 응답
        comp_candidates = [
            w for w in word_dict.get(chosung, [])
            if w not in st.session_state.used_words and len(w) == 2
        ]

        if comp_candidates:
            comp_word = random.choice(comp_candidates)
            st.info(f"💻 컴퓨터 단어: `{comp_word}`")
            st.session_state.used_words.append(comp_word)
        else:
            st.warning("💻 컴퓨터가 더 이상 단어를 내지 못합니다.")
            st.session_state.user_score += 100
            st.session_state.game_over = True
            st.session_state.winner = "사용자"

if st.session_state.used_words:
    st.markdown("### 사용된 단어 목록")
    st.write(", ".join(st.session_state.used_words))
