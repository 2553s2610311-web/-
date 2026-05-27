
# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
    layout="centered"
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반 상담 챗봇")

# ---------------------------
# API KEY 불러오기
# ---------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

except Exception:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# ---------------------------
# 모델 생성
# ---------------------------
try:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction="""
너는 따뜻하고 공감 능력이 뛰어난 연애상담 챗봇이다.

규칙:
- 사용자의 감정을 먼저 공감한다.
- 너무 단정적으로 판단하지 않는다.
- 현실적인 조언을 제공한다.
- 공격적이거나 위험한 조언은 하지 않는다.
- 답변은 자연스럽고 친근한 한국어로 한다.
"""
    )

except Exception as e:
    st.error(f"모델 초기화 오류: {e}")
    st.stop()

# ---------------------------
# 채팅 기록 저장
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------
# 사용자 입력
# ---------------------------
user_input = st.chat_input("연애 고민을 입력하세요...")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):

        with st.spinner("답변 생성 중..."):

            try:
                # 대화 기록 구성
                history_text = ""

                for msg in st.session_state.messages:
                    role = "사용자" if msg["role"] == "user" else "상담사"
                    history_text += f"{role}: {msg['content']}\n"

                prompt = f"""
다음은 사용자와의 연애상담 대화 기록이다.

{history_text}

상담사 답변:
"""

                response = model.generate_content(prompt)

                ai_response = response.text

                st.markdown(ai_response)

                # AI 응답 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response
                })

            except Exception as e:
                error_message = f"오류가 발생했습니다: {e}"

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })

# ---------------------------
# 사이드바
# ---------------------------
with st.sidebar:

    st.header("설정")

    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
### 사용 모델
- Gemini 2.5 Flash Lite

### 기능
- 채팅 기록 유지
- 오류 처리
- Streamlit Cloud 배포 가능
"""
    )
