
import streamlit as st
import requests

def get_score_emoji(score):
    if score > 0.8:
        return "🟢"
    elif score > 0.5:
        return "🟡"
    else:
        return "🔴"
        
ROLE_MODE_MAP = {
    "lawyer": ["legal"],
    "doctor": ["healthcare"],
    "researcher": ["academic"],
    "finance": ["finance"],
    "business": ["business"],
    "admin": ["legal", "finance", "academic", "healthcare", "business"]
}


API_URL = "http://127.0.0.1:8000"  # FastAPI backend

st.set_page_config(page_title="AIDocHub", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None

if "role" not in st.session_state:
    st.session_state.role = None

tab1, tab2 = st.tabs(["Login", "Signup"])

# LOGIN 
with tab1:
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(
            f"{API_URL}/auth/login",
            data={
                "username": email,   # OAuth2PasswordRequestForm expects "username"
                "password": password
            }
        )

        # 🔍 Always check response first
        st.write("Status:", res.status_code)

        if res.status_code == 200:
            # try:
            #     data = res.json()
            #     st.session_state.token = data["access_token"]
            #     st.session_state.role = data.get("role")
            #     st.success("Login successful ✅")
            try:
                data = res.json()
                st.session_state.token = data["access_token"]
                st.session_state.role = data.get("role")

                role_display = (st.session_state.role or "unknown").upper()

                st.success(f"Login successful ✅")
                st.info(f"🔐 You are logged in as: **{role_display}**")

            except Exception:
                st.error(f"Server returned non-JSON:\n{res.text}")
        else:
            # Show backend error instead of crashing
            try:
                err = res.json()
                st.error(err.get("detail", "Login failed"))
            except Exception:
                st.error(f"Login failed:\n{res.text}")


# POST-LOGIN DASHBOARD 
if st.session_state.token:

    st.divider()

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    st.subheader("📊 Dashboard")

    # 👑 ADMIN PANEL
    if st.session_state.role == "admin":

        st.subheader("👑 Admin Panel — User Management")

        # ---- LOAD USERS ----
        if st.button("Load Users"):
            res = requests.get(
                f"{API_URL}/admin/users",
                headers=headers
            )

            if res.status_code == 200:
                st.session_state.users = res.json()
            else:
                st.error(res.text)

        # ---- SHOW USERS (PERSISTENT) ----
        if "users" in st.session_state:

            st.dataframe(st.session_state.users)

            # ---- DELETE USER ----
            st.markdown("### 🗑 Delete User")

            user_id = st.number_input(
                "Enter User ID to delete",
                min_value=1,
                step=1
            )

            if st.button("Delete User"):
                delete_res = requests.delete(
                    f"{API_URL}/admin/users/{int(user_id)}",
                    headers=headers
                )

                if delete_res.status_code == 200:
                    st.success("User deleted successfully ✅")

                    # refresh users list automatically
                    res = requests.get(
                        f"{API_URL}/admin/users",
                        headers=headers
                    )
                    if res.status_code == 200:
                        st.session_state.users = res.json()

                else:
                    st.error(delete_res.text)


    # You must decode role from token or fetch from backend
    # If your /auth/login returns role, store it like:
    # st.session_state.role = data["role"]

    role = st.session_state.role

    if role == "admin":
        st.success("Welcome Admin 👑")
        st.write("• Manage users")
        st.write("• View system logs")

    elif role == "lawyer":
        st.success("Welcome Lawyer ⚖️")
        st.write("• Upload legal documents")
        st.write("• Ask legal questions")

    elif role == "doctor":
        st.success("Welcome Doctor 🩺")
        st.write("• Upload medical reports")
        st.write("• Ask health-related questions")

    elif role == "researcher":
        st.success("Welcome Researcher 🔬")
        st.write("• Upload research papers")
        st.write("• Ask research questions")

    elif role == "finance":
        st.success("Welcome Finance Analyst 💹")
        st.write("• Upload financial documents")
        st.write("• Ask finance questions")

    elif role == "business":
        st.success("Welcome Business User 📈")
        st.write("• Upload business docs")
        st.write("• Ask business questions")


#  SIGNUP 
with tab2:
    st.subheader("Signup")

    email_s = st.text_input("Signup Email")
    password_s = st.text_input("Signup Password", type="password")
    role = st.selectbox("Role", ["lawyer", "doctor", "researcher", "finance", "business", "admin"])

    if st.button("Create Account"):
        res = requests.post(
            f"{API_URL}/auth/signup",
            json={
                # "username": username,
                "email": email_s,
                "password": password_s,
                "role": role
            }
        )

        if res.status_code == 200:
            st.success("Account created 🎉 You can now login.")
        else:
            st.error(res.text)


# Main UI

if st.session_state.token:

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    st.title("📄 AIDocHub — AI Document Intelligence")

    tab1, tab2 = st.tabs(["📤 Upload ", "💬 Ask Your Docs"])

    with tab1:
        st.subheader("📤 Upload to AI Doc Hub")

        upload_type = st.radio(
            "Choose input type:",
            ["Audio", "PDF", "Text"]
        )

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        # AUDIO UPLOAD 
        
        if upload_type == "Audio":
            audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav", "m4a","webm"])

            if audio_file and st.button("Transcribe & Index Audio"):
                with st.spinner("Transcribing audio..."):
                    files = {"file": (audio_file.name, audio_file, audio_file.type)}

                    res = requests.post(
                        "http://localhost:8000/transcription/audio",
                        files=files,
                        headers=headers
                    )

                    if res.status_code == 200:
                        data = res.json()
                        transcript = data.get("text", "")

                        st.success("Audio processed!")

                        # Show transcript
                        st.text_area("Transcript", transcript, height=200)

                        # Save transcript so Streamlit remembers it
                        st.session_state["transcript"] = transcript

                    else:
                        st.error(res.text)

            # Generate summary button
            if "transcript" in st.session_state:
                if st.button("Generate Summary"):
                    with st.spinner("Generating summary..."):

                        summary_res = requests.post(
                            "http://localhost:8000/summarize/text",
                            json={
                                "text": st.session_state["transcript"],
                                "method": "extractive"
                            },
                            headers=headers
                        )

                        if summary_res.status_code == 200:
                            summary_data = summary_res.json()
                            summary = summary_data.get("summary", "")

                            st.text_area("Summary", summary, height=150)

                        else:
                            st.error(summary_res.text)


        # PDF UPLOAD 
        elif upload_type == "PDF":
            pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

            if pdf_file and st.button("Upload & Index PDF"):
                with st.spinner("Processing PDF..."):
                    files = {"file": (pdf_file.name, pdf_file, pdf_file.type)}
                    res = requests.post(
                        "http://localhost:8000/upload/file",
                        files=files,
                        headers=headers
                    )

                    if res.status_code == 200:
                        st.success("PDF indexed successfully!")
                    else:
                        st.error(res.text)


        # TEXT INPUT 
        elif upload_type == "Text":

            uploaded_file = st.file_uploader(
                "Upload TXT file",
                type=["txt"]
            )

            if uploaded_file and st.button("Upload TXT"):

                with st.spinner("Uploading and indexing text..."):

                    files = {
                        "file": (uploaded_file.name, uploaded_file, "text/plain")
                    }

                    res = requests.post(
                        "http://localhost:8000/upload/file",
                        files=files,
                        params={"domain": "general"},
                        headers=headers
                    )

                    if res.status_code == 200:
                        st.success("TXT file indexed successfully!")
                    else:
                        st.error(res.text)


    with tab2:
        st.subheader("Ask Your Docs")
        role = (st.session_state.role or "").lower().strip()
        st.write("DEBUG role:", st.session_state.role)
        # st.write("DEBUG selected mode:", mode)
        allowed_modes = ROLE_MODE_MAP.get(role, [])

        if not allowed_modes:
            st.warning("No modes available for your role.")
            st.stop()

        if "mode" in st.session_state:
            del st.session_state["mode"]

        mode = st.selectbox(
            "Select Assistant Mode",
            allowed_modes
        )

        st.caption(f"🔐 Role: **{role.upper()}** | Mode access restricted")

        question = st.text_input("Ask something about your uploaded docs/audio")

        if st.button("Ask"):
            res = requests.post(
                f"{API_URL}/rag/ask",
                params={
                    "question": question,
                    "mode": mode
                },
                headers=headers
            )


            if res.status_code == 200:
                data = res.json()

                # ✅ Answer
                st.markdown(f"**Answer:** {data['answer']}")

                # ✅ Evaluation Scores
                # st.subheader("📊 Evaluation Scores")

                # scores = data.get("evaluation", {})

                # col1, col2, col3 = st.columns(3)

                # f = scores.get("faithfulness", 0)
                # r = scores.get("answer_relevancy", 0)
                # p = scores.get("context_precision", 0)

                # col1.metric("Faithfulness", f"{get_score_emoji(f)} {round(f, 2)}")
                # col2.metric("Relevancy", f"{get_score_emoji(r)} {round(r, 2)}")
                # col3.metric("Context Precision", f"{get_score_emoji(p)} {round(p, 2)}")

            else:
                st.error(res.text)
        


