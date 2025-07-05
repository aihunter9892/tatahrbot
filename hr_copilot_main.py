import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="All-In-One HR Copilot",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .module-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        text-align: center;
    }
    .module-card h3 {
        color: white !important;
        margin-bottom: 0.5rem;
    }
    .status-badge {
        background: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .coming-soon {
        background: #ffc107;
        color: #212529;
    }
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🎯 All-In-One HR Copilot</h1>
    <p>AI-powered HR application for creating, customizing, and managing high-quality HR documents across the entire employee lifecycle</p>
</div>
""", unsafe_allow_html=True)

# API Key status (support both Gemini and OpenAI)
gemini_key = os.getenv('GEMINI_API_KEY')
openai_key = os.getenv('OPENAI_API_KEY')

if gemini_key and openai_key:
    st.success("✅ Gemini and OpenAI API Keys configured - Ready to use!")
elif gemini_key:
    st.success("✅ Gemini API Key configured - Gemini features enabled!")
elif openai_key:
    st.success("✅ OpenAI API Key configured - OpenAI features enabled!")
else:
    st.error("⚠️ Please configure GEMINI_API_KEY or OPENAI_API_KEY in your .env file to enable AI features")

# Module selection
st.header("🚀 Choose Your HR Module")
st.markdown("Select a module to access specific HR tools and AI-powered document generation:")

# Create module grid
col1, col2, col3 = st.columns(3)

# Module 1: Talent Development
with col1:
    st.markdown("""
    <div class="module-card">
        <h3>📚 Module 1: Talent Development</h3>
        <p>Build comprehensive talent management frameworks</p>
        <span class="status-badge">Available</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎯 Launch Talent Development", key="mod1", type="primary"):
        st.switch_page("pages/01_talent_development.py")
    
    with st.expander("🔍 View Module Features"):
        st.markdown("""
        - **📋 Individual Development Plans (IDPs)** - Role-specific career planning
        - **🏗️ Competency Frameworks** - Multi-level skill matrices  
        - **🗺️ Career Path Mapping** - Visual progression planning
        - **👥 Coaching Guides** - Comprehensive coaching templates
        - **⭐ HiPo Identification** - High-potential employee frameworks
        - **🎨 Custom Assistant** - Flexible AI-powered content generation
        """)

# Module 2: Succession Planning
with col2:
    st.markdown("""
    <div class="module-card">
        <h3>👑 Module 2: Succession Planning</h3>
        <p>Create robust succession strategies and leadership pipelines</p>
        <span class="status-badge">Available</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👑 Launch Succession Planning", key="mod2", type="primary"):
        st.switch_page("pages/02_succession_planning.py")
    
    with st.expander("🔍 View Module Features"):
        st.markdown("""
        - **📋 Succession Plan Formats** - Critical role succession frameworks
        - **✅ Readiness Checklists** - Successor preparation assessments
        - **🎯 Development Action Plans** - Targeted leadership development
        - **📢 Communication Templates** - Stakeholder engagement plans
        - **📊 Policy & Governance** - Succession planning frameworks
        - **🎨 Custom Assistant** - Flexible succession planning tools
        """)

# Module 3: Talent Acquisition & Onboarding
with col3:
    st.markdown("""
    <div class="module-card">
        <h3>🎯 Module 3: Talent Acquisition</h3>
        <p>Streamline hiring and onboarding processes</p>
        <span class="status-badge">Available</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎯 Launch Talent Acquisition", key="mod3", type="primary"):
        st.switch_page("pages/03_talent_acquisition.py")
    
    with st.expander("🔍 Planned Features"):
        st.markdown("""
        - **📝 Job Description Generator** - Inclusive, bias-free JDs
        - **🔍 CV vs JD Comparison** - AI-powered candidate ranking
        - **📄 Offer Letters & Contracts** - Standard template library
        - **✅ Pre-joining Checklists** - Comprehensive preparation
        - **📅 30-60-90 Day Plans** - Structured onboarding roadmaps
        - **📧 Welcome Communications** - New hire engagement
        """)

# Second row
col4, col5, col6 = st.columns(3)

# Module 4: Performance Management
with col4:
    st.markdown("""
    <div class="module-card">
        <h3>📊 Module 4: Performance Management</h3>
        <p>Drive performance excellence and employee development</p>
        <span class="status-badge">Available</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Launch Performance Management", key="mod4", type="primary"):
        st.switch_page("pages/04_performance_management.py")
    
    with st.expander("🔍 View Module Features"):
        st.markdown("""
        - **📊 Performance Review Templates** - Comprehensive evaluation forms
        - **🎯 Goal Setting Framework** - SMART goals and objective-setting
        - **📈 Development Plans** - Individual development roadmaps
        - **💼 Career Progression Maps** - Clear advancement pathways
        - **🏆 Recognition Programs** - Employee recognition system design
        - **🎨 Custom Performance Tools** - Any performance management document
        """)

# Module 5: Industrial Relations
with col5:
    st.markdown("""
    <div class="module-card">
        <h3>⚖️ Module 5: Industrial Relations</h3>
        <p>Manage employee relations and compliance</p>
        <span class="status-badge">Available</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⚖️ Launch IR Module", key="mod5", type="primary"):
        st.switch_page("pages/05_employee_relations.py")
    
    with st.expander("🔍 Planned Features"):
        st.markdown("""
        - **📝 Disciplinary Letters** - Show-cause and warning templates
        - **📋 Grievance Policies** - Redressal process frameworks
        - **❓ Employee IR FAQs** - Common questions and answers
        - **📋 Union Meeting Minutes** - Meeting documentation templates
        - **🤝 Settlement Agreements** - Dispute resolution documents
        - **📸 Incident Report** - Upload photos and make a report
        - **🎨 Custom IR Tools** - Flexible compliance solutions
        """)

# Module 6: Process Digitization
with col6:
    st.markdown("""
    <div class="module-card">
        <h3>🔄 Module 6: Process Digitization</h3>
        <p>Digitize and automate HR workflows</p>
        <span class="status-badge">Available</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Launch Digitization", key="mod6", type="primary"):
        st.switch_page("pages/06_process_digitization.py")
    
    with st.expander("🔍 Planned Features"):
        st.markdown("""
        - **🤖 Chatbot Scripts** - HR FAQ automation
        - **📋 Digital Forms** - Onboarding and exit processes
        - **📖 SOP Creation** - Standard operating procedures
        - **📚 Knowledge Base** - Self-service HR articles
        - **📧 Email Automation** - Template and workflow creation
        - **🎨 Custom Automation** - Flexible digitization tools
        """)

# Third row
col7, col8, col9 = st.columns(3)

# Module 7: L&D & Capability Development
with col7:
    st.markdown("""
    <div class="module-card">
        <h3>🎓 Module 7: L&D Development</h3>
        <p>Design training and capability programs</p>
        <span class="status-badge">Available</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎓 Launch L&D Module", key="mod7", type="primary"):
        st.switch_page("pages/07_learning_development.py")
    
    with st.expander("🔍 Planned Features"):
        st.markdown("""
        - **📚 Training Design Wizard** - Workshop and course creation
        - **❓ Assessment Builder** - Quiz and evaluation tools
        - **📝 Feedback Forms** - Training effectiveness measurement
        - **🛤️ Learning Pathways** - Personalized development journeys
        - **📧 Course Communications** - Training announcements and reminders
        - **🎨 Custom L&D Tools** - Flexible learning solutions
        """)

# Module 8: Compensation & Rewards
with col8:
    st.markdown("""
    <div class="module-card">
        <h3>💰 Module 8: Compensation</h3>
        <p>Manage rewards and recognition programs</p>
        <span class="status-badge">Available</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💰 Launch Compensation", key="mod8", type="primary"):
        st.switch_page("pages/08_compensation_rewards.py")
    
    with st.expander("🔍 Planned Features"):
        st.markdown("""
        - **📄 Pay Revision Letters** - Increment and promotion communications
        - **🎉 Bonus Communications** - Payout announcements and explanations
        - **📊 Total Rewards Statements** - Comprehensive compensation overview
        - **🏆 Recognition Certificates** - Achievement and appreciation documents
        - **📋 R&R Policy Creation** - Rewards and recognition frameworks
        - **🎨 Custom Compensation Tools** - Flexible rewards solutions
        """)

# Module 9: BSC Alignment & Goal Setting
with col9:
    st.markdown("""
    <div class="module-card">
        <h3>🎯 Module 9: Goal Setting</h3>
        <p>Align performance with business objectives</p>
        <span class="status-badge">Available</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎯 Launch Goal Setting", key="mod9", type="primary"):
        st.switch_page("pages/09_goal_setting.py")
    
    with st.expander("🔍 Planned Features"):
        st.markdown("""
        - **🎯 SMART Goals Library** - BSC-aligned objective creation
        - **📋 Goal-Setting Guides** - Manager toolkits and frameworks
        - **📊 Performance Templates** - Review and evaluation forms
        - **📧 Progress Reminders** - Automated goal tracking communications
        - **🏆 Achievement Recognition** - Success celebration templates
        - **🎨 Custom Goal Tools** - Flexible performance management
        """)

# Footer information
st.markdown("---")
st.header("🏢 About All-In-One HR Copilot")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.subheader("🎯 Purpose")
    st.markdown("""
    The All-In-One HR Copilot is an AI-powered application designed to help HR teams and business leaders rapidly create, customize, and manage high-quality HR documents, tools, and frameworks across the entire employee lifecycle.
    
    **Key Benefits:**
    - ⚡ **Boost Productivity** - Reduce document creation time by 80%
    - 📊 **Ensure Consistency** - Standardized templates and best practices
    - 🎯 **Improve Compliance** - Built-in regulatory and policy alignment
    - 🚀 **AI-Powered** - Leverage cutting-edge Gemini 2.0 Flash technology
    """)

with col_info2:
    st.subheader("🛠️ Getting Started")
    st.markdown("""
    **Prerequisites:**
    1. **Google Gemini API Key** - Get yours from [Google AI Studio](https://aistudio.google.com/app/apikey)
    2. **Python Environment** - Install required packages
    3. **Environment Setup** - Create `.env` file with your API key
    
    **Installation:**
    ```bash
    pip install streamlit google-generativeai python-dotenv
    echo "GEMINI_API_KEY=your_api_key_here" > .env
    streamlit run hr_copilot_main.py
    ```
    """)

# Development status
st.subheader("🚧 Development Status")
progress_col1, progress_col2 = st.columns([3, 1])

# All 9 modules are now available
st.progress(100)
    
with progress_col2:
    st.metric("Modules Ready", "9/9", "100%")

st.info("🎉 **Congratulations!** All modules are now available. Explore the full suite of HR Copilot features!")

# Quick actions
st.subheader("⚡ Quick Actions")
quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)

with quick_col1:
    if st.button("🎯 Try Talent Development", type="secondary"):
        st.switch_page("pages/01_talent_development.py")

with quick_col2:
    if st.button("👑 Try Succession Planning", type="secondary"):
        st.switch_page("pages/02_succession_planning.py")

with quick_col3:
    if st.button("📧 Request New Module", type="secondary"):
        st.info("Feature requests coming soon!")

with quick_col4:
    if st.button("📖 View Documentation", type="secondary"):
        st.info("Documentation coming soon!")
