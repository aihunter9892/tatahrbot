import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import base64 # Import base64 for image encoding

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="HR Copilot - Industrial Relations",
    page_icon="⚖️",
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
    st.markdown("### ⚖️ Module 5: Industrial Relations")
    st.markdown("Manage employee relations and compliance effectively")
    
    if st.button("🏠 Back to Main Menu"):
        st.switch_page("hr_copilot_main.py")

# Helper functions
def clean_text(text):
    """Remove markdown formatting for clean display"""
    if not text:
        return ""
    cleaned = text.replace('**', '').replace('*', '').replace('###', '').replace('##', '').replace('#', '')
    return cleaned.strip()

def generate_content(prompt, content_type, image_files=None):
    """Generate content using selected AI model, optionally with images."""
    model_choice = st.session_state.get('model_choice', available_models[0] if available_models else 'Gemini (Google)')
    if model_choice == "Gemini (Google)":
        if not GEMINI_API_KEY:
            st.error("Please add your Gemini API key to the .env file")
            return None
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            system_prompt = """You are a senior HR Industrial Relations specialist with 15+ years of experience in managing employee relations, compliance, disciplinary actions, grievance handling, and union negotiations.

CRITICAL INSTRUCTIONS:
- Write ONLY the document content, nothing else
- Do NOT include explanatory text, introductions, or commentary
- Do NOT write phrases like "Here's a comprehensive..." or "I'll create..."
- Start directly with the document content
- Use simple, clean formatting without markdown symbols
- Use CAPITAL LETTERS for main headings
- Use numbered lists and bullet points with dashes (-)
- Keep language professional, legally compliant, and actionable
- Include specific examples and clauses where relevant
- Make all content immediately usable in corporate environments

Focus on practical, legally sound, and implementable solutions that ensure fair treatment, maintain harmony, and mitigate risks."""
            
            # Prepare the content parts for the Gemini API call
            parts = [system_prompt, prompt]

            if image_files: # Iterate through multiple image files
                for img_file in image_files:
                    # Read image bytes and get mime type from Streamlit's UploadedFile object
                    image_bytes = img_file.getvalue()
                    mime_type = img_file.type
                    
                    parts.append({"inline_data": {"mime_type": mime_type, "data": base64.b64encode(image_bytes).decode('utf-8')}})
            
            response = model.generate_content(
                parts, # Pass the list of content parts
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2500,
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
st.title("⚖️ HR Copilot - Industrial Relations")
st.markdown("Create legally compliant documents and frameworks for employee relations and compliance")

# Tab layout
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([ # Added tab7 for Incident Report
    "📝 Disciplinary Letters/Notices",
    "📋 Grievance Policies", 
    "❓ IR FAQs",
    "📋 Union Meeting Minutes",
    "🤝 Settlement Agreements",
    "🎨 Custom IR Tools",
    "📸 Incident Report" # New tab
])

# Tab 1: Disciplinary Letters/Notices
with tab1:
    st.header("📝 Disciplinary Letters/Notices")
    st.markdown("Draft show-cause notices, warning letters, and other disciplinary communications.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Letters")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("Show-Cause Notice Sample", type="secondary", key="sample_sc_notice"):
            st.session_state.update({
                'employee_name_disc': 'Anjali Sharma',
                'employee_id_disc': 'EMP001',
                'position_disc': 'Customer Service Executive',
                'department_disc': 'Customer Service',
                'manager_disc': 'Sanjay Gupta',
                'incident_date_disc': '2024-06-25',
                'incident_desc_disc': 'Repeated absenteeism without prior notification, impacting team productivity.',
                'policy_violation_disc': 'Company Attendance Policy (Section 3.2)',
                'previous_warnings_disc': 'Verbal warning on 2024-06-10 regarding punctuality.',
                'proposed_action_disc': 'Written warning and mandatory counseling session.',
                'response_deadline_disc': '2024-07-08',
                'letter_type_disc': 'Show-Cause Notice'
            })
    
    with col_sample2:
        if st.button("Warning Letter Sample", type="secondary", key="sample_warning_letter"):
            st.session_state.update({
                'employee_name_disc': 'Rahul Verma',
                'employee_id_disc': 'EMP002',
                'position_disc': 'Sales Representative',
                'department_disc': 'Sales',
                'manager_disc': 'Priya Singh',
                'incident_date_disc': '2024-06-20',
                'incident_desc_disc': 'Failure to meet sales targets for two consecutive quarters despite performance coaching.',
                'policy_violation_disc': 'Company Performance Policy (Section 5.1)',
                'previous_warnings_disc': 'Performance Improvement Plan (PIP) initiated on 2024-03-15.',
                'proposed_action_disc': 'Final written warning and review of PIP progress.',
                'response_deadline_disc': 'N/A',
                'letter_type_disc': 'Warning Letter'
            })
    
    with col_sample3:
        if st.button("Suspension Letter Sample", type="secondary", key="sample_suspension_letter"):
            st.session_state.update({
                'employee_name_disc': 'Deepak Kumar',
                'employee_id_disc': 'EMP003',
                'position_disc': 'Warehouse Supervisor',
                'department_disc': 'Operations',
                'manager_disc': 'Amit Sharma',
                'incident_date_disc': '2024-07-01',
                'incident_desc_disc': 'Alleged violation of safety protocols leading to a minor workplace injury.',
                'policy_violation_disc': 'Company Health & Safety Policy (Section 7.3)',
                'previous_warnings_disc': 'None',
                'proposed_action_disc': 'Temporary suspension pending investigation.',
                'response_deadline_disc': 'N/A',
                'letter_type_disc': 'Suspension Letter'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Employee & Incident Details")
        employee_name_disc = st.text_input("Employee Name", value=st.session_state.get('employee_name_disc', ''), key="employee_name_disc_input")
        employee_id_disc = st.text_input("Employee ID", value=st.session_state.get('employee_id_disc', ''), key="employee_id_disc_input")
        position_disc = st.text_input("Position/Role", value=st.session_state.get('position_disc', ''), key="position_disc_input")
        department_disc = st.text_input("Department", value=st.session_state.get('department_disc', ''), key="department_disc_input")
        manager_disc = st.text_input("Issuing Manager/HR", value=st.session_state.get('manager_disc', ''), key="manager_disc_input")
        incident_date_disc = st.text_input("Date of Incident", value=st.session_state.get('incident_date_disc', ''), placeholder="YYYY-MM-DD", key="incident_date_disc_input")
    
    with col2:
        st.subheader("Disciplinary Specifics")
        incident_desc_disc = st.text_area("Description of Incident/Misconduct", height=100, value=st.session_state.get('incident_desc_disc', ''), key="incident_desc_disc_input")
        policy_violation_disc = st.text_input("Specific Policy/Rule Violated", value=st.session_state.get('policy_violation_disc', ''), key="policy_violation_disc_input")
        previous_warnings_disc = st.text_area("Previous Warnings/Actions (if any)", height=70, value=st.session_state.get('previous_warnings_disc', ''), key="previous_warnings_disc_input")
        proposed_action_disc = st.text_area("Proposed Disciplinary Action", height=70, value=st.session_state.get('proposed_action_disc', ''), key="proposed_action_disc_input")
        response_deadline_disc = st.text_input("Employee Response Deadline (if applicable)", value=st.session_state.get('response_deadline_disc', ''), placeholder="YYYY-MM-DD or N/A", key="response_deadline_disc_input")
        
        letter_type_options = [
            "Show-Cause Notice",
            "First Warning Letter",
            "Final Warning Letter",
            "Suspension Letter",
            "Termination Letter"
        ]
        letter_type_disc = st.selectbox("Type of Letter", letter_type_options, key="letter_type_disc_select")
        
        if st.button("📝 Generate Disciplinary Letter", type="primary", key="generate_disc_letter"):
            if employee_name_disc and incident_desc_disc and letter_type_disc:
                prompt = f"""Create a formal {letter_type_disc} for an employee.

Employee Name: {employee_name_disc}
Employee ID: {employee_id_disc}
Position: {position_disc}
Department: {department_disc}
Issuing Manager/HR: {manager_disc}
Date of Incident: {incident_date_disc}
Description of Incident/Misconduct: {incident_desc_disc}
Specific Policy/Rule Violated: {policy_violation_disc}
Previous Warnings/Actions: {previous_warnings_disc if previous_warnings_disc else 'None'}
Proposed Disciplinary Action: {proposed_action_disc}
Employee Response Deadline: {response_deadline_disc}

Ensure the letter is professional, legally sound, clearly states the facts, refers to company policy, outlines the disciplinary action, and specifies next steps. Include necessary headers and footers for a formal document."""

                with st.spinner(f"Creating {letter_type_disc.lower()}..."):
                    content = generate_content(prompt, "Disciplinary Letter")
                    if content:
                        st.session_state.generated_content['disciplinary_letter'] = content
            else:
                st.error("Please fill in Employee Name, Description of Incident, and select Letter Type.")
    
    # Display generated content
    if 'disciplinary_letter' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated {letter_type_disc}")
        cleaned_content = clean_text(st.session_state.generated_content['disciplinary_letter'])
        st.text_area("Disciplinary Letter Content", value=cleaned_content, height=400, key="disc_letter_output")
        create_download_button(cleaned_content, f"{letter_type_disc.replace(' ', '_')}_{employee_name_disc.replace(' ', '_')}", f"📥 Download {letter_type_disc}")

# Tab 2: Grievance Policies
with tab2:
    st.header("📋 Grievance Policies")
    st.markdown("Develop comprehensive grievance redressal policies and forms.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Policies")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Standard Grievance Policy Sample", type="secondary", key="sample_grievance_policy"):
            st.session_state.update({
                'company_name_grievance': 'Acme Corp',
                'policy_scope_grievance': 'All employees, including permanent, temporary, and contract staff.',
                'grievance_steps_grievance': '1. Informal discussion with immediate manager; 2. Formal complaint to HR; 3. Investigation by HR/Committee; 4. Decision and communication; 5. Appeal process.',
                'confidentiality_clause_grievance': 'All grievance matters will be handled with utmost confidentiality, shared only with those directly involved in the investigation.',
                'appeals_process_grievance': 'Employees may appeal a decision to senior management or a designated appeals committee within 7 working days of receiving the decision.'
            })
    
    with col_sample2:
        if st.button("Grievance Form Template Sample", type="secondary", key="sample_grievance_form"):
            st.session_state.update({
                'company_name_grievance': 'Global Solutions Inc.',
                'policy_scope_grievance': 'N/A (for form template)',
                'grievance_steps_grievance': 'N/A (for form template)',
                'confidentiality_clause_grievance': 'N/A (for form template)',
                'appeals_process_grievance': 'N/A (for form template)'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Policy Information")
        company_name_grievance = st.text_input("Company Name", value=st.session_state.get('company_name_grievance', ''), key="company_name_grievance_input")
        policy_scope_grievance = st.text_area("Policy Scope (who it applies to)", height=70, value=st.session_state.get('policy_scope_grievance', ''), key="policy_scope_grievance_input")
        
    with col2:
        st.subheader("Process Details")
        grievance_steps_grievance = st.text_area("Key Steps in Grievance Process", height=100, value=st.session_state.get('grievance_steps_grievance', ''), key="grievance_steps_grievance_input")
        confidentiality_clause_grievance = st.text_area("Confidentiality Clause", height=70, value=st.session_state.get('confidentiality_clause_grievance', ''), key="confidentiality_clause_grievance_input")
        appeals_process_grievance = st.text_area("Appeals Process", height=70, value=st.session_state.get('appeals_process_grievance', ''), key="appeals_process_grievance_input")
        
        policy_type_options = ["Grievance Redressal Policy", "Grievance Form Template"]
        policy_type_grievance = st.selectbox("Type of Document", policy_type_options, key="policy_type_grievance_select")
        
        if st.button("📋 Generate Grievance Document", type="primary", key="generate_grievance_doc"):
            if company_name_grievance and policy_type_grievance:
                if policy_type_grievance == "Grievance Redressal Policy":
                    prompt = f"""Create a comprehensive Grievance Redressal Policy for {company_name_grievance}.

Policy Scope: {policy_scope_grievance}
Key Steps in Grievance Process: {grievance_steps_grievance}
Confidentiality Clause: {confidentiality_clause_grievance}
Appeals Process: {appeals_process_grievance}

Ensure the policy is clear, fair, legally compliant, and outlines a structured process for employees to raise and resolve grievances. Include sections on purpose, scope, principles, procedure, investigation, decision, and appeals."""
                else: # Grievance Form Template
                    prompt = f"""Create a Grievance Form Template for {company_name_grievance}.

Include sections for:
- Employee Details (Name, ID, Department, Contact)
- Date of Complaint
- Nature of Grievance (brief description)
- Detailed Description of Grievance (with dates, times, individuals involved)
- Supporting Documents (if any)
- Desired Outcome
- Employee Signature and Date
- HR/Management Acknowledgment Section
- Confidentiality statement"""

                with st.spinner(f"Creating {policy_type_grievance.lower()}..."):
                    content = generate_content(prompt, "Grievance Document")
                    if content:
                        st.session_state.generated_content['grievance_doc'] = content
            else:
                st.error("Please fill in Company Name and select Document Type.")
    
    # Display generated content
    if 'grievance_doc' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated {policy_type_grievance}")
        cleaned_content = clean_text(st.session_state.generated_content['grievance_doc'])
        st.text_area("Grievance Document Content", value=cleaned_content, height=400, key="grievance_doc_output")
        create_download_button(cleaned_content, f"Grievance_Policy_{company_name_grievance.replace(' ', '_')}", f"📥 Download {policy_type_grievance}")

# Tab 3: IR FAQs
with tab3:
    st.header("❓ Industrial Relations FAQs")
    st.markdown("Generate common questions and answers related to industrial relations for employees.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample FAQs")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Disciplinary Process FAQs", type="secondary", key="sample_faq_disciplinary"):
            st.session_state.update({
                'ir_topic_faq': 'Disciplinary Process',
                'company_name_faq': 'Tech Innovations Inc.',
                'target_audience_faq': 'All employees',
                'num_faqs': 10
            })
    
    with col_sample2:
        if st.button("Grievance Handling FAQs", type="secondary", key="sample_faq_grievance"):
            st.session_state.update({
                'ir_topic_faq': 'Grievance Handling',
                'company_name_faq': 'Manufacturing Solutions Ltd.',
                'target_audience_faq': 'All employees',
                'num_faqs': 8
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("FAQ Details")
        ir_topic_faq = st.text_input("IR Topic for FAQs", value=st.session_state.get('ir_topic_faq', ''), placeholder="e.g., Disciplinary Process, Grievance Handling, Union Rights", key="ir_topic_faq_input")
        company_name_faq = st.text_input("Company Name", value=st.session_state.get('company_name_faq', ''), key="company_name_faq_input")
        
    with col2:
        st.subheader("Customization")
        target_audience_faq = st.text_input("Target Audience for FAQs", value=st.session_state.get('target_audience_faq', ''), placeholder="e.g., All employees, Managers, Union members", key="target_audience_faq_input")
        num_faqs = st.number_input("Number of FAQs to Generate", min_value=5, max_value=20, value=st.session_state.get('num_faqs', 10), key="num_faqs_input")
        
        if st.button("❓ Generate IR FAQs", type="primary", key="generate_ir_faqs"):
            if ir_topic_faq and company_name_faq:
                prompt = f"""Generate {num_faqs} common Frequently Asked Questions (FAQs) and their answers regarding '{ir_topic_faq}' for employees of {company_name_faq}.

Target Audience: {target_audience_faq}

Ensure the answers are:
- Clear, concise, and easy to understand
- Legally accurate and compliant with general labor laws (state general principles, avoid specific legal advice)
- Actionable where appropriate
- Empathetic and supportive in tone

Include questions covering common concerns, processes, employee rights, and responsibilities related to the topic."""

                with st.spinner(f"Generating {num_faqs} IR FAQs on {ir_topic_faq}..."):
                    content = generate_content(prompt, "IR FAQs")
                    if content:
                        st.session_state.generated_content['ir_faqs'] = content
            else:
                st.error("Please fill in IR Topic and Company Name.")
    
    # Display generated content
    if 'ir_faqs' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated IR FAQs on {ir_topic_faq}")
        cleaned_content = clean_text(st.session_state.generated_content['ir_faqs'])
        st.text_area("IR FAQs Content", value=cleaned_content, height=400, key="ir_faqs_output")
        create_download_button(cleaned_content, f"IR_FAQs_{ir_topic_faq.replace(' ', '_')}", "📥 Download IR FAQs")

# Tab 4: Union Meeting Minutes
with tab4:
    st.header("📋 Union Meeting Minutes Template")
    st.markdown("Draft structured templates for recording union meeting discussions and decisions.")
    
    # Quick sample
    st.subheader("🎯 Quick Sample Template")
    if st.button("Standard Union Meeting Minutes Template", type="secondary", key="sample_union_minutes"):
        st.session_state.update({
            'meeting_date_union': '2024-07-05',
            'meeting_time_union': '10:00 AM - 12:00 PM',
            'meeting_location_union': 'Conference Room A',
            'attendees_union': 'HR Manager, Operations Head, Union Representatives (John Doe, Jane Smith, etc.)',
            'agenda_items_union': 'Review of recent grievance cases, Discussion on new safety protocols, Upcoming collective bargaining agreement.',
            'key_discussions_union': 'Details about each agenda item, points raised by both management and union.',
            'decisions_made_union': 'Agreements reached, resolutions passed.',
            'action_items_union': 'Tasks assigned, responsible parties, deadlines.',
            'next_meeting_union': '2024-08-02, 10:00 AM'
        })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Meeting Details")
        meeting_date_union = st.text_input("Meeting Date", value=st.session_state.get('meeting_date_union', ''), placeholder="YYYY-MM-DD", key="meeting_date_union_input")
        meeting_time_union = st.text_input("Meeting Time", value=st.session_state.get('meeting_time_union', ''), placeholder="e.g., 10:00 AM - 12:00 PM", key="meeting_time_union_input")
        meeting_location_union = st.text_input("Meeting Location", value=st.session_state.get('meeting_location_union', ''), key="meeting_location_union_input")
        attendees_union = st.text_area("Attendees (Management & Union Reps)", height=70, value=st.session_state.get('attendees_union', ''), key="attendees_union_input")
        
    with col2:
        st.subheader("Content for Minutes")
        agenda_items_union = st.text_area("Agenda Items Discussed", height=70, value=st.session_state.get('agenda_items_union', ''), key="agenda_items_union_input")
        key_discussions_union = st.text_area("Key Discussions & Points Raised", height=100, value=st.session_state.get('key_discussions_union', ''), key="key_discussions_union_input")
        decisions_made_union = st.text_area("Decisions Made/Agreements Reached", height=70, value=st.session_state.get('decisions_made_union', ''), key="decisions_made_union_input")
        action_items_union = st.text_area("Action Items, Responsible Parties & Deadlines", height=70, value=st.session_state.get('action_items_union', ''), key="action_items_union_input")
        next_meeting_union = st.text_input("Next Meeting Date/Time (if any)", value=st.session_state.get('next_meeting_union', ''), placeholder="YYYY-MM-DD, HH:MM", key="next_meeting_union_input")
        
        if st.button("📋 Generate Union Meeting Minutes", type="primary", key="generate_union_minutes"):
            if meeting_date_union and attendees_union:
                prompt = f"""Create a formal Union Meeting Minutes template based on the following details:

Meeting Date: {meeting_date_union}
Meeting Time: {meeting_time_union}
Meeting Location: {meeting_location_union}
Attendees: {attendees_union}
Agenda Items Discussed: {agenda_items_union}
Key Discussions & Points Raised: {key_discussions_union}
Decisions Made/Agreements Reached: {decisions_made_union}
Action Items, Responsible Parties & Deadlines: {action_items_union}
Next Meeting Date/Time: {next_meeting_union}

Ensure the minutes are structured, factual, and accurately reflect the discussions and outcomes. Include sections for meeting details, attendees, agenda items, discussions, decisions, action items, and next steps."""

                with st.spinner("Creating Union Meeting Minutes..."):
                    content = generate_content(prompt, "Union Meeting Minutes")
                    if content:
                        st.session_state.generated_content['union_minutes'] = content
            else:
                st.error("Please fill in Meeting Date and Attendees.")
    
    # Display generated content
    if 'union_minutes' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Union Meeting Minutes Template")
        cleaned_content = clean_text(st.session_state.generated_content['union_minutes'])
        st.text_area("Union Meeting Minutes Content", value=cleaned_content, height=400, key="union_minutes_output")
        create_download_button(cleaned_content, f"Union_Meeting_Minutes_{meeting_date_union.replace('-', '')}", "📥 Download Union Meeting Minutes")

# Tab 5: Settlement Agreements
with tab5:
    st.header("🤝 Settlement Agreements")
    st.markdown("Prepare templates for formal settlement agreements in dispute resolution.")
    
    # Quick sample
    st.subheader("🎯 Quick Sample Agreement")
    if st.button("Standard Settlement Agreement Sample", type="secondary", key="sample_settlement_agreement"):
        st.session_state.update({
            'employee_name_settlement': 'Prakash Rao',
            'company_name_settlement': 'Innovate Solutions Ltd.',
            'dispute_summary_settlement': 'Dispute regarding alleged unfair dismissal and claims for unpaid wages.',
            'settlement_terms_settlement': 'Severance payment of 3 months salary, full and final settlement of all claims, non-disparagement clause, mutual release of claims.',
            'release_of_claims_settlement': 'Employee agrees to release company from all past, present, and future claims arising out of employment and its termination.',
            'confidentiality_settlement': 'Both parties agree to keep the terms of this agreement confidential.',
            'governing_law_settlement': 'Laws of India'
        })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parties & Dispute")
        employee_name_settlement = st.text_input("Employee Name", value=st.session_state.get('employee_name_settlement', ''), key="employee_name_settlement_input")
        company_name_settlement = st.text_input("Company Name", value=st.session_state.get('company_name_settlement', ''), key="company_name_settlement_input")
        dispute_summary_settlement = st.text_area("Summary of Dispute/Background", height=100, value=st.session_state.get('dispute_summary_settlement', ''), key="dispute_summary_settlement_input")
        
    with col2:
        st.subheader("Agreement Terms")
        settlement_terms_settlement = st.text_area("Key Settlement Terms (e.g., severance, final pay, non-disclosure)", height=100, value=st.session_state.get('settlement_terms_settlement', ''), key="settlement_terms_settlement_input")
        release_of_claims_settlement = st.text_area("Release of Claims Clause", height=70, value=st.session_state.get('release_of_claims_settlement', ''), key="release_of_claims_settlement_input")
        confidentiality_settlement = st.text_area("Confidentiality Clause", height=70, value=st.session_state.get('confidentiality_settlement', ''), key="confidentiality_settlement_input")
        governing_law_settlement = st.text_input("Governing Law/Jurisdiction", value=st.session_state.get('governing_law_settlement', ''), placeholder="e.g., Laws of India", key="governing_law_settlement_input")
        
        if st.button("🤝 Generate Settlement Agreement", type="primary", key="generate_settlement_agreement"):
            if employee_name_settlement and company_name_settlement and settlement_terms_settlement:
                prompt = f"""Draft a formal Settlement Agreement between {company_name_settlement} and {employee_name_settlement}.

Summary of Dispute/Background: {dispute_summary_settlement}
Key Settlement Terms: {settlement_terms_settlement}
Release of Claims Clause: {release_of_claims_settlement}
Confidentiality Clause: {confidentiality_settlement}
Governing Law/Jurisdiction: {governing_law_settlement}

Ensure the agreement is legally robust, clearly defines the terms of settlement, includes a comprehensive release of claims, and covers standard legal clauses such as confidentiality, non-disparagement, and governing law. Structure it with appropriate headings and signature blocks."""

                with st.spinner("Creating Settlement Agreement..."):
                    content = generate_content(prompt, "Settlement Agreement")
                    if content:
                        st.session_state.generated_content['settlement_agreement'] = content
            else:
                st.error("Please fill in Employee Name, Company Name, and Key Settlement Terms.")
    
    # Display generated content
    if 'settlement_agreement' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Settlement Agreement")
        cleaned_content = clean_text(st.session_state.generated_content['settlement_agreement'])
        st.text_area("Settlement Agreement Content", value=cleaned_content, height=400, key="settlement_agreement_output")
        create_download_button(cleaned_content, f"Settlement_Agreement_{employee_name_settlement.replace(' ', '_')}", "📥 Download Settlement Agreement")

# Tab 6: Custom IR Tools
with tab6:
    st.header("🎨 Custom Industrial Relations Tools")
    st.markdown("Create any industrial relations document, policy, or framework.")
    
    # Sample prompts
    st.subheader("🎯 Best Practice IR Prompts")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Sample: Collective Bargaining Strategy", type="secondary", key="sample_custom_cba"):
            st.session_state['custom_prompt_ir'] = """Develop a collective bargaining strategy for an upcoming negotiation with a labor union.

Context:
- Company: Manufacturing sector, 500 employees, unionized since 1990.
- Key issues: Wage increase demands, benefits review, working hours flexibility, automation impact on jobs.
- Company objectives: Maintain profitability, ensure competitive compensation, improve productivity, avoid strikes.

Create:
- Negotiation objectives and red lines for management.
- Communication strategy for internal stakeholders (employees, non-union staff, management).
- Contingency plans for potential disruptions.
- Key data points and arguments to support company's position.
- Proposed negotiation team structure and roles."""
    
    with col_sample2:
        if st.button("Sample: Employee Code of Conduct", type="secondary", key="sample_custom_code_conduct"):
            st.session_state['custom_prompt_ir'] = """Draft a comprehensive Employee Code of Conduct for a multinational technology company.

Focus Areas:
- Ethical conduct and integrity
- Workplace behavior (harassment, discrimination, respect)
- Conflict of interest
- Confidentiality and data protection
- Use of company assets
- Compliance with laws and regulations
- Reporting violations

Include:
- Purpose and scope.
- Core principles and values.
- Specific behavioral expectations.
- Consequences of non-compliance.
- Reporting mechanisms and whistleblower protection."""
    
    st.markdown("---")
    
    # Custom prompt input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💭 Your Custom Industrial Relations Request")
        custom_prompt_ir = st.text_area(
            "Enter your industrial relations question/request:",
            height=250,
            value=st.session_state.get('custom_prompt_ir', ''),
            placeholder="""Examples:
• Create a policy on workplace bullying and harassment.
• Draft guidelines for conducting internal investigations.
• Develop a communication plan for a plant closure.
• Generate a template for a mutual separation agreement.
• Create a training module on labor law compliance for managers.
• Design a framework for managing employee protests or strikes."""
        , key="custom_prompt_ir_input")
        
        # Context options
        st.subheader("🎯 Context & Customization")
        col_context1, col_context2 = st.columns(2)
        
        with col_context1:
            company_context_ir = st.selectbox(
                "Organization Type",
                ["Technology Company", "Financial Services", "Manufacturing", "Retail", "Healthcare", "Professional Services", "Startup", "Large Enterprise", "Unionized Environment", "Non-Unionized Environment", "Custom"],
                index=0,
                key="company_context_ir_select"
            )
            
            if company_context_ir == "Custom":
                custom_company_ir = st.text_input("Enter your organization context:", key="custom_company_ir_input")
                company_context_ir = custom_company_ir
            
            tool_type_ir = st.selectbox(
                "Tool Type",
                ["Policy Document", "Letter/Notice", "Process/Workflow", "Training Material", "Communication Plan", "Agreement/Contract", "FAQ Document", "Other"],
                key="tool_type_ir_select"
            )
        
        with col_context2:
            detail_level_ir = st.selectbox(
                "Detail Level",
                ["Comprehensive (Detailed)", "Standard (Moderate)", "Overview (High-level)"],
                key="detail_level_ir_select"
            )
            
            target_users_ir = st.multiselect(
                "Target Users",
                ["HR Team", "Managers/Supervisors", "Employees", "Union Representatives", "Senior Leadership", "Legal Counsel", "All Stakeholders"],
                default=["HR Team", "Managers/Supervisors"],
                key="target_users_ir_multiselect"
            )
    
    with col2:
        st.subheader("🚀 Generate Content")
        
        if st.button("🎨 Generate Custom IR Tool", type="primary", key="generate_custom_ir_tool"):
            if custom_prompt_ir.strip():
                enhanced_prompt = f"""
                Organization Context: {company_context_ir}
                Tool Type: {tool_type_ir}
                Target Users: {', '.join(target_users_ir)}
                Detail Level: {detail_level_ir}
                
                Industrial Relations Request: {custom_prompt_ir}
                
                Create professional industrial relations content that:
                1. Is specific to the organization context provided.
                2. Follows best practices in employee relations and labor law compliance.
                3. Is appropriate for the target users.
                4. Matches the requested detail level.
                5. Is immediately implementable and actionable.
                6. Includes relevant frameworks, templates, or processes.
                7. Promotes fair treatment and maintains workplace harmony.
                8. Helps mitigate legal and operational risks.
                
                If this is a policy, ensure clarity, enforceability, and compliance.
                If this is a letter, ensure formality, accuracy, and adherence to due process.
                If this is a process, ensure clear steps, roles, and accountability.
                """
                
                with st.spinner("Creating your custom industrial relations tool..."):
                    content = generate_content(enhanced_prompt, "Custom IR Tool")
                    if content:
                        st.session_state.generated_content['custom_ir'] = content
            else:
                st.error("Please enter your industrial relations request.")
        
        # Additional options
        st.markdown("---")
        st.subheader("📋 Quick Actions")
        
        if st.button("🔄 Clear Form", key="clear_custom_ir_form"):
            st.session_state['custom_prompt_ir'] = ''
            if 'custom_ir' in st.session_state.generated_content:
                del st.session_state.generated_content['custom_ir']
            st.rerun()
        
        if st.button("💡 Get Ideas", key="get_custom_ir_ideas"):
            st.session_state['custom_prompt_ir'] = """Suggest 5 key components of a robust employee grievance management system for a large enterprise:

- Clear and accessible grievance reporting channels (e.g., online portal, HR contact, ombudsman).
- Defined multi-stage grievance resolution process with clear timelines for each step.
- Impartial investigation procedures ensuring fairness and confidentiality.
- Training for managers and HR on grievance handling and conflict resolution.
- Documentation and record-keeping protocols for all grievance cases."""
    
    # Display generated content
    if 'custom_ir' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Custom Industrial Relations Tool")
        cleaned_content = clean_text(st.session_state.generated_content['custom_ir'])
        st.text_area("Custom IR Tool Content", value=cleaned_content, height=400, key="custom_ir_output")
        create_download_button(cleaned_content, f"Custom_IR_Tool_{datetime.now().strftime('%Y%m%d_%H%M')}", "📥 Download IR Tool")

# Tab 7: Incident Report (New Tab)
with tab7:
    st.header("📸 Incident Report")
    st.markdown("Generate a detailed incident report based on provided information and **multiple optional photos**.") # Updated description

    st.subheader("Incident Details")
    col_ir1, col_ir2 = st.columns(2)

    with col_ir1:
        # Prefill data from the image
        incident_type = st.text_input("Type of Incident", value="Accident by truck", key="incident_type_input")
        incident_date_time = st.text_input("Date & Time of Incident", value="2025-07-05", key="incident_date_time_input")
        incident_location = st.text_input("Location of Incident", value="Outside of Tata motors plant", key="incident_location_input")
        involved_parties = st.text_area("Involved Parties (Names, Roles, IDs)", height=70, value="Driver details", key="involved_parties_input")
        
    with col_ir2:
        # Prefill data from the image
        incident_description = st.text_area("Detailed Description of Incident", height=150, value="truck being hit by a waterhose", key="incident_description_input")
        incident_impact = st.text_area("Immediate Impact/Consequences", height=70, value="Check images for the same", key="incident_impact_input")
        actions_taken = st.text_area("Immediate Actions Taken", height=70, value="Please figure on your own", key="actions_taken_input")
        
    st.markdown("---")
    st.subheader("Upload Supporting Photos (Optional)")
    # Changed to allow multiple files
    uploaded_photos = st.file_uploader("Upload one or more images related to the incident", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="incident_photos_uploader")

    if uploaded_photos:
        st.write(f"Uploaded {len(uploaded_photos)} photo(s).")
        for i, photo in enumerate(uploaded_photos):
            st.image(photo, caption=f"Uploaded Incident Photo {i+1}", use_column_width=True)

    if st.button("📝 Generate Incident Report", type="primary", key="generate_incident_report"):
        if incident_type and incident_date_time and incident_location and incident_description:
            # Adjust prompt to indicate multiple images might be present
            image_hint = "Analyze the provided image(s) in conjunction with the textual description to enhance the report." if uploaded_photos else ""
            report_prompt = f"""Generate a comprehensive Incident Report based on the following details:

Incident Type: {incident_type}
Date & Time of Incident: {incident_date_time}
Location of Incident: {incident_location}
Involved Parties: {involved_parties if involved_parties else 'N/A'}
Detailed Description of Incident: {incident_description}
Immediate Impact/Consequences: {incident_impact if incident_impact else 'N/A'}
Immediate Actions Taken: {actions_taken if actions_taken else 'N/A'}

{image_hint}
The report should include sections for:
- INCIDENT OVERVIEW
- DETAILS OF INCIDENT (factual account)
- INVOLVED PARTIES
- IMMEDIATE ACTIONS TAKEN
- WITNESS STATEMENTS (if applicable, suggest placeholder)
- FINDINGS/PRELIMINARY ASSESSMENT
- RECOMMENDATIONS FOR PREVENTATIVE ACTIONS
- FOLLOW-UP ACTIONS REQUIRED
- REPORT PREPARED BY (placeholder)
- DATE OF REPORT"""

            with st.spinner("Generating incident report..."):
                # Pass the list of uploaded photos
                content = generate_content(report_prompt, "Incident Report", image_files=uploaded_photos)
                if content:
                    st.session_state.generated_content['incident_report'] = content
        else:
            st.error("Please fill in Incident Type, Date & Time, Location, and Detailed Description.")

    if 'incident_report' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Incident Report")
        cleaned_content = clean_text(st.session_state.generated_content['incident_report'])
        st.text_area("Incident Report Content", value=cleaned_content, height=500, key="incident_report_output")
        create_download_button(cleaned_content, f"Incident_Report_{incident_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}", "📥 Download Incident Report")

# Footer
st.markdown("---")
st.markdown("### 🚀 Ready for the next module?")
st.info("This is Module 5 of 9. Continue building your comprehensive HR toolkit with additional specialized modules.")

# Navigation
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("← Module 4: Performance Management", key="nav_prev_ir"):
        st.switch_page("pages/04_performance_management.py")

with col_nav2:
    if st.button("🏠 Back to Main Menu"):
        st.switch_page("pages/00_home.py")

with col_nav3:
    # This button is now enabled as Module 6 is the next logical step.
    if st.button("Module 6: Process Digitization →", key="nav_next_ir", disabled=True): # Keep disabled for now as Module 6 is not yet built
        st.info("Coming Soon!")
