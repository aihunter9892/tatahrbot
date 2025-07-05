import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="HR Copilot - Performance Management & Employee Development",
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
    st.markdown("### 🎯 Module 4: Performance Management")
    st.markdown("Drive performance excellence and employee development")
    
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
            
            system_prompt = """You are a senior HR performance management specialist with 15+ years of experience in employee development, performance reviews, goal setting, and talent management.

CRITICAL INSTRUCTIONS:
- Write ONLY the document content, nothing else
- Do NOT include explanatory text, introductions, or commentary
- Do NOT write phrases like "Here's a comprehensive..." or "I'll create..."
- Start directly with the document content
- Use simple, clean formatting without markdown symbols
- Use CAPITAL LETTERS for main headings
- Use numbered lists and bullet points with dashes (-)
- Keep language professional, actionable, and results-focused
- Include specific examples and metrics where relevant
- Make all content immediately usable in corporate environments

Focus on practical, implementable solutions that drive real performance improvements and employee growth."""
            
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
st.title("🎯 HR Copilot - Performance Management & Employee Development")
st.markdown("Create comprehensive performance management systems and development frameworks")

# Tab layout
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Performance Review Templates",
    "🎯 Goal Setting Framework", 
    "📈 Development Plans",
    "💼 Career Progression Maps",
    "🏆 Recognition Programs",
    "🎨 Custom Performance Tools"
])

# Tab 1: Performance Review Templates
with tab1:
    st.header("📊 Performance Review Templates")
    st.markdown("Create comprehensive performance evaluation forms and review processes")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Templates")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("👤 Individual Contributor Review", type="secondary", key="sample_perf_ic"):
            st.session_state.update({
                'employee_name_perf': 'Rajesh Kumar',
                'position_perf': 'Senior Software Developer',
                'department_perf': 'Technology',
                'manager_perf': 'Priya Sharma',
                'review_period': 'January 2024 - December 2024',
                'review_type': 'Annual Performance Review'
            })
    
    with col_sample2:
        if st.button("👥 Manager/Leadership Review", type="secondary", key="sample_perf_manager"):
            st.session_state.update({
                'employee_name_perf': 'Anita Desai',
                'position_perf': 'Engineering Manager',
                'department_perf': 'Product Engineering',
                'manager_perf': 'Vikram Singh',
                'review_period': 'January 2024 - December 2024',
                'review_type': 'Leadership Performance Review'
            })
    
    with col_sample3:
        if st.button("🎓 Graduate/Junior Review", type="secondary", key="sample_perf_junior"):
            st.session_state.update({
                'employee_name_perf': 'Arjun Patel',
                'position_perf': 'Associate Software Engineer',
                'department_perf': 'Technology',
                'manager_perf': 'Meera Joshi',
                'review_period': 'July 2024 - December 2024',
                'review_type': 'Mid-Year Development Review'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Employee Information")
        # Added unique keys here
        employee_name_perf = st.text_input("Employee Name", value=st.session_state.get('employee_name_perf', ''), key="employee_name_perf_input")
        position_perf = st.text_input("Position/Role", value=st.session_state.get('position_perf', ''), key="position_perf_input")
        department_perf = st.text_input("Department", value=st.session_state.get('department_perf', ''), key="department_perf_input")
        manager_perf = st.text_input("Manager/Reviewer", value=st.session_state.get('manager_perf', ''), key="manager_perf_input")
    
    with col2:
        st.subheader("Review Details")
        review_period = st.text_input("Review Period", value=st.session_state.get('review_period', ''), key="review_period_input")
        review_type_options = [
            "Annual Performance Review",
            "Mid-Year Review", 
            "Quarterly Check-in",
            "Leadership Performance Review",
            "Development Review",
            "Probation Review"
        ]
        review_type = st.selectbox("Review Type", review_type_options, key="review_type_select")
        
        if st.button("📊 Generate Performance Review Template", type="primary", key="generate_perf_review"):
            if employee_name_perf and position_perf:
                prompt = f"""Create a comprehensive performance review template for:

Employee: {employee_name_perf}
Position: {position_perf}
Department: {department_perf}
Manager: {manager_perf}
Review Period: {review_period}
Review Type: {review_type}

Create a detailed performance review template that includes:

EMPLOYEE INFORMATION SECTION
- Basic details and role summary

PERFORMANCE RATINGS SECTION
Create rating scales (1-5) for:
- Job Knowledge and Technical Skills
- Quality of Work
- Productivity and Efficiency
- Communication and Collaboration
- Problem Solving and Initiative
- Reliability and Dependability
- Leadership and Mentoring (if applicable)
- Goal Achievement
- Professional Development

GOAL REVIEW SECTION
- Previous period goals and achievement status
- Quantitative results and metrics
- Qualitative achievements and improvements
- Challenges faced and how they were addressed

STRENGTHS AND ACCOMPLISHMENTS
- Key achievements during review period
- Recognition and awards received
- Positive feedback from colleagues/clients
- Skills demonstrating growth

AREAS FOR IMPROVEMENT
- Development opportunities identified
- Skills gaps to address
- Behavioral improvements needed
- Performance enhancement suggestions

DEVELOPMENT PLANNING
- Learning and development needs
- Training recommendations
- Stretch assignments and projects
- Mentoring or coaching requirements

GOAL SETTING FOR NEXT PERIOD
- SMART goals framework
- Performance objectives
- Development objectives
- Career progression milestones

MANAGER COMMENTS SECTION
- Overall performance summary
- Specific feedback and observations
- Recognition of contributions
- Development recommendations

EMPLOYEE SELF-ASSESSMENT SECTION
- Self-reflection on performance
- Personal achievements and challenges
- Career aspirations and interests
- Support needed from organization

ACTION ITEMS AND NEXT STEPS
- Specific development actions
- Timeline for improvements
- Resources and support required
- Follow-up schedule

Create detailed sections with clear instructions for both manager and employee. Include rating guidelines and example comments to ensure consistency and fairness."""

                with st.spinner("Creating performance review template..."):
                    content = generate_content(prompt, "Performance Review")
                    if content:
                        st.session_state.generated_content['performance_review'] = content
            else:
                st.error("Please fill in Employee Name and Position")
    
    # Display generated content
    if 'performance_review' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📋 Generated Performance Review Template")
        cleaned_content = clean_text(st.session_state.generated_content['performance_review'])
        st.text_area("Performance Review Content", value=cleaned_content, height=400, key="perf_review_output")
        create_download_button(cleaned_content, f"Performance_Review_{employee_name_perf.replace(' ', '_')}", "📥 Download Performance Review")

# Tab 2: Goal Setting Framework
with tab2:
    st.header("🎯 Goal Setting Framework")
    st.markdown("Create SMART goals and objective-setting frameworks")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Goals")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("💻 Technical Goals", type="secondary", key="sample_goals_tech"):
            st.session_state.update({
                'employee_name_goals': 'Kavya Reddy',
                'role_goals': 'Full Stack Developer',
                'goal_period': '2024',
                'focus_areas': 'Technical skills development, Project delivery, Code quality, Team collaboration',
                'business_objectives': 'Improve application performance, Reduce deployment time, Enhance user experience'
            })
    
    with col_sample2:
        if st.button("📊 Sales Goals", type="secondary", key="sample_goals_sales"):
            st.session_state.update({
                'employee_name_goals': 'Rohit Agarwal',
                'role_goals': 'Sales Manager',
                'goal_period': '2024',
                'focus_areas': 'Revenue growth, Client acquisition, Team development, Market expansion',
                'business_objectives': 'Achieve 120% of sales target, Expand into 3 new territories, Build high-performing sales team'
            })
    
    with col_sample3:
        if st.button("👥 Leadership Goals", type="secondary", key="sample_goals_leadership"):
            st.session_state.update({
                'employee_name_goals': 'Deepika Sharma',
                'role_goals': 'HR Director',
                'goal_period': '2024',
                'focus_areas': 'Team leadership, Strategic planning, Culture development, Talent management',
                'business_objectives': 'Improve employee engagement by 15%, Reduce turnover by 20%, Implement new performance system'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Employee & Role Information")
        # Added unique keys here
        employee_name_goals = st.text_input("Employee Name", value=st.session_state.get('employee_name_goals', ''), key="employee_name_goals_input")
        role_goals = st.text_input("Role/Position", value=st.session_state.get('role_goals', ''), key="role_goals_input")
        goal_period = st.text_input("Goal Period (e.g., 2024, Q1 2024)", value=st.session_state.get('goal_period', ''), key="goal_period_input")
    
    with col2:
        st.subheader("Goal Focus Areas")
        focus_areas = st.text_area("Key Focus Areas", height=100, value=st.session_state.get('focus_areas', ''), key="focus_areas_input")
        business_objectives = st.text_area("Business Objectives", height=100, value=st.session_state.get('business_objectives', ''), key="business_objectives_input")
        
        if st.button("🎯 Generate Goal Setting Framework", type="primary", key="generate_goal_framework"):
            if employee_name_goals and role_goals:
                prompt = f"""Create a comprehensive goal setting framework for:

Employee: {employee_name_goals}
Role: {role_goals}
Goal Period: {goal_period}
Focus Areas: {focus_areas}
Business Objectives: {business_objectives}

Create a detailed SMART goals framework that includes:

GOAL SETTING OVERVIEW
- Purpose and importance of goal setting
- SMART criteria explanation (Specific, Measurable, Achievable, Relevant, Time-bound)
- Alignment with organizational objectives

PERFORMANCE GOALS SECTION
Create 3-5 specific performance goals:

For each goal include:
- Goal Statement (clear and specific)
- Success Metrics (quantifiable measures)
- Target Completion Date
- Resources Needed
- Potential Challenges and Mitigation
- Progress Milestones
- Success Indicators

DEVELOPMENT GOALS SECTION
Create 2-3 professional development goals:

For each development goal include:
- Skill or competency to develop
- Learning methods and resources
- Application opportunities
- Measurement criteria
- Timeline for development
- Support required

CAREER GOALS SECTION
- Short-term career objectives (6-12 months)
- Long-term career aspirations (2-3 years)
- Skills needed for advancement
- Experience requirements
- Networking and visibility plans

GOAL TRACKING FRAMEWORK
- Monthly check-in template
- Quarterly review process
- Progress tracking tools
- Adjustment mechanisms
- Success celebration plans

SUPPORT AND RESOURCES
- Manager support required
- Training and development needs
- Mentoring relationships
- Tools and technology needs
- Budget requirements

GOAL ACHIEVEMENT STRATEGIES
- Action planning methodology
- Time management techniques
- Priority setting framework
- Obstacle management approach
- Motivation and accountability systems

MEASUREMENT AND EVALUATION
- Key Performance Indicators (KPIs)
- Progress tracking metrics
- Regular review schedule
- Success criteria definition
- Performance documentation

Make each goal specific to the role and align with the business objectives provided. Include practical examples and actionable steps."""

                with st.spinner("Creating goal setting framework..."):
                    content = generate_content(prompt, "Goal Setting Framework")
                    if content:
                        st.session_state.generated_content['goal_framework'] = content
            else:
                st.error("Please fill in Employee Name and Role")
    
    # Display generated content
    if 'goal_framework' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("🎯 Generated Goal Setting Framework")
        cleaned_content = clean_text(st.session_state.generated_content['goal_framework'])
        st.text_area("Goal Framework Content", value=cleaned_content, height=400, key="goal_framework_output")
        create_download_button(cleaned_content, f"Goal_Framework_{employee_name_goals.replace(' ', '_')}", "📥 Download Goal Framework")

# Tab 3: Development Plans
with tab3:
    st.header("📈 Individual Development Plans (IDP)")
    st.markdown("Create personalized development roadmaps for employee growth")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Development Plans")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("⚙️ Technical Development", type="secondary", key="sample_dev_tech"):
            st.session_state.update({
                'employee_name_dev': 'Arun Kumar',
                'current_role_dev': 'Software Engineer',
                'target_role_dev': 'Senior Software Engineer / Tech Lead',
                'timeframe_dev': '12-18 months',
                'current_skills': 'Java, Spring Boot, MySQL, REST APIs, Git',
                'skill_gaps': 'Microservices architecture, Cloud platforms (AWS), System design, Team leadership',
                'career_interests': 'Technical leadership, Architecture design, Mentoring junior developers'
            })
    
    with col_sample2:
        if st.button("📊 Management Development", type="secondary", key="sample_dev_management"):
            st.session_state.update({
                'employee_name_dev': 'Priya Nair',
                'current_role_dev': 'Senior Marketing Specialist',
                'target_role_dev': 'Marketing Manager',
                'timeframe_dev': '9-12 months',
                'current_skills': 'Digital marketing, Content creation, Analytics, Campaign management',
                'skill_gaps': 'Team management, Budget planning, Strategic thinking, Stakeholder management',
                'career_interests': 'People management, Strategic marketing, Brand building, Cross-functional leadership'
            })
    
    with col_sample3:
        if st.button("🎯 Cross-functional Development", type="secondary", key="sample_dev_crossfunc"):
            st.session_state.update({
                'employee_name_dev': 'Vikram Singh',
                'current_role_dev': 'Business Analyst',
                'target_role_dev': 'Product Manager',
                'timeframe_dev': '15-24 months',
                'current_skills': 'Requirements analysis, Process mapping, SQL, Stakeholder communication',
                'skill_gaps': 'Product strategy, User experience design, Market research, Technical product knowledge',
                'career_interests': 'Product management, User experience, Technology strategy, Innovation'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Employee & Role Information")
        # Added unique keys here
        employee_name_dev = st.text_input("Employee Name", value=st.session_state.get('employee_name_dev', ''), key="employee_name_dev_input")
        current_role_dev = st.text_input("Current Role", value=st.session_state.get('current_role_dev', ''), key="current_role_dev_input")
        target_role_dev = st.text_input("Target Role/Career Goal", value=st.session_state.get('target_role_dev', ''), key="target_role_dev_input")
        timeframe_dev = st.text_input("Development Timeframe", value=st.session_state.get('timeframe_dev', ''), key="timeframe_dev_input")
    
    with col2:
        st.subheader("Skills & Development Areas")
        skill_gaps = st.text_area("Skill Gaps to Address", height=80, value=st.session_state.get('skill_gaps', ''), key="skill_gaps_input")
        current_skills = st.text_area("Current Skills & Strengths", height=80, value=st.session_state.get('current_skills', ''), key="current_skills_input")
        career_interests = st.text_area("Career Interests & Aspirations", height=80, value=st.session_state.get('career_interests', ''), key="career_interests_input")
        
        if st.button("📈 Generate Development Plan", type="primary", key="generate_dev_plan"):
            if employee_name_dev and current_role_dev:
                prompt = f"""Create a comprehensive Individual Development Plan (IDP) for:

Employee: {employee_name_dev}
Current Role: {current_role_dev}
Target Role: {target_role_dev}
Timeframe: {timeframe_dev}
Current Skills: {current_skills}
Skill Gaps: {skill_gaps}
Career Interests: {career_interests}

Create a detailed development plan that includes:

DEVELOPMENT OVERVIEW
- Employee profile and current state
- Career aspirations and target role
- Development timeframe and milestones
- Success criteria and measurement

SKILLS ASSESSMENT
- Current skills inventory and rating
- Skill gaps analysis
- Competency requirements for target role
- Priority areas for development
- Strengths to leverage

DEVELOPMENT OBJECTIVES
Create 4-6 specific development objectives covering:
- Technical/functional skills
- Leadership and management capabilities
- Communication and interpersonal skills
- Business acumen and strategic thinking
- Industry knowledge and expertise

For each objective include:
- Specific development goal
- Learning methods and activities
- Resources and tools needed
- Timeline and milestones
- Success measures
- Application opportunities

LEARNING AND DEVELOPMENT ACTIVITIES
- Formal training programs and courses
- Certification requirements
- Conference and workshop attendance
- Online learning platforms and resources
- Books, articles, and research materials
- Mentoring and coaching arrangements
- Job shadowing and cross-training
- Stretch assignments and projects
- Volunteer and committee participation

EXPERIENCE-BASED DEVELOPMENT
- Special projects and assignments
- Cross-functional collaboration
- Leadership opportunities
- Problem-solving challenges
- Innovation and improvement initiatives
- Client or stakeholder interaction
- Process improvement projects

SUPPORT STRUCTURE
- Manager support and involvement
- Mentor assignment and expectations
- Peer learning partnerships
- Expert guidance and subject matter experts
- Budget allocation for development
- Time allocation for learning activities

TIMELINE AND MILESTONES
- 3-month development targets
- 6-month progress checkpoints
- 12-month major milestones
- Long-term development goals
- Regular review and adjustment points

PROGRESS TRACKING
- Monthly self-assessment process
- Quarterly manager reviews
- Skills progression tracking
- Goal achievement measurement
- Feedback collection methods
- Documentation requirements

CAREER ADVANCEMENT PATH
- Next role readiness indicators
- Internal opportunity identification
- Network building strategies
- Visibility and recognition plans
- Performance demonstration opportunities

Make the plan specific, actionable, and aligned with both individual aspirations and organizational needs. Include practical steps and realistic timelines."""

                with st.spinner("Creating individual development plan..."):
                    content = generate_content(prompt, "Development Plan")
                    if content:
                        st.session_state.generated_content['development_plan'] = content
            else:
                st.error("Please fill in Employee Name and Current Role")
    
    # Display generated content
    if 'development_plan' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📈 Generated Individual Development Plan")
        cleaned_content = clean_text(st.session_state.generated_content['development_plan'])
        st.text_area("Development Plan Content", value=cleaned_content, height=400, key="dev_plan_output")
        create_download_button(cleaned_content, f"Development_Plan_{employee_name_dev.replace(' ', '_')}", "📥 Download Development Plan")

# Tab 4: Career Progression Maps
with tab4:
    st.header("💼 Career Progression Maps")
    st.markdown("Design clear career pathways and advancement frameworks")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Career Paths")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("💻 Technology Career Path", type="secondary", key="sample_career_tech"):
            st.session_state.update({
                'department_career': 'Technology',
                'career_function': 'Software Development',
                'entry_level': 'Associate Software Engineer',
                'career_tracks': 'Individual Contributor Track, Management Track, Architecture Track',
                'key_competencies': 'Programming, System design, Problem solving, Communication, Leadership'
            })
    
    with col_sample2:
        if st.button("📊 Sales Career Path", type="secondary", key="sample_career_sales"):
            st.session_state.update({
                'department_career': 'Sales & Marketing',
                'career_function': 'Sales',
                'entry_level': 'Sales Associate',
                'career_tracks': 'Sales Specialist Track, Sales Management Track, Key Account Management Track',
                'key_competencies': 'Sales skills, Relationship building, Negotiation, Strategic thinking, Team leadership'
            })
    
    with col_sample3:
        if st.button("👥 HR Career Path", type="secondary", key="sample_career_hr"):
            st.session_state.update({
                'department_career': 'Human Resources',
                'career_function': 'HR Generalist',
                'entry_level': 'HR Associate',
                'career_tracks': 'HR Specialist Track, HR Business Partner Track, HR Leadership Track',
                'key_competencies': 'HR expertise, Business acumen, Communication, Change management, Strategic planning'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Career Path Information")
        # Added unique keys here
        department_career = st.text_input("Department/Function", value=st.session_state.get('department_career', ''), key="department_career_input")
        career_function = st.text_input("Career Function Area", value=st.session_state.get('career_function', ''), key="career_function_input")
        entry_level = st.text_input("Entry Level Position", value=st.session_state.get('entry_level', ''), key="entry_level_input")
    
    with col2:
        st.subheader("Career Development Framework")
        career_tracks = st.text_area("Career Tracks Available", height=100, value=st.session_state.get('career_tracks', ''), key="career_tracks_input")
        key_competencies = st.text_area("Key Competencies", height=100, value=st.session_state.get('key_competencies', ''), key="key_competencies_input")
        
        if st.button("💼 Generate Career Progression Map", type="primary", key="generate_career_map"):
            if department_career and career_function:
                prompt = f"""Create a comprehensive career progression map for:

Department: {department_career}
Career Function: {career_function}
Entry Level: {entry_level}
Career Tracks: {career_tracks}
Key Competencies: {key_competencies}

Create a detailed career progression framework that includes:

CAREER PATHWAY OVERVIEW
- Function description and scope
- Career philosophy and principles
- Multiple progression tracks available
- Advancement criteria and timelines
- Growth opportunities and flexibility

CAREER LEVEL STRUCTURE
For each career level define:

ENTRY LEVEL
- Position title and grade
- Key responsibilities and scope
- Required qualifications and experience
- Core competencies needed
- Typical tenure at level
- Performance expectations

MID-LEVEL POSITIONS
- Position titles and progression options
- Expanded responsibilities
- Advanced skill requirements
- Leadership and mentoring expectations
- Decision-making authority
- Cross-functional collaboration needs

SENIOR LEVEL POSITIONS
- Senior role options and specializations
- Strategic responsibilities
- Expert-level competencies required
- Leadership and influence expectations
- Innovation and improvement contributions
- Stakeholder management requirements

LEADERSHIP POSITIONS
- Management and director-level roles
- Team leadership responsibilities
- Strategic planning and execution
- Business impact and P&L ownership
- Organization development duties
- External representation requirements

COMPETENCY FRAMEWORK
For each career level outline:

TECHNICAL COMPETENCIES
- Functional expertise requirements
- Tool and technology proficiency
- Industry knowledge expectations
- Certification and credential needs
- Continuous learning requirements

LEADERSHIP COMPETENCIES
- People management skills
- Communication and influence
- Decision-making and judgment
- Change management capabilities
- Strategic thinking abilities

BUSINESS COMPETENCIES
- Business acumen and understanding
- Customer focus and market awareness
- Financial literacy and analysis
- Process improvement and efficiency
- Innovation and creative thinking

ADVANCEMENT CRITERIA
- Performance rating requirements
- Competency demonstration evidence
- Experience and tenure guidelines
- Education and certification needs
- Leadership and impact examples
- 360-degree feedback results

DEVELOPMENT OPPORTUNITIES
- Training and education programs
- Mentoring and coaching options
- Stretch assignments and projects
- Cross-functional rotations
- External learning experiences
- Professional association involvement

ALTERNATIVE CAREER PATHS
- Lateral movement opportunities
- Cross-functional transitions
- Specialist vs. generalist tracks
- Geographic mobility options
- Project-based career options
- Consulting and advisory roles

CAREER PLANNING PROCESS
- Annual career discussions
- Development planning sessions
- Goal setting and tracking
- Progress review mechanisms
- Support and resource allocation
- Timeline expectations and flexibility

Create specific, actionable progression criteria and make the pathway clear and achievable for employees at all levels."""

                with st.spinner("Creating career progression map..."):
                    content = generate_content(prompt, "Career Progression Map")
                    if content:
                        st.session_state.generated_content['career_map'] = content
            else:
                st.error("Please fill in Department and Career Function")
    
    # Display generated content
    if 'career_map' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("💼 Generated Career Progression Map")
        cleaned_content = clean_text(st.session_state.generated_content['career_map'])
        st.text_area("Career Map Content", value=cleaned_content, height=400, key="career_map_output")
        create_download_button(cleaned_content, f"Career_Map_{department_career.replace(' ', '_')}", "📥 Download Career Map")

# Tab 5: Recognition Programs
with tab5:
    st.header("🏆 Recognition Programs")
    st.markdown("Design employee recognition and reward systems")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Recognition Programs")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("🌟 Peer Recognition Program", type="secondary", key="sample_recognition_peer"):
            st.session_state.update({
                'program_name': 'Peer Excellence Awards',
                'program_type': 'Peer-to-Peer Recognition',
                'target_audience': 'All employees',
                'recognition_frequency': 'Monthly',
                'program_objectives': 'Foster collaboration, Recognize daily contributions, Build positive culture, Encourage peer appreciation'
            })
    
    with col_sample2:
        if st.button("🎯 Performance Excellence", type="secondary", key="sample_recognition_performance"):
            st.session_state.update({
                'program_name': 'Performance Champion Awards',
                'program_type': 'Performance-Based Recognition',
                'target_audience': 'High performers across all levels',
                'recognition_frequency': 'Quarterly',
                'program_objectives': 'Reward exceptional performance, Motivate high achievement, Recognize goal attainment, Drive business results'
            })
    
    with col_sample3:
        if st.button("💡 Innovation Awards", type="secondary", key="sample_recognition_innovation"):
            st.session_state.update({
                'program_name': 'Innovation Excellence Program',
                'program_type': 'Innovation and Improvement Recognition',
                'target_audience': 'Innovators and process improvers',
                'recognition_frequency': 'Bi-annual',
                'program_objectives': 'Encourage innovation, Recognize creative solutions, Drive continuous improvement, Foster entrepreneurial thinking'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Program Information")
        # Added unique keys here
        program_name = st.text_input("Program Name", value=st.session_state.get('program_name', ''), key="program_name_input")
        program_type = st.text_input("Program Type", value=st.session_state.get('program_type', ''), key="program_type_input")
        target_audience = st.text_input("Target Audience", value=st.session_state.get('target_audience', ''), key="target_audience_input")
        recognition_frequency = st.text_input("Recognition Frequency", value=st.session_state.get('recognition_frequency', ''), key="recognition_frequency_input")
    
    with col2:
        st.subheader("Program Design")
        program_objectives = st.text_area("Program Objectives", height=150, value=st.session_state.get('program_objectives', ''), key="program_objectives_input")
        
        if st.button("🏆 Generate Recognition Program", type="primary", key="generate_recognition_program"):
            if program_name and program_type:
                prompt = f"""Create a comprehensive employee recognition program for:

Program Name: {program_name}
Program Type: {program_type}
Target Audience: {target_audience}
Recognition Frequency: {recognition_frequency}
Program Objectives: {program_objectives}

Create a detailed recognition program framework that includes:

PROGRAM OVERVIEW
- Program mission and vision
- Core values and principles
- Alignment with organizational culture
- Expected outcomes and benefits
- Program scope and coverage

RECOGNITION CATEGORIES
Create multiple recognition categories such as:
- Outstanding Performance Excellence
- Innovation and Creative Solutions
- Team Collaboration and Support
- Customer Service Excellence
- Leadership and Mentoring
- Continuous Improvement
- Values Demonstration
- Going Above and Beyond

For each category define:
- Specific criteria and requirements
- Examples of qualifying behaviors
- Nomination process and requirements
- Evaluation and selection method
- Recognition level and rewards

NOMINATION PROCESS
- Who can nominate (peers, managers, customers)
- Nomination criteria and guidelines
- Nomination form and requirements
- Supporting documentation needed
- Submission deadlines and process
- Review and approval workflow

EVALUATION AND SELECTION
- Review committee composition
- Evaluation criteria and scoring
- Selection process and timeline
- Fairness and transparency measures
- Appeals and feedback process
- Communication of results

RECOGNITION LEVELS AND REWARDS
- Bronze, Silver, Gold recognition tiers
- Monetary rewards and gift options
- Experience-based rewards (time off, events)
- Career development opportunities
- Public recognition and visibility
- Personalized appreciation methods
- Team-based vs individual recognition

PROGRAM IMPLEMENTATION
- Launch strategy and communication
- Training for managers and nominators
- Technology platform and tools
- Budget planning and allocation
- Resource requirements and support
- Timeline and rollout phases

COMMUNICATION STRATEGY
- Program awareness and promotion
- Success story sharing
- Regular updates and reminders
- Multiple communication channels
- Visual recognition displays
- Social media and internal platforms
- Leadership messaging and support

PROGRAM ADMINISTRATION
- Roles and responsibilities
- Administrative processes and workflows
- Record keeping and documentation
- Budget management and tracking
- Vendor management (if applicable)
- Quality assurance and compliance

MEASUREMENT AND EVALUATION
- Program success metrics and KPIs
- Employee satisfaction surveys
- Participation rates and trends
- Recognition distribution analysis
- Impact on engagement and retention
- ROI measurement and reporting
- Continuous improvement process

SUSTAINABILITY AND GROWTH
- Long-term program evolution
- Feedback incorporation mechanisms
- Program refresh and updates
- Expansion opportunities
- Integration with other HR programs
- Leadership development connections

Make the program engaging, fair, meaningful, and aligned with organizational values. Include practical implementation steps and clear guidelines for all stakeholders."""

                with st.spinner("Creating recognition program..."):
                    content = generate_content(prompt, "Recognition Program")
                    if content:
                        st.session_state.generated_content['recognition_program'] = content
            else:
                st.error("Please fill in Program Name and Program Type")
    
    # Display generated content
    if 'recognition_program' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("🏆 Generated Recognition Program")
        cleaned_content = clean_text(st.session_state.generated_content['recognition_program'])
        st.text_area("Recognition Program Content", value=cleaned_content, height=400, key="recognition_program_output")
        create_download_button(cleaned_content, f"Recognition_Program_{program_name.replace(' ', '_')}", "📥 Download Recognition Program")

# Tab 6: Custom Performance Tools
with tab6:
    st.header("🎨 Custom Performance Management Tools")
    st.markdown("Create any performance management document or framework")
    
    # Sample prompts
    st.subheader("🎯 Best Practice Performance Management Prompts")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("📊 Sample: 360-Degree Feedback", type="secondary", key="sample_custom_360"):
            st.session_state['custom_prompt_perf'] = """Design a comprehensive 360-degree feedback system for mid-level managers in a technology company.

Requirements:
- Include feedback from supervisors, peers, direct reports, and customers
- Focus on leadership competencies, communication skills, and business impact
- Provide clear rating scales and behavioral indicators
- Include development planning integration
- Ensure anonymity and psychological safety

Create:
- Feedback questionnaire design for each stakeholder group
- Competency framework and rating methodology
- Data collection and analysis process
- Feedback delivery and discussion framework
- Development planning integration
- Implementation timeline and best practices"""
    
    with col_sample2:
        if st.button("📈 Sample: Performance Improvement Plan", type="secondary", key="sample_custom_pip"):
            st.session_state['custom_prompt_perf'] = """Create a comprehensive Performance Improvement Plan (PIP) framework for underperforming employees.

Context:
- Address performance gaps while maintaining employee dignity
- Provide clear expectations and support mechanisms
- Include measurable goals and regular check-ins
- Focus on both performance and behavioral improvements
- Ensure legal compliance and documentation

Develop:
- PIP template with clear structure and requirements
- Performance standards and measurement criteria
- Support and development resources
- Progress tracking and review process
- Success criteria and evaluation methods
- Manager guidance and training materials"""
    
    with col_sample3:
        if st.button("🎯 Sample: Competency Framework", type="secondary", key="sample_custom_competency"):
            st.session_state['custom_prompt_perf'] = """Design a comprehensive competency framework for a financial services organization.

Scope:
- Core competencies for all employees
- Leadership competencies for managers
- Functional competencies by role family
- Behavioral indicators and proficiency levels
- Integration with performance management and development

Include:
- Competency model structure and definitions
- Proficiency levels and behavioral descriptions
- Assessment methods and tools
- Development planning alignment
- Career progression integration
- Implementation and rollout strategy"""
    
    st.markdown("---")
    
    # More sample prompts
    col_sample4, col_sample5 = st.columns(2)
    
    with col_sample4:
        if st.button("📋 Sample: Succession Planning", type="secondary", key="sample_custom_succession"):
            st.session_state['custom_prompt_perf'] = """Create a robust succession planning framework for critical leadership positions.

Focus Areas:
- Key position identification and risk assessment
- Talent pipeline development and readiness assessment
- Development acceleration programs
- Knowledge transfer and retention strategies
- Emergency succession protocols

Design:
- Succession planning process and methodology
- Candidate assessment and readiness evaluation
- Development planning for high-potential employees
- Risk mitigation and contingency planning
- Governance and review mechanisms
- Integration with performance and talent management"""
        
    with col_sample5:
        if st.button("🌟 Sample: Engagement Survey", type="secondary", key="sample_custom_engagement"):
            st.session_state['custom_prompt_perf'] = """Develop a comprehensive employee engagement survey and action planning framework.

Survey Components:
- Job satisfaction and role clarity
- Manager effectiveness and support
- Growth and development opportunities
- Recognition and rewards satisfaction
- Organizational culture and values alignment

Include:
- Survey design and question development
- Response analysis and interpretation methods
- Action planning templates and processes
- Manager toolkits for team discussions
- Follow-up and progress tracking mechanisms
- Best practices for driving sustainable improvements"""
    
    st.markdown("---")
    
    # Custom prompt input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💭 Your Custom Performance Management Request")
        custom_prompt = st.text_area(
            "Enter your performance management question/request:",
            height=250,
            value=st.session_state.get('custom_prompt_perf', ''),
            placeholder="""Examples:
• Create a talent calibration process for annual reviews
• Design a high-potential employee identification program
• Develop a manager effectiveness assessment tool
• Create a performance coaching conversation guide
• Design a career development planning template
• Build a skill gap analysis framework
• Create an onboarding performance tracking system
• Develop a remote work performance management approach""",
            key="custom_prompt_perf_input"
        )
        
        # Context options
        st.subheader("🎯 Context & Customization")
        col_context1, col_context2 = st.columns(2)
        
        with col_context1:
            company_context = st.selectbox(
                "Organization Type",
                ["Technology Company", "Financial Services", "Healthcare", "Manufacturing", "Retail", "Professional Services", "Startup", "Large Enterprise", "Custom"],
                index=0,
                key="company_context_select"
            )
            
            if company_context == "Custom":
                custom_company = st.text_input("Enter your organization context:", key="custom_company_input")
                company_context = custom_company
            
            tool_type = st.selectbox(
                "Tool Type",
                ["Assessment Framework", "Process/Workflow", "Template/Form", "Strategy Document", "Training Material", "Policy Document", "Measurement Tool", "Other"],
                key="tool_type_select"
            )
        
        with col_context2:
            detail_level = st.selectbox(
                "Detail Level",
                ["Comprehensive (Detailed)", "Standard (Moderate)", "Overview (High-level)"],
                key="detail_level_select"
            )
            
            target_users = st.multiselect(
                "Target Users",
                ["HR Team", "Managers/Supervisors", "Employees", "Senior Leadership", "External Coaches", "All Stakeholders"],
                default=["HR Team", "Managers/Supervisors"],
                key="target_users_multiselect"
            )
    
    with col2:
        st.subheader("🚀 Generate Content")
        
        if st.button("🎨 Generate Custom Performance Tool", type="primary", key="generate_custom_tool"):
            if custom_prompt.strip():
                enhanced_prompt = f"""
                Organization Context: {company_context}
                Tool Type: {tool_type}
                Target Users: {', '.join(target_users)}
                Detail Level: {detail_level}
                
                Performance Management Request: {custom_prompt}
                
                Create professional performance management content that:
                1. Is specific to the organization context provided
                2. Follows performance management best practices
                3. Is appropriate for the target users
                4. Matches the requested detail level
                5. Is immediately implementable and actionable
                6. Includes relevant frameworks, templates, or processes
                7. Considers employee engagement and development
                8. Promotes fair and objective performance evaluation
                
                If this is an assessment tool, make it measurable and reliable.
                If this is a process, ensure clear steps and accountability.
                If this is a strategy, include implementation guidelines and success metrics.
                If this is training material, make it engaging and practical.
                
                Focus on driving performance improvement and employee development.
                """
                
                with st.spinner("Creating your custom performance management tool..."):
                    content = generate_content(enhanced_prompt, "Custom Performance Tool")
                    if content:
                        st.session_state.generated_content['custom_performance'] = content
            else:
                st.error("Please enter your performance management request")
        
        # Additional options
        st.markdown("---")
        st.subheader("📋 Quick Actions")
        
        if st.button("🔄 Clear Form", key="clear_custom_form"):
            st.session_state['custom_prompt_perf'] = ''
            if 'custom_performance' in st.session_state.generated_content:
                del st.session_state.generated_content['custom_performance']
            st.rerun()
        
        if st.button("💡 Get Ideas", key="get_custom_ideas"):
            st.session_state['custom_prompt_perf'] = """Suggest 10 innovative performance management initiatives for a modern workplace:

- Continuous performance feedback systems instead of annual reviews
- Skills-based performance tracking and development
- AI-powered performance insights and recommendations
- Peer feedback and collaboration measurement tools
- Real-time goal tracking and adjustment frameworks
- Performance coaching and mentoring programs
- Cross-functional project performance evaluation
- Remote work performance management strategies
- Data-driven talent development programs
- Employee-driven career planning platforms

For each initiative, provide implementation approach, benefits, and success metrics."""
    
    # Display generated content
    if 'custom_performance' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Performance Management Tool")
        cleaned_content = clean_text(st.session_state.generated_content['custom_performance'])
        st.text_area("Custom Performance Tool Content", value=cleaned_content, height=400, key="custom_performance_output")
        create_download_button(cleaned_content, f"Custom_Performance_Tool_{datetime.now().strftime('%Y%m%d_%H%M')}", "📥 Download Performance Tool")

# Footer
st.markdown("---")
st.markdown("### 🚀 Ready for the next module?")
st.info("This is Module 4 of 9. Continue building your comprehensive HR toolkit with additional specialized modules.")

# Instructions
with st.expander("📖 How to Use This Performance Management Module"):
    st.markdown("""
    ## 🎯 **Standard Features (Tabs 1-5):**
    1. **📊 Performance Review Templates** - Comprehensive evaluation forms and review processes
    2. **🎯 Goal Setting Framework** - SMART goals and objective-setting systems
    3. **📈 Development Plans** - Individual development roadmaps and growth plans
    4. **💼 Career Progression Maps** - Clear advancement pathways and competency frameworks
    5. **🏆 Recognition Programs** - Employee recognition and reward system design
    
    ## 🎨 **Custom Performance Tools (Tab 6):**
    - **Best Practice Prompts** - Proven performance management templates
    - **Custom Requests** - Any performance management need or challenge
    - **Context-Aware** - Tailored to your organization type and culture
    - **Professional Output** - Ready-to-implement tools and frameworks
    
    **Tips:**
    - Use sample data buttons for quick testing and learning
    - Focus on measurable outcomes and clear expectations
    - Ensure fairness and objectivity in all performance processes
    - Integrate development planning with performance evaluation
    - Create regular feedback loops and check-in processes
    - Align individual goals with organizational objectives
    """)

# Navigation
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("← Module 3: Talent Acquisition", key="nav_prev_perf"):
        # Assuming pages/03_talent_acquisition.py exists
        # st.switch_page("pages/03_talent_acquisition.py")
        st.warning("Page navigation for Module 3 is not implemented in this snippet.")


with col_nav2:
    if st.button("🏠 Back to Main Menu", key="nav_home_perf"):
        st.switch_page("pages/00_home.py")


with col_nav3:
    if st.button("Module 5: Employee Relations →", key="nav_next_perf", disabled=True):
        st.info("Coming Soon!")