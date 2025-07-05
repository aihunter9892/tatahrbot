import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="HR Copilot - Talent Acquisition & Onboarding",
    page_icon="🎯",
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
    st.markdown("### 🎯 Module 3: Talent Acquisition & Onboarding")
    st.markdown("Streamline hiring and onboarding processes with AI-powered tools")
    
    if st.button("🏠 Back to Main Menu"):
        st.switch_page("hr_copilot_main.py")

# Main title
st.title("🎯 HR Copilot - Talent Acquisition & Onboarding Module")
st.markdown("Create comprehensive hiring workflows and seamless onboarding experiences")

# Helper functions for proper formatting and downloads
def clean_markdown_text(text):
    """Remove markdown formatting for clean display and downloads"""
    if not text:
        return ""
    
    # Remove markdown formatting
    cleaned = text.replace('**', '').replace('*', '').replace('###', '').replace('##', '').replace('#', '')
    cleaned = cleaned.replace('---', '─' * 50)
    cleaned = cleaned.replace('===', '═' * 50)
    
    # Clean up extra spaces and normalize line breaks
    lines = [line.strip() for line in cleaned.split('\n')]
    cleaned = '\n'.join(lines)
    
    # Remove multiple consecutive empty lines
    while '\n\n\n' in cleaned:
        cleaned = cleaned.replace('\n\n\n', '\n\n')
    
    return cleaned.strip()

def format_letter_with_letterhead(content, document_type, candidate_name, position, date):
    """Format letter with Tata Motors letterhead and proper formatting"""
    # Clean the content first
    cleaned_content = clean_markdown_text(content)
    
    # Remove any existing letterhead or redundant information
    if cleaned_content.startswith("Here's"):
        lines = cleaned_content.split('\n')
        start_index = 0
        for i, line in enumerate(lines):
            if 'Dear' in line and candidate_name.split()[0] in line:
                start_index = i
                break
        cleaned_content = '\n'.join(lines[start_index:])
    
    formatted_content = f"""TATA MOTORS LIMITED
Bombay House, 24 Homi Mody Street
Mumbai - 400 001, Maharashtra, India
Tel: +91-22-6665-8282 | Fax: +91-22-6665-7799
Email: investors@tatamotors.com | Website: www.tatamotors.com

{'═' * 80}

Date: {date}

{document_type.upper()}

{cleaned_content}


We look forward to welcoming you to the Tata Motors family.

Warm regards,


_________________________
Human Resources Department
Tata Motors Limited


{'═' * 80}
This is a computer-generated document and does not require a physical signature.
Tata Motors Limited | CIN: L28920MH1945PLC004520
Registered Office: Bombay House, 24 Homi Mody Street, Mumbai - 400 001
{'═' * 80}"""
    return formatted_content

def create_html_content(content, document_type, candidate_name):
    """Create properly formatted HTML content"""
    # Clean the content
    cleaned_content = clean_markdown_text(content)
    
    # Convert to HTML with proper formatting
    html_content = cleaned_content.replace('\n\n', '</p><p>').replace('\n', '<br>')
    html_content = f"<p>{html_content}</p>"
    
    # Replace section dividers
    html_content = html_content.replace('═' * 80, '<hr style="border: 2px solid #004d9f; margin: 20px 0;">')
    html_content = html_content.replace('─' * 50, '<hr style="border: 1px solid #ccc; margin: 15px 0;">')
    
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{document_type} - {candidate_name}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @page {{
            margin: 1in;
            size: A4;
        }}
        body {{
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: white;
            color: #000;
            max-width: 800px;
            margin: 0 auto;
        }}
        .letterhead {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #004d9f;
        }}
        .company-name {{
            color: #004d9f;
            font-size: 18pt;
            font-weight: bold;
            margin-bottom: 8px;
            letter-spacing: 2px;
        }}
        .company-address {{
            font-size: 10pt;
            line-height: 1.4;
            color: #333;
        }}
        .document-title {{
            text-align: center;
            font-size: 14pt;
            font-weight: bold;
            margin: 30px 0;
            text-decoration: underline;
        }}
        .content {{
            margin: 20px 0;
            text-align: justify;
        }}
        .signature-section {{
            margin-top: 40px;
            margin-bottom: 30px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #004d9f;
            font-size: 9pt;
            color: #666;
            text-align: center;
        }}
        hr {{
            border: none;
            border-top: 2px solid #004d9f;
            margin: 20px 0;
        }}
        p {{
            margin: 10px 0;
        }}
        @media print {{
            body {{ 
                margin: 0; 
                padding: 15mm; 
                font-size: 11pt;
            }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="content">
        {html_content}
    </div>
    
    <script>
        // Auto-print functionality
        function printDocument() {{
            window.print();
        }}
        
        // PDF conversion hint
        function convertToPDF() {{
            alert('To convert to PDF: Open this file in your browser and use "Print to PDF" option in the print dialog.');
        }}
    </script>
</body>
</html>"""
    return full_html

def create_word_doc_content(content, document_type, candidate_name):
    """Create proper Word document content in DOC format"""
    # Clean the content
    cleaned_content = clean_markdown_text(content)
    
    # Create Word-compatible HTML that can be saved as .doc
    word_html = f"""<html xmlns:o="urn:schemas-microsoft-com:office:office" 
xmlns:w="urn:schemas-microsoft-com:office:word" 
xmlns="http://www.w3.org/TR/REC-html40">

<head>
<meta http-equiv=Content-Type content="text/html; charset=utf-8">
<meta name=ProgId content=Word.Document>
<meta name=Generator content="Microsoft Word">
<meta name=Originator content="Microsoft Word">
<title>{document_type} - {candidate_name}</title>

<style>
@page {{
    size: 8.5in 11in;
    margin: 1in;
}}
body {{
    font-family: "Times New Roman", serif;
    font-size: 12pt;
    line-height: 1.5;
    margin: 0;
    padding: 0;
    text-align: left;
}}
.letterhead {{
    text-align: center;
    margin-bottom: 20pt;
    padding-bottom: 15pt;
    border-bottom: 2pt solid #004d9f;
}}
.company-name {{
    font-size: 16pt;
    font-weight: bold;
    color: #004d9f;
    margin-bottom: 8pt;
}}
.company-address {{
    font-size: 10pt;
    line-height: 1.3;
}}
.content {{
    text-align: left;
    margin-top: 15pt;
}}
.footer {{
    margin-top: 30pt;
    padding-top: 15pt;
    border-top: 1pt solid #004d9f;
    font-size: 9pt;
    text-align: center;
}}
p {{
    margin: 6pt 0;
    text-align: left;
}}
</style>
</head>

<body>
<div class="letterhead">
    <div class="company-name">TATA MOTORS LIMITED</div>
    <div class="company-address">
        Bombay House, 24 Homi Mody Street<br>
        Mumbai - 400 001, Maharashtra, India<br>
        Tel: +91-22-6665-8282 | Fax: +91-22-6665-7799<br>
        Email: investors@tatamotors.com | Website: www.tatamotors.com
    </div>
</div>

<div class="content">
{cleaned_content.replace(chr(10), '<br>').replace('  ', '&nbsp;&nbsp;')}
</div>

<div class="footer">
    This is a computer-generated document and does not require a physical signature.<br>
    Tata Motors Limited | CIN: L28920MH1945PLC004520<br>
    Registered Office: Bombay House, 24 Homi Mody Street, Mumbai - 400 001
</div>

</body>
</html>"""
    return word_html

def create_download_options(content, filename_base, candidate_name, document_type):
    """Create multiple download format options with proper formatting"""
    
    # Clean content for all formats
    cleaned_content = clean_markdown_text(content)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Text format download
        st.download_button(
            label="📄 Download as Text",
            data=cleaned_content,
            file_name=f"{filename_base}.txt",
            mime="text/plain",
            help="Plain text format for basic editing"
        )
    
    with col2:
        # HTML format for better formatting
        html_content = create_html_content(content, document_type, candidate_name)
        st.download_button(
            label="🌐 Download as HTML",
            data=html_content,
            file_name=f"{filename_base}.html",
            mime="text/html",
            help="HTML format for web viewing and PDF conversion"
        )
    
    with col3:
        # DOC format for Word compatibility (HTML saved as .doc)
        word_doc_content = create_word_doc_content(content, document_type, candidate_name)
        st.download_button(
            label="📝 Download as Word",
            data=word_doc_content,
            file_name=f"{filename_base}.doc",
            mime="application/msword",
            help="Word document format that opens directly in Microsoft Word"
        )
    
    with col4:
        # Markdown format
        markdown_content = f"""# {document_type} - {candidate_name}

{cleaned_content}

---
*Generated by Tata Motors HR Copilot*
*Document Type: {document_type}*
*Generated on: {datetime.now().strftime("%B %d, %Y")}*
"""
        st.download_button(
            label="📝 Download Markdown",
            data=markdown_content,
            file_name=f"{filename_base}.md",
            mime="text/markdown",
            help="Clean markdown format for documentation"
        )

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
            
            system_prompt = """You are an expert HR professional specializing in talent acquisition and employee onboarding. 

CRITICAL INSTRUCTIONS:
- Write ONLY the document content, nothing else
- Do NOT include explanatory text, introductions, or commentary
- Do NOT write phrases like "Here's a comprehensive..." or "Following best practices..."
- Do NOT use markdown formatting (**, *, ###, etc.)
- Start directly with the document content
- Use simple, clean formatting with clear structure
- Use plain text headings in CAPITAL LETTERS
- Use simple bullet points with dashes (-) or numbers
- Keep language professional but concise
- Make documents business-ready without additional editing

Generate clean, professional HR documents that are immediately usable."""
            
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2000,
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

# Tab layout for different features
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📝 Job Description Generator",
    "🔍 CV vs JD Comparison", 
    "📄 Offer Letters & Contracts",
    "✅ Pre-joining Checklists",
    "📅 30-60-90 Day Plans",
    "📧 Welcome Communications",
    "🎨 Custom Acquisition Assistant"
])

# Tab 1: Job Description Generator
with tab1:
    st.header("📝 Job Description Generator")
    st.markdown("Create inclusive, bias-free job descriptions that attract diverse talent")
    
    # Sample data for Tata Motors
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("⚙️ Sample 1: EV Software Engineer", type="secondary", key="jd1"):
            st.session_state.update({
                'job_title': 'Senior Software Engineer - Electric Vehicle Systems',
                'department_jd': 'Engineering - Electric Vehicle Division',
                'reporting_manager': 'Head of EV Software Development',
                'job_level': 'Senior Level',
                'employment_type': 'Full-time',
                'location_jd': 'Pune, Maharashtra',
                'job_purpose': 'Develop and maintain software systems for electric vehicle powertrains, battery management, and vehicle connectivity features',
                'key_responsibilities': 'Design and implement EV software architecture\nDevelop battery management system algorithms\nIntegrate vehicle connectivity and IoT features\nCollaborate with hardware teams on system optimization\nEnsure compliance with automotive safety standards\nMentor junior developers and conduct code reviews',
                'required_qualifications': 'Bachelor\'s in Computer Science, Electronics, or related field\n5+ years of experience in automotive software development\nProficiency in C/C++, Python, and embedded systems\nExperience with CAN bus, LIN, and automotive protocols\nKnowledge of battery management systems\nUnderstanding of ISO 26262 functional safety standards',
                'preferred_qualifications': 'Master\'s degree in relevant field\nExperience with electric vehicle development\nKnowledge of AUTOSAR architecture\nFamiliarity with Agile development methodologies\nExperience with simulation tools (MATLAB/Simulink)\nPrevious experience in automotive OEM or Tier 1 supplier',
                'company_benefits': 'Competitive salary with performance bonuses\nComprehensive health insurance for family\nEmployee vehicle purchase scheme\nProfessional development and training opportunities\nFlexible working arrangements\nRetirement benefits and stock options'
            })
    
    with col_sample2:
        if st.button("📊 Sample 2: Digital Marketing Manager", type="secondary", key="jd2"):
            st.session_state.update({
                'job_title': 'Digital Marketing Manager - Commercial Vehicles',
                'department_jd': 'Marketing & Sales',
                'reporting_manager': 'Head of Digital Marketing',
                'job_level': 'Manager',
                'employment_type': 'Full-time',
                'location_jd': 'Mumbai, Maharashtra',
                'job_purpose': 'Lead digital marketing strategies for commercial vehicle segment to drive brand awareness, lead generation, and customer engagement',
                'key_responsibilities': 'Develop and execute comprehensive digital marketing campaigns\nManage social media presence and content strategy\nOptimize website performance and SEO rankings\nLead performance marketing across Google Ads, Facebook, LinkedIn\nAnalyze campaign performance and provide insights\nCollaborate with sales teams on lead nurturing strategies\nManage digital marketing budget and vendor relationships',
                'required_qualifications': 'Bachelor\'s degree in Marketing, Business, or related field\n4+ years of digital marketing experience\nProficiency in Google Analytics, Google Ads, Facebook Business Manager\nExperience with marketing automation tools\nStrong analytical and data interpretation skills\nExcellent communication and presentation abilities',
                'preferred_qualifications': 'MBA in Marketing\nExperience in B2B marketing, preferably automotive\nCertifications in Google Ads, Facebook Marketing\nKnowledge of CRM systems and marketing automation\nExperience with video marketing and content creation\nFamiliarity with marketing attribution models',
                'company_benefits': 'Competitive compensation package\nHealth and wellness benefits\nLearning and development budget\nFlexible work arrangements\nEmployee assistance programs\nCareer progression opportunities'
            })
    
    with col_sample3:
        if st.button("🏭 Sample 3: Production Supervisor", type="secondary", key="jd3"):
            st.session_state.update({
                'job_title': 'Production Supervisor - Assembly Line',
                'department_jd': 'Manufacturing Operations',
                'reporting_manager': 'Production Manager',
                'job_level': 'Mid Level',
                'employment_type': 'Full-time',
                'location_jd': 'Lucknow, Uttar Pradesh',
                'job_purpose': 'Supervise daily production operations ensuring quality, safety, and efficiency targets are met while leading and developing the production team',
                'key_responsibilities': 'Supervise assembly line operations and production schedules\nEnsure quality standards and safety protocols are maintained\nLead and motivate production team members\nMonitor production metrics and implement improvements\nConduct daily team briefings and safety meetings\nCoordinate with maintenance teams for equipment uptime\nTrain new operators and conduct performance evaluations',
                'required_qualifications': 'Diploma/Bachelor\'s in Mechanical Engineering or related field\n3+ years of manufacturing/production experience\nKnowledge of lean manufacturing principles\nStrong leadership and team management skills\nUnderstanding of safety regulations and quality systems\nProficiency in production planning and scheduling',
                'preferred_qualifications': 'Experience in automotive manufacturing\nKnowledge of Six Sigma or Kaizen methodologies\nFamiliarity with ERP systems\nMultilingual communication skills (Hindi, English)\nPrevious supervisory experience\nCertification in safety management',
                'company_benefits': 'Attractive salary package\nMedical benefits for employee and family\nTransportation and meal allowances\nSkill development and training programs\nPerformance-based incentives\nJob security and career growth opportunities'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Job Details")
        job_title = st.text_input("Job Title", value=st.session_state.get('job_title', ''), key="jd_job_title")
        department_jd = st.text_input("Department", value=st.session_state.get('department_jd', ''), key="jd_department")
        reporting_manager = st.text_input("Reporting Manager", value=st.session_state.get('reporting_manager', ''), key="jd_reporting_manager")
        
        job_level_options = ["Entry Level", "Mid Level", "Senior Level", "Manager", "Senior Manager", "Director", "VP"]
        current_job_level = st.session_state.get('job_level', 'Mid Level')
        try:
            job_level_index = job_level_options.index(current_job_level)
        except ValueError:
            job_level_index = 1
        job_level = st.selectbox("Job Level", job_level_options, index=job_level_index, key="jd_job_level")
        
        employment_type_options = ["Full-time", "Part-time", "Contract", "Internship", "Temporary"]
        current_employment = st.session_state.get('employment_type', 'Full-time')
        try:
            employment_index = employment_type_options.index(current_employment)
        except ValueError:
            employment_index = 0
        employment_type = st.selectbox("Employment Type", employment_type_options, index=employment_index, key="jd_employment_type")
        
        location_jd = st.text_input("Location", value=st.session_state.get('location_jd', ''), key="jd_location")
    
    with col2:
        st.subheader("Job Content")
        job_purpose = st.text_area("Job Purpose/Summary", height=80, value=st.session_state.get('job_purpose', ''))
        key_responsibilities = st.text_area("Key Responsibilities (one per line)", height=120, value=st.session_state.get('key_responsibilities', ''))
        required_qualifications = st.text_area("Required Qualifications", height=100, value=st.session_state.get('required_qualifications', ''))
        preferred_qualifications = st.text_area("Preferred Qualifications", height=80, value=st.session_state.get('preferred_qualifications', ''))
        company_benefits = st.text_area("Company Benefits", height=80, value=st.session_state.get('company_benefits', ''))
        
        if st.button("📝 Generate Job Description", type="primary"):
            if job_title and key_responsibilities:
                prompt = f"""
                Create a comprehensive, inclusive, and bias-free job description for:
                
                Job Title: {job_title}
                Department: {department_jd}
                Reporting Manager: {reporting_manager}
                Job Level: {job_level}
                Employment Type: {employment_type}
                Location: {location_jd}
                
                Job Purpose: {job_purpose}
                Key Responsibilities: {key_responsibilities}
                Required Qualifications: {required_qualifications}
                Preferred Qualifications: {preferred_qualifications}
                Company Benefits: {company_benefits}
                
                Please create a detailed job description that includes:
                1. Company Overview (brief)
                2. Position Summary
                3. Key Responsibilities (well-structured)
                4. Required Qualifications and Skills
                5. Preferred Qualifications
                6. What We Offer (benefits and growth opportunities)
                7. How to Apply
                8. Equal Opportunity Statement
                
                Ensure the language is:
                - Inclusive and free from gender, age, or cultural bias
                - Clear and engaging
                - Professional yet approachable
                - Focused on skills and competencies rather than years of experience
                - Attractive to diverse candidates
                
                Use clean formatting without markdown symbols.
                """
                
                with st.spinner("Creating your job description..."):
                    content = generate_content(prompt, "Job Description")
                    if content:
                        st.session_state.generated_content['job_description'] = content
            else:
                st.error("Please fill in Job Title and Key Responsibilities")
    
    # Display generated job description
    if 'job_description' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Job Description")
        
        # Display cleaned content
        cleaned_content = clean_markdown_text(st.session_state.generated_content['job_description'])
        st.text_area(
            "Job Description Content",
            value=cleaned_content,
            height=400,
            help="Clean formatted job description ready for use"
        )
        
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                label="📥 Download Job Description",
                data=cleaned_content,
                file_name=f"JD_{job_title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        with col_dl2:
            if st.button("🔍 Check for Bias", key="bias_check"):
                bias_prompt = f"""
                Analyze the following job description for potential bias and suggest improvements:
                
                {st.session_state.generated_content['job_description']}
                
                Please check for:
                1. Gender bias in language
                2. Age discrimination indicators
                3. Cultural or educational bias
                4. Unnecessary experience requirements
                5. Exclusive language that might deter diverse candidates
                
                Provide specific suggestions for improvement.
                Use clean formatting without markdown symbols.
                """
                
                with st.spinner("Checking for bias..."):
                    bias_analysis = generate_content(bias_prompt, "Bias Analysis")
                    if bias_analysis:
                        st.session_state.generated_content['bias_analysis'] = bias_analysis
    
    # Display bias analysis if available
    if 'bias_analysis' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("🔍 Bias Analysis & Recommendations")
        cleaned_bias = clean_markdown_text(st.session_state.generated_content['bias_analysis'])
        st.text_area(
            "Bias Analysis Results",
            value=cleaned_bias,
            height=300,
            help="Bias analysis and improvement recommendations"
        )

# Tab 2: CV vs JD Comparison
with tab2:
    st.header("🔍 CV vs Job Description Comparison")
    st.markdown("AI-powered candidate ranking and assessment against job requirements")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Job Description")
        jd_for_comparison = st.text_area(
            "Paste Job Description or Key Requirements", 
            height=200,
            placeholder="Paste the job description or key requirements here..."
        )
    
    with col2:
        st.subheader("Candidate CV/Resume")
        cv_content = st.text_area(
            "Paste Candidate CV/Resume Content",
            height=200,
            placeholder="Paste the candidate's CV/resume content here..."
        )
    
    if st.button("🔍 Analyze CV vs JD Match", type="primary"):
        if jd_for_comparison and cv_content:
            prompt = f"""
            Analyze the following candidate's CV against the job requirements and provide a detailed assessment:
            
            JOB REQUIREMENTS:
            {jd_for_comparison}
            
            CANDIDATE CV:
            {cv_content}
            
            Please provide:
            1. Overall Match Score (1-5 scale where 5 is perfect match)
            2. Detailed Analysis by category:
               - Technical Skills Match (1-5 with reasoning)
               - Experience Relevance (1-5 with reasoning)
               - Education/Qualifications (1-5 with reasoning)
               - Cultural Fit Indicators (1-5 with reasoning)
            3. Strengths of the candidate
            4. Areas of concern or gaps
            5. Specific questions to ask during interview
            6. Recommendation (Strong Fit / Good Fit / Moderate Fit / Poor Fit)
            
            Be objective and provide specific examples from the CV to support your ratings.
            Use clean formatting without markdown symbols.
            """
            
            with st.spinner("Analyzing CV against job requirements..."):
                content = generate_content(prompt, "CV Analysis")
                if content:
                    st.session_state.generated_content['cv_analysis'] = content
        else:
            st.error("Please provide both Job Description and CV content")
    
    # Display CV analysis
    if 'cv_analysis' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📊 CV vs JD Analysis Results")
        cleaned_analysis = clean_markdown_text(st.session_state.generated_content['cv_analysis'])
        st.text_area(
            "Analysis Results",
            value=cleaned_analysis,
            height=400,
            help="Complete CV vs JD analysis results"
        )
        
        st.download_button(
            label="📥 Download Analysis Report",
            data=cleaned_analysis,
            file_name=f"CV_Analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )

# Tab 3: Offer Letters & Contracts
with tab3:
    st.header("📄 Offer Letters & Contracts")
    
    # Sample data
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("💼 Sample 1: Software Engineer Offer", type="secondary", key="offer1"):
            st.session_state.update({
                'candidate_name': 'Priya Sharma',
                'position_offered': 'Senior Software Engineer - EV Systems',
                'department_offer': 'Engineering - Electric Vehicle Division',
                'start_date': '2024-02-15',
                'salary_package': '₹18,00,000 per annum',
                'location_offer': 'Pune, Maharashtra',
                'reporting_to': 'Head of EV Software Development',
                'employment_terms': 'Full-time permanent position with 6 months probation period',
                'key_benefits': 'Health insurance for family, Employee vehicle scheme, Performance bonus, Professional development budget, Flexible working options'
            })
    
    with col_sample2:
        if st.button("📈 Sample 2: Manager Offer", type="secondary", key="offer2"):
            st.session_state.update({
                'candidate_name': 'Rajesh Kumar',
                'position_offered': 'Marketing Manager - Digital',
                'department_offer': 'Marketing & Sales',
                'start_date': '2024-03-01',
                'salary_package': '₹25,00,000 per annum',
                'location_offer': 'Mumbai, Maharashtra',
                'reporting_to': 'Head of Digital Marketing',
                'employment_terms': 'Full-time permanent position with 3 months probation period',
                'key_benefits': 'Comprehensive health coverage, Stock options, Variable pay up to 30%, Learning & development allowance, Car lease facility'
            })
    
    with col_sample3:
        if st.button("🏭 Sample 3: Production Role Offer", type="secondary", key="offer3"):
            st.session_state.update({
                'candidate_name': 'Amit Singh',
                'position_offered': 'Production Supervisor',
                'department_offer': 'Manufacturing Operations',
                'start_date': '2024-01-20',
                'salary_package': '₹8,50,000 per annum',
                'location_offer': 'Lucknow, Uttar Pradesh',
                'reporting_to': 'Production Manager',
                'employment_terms': 'Full-time permanent position with 6 months probation period',
                'key_benefits': 'Medical benefits, Transportation allowance, Shift allowances, Performance incentives, Training opportunities'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Candidate & Position Details")
        candidate_name = st.text_input("Candidate Name", value=st.session_state.get('candidate_name', ''), key="offer_candidate_name")
        position_offered = st.text_input("Position Offered", value=st.session_state.get('position_offered', ''), key="offer_position")
        department_offer = st.text_input("Department", value=st.session_state.get('department_offer', ''), key="offer_department")
        start_date = st.date_input("Start Date", value=datetime.strptime(st.session_state.get('start_date', '2024-02-01'), '%Y-%m-%d').date(), key="offer_start_date")
        salary_package = st.text_input("Salary Package", value=st.session_state.get('salary_package', ''), key="offer_salary")
        location_offer = st.text_input("Work Location", value=st.session_state.get('location_offer', ''), key="offer_location")
    
    with col2:
        st.subheader("Employment Terms & Benefits")
        reporting_to = st.text_input("Reporting To", value=st.session_state.get('reporting_to', ''), key="offer_reporting_to")
        employment_terms = st.text_area("Employment Terms", height=80, value=st.session_state.get('employment_terms', ''), key="offer_employment_terms")
        key_benefits = st.text_area("Key Benefits", height=100, value=st.session_state.get('key_benefits', ''), key="offer_key_benefits")
        
        document_type_options = ["Offer Letter", "Employment Contract", "Appointment Letter"]
        document_type = st.selectbox("Document Type", document_type_options, key="offer_document_type")
        
        if st.button("📄 Generate Offer Document", type="primary"):
            if candidate_name and position_offered:
                prompt = f"""
                Create a professional {document_type.lower()} for Tata Motors Limited.
                
                IMPORTANT: Write ONLY the document content. Do NOT include any explanatory text, introductions, or commentary.
                Start directly with the date and recipient information.
                
                Candidate Details:
                - Name: {candidate_name}
                - Position: {position_offered}
                - Department: {department_offer}
                - Start Date: {start_date}
                - Salary: {salary_package}
                - Location: {location_offer}
                - Reporting To: {reporting_to}
                - Employment Terms: {employment_terms}
                - Benefits: {key_benefits}
                
                Create a clean, business-ready {document_type.lower()} with:
                
                1. Date: {start_date.strftime("%B %d, %Y")}
                2. Professional salutation to {candidate_name.split()[0]}
                3. Opening congratulatory paragraph
                4. POSITION DETAILS section:
                   - Job title and department
                   - Reporting relationship
                   - Start date and location
                   
                5. COMPENSATION AND BENEFITS section:
                   - Annual salary clearly stated
                   - All benefits listed
                   
                6. EMPLOYMENT TERMS section:
                   - Employment type and probation period
                   - Notice period requirements
                   
                7. ACCEPTANCE section:
                   - Response deadline (7 days)
                   - Contact information for queries
                   
                8. Professional closing
                
                Write in clear, professional language suitable for Indian employment law.
                Use simple section headings in capital letters.
                Keep content concise but complete.
                """
                
                with st.spinner(f"Creating your {document_type.lower()}..."):
                    content = generate_content(prompt, document_type)
                    if content:
                        # Format with letterhead and company information
                        formatted_content = format_letter_with_letterhead(
                            content, document_type, candidate_name, position_offered, start_date.strftime("%B %d, %Y")
                        )
                        st.session_state.generated_content['offer_document'] = formatted_content
            else:
                st.error("Please fill in Candidate Name and Position Offered")
    
    # Display generated offer document
    if 'offer_document' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📋 Generated {document_type} with Tata Motors Letterhead")
        
        # Display the formatted letter in a clean text area
        st.text_area(
            "Letter Content (Clean Format)",
            value=st.session_state.generated_content['offer_document'],
            height=400,
            key="formatted_letter_display",
            help="This is the final formatted letter ready for download"
        )
        
        # Multiple download options
        st.subheader("📥 Download Options")
        filename_base = f"{document_type.replace(' ', '_')}_{candidate_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        
        create_download_options(
            st.session_state.generated_content['offer_document'],
            filename_base,
            candidate_name,
            document_type
        )
        
        # Preview and quality information
        st.markdown("---")
        st.subheader("ℹ️ Download Format Information")
        
        col_info1, col_info2, col_info3, col_info4 = st.columns(4)
        with col_info1:
            st.info("📄 **Text Format**\n- Clean, readable text\n- Easy to edit\n- Copy-paste ready")
        with col_info2:
            st.info("🌐 **HTML Format**\n- Professional layout\n- Print to PDF ready\n- Web viewable")
        with col_info3:
            st.info("📝 **Word Format**\n- Opens in MS Word\n- Full editing capability\n- Corporate standard")
        with col_info4:
            st.info("📝 **Markdown**\n- Clean documentation\n- Version control ready\n- Developer friendly")

# Tab 4: Pre-joining Checklists
with tab4:
    st.header("✅ Pre-joining Checklists")
    
    # Sample data
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("👨‍💻 Sample 1: Tech Professional", type="secondary", key="check1"):
            st.session_state.update({
                'new_hire_name': 'Ananya Patel',
                'position_checklist': 'Senior Software Engineer - EV Systems',
                'department_checklist': 'Engineering - Electric Vehicle Division',
                'start_date_checklist': '2024-02-15',
                'manager_checklist': 'Vikram Gupta',
                'location_checklist': 'Pune, Maharashtra',
                'special_requirements': 'Laptop setup with development tools, Access to EV simulation software, Security clearance for R&D facility',
                'documentation_needed': 'Educational certificates, Previous employment documents, PAN card, Aadhaar card, Passport, Bank account details, Medical fitness certificate'
            })
    
    with col_sample2:
        if st.button("📊 Sample 2: Sales Manager", type="secondary", key="check2"):
            st.session_state.update({
                'new_hire_name': 'Rohit Agarwal',
                'position_checklist': 'Regional Sales Manager',
                'department_checklist': 'Sales & Marketing',
                'start_date_checklist': '2024-03-01',
                'manager_checklist': 'Kavita Reddy',
                'location_checklist': 'Delhi NCR',
                'special_requirements': 'Company vehicle assignment, CRM system access, Sales territory mapping, Customer database access',
                'documentation_needed': 'Educational certificates, Experience certificates, Driving license, PAN card, Aadhaar card, Bank details, Address proof, Passport photos'
            })
    
    with col_sample3:
        if st.button("🏭 Sample 3: Manufacturing Role", type="secondary", key="check3"):
            st.session_state.update({
                'new_hire_name': 'Sunita Kumari',
                'position_checklist': 'Quality Inspector',
                'department_checklist': 'Quality Assurance',
                'start_date_checklist': '2024-01-25',
                'manager_checklist': 'Suresh Malik',
                'location_checklist': 'Jamshedpur, Jharkhand',
                'special_requirements': 'Safety training certification, Quality inspection tools access, PPE kit assignment, Shift schedule coordination',
                'documentation_needed': 'Educational certificates, Experience letters, Medical fitness certificate, PAN card, Aadhaar card, Bank details, Emergency contact information'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("New Hire Information")
        new_hire_name = st.text_input("New Hire Name", value=st.session_state.get('new_hire_name', ''), key="checklist_new_hire_name")
        position_checklist = st.text_input("Position", value=st.session_state.get('position_checklist', ''), key="checklist_position")
        department_checklist = st.text_input("Department", value=st.session_state.get('department_checklist', ''), key="checklist_department")
        start_date_checklist = st.date_input("Start Date", value=datetime.strptime(st.session_state.get('start_date_checklist', '2024-02-01'), '%Y-%m-%d').date(), key="checklist_start_date")
        manager_checklist = st.text_input("Reporting Manager", value=st.session_state.get('manager_checklist', ''), key="checklist_manager")
        location_checklist = st.text_input("Work Location", value=st.session_state.get('location_checklist', ''), key="checklist_location")
    
    with col2:
        st.subheader("Requirements & Documentation")
        special_requirements = st.text_area("Special Requirements/Access Needed", height=100, value=st.session_state.get('special_requirements', ''), key="checklist_special_requirements")
        documentation_needed = st.text_area("Documentation Required", height=100, value=st.session_state.get('documentation_needed', ''), key="checklist_documentation")
        
        checklist_type_options = ["Comprehensive Checklist", "HR Checklist", "IT Setup Checklist", "Manager's Checklist"]
        checklist_type = st.selectbox("Checklist Type", checklist_type_options, key="checklist_type")
        
        if st.button("✅ Generate Pre-joining Checklist", type="primary"):
            if new_hire_name and position_checklist:
                prompt = f"""
                Create a comprehensive pre-joining checklist for:
                
                New Hire: {new_hire_name}
                Position: {position_checklist}
                Department: {department_checklist}
                Start Date: {start_date_checklist}
                Manager: {manager_checklist}
                Location: {location_checklist}
                Special Requirements: {special_requirements}
                Documentation Needed: {documentation_needed}
                
                Create a detailed {checklist_type.lower()} that includes:
                1. Document collection and verification checklist
                2. IT setup and system access requirements
                3. Workspace preparation tasks
                4. Equipment and tool allocation
                5. Security and compliance requirements
                6. Manager preparation tasks
                7. HR administrative tasks
                8. Timeline with responsible parties
                9. Communication plan
                10. First day preparation checklist
                
                Organize by responsible party (HR, IT, Manager, Facilities) and include deadlines.
                Make it actionable with clear ownership and timelines.
                Use clean formatting without markdown symbols.
                """
                
                with st.spinner("Creating your pre-joining checklist..."):
                    content = generate_content(prompt, "Pre-joining Checklist")
                    if content:
                        st.session_state.generated_content['prejoining_checklist'] = content
            else:
                st.error("Please fill in New Hire Name and Position")
    
    # Display generated checklist
    if 'prejoining_checklist' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📋 Generated Pre-joining Checklist")
        cleaned_checklist = clean_markdown_text(st.session_state.generated_content['prejoining_checklist'])
        st.text_area(
            "Pre-joining Checklist",
            value=cleaned_checklist,
            height=400,
            help="Complete pre-joining checklist with responsibilities and timelines"
        )
        
        st.download_button(
            label="📥 Download Checklist",
            data=cleaned_checklist,
            file_name=f"Prejoining_Checklist_{new_hire_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 5: 30-60-90 Day Plans
with tab5:
    st.header("📅 30-60-90 Day Onboarding Plans")
    st.markdown("Create structured onboarding roadmaps for new hire success")
    
    # Sample data
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("🚗 Sample 1: Product Manager", type="secondary", key="plan1"):
            st.session_state.update({
                'employee_name_plan': 'Aarav Sharma',
                'role_plan': 'Product Manager - Electric Vehicles',
                'department_plan': 'Product Development',
                'manager_plan': 'Director of Product Strategy',
                'start_date_plan': '2024-02-01',
                'role_objectives': 'Lead product roadmap for new EV models, coordinate with engineering and design teams, conduct market research, manage product lifecycle',
                'key_stakeholders': 'Engineering teams, Design team, Marketing, Sales, Manufacturing, Supply chain, External partners',
                'learning_priorities': 'EV technology landscape, Tata Motors product portfolio, Market trends, Competitive analysis, Internal processes and systems',
                'success_metrics': 'Complete product training modules, Present market analysis to leadership, Build relationships with key stakeholders, Define product requirements for upcoming model'
            })
    
    with col_sample2:
        if st.button("💼 Sample 2: Finance Analyst", type="secondary", key="plan2"):
            st.session_state.update({
                'employee_name_plan': 'Neha Gupta',
                'role_plan': 'Senior Financial Analyst',
                'department_plan': 'Finance & Accounting',
                'manager_plan': 'Finance Manager',
                'start_date_plan': '2024-02-15',
                'role_objectives': 'Financial planning and analysis, Budget preparation, Variance analysis, Cost optimization, Financial reporting',
                'key_stakeholders': 'Finance team, Plant managers, Business unit heads, Auditors, Senior leadership',
                'learning_priorities': 'Tata Motors financial systems, ERP processes, Industry financial metrics, Compliance requirements, Cost accounting methods',
                'success_metrics': 'Complete ERP training, Contribute to monthly financial reporting, Assist in budget planning process, Present cost analysis to management'
            })
    
    with col_sample3:
        if st.button("⚙️ Sample 3: Manufacturing Engineer", type="secondary", key="plan3"):
            st.session_state.update({
                'employee_name_plan': 'Karthik Reddy',
                'role_plan': 'Manufacturing Engineer',
                'department_plan': 'Manufacturing Engineering',
                'manager_plan': 'Chief Manufacturing Engineer',
                'start_date_plan': '2024-01-20',
                'role_objectives': 'Process optimization, Equipment troubleshooting, Quality improvement, Safety compliance, Lean manufacturing implementation',
                'key_stakeholders': 'Production team, Quality team, Maintenance, Safety department, Suppliers, Plant management',
                'learning_priorities': 'Plant operations, Safety protocols, Manufacturing processes, Quality standards, Lean manufacturing principles',
                'success_metrics': 'Complete safety certification, Shadow senior engineers, Identify process improvement opportunity, Lead small improvement project'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Employee & Role Information")
        employee_name_plan = st.text_input("Employee Name", value=st.session_state.get('employee_name_plan', ''), key="plan_employee_name")
        role_plan = st.text_input("Role/Position", value=st.session_state.get('role_plan', ''), key="plan_role")
        department_plan = st.text_input("Department", value=st.session_state.get('department_plan', ''), key="plan_department")
        manager_plan = st.text_input("Reporting Manager", value=st.session_state.get('manager_plan', ''), key="plan_manager")
        start_date_plan = st.date_input("Start Date", value=datetime.strptime(st.session_state.get('start_date_plan', '2024-02-01'), '%Y-%m-%d').date(), key="plan_start_date")
        role_objectives = st.text_area("Key Role Objectives", height=80, value=st.session_state.get('role_objectives', ''), key="plan_role_objectives")
    
    with col2:
        st.subheader("Onboarding Focus Areas")
        key_stakeholders = st.text_area("Key Stakeholders to Meet", height=80, value=st.session_state.get('key_stakeholders', ''), key="plan_key_stakeholders")
        learning_priorities = st.text_area("Learning Priorities", height=80, value=st.session_state.get('learning_priorities', ''), key="plan_learning_priorities")
        success_metrics = st.text_area("Success Metrics/Goals", height=80, value=st.session_state.get('success_metrics', ''), key="plan_success_metrics")
        
        plan_focus_options = ["Comprehensive Plan", "Technical Focus", "Leadership Focus", "Sales Focus", "Operations Focus"]
        plan_focus = st.selectbox("Plan Focus", plan_focus_options, key="plan_focus")
        
        if st.button("📅 Generate 30-60-90 Day Plan", type="primary"):
            if employee_name_plan and role_plan:
                prompt = f"""
                Create a comprehensive 30-60-90 day onboarding plan for:
                
                Employee: {employee_name_plan}
                Role: {role_plan}
                Department: {department_plan}
                Manager: {manager_plan}
                Start Date: {start_date_plan}
                Role Objectives: {role_objectives}
                Key Stakeholders: {key_stakeholders}
                Learning Priorities: {learning_priorities}
                Success Metrics: {success_metrics}
                Focus Area: {plan_focus}
                
                Create a detailed onboarding plan with:
                
                FIRST 30 DAYS (Foundation & Orientation):
                - Week 1: Initial setup and basic orientation
                - Week 2: Department introduction and role understanding
                - Week 3: Process learning and initial assignments
                - Week 4: First month review and feedback
                
                NEXT 30 DAYS (Integration & Learning):
                - Week 5-6: Deeper role engagement and skill building
                - Week 7-8: Stakeholder meetings and project involvement
                
                FINAL 30 DAYS (Contribution & Growth):
                - Week 9-10: Independent project ownership
                - Week 11-12: Performance evaluation and future planning
                
                For each phase, include:
                1. Specific learning objectives
                2. Key activities and milestones
                3. Stakeholder meetings scheduled
                4. Training and development activities
                5. Success metrics and evaluation criteria
                6. Manager check-in points
                7. Resources and support needed
                
                Make it actionable with clear timelines and measurable outcomes.
                Use clean formatting without markdown symbols.
                """
                
                with st.spinner("Creating your 30-60-90 day plan..."):
                    content = generate_content(prompt, "30-60-90 Day Plan")
                    if content:
                        st.session_state.generated_content['onboarding_plan'] = content
            else:
                st.error("Please fill in Employee Name and Role")
    
    # Display generated plan
    if 'onboarding_plan' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📈 Generated 30-60-90 Day Onboarding Plan")
        cleaned_plan = clean_markdown_text(st.session_state.generated_content['onboarding_plan'])
        st.text_area(
            "30-60-90 Day Onboarding Plan",
            value=cleaned_plan,
            height=400,
            help="Comprehensive onboarding plan with clear milestones and objectives"
        )
        
        st.download_button(
            label="📥 Download Onboarding Plan",
            data=cleaned_plan,
            file_name=f"Onboarding_Plan_{employee_name_plan.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 6: Welcome Communications
with tab6:
    st.header("📧 Welcome Communications")
    st.markdown("Create warm, engaging welcome messages for new hires")
    
    # Sample data
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("📧 Sample 1: Welcome Email", type="secondary", key="welcome1"):
            st.session_state.update({
                'new_hire_welcome': 'Priya Menon',
                'position_welcome': 'UX Designer',
                'department_welcome': 'Digital Innovation',
                'start_date_welcome': '2024-02-12',
                'manager_welcome': 'Arjun Das',
                'team_welcome': 'Digital Innovation Team',
                'communication_type': 'Welcome Email',
                'tone_welcome': 'Warm and Professional',
                'key_info': 'First day reporting time: 9:00 AM, Location: Tech Center Pune, Parking: Level 2, Contact person: HR representative will meet at reception'
            })
    
    with col_sample2:
        if st.button("📱 Sample 2: WhatsApp/SMS", type="secondary", key="welcome2"):
            st.session_state.update({
                'new_hire_welcome': 'Rahul Singh',
                'position_welcome': 'Sales Executive',
                'department_welcome': 'Commercial Vehicle Sales',
                'start_date_welcome': '2024-02-08',
                'manager_welcome': 'Sanjay Kumar',
                'team_welcome': 'North Region Sales Team',
                'communication_type': 'WhatsApp/SMS',
                'tone_welcome': 'Friendly and Informative',
                'key_info': 'Reporting time: 9:30 AM, Office: Gurgaon Sales Office, Documents: Bring original certificates, Lunch: Team welcome lunch arranged'
            })
    
    with col_sample3:
        if st.button("📋 Sample 3: Welcome Package", type="secondary", key="welcome3"):
            st.session_state.update({
                'new_hire_welcome': 'Anjali Patel',
                'position_welcome': 'HR Business Partner',
                'department_welcome': 'Human Resources',
                'start_date_welcome': '2024-02-05',
                'manager_welcome': 'Deepak Sharma',
                'team_welcome': 'HR Excellence Team',
                'communication_type': 'Welcome Package Content',
                'tone_welcome': 'Professional and Inclusive',
                'key_info': 'Buddy assigned: Meera Joshi, Training schedule: Week 1-2, Office tour: 10:00 AM first day, IT setup: Pre-configured'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("New Hire Details")
        new_hire_welcome = st.text_input("New Hire Name", value=st.session_state.get('new_hire_welcome', ''), key="welcome_new_hire_name")
        position_welcome = st.text_input("Position", value=st.session_state.get('position_welcome', ''), key="welcome_position")
        department_welcome = st.text_input("Department", value=st.session_state.get('department_welcome', ''), key="welcome_department")
        start_date_welcome = st.date_input("Start Date", value=datetime.strptime(st.session_state.get('start_date_welcome', '2024-02-01'), '%Y-%m-%d').date(), key="welcome_start_date")
        manager_welcome = st.text_input("Manager Name", value=st.session_state.get('manager_welcome', ''), key="welcome_manager")
        team_welcome = st.text_input("Team Name", value=st.session_state.get('team_welcome', ''), key="welcome_team")
    
    with col2:
        st.subheader("Communication Style & Content")
        communication_type_options = ["Welcome Email", "WhatsApp/SMS", "Welcome Package Content", "Welcome Letter", "Video Script"]
        current_comm_type = st.session_state.get('communication_type', 'Welcome Email')
        try:
            comm_type_index = communication_type_options.index(current_comm_type)
        except ValueError:
            comm_type_index = 0
        communication_type = st.selectbox("Communication Type", communication_type_options, index=comm_type_index)
        
        tone_options = ["Warm and Professional", "Friendly and Informative", "Professional and Inclusive", "Casual and Welcoming"]
        current_tone = st.session_state.get('tone_welcome', 'Warm and Professional')
        try:
            tone_index = tone_options.index(current_tone)
        except ValueError:
            tone_index = 0
        tone_welcome = st.selectbox("Tone/Style", tone_options, index=tone_index)
        
        key_info = st.text_area("Key Information to Include", height=100, value=st.session_state.get('key_info', ''), key="welcome_key_info")
        
        if st.button("📧 Generate Welcome Communication", type="primary"):
            if new_hire_welcome and position_welcome:
                prompt = f"""
                Create a {communication_type.lower()} for:
                
                New Hire: {new_hire_welcome}
                Position: {position_welcome}
                Department: {department_welcome}
                Start Date: {start_date_welcome}
                Manager: {manager_welcome}
                Team: {team_welcome}
                Tone: {tone_welcome}
                Key Information: {key_info}
                
                Create an engaging {communication_type.lower()} that includes:
                1. Warm welcome message
                2. Excitement about their joining
                3. Key first day information
                4. Team introduction
                5. What to expect in first week
                6. Contact information for queries
                7. Company culture highlights
                8. Next steps and timeline
                
                Make it {tone_welcome.lower()}, engaging, and informative while reflecting Tata Motors' values and culture.
                Ensure the new hire feels valued, informed, and excited about their journey.
                Use clean formatting without markdown symbols.
                """
                
                with st.spinner(f"Creating your {communication_type.lower()}..."):
                    content = generate_content(prompt, communication_type)
                    if content:
                        st.session_state.generated_content['welcome_communication'] = content
            else:
                st.error("Please fill in New Hire Name and Position")
    
    # Display generated communication
    if 'welcome_communication' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"💌 Generated {communication_type}")
        cleaned_welcome = clean_markdown_text(st.session_state.generated_content['welcome_communication'])
        st.text_area(
            f"{communication_type} Content",
            value=cleaned_welcome,
            height=300,
            help=f"Professional {communication_type.lower()} ready for use"
        )
        
        st.download_button(
            label=f"📥 Download {communication_type}",
            data=cleaned_welcome,
            file_name=f"Welcome_{communication_type.replace(' ', '_')}_{new_hire_welcome.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 7: Custom Acquisition Assistant
with tab7:
    st.header("🎨 Custom Talent Acquisition Assistant")
    st.markdown("Create any recruitment or onboarding document with custom prompts")
    
    # Sample prompts
    st.subheader("🎯 Best Practice Prompts for Talent Acquisition")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("📊 Sample: Recruitment Strategy", type="secondary", key="custom_ta1"):
            st.session_state['custom_prompt_ta'] = """Develop a comprehensive talent acquisition strategy for Tata Motors to attract top talent in the electric vehicle space.

Current Context:
- Rapid expansion in EV segment
- Competition for skilled EV engineers and software developers
- Need for diverse and inclusive hiring practices
- Focus on innovation and sustainability
- Global talent requirements

Create a strategy covering:
- Target talent profiles and skills
- Sourcing channels and methods
- Employer branding initiatives
- Interview and assessment processes
- Diversity and inclusion measures
- Timeline and success metrics"""
    
    with col_sample2:
        if st.button("📝 Sample: Interview Guide", type="secondary", key="custom_ta2"):
            st.session_state['custom_prompt_ta'] = """Create a comprehensive interview guide for hiring Software Engineers specializing in Electric Vehicle systems at Tata Motors.

Interview Requirements:
- Technical assessment for EV software development
- Behavioral competency evaluation
- Cultural fit assessment
- Problem-solving and innovation mindset
- Collaboration and teamwork skills

Include:
- Pre-interview preparation checklist
- Technical questions and scenarios
- Behavioral interview questions
- Assessment criteria and scoring rubric
- Follow-up questions for different experience levels
- Decision-making framework"""
    
    with col_sample3:
        if st.button("🎓 Sample: Graduate Program", type="secondary", key="custom_ta3"):
            st.session_state['custom_prompt_ta'] = """Design a comprehensive graduate trainee program for Tata Motors focused on developing future leaders in automotive innovation.

Program Focus:
- Electric vehicle technology
- Sustainable mobility solutions
- Digital transformation in automotive
- Leadership development
- Innovation and entrepreneurship

Create:
- Program structure and curriculum
- Rotation plans across departments
- Learning objectives and outcomes
- Mentorship framework
- Assessment and evaluation methods
- Career progression pathways
- Success metrics and KPIs"""
    
    st.markdown("---")
    
    # More sample prompts
    col_sample4, col_sample5 = st.columns(2)
    
    with col_sample4:
        if st.button("📋 Sample: Assessment Center", type="secondary", key="custom_ta4"):
            st.session_state['custom_prompt_ta'] = """Design an assessment center for leadership roles at Tata Motors focusing on future automotive industry challenges.

Assessment Focus:
- Strategic thinking and decision making
- Innovation and digital mindset
- Sustainability leadership
- Change management capabilities
- Cross-cultural collaboration
- Customer-centricity

Include:
- Assessment center agenda and timeline
- Individual and group exercises
- Case study scenarios
- Role-play situations
- Assessment criteria and tools
- Observer training guidelines
- Scoring and feedback mechanisms"""
        
    with col_sample5:
        if st.button("🌍 Sample: Campus Hiring", type="secondary", key="custom_ta5"):
            st.session_state['custom_prompt_ta'] = """Create a campus hiring strategy for Tata Motors to attract top engineering talent from premier institutes for electric vehicle and autonomous driving roles.

Target Institutes:
- IITs, NITs, and premier engineering colleges
- Focus on Computer Science, Electronics, Mechanical streams
- Emphasis on innovation and research orientation

Develop:
- Campus engagement calendar
- Pre-placement talk content and strategy
- Selection process and timeline
- Internship to full-time conversion program
- Employer branding initiatives
- Student engagement activities
- Offer competitiveness strategy"""
    
    st.markdown("---")
    
    # Custom prompt input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💭 Your Custom Talent Acquisition Request")
        custom_prompt = st.text_area(
            "Enter your recruitment or onboarding question/request:",
            height=250,
            value=st.session_state.get('custom_prompt_ta', ''),
            placeholder="""Examples:
• Create interview questions for Data Scientist role
• Design diversity hiring initiative for technical roles
• Draft recruitment policy for remote positions
• Create onboarding checklist for international hires
• Design talent pipeline strategy for critical skills
• Create employee referral program guidelines
• Draft exit interview questionnaire template
• Design skills assessment for digital marketing roles"""
        )
        
        # Context options
        st.subheader("🎯 Context & Customization")
        col_context1, col_context2 = st.columns(2)
        
        with col_context1:
            company_context_ta = st.selectbox(
                "Company Context",
                ["Tata Motors", "Automotive Industry", "Manufacturing Company", "Technology Company", "Large Corporation", "Custom"],
                index=0
            )
            
            if company_context_ta == "Custom":
                custom_company_ta = st.text_input("Enter your company/industry context:")
                company_context_ta = custom_company_ta
            
            document_type_ta = st.selectbox(
                "Document Type",
                ["Strategy Document", "Process/Procedure", "Template/Form", "Assessment Tool", "Communication", "Policy Document", "Training Material", "Other"]
            )
        
        with col_context2:
            detail_level_ta = st.selectbox(
                "Detail Level",
                ["High Detail (Comprehensive)", "Medium Detail (Standard)", "Low Detail (Brief Overview)"]
            )
            
            target_audience_ta = st.multiselect(
                "Target Audience",
                ["HR Team", "Hiring Managers", "Interviewers", "Candidates", "Senior Leadership", "All Employees", "External Partners"],
                default=["HR Team"]
            )
    
    with col2:
        st.subheader("🚀 Generate Content")
        
        if st.button("🎨 Generate Custom TA Content", type="primary", key="generate_custom_ta"):
            if custom_prompt.strip():
                # Build enhanced prompt with context
                enhanced_prompt = f"""
                Company Context: {company_context_ta}
                Document Type: {document_type_ta}
                Target Audience: {', '.join(target_audience_ta)}
                Detail Level: {detail_level_ta}
                
                Talent Acquisition Request: {custom_prompt}
                
                Please create professional talent acquisition content that:
                1. Is specific to the company context provided
                2. Follows recruitment best practices and compliance requirements
                3. Promotes diversity, equity, and inclusion
                4. Is appropriate for the target audience
                5. Matches the requested detail level
                6. Is immediately usable and actionable
                7. Includes relevant frameworks, templates, or tools as needed
                8. Considers legal compliance and bias-free practices
                
                If this is a strategy document, include implementation guidelines and success metrics.
                If this is an assessment tool, make it practical and measurable.
                If this is a process, ensure clear steps and accountability.
                If this is communication, make it engaging and informative.
                
                Use clean formatting without markdown symbols.
                """
                
                with st.spinner("Creating your custom talent acquisition content..."):
                    content = generate_content(enhanced_prompt, "Custom TA Content")
                    if content:
                        st.session_state.generated_content['custom_ta'] = content
            else:
                st.error("Please enter your talent acquisition request in the text area")
        
        # Additional options
        st.markdown("---")
        st.subheader("📋 Quick Actions")
        
        if st.button("🔄 Clear Form", key="clear_custom_ta"):
            st.session_state['custom_prompt_ta'] = ''
            if 'custom_ta' in st.session_state.generated_content:
                del st.session_state.generated_content['custom_ta']
            st.rerun()
        
        if st.button("💡 Get Ideas", key="ideas_custom_ta"):
            st.session_state['custom_prompt_ta'] = """Suggest 10 innovative talent acquisition initiatives that Tata Motors could implement to:
- Attract top talent in electric vehicle and autonomous driving
- Build a diverse and inclusive workforce
- Enhance employer branding in the automotive industry
- Streamline recruitment processes with technology
- Improve candidate experience throughout the hiring journey
- Develop talent pipelines for future skill requirements
- Create competitive advantages in talent acquisition

For each initiative, provide a brief description, implementation approach, and expected benefits."""
    
    # Display generated content
    if 'custom_ta' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Talent Acquisition Content")
        
        # Content display with formatting
        cleaned_custom = clean_markdown_text(st.session_state.generated_content['custom_ta'])
        st.text_area(
            "Custom Talent Acquisition Content",
            value=cleaned_custom,
            height=400,
            help="Professional talent acquisition content ready for use"
        )
        
        # Download and action buttons
        col_download1, col_download2, col_download3 = st.columns(3)
        
        with col_download1:
            st.download_button(
                label="📥 Download as Text",
                data=cleaned_custom,
                file_name=f"Custom_TA_Content_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
        
        with col_download2:
            if st.button("📋 Copy to Clipboard", key="copy_custom_ta"):
                st.info("Content ready for copy! Select the text above and use Ctrl+C")
        
        with col_download3:
            if st.button("✏️ Refine Content", key="refine_custom_ta"):
                st.session_state['custom_prompt_ta'] = f"Please refine and improve the following talent acquisition content:\n\n{cleaned_custom}\n\nMake it more detailed, professional, and actionable with specific implementation steps."

# Footer
st.markdown("---")
st.markdown("### 🚀 Ready for the next module?")
st.info("This is Module 3 of 9. Continue building your comprehensive HR toolkit with additional specialized modules.")

# Instructions
with st.expander("📖 How to Use This Talent Acquisition & Onboarding Module"):
    st.markdown("""
    ## 🎯 **Standard Features (Tabs 1-6):**
    1. **📝 Job Description Generator** - Create inclusive, bias-free job descriptions
    2. **🔍 CV vs JD Comparison** - AI-powered candidate ranking and assessment
    3. **📄 Offer Letters & Contracts** - Professional employment documents with multiple download formats
    4. **✅ Pre-joining Checklists** - Comprehensive preparation workflows
    5. **📅 30-60-90 Day Plans** - Structured onboarding roadmaps
    6. **📧 Welcome Communications** - Engaging welcome messages and materials
    
    ## 🎨 **Custom Acquisition Assistant (Tab 7):**
    - **Best Practice Prompts** - Use proven talent acquisition templates
    - **Custom Requests** - Handle any recruitment or onboarding need
    - **Context-Aware** - Tailored to your industry and organization
    - **Professional Output** - Ready-to-use documents and strategies
    
    ## 📥 **Download Options:**
    - **📄 Text Format** - Clean, editable plain text
    - **🌐 HTML Format** - Professional layout for web viewing and PDF conversion
    - **📝 Word Format (RTF)** - Opens directly in Microsoft Word
    - **📄 PDF Ready** - Optimized HTML for easy PDF conversion via browser print
    
    **Tips:**
    - Use sample data buttons for quick testing and learning
    - All content is formatted without markdown symbols for clean downloads
    - HTML format works best for PDF conversion via browser print
    - RTF format provides full Word compatibility
    - Focus on inclusive language and bias-free practices
    - Consider diversity and inclusion in all processes
    - Ensure legal compliance in all documents
    """)

# Navigation
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("← Module 2: Succession Planning", key="nav_prev_ta"):
        st.switch_page("pages/02_succession_planning.py")

with col_nav2:
    if st.button("🏠 Main Menu", key="nav_home_ta"):
        st.switch_page("pages/00_home.py")

with col_nav3:
    if st.button("Module 4: Culture →", key="nav_next_ta", disabled=True):
        st.info("Coming Soon!")