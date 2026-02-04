
import streamlit as st
import requests

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
            try:
                data = res.json()
                st.session_state.token = data["access_token"]
                st.session_state.role = data.get("role")
                st.success("Login successful ✅")
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
    st.subheader("📊 Dashboard")

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
                        st.success("Audio processed!")
                        st.text_area("Transcript", data["transcript"], height=200)
                        st.text_area("Summary", data["summary"], height=150)
                    else:
                        st.error(res.text)


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
            text_input = st.text_area("Paste your text here")

            if text_input and st.button("Index Text"):
                with st.spinner("Indexing text..."):
                    res = requests.post(
                        "http://localhost:8000/upload/text",
                        json={"text": text_input},
                        headers=headers
                    )

                    if res.status_code == 200:
                        st.success("Text indexed successfully!")
                    else:
                        st.error(res.text)


    with tab2:
        st.subheader("Ask Questions")
        question = st.text_input("Ask something about your uploaded docs/audio")

        if st.button("Ask"):
            res = requests.post(
                f"{API_URL}/rag/ask",
                params={"question": question},
                headers=headers
            )

            if res.status_code == 200:
                st.markdown(f"**Answer:** {res.json()['answer']}")
            else:
                st.error(res.text)




