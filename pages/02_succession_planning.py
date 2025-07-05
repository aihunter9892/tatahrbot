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
    page_title="HR Copilot - Succession Planning",
    page_icon="👑",
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
    st.markdown("### 👑 Module 2: Succession Planning")
    st.markdown("Build comprehensive succession strategies and leadership pipelines")
    
    if st.button("🏠 Back to Main Menu"):
        st.switch_page("hr_copilot_main.py")

# Main title
st.title("👑 HR Copilot - Succession Planning Module")
st.markdown("Create robust succession plans and develop future leaders with AI assistance")

# Tab layout for different features
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Succession Plan Formats",
    "✅ Readiness Checklists", 
    "🎯 Development Action Plans",
    "📢 Communication Templates",
    "📊 Policy & Governance",
    "🎨 Custom Succession Assistant"
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
            system_prompt = """You are an expert HR professional and consultant specializing in succession planning, leadership development, and organizational continuity. Provide detailed, professional, and actionable succession planning content that follows industry best practices and compliance standards."""
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

# Tab 1: Succession Plan Formats
with tab1:
    st.header("📋 Succession Plan Formats")
    
    # Dummy data samples
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("🏭 Sample 1: Plant Manager", type="secondary", key="succ1"):
            st.session_state.update({
                'critical_role': 'Plant Manager - Pune Manufacturing Facility',
                'current_incumbent': 'Rajesh Patel',
                'department_succ': 'Manufacturing Operations',
                'business_impact': 'High - Direct impact on production targets, safety, quality, and 2000+ employee management',
                'succession_urgency': 'Medium (2-3 years)',
                'internal_candidates': 'Suresh Kumar (Deputy Plant Manager), Meera Shah (Production Head), Vikram Singh (Quality Head)',
                'external_requirement': 'Yes - Backup plan for specialized automotive manufacturing expertise',
                'key_competencies': 'Operational Excellence, Safety Leadership, Team Management, Cost Control, Quality Assurance, Regulatory Compliance',
                'development_timeline': '18-24 months'
            })
    
    with col_sample2:
        if st.button("💼 Sample 2: R&D Director", type="secondary", key="succ2"):
            st.session_state.update({
                'critical_role': 'Director - Electric Vehicle R&D',
                'current_incumbent': 'Dr. Priya Sharma',
                'department_succ': 'Research & Development',
                'business_impact': 'Critical - Leads EV innovation strategy, patent development, and future technology roadmap',
                'succession_urgency': 'High (1-2 years)',
                'internal_candidates': 'Amit Verma (Senior Manager EV Tech), Sanjana Gupta (Innovation Lead), Rohan Desai (Battery Technology Head)',
                'external_requirement': 'Yes - May need external expertise in advanced battery technology',
                'key_competencies': 'Technical Leadership, Innovation Management, Strategic Planning, Cross-functional Collaboration, Patent Development',
                'development_timeline': '12-18 months'
            })
    
    with col_sample3:
        if st.button("📈 Sample 3: Sales Head", type="secondary", key="succ3"):
            st.session_state.update({
                'critical_role': 'Head of Commercial Vehicle Sales - India',
                'current_incumbent': 'Kavita Reddy',
                'department_succ': 'Sales & Marketing',
                'business_impact': 'High - Responsible for 60% of Tata Motors revenue from commercial vehicles',
                'succession_urgency': 'Low (3-5 years)',
                'internal_candidates': 'Arjun Patel (Regional Sales Manager West), Neha Agarwal (Regional Sales Manager North), Ravi Kumar (Key Account Manager)',
                'external_requirement': 'Optional - Strong internal pipeline available',
                'key_competencies': 'Sales Leadership, Market Strategy, Customer Relationship Management, Team Building, P&L Management',
                'development_timeline': '24-36 months'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Critical Role Information")
        critical_role = st.text_input("Critical Role/Position", value=st.session_state.get('critical_role', ''))
        current_incumbent = st.text_input("Current Incumbent", value=st.session_state.get('current_incumbent', ''))
        department_succ = st.text_input("Department/Division", value=st.session_state.get('department_succ', ''))
        business_impact = st.text_area("Business Impact & Criticality", height=80, value=st.session_state.get('business_impact', ''))
        succession_urgency_options = ["Immediate (0-6 months)", "Short-term (6-12 months)", "Medium (1-3 years)", "Long-term (3+ years)"]
        current_urgency = st.session_state.get('succession_urgency', 'Medium (1-3 years)')
        
        # Handle cases where stored value doesn't match current options
        try:
            urgency_index = succession_urgency_options.index(current_urgency)
        except ValueError:
            # If stored value doesn't match, default to Medium
            urgency_index = 2
            
        succession_urgency = st.selectbox("Succession Urgency", 
                                        succession_urgency_options,
                                        index=urgency_index)
    
    with col2:
        st.subheader("Succession Planning Details")
        internal_candidates = st.text_area("Internal Candidates (with current roles)", height=100, 
                                         value=st.session_state.get('internal_candidates', ''))
        external_requirement_options = ["Yes - External candidates needed", "No - Internal pipeline sufficient", "Optional - Backup plan"]
        current_external = st.session_state.get('external_requirement', 'Yes - External candidates needed')
        
        try:
            external_index = external_requirement_options.index(current_external)
        except ValueError:
            external_index = 0
            
        external_requirement = st.selectbox("External Hiring Requirement", 
                                          external_requirement_options,
                                          index=external_index)
        
        key_competencies = st.text_area("Key Competencies Required", height=80, value=st.session_state.get('key_competencies', ''))
        
        development_timeline_options = ["6-12 months", "12-18 months", "18-24 months", "24-36 months", "36+ months"]
        current_timeline = st.session_state.get('development_timeline', '12-18 months')
        
        try:
            timeline_index = development_timeline_options.index(current_timeline)
        except ValueError:
            timeline_index = 1
            
        development_timeline = st.selectbox("Development Timeline",
                                          development_timeline_options,
                                          index=timeline_index)
        
        if st.button("📋 Generate Succession Plan", type="primary"):
            if critical_role and current_incumbent:
                prompt = f"""
                Create a comprehensive succession plan format for:
                
                Critical Role: {critical_role}
                Current Incumbent: {current_incumbent}
                Department: {department_succ}
                Business Impact: {business_impact}
                Succession Urgency: {succession_urgency}
                Internal Candidates: {internal_candidates}
                External Requirement: {external_requirement}
                Key Competencies: {key_competencies}
                Development Timeline: {development_timeline}
                
                Please create a detailed succession plan that includes:
                1. Executive Summary
                2. Role Profile and Criticality Assessment
                3. Current State Analysis
                4. Successor Identification and Assessment
                5. Development Plans for Each Candidate
                6. Risk Mitigation Strategies
                7. Timeline and Milestones
                8. Success Metrics and KPIs
                9. Governance and Review Process
                10. Emergency Succession Protocol
                
                Make it comprehensive, actionable, and suitable for senior leadership review.
                """
                
                with st.spinner("Creating your succession plan..."):
                    content = generate_ai_content(prompt, "Succession Plan")
                    if content:
                        st.session_state.generated_content['succession_plan'] = content
            else:
                st.error("Please fill in Critical Role and Current Incumbent")
    
    # Display generated succession plan
    if 'succession_plan' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Succession Plan")
        st.markdown(st.session_state.generated_content['succession_plan'])
        
        st.download_button(
            label="📥 Download Succession Plan",
            data=st.session_state.generated_content['succession_plan'],
            file_name=f"Succession_Plan_{critical_role.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 2: Readiness Checklists
with tab2:
    st.header("✅ Successor Readiness Checklists")
    
    # Dummy data samples
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("👨‍💼 Sample 1: Technical Leader", type="secondary", key="ready1"):
            st.session_state.update({
                'successor_name': 'Amit Verma',
                'current_position': 'Senior Manager - EV Technology',
                'target_role': 'Director - Electric Vehicle R&D',
                'readiness_timeline': '12-18 months',
                'technical_skills': 'Electric powertrain design, Battery technology, Automotive electronics, Software integration, Regulatory standards',
                'leadership_skills': 'Team management, Cross-functional collaboration, Strategic planning, Innovation leadership, Vendor management',
                'experience_gaps': 'P&L responsibility, Board-level presentations, Patent strategy, Global team management, M&A experience',
                'development_priorities': 'Business acumen, Executive presence, Strategic thinking, Financial management, Global perspective'
            })
    
    with col_sample2:
        if st.button("👩‍💼 Sample 2: Operations Leader", type="secondary", key="ready2"):
            st.session_state.update({
                'successor_name': 'Meera Shah',
                'current_position': 'Production Head - Passenger Vehicles',
                'target_role': 'Plant Manager - Pune Manufacturing',
                'readiness_timeline': '18-24 months',
                'technical_skills': 'Manufacturing operations, Quality systems, Lean manufacturing, Safety protocols, Automation systems',
                'leadership_skills': 'Team leadership, Crisis management, Change management, Communication, Performance management',
                'experience_gaps': 'Union negotiations, Capital investment decisions, Strategic planning, Multi-site management, Digital transformation',
                'development_priorities': 'Strategic leadership, Financial acumen, Stakeholder management, Digital skills, Change leadership'
            })
    
    with col_sample3:
        if st.button("💼 Sample 3: Sales Leader", type="secondary", key="ready3"):
            st.session_state.update({
                'successor_name': 'Arjun Patel',
                'current_position': 'Regional Sales Manager - Western India',
                'target_role': 'Head of Commercial Vehicle Sales',
                'readiness_timeline': '24-36 months',
                'technical_skills': 'Sales process management, Market analysis, Customer relationship management, Product knowledge, Digital sales tools',
                'leadership_skills': 'Team building, Coaching, Conflict resolution, Negotiation, Performance management',
                'experience_gaps': 'National market strategy, Key account management, International sales, Channel partnerships, P&L ownership',
                'development_priorities': 'Strategic thinking, Business development, Market expansion, Leadership presence, Financial management'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Successor Information")
        successor_name = st.text_input("Successor Name", value=st.session_state.get('successor_name', ''))
        current_position = st.text_input("Current Position", value=st.session_state.get('current_position', ''))
        target_role = st.text_input("Target Role", value=st.session_state.get('target_role', ''))
        readiness_timeline_options = ["6-12 months", "12-18 months", "18-24 months", "24-36 months", "36+ months"]
        current_readiness = st.session_state.get('readiness_timeline', '12-18 months')
        
        try:
            readiness_index = readiness_timeline_options.index(current_readiness)
        except ValueError:
            readiness_index = 1
            
        readiness_timeline = st.selectbox("Readiness Timeline",
                                        readiness_timeline_options,
                                        index=readiness_index)
    
    with col2:
        st.subheader("Current Capabilities")
        technical_skills = st.text_area("Technical Skills & Knowledge", height=80, value=st.session_state.get('technical_skills', ''))
        leadership_skills = st.text_area("Leadership & Management Skills", height=80, value=st.session_state.get('leadership_skills', ''))
        
    # Development needs
    st.subheader("Development Requirements")
    col3, col4 = st.columns([1, 1])
    
    with col3:
        experience_gaps = st.text_area("Experience Gaps", height=80, value=st.session_state.get('experience_gaps', ''))
        
    with col4:
        development_priorities = st.text_area("Development Priorities", height=80, value=st.session_state.get('development_priorities', ''))
        
        if st.button("✅ Generate Readiness Checklist", type="primary"):
            if successor_name and target_role:
                prompt = f"""
                Create a comprehensive successor readiness checklist for:
                
                Successor: {successor_name}
                Current Position: {current_position}
                Target Role: {target_role}
                Readiness Timeline: {readiness_timeline}
                
                Current Capabilities:
                - Technical Skills: {technical_skills}
                - Leadership Skills: {leadership_skills}
                
                Development Needs:
                - Experience Gaps: {experience_gaps}
                - Development Priorities: {development_priorities}
                
                Please create a detailed readiness checklist that includes:
                1. Current State Assessment Matrix
                2. Target Role Requirements Mapping
                3. Skills Gap Analysis
                4. Readiness Criteria and Benchmarks
                5. Assessment Methods and Tools
                6. Development Recommendations
                7. Progress Tracking Framework
                8. Readiness Milestones and Timeline
                9. Risk Assessment and Mitigation
                10. Final Readiness Certification Criteria
                
                Make it practical for use by HR and line managers to track successor development.
                """
                
                with st.spinner("Creating your readiness checklist..."):
                    content = generate_ai_content(prompt, "Readiness Checklist")
                    if content:
                        st.session_state.generated_content['readiness_checklist'] = content
            else:
                st.error("Please fill in Successor Name and Target Role")
    
    # Display generated checklist
    if 'readiness_checklist' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📋 Generated Readiness Checklist")
        st.markdown(st.session_state.generated_content['readiness_checklist'])
        
        st.download_button(
            label="📥 Download Readiness Checklist",
            data=st.session_state.generated_content['readiness_checklist'],
            file_name=f"Readiness_Checklist_{successor_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 3: Development Action Plans
with tab3:
    st.header("🎯 Development Action Plans")
    
    # Dummy data samples
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("🎓 Sample 1: Leadership Development", type="secondary", key="dev1"):
            st.session_state.update({
                'successor_name_dev': 'Sanjana Gupta',
                'development_goal': 'Prepare for Innovation Lead to Director transition',
                'current_level_dev': 'Senior Manager',
                'target_level': 'Director Level',
                'development_areas': 'Strategic thinking, Executive communication, Financial acumen, Global perspective, Innovation strategy',
                'learning_style': 'Experiential learning, Mentoring, Project-based development',
                'timeline_dev': '18 months',
                'budget_constraints': 'Medium budget - Up to ₹5 lakhs for development',
                'success_metrics': 'Successfully lead 2 major innovation projects, Complete executive education, Achieve 360 feedback score >4.0, Build global partnerships'
            })
    
    with col_sample2:
        if st.button("⚙️ Sample 2: Technical Development", type="secondary", key="dev2"):
            st.session_state.update({
                'successor_name_dev': 'Rohan Desai',
                'development_goal': 'Build comprehensive EV technology leadership capabilities',
                'current_level_dev': 'Manager',
                'target_level': 'Senior Manager',
                'development_areas': 'Advanced battery technology, Electric powertrain systems, Regulatory compliance, Team leadership, Cross-functional collaboration',
                'learning_style': 'Technical training, Certification programs, Hands-on projects',
                'timeline_dev': '12 months',
                'budget_constraints': 'High budget - Up to ₹8 lakhs for specialized training',
                'success_metrics': 'Obtain EV certification, Lead battery technology project, Manage 15+ team members, Establish vendor partnerships'
            })
    
    with col_sample3:
        if st.button("💼 Sample 3: Business Development", type="secondary", key="dev3"):
            st.session_state.update({
                'successor_name_dev': 'Neha Agarwal',
                'development_goal': 'Transition from regional to national sales leadership',
                'current_level_dev': 'Regional Manager',
                'target_level': 'National Head',
                'development_areas': 'Market strategy, P&L management, Channel development, Digital transformation, Leadership presence',
                'learning_style': 'Business school programs, Executive coaching, Job rotation',
                'timeline_dev': '24 months',
                'budget_constraints': 'Medium budget - Up to ₹6 lakhs for development',
                'success_metrics': 'Complete MBA/Executive program, Manage multi-regional P&L, Launch 3 new market segments, Build digital sales capabilities'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Development Context")
        successor_name_dev = st.text_input("Successor Name", value=st.session_state.get('successor_name_dev', ''), key="succ_name_dev")
        development_goal = st.text_area("Development Goal", height=80, value=st.session_state.get('development_goal', ''))
        current_level_dev = st.text_input("Current Level/Role", value=st.session_state.get('current_level_dev', ''))
        target_level = st.text_input("Target Level/Role", value=st.session_state.get('target_level', ''))
        development_areas = st.text_area("Key Development Areas", height=100, value=st.session_state.get('development_areas', ''))
    
    with col2:
        st.subheader("Development Parameters")
        learning_style = st.text_area("Preferred Learning Style", height=80, value=st.session_state.get('learning_style', ''))
        timeline_dev_options = ["6 months", "12 months", "18 months", "24 months", "36 months"]
        current_timeline_dev = st.session_state.get('timeline_dev', '18 months')
        
        try:
            timeline_dev_index = timeline_dev_options.index(current_timeline_dev)
        except ValueError:
            timeline_dev_index = 2
            
        timeline_dev = st.selectbox("Development Timeline",
                                  timeline_dev_options,
                                  index=timeline_dev_index)
        budget_constraints = st.text_input("Budget Constraints", value=st.session_state.get('budget_constraints', ''))
        success_metrics = st.text_area("Success Metrics", height=80, value=st.session_state.get('success_metrics', ''))
        
        if st.button("🎯 Generate Development Plan", type="primary"):
            if successor_name_dev and development_goal:
                prompt = f"""
                Create a comprehensive development action plan for:
                
                Successor: {successor_name_dev}
                Development Goal: {development_goal}
                Current Level: {current_level_dev}
                Target Level: {target_level}
                Development Areas: {development_areas}
                Learning Style: {learning_style}
                Timeline: {timeline_dev}
                Budget: {budget_constraints}
                Success Metrics: {success_metrics}
                
                Please create a detailed development action plan that includes:
                1. Development Objectives and Goals
                2. Learning and Development Strategy
                3. Specific Development Activities and Programs
                4. Timeline and Milestones
                5. Resource Requirements and Budget Allocation
                6. Mentoring and Coaching Plan
                7. Stretch Assignments and Projects
                8. Progress Monitoring and Evaluation
                9. Success Metrics and KPIs
                10. Risk Mitigation and Alternative Approaches
                11. Support System and Stakeholders
                12. Career Progression Pathway
                
                Make it actionable with specific timelines, resources, and measurable outcomes.
                """
                
                with st.spinner("Creating your development action plan..."):
                    content = generate_ai_content(prompt, "Development Action Plan")
                    if content:
                        st.session_state.generated_content['development_plan'] = content
            else:
                st.error("Please fill in Successor Name and Development Goal")
    
    # Display generated development plan
    if 'development_plan' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📈 Generated Development Action Plan")
        st.markdown(st.session_state.generated_content['development_plan'])
        
        st.download_button(
            label="📥 Download Development Plan",
            data=st.session_state.generated_content['development_plan'],
            file_name=f"Development_Plan_{successor_name_dev.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 4: Communication Templates
with tab4:
    st.header("📢 Communication Templates")
    
    # Dummy data samples
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("📋 Sample 1: Board Communication", type="secondary", key="comm1"):
            st.session_state.update({
                'communication_type': 'Board Presentation',
                'audience_comm': 'Board of Directors, Senior Leadership',
                'purpose_comm': 'Present succession planning strategy and progress for critical roles',
                'key_message': 'Strong succession pipeline established for all critical positions with 85% readiness achieved',
                'tone_style': 'Professional, Data-driven, Strategic',
                'urgency_level': 'Medium',
                'follow_up_required': 'Yes - Quarterly updates on progress'
            })
    
    with col_sample2:
        if st.button("👥 Sample 2: Manager Communication", type="secondary", key="comm2"):
            st.session_state.update({
                'communication_type': 'Manager Toolkit',
                'audience_comm': 'Line Managers, Department Heads',
                'purpose_comm': 'Guide managers on identifying and developing successors in their teams',
                'key_message': 'Every manager is responsible for building a succession pipeline and developing their team members',
                'tone_style': 'Supportive, Instructional, Collaborative',
                'urgency_level': 'Medium',
                'follow_up_required': 'Yes - Training sessions and support materials'
            })
    
    with col_sample3:
        if st.button("🎯 Sample 3: Employee Communication", type="secondary", key="comm3"):
            st.session_state.update({
                'communication_type': 'Employee Announcement',
                'audience_comm': 'All Employees',
                'purpose_comm': 'Communicate succession planning initiative and career development opportunities',
                'key_message': 'Tata Motors is investing in your career growth through structured succession planning and development programs',
                'tone_style': 'Encouraging, Transparent, Motivational',
                'urgency_level': 'Low',
                'follow_up_required': 'Yes - Career development sessions'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Communication Context")
        communication_type_options = ["Board Presentation", "Executive Update", "Manager Toolkit", "Employee Announcement", 
                                     "Succession Plan Review", "Development Progress Update", "Stakeholder Brief"]
        current_comm_type = st.session_state.get('communication_type', 'Board Presentation')
        
        try:
            comm_type_index = communication_type_options.index(current_comm_type)
        except ValueError:
            comm_type_index = 0
            
        communication_type = st.selectbox("Communication Type",
                                        communication_type_options,
                                        index=comm_type_index)
        audience_comm = st.text_input("Target Audience", value=st.session_state.get('audience_comm', ''))
        purpose_comm = st.text_area("Communication Purpose", height=80, value=st.session_state.get('purpose_comm', ''))
        key_message = st.text_area("Key Message/Outcome", height=80, value=st.session_state.get('key_message', ''))
    
    with col2:
        st.subheader("Communication Style")
        tone_style = st.text_input("Tone & Style", value=st.session_state.get('tone_style', ''))
        urgency_level_options = ["Low", "Medium", "High", "Critical"]
        current_urgency_level = st.session_state.get('urgency_level', 'Medium')
        
        try:
            urgency_level_index = urgency_level_options.index(current_urgency_level)
        except ValueError:
            urgency_level_index = 1
            
        urgency_level = st.selectbox("Urgency Level",
                                   urgency_level_options,
                                   index=urgency_level_index)
        follow_up_required = st.text_input("Follow-up Required", value=st.session_state.get('follow_up_required', ''))
        
        if st.button("📢 Generate Communication Template", type="primary"):
            if communication_type and audience_comm:
                prompt = f"""
                Create a comprehensive communication template for:
                
                Communication Type: {communication_type}
                Target Audience: {audience_comm}
                Purpose: {purpose_comm}
                Key Message: {key_message}
                Tone & Style: {tone_style}
                Urgency Level: {urgency_level}
                Follow-up Required: {follow_up_required}
                
                Please create a detailed communication template that includes:
                1. Communication Objective and Scope
                2. Key Messages and Talking Points
                3. Structured Content Framework
                4. Presentation/Document Template
                5. Q&A Preparation (anticipated questions and responses)
                6. Stakeholder Engagement Strategy
                7. Feedback Collection Methods
                8. Follow-up Action Plan
                9. Success Metrics for Communication
                10. Timeline and Distribution Plan
                
                For presentations, include slide structure and key visuals.
                For written communications, provide email/document templates.
                Make it professional and immediately usable.
                """
                
                with st.spinner("Creating your communication template..."):
                    content = generate_ai_content(prompt, "Communication Template")
                    if content:
                        st.session_state.generated_content['communication_template'] = content
            else:
                st.error("Please select Communication Type and specify Target Audience")
    
    # Display generated communication template
    if 'communication_template' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Communication Template")
        st.markdown(st.session_state.generated_content['communication_template'])
        
        st.download_button(
            label="📥 Download Communication Template",
            data=st.session_state.generated_content['communication_template'],
            file_name=f"Communication_Template_{communication_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 5: Policy & Governance
with tab5:
    st.header("📊 Policy & Governance Frameworks")
    
    # Dummy data samples
    st.subheader("🎯 Quick Test with Tata Motors Sample Data")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("📋 Sample 1: Corporate Policy", type="secondary", key="policy1"):
            st.session_state.update({
                'organization_size': '5000+ employees',
                'industry_policy': 'Automotive Manufacturing',
                'geographic_scope': 'India with global operations',
                'governance_level': 'Board Level',
                'policy_scope': 'All critical roles (Director level and above)',
                'review_frequency': 'Annual with quarterly updates',
                'compliance_requirements': 'Companies Act 2013, SEBI regulations, Tata Group governance standards'
            })
    
    with col_sample2:
        if st.button("🏢 Sample 2: Divisional Framework", type="secondary", key="policy2"):
            st.session_state.update({
                'organization_size': '1000-2000 employees per division',
                'industry_policy': 'Automotive Manufacturing',
                'geographic_scope': 'Multiple manufacturing locations in India',
                'governance_level': 'Divisional Leadership',
                'policy_scope': 'Key roles (Manager level and above)',
                'review_frequency': 'Bi-annual',
                'compliance_requirements': 'Corporate governance standards, local labor laws, safety regulations'
            })
    
    with col_sample3:
        if st.button("⚡ Sample 3: Emergency Protocol", type="secondary", key="policy3"):
            st.session_state.update({
                'organization_size': '5000+ employees',
                'industry_policy': 'Automotive Manufacturing',
                'geographic_scope': 'All operations',
                'governance_level': 'Executive Level',
                'policy_scope': 'Critical roles requiring immediate succession',
                'review_frequency': 'Quarterly',
                'compliance_requirements': 'Business continuity requirements, regulatory compliance, stakeholder obligations'
            })
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Organization Context")
        organization_size = st.text_input("Organization Size", value=st.session_state.get('organization_size', ''))
        industry_policy = st.text_input("Industry/Sector", value=st.session_state.get('industry_policy', ''))
        geographic_scope = st.text_input("Geographic Scope", value=st.session_state.get('geographic_scope', ''))
        governance_level_options = ["Board Level", "Executive Level", "Divisional Leadership", "Department Level"]
        current_governance = st.session_state.get('governance_level', 'Board Level')
        
        try:
            governance_index = governance_level_options.index(current_governance)
        except ValueError:
            governance_index = 0
            
        governance_level = st.selectbox("Governance Level",
                                      governance_level_options,
                                      index=governance_index)
    
    with col2:
        st.subheader("Policy Framework")
        policy_scope = st.text_area("Policy Scope & Coverage", height=80, value=st.session_state.get('policy_scope', ''))
        review_frequency_options = ["Monthly", "Quarterly", "Bi-annual", "Annual", "As needed"]
        current_review_freq = st.session_state.get('review_frequency', 'Annual')
        
        try:
            review_freq_index = review_frequency_options.index(current_review_freq)
        except ValueError:
            review_freq_index = 3
            
        review_frequency = st.selectbox("Review Frequency",
                                      review_frequency_options,
                                      index=review_freq_index)
        compliance_requirements = st.text_area("Compliance Requirements", height=80, value=st.session_state.get('compliance_requirements', ''))
        
        if st.button("📊 Generate Policy Framework", type="primary"):
            if organization_size and policy_scope:
                prompt = f"""
                Create a comprehensive succession planning policy and governance framework for:
                
                Organization Size: {organization_size}
                Industry: {industry_policy}
                Geographic Scope: {geographic_scope}
                Governance Level: {governance_level}
                Policy Scope: {policy_scope}
                Review Frequency: {review_frequency}
                Compliance Requirements: {compliance_requirements}
                
                Please create a detailed policy and governance framework that includes:
                1. Policy Statement and Objectives
                2. Scope and Applicability
                3. Roles and Responsibilities
                4. Succession Planning Process
                5. Governance Structure and Oversight
                6. Critical Role Identification Criteria
                7. Successor Assessment Standards
                8. Development and Readiness Requirements
                9. Emergency Succession Protocols
                10. Review and Monitoring Mechanisms
                11. Compliance and Audit Framework
                12. Communication and Transparency Guidelines
                13. Policy Implementation Timeline
                14. Performance Metrics and KPIs
                15. Risk Management and Mitigation
                
                Make it comprehensive, compliant, and suitable for board approval.
                """
                
                with st.spinner("Creating your policy framework..."):
                    content = generate_ai_content(prompt, "Policy Framework")
                    if content:
                        st.session_state.generated_content['policy_framework'] = content
            else:
                st.error("Please fill in Organization Size and Policy Scope")
    
    # Display generated policy framework
    if 'policy_framework' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📜 Generated Policy & Governance Framework")
        st.markdown(st.session_state.generated_content['policy_framework'])
        
        st.download_button(
            label="📥 Download Policy Framework",
            data=st.session_state.generated_content['policy_framework'],
            file_name=f"Succession_Policy_Framework_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Tab 6: Custom Succession Assistant
with tab6:
    st.header("🎨 Custom Succession Planning Assistant")
    st.markdown("Create any succession planning document or get expert advice with custom prompts")
    
    # Sample prompts based on best practices
    st.subheader("🎯 Best Practice Prompts for Succession Planning")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("📊 Sample: Comprehensive Strategy", type="secondary", key="custom_succ1"):
            st.session_state['custom_prompt_succ'] = """Develop a comprehensive succession planning strategy that ensures a smooth transition of key roles within Tata Motors. Include best practices for identifying and developing high-potential employees.

Current Organizational Context:
- 45,000+ employees globally
- Multiple business units (Passenger Vehicles, Commercial Vehicles, JLR)
- Critical roles: Plant Managers, R&D Directors, Sales Heads, Functional Leaders
- Current challenge: 60% of senior leadership eligible for retirement in next 5 years
- Focus on electric vehicle transition requiring new skill sets

Please provide a detailed strategy covering identification, development, and transition processes."""
    
    with col_sample2:
        if st.button("📋 Sample: Planning Template", type="secondary", key="custom_succ2"):
            st.session_state['custom_prompt_succ'] = """Create a succession planning template that outlines the key steps and timelines for identifying and developing successors for critical positions at Tata Motors. Include guidelines for assessing and mitigating potential risks.

Key Requirements:
- Template for Plant Manager positions across 8 manufacturing facilities
- Assessment criteria for technical and leadership competencies
- Risk mitigation for single points of failure
- Development timeline of 18-36 months
- Integration with annual talent reviews
- Compliance with Tata Group governance standards

Include specific timelines, assessment tools, and risk scenarios."""
    
    with col_sample3:
        if st.button("📈 Sample: Program Evaluation", type="secondary", key="custom_succ3"):
            st.session_state['custom_prompt_succ'] = """Evaluate the effectiveness of Tata Motors' current succession planning program and identify areas for improvement. Provide recommendations to enhance the program's impact and ensure seamless leadership transition.

Current Program Elements:
- Annual talent reviews conducted
- 70% of critical roles have identified successors
- Leadership development programs in place
- Cross-functional rotation opportunities available
- Challenges: Limited diversity in succession pipeline, gaps in digital/EV skills

Analyze gaps and provide specific recommendations for improvement."""
    
    st.markdown("---")
    
    # More sample prompts
    col_sample4, col_sample5 = st.columns(2)
    
    with col_sample4:
        if st.button("📢 Sample: Communication Plan", type="secondary", key="custom_succ4"):
            st.session_state['custom_prompt_succ'] = """Develop a communication plan for succession planning that effectively engages stakeholders and ensures transparency throughout the process at Tata Motors. Include strategies for managing potential resistance and fostering buy-in from key individuals.

Stakeholder Groups:
- Board of Directors and Tata Sons
- Senior Leadership Team
- Middle Management
- High-potential employees
- Union representatives
- External stakeholders (investors, analysts)

Address concerns about job security, fairness, and transparency while maintaining confidentiality."""
        
    with col_sample5:
        if st.button("🎯 Sample: Talent Assessment", type="secondary", key="custom_succ5"):
            st.session_state['custom_prompt_succ'] = """Conduct a talent assessment framework to identify high-potential employees and create individual development plans tailored to their specific needs at Tata Motors. Include recommendations for training, mentoring, and career progression opportunities.

Assessment Focus:
- Technical competencies for automotive industry
- Leadership potential for diverse teams
- Adaptability for electric vehicle transition
- Cultural fit with Tata values
- Global mindset for international operations

Include specific assessment tools, development recommendations, and career progression pathways."""
    
    st.markdown("---")
    
    # Custom prompt input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💭 Your Custom Succession Planning Request")
        custom_prompt = st.text_area(
            "Enter your succession planning question or document request:",
            height=250,
            value=st.session_state.get('custom_prompt_succ', ''),
            placeholder="""Examples:
• Create a emergency succession protocol for CEO position
• Design a cross-functional leadership rotation program
• Draft a diversity and inclusion strategy for succession pipeline
• Develop metrics to measure succession planning effectiveness
• Create a competency model for future automotive leaders
• Design a mentoring program for high-potential employees
• Build a knowledge transfer framework for retiring executives
• Create succession planning for international assignments"""
        )
        
        # Context options
        st.subheader("🎯 Context & Customization")
        col_context1, col_context2 = st.columns(2)
        
        with col_context1:
            company_context_succ = st.selectbox(
                "Company Context",
                ["Tata Motors", "Automotive Industry", "Manufacturing Company", "Large Corporation", "MNC", "Custom"],
                index=0
            )
            
            if company_context_succ == "Custom":
                custom_company_succ = st.text_input("Enter your company/industry context:")
                company_context_succ = custom_company_succ
            
            document_type_succ = st.selectbox(
                "Document Type",
                ["Strategy Document", "Policy Framework", "Process/Procedure", "Assessment Tool", "Communication Plan", "Training Material", "Template/Form", "Other"]
            )
        
        with col_context2:
            urgency_succ = st.selectbox(
                "Detail Level",
                ["High Detail (Comprehensive)", "Medium Detail (Standard)", "Low Detail (Brief Overview)"]
            )
            
            target_audience_succ = st.multiselect(
                "Target Audience",
                ["Board of Directors", "Senior Leadership", "HR Team", "Line Managers", "High-Potential Employees", "All Employees", "External Stakeholders"],
                default=["Senior Leadership"]
            )
    
    with col2:
        st.subheader("🚀 Generate Content")
        
        if st.button("🎨 Generate Custom Succession Content", type="primary", key="generate_custom_succ"):
            if custom_prompt.strip():
                # Build enhanced prompt with context
                enhanced_prompt = f"""
                Company Context: {company_context_succ}
                Document Type: {document_type_succ}
                Target Audience: {', '.join(target_audience_succ)}
                Detail Level: {urgency_succ}
                
                Succession Planning Request: {custom_prompt}
                
                Please create professional succession planning content that:
                1. Is specific to the company context provided
                2. Follows succession planning best practices and governance standards
                3. Is appropriate for the target audience
                4. Matches the requested detail level
                5. Is immediately usable and actionable
                6. Includes relevant frameworks, templates, or tools as needed
                7. Addresses risk mitigation and compliance requirements
                8. Considers organizational continuity and leadership development
                
                If this is a strategy document, include implementation guidelines and success metrics.
                If this is a policy, ensure governance and compliance alignment.
                If this is an assessment tool, make it practical and measurable.
                If this is a communication plan, address stakeholder concerns and resistance.
                """
                
                with st.spinner("Creating your custom succession planning content..."):
                    content = generate_ai_content(enhanced_prompt, "Custom Succession Content")
                    if content:
                        st.session_state.generated_content['custom_succession'] = content
            else:
                st.error("Please enter your succession planning request in the text area")
        
        # Additional options
        st.markdown("---")
        st.subheader("📋 Quick Actions")
        
        if st.button("🔄 Clear Form", key="clear_custom_succ"):
            st.session_state['custom_prompt_succ'] = ''
            if 'custom_succession' in st.session_state.generated_content:
                del st.session_state.generated_content['custom_succession']
            st.rerun()
        
        if st.button("💡 Get Ideas", key="ideas_custom_succ"):
            st.session_state['custom_prompt_succ'] = """Suggest 10 innovative succession planning initiatives that Tata Motors could implement to:
- Build a robust leadership pipeline for the electric vehicle era
- Ensure diversity and inclusion in succession planning
- Create effective knowledge transfer from retiring leaders
- Develop global leadership capabilities
- Strengthen succession planning for technical roles
- Build resilience in critical manufacturing positions

For each initiative, provide a brief description, implementation approach, and expected benefits."""
    
    # Display generated content
    if 'custom_succession' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Succession Planning Content")
        
        # Content display with formatting
        content = st.session_state.generated_content['custom_succession']
        st.markdown(content)
        
        # Download and action buttons
        col_download1, col_download2, col_download3 = st.columns(3)
        
        with col_download1:
            st.download_button(
                label="📥 Download as Text",
                data=content,
                file_name=f"Custom_Succession_Content_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
        
        with col_download2:
            if st.button("📋 Copy to Clipboard", key="copy_custom_succ"):
                st.info("Content copied! (Paste using Ctrl+V)")
        
        with col_download3:
            if st.button("✏️ Refine Content", key="refine_custom_succ"):
                st.session_state['custom_prompt_succ'] = f"Please refine and improve the following succession planning content:\n\n{content}\n\nMake it more detailed, professional, and actionable with specific implementation steps."

# Footer
st.markdown("---")
st.markdown("### 🚀 Ready for the next module?")
st.info("This is Module 2 of 9. Continue building your comprehensive HR toolkit with additional specialized modules.")

# Instructions
with st.expander("📖 How to Use This Succession Planning Module"):
    st.markdown("""
    ## 🎯 **Standard Features (Tabs 1-5):**
    1. **📋 Succession Plan Formats** - Create comprehensive succession plans for critical roles
    2. **✅ Readiness Checklists** - Assess successor preparedness with detailed checklists
    3. **🎯 Development Action Plans** - Build targeted development programs for successors
    4. **📢 Communication Templates** - Engage stakeholders with professional communications
    5. **📊 Policy & Governance** - Establish robust succession planning frameworks
    
    ## 🎨 **Custom Succession Assistant (Tab 6):**
    - **Best Practice Prompts** - Use proven succession planning templates
    - **Custom Requests** - Handle any succession planning need
    - **Context-Aware** - Tailored to your industry and organization
    - **Professional Output** - Board-ready documents and strategies
    
    **Tips:**
    - Use sample data buttons for quick testing and learning
    - Be specific about roles, timelines, and development needs
    - Consider both technical and leadership competencies
    - Address compliance and governance requirements
    - Plan for emergency succession scenarios
    - Include diversity and inclusion considerations
    """)

# Navigation
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("← Module 1: Talent Development", key="nav_prev"):
        st.switch_page("pages/01_talent_development.py")

with col_nav2:
    if st.button("🏠 Main Menu", key="nav_home"):
        st.switch_page("hr_copilot_main.py")

with col_nav3:
    if st.button("Module 3: Talent Acquisition →", key="nav_next", disabled=True):
        st.info("Coming Soon!")