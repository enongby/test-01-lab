import streamlit as st
from typing import List, Dict


def initialize_session_state() -> None:
    """세션 상태 초기화"""
    if "todos" not in st.session_state:
        st.session_state.todos = []
    if "next_todo_id" not in st.session_state:
        st.session_state.next_todo_id = 0


def add_todo(title: str) -> None:
    """할 일 추가"""
    if title.strip():
        todo = {
            "id": st.session_state.next_todo_id,
            "title": title.strip(),
            "completed": False,
        }
        st.session_state.todos.append(todo)
        st.session_state.next_todo_id += 1


def toggle_todo(todo_id: int) -> None:
    """할 일 완료 상태 토글"""
    for todo in st.session_state.todos:
        if todo["id"] == todo_id:
            todo["completed"] = st.session_state[f"todo_{todo_id}_completed"]
            break


def delete_todo(todo_id: int) -> None:
    """할 일 삭제"""
    st.session_state.todos = [
        todo for todo in st.session_state.todos if todo["id"] != todo_id
    ]


def get_todo_stats() -> Dict[str, int]:
    """할 일 통계 계산"""
    total = len(st.session_state.todos)
    completed = sum(1 for todo in st.session_state.todos if todo["completed"])
    remaining = total - completed
    return {"total": total, "completed": completed, "remaining": remaining}


def render_stats() -> None:
    """통계 표시"""
    stats = get_todo_stats()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("전체", stats["total"])
    with col2:
        st.metric("완료", stats["completed"])
    with col3:
        st.metric("미완료", stats["remaining"])


def render_todos() -> None:
    """할 일 목록 표시"""
    if not st.session_state.todos:
        st.info("📝 할 일이 없습니다. 새로 추가해보세요!")
        return

    st.subheader("📋 할 일 목록")
    
    for todo in st.session_state.todos:
        col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
        
        with col1:
            # 체크박스로 완료 상태 표시 및 업데이트
            st.checkbox(
                todo["title"],
                value=todo["completed"],
                key=f"todo_{todo['id']}_completed",
                on_change=lambda todo_id=todo['id']: toggle_todo(todo_id),
            )
        
        with col2:
            # 완료/미완료 표시
            status = "✅ 완료" if todo["completed"] else "⏳ 미완료"
            st.caption(status)
        
        with col3:
            # 삭제 버튼
            if st.button("🗑️", key=f"delete_{todo['id']}", help="삭제"):
                delete_todo(todo["id"])
                st.rerun()


def main() -> None:
    """메인 앱"""
    st.set_page_config(
        page_title="할 일 관리",
        page_icon="✅",
        layout="wide",
    )
    
    # 모바일 최적화 CSS
    st.markdown("""
        <style>
        h1 { font-size: 1.8rem !important; margin-bottom: 0.5rem !important; }
        h2 { font-size: 1.3rem !important; margin-bottom: 0.3rem !important; }
        .stMetric { font-size: 0.95rem !important; }
        input, button { font-size: 0.95rem !important; }
        label { font-size: 0.9rem !important; }
        p, div { font-size: 0.9rem !important; }
        .stCaption { font-size: 0.85rem !important; }
        </style>
    """, unsafe_allow_html=True)
    
    initialize_session_state()
    
    st.title("✅ 할 일 관리")
    st.divider()
    
    # 통계 영역
    st.subheader("📊 통계")
    render_stats()
    st.divider()
    
    # 할 일 추가 영역
    st.subheader("➕ 새 할 일 추가")
    new_todo = st.text_input(
        "할 일을 입력하세요",
        placeholder="예: 으농비 생각하기",
        label_visibility="collapsed",
    )
    
    if st.button("추가", type="primary", use_container_width=True):
        add_todo(new_todo)
        st.rerun()
    
    st.divider()
    
    # 할 일 목록 영역
    render_todos()


if __name__ == "__main__":
    main()
