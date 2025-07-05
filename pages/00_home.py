import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="HR Copilot Home",
    page_icon="🎯",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("📚 HR Copilot Modules")
modules = [
    ("01. Talent Development", "01_talent_development.py"),
    ("02. Succession Planning", "02_succession_planning.py"),
    ("03. Talent Acquisition", "03_talent_acquisition.py"),
    ("04. Performance Management", "04_performance_management.py"),
    ("05. Employee Relations", "05_employee_relations.py"),
    ("06. Process Digitization", "06_process_digitization.py"),
    ("07. Learning & Development", "07_learning_development.py"),
    ("08. Compensation & Rewards", "08_compensation_rewards.py"),
    ("09. Goal Setting", "09_goal_setting.py")
]

# Search feature
search_query = st.sidebar.text_input("🔍 Search modules or features", "")

# Filter modules by search
filtered_modules = [m for m in modules if search_query.lower() in m[0].lower()]

# Show modules in a vertical list on the left
for name, page in filtered_modules:
    if st.sidebar.button(name, key=page):
        st.switch_page(f"pages/{page}")

# Global model selector in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Model Selection")
if 'model_choice' not in st.session_state:
    st.session_state['model_choice'] = "Gemini (Google)"
st.session_state['model_choice'] = st.sidebar.selectbox(
    "Choose AI Model",
    ["Gemini (Google)", "GPT-4.1 (OpenAI)"],
    index=0 if st.session_state['model_choice'] == "Gemini (Google)" else 1,
    key="global_model_choice_home"
)

st.title("🎯 Welcome to HR Copilot")
st.markdown("**Select a module from the left sidebar or below to get started.**")

# Main area: clickable module grid (filtered by search)
st.markdown("---")
col1, col2, col3 = st.columns(3)
# Use the same filtered_modules for the grid, but add icons and ensure names are well written
module_grid_full = [
    ("01. Talent Development", "01_talent_development.py", "🎯"),
    ("02. Succession Planning", "02_succession_planning.py", "👑"),
    ("03. Talent Acquisition", "03_talent_acquisition.py", "🧑‍💼"),
    ("04. Performance Management", "04_performance_management.py", "📈"),
    ("05. Employee Relations", "05_employee_relations.py", "⚖️"),
    ("06. Process Digitization", "06_process_digitization.py", "🔄"),
    ("07. Learning & Development", "07_learning_development.py", "🎓"),
    ("08. Compensation & Rewards", "08_compensation_rewards.py", "💰"),
    ("09. Goal Setting", "09_goal_setting.py", "🎯")
]
# Filter the grid by search
filtered_grid = [m for m in module_grid_full if search_query.lower() in m[0].lower()]
for i, (name, page, icon) in enumerate(filtered_grid):
    col = [col1, col2, col3][i % 3]
    with col:
        if st.button(f"{icon} {name}", key=f"main_{page}"):
            st.switch_page(f"pages/{page}")

st.markdown("---")
st.markdown("""
### About HR Copilot
This app provides AI-powered tools for the entire HR lifecycle, including:
- 01. Talent Development
- 02. Succession Planning
- 03. Talent Acquisition
- 04. Performance Management
- 05. Employee Relations
- 06. Process Digitization
- 07. Learning & Development
- 08. Compensation & Rewards
- 09. Goal Setting

---

**Tip:** You can always return to this home page from the sidebar or by clicking 'home'.
""")
