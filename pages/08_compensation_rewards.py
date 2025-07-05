import streamlit as st
import google.generativeai as genai
import openai
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="HR Copilot - Compensation & Rewards",
    page_icon="💰",
    layout="wide"
)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {}

# Get API keys from environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Sidebar information
with st.sidebar:
    st.title("🔧 Configuration")
    if st.session_state.get('model_choice', None) == "Gemini (Google)":
        if GEMINI_API_KEY:
            st.success("✅ Gemini API Key loaded")
        else:
            st.error("❌ GEMINI_API_KEY not found")
    else:
        if OPENAI_API_KEY:
            st.success("✅ OpenAI API Key loaded")
        else:
            st.error("❌ OPENAI_API_KEY not found")
    st.markdown("---")
    st.markdown("### 💰 Module 8: Compensation & Rewards")
    st.markdown("Manage rewards and recognition programs effectively")

# Helper functions
def clean_text(text):
    """Remove markdown formatting for clean display"""
    if not text:
        return ""
    cleaned = text.replace('**', '').replace('*', '').replace('###', '').replace('##', '').replace('#', '')
    return cleaned.strip()

def generate_content(prompt, content_type):
    """Generate content using selected AI model"""
    model_choice = st.session_state.get('model_choice', 'Gemini (Google)')
    if model_choice == "Gemini (Google)":
        if not GEMINI_API_KEY:
            st.error("Please add your Gemini API key to the .env file")
            return None
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            system_prompt = """You are a senior HR Compensation & Rewards specialist with 15+ years of experience in designing pay structures, managing incentive programs, and developing recognition frameworks.

CRITICAL INSTRUCTIONS:
- Write ONLY the document content, nothing else
- Do NOT include explanatory text, introductions, or commentary
- Do NOT write phrases like \"Here's a comprehensive...\" or \"I'll create...\")
- Start directly with the document content
- Use simple, clean formatting without markdown symbols
- Use CAPITAL LETTERS for main headings
- Use numbered lists and bullet points with dashes (-)
- Keep language professional, clear, and legally compliant where applicable
- Include specific examples and metrics where relevant
- Make all content immediately usable in corporate environments

Focus on practical, transparent, and motivating solutions that attract, retain, and reward talent fairly."""
            full_prompt = f"{system_prompt}\n\n{prompt}"
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2500,
                )
            )
            return response.text
        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
            return None
    else:
        from openai import OpenAI
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        if not OPENAI_API_KEY:
            st.error("Please add your OpenAI API key to the .env file")
            return None
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.responses.create(
                model="gpt-4.1",
                input=prompt
            )
            return response.output_text
        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
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
st.title("💰 HR Copilot - Compensation & Rewards")
st.markdown("Manage pay structures, incentive programs, and recognition frameworks.")

# Tab layout
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 Pay Revision Letters",
    "🎉 Bonus Communications", 
    "📊 Total Rewards Statements",
    "🏆 Recognition Certificates",
    "📋 R&R Policy Creation",
    "🎨 Custom Compensation Tools"
])

# Tab 1: Pay Revision Letters
with tab1:
    st.header("📄 Pay Revision/Increment Letters")
    st.markdown("Draft formal letters for salary revisions, increments, and promotions.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Letters")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Annual Increment Letter", type="secondary", key="sample_pay_increment"):
            st.session_state.update({
                'employee_name_pay': 'Ravi Kumar',
                'employee_id_pay': 'EMP045',
                'position_pay': 'Senior Software Engineer',
                'department_pay': 'Technology',
                'effective_date_pay': '2025-01-01',
                'old_salary_pay': '₹ 1,000,000',
                'new_salary_pay': '₹ 1,100,000',
                'reason_pay': 'Annual performance review and market adjustment.',
                'letter_type_pay': 'Annual Increment Letter'
            })
    
    with col_sample2:
        if st.button("Promotion Letter with Salary Change", type="secondary", key="sample_pay_promotion"):
            st.session_state.update({
                'employee_name_pay': 'Meera Desai',
                'employee_id_pay': 'EMP067',
                'position_pay': 'Marketing Specialist',
                'department_pay': 'Marketing',
                'effective_date_pay': '2024-09-01',
                'old_salary_pay': '₹ 750,000',
                'new_salary_pay': '₹ 900,000',
                'reason_pay': 'Promotion to Marketing Manager based on outstanding performance and leadership potential.',
                'letter_type_pay': 'Promotion Letter'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Employee & Revision Details")
        employee_name_pay = st.text_input("Employee Name", value=st.session_state.get('employee_name_pay', ''), key="employee_name_pay_input")
        employee_id_pay = st.text_input("Employee ID", value=st.session_state.get('employee_id_pay', ''), key="employee_id_pay_input")
        position_pay = st.text_input("Position/Role", value=st.session_state.get('position_pay', ''), key="position_pay_input")
        department_pay = st.text_input("Department", value=st.session_state.get('department_pay', ''), key="department_pay_input")
        effective_date_pay = st.text_input("Effective Date of Change", value=st.session_state.get('effective_date_pay', ''), placeholder="YYYY-MM-DD", key="effective_date_pay_input")
        
    with col2:
        st.subheader("Financial & Reason Details")
        old_salary_pay = st.text_input("Current Annual Salary", value=st.session_state.get('old_salary_pay', ''), placeholder="e.g., ₹ 800,000", key="old_salary_pay_input")
        new_salary_pay = st.text_input("New Annual Salary", value=st.session_state.get('new_salary_pay', ''), placeholder="e.g., ₹ 900,000", key="new_salary_pay_input")
        reason_pay = st.text_area("Reason for Revision/Increment/Promotion", height=100, value=st.session_state.get('reason_pay', ''), key="reason_pay_input")
        
        letter_type_options = ["Annual Increment Letter", "Promotion Letter", "Salary Adjustment Letter", "Demotion Letter"]
        letter_type_pay = st.selectbox("Type of Letter", letter_type_options, key="letter_type_pay_select")
        
        if st.button("📄 Generate Pay Revision Letter", type="primary", key="generate_pay_letter"):
            if employee_name_pay and new_salary_pay and letter_type_pay:
                prompt = f"""Create a formal {letter_type_pay} for the employee {employee_name_pay}.

Employee ID: {employee_id_pay}
Current Position: {position_pay}
Department: {department_pay}
Effective Date of Change: {effective_date_pay}
Current Annual Salary: {old_salary_pay}
New Annual Salary: {new_salary_pay}
Reason for Revision: {reason_pay}

Ensure the letter is professional, clearly states the changes, effective date, and reason. Include necessary formal greetings, closing, and placeholders for signatures."""

                with st.spinner(f"Creating {letter_type_pay.lower()}..."):
                    content = generate_content(prompt, "Pay Revision Letter")
                    if content:
                        st.session_state.generated_content['pay_revision_letter'] = content
            else:
                st.error("Please fill in Employee Name, New Annual Salary, and select Letter Type.")
    
    # Display generated content
    if 'pay_revision_letter' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated {letter_type_pay}")
        cleaned_content = clean_text(st.session_state.generated_content['pay_revision_letter'])
        st.text_area("Pay Revision Letter Content", value=cleaned_content, height=400, key="pay_revision_output")
        create_download_button(cleaned_content, f"{letter_type_pay.replace(' ', '_')}_{employee_name_pay.replace(' ', '_')}", f"📥 Download {letter_type_pay}")

# Tab 2: Bonus Payout Communications
with tab2:
    st.header("🎉 Bonus Payout Communications")
    st.markdown("Draft communications for annual bonuses, performance bonuses, or special incentives.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Communications")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Annual Performance Bonus Announcement", type="secondary", key="sample_bonus_annual"):
            st.session_state.update({
                'bonus_type': 'Annual Performance Bonus',
                'bonus_recipient_group': 'All Eligible Employees',
                'bonus_payout_date': '2025-03-31',
                'bonus_criteria': 'Based on company and individual performance against FY2024 targets.',
                'bonus_message': 'Celebrate collective achievements and individual contributions.',
                'bonus_contact': 'HR Department'
            })
    
    with col_sample2:
        if st.button("Spot Bonus Notification", type="secondary", key="sample_bonus_spot"):
            st.session_state.update({
                'bonus_type': 'Spot Bonus',
                'bonus_recipient_group': 'Individual Employee',
                'bonus_payout_date': '2024-08-15',
                'bonus_criteria': 'Exceptional contribution to Project Alpha, demonstrating outstanding problem-solving.',
                'bonus_message': 'Recognition of immediate, impactful contribution.',
                'bonus_contact': 'Manager and HR'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bonus Details")
        bonus_type = st.text_input("Type of Bonus", value=st.session_state.get('bonus_type', ''), placeholder="e.g., Annual, Performance, Spot, Project Completion", key="bonus_type_input")
        bonus_recipient_group = st.text_input("Recipient Group (or Employee Name)", value=st.session_state.get('bonus_recipient_group', ''), key="bonus_recipient_group_input")
        bonus_payout_date = st.text_input("Expected Payout Date", value=st.session_state.get('bonus_payout_date', ''), placeholder="YYYY-MM-DD", key="bonus_payout_date_input")
        
    with col2:
        st.subheader("Communication Content")
        bonus_criteria = st.text_area("Criteria for Bonus/Reason for Award", height=100, value=st.session_state.get('bonus_criteria', ''), key="bonus_criteria_input")
        bonus_message = st.text_area("Key Message/Sentiment", height=70, value=st.session_state.get('bonus_message', ''), placeholder="e.g., Congratulations, Thank you for your hard work", key="bonus_message_input")
        bonus_contact = st.text_input("Contact for Questions", value=st.session_state.get('bonus_contact', ''), placeholder="e.g., HR, Finance", key="bonus_contact_input")
        
        if st.button("🎉 Generate Bonus Communication", type="primary", key="generate_bonus_comm"):
            if bonus_type and bonus_recipient_group and bonus_payout_date:
                prompt = f"""Draft a formal communication for a '{bonus_type}' payout.

Recipient Group/Employee: {bonus_recipient_group}
Expected Payout Date: {bonus_payout_date}
Criteria for Bonus/Reason for Award: {bonus_criteria}
Key Message/Sentiment: {bonus_message}
Contact for Questions: {bonus_contact}

The communication should include:
- A clear subject line.
- A congratulatory tone.
- Details about the bonus type and reason for eligibility.
- The expected payout date.
- Instructions for any questions.
- A professional closing.
- Use placeholders like [Employee Name] or [Team Name] where appropriate."""

                with st.spinner(f"Creating {bonus_type.lower()} communication..."):
                    content = generate_content(prompt, "Bonus Communication")
                    if content:
                        st.session_state.generated_content['bonus_comm'] = content
            else:
                st.error("Please fill in Bonus Type, Recipient Group, and Payout Date.")
    
    # Display generated content
    if 'bonus_comm' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated {bonus_type} Communication")
        cleaned_content = clean_text(st.session_state.generated_content['bonus_comm'])
        st.text_area("Bonus Communication Content", value=cleaned_content, height=400, key="bonus_comm_output")
        create_download_button(cleaned_content, f"Bonus_Comm_{bonus_type.replace(' ', '_')}", "📥 Download Bonus Communication")

# Tab 3: Total Rewards Statements
with tab3:
    st.header("📊 Total Rewards Statements")
    st.markdown("Generate comprehensive statements outlining an employee's full compensation and benefits package.")
    
    # Quick sample
    st.subheader("🎯 Quick Sample Statement")
    if st.button("Standard Total Rewards Statement Sample", type="secondary", key="sample_trs"):
        st.session_state.update({
            'employee_name_trs': 'Priya Singh',
            'employee_id_trs': 'EMP099',
            'statement_period_trs': 'January 1, 2024 - December 31, 2024',
            'base_salary_trs': '₹ 1,200,000',
            'bonus_trs': '₹ 150,000 (Performance Bonus)',
            'benefits_trs': 'Health Insurance (Company Paid), Provident Fund (12% of Basic), Gratuity, Life Insurance, Employee Stock Purchase Plan, Wellness Program, Paid Time Off (25 days annual)',
            'perks_trs': 'Meal Vouchers, Transport Allowance, Gym Membership Subsidy, Professional Development Budget',
            'company_contribution_trs': '₹ 250,000 (towards benefits and perks)',
            'statement_purpose_trs': 'To provide a holistic view of the value of their employment beyond just salary.'
        })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Employee & Period Details")
        employee_name_trs = st.text_input("Employee Name", value=st.session_state.get('employee_name_trs', ''), key="employee_name_trs_input")
        employee_id_trs = st.text_input("Employee ID", value=st.session_state.get('employee_id_trs', ''), key="employee_id_trs_input")
        statement_period_trs = st.text_input("Statement Period", value=st.session_state.get('statement_period_trs', ''), placeholder="e.g., Jan 1, 2024 - Dec 31, 2024", key="statement_period_trs_input")
        
    with col2:
        st.subheader("Reward Components")
        base_salary_trs = st.text_input("Base Salary (Annual)", value=st.session_state.get('base_salary_trs', ''), key="base_salary_trs_input")
        bonus_trs = st.text_input("Bonus/Incentives (Total)", value=st.session_state.get('bonus_trs', ''), placeholder="e.g., ₹ 150,000 (Performance Bonus)", key="bonus_trs_input")
        benefits_trs = st.text_area("Benefits (e.g., Health, Retirement, Insurance)", height=100, value=st.session_state.get('benefits_trs', ''), key="benefits_trs_input")
        perks_trs = st.text_area("Perks/Allowances (e.g., Meal, Transport, Wellness)", height=70, value=st.session_state.get('perks_trs', ''), key="perks_trs_input")
        company_contribution_trs = st.text_input("Estimated Company Contribution to Benefits/Perks", value=st.session_state.get('company_contribution_trs', ''), placeholder="e.g., ₹ 250,000", key="company_contribution_trs_input")
        statement_purpose_trs = st.text_area("Purpose/Message of Statement", height=70, value=st.session_state.get('statement_purpose_trs', ''), placeholder="e.g., To highlight total value of employment.", key="statement_purpose_trs_input")
        
        if st.button("📊 Generate Total Rewards Statement", type="primary", key="generate_trs"):
            if employee_name_trs and base_salary_trs:
                prompt = f"""Generate a Total Rewards Statement for {employee_name_trs} for the period {statement_period_trs}.

Employee ID: {employee_id_trs}
Base Salary (Annual): {base_salary_trs}
Bonus/Incentives (Total): {bonus_trs}
Benefits: {benefits_trs}
Perks/Allowances: {perks_trs}
Estimated Company Contribution to Benefits/Perks: {company_contribution_trs}
Purpose/Message of Statement: {statement_purpose_trs}

The statement should clearly itemize all components of their total compensation, including:
- Base Salary
- Variable Pay (Bonuses, Incentives)
- Health & Wellness Benefits
- Retirement & Savings Plans
- Paid Time Off
- Professional Development & Learning
- Other Perks and Allowances
- Total Estimated Value of Rewards

Ensure the statement is professional, easy to understand, and highlights the full value of the employee's package."""

                with st.spinner("Creating Total Rewards Statement..."):
                    content = generate_content(prompt, "Total Rewards Statement")
                    if content:
                        st.session_state.generated_content['total_rewards_statement'] = content
            else:
                st.error("Please fill in Employee Name and Base Salary.")
    
    # Display generated content
    if 'total_rewards_statement' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Total Rewards Statement")
        cleaned_content = clean_text(st.session_state.generated_content['total_rewards_statement'])
        st.text_area("Total Rewards Statement Content", value=cleaned_content, height=400, key="trs_output")
        create_download_button(cleaned_content, f"Total_Rewards_Statement_{employee_name_trs.replace(' ', '_')}", "📥 Download Total Rewards Statement")

# Tab 4: Recognition Certificates
with tab4:
    st.header("🏆 Recognition Certificates")
    st.markdown("Draft templates for employee recognition certificates.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Certificates")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Employee of the Month Certificate", type="secondary", key="sample_cert_eom"):
            st.session_state.update({
                'recipient_name_cert': 'Sarah Johnson',
                'award_type_cert': 'Employee of the Month',
                'award_reason_cert': 'Outstanding dedication to customer satisfaction and consistent positive attitude.',
                'award_date_cert': 'July 2024',
                'issuer_name_cert': 'CEO Office',
                'company_name_cert': 'Innovate Corp'
            })
    
    with col_sample2:
        if st.button("Project Achievement Certificate", type="secondary", key="sample_cert_project"):
            st.session_state.update({
                'recipient_name_cert': 'Team Alpha',
                'award_type_cert': 'Project Excellence Award',
                'award_reason_cert': 'Exceptional teamwork and successful delivery of Project Phoenix ahead of schedule and under budget.',
                'award_date_cert': '2024-06-30',
                'issuer_name_cert': 'Head of Engineering',
                'company_name_cert': 'Tech Solutions Inc.'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Certificate Details")
        recipient_name_cert = st.text_input("Recipient Name (Individual or Team)", value=st.session_state.get('recipient_name_cert', ''), key="recipient_name_cert_input")
        award_type_cert = st.text_input("Type of Award/Recognition", value=st.session_state.get('award_type_cert', ''), placeholder="e.g., Employee of the Year, Service Award, Innovation Award", key="award_type_cert_input")
        award_date_cert = st.text_input("Date of Award/Period", value=st.session_state.get('award_date_cert', ''), placeholder="e.g., July 2024, 2024-06-30", key="award_date_cert_input")
        
    with col2:
        st.subheader("Content & Issuer")
        award_reason_cert = st.text_area("Reason for Award/Achievement", height=100, value=st.session_state.get('award_reason_cert', ''), key="award_reason_cert_input")
        issuer_name_cert = st.text_input("Issuer Name/Department", value=st.session_state.get('issuer_name_cert', ''), placeholder="e.g., CEO, HR Department", key="issuer_name_cert_input")
        company_name_cert = st.text_input("Company Name", value=st.session_state.get('company_name_cert', ''), key="company_name_cert_input")
        
        if st.button("🏆 Generate Recognition Certificate", type="primary", key="generate_certificate"):
            if recipient_name_cert and award_type_cert:
                prompt = f"""Draft a formal Recognition Certificate for '{recipient_name_cert}'.

Award Type: {award_type_cert}
Reason for Award/Achievement: {award_reason_cert}
Date of Award/Period: {award_date_cert}
Issuer Name/Department: {issuer_name_cert}
Company Name: {company_name_cert}

Design the certificate with:
- A prominent title (e.g., Certificate of Achievement).
- Clear statement of recognition.
- Space for recipient's name.
- Description of the achievement/reason.
- Date of issuance.
- Company logo placeholder.
- Signature line for issuer.

Ensure it conveys appreciation and professionalism."""

                with st.spinner("Creating Recognition Certificate..."):
                    content = generate_content(prompt, "Recognition Certificate")
                    if content:
                        st.session_state.generated_content['recognition_certificate'] = content
            else:
                st.error("Please fill in Recipient Name and Award Type.")
    
    # Display generated content
    if 'recognition_certificate' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated {award_type_cert} Certificate")
        cleaned_content = clean_text(st.session_state.generated_content['recognition_certificate'])
        st.text_area("Certificate Content", value=cleaned_content, height=400, key="certificate_output")
        create_download_button(cleaned_content, f"Certificate_{award_type_cert.replace(' ', '_')}_{recipient_name_cert.replace(' ', '_')}", "📥 Download Certificate")

# Tab 5: R&R Policy Creation
with tab5:
    st.header("📋 Rewards & Recognition (R&R) Policy Creation")
    st.markdown("Create summaries or full policy documents for your company's R&R programs.")
    
    # Quick sample
    st.subheader("🎯 Quick Sample Policy")
    if st.button("Comprehensive R&R Policy Sample", type="secondary", key="sample_rnr_policy"):
        st.session_state.update({
            'company_name_rnr': 'Global Innovations Ltd.',
            'policy_purpose_rnr': 'To establish a fair and consistent framework for recognizing and rewarding employee contributions.',
            'policy_scope_rnr': 'All permanent employees.',
            'recognition_types_rnr': 'Spot Recognition, Quarterly Awards, Annual Awards, Service Awards, Innovation Awards.',
            'eligibility_criteria_rnr': 'All employees are eligible, specific criteria apply for each award type.',
            'nomination_process_rnr': 'Peer and Manager nominations via HR portal, reviewed by R&R Committee.',
            'policy_benefits_rnr': 'Increased employee engagement, motivation, retention, and alignment with company values.'
        })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Policy Details")
        company_name_rnr = st.text_input("Company Name", value=st.session_state.get('company_name_rnr', ''), key="company_name_rnr_input")
        policy_purpose_rnr = st.text_area("Purpose of the Policy", height=70, value=st.session_state.get('policy_purpose_rnr', ''), key="policy_purpose_rnr_input")
        policy_scope_rnr = st.text_area("Scope of the Policy (who it applies to)", height=70, value=st.session_state.get('policy_scope_rnr', ''), key="policy_scope_rnr_input")
        
    with col2:
        st.subheader("Program Elements")
        recognition_types_rnr = st.text_area("Types of Recognition/Awards", height=100, value=st.session_state.get('recognition_types_rnr', ''), placeholder="e.g., Spot, Quarterly, Annual, Service", key="recognition_types_rnr_input")
        eligibility_criteria_rnr = st.text_area("Eligibility Criteria", height=70, value=st.session_state.get('eligibility_criteria_rnr', ''), key="eligibility_criteria_rnr_input")
        nomination_process_rnr = st.text_area("Nomination & Selection Process", height=70, value=st.session_state.get('nomination_process_rnr', ''), key="nomination_process_rnr_input")
        policy_benefits_rnr = st.text_area("Expected Benefits of Policy", height=70, value=st.session_state.get('policy_benefits_rnr', ''), key="policy_benefits_rnr_input")
        
        if st.button("📋 Generate R&R Policy", type="primary", key="generate_rnr_policy"):
            if company_name_rnr and policy_purpose_rnr:
                prompt = f"""Create a comprehensive Rewards & Recognition (R&R) Policy for {company_name_rnr}.

Purpose of the Policy: {policy_purpose_rnr}
Scope of the Policy: {policy_scope_rnr}
Types of Recognition/Awards: {recognition_types_rnr}
Eligibility Criteria: {eligibility_criteria_rnr}
Nomination & Selection Process: {nomination_process_rnr}
Expected Benefits of Policy: {policy_benefits_rnr}

The policy should include:
- POLICY STATEMENT (Purpose, Philosophy)
- SCOPE AND APPLICABILITY
- TYPES OF RECOGNITION (Detailed description for each type, e.g., criteria, frequency, reward)
- ELIGIBILITY
- NOMINATION AND SELECTION PROCESS (Steps, roles, committee)
- GUIDELINES FOR MANAGERS
- ADMINISTRATION AND GOVERNANCE
- COMMUNICATION AND PROMOTION
- REVIEW AND REVISION
- EXPECTED OUTCOMES

Ensure the policy is clear, fair, motivating, and aligned with company values."""

                with st.spinner("Creating R&R Policy..."):
                    content = generate_content(prompt, "R&R Policy")
                    if content:
                        st.session_state.generated_content['rnr_policy'] = content
            else:
                st.error("Please fill in Company Name and Purpose of the Policy.")
    
    # Display generated content
    if 'rnr_policy' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Rewards & Recognition Policy")
        cleaned_content = clean_text(st.session_state.generated_content['rnr_policy'])
        st.text_area("R&R Policy Content", value=cleaned_content, height=400, key="rnr_policy_output")
        create_download_button(cleaned_content, f"R_and_R_Policy_{company_name_rnr.replace(' ', '_')}", "📥 Download R&R Policy")

# Tab 6: Custom Compensation Tools
with tab6:
    st.header("🎨 Custom Compensation & Rewards Tools")
    st.markdown("Create any compensation or rewards document, framework, or strategy.")
    
    # Sample prompts
    st.subheader("🎯 Best Practice C&R Prompts")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Sample: Sales Incentive Plan Design", type="secondary", key="sample_custom_sales_incentive"):
            st.session_state['custom_prompt_comp'] = """Design a new sales incentive plan for a B2B SaaS company.

Objectives:
- Drive revenue growth and new customer acquisition.
- Motivate sales team and align with business goals.
- Ensure fairness and transparency.

Include:
- Target audience (e.g., Sales Reps, Sales Managers).
- Key performance indicators (KPIs) for incentives (e.g., revenue, new logos, retention).
- Payout structure (e.g., base salary, commission, bonus).
- Tiered performance levels and accelerators.
- Rules for quota attainment and dispute resolution."""
    
    with col_sample2:
        if st.button("Sample: Compensation Philosophy Statement", type="secondary", key="sample_custom_comp_philosophy"):
            st.session_state['custom_prompt_comp'] = """Draft a Compensation Philosophy Statement for a growing tech startup.

Goals:
- Attract and retain top talent.
- Promote internal equity and external competitiveness.
- Link pay to performance.
- Ensure transparency and understanding.

Cover:
- Guiding principles of compensation.
- Approach to base pay, variable pay, and benefits.
- Market positioning strategy.
- Communication approach for employees.
- Review and adjustment process."""
    
    st.markdown("---")
    
    # Custom prompt input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💭 Your Custom Compensation Request")
        custom_prompt_comp = st.text_area(
            "Enter your compensation/rewards question/request:",
            height=250,
            value=st.session_state.get('custom_prompt_comp', ''),
            placeholder="""Examples:
• Create a framework for job grading and salary banding.
• Design a retention bonus plan for critical roles.
• Develop guidelines for equity compensation (ESOPs).
• Generate a communication plan for annual compensation review.
• Propose a strategy for non-monetary recognition programs."""
        , key="custom_prompt_comp_input")
        
        # Context options
        st.subheader("🎯 Context & Customization")
        col_context1, col_context2 = st.columns(2)
        
        with col_context1:
            company_context_comp = st.selectbox(
                "Organization Type",
                ["Technology Company", "Financial Services", "Manufacturing", "Retail", "Healthcare", "Professional Services", "Startup", "Large Enterprise", "Non-profit", "Government", "Custom"],
                index=0,
                key="company_context_comp_select"
            )
            
            if company_context_comp == "Custom":
                custom_company_comp = st.text_input("Enter your organization context:", key="custom_company_comp_input")
                company_context_comp = custom_company_comp
            
            tool_type_comp = st.selectbox(
                "Tool Type",
                ["Plan Design", "Policy Document", "Framework", "Communication Strategy", "Guidelines", "Analysis Tool", "Other"],
                key="tool_type_comp_select"
            )
        
        with col_context2:
            detail_level_comp = st.selectbox(
                "Detail Level",
                ["Comprehensive (Detailed)", "Standard (Moderate)", "Overview (High-level)"],
                key="detail_level_comp_select"
            )
            
            target_users_comp = st.multiselect(
                "Target Users",
                ["HR Team", "Employees", "Managers", "Senior Leadership", "Finance Team", "All Stakeholders"],
                default=["HR Team", "Managers"],
                key="target_users_comp_multiselect"
            )
    
    with col2:
        st.subheader("🚀 Generate Content")
        
        if st.button("🎨 Generate Custom C&R Tool", type="primary", key="generate_custom_comp_tool"):
            if custom_prompt_comp.strip():
                enhanced_prompt = f"""
                Organization Context: {company_context_comp}
                Tool Type: {tool_type_comp}
                Target Users: {', '.join(target_users_comp)}
                Detail Level: {detail_level_comp}
                
                Compensation & Rewards Request: {custom_prompt_comp}
                
                Create professional content for Compensation & Rewards that:
                1. Is specific to the organization context provided.
                2. Follows best practices in compensation management and reward systems.
                3. Is appropriate for the target users.
                4. Matches the requested detail level.
                5. Is immediately implementable and actionable.
                6. Includes relevant frameworks, policies, or strategies.
                7. Focuses on attracting, retaining, and motivating talent.
                8. Considers fairness, transparency, and legal compliance.
                
                If this is a plan design, ensure clear objectives, KPIs, and payout structures.
                If this is a policy, ensure clarity, enforceability, and alignment with business goals.
                If this is a strategy, include principles, initiatives, and success metrics.
                """
                
                with st.spinner("Creating your custom C&R tool..."):
                    content = generate_content(enhanced_prompt, "Custom Compensation Tool")
                    if content:
                        st.session_state.generated_content['custom_comp'] = content
            else:
                st.error("Please enter your compensation/rewards request.")
        
        # Additional options
        st.markdown("---")
        st.subheader("📋 Quick Actions")
        
        if st.button("🔄 Clear Form", key="clear_custom_comp_form"):
            st.session_state['custom_prompt_comp'] = ''
            if 'custom_comp' in st.session_state.generated_content:
                del st.session_state.generated_content['custom_comp']
            st.rerun()
        
        if st.button("💡 Get Ideas", key="get_custom_comp_ideas"):
            st.session_state['custom_prompt_comp'] = """Suggest 5 innovative compensation and rewards strategies for a modern workforce:

- Personalized benefits packages (flex benefits).
- Skills-based pay models for continuous learning.
- Transparent pay ranges and salary bands.
- Peer-to-peer micro-recognition platforms.
- Equity compensation for all employees (e.g., phantom stock, profit sharing)."""
    
    # Display generated content
    if 'custom_comp' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Custom Compensation & Rewards Tool")
        cleaned_content = clean_text(st.session_state.generated_content['custom_comp'])
        st.text_area("Custom C&R Tool Content", value=cleaned_content, height=400, key="custom_comp_output")
        create_download_button(cleaned_content, f"Custom_Comp_Tool_{datetime.now().strftime('%Y%m%d_%H%M')}", "📥 Download C&R Tool")

# Footer
st.markdown("---")
st.markdown("### 🚀 Ready for the next module?")
st.info("This is Module 8 of 9. Continue building your comprehensive HR toolkit with additional specialized modules.")

# Navigation
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("← Module 7: L&D Development", key="nav_prev_comp"):
        st.switch_page("pages/07_learning_development.py")

with col_nav2:
    if st.button("🏠 Main Menu", key="nav_home_comp"):
        st.switch_page("pages/00_home.py")

with col_nav3:
    if st.button("Module 9: Goal Setting →", key="nav_next_comp", disabled=True):
        st.info("Coming Soon!")