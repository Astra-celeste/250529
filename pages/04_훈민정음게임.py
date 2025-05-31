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

# 상태 초기화
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.current_chosung = random.choice(all_chosungs)
    st.session_state.used_words = []
    st.session_state.game_over = False
    st.session_state.winner = ""

# UI 타이틀
st.title("훈민정음 초성 게임")
st.markdown("2글자 한국어 단어를 들이면 전달! 예: 'ㅂㅈ' → '바지'")

col1, col2 = st.columns(2)
col1.metric("호주자", st.session_state.user_score)
col2.metric("컴퓨터", st.session_state.computer_score)

chosung = st.session_state.current_chosung
st.markdown(f"### 현재 초성: `{chosung}`")

if st.session_state.game_over:
    st.success(f"평가: **{st.session_state.winner}** 가 이겡했습니다!")
    if st.button("다음 라움드 시작"):
        st.session_state.current_chosung = random.choice(all_chosungs)
        st.session_state.used_words = []
        st.session_state.game_over = False
        st.session_state.winner = ""
    st.stop()

# 사용자 입력
with st.form("word_form", clear_on_submit=True):
    user_input = st.text_input("단어 입력 (2글자 한국어):", max_chars=10)
    submitted = st.form_submit_button("제출")

if submitted and not st.session_state.game_over:
    user_input = user_input.strip()
    user_chosung = get_chosung(user_input)

    if not re.fullmatch(r'[\uac00-\ud7a3]{2}', user_input):
        st.error("오바른 2글자 한국어를 입력해주세요.")
        st.session_state.user_score -= 50
    elif user_input in st.session_state.used_words:
        st.error("이미 사용한 단어입니다.")
        st.session_state.user_score -= 50
    elif user_chosung != chosung:
        st.error(f"초성 잘못! 입력한 초성: `{user_chosung}`")
        st.session_state.user_score -= 50
        st.session_state.computer_score += 100
        st.session_state.game_over = True
        st.session_state.winner = "컴퓨터"
    elif user_input not in dictionary:
        st.error(f"'{user_input}'는(는) 사전적으로 정의되지 않은 단어입니다.")
        st.session_state.user_score -= 50
    else:
        st.success(f"건조가 정확합니다: `{user_input}` (+100)")
        st.session_state.user_score += 100
        st.session_state.used_words.append(user_input)

        # 컴퓨터 첫줄
        comp_candidates = [
            w for w in word_dict.get(chosung, [])
            if w not in st.session_state.used_words and len(w) == 2
        ]

        if comp_candidates:
            comp_word = random.choice(comp_candidates)
            st.info(f"컴퓨터는 `{comp_word}` 을(를) 내었습니다.")
            st.session_state.used_words.append(comp_word)
        else:
            st.warning("컴퓨터는 더 이상 내 단어가 없습니다.")
            st.session_state.user_score += 100
            st.session_state.game_over = True
            st.session_state.winner = "사용자"

if st.session_state.used_words:
    st.markdown("### 사용된 단어")
    st.write(", ".join(st.session_state.used_words))

if not all_chosungs:
    st.error("유효한 단어가 포함된 dictionary.txt 파일이 필요합니다. 최소 하나 이상의 2글자 한글 단어를 추가해주세요.")
    st.stop()

dictionary = load_dictionary()
word_dict = make_word_dict(dictionary)
all_chosungs = list(word_dict.keys())

# ✅ 예외 처리
if not all_chosungs:
    st.error("유효한 단어가 포함된 dictionary.txt 파일이 필요합니다. 최소 하나 이상의 2글자 한글 단어를 추가해주세요.")
    st.stop()
