import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="HR Copilot - Process Digitization",
    page_icon="🔄",
    layout="wide"
)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {}

# Get API keys from environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Determine available models
available_models = []
if GEMINI_API_KEY:
    available_models.append("Gemini (Google)")
if OPENAI_API_KEY:
    available_models.append("GPT-4.1 (OpenAI)")

# Sidebar information
with st.sidebar:
    st.title("🔧 Configuration")
    if not available_models:
        st.error("❌ No API key found. Please add GEMINI_API_KEY or OPENAI_API_KEY to your .env file.")
    else:
        if 'model_choice' not in st.session_state or st.session_state['model_choice'] not in available_models:
            st.session_state['model_choice'] = available_models[0]
        st.session_state['model_choice'] = st.selectbox(
            "Choose AI Model",
            available_models,
            index=available_models.index(st.session_state['model_choice']),
            key="global_model_choice"
        )
        if st.session_state['model_choice'] == "Gemini (Google)":
            st.success("✅ Gemini API Key loaded from .env file")
        else:
            st.success("✅ OpenAI API Key loaded from .env file")
    st.markdown("---")
    st.markdown("### 🔄 Module 6: Process Digitization")
    st.markdown("Digitize and automate HR workflows for efficiency")
    
    if st.button("🏠 Back to Main Menu"):
        st.switch_page("hr_copilot_main.py")

# Helper functions
def clean_text(text):
    """Remove markdown formatting for clean display"""
    if not text:
        return ""
    cleaned = text.replace('**', '').replace('*', '').replace('###', '').replace('##', '').replace('#', '')
    return cleaned.strip()

def generate_content(prompt, content_type):
    """Generate content using selected AI model"""
    model_choice = st.session_state.get('model_choice', available_models[0] if available_models else 'Gemini (Google)')
    if model_choice == "Gemini (Google)":
        if not GEMINI_API_KEY:
            st.error("Please add your Gemini API key to the .env file")
            return None
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            system_prompt = """You are a senior HR process digitization and automation specialist with 15+ years of experience in streamlining HR workflows, creating digital forms, knowledge bases, and automated communications.

CRITICAL INSTRUCTIONS:
- Write ONLY the document content, nothing else
- Do NOT include explanatory text, introductions, or commentary
- Do NOT write phrases like "Here's a comprehensive..." or "I'll create..."
- Start directly with the document content
- Use simple, clean formatting without markdown symbols
- Use CAPITAL LETTERS for main headings
- Use numbered lists and bullet points with dashes (-)
- Keep language professional, clear, and actionable
- Include specific examples and metrics where relevant
- Make all content immediately usable in corporate environments

Focus on practical, implementable solutions that drive efficiency, consistency, and employee self-service."""
            full_prompt = f"{system_prompt}\n\n{prompt}"
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2500
                )
            )
            return response.text
        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
            return None
    elif model_choice == "GPT-4.1 (OpenAI)":
        if not OPENAI_API_KEY:
            st.error("Please add your OpenAI API key to the .env file")
            return None
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.responses.create(
                model="gpt-4.1",
                input=prompt
            )
            return response.output_text
        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
            return None
    else:
        st.error("No valid model selected or available.")
        return None

def create_download_button(content, filename, label):
    """Create a simple download button"""
    cleaned_content = clean_text(content)
    st.download_button(
        label=label,
        data=cleaned_content,
        file_name=f"{filename}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

# Main title
st.title("🔄 HR Copilot - Process Digitization")
st.markdown("Digitize and automate HR workflows for enhanced efficiency and employee experience")

# Tab layout
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🤖 Chatbot Scripts",
    "📋 Digital Forms", 
    "📖 SOP Creation",
    "📚 Knowledge Base Articles",
    "📧 Email Automation Templates",
    "🎨 Custom Process Tools"
])

# Tab 1: Chatbot Scripts
with tab1:
    st.header("🤖 HR Chatbot Q&A Scripts")
    st.markdown("Draft Q&A scripts for HR chatbots to automate responses to common employee queries.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Scripts")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Onboarding FAQs Script", type="secondary", key="sample_chatbot_onboarding"):
            st.session_state.update({
                'chatbot_topic': 'Onboarding Process',
                'target_user_chatbot': 'New Hires',
                'num_qa_pairs': 10,
                'additional_context_chatbot': 'Focus on common questions about first day, necessary documents and initial access.'
            })
    
    with col_sample2:
        if st.button("Leave Policy FAQs Script", type="secondary", key="sample_chatbot_leave"):
            st.session_state.update({
                'chatbot_topic': 'Leave Policy',
                'target_user_chatbot': 'All Employees',
                'num_qa_pairs': 8,
                'additional_context_chatbot': 'Include questions about different leave types (sick, casual, annual), application process, and approval.'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Script Details")
        chatbot_topic = st.text_input("Chatbot Topic", value=st.session_state.get('chatbot_topic', ''), placeholder="e.g., Onboarding, Leave Policy, Payroll, Benefits", key="chatbot_topic_input")
        target_user_chatbot = st.text_input("Target User Group", value=st.session_state.get('target_user_chatbot', ''), placeholder="e.g., New Hires, All Employees, Managers", key="target_user_chatbot_input")
        
    with col2:
        st.subheader("Customization")
        num_qa_pairs = st.number_input("Number of Q&A Pairs", min_value=5, max_value=25, value=st.session_state.get('num_qa_pairs', 10), key="num_qa_pairs_input")
        additional_context_chatbot = st.text_area("Additional Context/Specifics", height=100, value=st.session_state.get('additional_context_chatbot', ''), placeholder="e.g., Mention specific company policies or systems.", key="additional_context_chatbot_input")
        
        if st.button("🤖 Generate Chatbot Script", type="primary", key="generate_chatbot_script"):
            if chatbot_topic and target_user_chatbot:
                prompt = f"""Generate {num_qa_pairs} Q&A pairs for an HR chatbot script on the topic of '{chatbot_topic}'.

Target User Group: {target_user_chatbot}
Additional Context: {additional_context_chatbot if additional_context_chatbot else 'None'}

Each Q&A pair should be:
- A common question a user might ask.
- A concise, clear, and helpful answer.
- Formatted as "Q: [Question]\nA: [Answer]".

Focus on practical information that can be easily automated by a chatbot."""

                with st.spinner(f"Generating chatbot script for {chatbot_topic}..."):
                    content = generate_content(prompt, "Chatbot Script")
                    if content:
                        st.session_state.generated_content['chatbot_script'] = content
            else:
                st.error("Please fill in Chatbot Topic and Target User Group.")
    
    # Display generated content
    if 'chatbot_script' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated Chatbot Script for {chatbot_topic}")
        cleaned_content = clean_text(st.session_state.generated_content['chatbot_script'])
        st.text_area("Chatbot Script Content", value=cleaned_content, height=400, key="chatbot_script_output")
        create_download_button(cleaned_content, f"Chatbot_Script_{chatbot_topic.replace(' ', '_')}", "📥 Download Chatbot Script")

# Tab 2: Digital Forms
with tab2:
    st.header("📋 Digital Forms")
    st.markdown("Create standard digital forms for various HR processes (e.g., onboarding, exit, internal requests).")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Forms")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("New Hire Onboarding Form", type="secondary", key="sample_form_onboarding"):
            st.session_state.update({
                'form_purpose': 'New Hire Onboarding',
                'form_sections': 'Personal Information, Emergency Contact, Bank Details, Tax Information, IT Access Request, Equipment Request',
                'form_audience': 'New Employees',
                'form_required_fields': 'Full Name, Employee ID, Date of Joining, Department, Position'
            })
    
    with col_sample2:
        if st.button("Employee Exit Checklist", type="secondary", key="sample_form_exit"):
            st.session_state.update({
                'form_purpose': 'Employee Exit Checklist',
                'form_sections': 'Last Working Day, Reason for Exit, Equipment Return, Access Revocation, Final Settlement, Feedback Survey Link',
                'form_audience': 'Exiting Employees and Managers',
                'form_required_fields': 'Employee Name, Employee ID, Last Working Day'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Form Details")
        form_purpose = st.text_input("Purpose of the Form", value=st.session_state.get('form_purpose', ''), placeholder="e.g., New Hire Onboarding, Leave Request, Expense Claim", key="form_purpose_input")
        form_sections = st.text_area("Key Sections/Fields to Include", height=100, value=st.session_state.get('form_sections', ''), placeholder="e.g., Personal Details, Employment History, Skills, Education", key="form_sections_input")
        
    with col2:
        st.subheader("Customization")
        form_audience = st.text_input("Target Audience for the Form", value=st.session_state.get('form_audience', ''), placeholder="e.g., All Employees, Managers, HR", key="form_audience_input")
        form_required_fields = st.text_area("Mandatory Fields", height=70, value=st.session_state.get('form_required_fields', ''), placeholder="e.g., Employee Name, Date, Signature", key="form_required_fields_input")
        
        if st.button("📋 Generate Digital Form", type="primary", key="generate_digital_form"):
            if form_purpose and form_sections:
                prompt = f"""Create a comprehensive digital form template for '{form_purpose}'.

Key Sections/Fields to Include: {form_sections}
Target Audience: {form_audience}
Mandatory Fields: {form_required_fields}

Structure the form with clear headings, field labels, and instructions. Include sections for:
- Form Title and Purpose
- Instructions for Completion
- Data Input Fields (specify type: text, date, dropdown, checkbox, etc.)
- Signature/Acknowledgment Sections
- Submission Guidelines

Ensure the form is user-friendly and captures all necessary information for the specified purpose."""

                with st.spinner(f"Generating digital form for {form_purpose}..."):
                    content = generate_content(prompt, "Digital Form")
                    if content:
                        st.session_state.generated_content['digital_form'] = content
            else:
                st.error("Please fill in Purpose of the Form and Key Sections/Fields.")
    
    # Display generated content
    if 'digital_form' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated Digital Form for {form_purpose}")
        cleaned_content = clean_text(st.session_state.generated_content['digital_form'])
        st.text_area("Digital Form Content", value=cleaned_content, height=400, key="digital_form_output")
        create_download_button(cleaned_content, f"Digital_Form_{form_purpose.replace(' ', '_')}", "📥 Download Digital Form")

# Tab 3: SOP Creation
with tab3:
    st.header("📖 Standard Operating Procedure (SOP) Creation")
    st.markdown("Generate detailed SOPs for various HR processes to ensure consistency and compliance.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample SOPs")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Employee Onboarding SOP", type="secondary", key="sample_sop_onboarding"):
            st.session_state.update({
                'sop_process_name': 'Employee Onboarding Process',
                'sop_scope': 'From offer acceptance to 90-day review.',
                'sop_responsible_roles': 'HR Team, Hiring Managers, IT Department, Payroll.',
                'sop_key_steps': 'Offer Letter, Background Check, System Access, Induction, First Day Checklist, Training, 30-60-90 Day Check-ins.',
                'sop_compliance': 'Adherence to local labor laws and company policies.'
            })
    
    with col_sample2:
        if st.button("Performance Review SOP", type="secondary", key="sample_sop_performance"):
            st.session_state.update({
                'sop_process_name': 'Annual Performance Review Process',
                'sop_scope': 'Annual cycle for all permanent employees.',
                'sop_responsible_roles': 'Employees, Managers, HR Business Partners.',
                'sop_key_steps': 'Goal Setting, Mid-Year Check-in, Self-Assessment, Manager Review, Calibration, Final Discussion, Development Planning.',
                'sop_compliance': 'Fairness, objectivity, and non-discrimination principles.'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("SOP Details")
        sop_process_name = st.text_input("Process Name for SOP", value=st.session_state.get('sop_process_name', ''), placeholder="e.g., Leave Application, Recruitment, Expense Approval", key="sop_process_name_input")
        sop_scope = st.text_area("Scope of the SOP", height=70, value=st.session_state.get('sop_scope', ''), placeholder="e.g., Applies to all full-time employees.", key="sop_scope_input")
        
    with col2:
        st.subheader("SOP Content")
        sop_responsible_roles = st.text_area("Responsible Roles/Departments", height=70, value=st.session_state.get('sop_responsible_roles', ''), placeholder="e.g., HR, Finance, Employees", key="sop_responsible_roles_input")
        sop_key_steps = st.text_area("Key Steps/Workflow", height=100, value=st.session_state.get('sop_key_steps', ''), placeholder="List sequential steps of the process.", key="sop_key_steps_input")
        sop_compliance = st.text_area("Compliance/Regulatory Considerations", height=70, value=st.session_state.get('sop_compliance', ''), placeholder="e.g., GDPR, local labor laws", key="sop_compliance_input")
        
        if st.button("📖 Generate SOP", type="primary", key="generate_sop"):
            if sop_process_name and sop_key_steps:
                prompt = f"""Create a detailed Standard Operating Procedure (SOP) for the '{sop_process_name}'.

Scope: {sop_scope}
Responsible Roles/Departments: {sop_responsible_roles}
Key Steps/Workflow: {sop_key_steps}
Compliance/Regulatory Considerations: {sop_compliance if sop_compliance else 'None'}

The SOP should include:
- SOP Title, Version, Date, and Review Date
- Purpose and Objectives
- Scope
- Definitions (if applicable)
- Roles and Responsibilities
- Detailed Step-by-Step Procedure (with clear instructions and decision points)
- Flowchart (describe verbally if not visual)
- Related Documents/Forms
- Compliance and Safety Notes
- Revision History

Ensure clarity, conciseness, and logical flow for easy understanding and adherence."""

                with st.spinner(f"Generating SOP for {sop_process_name}..."):
                    content = generate_content(prompt, "SOP")
                    if content:
                        st.session_state.generated_content['sop'] = content
            else:
                st.error("Please fill in Process Name and Key Steps.")
    
    # Display generated content
    if 'sop' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated SOP for {sop_process_name}")
        cleaned_content = clean_text(st.session_state.generated_content['sop'])
        st.text_area("SOP Content", value=cleaned_content, height=400, key="sop_output")
        create_download_button(cleaned_content, f"SOP_{sop_process_name.replace(' ', '_')}", "📥 Download SOP")

# Tab 4: Knowledge Base Articles
with tab4:
    st.header("📚 Knowledge Base Articles")
    st.markdown("Generate informative articles for your HR knowledge base or internal wiki.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Articles")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Understanding Your Benefits Article", type="secondary", key="sample_kb_benefits"):
            st.session_state.update({
                'kb_topic': 'Understanding Your Employee Benefits',
                'kb_target_audience': 'All Employees',
                'kb_key_points': 'Health Insurance, Retirement Plans, Paid Time Off, Wellness Programs, Employee Assistance Program.',
                'kb_tone': 'Informative and supportive'
            })
    
    with col_sample2:
        if st.button("How to Submit an Expense Report Article", type="secondary", key="sample_kb_expense"):
            st.session_state.update({
                'kb_topic': 'How to Submit an Expense Report',
                'kb_target_audience': 'All Employees',
                'kb_key_points': 'Accessing the system, Required documentation, Approval process, Reimbursement timeline, Common errors.',
                'kb_tone': 'Instructional and clear'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Article Details")
        kb_topic = st.text_input("Knowledge Base Article Topic", value=st.session_state.get('kb_topic', ''), placeholder="e.g., Remote Work Policy, Performance Management Cycle", key="kb_topic_input")
        kb_target_audience = st.text_input("Target Audience", value=st.session_state.get('kb_target_audience', ''), placeholder="e.g., All Employees, Managers", key="kb_target_audience_input")
        
    with col2:
        st.subheader("Article Content")
        kb_key_points = st.text_area("Key Points/Sections to Cover", height=100, value=st.session_state.get('kb_key_points', ''), placeholder="e.g., Eligibility, Application Process, Approval, FAQs", key="kb_key_points_input")
        kb_tone = st.text_input("Tone of Article", value=st.session_state.get('kb_tone', ''), placeholder="e.g., Formal, Friendly, Instructional", key="kb_tone_input")
        
        if st.button("📚 Generate Knowledge Base Article", type="primary", key="generate_kb_article"):
            if kb_topic and kb_key_points:
                prompt = f"""Generate a comprehensive Knowledge Base Article on the topic of '{kb_topic}'.

Target Audience: {kb_target_audience}
Key Points/Sections to Cover: {kb_key_points}
Tone of Article: {kb_tone}

Structure the article with:
- A clear title
- An introduction
- Detailed sections for each key point
- A summary or conclusion
- Relevant FAQs (if applicable)
- Links to related policies or forms (suggest placeholders)

Ensure the language is accessible, accurate, and directly addresses the needs of the target audience."""

                with st.spinner(f"Generating knowledge base article on {kb_topic}..."):
                    content = generate_content(prompt, "Knowledge Base Article")
                    if content:
                        st.session_state.generated_content['kb_article'] = content
            else:
                st.error("Please fill in Article Topic and Key Points.")
    
    # Display generated content
    if 'kb_article' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated Knowledge Base Article on {kb_topic}")
        cleaned_content = clean_text(st.session_state.generated_content['kb_article'])
        st.text_area("Knowledge Base Article Content", value=cleaned_content, height=400, key="kb_article_output")
        create_download_button(cleaned_content, f"KB_Article_{kb_topic.replace(' ', '_')}", "📥 Download KB Article")

# Tab 5: Email Automation Templates
with tab5:
    st.header("📧 Automated Email Templates")
    st.markdown("Draft standard email templates for automated HR communications (e.g., onboarding, reminders, announcements).")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Templates")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("New Hire Welcome Email", type="secondary", key="sample_email_welcome"):
            st.session_state.update({
                'email_purpose': 'New Hire Welcome',
                'email_sender': 'HR Department',
                'email_recipient': 'New Employee',
                'email_key_info': 'First day instructions, IT setup, Benefits overview, Team introduction, Link to onboarding portal.',
                'email_tone': 'Warm and welcoming',
                'email_cta': 'Complete pre-joining formalities, Contact HR for questions.'
            })
    
    with col_sample2:
        if st.button("Performance Review Reminder Email", type="secondary", key="sample_email_review_reminder"):
            st.session_state.update({
                'email_purpose': 'Performance Review Reminder',
                'email_sender': 'HR Operations',
                'email_recipient': 'Employees and Managers',
                'email_key_info': 'Review period, Deadline for self-assessment/manager review, Link to performance system, Resources/guides.',
                'email_tone': 'Formal and helpful',
                'email_cta': 'Submit your review by deadline, Reach out to HRBP for support.'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Email Details")
        email_purpose = st.text_input("Purpose of the Email", value=st.session_state.get('email_purpose', ''), placeholder="e.g., New Hire Welcome, Policy Update, Training Invitation", key="email_purpose_input")
        email_sender = st.text_input("Sender (e.g., HR Department, Your Name)", value=st.session_state.get('email_sender', ''), key="email_sender_input")
        email_recipient = st.text_input("Recipient Group", value=st.session_state.get('email_recipient', ''), placeholder="e.g., All Employees, New Hires, Managers", key="email_recipient_input")
        
    with col2:
        st.subheader("Email Content")
        email_key_info = st.text_area("Key Information to Convey", height=100, value=st.session_state.get('email_key_info', ''), placeholder="e.g., Date, Time, Location, Action Required", key="email_key_info_input")
        email_tone = st.text_input("Tone of Email", value=st.session_state.get('email_tone', ''), placeholder="e.g., Formal, Friendly, Urgent", key="email_tone_input")
        email_cta = st.text_area("Call to Action (if any)", height=70, value=st.session_state.get('email_cta', ''), placeholder="e.g., Click here to register, Submit by deadline", key="email_cta_input")
        
        if st.button("📧 Generate Email Template", type="primary", key="generate_email_template"):
            if email_purpose and email_key_info:
                prompt = f"""Draft an automated email template for the purpose of '{email_purpose}'.

Sender: {email_sender}
Recipient Group: {email_recipient}
Key Information to Convey: {email_key_info}
Tone of Email: {email_tone}
Call to Action: {email_cta if email_cta else 'None'}

The email should include:
- A clear and concise subject line.
- A personalized greeting.
- All key information clearly presented.
- A call to action (if applicable).
- A professional closing.
- Placeholder for dynamic information (e.g., [Employee Name]).

Ensure the email is suitable for automated delivery and effectively communicates its purpose."""

                with st.spinner(f"Generating email template for {email_purpose}..."):
                    content = generate_content(prompt, "Email Template")
                    if content:
                        st.session_state.generated_content['email_template'] = content
            else:
                st.error("Please fill in Purpose of the Email and Key Information.")
    
    # Display generated content
    if 'email_template' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated Email Template for {email_purpose}")
        cleaned_content = clean_text(st.session_state.generated_content['email_template'])
        st.text_area("Email Template Content", value=cleaned_content, height=400, key="email_template_output")
        create_download_button(cleaned_content, f"Email_Template_{email_purpose.replace(' ', '_')}", "📥 Download Email Template")

# Tab 6: Custom Process Tools
with tab6:
    st.header("🎨 Custom Process Digitization Tools")
    st.markdown("Create any HR process document, workflow, or automation framework.")
    
    # Sample prompts
    st.subheader("🎯 Best Practice Process Prompts")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Sample: Digital Onboarding Workflow", type="secondary", key="sample_custom_onboarding_workflow"):
            st.session_state['custom_prompt_process'] = """Design a digital onboarding workflow for a remote-first technology company.

Requirements:
- Fully digital, minimal manual intervention.
- Integrates with HRIS, IT systems, and learning platforms.
- Covers pre-boarding, first week, and 30-60-90 day check-ins.
- Focus on employee experience and productivity from day one.

Create:
- Step-by-step workflow with responsible parties and triggers.
- List of automated touchpoints (emails, notifications).
- Integration points with other systems.
- Key metrics for success."""
    
    with col_sample2:
        if st.button("Sample: HR Knowledge Base Structure", type="secondary", key="sample_custom_kb_structure"):
            st.session_state['custom_prompt_process'] = """Propose a logical structure and content categories for a new HR knowledge base for a large enterprise.

Goals:
- Improve employee self-service.
- Reduce HR helpdesk tickets.
- Ensure easy navigation and searchability.

Suggest:
- Main categories and sub-categories.
- Examples of articles under each category.
- Best practices for content creation and maintenance.
- Search optimization considerations."""
    
    st.markdown("---")
    
    # Custom prompt input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💭 Your Custom Process Digitization Request")
        custom_prompt_process = st.text_area(
            "Enter your process digitization question/request:",
            height=250,
            value=st.session_state.get('custom_prompt_process', ''),
            placeholder="""Examples:
• Design a workflow for automated leave approval.
• Create a checklist for digitizing employee records.
• Develop a plan for implementing an HR chatbot.
• Generate a guide for creating effective knowledge base articles.
• Propose a strategy for automating internal HR announcements."""
        , key="custom_prompt_process_input")
        
        # Context options
        st.subheader("🎯 Context & Customization")
        col_context1, col_context2 = st.columns(2)
        
        with col_context1:
            company_context_process = st.selectbox(
                "Organization Type",
                ["Technology Company", "Financial Services", "Manufacturing", "Retail", "Healthcare", "Professional Services", "Startup", "Large Enterprise", "Remote-First Company", "Hybrid Model Company", "Custom"],
                index=0,
                key="company_context_process_select"
            )
            
            if company_context_process == "Custom":
                custom_company_process = st.text_input("Enter your organization context:", key="custom_company_process_input")
                company_context_process = custom_company_process
            
            tool_type_process = st.selectbox(
                "Tool Type",
                ["Workflow Design", "Template/Form", "Strategy Document", "Implementation Plan", "Content Structure", "Automation Script", "Other"],
                key="tool_type_process_select"
            )
        
        with col_context2:
            detail_level_process = st.selectbox(
                "Detail Level",
                ["Comprehensive (Detailed)", "Standard (Moderate)", "Overview (High-level)"],
                key="detail_level_process_select"
            )
            
            target_users_process = st.multiselect(
                "Target Users",
                ["HR Team", "Employees", "Managers", "IT Department", "Senior Leadership", "All Stakeholders"],
                default=["HR Team", "Employees"],
                key="target_users_process_multiselect"
            )
    
    with col2:
        st.subheader("🚀 Generate Content")
        
        if st.button("🎨 Generate Custom Process Tool", type="primary", key="generate_custom_process_tool"):
            if custom_prompt_process.strip():
                enhanced_prompt = f"""
                Organization Context: {company_context_process}
                Tool Type: {tool_type_process}
                Target Users: {', '.join(target_users_process)}
                Detail Level: {detail_level_process}
                
                Process Digitization Request: {custom_prompt_process}
                
                Create professional content for HR process digitization that:
                1. Is specific to the organization context provided.
                2. Follows best practices in process automation and HR technology.
                3. Is appropriate for the target users.
                4. Matches the requested detail level.
                5. Is immediately implementable and actionable.
                6. Includes relevant frameworks, templates, or strategies.
                7. Focuses on improving efficiency, consistency, and employee experience.
                8. Considers scalability and integration with existing systems.
                
                If this is a workflow, ensure clear steps, roles, and triggers.
                If this is a content structure, ensure logical organization and user-friendliness.
                If this is an implementation plan, include phases, timelines, and success metrics.
                """
                
                with st.spinner("Creating your custom process digitization tool..."):
                    content = generate_content(enhanced_prompt, "Custom Process Tool")
                    if content:
                        st.session_state.generated_content['custom_process'] = content
            else:
                st.error("Please enter your process digitization request.")
        
        # Additional options
        st.markdown("---")
        st.subheader("📋 Quick Actions")
        
        if st.button("🔄 Clear Form", key="clear_custom_process_form"):
            st.session_state['custom_prompt_process'] = ''
            if 'custom_process' in st.session_state.generated_content:
                del st.session_state.generated_content['custom_process']
            st.rerun()
        
        if st.button("💡 Get Ideas", key="get_custom_process_ideas"):
            st.session_state['custom_prompt_process'] = """Suggest 5 innovative ways to leverage AI in HR process automation:

- AI-powered resume screening and candidate matching.
- Automated onboarding task assignment and tracking.
- Intelligent chatbot for instant HR policy queries.
- Predictive analytics for employee turnover risk.
- AI-driven personalized learning recommendations."""
    
    # Display generated content
    if 'custom_process' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Custom Process Digitization Tool")
        cleaned_content = clean_text(st.session_state.generated_content['custom_process'])
        st.text_area("Custom Process Tool Content", value=cleaned_content, height=400, key="custom_process_output")
        create_download_button(cleaned_content, f"Custom_Process_Tool_{datetime.now().strftime('%Y%m%d_%H%M')}", "📥 Download Process Tool")

# Footer
st.markdown("---")
st.markdown("### 🚀 Ready for the next module?")
st.info("This is Module 6 of 9. Continue building your comprehensive HR toolkit with additional specialized modules.")

# Navigation
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("← Module 5: Industrial Relations", key="nav_prev_process"):
        st.switch_page("pages/05_employee_relations.py")

with col_nav2:
    if st.button("🏠 Main Menu", key="nav_home_process"):
        st.switch_page("pages/00_home.py")

with col_nav3:
    if st.button("Module 7: L&D Development →", key="nav_next_process", type="primary"): # Enabled this button
        st.switch_page("pages/07_learning_development.py")
