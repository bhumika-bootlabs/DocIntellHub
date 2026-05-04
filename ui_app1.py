# """
# DocuMind AI — Streamlit UI
# Run: streamlit run streamlit_app.py
# Deps: pip install streamlit requests
# """

# import streamlit as st
# import requests
# import json
# import base64
# from datetime import datetime, timezone

# # ── PAGE CONFIG ─────────────────────────────────────────────
# st.set_page_config(
#     page_title="DocuMind AI",
#     page_icon="📜",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ── GLOBAL CSS ───────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

# /* ── TOKENS ──────────────────────────────────── */
# :root {
#   --cream:   #F7F4EF;
#   --parchment: #EDE8DF;
#   --warm-white: #FAF8F5;
#   --ink:     #1A1714;
#   --ink-2:   #4A4540;
#   --ink-3:   #8A8480;
#   --ink-4:   #B8B4B0;
#   --accent:  #2D5A3D;
#   --accent-light: #E8F0EA;
#   --accent-2: #8B4513;
#   --gold:    #C49A3C;
#   --gold-lt: #FDF4E3;
#   --border:  #DDD8D0;
#   --border-2: #C8C2B8;
#   --danger:  #8B2020;
#   --danger-lt: #FDF0F0;
#   --shadow:  0 1px 3px rgba(26,23,20,.08), 0 4px 16px rgba(26,23,20,.06);
# }

# /* ── RESET ───────────────────────────────────── */
# html, body, [class*="css"] {
#   font-family: 'DM Sans', sans-serif !important;
#   background-color: var(--cream) !important;
#   color: var(--ink) !important;
# }

# /* Hide Streamlit chrome */
# #MainMenu, footer, header { visibility: hidden; }
# .block-container {
#   padding: 0 2rem 2rem !important;
#   max-width: 100% !important;
# }

# /* ── SIDEBAR ─────────────────────────────────── */
# [data-testid="stSidebar"] {
#   background: var(--ink) !important;
#   border-right: none !important;
# }
# [data-testid="stSidebar"] * { color: var(--ink-4) !important; }
# [data-testid="stSidebarContent"] { padding: 0 !important; }

# /* Sidebar buttons */
# [data-testid="stSidebar"] .stButton > button {
#   background: transparent !important;
#   color: var(--ink-4) !important;
#   border: none !important;
#   border-radius: 6px !important;
#   text-align: left !important;
#   font-size: 13px !important;
#   font-weight: 400 !important;
#   padding: 8px 12px !important;
#   width: 100% !important;
#   justify-content: flex-start !important;
#   letter-spacing: 0 !important;
# }
# [data-testid="stSidebar"] .stButton > button:hover {
#   background: rgba(255,255,255,.07) !important;
#   color: #fff !important;
#   transform: none !important;
#   box-shadow: none !important;
# }

# /* ── TYPOGRAPHY ──────────────────────────────── */
# h1 {
#   font-family: 'DM Serif Display', serif !important;
#   font-size: 2rem !important;
#   font-weight: 400 !important;
#   color: var(--ink) !important;
#   letter-spacing: -.02em !important;
#   line-height: 1.15 !important;
# }
# h2 {
#   font-family: 'DM Serif Display', serif !important;
#   font-size: 1.35rem !important;
#   font-weight: 400 !important;
#   color: var(--ink) !important;
# }
# h3 {
#   font-family: 'DM Sans', sans-serif !important;
#   font-size: .75rem !important;
#   font-weight: 600 !important;
#   color: var(--ink-3) !important;
#   letter-spacing: .1em !important;
#   text-transform: uppercase !important;
# }

# /* ── BUTTONS ─────────────────────────────────── */
# .stButton > button {
#   background: var(--ink) !important;
#   color: var(--cream) !important;
#   border: none !important;
#   border-radius: 6px !important;
#   font-family: 'DM Sans', sans-serif !important;
#   font-size: 13px !important;
#   font-weight: 500 !important;
#   padding: 9px 20px !important;
#   letter-spacing: .01em !important;
#   transition: background .15s, transform .15s !important;
#   box-shadow: none !important;
# }
# .stButton > button:hover {
#   background: var(--accent) !important;
#   transform: translateY(-1px) !important;
# }
# .stButton > button:disabled { opacity: .4 !important; }

# /* ── INPUTS ──────────────────────────────────── */
# .stTextInput > div > div > input,
# .stTextArea > div > div > textarea,
# .stSelectbox > div > div,
# .stNumberInput > div > div > input {
#   background: var(--warm-white) !important;
#   border: 1px solid var(--border) !important;
#   border-radius: 6px !important;
#   color: var(--ink) !important;
#   font-family: 'DM Sans', sans-serif !important;
#   font-size: 13px !important;
#   box-shadow: none !important;
# }
# .stTextInput > div > div > input:focus,
# .stTextArea > div > div > textarea:focus {
#   border-color: var(--accent) !important;
#   box-shadow: 0 0 0 3px rgba(45,90,61,.1) !important;
# }

# /* ── TABS ────────────────────────────────────── */
# .stTabs [data-baseweb="tab-list"] {
#   background: transparent !important;
#   border-bottom: 1.5px solid var(--border) !important;
#   gap: 0 !important;
# }
# .stTabs [data-baseweb="tab"] {
#   background: transparent !important;
#   color: var(--ink-3) !important;
#   font-family: 'DM Sans', sans-serif !important;
#   font-size: 13px !important;
#   font-weight: 500 !important;
#   padding: 10px 20px !important;
#   border-bottom: 2px solid transparent !important;
#   border-radius: 0 !important;
# }
# .stTabs [aria-selected="true"] {
#   color: var(--accent) !important;
#   border-bottom-color: var(--accent) !important;
# }

# /* ── FILE UPLOADER ───────────────────────────── */
# [data-testid="stFileUploader"] {
#   background: var(--warm-white) !important;
#   border: 1.5px dashed var(--border-2) !important;
#   border-radius: 10px !important;
#   padding: 20px !important;
# }

# /* ── METRICS ─────────────────────────────────── */
# [data-testid="stMetric"] {
#   background: var(--warm-white) !important;
#   border: 1px solid var(--border) !important;
#   border-radius: 8px !important;
#   padding: 14px 16px !important;
#   box-shadow: var(--shadow) !important;
# }
# [data-testid="stMetricLabel"] {
#   font-size: 10px !important;
#   font-weight: 600 !important;
#   color: var(--ink-3) !important;
#   text-transform: uppercase !important;
#   letter-spacing: .08em !important;
# }
# [data-testid="stMetricValue"] {
#   font-family: 'DM Serif Display', serif !important;
#   font-size: 1.5rem !important;
#   color: var(--ink) !important;
# }

# /* ── EXPANDER ────────────────────────────────── */
# [data-testid="stExpander"] {
#   border: 1px solid var(--border) !important;
#   border-radius: 8px !important;
#   background: var(--warm-white) !important;
#   box-shadow: none !important;
# }

# /* ── ALERTS / BADGES ─────────────────────────── */
# .stSuccess, .stInfo, .stWarning, .stError {
#   border-radius: 6px !important;
#   font-size: 13px !important;
# }

# /* ── DIVIDER ─────────────────────────────────── */
# hr { border-color: var(--border) !important; margin: 16px 0 !important; }

# /* ── RADIO ───────────────────────────────────── */
# .stRadio > div { flex-direction: row !important; gap: 16px; }
# .stRadio label { font-size: 13px !important; color: var(--ink-2) !important; }

# /* ── SELECTBOX ───────────────────────────────── */
# .stSelectbox label, .stTextArea label, .stTextInput label, .stFileUploader label {
#   font-size: 11px !important;
#   font-weight: 600 !important;
#   color: var(--ink-3) !important;
#   text-transform: uppercase !important;
#   letter-spacing: .07em !important;
# }

# /* ── CUSTOM COMPONENTS ───────────────────────── */
# .doc-topbar {
#   background: var(--warm-white);
#   border-bottom: 1px solid var(--border);
#   padding: 14px 24px;
#   display: flex;
#   align-items: center;
#   justify-content: space-between;
#   margin: 0 -2rem 1.5rem;
#   position: sticky;
#   top: 0;
#   z-index: 99;
# }
# .page-kicker {
#   font-size: 10px;
#   font-weight: 600;
#   color: var(--ink-3);
#   letter-spacing: .12em;
#   text-transform: uppercase;
#   margin-bottom: 4px;
# }
# .endpoint-pill {
#   display: inline-flex;
#   align-items: center;
#   gap: 6px;
#   background: var(--parchment);
#   border: 1px solid var(--border);
#   border-radius: 999px;
#   padding: 4px 12px;
#   font-family: 'DM Mono', monospace;
#   font-size: 11px;
#   color: var(--ink-2);
# }
# .method-tag {
#   font-size: 9px;
#   font-weight: 700;
#   padding: 2px 5px;
#   border-radius: 3px;
#   background: var(--accent);
#   color: #fff;
#   letter-spacing: .04em;
# }
# .method-get { background: var(--accent-2) !important; }
# .method-delete { background: var(--danger) !important; }

# .chat-bubble-user {
#   background: var(--parchment);
#   border: 1px solid var(--border);
#   border-radius: 12px 12px 4px 12px;
#   padding: 12px 16px;
#   font-size: 14px;
#   color: var(--ink);
#   line-height: 1.6;
#   margin-bottom: 4px;
#   max-width: 85%;
#   margin-left: auto;
# }
# .chat-bubble-ai {
#   background: var(--warm-white);
#   border: 1px solid var(--border);
#   border-left: 3px solid var(--accent);
#   border-radius: 4px 12px 12px 12px;
#   padding: 14px 16px;
#   font-size: 14px;
#   color: var(--ink-2);
#   line-height: 1.7;
#   margin-bottom: 4px;
#   max-width: 90%;
# }
# .eval-row {
#   display: flex;
#   gap: 8px;
#   flex-wrap: wrap;
#   margin-top: 10px;
#   padding-top: 10px;
#   border-top: 1px solid var(--border);
# }
# .eval-chip {
#   background: var(--parchment);
#   border: 1px solid var(--border);
#   border-radius: 999px;
#   padding: 3px 10px;
#   font-family: 'DM Mono', monospace;
#   font-size: 11px;
#   color: var(--ink-2);
# }
# .eval-chip b { color: var(--accent); }

# .quick-chip {
#   display: inline-block;
#   background: var(--warm-white);
#   border: 1px solid var(--border-2);
#   border-radius: 999px;
#   padding: 5px 13px;
#   font-size: 12px;
#   color: var(--ink-2);
#   cursor: pointer;
#   transition: all .15s;
#   margin: 3px;
# }
# .quick-chip:hover {
#   background: var(--accent-light);
#   border-color: var(--accent);
#   color: var(--accent);
# }

# .result-block {
#   background: var(--warm-white);
#   border: 1px solid var(--border);
#   border-left: 3px solid var(--gold);
#   border-radius: 8px;
#   padding: 16px 18px;
#   font-size: 13px;
#   line-height: 1.8;
#   color: var(--ink-2);
#   font-family: 'DM Sans', sans-serif;
#   white-space: pre-wrap;
#   margin-top: 12px;
# }

# .token-block {
#   background: var(--ink);
#   border-radius: 8px;
#   padding: 16px 18px;
#   font-family: 'DM Mono', monospace;
#   font-size: 11.5px;
#   color: #A8D5A2;
#   word-break: break-all;
#   line-height: 1.7;
#   margin: 10px 0;
# }
# .token-key { color: #7EB8E8; }
# .token-val { color: #F5C97A; }

# .file-row {
#   display: flex;
#   align-items: center;
#   gap: 12px;
#   background: var(--warm-white);
#   border: 1px solid var(--border);
#   border-radius: 8px;
#   padding: 12px 14px;
#   margin-bottom: 8px;
# }
# .file-icon { font-size: 22px; }
# .file-name { font-size: 13px; font-weight: 500; color: var(--ink); }
# .file-meta { font-size: 11px; color: var(--ink-3); margin-top: 2px; }
# .file-domain {
#   margin-left: auto;
#   background: var(--accent-light);
#   border: 1px solid rgba(45,90,61,.2);
#   color: var(--accent);
#   padding: 3px 10px;
#   border-radius: 999px;
#   font-size: 11px;
#   font-weight: 600;
# }

# .pipeline-step {
#   display: flex;
#   align-items: flex-start;
#   gap: 12px;
#   padding: 10px 0;
#   border-bottom: 1px solid var(--border);
#   font-size: 13px;
#   color: var(--ink-2);
# }
# .pipeline-step:last-child { border-bottom: none; }
# .step-badge {
#   min-width: 22px;
#   height: 22px;
#   border-radius: 50%;
#   background: var(--parchment);
#   border: 1px solid var(--border-2);
#   color: var(--ink-3);
#   display: flex;
#   align-items: center;
#   justify-content: center;
#   font-size: 10px;
#   font-weight: 700;
#   flex-shrink: 0;
#   margin-top: 1px;
# }

# .user-card {
#   display: flex;
#   align-items: center;
#   gap: 14px;
#   background: var(--warm-white);
#   border: 1px solid var(--border);
#   border-radius: 8px;
#   padding: 12px 16px;
#   margin-bottom: 6px;
# }
# .user-avatar {
#   width: 34px; height: 34px;
#   border-radius: 50%;
#   background: var(--parchment);
#   border: 1px solid var(--border-2);
#   display: flex; align-items: center; justify-content: center;
#   font-size: 13px; font-weight: 600;
#   color: var(--ink-2);
#   flex-shrink: 0;
# }
# .user-id {
#   font-family: 'DM Mono', monospace;
#   font-size: 10px;
#   color: var(--ink-4);
# }
# .user-email-txt { font-size: 13px; color: var(--ink); font-weight: 500; }
# .role-badge {
#   margin-left: auto;
#   padding: 3px 10px;
#   border-radius: 999px;
#   font-size: 10px;
#   font-weight: 700;
#   letter-spacing: .05em;
#   text-transform: uppercase;
# }
# .rb-lawyer     { background: #E8F0F8; color: #2B5E8A; }
# .rb-doctor     { background: #E8F4EE; color: #2B6B44; }
# .rb-researcher { background: #F4E8F5; color: #6B2B8A; }
# .rb-finance    { background: #FDF4E3; color: #7A5A1A; }
# .rb-business   { background: #F5F4EF; color: #5A5040; }
# .rb-admin      { background: #FDF0F0; color: #8B2020; }

# .section-divider {
#   display: flex;
#   align-items: center;
#   gap: 12px;
#   margin: 20px 0 16px;
# }
# .section-divider-line { flex: 1; height: 1px; background: var(--border); }
# .section-divider-text {
#   font-size: 10px;
#   font-weight: 600;
#   color: var(--ink-4);
#   letter-spacing: .1em;
#   text-transform: uppercase;
# }

# /* Sidebar active state */
# .nav-active {
#   background: rgba(255,255,255,.1) !important;
#   color: #fff !important;
# }
# </style>
# """, unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════
# #  SESSION STATE
# # ═══════════════════════════════════════════════════════════
# def init_state():
#     defaults = {
#         "token":          None,
#         "user_email":     None,
#         "user_role":      None,
#         "base_url":       "http://localhost:8000",
#         "chat_history":   [],
#         "uploaded_docs":  [],
#         "page":           "ask",
#         "admin_users":    None,
#     }
#     for k, v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v

# init_state()


# # ═══════════════════════════════════════════════════════════
# #  CONSTANTS
# # ═══════════════════════════════════════════════════════════
# ROLE_MODES = {
#     "lawyer":     ["legal"],
#     "doctor":     ["healthcare"],
#     "researcher": ["academic"],
#     "finance":    ["finance"],
#     "business":   ["business"],
#     "admin":      ["legal", "finance", "academic", "healthcare", "business"],
# }
# MODE_LABELS = {
#     "legal": "⚖️ Legal", "finance": "📊 Finance",
#     "academic": "🔬 Academic", "healthcare": "🩺 Healthcare",
#     "business": "🏢 Business",
# }
# ROLE_ICONS = {
#     "lawyer": "⚖️", "doctor": "🩺", "researcher": "🔬",
#     "finance": "📊", "business": "🏢", "admin": "🛡️",
# }


# # ═══════════════════════════════════════════════════════════
# #  API WRAPPER
# # ═══════════════════════════════════════════════════════════
# def api(method: str, path: str, **kwargs):
#     base = st.session_state.base_url.rstrip("/")
#     headers = kwargs.pop("headers", {})
#     if st.session_state.token:
#         headers["Authorization"] = f"Bearer {st.session_state.token}"
#     try:
#         return requests.request(
#             method, f"{base}{path}",
#             headers=headers, timeout=60, **kwargs
#         )
#     except requests.exceptions.ConnectionError:
#         return None
#     except Exception as e:
#         st.error(f"Request error: {e}")
#         return None


# def decode_jwt(token: str) -> dict:
#     try:
#         parts = token.split(".")
#         padded = parts[1] + "=" * (4 - len(parts[1]) % 4)
#         return json.loads(base64.urlsafe_b64decode(padded))
#     except Exception:
#         return {}


# # ═══════════════════════════════════════════════════════════
# #  SHARED UI HELPERS
# # ═══════════════════════════════════════════════════════════
# def page_header(title: str, kicker: str, method: str, endpoint: str):
#     method_class = {
#         "POST": "method-tag",
#         "GET": "method-tag method-get",
#         "DELETE": "method-tag method-delete",
#     }.get(method, "method-tag")

#     st.markdown(f"""
#     <div class="doc-topbar">
#       <div>
#         <div class="page-kicker">{kicker}</div>
#         <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;
#                     color:var(--ink);line-height:1.2">{title}</div>
#       </div>
#       <div class="endpoint-pill">
#         <span class="{method_class}">{method}</span>
#         {endpoint}
#       </div>
#     </div>
#     """, unsafe_allow_html=True)


# def section_divider(label: str):
#     st.markdown(f"""
#     <div class="section-divider">
#       <div class="section-divider-line"></div>
#       <div class="section-divider-text">{label}</div>
#       <div class="section-divider-line"></div>
#     </div>
#     """, unsafe_allow_html=True)


# def result_block(content: str):
#     safe = content.replace("<", "&lt;").replace(">", "&gt;")
#     st.markdown(f'<div class="result-block">{safe}</div>', unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════
# #  SIDEBAR
# # ═══════════════════════════════════════════════════════════
# def render_sidebar():
#     role  = st.session_state.user_role  or "user"
#     email = st.session_state.user_email or "—"
#     icon  = ROLE_ICONS.get(role, "👤")

#     with st.sidebar:
#         # Brand
#         st.markdown(f"""
#         <div style="padding:20px 18px 16px;border-bottom:1px solid rgba(255,255,255,.08)">
#           <div style="font-family:'DM Serif Display',serif;font-size:20px;
#                       font-weight:400;color:#FAF8F5;letter-spacing:-.02em;
#                       margin-bottom:14px">📜 DocuMind AI</div>
#           <div style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);
#                       border-radius:8px;padding:10px 12px;display:flex;align-items:center;gap:10px">
#             <div style="width:28px;height:28px;border-radius:50%;
#                         background:rgba(255,255,255,.12);color:#FAF8F5;
#                         display:flex;align-items:center;justify-content:center;
#                         font-size:13px;flex-shrink:0">{icon}</div>
#             <div style="min-width:0">
#               <div style="font-size:11px;color:rgba(255,255,255,.5);
#                           overflow:hidden;text-overflow:ellipsis;
#                           white-space:nowrap;max-width:130px">{email}</div>
#               <div style="font-size:9px;font-weight:700;letter-spacing:.07em;
#                           color:#C49A3C;text-transform:uppercase;margin-top:2px">{role}</div>
#             </div>
#           </div>
#         </div>
#         """, unsafe_allow_html=True)

#         st.markdown('<div style="padding:10px 8px">', unsafe_allow_html=True)

#         # Nav items
#         nav_items = [
#             ("💬", "Ask AI (RAG)",      "ask"),
#             ("📁", "Upload Document",   "upload"),
#             ("📝", "Summarize",         "summarize"),
#             ("🔧", "Format Response",   "format"),
#             ("🎙", "Transcribe Audio",  "transcribe"),
#             ("🔑", "JWT Token",         "token"),
#         ]
#         if role == "admin":
#             nav_items.append(("🛡️", "Admin Panel", "admin"))

#         for ico, label, key in nav_items:
#             is_active = st.session_state.page == key
#             if is_active:
#                 st.markdown(f"""
#                 <div style="background:rgba(255,255,255,.12);border-radius:6px;
#                             padding:8px 12px;margin-bottom:2px;display:flex;
#                             align-items:center;gap:8px;cursor:default">
#                   <span style="font-size:14px">{ico}</span>
#                   <span style="font-size:13px;color:#FAF8F5;font-weight:500">{label}</span>
#                 </div>
#                 """, unsafe_allow_html=True)
#             else:
#                 if st.button(f"{ico}  {label}", key=f"nav_{key}", use_container_width=True):
#                     st.session_state.page = key
#                     st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown('<div style="padding:0 8px 8px;border-top:1px solid rgba(255,255,255,.06);margin-top:auto">', unsafe_allow_html=True)

#         st.markdown("<br>", unsafe_allow_html=True)
#         # Backend URL
#         with st.expander("⚙️ Backend", expanded=False):
#             url = st.text_input("URL", value=st.session_state.base_url,
#                                 label_visibility="collapsed",
#                                 key="sidebar_url")
#             if url != st.session_state.base_url:
#                 st.session_state.base_url = url

#         if st.button("↩  Sign out", key="logout", use_container_width=True):
#             for k in ["token", "user_email", "user_role",
#                       "chat_history", "uploaded_docs", "admin_users"]:
#                 st.session_state[k] = [] if k in ("chat_history","uploaded_docs") else None
#             st.session_state.page = "ask"
#             st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════
# #  AUTH
# # ═══════════════════════════════════════════════════════════
# def render_auth():
#     _, mid, _ = st.columns([1, 1.2, 1])
#     with mid:
#         st.markdown("<br><br>", unsafe_allow_html=True)
#         st.markdown("""
#         <div style="text-align:center;margin-bottom:28px">
#           <div style="font-family:'DM Serif Display',serif;font-size:2.4rem;
#                       color:var(--ink);letter-spacing:-.03em;line-height:1.1">
#             📜 DocuMind AI
#           </div>
#           <div style="font-size:13px;color:var(--ink-3);margin-top:6px">
#             AI-Powered Document Intelligence Hub
#           </div>
#         </div>
#         """, unsafe_allow_html=True)

#         with st.expander("⚙️  Backend URL", expanded=False):
#             url = st.text_input("FastAPI URL", value=st.session_state.base_url,
#                                 label_visibility="collapsed", key="auth_url_input")
#             if url != st.session_state.base_url:
#                 st.session_state.base_url = url

#         tab_in, tab_up = st.tabs(["Sign in", "Create account"])

#         # ── LOGIN ──────────────────────────────────────
#         with tab_in:
#             st.markdown("<br>", unsafe_allow_html=True)
#             email = st.text_input("Email address", placeholder="you@lawfirm.com",
#                                   key="li_email")
#             password = st.text_input("Password", type="password",
#                                      placeholder="••••••••", key="li_pw")
#             st.markdown("<br>", unsafe_allow_html=True)

#             if st.button("Sign in →", key="btn_login", use_container_width=True):
#                 if not email or not password:
#                     st.error("Please enter your email and password.")
#                 else:
#                     with st.spinner("Signing in…"):
#                         resp = api(
#                             "POST", "/auth/login",
#                             data={"username": email, "password": password},
#                             headers={"Content-Type": "application/x-www-form-urlencoded"},
#                         )
#                     if resp is None:
#                         st.error("⚠️  Cannot reach backend. Check the URL above.")
#                     elif resp.status_code == 200:
#                         d = resp.json()
#                         st.session_state.token      = d["access_token"]
#                         st.session_state.user_email = email
#                         st.session_state.user_role  = d.get("role", "lawyer")
#                         st.rerun()
#                     else:
#                         try:
#                             st.error(resp.json().get("detail", "Login failed."))
#                         except Exception:
#                             st.error("Login failed.")

#         # ── SIGNUP ─────────────────────────────────────
#         with tab_up:
#             st.markdown("<br>", unsafe_allow_html=True)
#             su_email = st.text_input("Email address", placeholder="priya@legalfirm.in",
#                                      key="su_email")
#             su_pw    = st.text_input("Password", type="password",
#                                      placeholder="Minimum 8 characters", key="su_pw")

#             role_opts = ["lawyer","doctor","researcher","finance","business","admin"]
#             su_role   = st.selectbox(
#                 "Your role",
#                 role_opts,
#                 format_func=lambda r: f"{ROLE_ICONS.get(r,'')}  {r.capitalize()}",
#                 key="su_role",
#             )
#             st.markdown("<br>", unsafe_allow_html=True)

#             if st.button("Create account →", key="btn_signup", use_container_width=True):
#                 if not su_email or not su_pw:
#                     st.error("Please fill in all fields.")
#                 elif len(su_pw) < 8:
#                     st.error("Password must be at least 8 characters.")
#                 else:
#                     with st.spinner("Creating your account…"):
#                         resp = api(
#                             "POST", "/auth/signup",
#                             json={"email": su_email, "password": su_pw, "role": su_role},
#                         )
#                     if resp is None:
#                         st.error("Cannot reach backend.")
#                     elif resp.status_code == 200:
#                         st.success("✓ Account created! Switch to Sign in.")
#                     else:
#                         try:
#                             st.error(resp.json().get("detail", "Signup failed."))
#                         except Exception:
#                             st.error("Signup failed.")


# # ═══════════════════════════════════════════════════════════
# #  PAGE: ASK / RAG
# # ═══════════════════════════════════════════════════════════
# def page_ask():
#     page_header("Ask AI", "RAG Query")

#     role  = st.session_state.user_role or "lawyer"
#     modes = ROLE_MODES.get(role, ["legal"])

#     # Stats
#     c1, c2, c3 = st.columns(3)
#     c1.metric("Endpoint",  "POST /ask")
#     c2.metric("Auth",      "Bearer JWT")
#     c3.metric("Backend",   "Weaviate RAG")

#     section_divider("MODE")

#     mode_labels = [MODE_LABELS.get(m, m) for m in modes]
#     mode_idx = st.radio(
#         "mode_radio", range(len(modes)),
#         format_func=lambda i: mode_labels[i],
#         horizontal=True, label_visibility="collapsed",
#         key="ask_mode_idx",
#     )
#     selected_mode = modes[mode_idx]

#     section_divider("CONVERSATION")

#     # Chat history
#     for entry in st.session_state.chat_history:
#         st.markdown(f'<div class="chat-bubble-user">{entry["q"]}</div>', unsafe_allow_html=True)
#         answer_html = entry["a"].replace("<", "&lt;").replace(">", "&gt;")
#         eval_html = ""
#         if entry.get("eval"):
#             chips = "".join(
#                 f'<span class="eval-chip">{k}: <b>{v:.2f}</b></span>'
#                 if isinstance(v, float)
#                 else f'<span class="eval-chip">{k}: <b>{v}</b></span>'
#                 for k, v in entry["eval"].items()
#             )
#             eval_html = f'<div class="eval-row">{chips}</div>'
#         st.markdown(
#             f'<div class="chat-bubble-ai">{answer_html}{eval_html}</div>',
#             unsafe_allow_html=True,
#         )

#     # Quick chips as buttons in columns
#     st.markdown("<br>", unsafe_allow_html=True)
#     prompts = [
#         "Summarize termination clauses",
#         "List all payment obligations",
#         "Identify liability limitations",
#         "Extract key dates and deadlines",
#     ]
#     qc = st.columns(len(prompts))
#     quick_hit = None
#     for col, prompt in zip(qc, prompts):
#         short = prompt.split(" ", 2)[-1].strip().capitalize()
#         if col.button(short, key=f"qchip_{prompt}"):
#             quick_hit = prompt

#     # Input
#     question = st.text_area(
#         "Question",
#         placeholder="Ask about clauses, obligations, legal terms, or any document insight…",
#         height=90,
#         label_visibility="collapsed",
#         key="ask_question",
#     )

#     col_send, col_clear = st.columns([4, 1])
#     send = col_send.button("Ask AI  ↗", key="btn_ask", use_container_width=True)
#     clear = col_clear.button("Clear", key="btn_clear_chat")

#     if clear:
#         st.session_state.chat_history = []
#         st.rerun()

#     q = quick_hit or (question.strip() if send else None)
#     if q:
#         with st.spinner("Querying RAG backend…"):
#             resp = api(
#                 "POST",
#                 f"/ask?question={requests.utils.quote(q)}&mode={selected_mode}",
#             )
#         if resp is None:
#             st.error("Cannot reach backend.")
#         elif resp.status_code == 200:
#             d = resp.json()
#             st.session_state.chat_history.append({
#                 "q":    q,
#                 "a":    d.get("answer", "No answer returned."),
#                 "eval": d.get("evaluation", {}),
#             })
#             st.rerun()
#         else:
#             try:
#                 st.error(resp.json().get("detail", "Error from backend."))
#             except Exception:
#                 st.error("Error from backend.")


# # ═══════════════════════════════════════════════════════════
# #  PAGE: UPLOAD
# # ═══════════════════════════════════════════════════════════
# def page_upload():
#     page_header("Upload Document", "File Ingestion", "POST", "/upload/file")

#     col_up, col_pipe = st.columns([1.2, 1])

#     with col_up:
#         st.markdown("### Upload")
#         uploaded = st.file_uploader(
#             "Select a file",
#             type=["pdf","docx","txt"],
#             label_visibility="collapsed",
#             key="file_uploader",
#         )
#         if uploaded:
#             st.markdown("<br>", unsafe_allow_html=True)
#             if st.button("Upload & Process  ↗", key="btn_upload", use_container_width=True):
#                 with st.spinner(f"Uploading {uploaded.name}…"):
#                     resp = api(
#                         "POST", "/upload/file",
#                         files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)},
#                     )
#                 if resp is None:
#                     st.error("Cannot reach backend.")
#                 elif resp.status_code == 200:
#                     d = resp.json()
#                     st.success(f"✓  Uploaded — Doc ID: **{d.get('document_id')}**  ·  Domain: **{d.get('domain')}**")
#                     st.session_state.uploaded_docs.append({
#                         "name":   uploaded.name,
#                         "doc_id": d.get("document_id"),
#                         "domain": d.get("domain"),
#                     })
#                 else:
#                     try:
#                         st.error(resp.json().get("detail", "Upload failed."))
#                     except Exception:
#                         st.error("Upload failed.")

#         # Session docs
#         if st.session_state.uploaded_docs:
#             section_divider("THIS SESSION")
#             for doc in reversed(st.session_state.uploaded_docs):
#                 st.markdown(f"""
#                 <div class="file-row">
#                   <div class="file-icon">📄</div>
#                   <div>
#                     <div class="file-name">{doc['name']}</div>
#                     <div class="file-meta">ID: {doc['doc_id']}</div>
#                   </div>
#                   <div class="file-domain">{doc['domain']}</div>
#                 </div>
#                 """, unsafe_allow_html=True)

#     with col_pipe:
#         section_divider("UPLOAD PIPELINE")
#         steps = [
#             ("1", "Save file temporarily to disk"),
#             ("2", "OCR / text extraction"),
#             ("3", "Domain auto-detection"),
#             ("4", "RBAC role vs. domain check"),
#             ("5", "Move to domain folder → PostgreSQL"),
#             ("6", "Ingest into Weaviate for RAG"),
#         ]
#         for num, desc in steps:
#             st.markdown(f"""
#             <div class="pipeline-step">
#               <div class="step-badge">{num}</div>
#               <div>{desc}</div>
#             </div>
#             """, unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════
# #  PAGE: SUMMARIZE
# # ═══════════════════════════════════════════════════════════
# def page_summarize():
#     page_header("Summarize Text", "NLP Extraction", "POST", "/summarize/text")

#     col_l, col_r = st.columns(2, gap="large")

#     with col_l:
#         st.markdown("### Input")
#         text   = st.text_area(
#             "Text to summarize",
#             placeholder="Paste contract text, legal brief, research paper, or any document…",
#             height=240,
#             label_visibility="collapsed",
#             key="sum_text",
#         )
#         method = st.selectbox("Method", ["extractive"], key="sum_method")
#         submit = st.button("Summarize  ↗", key="btn_sum", use_container_width=True)

#     with col_r:
#         st.markdown("### Summary")
#         if submit:
#             if not text.strip():
#                 st.warning("Please enter some text first.")
#             else:
#                 with st.spinner("Summarizing…"):
#                     resp = api(
#                         "POST", "/summarize/text",
#                         json={"text": text, "method": method},
#                     )
#                 if resp is None:
#                     st.error("Cannot reach backend.")
#                 elif resp.status_code == 200:
#                     summary = resp.json().get("summary", "No summary returned.")
#                     result_block(summary)
#                     st.download_button(
#                         "Download summary",
#                         data=summary,
#                         file_name="summary.txt",
#                         mime="text/plain",
#                         key="dl_sum",
#                     )
#                 else:
#                     try:
#                         st.error(resp.json().get("detail", "Summarization failed."))
#                     except Exception:
#                         st.error("Summarization failed.")
#         else:
#             st.markdown("""
#             <div style="height:200px;display:flex;align-items:center;
#                         justify-content:center;border:1px dashed var(--border);
#                         border-radius:8px;color:var(--ink-4);font-size:13px">
#               Summary will appear here
#             </div>
#             """, unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════
# #  PAGE: FORMAT
# # ═══════════════════════════════════════════════════════════
# def page_format():
#     page_header("Format Response", "Output Formatting", "POST", "/format/response")

#     col_l, col_r = st.columns(2, gap="large")

#     with col_l:
#         st.markdown("### Input")
#         text = st.text_area(
#             "Text to format",
#             placeholder="Paste any text or AI response to reformat…",
#             height=240,
#             label_visibility="collapsed",
#             key="fmt_text",
#         )
#         fmt    = st.selectbox("Output format", ["markdown", "json", "plain"], key="fmt_type")
#         submit = st.button("Format  ↗", key="btn_fmt", use_container_width=True)

#     with col_r:
#         st.markdown("### Output")
#         if submit:
#             if not text.strip():
#                 st.warning("Please enter some text first.")
#             else:
#                 with st.spinner("Formatting…"):
#                     resp = api(
#                         "POST", "/format/response",
#                         json={"text": text, "format": fmt},
#                     )
#                 if resp is None:
#                     st.error("Cannot reach backend.")
#                 elif resp.status_code == 200:
#                     result = resp.json().get("formatted_text", "No result.")
#                     lang   = {"markdown": "markdown", "json": "json"}.get(fmt, "text")
#                     st.code(result, language=lang)
#                     st.download_button(
#                         "Download output",
#                         data=result,
#                         file_name=f"formatted.{fmt if fmt != 'plain' else 'txt'}",
#                         key="dl_fmt",
#                     )
#                 else:
#                     try:
#                         st.error(resp.json().get("detail", "Format failed."))
#                     except Exception:
#                         st.error("Format failed.")
#         else:
#             st.markdown("""
#             <div style="height:200px;display:flex;align-items:center;
#                         justify-content:center;border:1px dashed var(--border);
#                         border-radius:8px;color:var(--ink-4);font-size:13px">
#               Formatted output will appear here
#             </div>
#             """, unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════
# #  PAGE: TRANSCRIBE
# # ═══════════════════════════════════════════════════════════
# def page_transcribe():
#     page_header("Transcribe Audio", "Speech-to-Text", "POST", "/transcription/audio")

#     mode = st.radio(
#         "Processing mode",
#         ["Transcribe only", "Transcribe + Summarize + RAG ingest"],
#         horizontal=True,
#         label_visibility="collapsed",
#         key="tr_mode",
#     )
#     endpoint = (
#         "/transcription/audio/process"
#         if "Summarize" in mode
#         else "/transcription/audio"
#     )

#     st.markdown("<br>", unsafe_allow_html=True)
#     audio_file = st.file_uploader(
#         "Select audio",
#         type=["mp3","wav","m4a","ogg"],
#         label_visibility="collapsed",
#         key="audio_uploader",
#     )

#     if audio_file:
#         st.audio(audio_file)
#         st.markdown("<br>", unsafe_allow_html=True)
#         if st.button("Transcribe  ↗", key="btn_tr", use_container_width=True):
#             with st.spinner("Transcribing via Whisper — this may take a moment…"):
#                 resp = api(
#                     "POST", endpoint,
#                     files={"file": (audio_file.name, audio_file.getvalue(), audio_file.type)},
#                 )
#             if resp is None:
#                 st.error("Cannot reach backend.")
#             elif resp.status_code == 200:
#                 d = resp.json()
#                 st.success("✓  Transcription complete!")
#                 if "process" in endpoint:
#                     section_divider("TRANSCRIPT")
#                     result_block(d.get("transcript", "—"))
#                     section_divider("SUMMARY")
#                     result_block(d.get("summary", "—"))
#                 else:
#                     section_divider("TRANSCRIPT")
#                     result_block(d.get("text", "—"))
#             else:
#                 try:
#                     st.error(resp.json().get("detail", "Transcription failed."))
#                 except Exception:
#                     st.error("Transcription failed.")
#     else:
#         st.markdown("""
#         <div style="border:1.5px dashed var(--border-2);border-radius:10px;
#                     padding:40px;text-align:center;margin-top:12px">
#           <div style="font-size:28px;margin-bottom:10px">🎙</div>
#           <div style="font-size:14px;font-weight:500;color:var(--ink)">
#             Drop an audio file to transcribe
#           </div>
#           <div style="font-size:12px;color:var(--ink-3);margin-top:4px">
#             MP3, WAV, M4A — processed by OpenAI Whisper
#           </div>
#         </div>
#         """, unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════
# #  PAGE: JWT TOKEN
# # ═══════════════════════════════════════════════════════════
# def page_token():
#     page_header("JWT Token", "Authentication", "—", "HS256 · Bearer")

#     token = st.session_state.token or ""

#     section_divider("ACCESS TOKEN")
#     if token:
#         st.markdown(f'<div class="token-block">{token}</div>', unsafe_allow_html=True)
#         st.code(f"Authorization: Bearer {token}", language="bash")

#         col_copy, _ = st.columns([1, 3])
#         col_copy.download_button(
#             "Download token",
#             data=token,
#             file_name="jwt_token.txt",
#             mime="text/plain",
#             key="dl_token",
#         )

#         # Decoded payload
#         payload = decode_jwt(token)
#         if payload:
#             section_divider("DECODED PAYLOAD")
#             cols = st.columns(min(len(payload), 3))
#             for i, (k, v) in enumerate(payload.items()):
#                 display = str(v)
#                 if k in ("exp", "iat"):
#                     try:
#                         display = datetime.utcfromtimestamp(v).strftime("%d %b %Y · %H:%M UTC")
#                     except Exception:
#                         pass
#                 cols[i % len(cols)].metric(k, display)

#             # Expiry check
#             if "exp" in payload:
#                 remaining = payload["exp"] - datetime.utcnow().timestamp()
#                 if remaining > 0:
#                     mins = int(remaining // 60)
#                     st.info(f"⏱  Token expires in **{mins} minutes**.")
#                 else:
#                     st.error("⚠️  Token has expired. Please sign in again.")
#     else:
#         st.warning("No token in session. Please sign in first.")

#     section_divider("USAGE")
#     st.code(
#         'curl -H "Authorization: Bearer <your_token>" \\\n'
#         '     -X POST http://localhost:8000/ask?question=hello&mode=legal',
#         language="bash",
#     )


# # ═══════════════════════════════════════════════════════════
# #  PAGE: ADMIN
# # ═══════════════════════════════════════════════════════════
# def page_admin():
#     page_header("Admin Panel", "User Management", "GET", "/admin/users")

#     col_hdr, col_btn = st.columns([5, 1])
#     col_hdr.markdown("### All registered users")
#     if col_btn.button("↻  Refresh", key="adm_refresh"):
#         st.session_state.admin_users = None

#     if st.session_state.admin_users is None:
#         with st.spinner("Loading users…"):
#             resp = api("GET", "/admin/users")
#         if resp is None:
#             st.error("Cannot reach backend.")
#             return
#         if resp.status_code == 200:
#             st.session_state.admin_users = resp.json()
#         else:
#             try:
#                 st.error(resp.json().get("detail", "Failed to load users."))
#             except Exception:
#                 st.error("Failed to load users.")
#             return

#     users = st.session_state.admin_users or []
#     if not users:
#         st.info("No users found.")
#         return

#     section_divider(f"{len(users)} USER{'S' if len(users) != 1 else ''}")

#     for user in users:
#         initials = user["email"][0].upper()
#         role     = user.get("role", "user")
#         col_av, col_info, col_role, col_del = st.columns([0.5, 3, 1.5, 1])

#         col_av.markdown(f"""
#         <div class="user-avatar" style="margin-top:4px">{initials}</div>
#         """, unsafe_allow_html=True)

#         col_info.markdown(f"""
#         <div class="user-email-txt">{user['email']}</div>
#         <div class="user-id">ID #{user['id']}</div>
#         """, unsafe_allow_html=True)

#         col_role.markdown(f"""
#         <div style="margin-top:8px">
#           <span class="role-badge rb-{role}">{role}</span>
#         </div>
#         """, unsafe_allow_html=True)

#         if col_del.button("Delete", key=f"del_{user['id']}"):
#             resp = api("DELETE", f"/admin/users/{user['id']}")
#             if resp and resp.status_code == 200:
#                 st.success(f"Deleted {user['email']}")
#                 st.session_state.admin_users = [
#                     u for u in users if u["id"] != user["id"]
#                 ]
#                 st.rerun()
#             else:
#                 st.error("Delete failed.")

#         st.markdown("<hr style='margin:6px 0;border-color:var(--border)'>", unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════
# #  ROUTER
# # ═══════════════════════════════════════════════════════════
# PAGE_MAP = {
#     "ask":        page_ask,
#     "upload":     page_upload,
#     "summarize":  page_summarize,
#     "format":     page_format,
#     "transcribe": page_transcribe,
#     "token":      page_token,
#     "admin":      page_admin,
# }

# def main():
#     if not st.session_state.token:
#         render_auth()
#     else:
#         render_sidebar()
#         page_fn = PAGE_MAP.get(st.session_state.page, page_ask)
#         page_fn()

# if __name__ == "__main__":
#     main()


"""
DocuMind AI — Streamlit UI
Run: streamlit run ui_app.py
Deps: pip install streamlit requests
"""

import streamlit as st
import requests
import json
import base64
from datetime import datetime

# ── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

:root {
  --cream:       #F7F4EF;
  --parchment:   #EDE8DF;
  --warm-white:  #FAF8F5;
  --ink:         #1A1714;
  --ink-2:       #4A4540;
  --ink-3:       #8A8480;
  --ink-4:       #B8B4B0;
  --accent:      #2D5A3D;
  --accent-light:#E8F0EA;
  --accent-2:    #8B4513;
  --gold:        #C49A3C;
  --gold-lt:     #FDF4E3;
  --border:      #DDD8D0;
  --border-2:    #C8C2B8;
  --danger:      #8B2020;
  --danger-lt:   #FDF0F0;
  --shadow:      0 1px 3px rgba(26,23,20,.08), 0 4px 16px rgba(26,23,20,.06);
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  background-color: var(--cream) !important;
  color: var(--ink) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem !important; max-width: 100% !important; }

/* SIDEBAR */
[data-testid="stSidebar"] { background: var(--ink) !important; border-right: none !important; }
[data-testid="stSidebar"] * { color: var(--ink-4) !important; }
[data-testid="stSidebarContent"] { padding: 0 !important; }
[data-testid="stSidebar"] .stButton > button {
  background: transparent !important; color: var(--ink-4) !important;
  border: none !important; border-radius: 6px !important; text-align: left !important;
  font-size: 13px !important; font-weight: 400 !important; padding: 8px 12px !important;
  width: 100% !important; justify-content: flex-start !important; letter-spacing: 0 !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(255,255,255,.07) !important; color: #fff !important;
  transform: none !important; box-shadow: none !important;
}

/* TYPOGRAPHY */
h1 { font-family:'DM Serif Display',serif !important; font-size:2rem !important; font-weight:400 !important; color:var(--ink) !important; letter-spacing:-.02em !important; line-height:1.15 !important; }
h2 { font-family:'DM Serif Display',serif !important; font-size:1.35rem !important; font-weight:400 !important; color:var(--ink) !important; }
h3 { font-family:'DM Sans',sans-serif !important; font-size:.75rem !important; font-weight:600 !important; color:var(--ink-3) !important; letter-spacing:.1em !important; text-transform:uppercase !important; }

/* BUTTONS */
.stButton > button {
  background: var(--ink) !important; color: var(--cream) !important; border: none !important;
  border-radius: 6px !important; font-family:'DM Sans',sans-serif !important;
  font-size: 13px !important; font-weight: 500 !important; padding: 9px 20px !important;
  letter-spacing: .01em !important; transition: background .15s, transform .15s !important; box-shadow: none !important;
}
.stButton > button:hover { background: var(--accent) !important; transform: translateY(-1px) !important; }
.stButton > button:disabled { opacity: .4 !important; }

/* INPUTS */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stNumberInput > div > div > input {
  background: var(--warm-white) !important; border: 1px solid var(--border) !important;
  border-radius: 6px !important; color: var(--ink) !important;
  font-family:'DM Sans',sans-serif !important; font-size: 13px !important; box-shadow: none !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(45,90,61,.1) !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1.5px solid var(--border) !important; gap: 0 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: var(--ink-3) !important; font-family:'DM Sans',sans-serif !important; font-size: 13px !important; font-weight: 500 !important; padding: 10px 20px !important; border-bottom: 2px solid transparent !important; border-radius: 0 !important; }
.stTabs [aria-selected="true"] { color: var(--accent) !important; border-bottom-color: var(--accent) !important; }

/* FILE UPLOADER */
[data-testid="stFileUploader"] { background: var(--warm-white) !important; border: 1.5px dashed var(--border-2) !important; border-radius: 10px !important; padding: 20px !important; }

/* METRICS */
[data-testid="stMetric"] { background: var(--warm-white) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; padding: 14px 16px !important; box-shadow: var(--shadow) !important; }
[data-testid="stMetricLabel"] { font-size: 10px !important; font-weight: 600 !important; color: var(--ink-3) !important; text-transform: uppercase !important; letter-spacing: .08em !important; }
[data-testid="stMetricValue"] { font-family:'DM Serif Display',serif !important; font-size: 1.5rem !important; color: var(--ink) !important; }

/* EXPANDER */
[data-testid="stExpander"] { border: 1px solid var(--border) !important; border-radius: 8px !important; background: var(--warm-white) !important; box-shadow: none !important; }

/* ALERTS */
.stSuccess, .stInfo, .stWarning, .stError { border-radius: 6px !important; font-size: 13px !important; }
hr { border-color: var(--border) !important; margin: 16px 0 !important; }

/* RADIO */
.stRadio > div { flex-direction: row !important; gap: 16px; }
.stRadio label { font-size: 13px !important; color: var(--ink-2) !important; }

/* LABELS */
.stSelectbox label, .stTextArea label, .stTextInput label, .stFileUploader label {
  font-size: 11px !important; font-weight: 600 !important; color: var(--ink-3) !important;
  text-transform: uppercase !important; letter-spacing: .07em !important;
}

/* CUSTOM COMPONENTS */
.doc-topbar {
  background: var(--warm-white); border-bottom: 1px solid var(--border);
  padding: 14px 24px; display: flex; align-items: center;
  justify-content: space-between; margin: 0 -2rem 1.5rem;
  position: sticky; top: 0; z-index: 99;
}
.page-kicker { font-size: 10px; font-weight: 600; color: var(--ink-3); letter-spacing: .12em; text-transform: uppercase; margin-bottom: 4px; }
.endpoint-pill { display: inline-flex; align-items: center; gap: 6px; background: var(--parchment); border: 1px solid var(--border); border-radius: 999px; padding: 4px 12px; font-family:'DM Mono',monospace; font-size: 11px; color: var(--ink-2); }
.method-tag { font-size: 9px; font-weight: 700; padding: 2px 5px; border-radius: 3px; background: var(--accent); color: #fff; letter-spacing: .04em; }
.method-get { background: var(--accent-2) !important; }
.method-delete { background: var(--danger) !important; }

.chat-bubble-user { background: var(--parchment); border: 1px solid var(--border); border-radius: 12px 12px 4px 12px; padding: 12px 16px; font-size: 14px; color: var(--ink); line-height: 1.6; margin-bottom: 4px; max-width: 85%; margin-left: auto; }
.chat-bubble-ai { background: var(--warm-white); border: 1px solid var(--border); border-left: 3px solid var(--accent); border-radius: 4px 12px 12px 12px; padding: 14px 16px; font-size: 14px; color: var(--ink-2); line-height: 1.7; margin-bottom: 4px; max-width: 90%; }
.eval-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--border); }
.eval-chip { background: var(--parchment); border: 1px solid var(--border); border-radius: 999px; padding: 3px 10px; font-family:'DM Mono',monospace; font-size: 11px; color: var(--ink-2); }
.eval-chip b { color: var(--accent); }

.result-block { background: var(--warm-white); border: 1px solid var(--border); border-left: 3px solid var(--gold); border-radius: 8px; padding: 16px 18px; font-size: 13px; line-height: 1.8; color: var(--ink-2); font-family:'DM Sans',sans-serif; white-space: pre-wrap; margin-top: 12px; }
.token-block { background: var(--ink); border-radius: 8px; padding: 16px 18px; font-family:'DM Mono',monospace; font-size: 11.5px; color: #A8D5A2; word-break: break-all; line-height: 1.7; margin: 10px 0; }

.file-row { display: flex; align-items: center; gap: 12px; background: var(--warm-white); border: 1px solid var(--border); border-radius: 8px; padding: 12px 14px; margin-bottom: 8px; }
.file-icon { font-size: 22px; }
.file-name { font-size: 13px; font-weight: 500; color: var(--ink); }
.file-meta { font-size: 11px; color: var(--ink-3); margin-top: 2px; }
.file-domain { margin-left: auto; background: var(--accent-light); border: 1px solid rgba(45,90,61,.2); color: var(--accent); padding: 3px 10px; border-radius: 999px; font-size: 11px; font-weight: 600; }

.pipeline-step { display: flex; align-items: flex-start; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--border); font-size: 13px; color: var(--ink-2); }
.pipeline-step:last-child { border-bottom: none; }
.step-badge { min-width: 22px; height: 22px; border-radius: 50%; background: var(--parchment); border: 1px solid var(--border-2); color: var(--ink-3); display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; flex-shrink: 0; margin-top: 1px; }

.user-card { display: flex; align-items: center; gap: 14px; background: var(--warm-white); border: 1px solid var(--border); border-radius: 8px; padding: 12px 16px; margin-bottom: 6px; }
.user-avatar { width: 34px; height: 34px; border-radius: 50%; background: var(--parchment); border: 1px solid var(--border-2); display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600; color: var(--ink-2); flex-shrink: 0; }
.user-id { font-family:'DM Mono',monospace; font-size: 10px; color: var(--ink-4); }
.user-email-txt { font-size: 13px; color: var(--ink); font-weight: 500; }
.role-badge { margin-left: auto; padding: 3px 10px; border-radius: 999px; font-size: 10px; font-weight: 700; letter-spacing: .05em; text-transform: uppercase; }
.rb-lawyer     { background: #E8F0F8; color: #2B5E8A; }
.rb-doctor     { background: #E8F4EE; color: #2B6B44; }
.rb-researcher { background: #F4E8F5; color: #6B2B8A; }
.rb-finance    { background: #FDF4E3; color: #7A5A1A; }
.rb-business   { background: #F5F4EF; color: #5A5040; }
.rb-admin      { background: #FDF0F0; color: #8B2020; }

.section-divider { display: flex; align-items: center; gap: 12px; margin: 20px 0 16px; }
.section-divider-line { flex: 1; height: 1px; background: var(--border); }
.section-divider-text { font-size: 10px; font-weight: 600; color: var(--ink-4); letter-spacing: .1em; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  ROLE CONFIG — single source of truth
#  Add/edit roles here; everything else adapts automatically
# ═══════════════════════════════════════════════════════════
ROLE_CONFIG = {
    "lawyer": {
        "icon":        "⚖️",
        "label":       "Lawyer",
        "mode":        "legal",
        "mode_label":  "⚖️ Legal",
        "placeholder": "Ask about clauses, obligations, jurisdiction, liability, or any legal term…",
        "quick_chips": [
            "Summarize termination clauses",
            "List all payment obligations",
            "Identify liability limitations",
            "Extract key dates and deadlines",
        ],
        "badge_css":   "rb-lawyer",
    },
    "doctor": {
        "icon":        "🩺",
        "label":       "Doctor",
        "mode":        "healthcare",
        "mode_label":  "🩺 Healthcare",
        "placeholder": "Ask about patient history, diagnoses, treatment plans, or medical reports…",
        "quick_chips": [
            "Summarize patient history",
            "List prescribed medications",
            "Extract diagnoses",
            "Identify treatment recommendations",
        ],
        "badge_css":   "rb-doctor",
    },
    "researcher": {
        "icon":        "🔬",
        "label":       "Researcher",
        "mode":        "academic",
        "mode_label":  "🔬 Academic",
        "placeholder": "Ask about research findings, methodologies, citations, or paper summaries…",
        "quick_chips": [
            "Summarize key findings",
            "List research methodologies",
            "Extract citations",
            "Identify research gaps",
        ],
        "badge_css":   "rb-researcher",
    },
    "finance": {
        "icon":        "📊",
        "label":       "Analyst",
        "mode":        "finance",
        "mode_label":  "📊 Finance",
        "placeholder": "Ask about financial terms, loan policies, credit risk, or bank reports…",
        "quick_chips": [
            "Summarize loan terms",
            "List interest rate clauses",
            "Extract risk indicators",
            "Identify repayment obligations",
        ],
        "badge_css":   "rb-finance",
    },
    "business": {
        "icon":        "🏢",
        "label":       "Manager",
        "mode":        "business",
        "mode_label":  "🏢 Business",
        "placeholder": "Ask about meeting action items, decisions, project updates, or business reports…",
        "quick_chips": [
            "Extract action items",
            "List key decisions made",
            "Summarize meeting notes",
            "Identify open blockers",
        ],
        "badge_css":   "rb-business",
    },
    "admin": {
        "icon":        "🛡️",
        "label":       "Admin",
        "mode":        "general",
        "mode_label":  "🛡️ All Modes",
        "placeholder": "Ask anything across all domains — legal, medical, academic, finance, or business…",
        "quick_chips": [
            "Summarize this document",
            "Extract key entities",
            "List all obligations",
            "Identify critical dates",
        ],
        "badge_css":   "rb-admin",
    },
}

# Admin can access all modes
ALL_MODES = {
    "legal":      "⚖️ Legal",
    "healthcare": "🩺 Healthcare",
    "academic":   "🔬 Academic",
    "finance":    "📊 Finance",
    "business":   "🏢 Business",
}

ROLE_ICONS = {r: cfg["icon"] for r, cfg in ROLE_CONFIG.items()}


def get_role_cfg(role: str) -> dict:
    """Return config for a role, falling back to a safe default."""
    return ROLE_CONFIG.get(role, ROLE_CONFIG["admin"])


def get_available_modes(role: str) -> dict:
    """Return {mode_key: label} dict available to this role."""
    if role == "admin":
        return ALL_MODES
    cfg = get_role_cfg(role)
    key = cfg["mode"]
    return {key: cfg["mode_label"]}


# ═══════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "token":        None,
        "user_email":   None,
        "user_role":    None,
        "base_url":     "http://localhost:8000",
        "chat_history": [],
        "uploaded_docs":[],
        "page":         "ask",
        "admin_users":  None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ═══════════════════════════════════════════════════════════
#  API WRAPPER
# ═══════════════════════════════════════════════════════════
def api(method: str, path: str, **kwargs):
    base    = st.session_state.base_url.rstrip("/")
    headers = kwargs.pop("headers", {})
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    try:
        return requests.request(method, f"{base}{path}", headers=headers, timeout=60, **kwargs)
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        st.error(f"Request error: {e}")
        return None


def decode_jwt(token: str) -> dict:
    try:
        parts  = token.split(".")
        padded = parts[1] + "=" * (4 - len(parts[1]) % 4)
        return json.loads(base64.urlsafe_b64decode(padded))
    except Exception:
        return {}


# ═══════════════════════════════════════════════════════════
#  SHARED UI HELPERS
# ═══════════════════════════════════════════════════════════
def page_header(title: str, kicker: str, method: str, endpoint: str):
    method_class = {
        "POST":   "method-tag",
        "GET":    "method-tag method-get",
        "DELETE": "method-tag method-delete",
    }.get(method, "method-tag")
    st.markdown(f"""
    <div class="doc-topbar">
      <div>
        <div class="page-kicker">{kicker}</div>
        <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;
                    color:var(--ink);line-height:1.2">{title}</div>
      </div>
      <div class="endpoint-pill">
        <span class="{method_class}">{method}</span>
        {endpoint}
      </div>
    </div>
    """, unsafe_allow_html=True)


def section_divider(label: str):
    st.markdown(f"""
    <div class="section-divider">
      <div class="section-divider-line"></div>
      <div class="section-divider-text">{label}</div>
      <div class="section-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)


def result_block(content: str):
    safe = content.replace("<", "&lt;").replace(">", "&gt;")
    st.markdown(f'<div class="result-block">{safe}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════
def render_sidebar():
    role  = st.session_state.user_role  or "admin"
    email = st.session_state.user_email or "—"
    cfg   = get_role_cfg(role)
    icon  = cfg["icon"]
    label = cfg["label"]

    with st.sidebar:
        st.markdown(f"""
        <div style="padding:20px 18px 16px;border-bottom:1px solid rgba(255,255,255,.08)">
          <div style="font-family:'DM Serif Display',serif;font-size:20px;
                      font-weight:400;color:#FAF8F5;letter-spacing:-.02em;
                      margin-bottom:14px">📜 DocuMind AI</div>
          <div style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);
                      border-radius:8px;padding:10px 12px;display:flex;align-items:center;gap:10px">
            <div style="width:28px;height:28px;border-radius:50%;
                        background:rgba(255,255,255,.12);color:#FAF8F5;
                        display:flex;align-items:center;justify-content:center;
                        font-size:13px;flex-shrink:0">{icon}</div>
            <div style="min-width:0">
              <div style="font-size:11px;color:rgba(255,255,255,.5);
                          overflow:hidden;text-overflow:ellipsis;
                          white-space:nowrap;max-width:130px">{email}</div>
              <div style="font-size:9px;font-weight:700;letter-spacing:.07em;
                          color:#C49A3C;text-transform:uppercase;margin-top:2px">{label}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="padding:10px 8px">', unsafe_allow_html=True)

        nav_items = [
            ("💬", "Ask AI (RAG)",     "ask"),
            ("📁", "Upload Document",  "upload"),
            ("📝", "Summarize",        "summarize"),
            ("🔧", "Format Response",  "format"),
            ("🎙", "Transcribe Audio", "transcribe"),
            ("🔑", "JWT Token",        "token"),
        ]
        if role == "admin":
            nav_items.append(("🛡️", "Admin Panel", "admin"))

        for ico, lbl, key in nav_items:
            if st.session_state.page == key:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,.12);border-radius:6px;
                            padding:8px 12px;margin-bottom:2px;display:flex;
                            align-items:center;gap:8px">
                  <span style="font-size:14px">{ico}</span>
                  <span style="font-size:13px;color:#FAF8F5;font-weight:500">{lbl}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"{ico}  {lbl}", key=f"nav_{key}", use_container_width=True):
                    st.session_state.page = key
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="padding:0 8px 8px;border-top:1px solid rgba(255,255,255,.06);margin-top:auto">', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("⚙️ Backend", expanded=False):
            url = st.text_input("URL", value=st.session_state.base_url,
                                label_visibility="collapsed", key="sidebar_url")
            if url != st.session_state.base_url:
                st.session_state.base_url = url

        if st.button("↩  Sign out", key="logout", use_container_width=True):
            for k in ["token","user_email","user_role","admin_users"]:
                st.session_state[k] = None
            st.session_state.chat_history  = []
            st.session_state.uploaded_docs = []
            st.session_state.page = "ask"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  AUTH
# ═══════════════════════════════════════════════════════════
def render_auth():
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;margin-bottom:28px">
          <div style="font-family:'DM Serif Display',serif;font-size:2.4rem;
                      color:var(--ink);letter-spacing:-.03em;line-height:1.1">
            📜 DocuMind AI
          </div>
          <div style="font-size:13px;color:var(--ink-3);margin-top:6px">
            AI-Powered Document Intelligence Hub
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("⚙️  Backend URL", expanded=False):
            url = st.text_input("FastAPI URL", value=st.session_state.base_url,
                                label_visibility="collapsed", key="auth_url_input")
            if url != st.session_state.base_url:
                st.session_state.base_url = url

        tab_in, tab_up = st.tabs(["Sign in", "Create account"])

        # ── LOGIN ──────────────────────────────────────
        with tab_in:
            st.markdown("<br>", unsafe_allow_html=True)
            email    = st.text_input("Email address", placeholder="you@organisation.com", key="li_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="li_pw")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Sign in →", key="btn_login", use_container_width=True):
                if not email or not password:
                    st.error("Please enter your email and password.")
                else:
                    with st.spinner("Signing in…"):
                        resp = api(
                            "POST", "/auth/login",
                            data={"username": email, "password": password},
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                        )
                    if resp is None:
                        st.error("⚠️  Cannot reach backend. Check the URL above.")
                    elif resp.status_code == 200:
                        d = resp.json()
                        st.session_state.token      = d["access_token"]
                        st.session_state.user_email = email
                        # Role comes from the backend response
                        st.session_state.user_role  = d.get("role", "admin")
                        st.rerun()
                    else:
                        try:    st.error(resp.json().get("detail", "Login failed."))
                        except: st.error("Login failed.")

        # ── SIGNUP ─────────────────────────────────────
        with tab_up:
            st.markdown("<br>", unsafe_allow_html=True)
            su_email = st.text_input("Email address", placeholder="priya@organisation.com", key="su_email")
            su_pw    = st.text_input("Password", type="password", placeholder="Minimum 8 characters", key="su_pw")

            # Role picker with icon + label
            role_keys = list(ROLE_CONFIG.keys())
            su_role   = st.selectbox(
                "Your role",
                role_keys,
                format_func=lambda r: f"{ROLE_CONFIG[r]['icon']}  {ROLE_CONFIG[r]['label']}",
                key="su_role",
            )

            # Live preview of what this role unlocks
            preview_modes = get_available_modes(su_role)
            mode_str = "  ·  ".join(preview_modes.values())
            st.markdown(
                f'<p style="font-size:11px;color:var(--accent);margin-top:4px">'
                f'Unlocks: {mode_str}</p>',
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Create account →", key="btn_signup", use_container_width=True):
                if not su_email or not su_pw:
                    st.error("Please fill in all fields.")
                elif len(su_pw) < 8:
                    st.error("Password must be at least 8 characters.")
                else:
                    with st.spinner("Creating your account…"):
                        resp = api(
                            "POST", "/auth/signup",
                            json={"email": su_email, "password": su_pw, "role": su_role},
                        )
                    if resp is None:
                        st.error("Cannot reach backend.")
                    elif resp.status_code == 200:
                        st.success("✓ Account created! Switch to Sign in.")
                    else:
                        try:    st.error(resp.json().get("detail", "Signup failed."))
                        except: st.error("Signup failed.")


# ═══════════════════════════════════════════════════════════
#  PAGE: ASK / RAG  (fully role-aware)
# ═══════════════════════════════════════════════════════════
def page_ask():
    role = st.session_state.user_role or "admin"
    cfg  = get_role_cfg(role)

    page_header("Ask AI", f"{cfg['mode_label']} · RAG Query", "POST", "/ask")

    # Stats row
    c1, c2, c3 = st.columns(3)
    c1.metric("Mode",    cfg["mode_label"])
    c2.metric("Auth",    "Bearer JWT")
    c3.metric("Backend", "Weaviate RAG")

    available_modes = get_available_modes(role)

    # Mode selector — admins see all, others see only their mode
    if len(available_modes) > 1:
        section_divider("SELECT MODE")
        mode_keys   = list(available_modes.keys())
        mode_labels = list(available_modes.values())
        mode_idx    = st.radio(
            "mode_radio", range(len(mode_keys)),
            format_func=lambda i: mode_labels[i],
            horizontal=True, label_visibility="collapsed",
            key="ask_mode_idx",
        )
        selected_mode = mode_keys[mode_idx]
        # For admin, use per-mode config chips/placeholder if exists
        active_cfg = next(
            (c for c in ROLE_CONFIG.values() if c["mode"] == selected_mode),
            cfg,
        )
    else:
        selected_mode = cfg["mode"]
        active_cfg    = cfg

    section_divider("CONVERSATION")

    # Chat history
    for entry in st.session_state.chat_history:
        st.markdown(f'<div class="chat-bubble-user">{entry["q"]}</div>', unsafe_allow_html=True)
        answer_html = entry["a"].replace("<", "&lt;").replace(">", "&gt;")
        eval_html   = ""
        if entry.get("eval"):
            chips = "".join(
                f'<span class="eval-chip">{k}: <b>{v:.2f}</b></span>'
                if isinstance(v, float)
                else f'<span class="eval-chip">{k}: <b>{v}</b></span>'
                for k, v in entry["eval"].items()
            )
            eval_html = f'<div class="eval-row">{chips}</div>'
        st.markdown(
            f'<div class="chat-bubble-ai">{answer_html}{eval_html}</div>',
            unsafe_allow_html=True,
        )

    # Quick chips — driven by active role/mode config
    st.markdown("<br>", unsafe_allow_html=True)
    chips   = active_cfg["quick_chips"]
    qcols   = st.columns(len(chips))
    quick_hit = None
    for col, prompt in zip(qcols, chips):
        short = " ".join(prompt.split()[1:3]).capitalize()
        if col.button(short, key=f"qchip_{prompt}"):
            quick_hit = prompt

    # Input
    question = st.text_area(
        "Question",
        placeholder=active_cfg["placeholder"],
        height=90,
        label_visibility="collapsed",
        key="ask_question",
    )

    col_send, col_clear = st.columns([4, 1])
    send  = col_send.button("Ask AI  ↗", key="btn_ask", use_container_width=True)
    clear = col_clear.button("Clear", key="btn_clear_chat")

    if clear:
        st.session_state.chat_history = []
        st.rerun()

    q = quick_hit or (question.strip() if send else None)
    if q:
        with st.spinner("Querying RAG backend…"):
            resp = api(
                "POST",
                f"/ask?question={requests.utils.quote(q)}&mode={selected_mode}",
            )
        if resp is None:
            st.error("Cannot reach backend.")
        elif resp.status_code == 200:
            d = resp.json()
            st.session_state.chat_history.append({
                "q":    q,
                "a":    d.get("answer", "No answer returned."),
                "eval": d.get("evaluation", {}),
            })
            st.rerun()
        else:
            try:    st.error(resp.json().get("detail", "Error from backend."))
            except: st.error("Error from backend.")


# ═══════════════════════════════════════════════════════════
#  PAGE: UPLOAD
# ═══════════════════════════════════════════════════════════
def page_upload():
    page_header("Upload Document", "File Ingestion", "POST", "/upload/file")

    col_up, col_pipe = st.columns([1.2, 1])

    with col_up:
        st.markdown("### Upload")
        uploaded = st.file_uploader(
            "Select a file",
            type=["pdf","docx","png","jpg","jpeg","mp3","wav","txt"],
            label_visibility="collapsed",
            key="file_uploader",
        )
        if uploaded:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Upload & Process  ↗", key="btn_upload", use_container_width=True):
                with st.spinner(f"Uploading {uploaded.name}…"):
                    resp = api(
                        "POST", "/upload/file",
                        files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)},
                    )
                if resp is None:
                    st.error("Cannot reach backend.")
                elif resp.status_code == 200:
                    d = resp.json()
                    st.success(f"✓  Uploaded — Doc ID: **{d.get('document_id')}**  ·  Domain: **{d.get('domain')}**")
                    st.session_state.uploaded_docs.append({
                        "name":   uploaded.name,
                        "doc_id": d.get("document_id"),
                        "domain": d.get("domain"),
                    })
                else:
                    try:    st.error(resp.json().get("detail", "Upload failed."))
                    except: st.error("Upload failed.")

        if st.session_state.uploaded_docs:
            section_divider("THIS SESSION")
            for doc in reversed(st.session_state.uploaded_docs):
                st.markdown(f"""
                <div class="file-row">
                  <div class="file-icon">📄</div>
                  <div>
                    <div class="file-name">{doc['name']}</div>
                    <div class="file-meta">ID: {doc['doc_id']}</div>
                  </div>
                  <div class="file-domain">{doc['domain']}</div>
                </div>
                """, unsafe_allow_html=True)

    with col_pipe:
        section_divider("UPLOAD PIPELINE")
        steps = [
            ("1", "Save file temporarily to disk"),
            ("2", "OCR / text extraction"),
            ("3", "Domain auto-detection"),
            ("4", "RBAC role vs. domain check"),
            ("5", "Move to domain folder → PostgreSQL"),
            ("6", "Ingest into Weaviate for RAG"),
        ]
        for num, desc in steps:
            st.markdown(f"""
            <div class="pipeline-step">
              <div class="step-badge">{num}</div>
              <div>{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  PAGE: SUMMARIZE
# ═══════════════════════════════════════════════════════════
def page_summarize():
    page_header("Summarize Text", "NLP Extraction", "POST", "/summarize/text")

    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown("### Input")
        role = st.session_state.user_role or "admin"
        cfg  = get_role_cfg(role)
        text = st.text_area(
            "Text to summarize",
            placeholder=f"Paste your {cfg['label'].lower()} document here…",
            height=240,
            label_visibility="collapsed",
            key="sum_text",
        )
        method = st.selectbox("Method", ["extractive", "abstractive"], key="sum_method")
        submit = st.button("Summarize  ↗", key="btn_sum", use_container_width=True)

    with col_r:
        st.markdown("### Summary")
        if submit:
            if not text.strip():
                st.warning("Please enter some text first.")
            else:
                with st.spinner("Summarizing…"):
                    resp = api("POST", "/summarize/text", json={"text": text, "method": method})
                if resp is None:
                    st.error("Cannot reach backend.")
                elif resp.status_code == 200:
                    summary = resp.json().get("summary", "No summary returned.")
                    result_block(summary)
                    st.download_button("Download summary", data=summary, file_name="summary.txt", mime="text/plain", key="dl_sum")
                else:
                    try:    st.error(resp.json().get("detail", "Summarization failed."))
                    except: st.error("Summarization failed.")
        else:
            st.markdown("""
            <div style="height:200px;display:flex;align-items:center;justify-content:center;
                        border:1px dashed var(--border);border-radius:8px;
                        color:var(--ink-4);font-size:13px">Summary will appear here</div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  PAGE: FORMAT
# ═══════════════════════════════════════════════════════════
def page_format():
    page_header("Format Response", "Output Formatting", "POST", "/format/response")

    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown("### Input")
        text   = st.text_area("Text to format", placeholder="Paste any text or AI response to reformat…", height=240, label_visibility="collapsed", key="fmt_text")
        fmt    = st.selectbox("Output format", ["markdown","json","plain"], key="fmt_type")
        submit = st.button("Format  ↗", key="btn_fmt", use_container_width=True)

    with col_r:
        st.markdown("### Output")
        if submit:
            if not text.strip():
                st.warning("Please enter some text first.")
            else:
                with st.spinner("Formatting…"):
                    resp = api("POST", "/format/response", json={"text": text, "format": fmt})
                if resp is None:
                    st.error("Cannot reach backend.")
                elif resp.status_code == 200:
                    result = resp.json().get("formatted_text", "No result.")
                    lang   = {"markdown":"markdown","json":"json"}.get(fmt, "text")
                    st.code(result, language=lang)
                    st.download_button("Download output", data=result,
                                       file_name=f"formatted.{fmt if fmt != 'plain' else 'txt'}",
                                       key="dl_fmt")
                else:
                    try:    st.error(resp.json().get("detail", "Format failed."))
                    except: st.error("Format failed.")
        else:
            st.markdown("""
            <div style="height:200px;display:flex;align-items:center;justify-content:center;
                        border:1px dashed var(--border);border-radius:8px;
                        color:var(--ink-4);font-size:13px">Formatted output will appear here</div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  PAGE: TRANSCRIBE
# ═══════════════════════════════════════════════════════════
def page_transcribe():
    page_header("Transcribe Audio", "Speech-to-Text", "POST", "/transcription/audio")

    mode = st.radio(
        "Processing mode",
        ["Transcribe only", "Transcribe + Summarize + RAG ingest"],
        horizontal=True, label_visibility="collapsed", key="tr_mode",
    )
    endpoint = "/transcription/audio/process" if "Summarize" in mode else "/transcription/audio"

    st.markdown("<br>", unsafe_allow_html=True)
    audio_file = st.file_uploader("Select audio", type=["mp3","wav","m4a","ogg"],
                                  label_visibility="collapsed", key="audio_uploader")

    if audio_file:
        st.audio(audio_file)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Transcribe  ↗", key="btn_tr", use_container_width=True):
            with st.spinner("Transcribing via Whisper — this may take a moment…"):
                resp = api("POST", endpoint,
                           files={"file": (audio_file.name, audio_file.getvalue(), audio_file.type)})
            if resp is None:
                st.error("Cannot reach backend.")
            elif resp.status_code == 200:
                d = resp.json()
                st.success("✓  Transcription complete!")
                if "process" in endpoint:
                    section_divider("TRANSCRIPT")
                    result_block(d.get("transcript", "—"))
                    section_divider("SUMMARY")
                    result_block(d.get("summary", "—"))
                else:
                    section_divider("TRANSCRIPT")
                    result_block(d.get("text", "—"))
            else:
                try:    st.error(resp.json().get("detail", "Transcription failed."))
                except: st.error("Transcription failed.")
    else:
        st.markdown("""
        <div style="border:1.5px dashed var(--border-2);border-radius:10px;
                    padding:40px;text-align:center;margin-top:12px">
          <div style="font-size:28px;margin-bottom:10px">🎙</div>
          <div style="font-size:14px;font-weight:500;color:var(--ink)">Drop an audio file to transcribe</div>
          <div style="font-size:12px;color:var(--ink-3);margin-top:4px">MP3 · WAV · M4A — processed by OpenAI Whisper</div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  PAGE: JWT TOKEN
# ═══════════════════════════════════════════════════════════
def page_token():
    page_header("JWT Token", "Authentication", "—", "HS256 · Bearer")
    token = st.session_state.token or ""

    section_divider("ACCESS TOKEN")
    if token:
        st.markdown(f'<div class="token-block">{token}</div>', unsafe_allow_html=True)
        st.code(f"Authorization: Bearer {token}", language="bash")
        col_copy, _ = st.columns([1, 3])
        col_copy.download_button("Download token", data=token, file_name="jwt_token.txt", mime="text/plain", key="dl_token")

        payload = decode_jwt(token)
        if payload:
            section_divider("DECODED PAYLOAD")
            cols = st.columns(min(len(payload), 3))
            for i, (k, v) in enumerate(payload.items()):
                display = str(v)
                if k in ("exp","iat"):
                    try:    display = datetime.utcfromtimestamp(v).strftime("%d %b %Y · %H:%M UTC")
                    except: pass
                cols[i % len(cols)].metric(k, display)

            if "exp" in payload:
                remaining = payload["exp"] - datetime.utcnow().timestamp()
                if remaining > 0:
                    st.info(f"⏱  Token expires in **{int(remaining // 60)} minutes**.")
                else:
                    st.error("⚠️  Token has expired. Please sign in again.")
    else:
        st.warning("No token in session. Please sign in first.")

    section_divider("USAGE EXAMPLE")
    role = st.session_state.user_role or "admin"
    mode = get_role_cfg(role)["mode"]
    st.code(
        f'curl -H "Authorization: Bearer <your_token>" \\\n'
        f'     -X POST "http://localhost:8000/ask?question=hello&mode={mode}"',
        language="bash",
    )


# ═══════════════════════════════════════════════════════════
#  PAGE: ADMIN
# ═══════════════════════════════════════════════════════════
def page_admin():
    page_header("Admin Panel", "User Management", "GET", "/admin/users")

    col_hdr, col_btn = st.columns([5, 1])
    col_hdr.markdown("### All registered users")
    if col_btn.button("↻  Refresh", key="adm_refresh"):
        st.session_state.admin_users = None

    if st.session_state.admin_users is None:
        with st.spinner("Loading users…"):
            resp = api("GET", "/admin/users")
        if resp is None:
            st.error("Cannot reach backend.")
            return
        if resp.status_code == 200:
            st.session_state.admin_users = resp.json()
        else:
            try:    st.error(resp.json().get("detail", "Failed to load users."))
            except: st.error("Failed to load users.")
            return

    users = st.session_state.admin_users or []
    if not users:
        st.info("No users found.")
        return

    section_divider(f"{len(users)} USER{'S' if len(users) != 1 else ''}")

    for user in users:
        initials = user["email"][0].upper()
        role     = user.get("role", "admin")
        col_av, col_info, col_role, col_del = st.columns([0.5, 3, 1.5, 1])

        col_av.markdown(f'<div class="user-avatar" style="margin-top:4px">{initials}</div>', unsafe_allow_html=True)
        col_info.markdown(f'<div class="user-email-txt">{user["email"]}</div><div class="user-id">ID #{user["id"]}</div>', unsafe_allow_html=True)
        col_role.markdown(f'<div style="margin-top:8px"><span class="role-badge rb-{role}">{role}</span></div>', unsafe_allow_html=True)

        if col_del.button("Delete", key=f"del_{user['id']}"):
            resp = api("DELETE", f"/admin/users/{user['id']}")
            if resp and resp.status_code == 200:
                st.success(f"Deleted {user['email']}")
                st.session_state.admin_users = [u for u in users if u["id"] != user["id"]]
                st.rerun()
            else:
                st.error("Delete failed.")

        st.markdown("<hr style='margin:6px 0;border-color:var(--border)'>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  ROUTER
# ═══════════════════════════════════════════════════════════
PAGE_MAP = {
    "ask":        page_ask,
    "upload":     page_upload,
    "summarize":  page_summarize,
    "format":     page_format,
    "transcribe": page_transcribe,
    "token":      page_token,
    "admin":      page_admin,
}

def main():
    if not st.session_state.token:
        render_auth()
    else:
        render_sidebar()
        PAGE_MAP.get(st.session_state.page, page_ask)()

if __name__ == "__main__":
    main()