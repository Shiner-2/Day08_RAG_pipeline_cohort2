"""Simple Streamlit chatbot frontend following Design.md."""

from __future__ import annotations

import html
from pathlib import Path

import requests
import streamlit as st


BACKEND_URL = "http://127.0.0.1:8000"
FONT_STACK = 'din-round, "Trebuchet MS", Helvetica, Arial, sans-serif'
FONT_SIZE = "17px"

SAMPLE_QUESTIONS = [
    "Hình phạt cho tội tàng trữ trái phép chất ma túy là gì?",
    "Luật Phòng, chống ma túy 2021 quy định gì về cai nghiện?",
    "Những nghệ sĩ nào trong dữ liệu tin tức liên quan tới ma túy?",
]


def inject_styles() -> None:
    st.markdown(
        f"""
        <style>
        :root {{
            --brand: #1CB0F6;
            --brand-hover: #1A95D1;
            --accent: #00B086;
            --text: #3C3C3C;
            --border: #C1C1C1;
            --soft-border: #E0E0E0;
            --page: #F5F5F5;
            --white: #FFFFFF;
            --font: {FONT_STACK};
            --font-size: {FONT_SIZE};
        }}

        html, body, .stApp, .stApp *, [data-testid="stSidebar"], [data-testid="stSidebar"] * {{
            font-family: var(--font) !important;
            font-size: var(--font-size) !important;
            line-height: 24px !important;
            letter-spacing: 0 !important;
            color: var(--text);
        }}

        .stApp {{
            background: var(--page);
        }}

        .main .block-container {{
            max-width: 900px;
            padding: 24px 24px 80px 24px;
        }}

        .app-shell {{
            background: var(--white);
            border: 1px solid var(--soft-border);
            border-radius: 12px;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.08);
            padding: 24px;
        }}

        .topbar {{
            align-items: center;
            border-bottom: 1px solid #EEEEEE;
            display: flex;
            gap: 12px;
            min-height: 70px;
            padding-bottom: 16px;
        }}

        .brand-dot {{
            background: var(--brand);
            border-radius: 50%;
            display: inline-block;
            height: 16px;
            width: 16px;
        }}

        .brand-title {{
            font-weight: 700;
        }}

        .subtitle {{
            color: #666666;
            margin-top: 8px;
        }}

        .chat-list {{
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin: 24px 0;
        }}

        .message {{
            border: 1px solid var(--soft-border);
            border-radius: 12px;
            padding: 16px;
            white-space: pre-wrap;
        }}

        .message-user {{
            background: rgba(28, 176, 246, 0.10);
            border-color: rgba(28, 176, 246, 0.28);
        }}

        .message-assistant {{
            background: var(--white);
        }}

        .message-label {{
            color: var(--brand);
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .meta-row {{
            border-top: 1px solid #EEEEEE;
            color: #666666;
            margin-top: 12px;
            padding-top: 8px;
        }}

        .source-box {{
            background: #F5F5F5;
            border: 1px solid var(--soft-border);
            border-radius: 8px;
            margin-top: 8px;
            padding: 12px 16px;
            white-space: pre-wrap;
        }}

        div[data-testid="stForm"] {{
            background: var(--white);
            border: 1px solid var(--soft-border);
            border-radius: 12px;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.08);
            padding: 16px;
        }}

        div[data-testid="stTextArea"] textarea {{
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            min-height: 96px !important;
            padding: 12px 16px !important;
        }}

        .stButton button, div[data-testid="stFormSubmitButton"] button {{
            background: var(--brand) !important;
            border: none !important;
            border-radius: 12px !important;
            color: var(--white) !important;
            font-weight: 700 !important;
            min-height: 50px !important;
            padding: 0 16px !important;
        }}

        .stButton button:hover, div[data-testid="stFormSubmitButton"] button:hover {{
            background: var(--brand-hover) !important;
            color: var(--white) !important;
        }}

        .status-pill {{
            background: var(--accent);
            border-radius: 2px;
            color: var(--white) !important;
            display: inline-block;
            font-weight: 700;
            padding: 4px 8px;
        }}

        .offline {{
            background: #CCCCCC;
            color: #666666 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("session_id", None)


def reset_chat() -> None:
    st.session_state.messages = []
    st.session_state.session_id = None


def backend_health() -> dict:
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=4)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        return {"status": "offline", "error": str(exc), "llm_configured": False}


def call_backend(message: str, top_k: int, use_llm: bool) -> dict:
    response = requests.post(
        f"{BACKEND_URL}/chat",
        json={
            "message": message,
            "session_id": st.session_state.session_id,
            "top_k": top_k,
            "use_memory": True,
            "use_llm": use_llm,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def safe_text(value: object) -> str:
    return html.escape(str(value or "").strip())


def render_header() -> None:
    st.markdown(
        """
        <div class="app-shell">
            <div class="topbar">
                <span class="brand-dot"></span>
                <span class="brand-title">RAG Chatbot Pháp Luật Ma Túy</span>
            </div>
            <div class="subtitle">
                Chatbot hỏi đáp dựa trên văn bản pháp luật và bài báo đã crawl. Câu trả lời có citation và source documents.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_message(message: dict) -> None:
    role = message.get("role", "assistant")
    label = "Bạn" if role == "user" else "Chatbot"
    css_class = "message-user" if role == "user" else "message-assistant"
    content = safe_text(message.get("content", ""))

    meta = ""
    if role == "assistant":
        meta = (
            "<div class='meta-row'>"
            f"Generation: {safe_text(message.get('generation_mode', 'unknown'))} | "
            f"Retrieval: {safe_text(message.get('retrieval_source', 'unknown'))}"
            "</div>"
        )

    st.markdown(
        f"""
        <div class="message {css_class}">
            <div class="message-label">{label}</div>
            <div>{content}</div>
            {meta}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if role == "assistant":
        render_sources(message.get("sources", []))


def render_sources(sources: list[dict]) -> None:
    if not sources:
        return

    with st.expander(f"Source documents ({len(sources)})", expanded=False):
        for index, source in enumerate(sources, 1):
            metadata = source.get("metadata", {})
            source_name = safe_text(metadata.get("source", "unknown"))
            doc_type = safe_text(metadata.get("type", "unknown"))
            score = float(source.get("score", 0.0))
            content = safe_text(source.get("content", "")[:1200])
            st.markdown(
                f"""
                <div class="source-box">
                    <b>{index}. {source_name}</b><br>
                    Type: {doc_type} | Score: {score:.3f}<br><br>
                    {content}
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_sidebar() -> tuple[int, bool]:
    health = backend_health()
    online = health.get("status") == "ok"

    with st.sidebar:
        st.markdown("**Trạng thái**")
        pill_class = "status-pill" if online else "status-pill offline"
        pill_text = "Backend online" if online else "Backend offline"
        st.markdown(f"<span class='{pill_class}'>{pill_text}</span>", unsafe_allow_html=True)
        st.write(f"API: {BACKEND_URL}/chat")
        st.write(f"LLM key: {'ready' if health.get('llm_configured') else 'not configured'}")

        st.divider()
        top_k = st.slider("Số source truy xuất", min_value=2, max_value=8, value=5)
        use_llm = st.toggle("Gọi LLM API", value=True)
        st.button("Xóa hội thoại", on_click=reset_chat, use_container_width=True)

        st.divider()
        st.markdown("**Câu hỏi mẫu**")
        for question in SAMPLE_QUESTIONS:
            if st.button(question, use_container_width=True):
                st.session_state.pending_question = question

        st.divider()
        st.write(f"Workspace: {Path.cwd().name}")

    return top_k, use_llm


def render_chat_history() -> None:
    if not st.session_state.messages:
        st.markdown(
            """
            <div class="message message-assistant">
                <div class="message-label">Chatbot</div>
                <div>Nhập câu hỏi bên dưới để bắt đầu.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown("<div class='chat-list'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        render_message(message)
    st.markdown("</div>", unsafe_allow_html=True)


def render_input(top_k: int, use_llm: bool) -> None:
    pending = st.session_state.pop("pending_question", "")

    with st.form("chat_form", clear_on_submit=True):
        question = st.text_area(
            "Câu hỏi",
            value=pending,
            placeholder="Nhập câu hỏi về pháp luật ma túy hoặc tin tức liên quan...",
            label_visibility="visible",
        )
        submitted = st.form_submit_button("Gửi câu hỏi", use_container_width=True)

    if not submitted or not question.strip():
        return

    user_message = {"role": "user", "content": question.strip()}
    st.session_state.messages.append(user_message)

    try:
        result = call_backend(question.strip(), top_k=top_k, use_llm=use_llm)
        st.session_state.session_id = result.get("session_id")
        assistant_message = {
            "role": "assistant",
            "content": result.get("answer", "Tôi không thể xác minh thông tin này từ nguồn hiện có."),
            "sources": result.get("sources", []),
            "generation_mode": result.get("generation_mode", "unknown"),
            "retrieval_source": result.get("retrieval_source", "unknown"),
        }
    except requests.RequestException as exc:
        assistant_message = {
            "role": "assistant",
            "content": f"Backend chưa sẵn sàng hoặc lỗi kết nối: {exc}",
            "sources": [],
            "generation_mode": "error",
            "retrieval_source": "none",
        }

    st.session_state.messages.append(assistant_message)
    st.rerun()


def main() -> None:
    st.set_page_config(page_title="RAG Chatbot", page_icon=":material/chat:", layout="centered")
    inject_styles()
    init_state()

    top_k, use_llm = render_sidebar()
    render_header()
    render_chat_history()
    render_input(top_k=top_k, use_llm=use_llm)


if __name__ == "__main__":
    main()
