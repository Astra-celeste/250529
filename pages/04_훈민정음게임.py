import streamlit as st
import random
import time

# 예시 단어 사전 (더 확장 가능)
word_dict = {
    "ㅂㅈ": ["바지", "보자기", "벌집", "배지"],
    "ㅇㅇ": ["우유", "오이", "이유", "의의", "야유"],
    "ㄱㅅ": ["감사", "급식", "경사", "간식"],
    "ㅈㅂ": ["자바", "조별", "지방", "전방"],
    "ㅅㅈ": ["사진", "소주", "시작", "신전"]
}

all_chosungs = list(word_dict.keys())

# Streamlit UI
st.title("🟠 훈민정음 초성 게임")
st.write("사용자와 컴퓨터가 번갈아 가며 초성에 맞는 단어를 말하는 게임입니다.")

if "round" not in st.session_state:
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.current_chosung = random.choice(all_chosungs)
    st.session_state.used_words = []

st.markdown(f"### 🕹️ 라운드 {st.session_state.round}")
st.markdown(f"**초성:** `{st.session_state.current_chosung}`")

user_input = st.text_input("당신의 단어 입력:", "")

if st.button("제출"):
    chosung = st.session_state.current_chosung
    valid_words = word_dict.get(chosung, [])

    if user_input in st.session_state.used_words:
        st.error("⚠️ 이미 사용된 단어입니다!")
    elif user_input in valid_words:
        st.success(f"✅ '{user_input}' 정답입니다!")
        st.session_state.score += 1
        st.session_state.used_words.append(user_input)

        # 컴퓨터 차례
        remaining = [w for w in valid_words if w not in st.session_state.used_words]
        if remaining:
            comp_choice = random.choice(remaining)
            st.info(f"🤖 컴퓨터의 단어: `{comp_choice}`")
            st.session_state.used_words.append(comp_choice)
            st.session_state.round += 1
            st.session_state.current_chosung = random.choice(all_chosungs)
        else:
            st.success("🎉 모든 단어를 맞혔어요! 다음 초성으로 넘어갑니다.")
            st.session_state.round += 1
            st.session_state.current_chosung = random.choice(all_chosungs)
            st.session_state.used_words = []
    else:
        st.error("❌ 존재하지 않거나 틀린 단어입니다.")

st.markdown(f"### 🔢 현재 점수: {st.session_state.score}")
