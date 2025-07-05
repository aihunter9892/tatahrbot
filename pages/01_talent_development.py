import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="HR Copilot - Talent Development",
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
    st.markdown("### 📚 Module 1: Talent Development")
    st.markdown("Build comprehensive talent management tools with AI assistance")
    
    if st.button("🏠 Back to Main Menu"):
        st.switch_page("hr_copilot_main.py")

# Main title
st.title("🎯 HR Copilot - Talent Development Module")
st.markdown("Generate professional HR documents and frameworks using AI")

# Tab layout for different features
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Individual Development Plans",
    "🏗️ Competency Frameworks", 
    "🗺️ Career Path Mapping",
    "👥 Coaching Guides",
    "⭐ HiPo Identification",
    "🎨 Custom HR Assistant"
])

def generate_ai_content(prompt, content_type):
    """Generate content using selected AI model"""
    model_choice = st.session_state.get('model_choice', available_models[0] if available_models else 'Gemini (Google)')
    if model_choice == "Gemini (Google)":
        if not GEMINI_API_KEY:
            st.error("Please add your Gemini API key to the .env file")
            return None
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            system_prompt = """You are an expert HR professional and consultant specializing in talent development, succession planning, and organizational development. Provide detailed, professional, and actionable HR content that follows industry best practices and compliance standards."""
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

# Tab 1: Individual Development Plans
with tab1:
    st.header("📋 Individual Development Plan (IDP) Builder")
    
    # Dummy data samples
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("👨‍💼 Sample 1: Senior Engineer", type="secondary"):
            st.session_state.update({
                'employee_name': 'Rajesh Kumar Sharma',
                'current_role': 'Senior Design Engineer',
                'department': 'Product Development - Passenger Vehicles',
                'manager_name': 'Priya Mehta',
                'career_goals': 'Transition to Engineering Manager role within 2 years, lead cross-functional teams in electric vehicle development, and contribute to Tata\'s sustainability goals',
                'current_strengths': 'Strong technical expertise in automotive design, proficient in CAD software, excellent problem-solving skills, good understanding of safety regulations',
                'development_areas': 'Leadership and team management, project management, stakeholder communication, electric vehicle technology',
                'timeline': '2 years',
                'job_level': 'Individual Contributor',
                'industry': 'Automotive Manufacturing',
                'specific_skills': 'Electric powertrain design, team leadership, agile project management, vendor management',
                'learning_preferences': ['Formal Training', 'Mentoring', 'Project Assignments', 'Online Courses']
            })
    
    with col_sample2:
        if st.button("👩‍💼 Sample 2: Quality Manager", type="secondary"):
            st.session_state.update({
                'employee_name': 'Anita Desai',
                'current_role': 'Assistant Manager - Quality Assurance',
                'department': 'Quality & Manufacturing',
                'manager_name': 'Vikram Singh',
                'career_goals': 'Advance to Quality Head role, implement Industry 4.0 quality systems, lead digital transformation in quality processes',
                'current_strengths': 'Deep knowledge of quality standards, Six Sigma Black Belt, strong analytical skills, experience with ISO certifications',
                'development_areas': 'Strategic planning, digital technology adoption, change management, cross-functional leadership',
                'timeline': '1 year',
                'job_level': 'Manager',
                'industry': 'Automotive Manufacturing',
                'specific_skills': 'Digital quality systems, data analytics, lean manufacturing, supplier quality management',
                'learning_preferences': ['Formal Training', 'Project Assignments', 'Conferences', 'Online Courses']
            })
    
    with col_sample3:
        if st.button("👨‍💼 Sample 3: Sales Executive", type="secondary"):
            st.session_state.update({
                'employee_name': 'Arjun Patel',
                'current_role': 'Regional Sales Executive',
                'department': 'Sales & Marketing - Commercial Vehicles',
                'manager_name': 'Kavita Reddy',
                'career_goals': 'Become Regional Sales Manager, expand market share in Western India, specialize in electric commercial vehicle sales',
                'current_strengths': 'Strong customer relationships, excellent communication skills, deep understanding of commercial vehicle market, consistent sales performance',
                'development_areas': 'Team management, strategic sales planning, electric vehicle technology knowledge, digital marketing',
                'timeline': '6 months',
                'job_level': 'Individual Contributor',
                'industry': 'Automotive Manufacturing',
                'specific_skills': 'Electric vehicle sales, team leadership, market analysis, digital sales tools',
                'learning_preferences': ['Mentoring', 'Job Rotation', 'Online Courses', 'Conferences']
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Employee Information")
        employee_name = st.text_input("Employee Name", value=st.session_state.get('employee_name', ''))
        current_role = st.text_input("Current Role/Position", value=st.session_state.get('current_role', ''))
        department = st.text_input("Department", value=st.session_state.get('department', ''))
        manager_name = st.text_input("Manager Name", value=st.session_state.get('manager_name', ''))
        
        st.subheader("Development Focus")
        career_goals = st.text_area("Career Goals & Aspirations", height=100, value=st.session_state.get('career_goals', ''))
        current_strengths = st.text_area("Current Strengths", height=80, value=st.session_state.get('current_strengths', ''))
        development_areas = st.text_area("Areas for Development", height=80, value=st.session_state.get('development_areas', ''))
        timeline = st.selectbox("Development Timeline", ["3 months", "6 months", "1 year", "2 years"], 
                               index=["3 months", "6 months", "1 year", "2 years"].index(st.session_state.get('timeline', '1 year')))
    
    with col2:
        st.subheader("Additional Context")
        job_level = st.selectbox("Job Level", ["Individual Contributor", "Team Lead", "Manager", "Senior Manager", "Director", "VP", "C-Level"],
                                index=["Individual Contributor", "Team Lead", "Manager", "Senior Manager", "Director", "VP", "C-Level"].index(st.session_state.get('job_level', 'Individual Contributor')))
        industry = st.text_input("Industry/Sector", value=st.session_state.get('industry', ''))
        specific_skills = st.text_area("Specific Skills to Develop", height=80, value=st.session_state.get('specific_skills', ''))
        learning_preferences = st.multiselect(
            "Learning Preferences",
            ["Formal Training", "Mentoring", "Job Rotation", "Project Assignments", "Online Courses", "Conferences", "Reading"],
            default=st.session_state.get('learning_preferences', [])
        )
        
        if st.button("🚀 Generate IDP", type="primary"):
            if employee_name and current_role:
                prompt = f"""
                Create a comprehensive Individual Development Plan (IDP) for:
                
                Employee: {employee_name}
                Current Role: {current_role}
                Department: {department}
                Manager: {manager_name}
                Job Level: {job_level}
                Industry: {industry}
                Timeline: {timeline}
                
                Career Goals: {career_goals}
                Current Strengths: {current_strengths}
                Development Areas: {development_areas}
                Specific Skills: {specific_skills}
                Learning Preferences: {', '.join(learning_preferences)}
                
                Please create a detailed IDP that includes:
                1. Executive Summary
                2. Current State Assessment
                3. Development Objectives (SMART goals)
                4. Action Plan with specific activities
                5. Resources and Support Needed
                6. Success Metrics
                7. Review Timeline
                
                Make it professional, actionable, and tailored to the specific role and industry.
                """
                
                with st.spinner("Generating your IDP..."):
                    content = generate_ai_content(prompt, "IDP")
                    if content:
                        st.session_state.generated_content['idp'] = content
            else:
                st.error("Please fill in at least Employee Name and Current Role")
    
    # Display generated IDP
    if 'idp' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Individual Development Plan")
        st.markdown(st.session_state.generated_content['idp'])
        
        # Download button
        st.download_button(
            label="📥 Download IDP",
            data=st.session_state.generated_content['idp'],
            file_name=f"IDP_{employee_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 2: Competency Frameworks
with tab2:
    st.header("🏗️ Competency Framework Builder")
    
    # Dummy data samples
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("🔧 Sample 1: Engineering", type="secondary", key="comp1"):
            st.session_state.update({
                'job_family_comp': 'Engineering - Product Development',
                'job_levels_comp': ['Entry Level', 'Mid Level', 'Senior Level', 'Lead Level', 'Manager Level'],
                'organization_type_comp': 'Corporate',
                'core_competencies_comp': 'Innovation and Creativity\nProblem Solving\nQuality Focus\nSafety Consciousness\nSustainability Mindset\nCollaboration\nCommunication\nContinuous Learning',
                'functional_competencies_comp': 'Automotive Design\nCAD/CAM Proficiency\nVehicle Testing\nRegulatory Compliance\nElectric Vehicle Technology\nManufacturing Processes\nProject Management\nVendor Management'
            })
    
    with col_sample2:
        if st.button("📊 Sample 2: Sales & Marketing", type="secondary", key="comp2"):
            st.session_state.update({
                'job_family_comp': 'Sales & Marketing',
                'job_levels_comp': ['Entry Level', 'Mid Level', 'Senior Level', 'Manager Level'],
                'organization_type_comp': 'Corporate',
                'core_competencies_comp': 'Customer Focus\nResult Orientation\nCommunication\nRelationship Building\nAdaptability\nTeamwork\nIntegrity\nCommercial Acumen',
                'functional_competencies_comp': 'Sales Process Management\nMarket Analysis\nCustomer Relationship Management\nDigital Marketing\nProduct Knowledge\nNegotiation Skills\nTerritory Management\nChannel Management'
            })
    
    with col_sample3:
        if st.button("⚙️ Sample 3: Manufacturing", type="secondary", key="comp3"):
            st.session_state.update({
                'job_family_comp': 'Manufacturing & Operations',
                'job_levels_comp': ['Entry Level', 'Mid Level', 'Senior Level', 'Lead Level', 'Manager Level', 'Director Level'],
                'organization_type_comp': 'Corporate',
                'core_competencies_comp': 'Operational Excellence\nSafety Leadership\nQuality Focus\nContinuous Improvement\nTeam Leadership\nProblem Solving\nDecision Making\nChange Management',
                'functional_competencies_comp': 'Production Planning\nLean Manufacturing\nSix Sigma\nEquipment Management\nSupply Chain\nCost Management\nProcess Optimization\nWorkforce Management'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Framework Details")
        job_family = st.text_input("Job Family (e.g., Engineering, Sales, Marketing)", value=st.session_state.get('job_family_comp', ''))
        job_levels = st.multiselect(
            "Job Levels to Include",
            ["Entry Level", "Mid Level", "Senior Level", "Lead Level", "Manager Level", "Director Level"],
            default=st.session_state.get('job_levels_comp', [])
        )
        organization_type = st.selectbox("Organization Type", ["Corporate", "Startup", "Non-profit", "Government", "Consulting"],
                                       index=["Corporate", "Startup", "Non-profit", "Government", "Consulting"].index(st.session_state.get('organization_type_comp', 'Corporate')))
        
    with col2:
        st.subheader("Competency Focus Areas")
        core_competencies = st.text_area("Core Competencies (one per line)", height=100, 
                                       placeholder="Leadership\nCommunication\nProblem Solving\nTeamwork",
                                       value=st.session_state.get('core_competencies_comp', ''))
        functional_competencies = st.text_area("Functional/Technical Competencies (one per line)", height=100,
                                             placeholder="Data Analysis\nProject Management\nCustomer Service",
                                             value=st.session_state.get('functional_competencies_comp', ''))
        
        if st.button("🏗️ Generate Competency Framework", type="primary"):
            if job_family and job_levels:
                prompt = f"""
                Create a comprehensive competency framework for:
                
                Job Family: {job_family}
                Job Levels: {', '.join(job_levels)}
                Organization Type: {organization_type}
                
                Core Competencies to include: {core_competencies}
                Functional Competencies to include: {functional_competencies}
                
                Please create a detailed competency framework that includes:
                1. Framework Overview
                2. Competency Definitions
                3. Proficiency Levels (1-5 scale) for each job level
                4. Behavioral Indicators for each competency
                5. Assessment Guidelines
                6. Development Recommendations
                
                Format it as a structured document with clear sections and make it practical for HR use.
                """
                
                with st.spinner("Building your competency framework..."):
                    content = generate_ai_content(prompt, "Competency Framework")
                    if content:
                        st.session_state.generated_content['competency'] = content
            else:
                st.error("Please fill in Job Family and select at least one Job Level")
    
    # Display generated framework
    if 'competency' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📊 Generated Competency Framework")
        st.markdown(st.session_state.generated_content['competency'])
        
        st.download_button(
            label="📥 Download Framework",
            data=st.session_state.generated_content['competency'],
            file_name=f"Competency_Framework_{job_family.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 3: Career Path Mapping
with tab3:
    st.header("🗺️ Career Path Mapping")
    
    # Dummy data samples
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("🚗 Sample 1: Design Engineer", type="secondary", key="career1"):
            st.session_state.update({
                'start_role_career': 'Senior Design Engineer',
                'start_level_career': 'Senior',
                'department_path_career': 'Product Development - Electric Vehicles',
                'career_direction_career': ['Management Track', 'Specialization'],
                'time_horizon_career': '3-5 years'
            })
    
    with col_sample2:
        if st.button("📈 Sample 2: Quality Manager", type="secondary", key="career2"):
            st.session_state.update({
                'start_role_career': 'Assistant Manager - Quality Assurance',
                'start_level_career': 'Manager',
                'department_path_career': 'Quality & Manufacturing',
                'career_direction_career': ['Management Track', 'Cross-functional Move'],
                'time_horizon_career': '3-5 years'
            })
    
    with col_sample3:
        if st.button("💼 Sample 3: Sales Professional", type="secondary", key="career3"):
            st.session_state.update({
                'start_role_career': 'Regional Sales Executive',
                'start_level_career': 'Mid',
                'department_path_career': 'Sales & Marketing - Commercial Vehicles',
                'career_direction_career': ['Management Track', 'Individual Contributor Track'],
                'time_horizon_career': '1-2 years'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Starting Position")
        start_role = st.text_input("Current Role", value=st.session_state.get('start_role_career', ''))
        start_level = st.selectbox("Current Level", ["Entry", "Mid", "Senior", "Lead", "Manager", "Director"],
                                 index=["Entry", "Mid", "Senior", "Lead", "Manager", "Director"].index(st.session_state.get('start_level_career', 'Mid')))
        department_path = st.text_input("Department/Function", value=st.session_state.get('department_path_career', ''))
        
    with col2:
        st.subheader("Career Preferences")
        career_direction = st.multiselect(
            "Career Direction Interests",
            ["Management Track", "Individual Contributor Track", "Cross-functional Move", "Leadership Development", "Specialization"],
            default=st.session_state.get('career_direction_career', [])
        )
        time_horizon = st.selectbox("Time Horizon", ["1-2 years", "3-5 years", "5-10 years", "Long-term (10+ years)"],
                                  index=["1-2 years", "3-5 years", "5-10 years", "Long-term (10+ years)"].index(st.session_state.get('time_horizon_career', '3-5 years')))
        
        if st.button("🗺️ Generate Career Paths", type="primary"):
            if start_role and career_direction:
                prompt = f"""
                Create comprehensive career path options for:
                
                Current Role: {start_role}
                Current Level: {start_level}
                Department: {department_path}
                Career Interests: {', '.join(career_direction)}
                Time Horizon: {time_horizon}
                
                Please create detailed career path mapping that includes:
                1. Multiple Career Path Options (3-4 different paths)
                2. Step-by-step progression for each path
                3. Required skills and competencies for each step
                4. Typical timeline for advancement
                5. Recommended development activities
                6. Potential challenges and how to overcome them
                7. Alternative lateral moves
                
                Make it visual and easy to follow, with clear milestones and requirements.
                """
                
                with st.spinner("Mapping your career paths..."):
                    content = generate_ai_content(prompt, "Career Path")
                    if content:
                        st.session_state.generated_content['career_path'] = content
            else:
                st.error("Please fill in Current Role and select Career Direction")
    
    # Display generated career paths
    if 'career_path' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("🛣️ Generated Career Path Map")
        st.markdown(st.session_state.generated_content['career_path'])
        
        st.download_button(
            label="📥 Download Career Path",
            data=st.session_state.generated_content['career_path'],
            file_name=f"Career_Path_{start_role.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 4: Coaching Guides
with tab4:
    st.header("👥 Coaching Guides & Templates")
    
    # Dummy data samples
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("👨‍💼 Sample 1: Leadership Coaching", type="secondary", key="coach1"):
            st.session_state.update({
                'coaching_type_coach': 'Leadership Coaching',
                'coachee_level_coach': 'Mid Level',
                'focus_area_coach': 'Developing leadership presence, improving cross-functional collaboration, preparing for management responsibilities in the transition to electric vehicles',
                'session_duration_coach': '60 minutes',
                'frequency_coach': 'Bi-weekly',
                'coaching_style_coach': 'Mixed Approach'
            })
    
    with col_sample2:
        if st.button("📈 Sample 2: Performance Coaching", type="secondary", key="coach2"):
            st.session_state.update({
                'coaching_type_coach': 'Performance Coaching',
                'coachee_level_coach': 'Senior Level',
                'focus_area_coach': 'Improving technical delivery quality, enhancing project management skills, developing better stakeholder communication in manufacturing operations',
                'session_duration_coach': '45 minutes',
                'frequency_coach': 'Weekly',
                'coaching_style_coach': 'Directive'
            })
    
    with col_sample3:
        if st.button("🎯 Sample 3: Career Coaching", type="secondary", key="coach3"):
            st.session_state.update({
                'coaching_type_coach': 'Career Coaching',
                'coachee_level_coach': 'Manager',
                'focus_area_coach': 'Career transition from technical role to business leadership, developing commercial acumen, building strategic thinking capabilities',
                'session_duration_coach': '60 minutes',
                'frequency_coach': 'Monthly',
                'coaching_style_coach': 'Non-directive'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Coaching Context")
        coaching_type = st.selectbox(
            "Type of Coaching",
            ["Performance Coaching", "Development Coaching", "Career Coaching", "Skills Coaching", "Leadership Coaching"],
            index=["Performance Coaching", "Development Coaching", "Career Coaching", "Skills Coaching", "Leadership Coaching"].index(st.session_state.get('coaching_type_coach', 'Performance Coaching'))
        )
        coachee_level = st.selectbox("Coachee Level", ["Entry Level", "Mid Level", "Senior Level", "Manager", "Director"],
                                   index=["Entry Level", "Mid Level", "Senior Level", "Manager", "Director"].index(st.session_state.get('coachee_level_coach', 'Mid Level')))
        focus_area = st.text_area("Specific Focus Areas", height=100, value=st.session_state.get('focus_area_coach', ''))
        
    with col2:
        st.subheader("Coaching Preferences")
        session_duration = st.selectbox("Session Duration", ["30 minutes", "45 minutes", "60 minutes", "90 minutes"],
                                      index=["30 minutes", "45 minutes", "60 minutes", "90 minutes"].index(st.session_state.get('session_duration_coach', '60 minutes')))
        frequency = st.selectbox("Frequency", ["Weekly", "Bi-weekly", "Monthly", "As needed"],
                               index=["Weekly", "Bi-weekly", "Monthly", "As needed"].index(st.session_state.get('frequency_coach', 'Bi-weekly')))
        coaching_style = st.selectbox("Coaching Style", ["Directive", "Non-directive", "Mixed Approach"],
                                    index=["Directive", "Non-directive", "Mixed Approach"].index(st.session_state.get('coaching_style_coach', 'Mixed Approach')))
        
        if st.button("👥 Generate Coaching Guide", type="primary"):
            if coaching_type and focus_area:
                prompt = f"""
                Create a comprehensive coaching guide for:
                
                Coaching Type: {coaching_type}
                Coachee Level: {coachee_level}
                Focus Areas: {focus_area}
                Session Duration: {session_duration}
                Frequency: {frequency}
                Coaching Style: {coaching_style}
                
                Please create a detailed coaching guide that includes:
                1. Coaching Framework and Approach
                2. Session Structure Template
                3. Key Questions to Ask
                4. Goal Setting Templates
                5. Progress Tracking Methods
                6. Common Challenges and Solutions
                7. Resource Recommendations
                8. Sample Coaching Conversation Scripts
                9. Action Planning Templates
                
                Make it practical and immediately usable by managers and HR professionals.
                """
                
                with st.spinner("Creating your coaching guide..."):
                    content = generate_ai_content(prompt, "Coaching Guide")
                    if content:
                        st.session_state.generated_content['coaching'] = content
            else:
                st.error("Please select Coaching Type and describe Focus Areas")
    
    # Display generated coaching guide
    if 'coaching' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📚 Generated Coaching Guide")
        st.markdown(st.session_state.generated_content['coaching'])
        
        st.download_button(
            label="📥 Download Coaching Guide",
            data=st.session_state.generated_content['coaching'],
            file_name=f"Coaching_Guide_{coaching_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 5: HiPo Identification
with tab5:
    st.header("⭐ High Potential (HiPo) Identification")
    
    # Dummy data samples
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("🏭 Sample 1: Manufacturing Focus", type="secondary", key="hipo1"):
            st.session_state.update({
                'org_size_hipo': '5000+',
                'industry_hipo': 'Automotive Manufacturing',
                'leadership_levels_hipo': ['Individual Contributors', 'Team Leads', 'Managers'],
                'key_attributes_hipo': 'Leadership Potential\nLearning Agility\nPerformance Excellence\nInnovation Mindset\nCultural Alignment with Tata Values\nCross-functional Collaboration\nChange Adaptability\nOperational Excellence',
                'assessment_method_hipo': ['Performance Reviews', '360 Feedback', 'Assessment Centers']
            })
    
    with col_sample2:
        if st.button("💼 Sample 2: Corporate Leadership", type="secondary", key="hipo2"):
            st.session_state.update({
                'org_size_hipo': '5000+',
                'industry_hipo': 'Automotive Manufacturing',
                'leadership_levels_hipo': ['Managers', 'Senior Managers', 'Directors'],
                'key_attributes_hipo': 'Strategic Thinking\nLeadership Presence\nBusiness Acumen\nGlobal Mindset\nDigital Leadership\nSustainability Focus\nStakeholder Management\nTransformation Leadership',
                'assessment_method_hipo': ['360 Feedback', 'Assessment Centers', 'Behavioral Interviews', 'Psychometric Tests']
            })
    
    with col_sample3:
        if st.button("🚀 Sample 3: Technical Innovation", type="secondary", key="hipo3"):
            st.session_state.update({
                'org_size_hipo': '5000+',
                'industry_hipo': 'Automotive Manufacturing',
                'leadership_levels_hipo': ['Individual Contributors', 'Team Leads', 'Managers', 'Senior Managers'],
                'key_attributes_hipo': 'Technical Excellence\nInnovation Capability\nProblem Solving\nLearning Agility\nCollaboration\nCustomer Focus\nQuality Mindset\nFuture Technology Adoption',
                'assessment_method_hipo': ['Performance Reviews', 'Behavioral Interviews', 'Assessment Centers']
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Organization Context")
        org_size = st.selectbox("Organization Size", ["<100", "100-500", "500-1000", "1000-5000", "5000+"],
                               index=["<100", "100-500", "500-1000", "1000-5000", "5000+"].index(st.session_state.get('org_size_hipo', '5000+')))
        industry_hipo = st.text_input("Industry", value=st.session_state.get('industry_hipo', ''))
        leadership_levels = st.multiselect(
            "Leadership Levels to Assess",
            ["Individual Contributors", "Team Leads", "Managers", "Senior Managers", "Directors"],
            default=st.session_state.get('leadership_levels_hipo', [])
        )
        
    with col2:
        st.subheader("HiPo Criteria Focus")
        key_attributes = st.text_area("Key Attributes to Assess", height=100,
                                    placeholder="Leadership potential\nLearning agility\nPerformance track record\nCultural fit",
                                    value=st.session_state.get('key_attributes_hipo', ''))
        assessment_method = st.multiselect(
            "Assessment Methods",
            ["Performance Reviews", "360 Feedback", "Assessment Centers", "Behavioral Interviews", "Psychometric Tests"],
            default=st.session_state.get('assessment_method_hipo', [])
        )
        
        if st.button("⭐ Generate HiPo Framework", type="primary"):
            if leadership_levels and key_attributes:
                prompt = f"""
                Create a comprehensive High Potential (HiPo) identification framework for:
                
                Organization Size: {org_size}
                Industry: {industry_hipo}
                Leadership Levels: {', '.join(leadership_levels)}
                Key Attributes: {key_attributes}
                Assessment Methods: {', '.join(assessment_method)}
                
                Please create a detailed HiPo identification framework that includes:
                1. HiPo Definition and Criteria
                2. Assessment Framework with scoring rubrics
                3. Identification Process and Timeline
                4. Talent Review Templates
                5. Development Planning for HiPos
                6. Succession Planning Integration
                7. Communication Guidelines
                8. Tracking and Monitoring Methods
                9. Sample Forms and Checklists
                
                Make it comprehensive yet practical for immediate implementation.
                """
                
                with st.spinner("Building your HiPo identification framework..."):
                    content = generate_ai_content(prompt, "HiPo Framework")
                    if content:
                        st.session_state.generated_content['hipo'] = content
            else:
                st.error("Please select Leadership Levels and describe Key Attributes")
    
    # Display generated HiPo framework
    if 'hipo' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("🌟 Generated HiPo Identification Framework")
        st.markdown(st.session_state.generated_content['hipo'])
        
        st.download_button(
            label="📥 Download HiPo Framework",
            data=st.session_state.generated_content['hipo'],
            file_name=f"HiPo_Framework_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 6: Custom HR Assistant
with tab6:
    st.header("🎨 Custom HR Assistant")
    st.markdown("Create any HR document or get answers to HR questions with custom prompts")
    
    # Sample prompts for Tata Motors
    st.subheader("🎯 Quick Start with Tata Motors Sample Prompts")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("📄 Sample: Policy Document", type="secondary", key="custom1"):
            st.session_state['custom_prompt'] = """Create a comprehensive Remote Work Policy for Tata Motors that includes:
- Eligibility criteria for remote work
- Equipment and technology requirements
- Communication guidelines and expectations
- Performance measurement for remote employees
- Security and confidentiality protocols
- Work-life balance considerations
- Review and approval process

Make it specific to automotive industry requirements and Tata Motors' culture."""
    
    with col_sample2:
        if st.button("📊 Sample: Survey Questions", type="secondary", key="custom2"):
            st.session_state['custom_prompt'] = """Design an Employee Engagement Survey for Tata Motors manufacturing employees that covers:
- Job satisfaction and work environment
- Leadership effectiveness
- Career development opportunities
- Work-life balance
- Safety culture and practices
- Innovation and continuous improvement
- Compensation and benefits satisfaction
- Tata values alignment

Include 25-30 questions with a mix of rating scales and open-ended questions."""
    
    with col_sample3:
        if st.button("🎓 Sample: Training Program", type="secondary", key="custom3"):
            st.session_state['custom_prompt'] = """Create a comprehensive Electric Vehicle Technology Training Program for Tata Motors engineers including:
- Learning objectives and outcomes
- Module-wise curriculum (8-10 modules)
- Training methodology (classroom, hands-on, virtual)
- Duration and schedule
- Assessment criteria
- Prerequisites and target audience
- Resource requirements
- Post-training certification process

Focus on practical application in automotive manufacturing."""
    
    st.markdown("---")
    
    # Custom prompt input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💭 Your Custom HR Request")
        custom_prompt = st.text_area(
            "Enter your HR question or document request:",
            height=200,
            value=st.session_state.get('custom_prompt', ''),
            placeholder="""Examples:
• Create an onboarding checklist for new software engineers
• Draft a performance improvement plan template
• Design interview questions for a sales manager role
• Write a company culture assessment framework
• Create a wellness program proposal
• Draft a diversity and inclusion policy
• Design a 360-feedback process
• Create a succession planning template for critical roles"""
        )
        
        # Context options
        st.subheader("🎯 Context & Customization")
        col_context1, col_context2 = st.columns(2)
        
        with col_context1:
            company_context = st.selectbox(
                "Company Context",
                ["Tata Motors", "Automotive Industry", "Manufacturing Company", "Technology Company", "Generic Corporate", "Custom"],
                index=0
            )
            
            if company_context == "Custom":
                custom_company = st.text_input("Enter your company/industry context:")
                company_context = custom_company
            
            document_type = st.selectbox(
                "Document Type",
                ["Policy Document", "Process/Procedure", "Template/Form", "Training Material", "Assessment Tool", "Communication", "Strategy Document", "Other"]
            )
        
        with col_context2:
            urgency = st.selectbox(
                "Detail Level",
                ["High Detail (Comprehensive)", "Medium Detail (Standard)", "Low Detail (Brief Overview)"]
            )
            
            target_audience = st.multiselect(
                "Target Audience",
                ["All Employees", "Managers", "HR Team", "Senior Leadership", "New Hires", "Specific Department", "External Stakeholders"],
                default=["All Employees"]
            )
    
    with col2:
        st.subheader("🚀 Generate Content")
        
        if st.button("🎨 Generate Custom HR Content", type="primary", key="generate_custom"):
            if custom_prompt.strip():
                # Build enhanced prompt with context
                enhanced_prompt = f"""
                Company Context: {company_context}
                Document Type: {document_type}
                Target Audience: {', '.join(target_audience)}
                Detail Level: {urgency}
                
                HR Request: {custom_prompt}
                
                Please create professional HR content that:
                1. Is specific to the company context provided
                2. Follows HR best practices and compliance requirements
                3. Is appropriate for the target audience
                4. Matches the requested detail level
                5. Is immediately usable and actionable
                6. Includes relevant sections, templates, or frameworks as needed
                
                If this is a policy or procedure, include implementation guidelines.
                If this is a template, make it customizable and practical.
                If this is training material, include learning objectives and activities.
                """
                
                with st.spinner("Creating your custom HR content..."):
                    content = generate_ai_content(enhanced_prompt, "Custom HR Content")
                    if content:
                        st.session_state.generated_content['custom'] = content
            else:
                st.error("Please enter your HR request in the text area")
        
        # Additional options
        st.markdown("---")
        st.subheader("📋 Quick Actions")
        
        if st.button("🔄 Clear Form", key="clear_custom"):
            st.session_state['custom_prompt'] = ''
            if 'custom' in st.session_state.generated_content:
                del st.session_state.generated_content['custom']
            st.rerun()
        
        if st.button("💡 Get Ideas", key="ideas_custom"):
            st.session_state['custom_prompt'] = """Suggest 10 innovative HR initiatives that Tata Motors could implement to:
- Enhance employee engagement in manufacturing environments
- Attract and retain top talent in the automotive industry
- Build a future-ready workforce for electric vehicles
- Strengthen safety culture across all operations
- Promote diversity and inclusion
- Support work-life balance for shift workers

For each initiative, provide a brief description and expected benefits."""
    
    # Display generated content
    if 'custom' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated HR Content")
        
        # Content display with formatting
        content = st.session_state.generated_content['custom']
        st.markdown(content)
        
        # Download and action buttons
        col_download1, col_download2, col_download3 = st.columns(3)
        
        with col_download1:
            st.download_button(
                label="📥 Download as Text",
                data=content,
                file_name=f"Custom_HR_Content_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
        
        with col_download2:
            if st.button("📋 Copy to Clipboard", key="copy_custom"):
                st.info("Content copied! (Paste using Ctrl+V)")
        
        with col_download3:
            if st.button("✏️ Refine Content", key="refine_custom"):
                st.session_state['custom_prompt'] = f"Please refine and improve the following HR content:\n\n{content}\n\nMake it more detailed, professional, and actionable."

# Footer
st.markdown("---")
st.markdown("### 🚀 Ready for the next module?")
st.info("This is Module 1 of 9. Each module focuses on a specific HR domain to help you build comprehensive HR tools and documents.")

# Instructions
with st.expander("📖 How to Use This App"):
    st.markdown("""
    ## 🎯 **Standard Modules (Tabs 1-5):**
    1. **Enter your Gemini API Key** by creating a `.env` file with `GEMINI_API_KEY=your_key`
    2. **Choose a tab** for the type of document you want to create
    3. **Use sample data** by clicking the sample buttons for quick testing
    4. **Fill in the required information** in the form fields
    5. **Click the Generate button** to create your AI-powered HR document
    6. **Review and download** the generated content
    
    ## 🎨 **Custom HR Assistant (Tab 6):**
    1. **Use sample prompts** or write your own custom HR request
    2. **Set context** (company, document type, audience, detail level)
    3. **Generate content** with the custom prompt
    4. **Download, copy, or refine** the generated content
    
    **Tips:**
    - Be specific in your inputs for better AI-generated content
    - Use the sample data to understand the expected format
    - The Custom HR Assistant can handle any HR-related request
    - All generated content can be downloaded as text files
    - Use the content as a starting point and customize as needed
    """)

# Navigation
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("🏠 Main Menu", key="nav_home_talent"):
        st.switch_page("hr_copilot_main.py")

with col_nav2:
    if st.button("Module 2: Succession Planning →", key="nav_next_talent"):
        st.switch_page("pages/02_succession_planning.py")

with col_nav3:
    st.markdown("")  # Empty space for alignment