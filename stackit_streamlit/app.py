import streamlit as st
import json
import uuid
import os

DATA_FILE = "questions.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def post_question(title, description, tags):
    data = load_data()
    question = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "tags": tags.split(","),
        "answers": []
    }
    data.append(question)
    save_data(data)

def add_answer(question_id, answer_text):
    data = load_data()
    for q in data:
        if q["id"] == question_id:
            q["answers"].append(answer_text)
            break
    save_data(data)

st.title("🧠 StackIt – Minimal Q&A Forum")

menu = ["Home", "Ask Question"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "Home":
    st.subheader("📋 All Questions")
    data = load_data()
    for q in data:
        st.markdown(f"### {q['title']}")
        st.write(q['description'])
        st.markdown(f"**Tags:** {', '.join(q['tags'])}")

        if q["answers"]:
            st.markdown("**Answers:**")
            for a in q["answers"]:
                st.write("- " + a)
        else:
            st.write("_No answers yet_")

        with st.expander("💬 Add an answer"):
            ans = st.text_area(f"Your answer to: {q['title']}", key=q['id'])
            if st.button("Submit Answer", key="submit_" + q['id']):
                if ans.strip():
                    add_answer(q["id"], ans.strip())
                    st.success("Answer submitted!")
                    st.rerun()

elif choice == "Ask Question":
    st.subheader("❓ Ask a New Question")
    title = st.text_input("Title")
    desc = st.text_area("Description")
    tags = st.text_input("Tags (comma separated)")

    if st.button("Post Question"):
        if title and desc:
            post_question(title, desc, tags)
            st.success("Question posted!")
        else:
            st.warning("Please fill in title and description")