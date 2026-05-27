import streamlit as st
import google.generativeai as genai

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="💌 연애상담 챗봇",
    page_icon="💌",
    layout="centered"
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 기반 AI 상담 챗봇")

# -----------------------------
# API KEY 설정
# -----------------------------
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)

except Exception:
    st.error("❌ GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# -----------------------------
# 모델 설정
# -----------------------------
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="""
너는 공감 능력이 뛰어난 연애상담 AI이다.

규칙:
- 사용자의 감정을 먼저 공감한다.
- 따뜻하고 자연스럽게 답변한다.
- 위험하거나 공격적인 조언은 하지 않는다.
- 현실적인 연애 조언을 제공한다.
- 답변은 한국어로 한다.
"""
    )

except Exception as e:
    st.error(f"❌ 모델 초기화 오류: {e}")
    st.stop()

# -----------------------------
# 채팅 기록 저장
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 이전 채팅 출력
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
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
                # 대화 기록 만들기
                conversation = ""

                for msg in st.session_state.messages:

                    role = "사용자" if msg["role"] == "user" else "상담사"

                    conversation += f"{role}: {msg['content']}\n"

                prompt = f"""
다음은 연애상담 대화이다.

{conversation}

상담사 답변:
"""

                response = model.generate_content(prompt)

                ai_reply = response.text

                st.markdown(ai_reply)

                # AI 답변 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_reply
                })

            except Exception as e:

                error_message = f"❌ 오류 발생: {str(e)}"

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:

    st.header("⚙️ 메뉴")

    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.markdown("""
### 📌 사용 모델
- Gemini 1.5 Flash

### ✅ 기능
- 채팅 기록 유지
- 오류 처리
- Streamlit Cloud 배포 가능
""")
