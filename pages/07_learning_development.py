import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="HR Copilot - L&D & Capability Development",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {}

# Get API key from environment
api_key = os.getenv('GEMINI_API_KEY')

# Configure Gemini if API key is available
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ GEMINI_API_KEY not found in .env file. Please add your API key to the .env file.")

# Sidebar information
with st.sidebar:
    st.title("🔧 Configuration")
    if st.session_state.get('model_choice', None) == "Gemini (Google)":
        if api_key:
            st.success("✅ Gemini API Key loaded")
        else:
            st.error("❌ GEMINI_API_KEY not found")
    else:
        if os.getenv('OPENAI_API_KEY'):
            st.success("✅ OpenAI API Key loaded")
        else:
            st.error("❌ OPENAI_API_KEY not found")
    st.markdown("---")
    st.markdown("### 🎓 Module 7: L&D & Capability Development")
    st.markdown("Design training and capability programs for employee growth")

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
        if not api_key:
            st.error("Please add your Gemini API key to the .env file")
            return None
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            system_prompt = """You are a senior HR Learning & Development specialist with 15+ years of experience in designing training programs, creating assessment tools, building learning pathways, and developing capability frameworks.

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

Focus on practical, engaging, and measurable solutions that drive employee skill development and organizational capability."""
            
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
st.title("🎓 HR Copilot - L&D & Capability Development")
st.markdown("Design impactful training programs, assessments, and learning pathways for employee growth.")

# Tab layout
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📚 Training Design Wizard",
    "❓ Assessment Question Bank", 
    "📝 Feedback Forms",
    "🛤️ Learning Pathway Builder",
    "📧 Course Communication Templates",
    "🎨 Custom L&D Tools"
])

# Tab 1: Training Design Wizard
with tab1:
    st.header("📚 Training Design Wizard")
    st.markdown("Design comprehensive training outlines and workshop agendas.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Designs")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Leadership Development Workshop", type="secondary", key="sample_training_leadership"):
            st.session_state.update({
                'training_topic': 'Effective Leadership for Mid-Managers',
                'training_audience': 'Mid-Level Managers',
                'training_duration': '2 days (16 hours)',
                'training_objectives': 'Enhance communication, delegation, and conflict resolution skills; Foster strategic thinking.',
                'training_modules': 'Module 1: Foundations of Leadership; Module 2: Communication & Influence; Module 3: Team Building & Motivation; Module 4: Conflict Resolution & Coaching; Module 5: Strategic Planning & Execution.',
                'training_delivery': 'Blended (in-person workshops, online pre-work, post-workshop coaching)',
                'training_assessment': 'Pre/post assessment, peer feedback, manager observation'
            })
    
    with col_sample2:
        if st.button("New Software Onboarding Training", type="secondary", key="sample_training_software"):
            st.session_state.update({
                'training_topic': 'Introduction to CRM Software (Sales Team)',
                'training_audience': 'New Sales Representatives',
                'training_duration': '1 day (8 hours)',
                'training_objectives': 'Familiarize with CRM interface, enable lead management, opportunity tracking, and reporting.',
                'training_modules': 'Module 1: CRM Navigation; Module 2: Lead & Account Management; Module 3: Opportunity Pipeline; Module 4: Reporting & Dashboards; Module 5: Best Practices & Q&A.',
                'training_delivery': 'Virtual instructor-led training with hands-on exercises',
                'training_assessment': 'Practical exercises, short quiz'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Training Program Details")
        training_topic = st.text_input("Training Topic/Title", value=st.session_state.get('training_topic', ''), placeholder="e.g., Project Management Basics, Diversity & Inclusion", key="training_topic_input")
        training_audience = st.text_input("Target Audience", value=st.session_state.get('training_audience', ''), placeholder="e.g., All Employees, New Managers, IT Staff", key="training_audience_input")
        training_duration = st.text_input("Estimated Duration", value=st.session_state.get('training_duration', ''), placeholder="e.g., 4 hours, 3 days, 1 week", key="training_duration_input")
        
    with col2:
        st.subheader("Design Elements")
        training_objectives = st.text_area("Learning Objectives (SMART)", height=100, value=st.session_state.get('training_objectives', ''), placeholder="e.g., By end of training, participants will be able to...", key="training_objectives_input")
        training_modules = st.text_area("Key Modules/Sections", height=100, value=st.session_state.get('training_modules', ''), placeholder="e.g., Module 1: Intro; Module 2: Core Concepts; Module 3: Application", key="training_modules_input")
        training_delivery = st.text_input("Delivery Method", value=st.session_state.get('training_delivery', ''), placeholder="e.g., In-person, Virtual, Blended, E-learning", key="training_delivery_input")
        training_assessment = st.text_input("Assessment/Evaluation Methods", value=st.session_state.get('training_assessment', ''), placeholder="e.g., Quiz, Role-play, Project, Feedback survey", key="training_assessment_input")
        
        if st.button("📚 Generate Training Design", type="primary", key="generate_training_design"):
            if training_topic and training_objectives:
                prompt = f"""Create a detailed training design document for a program titled '{training_topic}'.

Target Audience: {training_audience}
Estimated Duration: {training_duration}
Learning Objectives: {training_objectives}
Key Modules/Sections: {training_modules}
Delivery Method: {training_delivery}
Assessment/Evaluation Methods: {training_assessment}

The training design should include:
- PROGRAM OVERVIEW (Title, Purpose, Target Audience, Duration)
- LEARNING OBJECTIVES (Specific, Measurable, Achievable, Relevant, Time-bound)
- MODULE BREAKDOWN (For each module: Topic, Duration, Key Content Areas, Activities, Materials)
- DELIVERY STRATEGY (Methodology, Facilitator Notes, Participant Engagement)
- ASSESSMENT AND EVALUATION PLAN (Methods, Criteria, Follow-up)
- RESOURCES AND MATERIALS (List of handouts, tools, technology)
- PRE-REQUISITES (if any)
- POST-TRAINING SUPPORT (e.g., coaching, follow-up sessions)

Ensure the design is practical, engaging, and aligned with adult learning principles."""

                with st.spinner(f"Generating training design for {training_topic}..."):
                    content = generate_content(prompt, "Training Design")
                    if content:
                        st.session_state.generated_content['training_design'] = content
            else:
                st.error("Please fill in Training Topic and Learning Objectives.")
    
    # Display generated content
    if 'training_design' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated Training Design for {training_topic}")
        cleaned_content = clean_text(st.session_state.generated_content['training_design'])
        st.text_area("Training Design Content", value=cleaned_content, height=400, key="training_design_output")
        create_download_button(cleaned_content, f"Training_Design_{training_topic.replace(' ', '_')}", "📥 Download Training Design")

# Tab 2: Assessment Question Bank
with tab2:
    st.header("❓ Assessment Question Bank")
    st.markdown("Create quizzes and assessment questions for various learning topics.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Questions")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Project Management Quiz", type="secondary", key="sample_assessment_pm"):
            st.session_state.update({
                'assessment_topic': 'Project Management Fundamentals',
                'assessment_type': 'Multiple Choice, True/False, Short Answer',
                'assessment_difficulty': 'Intermediate',
                'num_questions': 10,
                'learning_objectives_assessment': 'Understand project lifecycle, risk management, stakeholder communication.',
                'additional_context_assessment': 'Focus on Agile methodologies.'
            })
    
    with col_sample2:
        if st.button("Cybersecurity Awareness Quiz", type="secondary", key="sample_assessment_cyber"):
            st.session_state.update({
                'assessment_topic': 'Cybersecurity Awareness for Employees',
                'assessment_type': 'Multiple Choice, Scenario-based',
                'assessment_difficulty': 'Beginner',
                'num_questions': 8,
                'learning_objectives_assessment': 'Identify phishing attempts, understand password hygiene, recognize data privacy best practices.',
                'additional_context_assessment': 'Include common threats like ransomware and social engineering.'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Assessment Details")
        assessment_topic = st.text_input("Assessment Topic", value=st.session_state.get('assessment_topic', ''), placeholder="e.g., Sales Techniques, HR Policies", key="assessment_topic_input")
        assessment_type = st.text_input("Question Types", value=st.session_state.get('assessment_type', ''), placeholder="e.g., Multiple Choice, True/False, Short Answer, Scenario-based", key="assessment_type_input")
        
    with col2:
        st.subheader("Customization")
        assessment_difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"], index=0, key="assessment_difficulty_select")
        num_questions = st.number_input("Number of Questions", min_value=5, max_value=30, value=st.session_state.get('num_questions', 10), key="num_questions_input")
        learning_objectives_assessment = st.text_area("Related Learning Objectives", height=70, value=st.session_state.get('learning_objectives_assessment', ''), placeholder="e.g., What should the learner know after this assessment?", key="learning_objectives_assessment_input")
        additional_context_assessment = st.text_area("Additional Context/Specifics", height=70, value=st.session_state.get('additional_context_assessment', ''), placeholder="e.g., Specific industry terms, company-specific scenarios.", key="additional_context_assessment_input")
        
        if st.button("❓ Generate Assessment Questions", type="primary", key="generate_assessment_questions"):
            if assessment_topic and learning_objectives_assessment:
                prompt = f"""Generate {num_questions} assessment questions on the topic of '{assessment_topic}'.

Question Types: {assessment_type}
Difficulty Level: {assessment_difficulty}
Related Learning Objectives: {learning_objectives_assessment}
Additional Context: {additional_context_assessment if additional_context_assessment else 'None'}

For each question:
- State the question clearly.
- If multiple choice, provide 4 options (one correct, three plausible distractors). Mark the correct answer.
- If True/False, provide the statement and indicate True/False.
- If Short Answer, specify expected key points.
- If Scenario-based, describe a scenario and ask a relevant question.

Ensure questions are relevant to the learning objectives and appropriate for the difficulty level."""

                with st.spinner(f"Generating {num_questions} assessment questions on {assessment_topic}..."):
                    content = generate_content(prompt, "Assessment Questions")
                    if content:
                        st.session_state.generated_content['assessment_questions'] = content
            else:
                st.error("Please fill in Assessment Topic and Related Learning Objectives.")
    
    # Display generated content
    if 'assessment_questions' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated Assessment Questions for {assessment_topic}")
        cleaned_content = clean_text(st.session_state.generated_content['assessment_questions'])
        st.text_area("Assessment Questions Content", value=cleaned_content, height=400, key="assessment_questions_output")
        create_download_button(cleaned_content, f"Assessment_Questions_{assessment_topic.replace(' ', '_')}", "📥 Download Assessment Questions")

# Tab 3: Feedback Forms
with tab3:
    st.header("📝 Training Feedback Forms")
    st.markdown("Draft feedback forms to evaluate training effectiveness and gather participant insights.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Forms")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Post-Training Feedback Form", type="secondary", key="sample_feedback_post"):
            st.session_state.update({
                'feedback_form_purpose': 'Evaluate effectiveness of a recent training program.',
                'feedback_target_audience': 'Training Participants',
                'feedback_topic': 'Customer Service Excellence Training',
                'feedback_sections': 'Overall Satisfaction, Trainer Effectiveness, Content Relevance, Learning Environment, Future Needs.',
                'feedback_rating_scale': '1-5 (1=Poor, 5=Excellent)',
                'feedback_open_ended': 'What did you like most? What could be improved? Any other comments?'
            })
    
    with col_sample2:
        if st.button("Trainer Evaluation Form", type="secondary", key="sample_feedback_trainer"):
            st.session_state.update({
                'feedback_form_purpose': 'Assess trainer performance.',
                'feedback_target_audience': 'Training Participants',
                'feedback_topic': 'Trainer Evaluation for "Effective Communication"',
                'feedback_sections': 'Knowledge, Presentation Skills, Engagement, Responsiveness, Overall Effectiveness.',
                'feedback_rating_scale': '1-5 (1=Strongly Disagree, 5=Strongly Agree)',
                'feedback_open_ended': 'Specific examples of effective teaching? Suggestions for improvement?'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Form Details")
        feedback_form_purpose = st.text_input("Purpose of the Feedback Form", value=st.session_state.get('feedback_form_purpose', ''), placeholder="e.g., Evaluate training, Assess trainer, Gather topic ideas", key="feedback_form_purpose_input")
        feedback_target_audience = st.text_input("Target Audience", value=st.session_state.get('feedback_target_audience', ''), placeholder="e.g., Training Participants, Managers, L&D Team", key="feedback_target_audience_input")
        feedback_topic = st.text_input("Specific Training/Topic", value=st.session_state.get('feedback_topic', ''), placeholder="e.g., Leadership Workshop, New Employee Orientation", key="feedback_topic_input")
        
    with col2:
        st.subheader("Content & Structure")
        feedback_sections = st.text_area("Key Sections/Questions to Include", height=100, value=st.session_state.get('feedback_sections', ''), placeholder="e.g., Content, Delivery, Relevance, Logistics", key="feedback_sections_input")
        feedback_rating_scale = st.text_input("Rating Scale (if applicable)", value=st.session_state.get('feedback_rating_scale', ''), placeholder="e.g., 1-5, Strongly Agree/Disagree", key="feedback_rating_scale_input")
        feedback_open_ended = st.text_area("Open-ended Questions", height=70, value=st.session_state.get('feedback_open_ended', ''), placeholder="e.g., What did you like most? What could be improved?", key="feedback_open_ended_input")
        
        if st.button("📝 Generate Feedback Form", type="primary", key="generate_feedback_form"):
            if feedback_form_purpose and feedback_topic:
                prompt = f"""Create a detailed feedback form for '{feedback_form_purpose}'.

Target Audience: {feedback_target_audience}
Specific Training/Topic: {feedback_topic}
Key Sections/Questions to Include: {feedback_sections}
Rating Scale: {feedback_rating_scale if feedback_rating_scale else 'N/A'}
Open-ended Questions: {feedback_open_ended if feedback_open_ended else 'None'}

The feedback form should include:
- Form Title and Purpose
- Instructions for Completion
- Participant Demographics (optional: Department, Role)
- Rating-based questions for each key section.
- Open-ended questions for qualitative feedback.
- Space for additional comments.
- Thank you message.

Ensure the form is clear, easy to complete, and designed to gather actionable insights."""

                with st.spinner(f"Generating feedback form for {feedback_topic}..."):
                    content = generate_content(prompt, "Feedback Form")
                    if content:
                        st.session_state.generated_content['feedback_form'] = content
            else:
                st.error("Please fill in Purpose of the Feedback Form and Specific Training/Topic.")
    
    # Display generated content
    if 'feedback_form' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated Feedback Form for {feedback_topic}")
        cleaned_content = clean_text(st.session_state.generated_content['feedback_form'])
        st.text_area("Feedback Form Content", value=cleaned_content, height=400, key="feedback_form_output")
        create_download_button(cleaned_content, f"Feedback_Form_{feedback_topic.replace(' ', '_')}", "📥 Download Feedback Form")

# Tab 4: Learning Pathway Builder
with tab4:
    st.header("🛤️ Learning Pathway Builder")
    st.markdown("Build personalized learning pathways for specific roles or career goals.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Pathways")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Data Analyst Career Path", type="secondary", key="sample_path_data_analyst"):
            st.session_state.update({
                'path_role': 'Data Analyst',
                'path_target_level': 'Senior Data Analyst',
                'path_current_skills': 'SQL, Excel, Basic Python',
                'path_skills_to_develop': 'Advanced Python (Pandas, NumPy), R, Data Visualization (Tableau/Power BI), Statistical Modeling, Machine Learning Basics.',
                'path_learning_resources': 'Online courses (Coursera, Udemy), Internal workshops, Mentorship, Hands-on projects.',
                'path_timeline': '12-18 months'
            })
    
    with col_sample2:
        if st.button("Marketing Manager Pathway", type="secondary", key="sample_path_marketing_manager"):
            st.session_state.update({
                'path_role': 'Marketing Specialist',
                'path_target_level': 'Marketing Manager',
                'path_current_skills': 'Digital Marketing, Content Creation, Social Media Management',
                'path_skills_to_develop': 'Team Leadership, Budget Management, Strategic Planning, Market Research, Performance Analytics.',
                'path_learning_resources': 'Managerial training programs, Leadership coaching, Cross-functional projects, Industry conferences.',
                'path_timeline': '18-24 months'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pathway Details")
        path_role = st.text_input("Current Role", value=st.session_state.get('path_role', ''), placeholder="e.g., Junior Developer, HR Generalist", key="path_role_input")
        path_target_level = st.text_input("Target Role/Level", value=st.session_state.get('path_target_level', ''), placeholder="e.g., Senior Developer, HR Business Partner", key="path_target_level_input")
        path_timeline = st.text_input("Proposed Timeline", value=st.session_state.get('path_timeline', ''), placeholder="e.g., 6 months, 1 year, 2 years", key="path_timeline_input")
        
    with col2:
        st.subheader("Content & Resources")
        path_current_skills = st.text_area("Current Skills/Strengths", height=70, value=st.session_state.get('path_current_skills', ''), placeholder="e.g., Communication, Technical skills", key="path_current_skills_input")
        path_skills_to_develop = st.text_area("Skills/Competencies to Develop", height=100, value=st.session_state.get('path_skills_to_develop', ''), placeholder="e.g., Leadership, Data Analysis, Strategic Thinking", key="path_skills_to_develop_input")
        path_learning_resources = st.text_area("Recommended Learning Resources/Activities", height=100, value=st.session_state.get('path_learning_resources', ''), placeholder="e.g., Online courses, Mentorship, Projects", key="path_learning_resources_input")
        
        if st.button("🛤️ Generate Learning Pathway", type="primary", key="generate_learning_pathway"):
            if path_role and path_target_level and path_skills_to_develop:
                prompt = f"""Create a personalized learning pathway for an individual in the '{path_role}' role aiming for '{path_target_level}'.

Proposed Timeline: {path_timeline}
Current Skills/Strengths: {path_current_skills}
Skills/Competencies to Develop: {path_skills_to_develop}
Recommended Learning Resources/Activities: {path_learning_resources}

The learning pathway should include:
- PATHWAY OVERVIEW (Current Role, Target Role, Timeline, Purpose)
- SKILLS GAP ANALYSIS (Identify key skills to bridge)
- LEARNING OBJECTIVES (SMART goals for skill acquisition)
- MODULES/PHASES OF LEARNING (Breakdown into logical stages)
- RECOMMENDED RESOURCES (Specific courses, books, tools, mentors)
- EXPERIENTIAL LEARNING (Projects, stretch assignments, job shadowing)
- MILESTONES AND CHECKPOINTS (Progress tracking, review dates)
- MEASUREMENT OF SUCCESS (How will skill acquisition be validated?)
- SUPPORT MECHANISMS (Manager support, peer learning, coaching)

Ensure the pathway is actionable, realistic, and tailored to individual growth."""

                with st.spinner(f"Generating learning pathway for {path_role} to {path_target_level}..."):
                    content = generate_content(prompt, "Learning Pathway")
                    if content:
                        st.session_state.generated_content['learning_pathway'] = content
            else:
                st.error("Please fill in Current Role, Target Role, and Skills to Develop.")
    
    # Display generated content
    if 'learning_pathway' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated Learning Pathway for {path_role} to {path_target_level}")
        cleaned_content = clean_text(st.session_state.generated_content['learning_pathway'])
        st.text_area("Learning Pathway Content", value=cleaned_content, height=400, key="learning_pathway_output")
        create_download_button(cleaned_content, f"Learning_Pathway_{path_role.replace(' ', '_')}_{path_target_level.replace(' ', '_')}", "📥 Download Learning Pathway")

# Tab 5: Course Communication Templates
with tab5:
    st.header("📧 Course Communication Templates")
    st.markdown("Write email templates for training announcements, invitations, reminders, and follow-ups.")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Templates")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Training Invitation Email", type="secondary", key="sample_comm_invite"):
            st.session_state.update({
                'comm_type': 'Training Invitation',
                'course_name_comm': 'Advanced Excel for Data Analysis',
                'course_date_time_comm': 'August 15, 2024, 9:00 AM - 5:00 PM IST',
                'course_platform_comm': 'Microsoft Teams',
                'course_audience_comm': 'Employees working with data',
                'course_objectives_comm': 'Master advanced Excel functions, create dynamic dashboards, perform data analysis.',
                'course_cta_comm': 'Register by August 10th via the Learning Portal link provided.',
                'course_sender_comm': 'L&D Department'
            })
    
    with col_sample2:
        if st.button("Post-Course Follow-up Email", type="secondary", key="sample_comm_followup"):
            st.session_state.update({
                'comm_type': 'Post-Course Follow-up',
                'course_name_comm': 'Effective Communication Skills',
                'course_date_time_comm': 'July 1-3, 2024',
                'course_platform_comm': 'In-person Workshop',
                'course_audience_comm': 'All Participants',
                'course_objectives_comm': 'N/A (follow-up)',
                'course_cta_comm': 'Complete the feedback survey, access supplementary materials, apply learned skills.',
                'course_sender_comm': 'L&D Team'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Communication Details")
        comm_type = st.selectbox("Communication Type", ["Training Invitation", "Reminder Email", "Post-Course Follow-up", "Certification Announcement"], key="comm_type_select")
        course_name_comm = st.text_input("Course/Program Name", value=st.session_state.get('course_name_comm', ''), key="course_name_comm_input")
        course_date_time_comm = st.text_input("Date/Time/Duration", value=st.session_state.get('course_date_time_comm', ''), placeholder="e.g., Aug 15, 9 AM - 5 PM", key="course_date_time_comm_input")
        course_platform_comm = st.text_input("Platform/Location", value=st.session_state.get('course_platform_comm', ''), placeholder="e.g., Zoom, Conference Room A", key="course_platform_comm_input")
        
    with col2:
        st.subheader("Content & Call to Action")
        course_audience_comm = st.text_input("Target Audience", value=st.session_state.get('course_audience_comm', ''), placeholder="e.g., All Employees, Sales Team", key="course_audience_comm_input")
        course_objectives_comm = st.text_area("Key Objectives/Benefits (for invitation)", height=70, value=st.session_state.get('course_objectives_comm', ''), placeholder="e.g., Learn X, Improve Y", key="course_objectives_comm_input")
        course_cta_comm = st.text_area("Call to Action", height=70, value=st.session_state.get('course_cta_comm', ''), placeholder="e.g., Register here, Complete survey", key="course_cta_comm_input")
        course_sender_comm = st.text_input("Sender Name/Department", value=st.session_state.get('course_sender_comm', ''), key="course_sender_comm_input")
        
        if st.button("📧 Generate Communication", type="primary", key="generate_course_comm"):
            if comm_type and course_name_comm:
                prompt = f"""Draft an email template for a '{comm_type}' related to the course/program '{course_name_comm}'.

Course Date/Time/Duration: {course_date_time_comm}
Platform/Location: {course_platform_comm}
Target Audience: {course_audience_comm}
Key Objectives/Benefits (for invitation): {course_objectives_comm if course_objectives_comm else 'N/A'}
Call to Action: {course_cta_comm if course_cta_comm else 'None'}
Sender Name/Department: {course_sender_comm}

The email should be:
- Professional and engaging.
- Clearly state the purpose of the communication.
- Include all relevant details.
- Have a clear subject line and call to action.
- Use placeholders for personalization (e.g., [Participant Name])."""

                with st.spinner(f"Generating {comm_type.lower()} for {course_name_comm}..."):
                    content = generate_content(prompt, "Course Communication")
                    if content:
                        st.session_state.generated_content['course_comm'] = content
            else:
                st.error("Please fill in Communication Type and Course/Program Name.")
    
    # Display generated content
    if 'course_comm' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader(f"📄 Generated {comm_type} for {course_name_comm}")
        cleaned_content = clean_text(st.session_state.generated_content['course_comm'])
        st.text_area("Communication Content", value=cleaned_content, height=400, key="course_comm_output")
        create_download_button(cleaned_content, f"Course_Comm_{comm_type.replace(' ', '_')}_{course_name_comm.replace(' ', '_')}", "📥 Download Communication")

# Tab 6: Custom L&D Tools
with tab6:
    st.header("🎨 Custom L&D & Capability Development Tools")
    st.markdown("Create any L&D document, framework, or strategy.")
    
    # Sample prompts
    st.subheader("🎯 Best Practice L&D Prompts")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("Sample: Skills Gap Analysis Framework", type="secondary", key="sample_custom_skills_gap"):
            st.session_state['custom_prompt_lnd'] = """Design a framework for conducting a company-wide skills gap analysis.

Objectives:
- Identify critical skill gaps for future business needs.
- Inform L&D strategy and program development.
- Support talent mobility and succession planning.

Include:
- Methodology for identifying current and future skills.
- Data collection methods (e.g., surveys, assessments, performance data).
- Analysis and reporting approach.
- Action planning integration (training, hiring, redeployment).
- Stakeholder roles and responsibilities."""
    
    with col_sample2:
        if st.button("Sample: Mentorship Program Guidelines", type="secondary", key="sample_custom_mentorship"):
            st.session_state['custom_prompt_lnd'] = """Develop comprehensive guidelines for a new internal mentorship program.

Goals:
- Foster employee development and knowledge transfer.
- Enhance leadership capabilities.
- Improve retention and engagement.

Cover:
- Program objectives and benefits.
- Roles and responsibilities of mentors and mentees.
- Matching process and criteria.
- Program duration and structure (e.g., meeting frequency, topics).
- Resources and tools for participants.
- Evaluation and feedback mechanisms."""
    
    st.markdown("---")
    
    # Custom prompt input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💭 Your Custom L&D Request")
        custom_prompt_lnd = st.text_area(
            "Enter your L&D question/request:",
            height=250,
            value=st.session_state.get('custom_prompt_lnd', ''),
            placeholder="""Examples:
• Create a framework for measuring training ROI.
• Design a gamified learning experience for compliance training.
• Develop a strategy for promoting a culture of continuous learning.
• Generate a checklist for evaluating external training vendors.
• Propose a framework for building a leadership pipeline."""
        , key="custom_prompt_lnd_input")
        
        # Context options
        st.subheader("🎯 Context & Customization")
        col_context1, col_context2 = st.columns(2)
        
        with col_context1:
            company_context_lnd = st.selectbox(
                "Organization Type",
                ["Technology Company", "Financial Services", "Manufacturing", "Retail", "Healthcare", "Professional Services", "Startup", "Large Enterprise", "Non-profit", "Government", "Custom"],
                index=0,
                key="company_context_lnd_select"
            )
            
            if company_context_lnd == "Custom":
                custom_company_lnd = st.text_input("Enter your organization context:", key="custom_company_lnd_input")
                company_context_lnd = custom_company_lnd
            
            tool_type_lnd = st.selectbox(
                "Tool Type",
                ["Framework", "Strategy Document", "Guidelines", "Assessment Tool", "Training Module Outline", "Policy", "Other"],
                key="tool_type_lnd_select"
            )
        
        with col_context2:
            detail_level_lnd = st.selectbox(
                "Detail Level",
                ["Comprehensive (Detailed)", "Standard (Moderate)", "Overview (High-level)"],
                key="detail_level_lnd_select"
            )
            
            target_users_lnd = st.multiselect(
                "Target Users",
                ["L&D Team", "Employees", "Managers", "HR Business Partners", "Senior Leadership", "All Stakeholders"],
                default=["L&D Team", "Managers"],
                key="target_users_lnd_multiselect"
            )
    
    with col2:
        st.subheader("🚀 Generate Content")
        
        if st.button("🎨 Generate Custom L&D Tool", type="primary", key="generate_custom_lnd_tool"):
            if custom_prompt_lnd.strip():
                enhanced_prompt = f"""
                Organization Context: {company_context_lnd}
                Tool Type: {tool_type_lnd}
                Target Users: {', '.join(target_users_lnd)}
                Detail Level: {detail_level_lnd}
                
                L&D Request: {custom_prompt_lnd}
                
                Create professional content for L&D and capability development that:
                1. Is specific to the organization context provided.
                2. Follows best practices in adult learning and talent development.
                3. Is appropriate for the target users.
                4. Matches the requested detail level.
                5. Is immediately implementable and actionable.
                6. Includes relevant frameworks, guidelines, or strategies.
                7. Focuses on enhancing employee skills and organizational capabilities.
                8. Considers measurement and impact.
                
                If this is a framework, ensure clear components and interdependencies.
                If this is a strategy, include objectives, initiatives, and success metrics.
                If this is a guideline, ensure clarity and practical applicability.
                """
                
                with st.spinner("Creating your custom L&D tool..."):
                    content = generate_content(enhanced_prompt, "Custom L&D Tool")
                    if content:
                        st.session_state.generated_content['custom_lnd'] = content
            else:
                st.error("Please enter your L&D request.")
        
        # Additional options
        st.markdown("---")
        st.subheader("📋 Quick Actions")
        
        if st.button("🔄 Clear Form", key="clear_custom_lnd_form"):
            st.session_state['custom_prompt_lnd'] = ''
            if 'custom_lnd' in st.session_state.generated_content:
                del st.session_state.generated_content['custom_lnd']
            st.rerun()
        
        if st.button("💡 Get Ideas", key="get_custom_lnd_ideas"):
            st.session_state['custom_prompt_lnd'] = """Suggest 5 innovative approaches to employee upskilling and reskilling:

- Micro-learning modules integrated into daily workflows.
- Internal expert-led workshops and knowledge-sharing sessions.
- AI-driven personalized learning recommendations and content curation.
- Project-based learning with real-world business challenges.
- Cross-functional rotations and stretch assignments for skill diversification."""
    
    # Display generated content
    if 'custom_lnd' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Custom L&D Tool")
        cleaned_content = clean_text(st.session_state.generated_content['custom_lnd'])
        st.text_area("Custom L&D Tool Content", value=cleaned_content, height=400, key="custom_lnd_output")
        create_download_button(cleaned_content, f"Custom_LND_Tool_{datetime.now().strftime('%Y%m%d_%H%M')}", "📥 Download L&D Tool")

# Footer
st.markdown("---")
st.markdown("### 🚀 Ready for the next module?")
st.info("This is Module 7 of 9. Continue building your comprehensive HR toolkit with additional specialized modules.")

# Navigation
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("← Module 6: Process Digitization", key="nav_prev_lnd"):
        st.switch_page("pages/06_process_digitization.py")

with col_nav2:
    if st.button("🏠 Back to Main Menu"):
        st.switch_page("pages/00_home.py")

with col_nav3:
    if st.button("Module 8: Compensation & Rewards →", key="nav_next_lnd", disabled=True):
        st.info("Coming Soon!")
