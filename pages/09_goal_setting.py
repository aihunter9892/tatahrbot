import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="HR Copilot - BSC Alignment & Goal Setting",
    page_icon="🎯",
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
    st.markdown("### 🎯 Module 5: BSC Alignment & Goal Setting")
    st.markdown("Align performance with business objectives and drive strategic accountability")

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
            
            system_prompt = """You are a world-class Strategic Performance Management and Balanced Scorecard specialist with 20+ years of experience in:
- Balanced Scorecard (BSC) framework implementation across Fortune 500 companies
- Strategic goal cascading and alignment methodologies
- SMART and OKR goal-setting frameworks
- Performance measurement and KPI development
- Strategic planning and execution excellence

CRITICAL CONTENT GENERATION INSTRUCTIONS:
- Write ONLY the requested document content - no introductions, explanations, or commentary
- Do NOT write phrases like "Here's a comprehensive..." or "I'll create..." or "This document..."
- Start directly with the substantive content
- Use clear, professional language without markdown formatting
- Use CAPITAL LETTERS for main section headings
- Use numbered lists and bullet points with dashes (-)
- Include specific, measurable examples and industry best practices
- Make all content immediately implementable in corporate environments
- Focus on strategic alignment and measurable business outcomes

Expertise Areas:
- Financial perspective: Revenue growth, profitability, cost management, ROI optimization
- Customer perspective: Satisfaction, retention, market share, value proposition
- Internal process perspective: Operational excellence, quality, efficiency, innovation
- Learning & growth perspective: Employee capabilities, culture, technology, leadership

Generate practical, strategic content that drives real business performance and organizational alignment."""
            
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=3000,
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
st.title("🎯 HR Copilot - BSC Alignment & Goal Setting")
st.markdown("Align individual and team performance with strategic business objectives through proven BSC methodologies")

# Tab layout
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎯 SMART Goals Generator (BSC-Aligned)",
    "📊 BSC Performance Framework", 
    "📈 Goal Cascading System",
    "📋 Performance Review Templates",
    "📧 Goal Management Communications",
    "🎨 Custom BSC Tools"
])

# Tab 1: SMART Goals Generator (BSC-Aligned)
with tab1:
    st.header("🎯 SMART Goals Generator (BSC-Aligned)")
    st.markdown("Generate strategic SMART goals aligned with Balanced Scorecard perspectives")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Goal Types")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("💰 Financial Perspective Goal", type="secondary"):
            st.session_state.update({
                'goal_role': 'Sales Director',
                'bsc_perspective': 'Financial',
                'strategic_objective': 'Increase Revenue Growth',
                'goal_timeframe': 'FY 2024',
                'specific_focus': 'Enterprise client acquisition',
                'current_baseline': 'Current enterprise revenue: $2.5M annually, 15 enterprise clients',
                'success_metrics': 'Revenue target, number of new enterprise clients, average deal size',
                'constraints': 'Limited sales team size, competitive market conditions'
            })
    
    with col_sample2:
        if st.button("👥 Customer Perspective Goal", type="secondary"):
            st.session_state.update({
                'goal_role': 'Customer Success Manager',
                'bsc_perspective': 'Customer',
                'strategic_objective': 'Enhance Customer Satisfaction & Retention',
                'goal_timeframe': 'Q3-Q4 2024',
                'specific_focus': 'Customer onboarding experience improvement',
                'current_baseline': 'Current NPS: 7.2, Customer retention: 85%, Time to value: 45 days',
                'success_metrics': 'Net Promoter Score (NPS), Customer retention rate, Time to first value',
                'constraints': 'Resource limitations, complex product features'
            })
    
    with col_sample3:
        if st.button("⚙️ Internal Process Goal", type="secondary"):
            st.session_state.update({
                'goal_role': 'Operations Manager',
                'bsc_perspective': 'Internal Business Process',
                'strategic_objective': 'Improve Operational Efficiency',
                'goal_timeframe': '6 months',
                'specific_focus': 'Automation of manual processes',
                'current_baseline': 'Current process time: 4 hours/task, Error rate: 8%, Manual steps: 12',
                'success_metrics': 'Process completion time, Error reduction percentage, Automation rate',
                'constraints': 'Technology budget, Change management requirements'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Goal Context & Alignment")
        goal_role = st.text_input("Role/Position", value=st.session_state.get('goal_role', ''))
        bsc_perspective = st.selectbox("BSC Perspective", [
            "Financial", 
            "Customer", 
            "Internal Business Process", 
            "Learning & Growth"
        ])
        strategic_objective = st.text_input("Strategic Objective", value=st.session_state.get('strategic_objective', ''))
        goal_timeframe = st.text_input("Goal Timeframe", value=st.session_state.get('goal_timeframe', ''))
    
    with col2:
        st.subheader("Goal Specifics & Metrics")
        specific_focus = st.text_area("Specific Focus Area", height=80, value=st.session_state.get('specific_focus', ''))
        current_baseline = st.text_area("Current State/Baseline", height=80, value=st.session_state.get('current_baseline', ''))
        success_metrics = st.text_area("Success Metrics/KPIs", height=80, value=st.session_state.get('success_metrics', ''))
        constraints = st.text_area("Constraints/Challenges", height=80, value=st.session_state.get('constraints', ''))
        
        if st.button("🎯 Generate SMART Goal", type="primary"):
            if goal_role and strategic_objective and specific_focus:
                prompt = f"""Create a comprehensive SMART goal aligned with Balanced Scorecard methodology for:

ROLE/POSITION: {goal_role}
BSC PERSPECTIVE: {bsc_perspective}
STRATEGIC OBJECTIVE: {strategic_objective}
TIMEFRAME: {goal_timeframe}
SPECIFIC FOCUS AREA: {specific_focus}
CURRENT STATE/BASELINE: {current_baseline}
SUCCESS METRICS/KPIS: {success_metrics}
CONSTRAINTS/CHALLENGES: {constraints}

Generate a complete SMART goal framework including:

SMART GOAL STATEMENT
Create one clear, compelling goal statement that incorporates all SMART criteria

SMART BREAKDOWN ANALYSIS
- Specific: Detailed explanation of what exactly will be accomplished
- Measurable: Quantifiable metrics and measurement methods
- Achievable: Realistic assessment based on resources and constraints
- Relevant: Clear connection to strategic objective and BSC perspective
- Time-bound: Specific deadlines and milestone timeline

KEY PERFORMANCE INDICATORS (KPIS)
- Primary KPIs with specific targets and measurement frequency
- Secondary metrics for comprehensive performance tracking
- Leading indicators for early progress assessment
- Lagging indicators for final outcome measurement

ACTION PLAN FRAMEWORK
- Critical activities required for goal achievement
- Resource requirements and budget implications
- Risk mitigation strategies for identified constraints
- Dependencies and stakeholder requirements

PROGRESS TRACKING SYSTEM
- Weekly/monthly check-in framework
- Progress reporting methodology
- Course correction triggers and processes
- Success celebration and recognition plan

BSC STRATEGIC ALIGNMENT
- Direct contribution to organizational financial performance
- Impact on customer value proposition and satisfaction
- Internal process improvements and operational excellence
- Learning and growth capability development

Ensure the goal drives measurable business impact and aligns with enterprise strategic priorities."""

                with st.spinner("Generating strategic SMART goal..."):
                    content = generate_content(prompt, "SMART Goal Framework")
                    if content:
                        st.session_state.generated_content['smart_goal'] = content
            else:
                st.error("Please fill in Role, Strategic Objective, and Specific Focus Area")
    
    # Display generated content
    if 'smart_goal' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated SMART Goal Framework")
        cleaned_content = clean_text(st.session_state.generated_content['smart_goal'])
        st.text_area("SMART Goal Content", value=cleaned_content, height=500)
        create_download_button(cleaned_content, f"SMART_Goal_{goal_role.replace(' ', '_')}", "📥 Download SMART Goal")

# Tab 2: BSC Performance Framework
with tab2:
    st.header("📊 BSC Performance Framework")
    st.markdown("Create comprehensive Balanced Scorecard frameworks for departments or organizations")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Frameworks")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("🏢 Department BSC", type="secondary"):
            st.session_state.update({
                'framework_scope': 'Human Resources Department',
                'organization_type': 'Technology Company',
                'strategic_priorities': 'Talent acquisition, Employee engagement, Performance management, Learning & development',
                'key_stakeholders': 'Executive team, Department managers, Employees, External candidates',
                'measurement_period': 'Annual with quarterly reviews',
                'current_challenges': 'High turnover, Skills gaps, Remote work management'
            })
    
    with col_sample2:
        if st.button("🏭 Business Unit BSC", type="secondary"):
            st.session_state.update({
                'framework_scope': 'Manufacturing Operations',
                'organization_type': 'Manufacturing Company',
                'strategic_priorities': 'Quality improvement, Cost reduction, Safety excellence, Productivity optimization',
                'key_stakeholders': 'Plant managers, Production teams, Quality assurance, Supply chain',
                'measurement_period': 'Monthly with annual strategic reviews',
                'current_challenges': 'Supply chain disruptions, Quality consistency, Safety incidents'
            })
    
    with col_sample3:
        if st.button("🚀 Startup BSC", type="secondary"):
            st.session_state.update({
                'framework_scope': 'Entire Organization',
                'organization_type': 'Technology Startup',
                'strategic_priorities': 'Customer acquisition, Product development, Revenue growth, Team scaling',
                'key_stakeholders': 'Founders, Investors, Customers, Employees, Partners',
                'measurement_period': 'Monthly with quarterly pivots',
                'current_challenges': 'Limited resources, Market validation, Scaling challenges'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Framework Scope & Context")
        framework_scope = st.text_input("Framework Scope", value=st.session_state.get('framework_scope', ''))
        organization_type = st.selectbox("Organization Type", [
            "Technology Company",
            "Financial Services", 
            "Healthcare Organization",
            "Manufacturing Company",
            "Retail Business",
            "Professional Services",
            "Non-profit Organization",
            "Government Agency",
            "Startup",
            "Other"
        ])
        strategic_priorities = st.text_area("Strategic Priorities", height=100, value=st.session_state.get('strategic_priorities', ''))
    
    with col2:
        st.subheader("Implementation Details")
        key_stakeholders = st.text_area("Key Stakeholders", height=80, value=st.session_state.get('key_stakeholders', ''))
        measurement_period = st.text_input("Measurement Period", value=st.session_state.get('measurement_period', ''))
        current_challenges = st.text_area("Current Challenges", height=100, value=st.session_state.get('current_challenges', ''))
        
        if st.button("📊 Generate BSC Framework", type="primary"):
            if framework_scope and strategic_priorities:
                prompt = f"""Create a comprehensive Balanced Scorecard performance framework for:

FRAMEWORK SCOPE: {framework_scope}
ORGANIZATION TYPE: {organization_type}
STRATEGIC PRIORITIES: {strategic_priorities}
KEY STAKEHOLDERS: {key_stakeholders}
MEASUREMENT PERIOD: {measurement_period}
CURRENT CHALLENGES: {current_challenges}

Develop a complete BSC framework including:

BALANCED SCORECARD OVERVIEW
- Framework purpose and strategic alignment
- Success criteria and expected outcomes
- Implementation timeline and phases
- Governance structure and accountability

FINANCIAL PERSPECTIVE
- Strategic objectives aligned with business goals
- Key performance indicators with specific targets
- Measurement methodologies and data sources
- Revenue, profitability, and cost management metrics
- Investment ROI and efficiency measures

CUSTOMER PERSPECTIVE  
- Customer value proposition definition
- Customer satisfaction and loyalty metrics
- Market share and customer acquisition KPIs
- Customer lifetime value and retention rates
- Service quality and delivery excellence measures

INTERNAL BUSINESS PROCESS PERSPECTIVE
- Core process optimization objectives
- Operational efficiency and quality metrics
- Innovation and new product development KPIs
- Technology and digital transformation measures
- Risk management and compliance indicators

LEARNING AND GROWTH PERSPECTIVE
- Employee capability development objectives
- Skills and competency assessment metrics
- Employee engagement and satisfaction KPIs
- Leadership development and succession planning
- Technology and infrastructure readiness measures

STRATEGIC LINKAGE MAP
- Cause-and-effect relationships between perspectives
- Strategic initiative prioritization matrix
- Resource allocation and investment priorities
- Risk assessment and mitigation strategies

IMPLEMENTATION ROADMAP
- Phase 1: Foundation and baseline establishment
- Phase 2: Measurement system deployment
- Phase 3: Performance management integration
- Phase 4: Continuous improvement and optimization

PERFORMANCE MEASUREMENT SYSTEM
- KPI dashboard design and visualization
- Data collection and validation processes
- Reporting frequency and distribution
- Performance review and decision-making protocols
- Continuous improvement and adjustment mechanisms

Address the specific challenges mentioned and ensure alignment with organizational strategic priorities."""

                with st.spinner("Generating BSC framework..."):
                    content = generate_content(prompt, "BSC Framework")
                    if content:
                        st.session_state.generated_content['bsc_framework'] = content
            else:
                st.error("Please fill in Framework Scope and Strategic Priorities")
    
    # Display generated content
    if 'bsc_framework' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated BSC Performance Framework")
        cleaned_content = clean_text(st.session_state.generated_content['bsc_framework'])
        st.text_area("BSC Framework Content", value=cleaned_content, height=500)
        create_download_button(cleaned_content, f"BSC_Framework_{framework_scope.replace(' ', '_')}", "📥 Download BSC Framework")

# Tab 3: Goal Cascading System
with tab3:
    st.header("📈 Goal Cascading System")
    st.markdown("Create systematic goal cascading from strategic to individual levels")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Cascading Scenarios")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("🏢 Corporate to Department", type="secondary"):
            st.session_state.update({
                'cascade_level': 'Corporate to Department',
                'organization_goal': 'Achieve 25% revenue growth and expand into 3 new markets by end of FY2024',
                'target_level': 'Sales & Marketing Departments',
                'current_performance': 'Current revenue: $10M, Markets: 2, Sales team: 15 people',
                'cascade_timeframe': '12 months with quarterly milestones',
                'resource_constraints': 'Limited marketing budget, Need to hire 5 additional sales staff'
            })
    
    with col_sample2:
        if st.button("📊 Department to Team", type="secondary"):
            st.session_state.update({
                'cascade_level': 'Department to Team',
                'organization_goal': 'Improve customer satisfaction score from 7.5 to 9.0 and reduce churn by 15%',
                'target_level': 'Customer Success Teams',
                'current_performance': 'Current CSAT: 7.5, Churn rate: 12%, Team size: 8 members',
                'cascade_timeframe': '6 months with monthly check-ins',
                'resource_constraints': 'Limited training budget, High workload per team member'
            })
    
    with col_sample3:
        if st.button("👤 Team to Individual", type="secondary"):
            st.session_state.update({
                'cascade_level': 'Team to Individual',
                'organization_goal': 'Reduce software defects by 50% and improve deployment frequency to weekly releases',
                'target_level': 'Individual Software Engineers',
                'current_performance': 'Current defect rate: 20 bugs/release, Deployment: Bi-weekly',
                'cascade_timeframe': '3 months with weekly sprint reviews',
                'resource_constraints': 'Legacy codebase, Limited testing automation'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cascading Context")
        cascade_level = st.selectbox("Cascading Level", [
            "Corporate to Department",
            "Department to Team", 
            "Team to Individual",
            "Corporate to Individual",
            "Multi-level Cascade"
        ])
        organization_goal = st.text_area("Organizational/Higher-Level Goal", height=100, value=st.session_state.get('organization_goal', ''))
        target_level = st.text_input("Target Level/Recipients", value=st.session_state.get('target_level', ''))
    
    with col2:
        st.subheader("Performance Context")
        current_performance = st.text_area("Current Performance Baseline", height=80, value=st.session_state.get('current_performance', ''))
        cascade_timeframe = st.text_input("Cascading Timeframe", value=st.session_state.get('cascade_timeframe', ''))
        resource_constraints = st.text_area("Resource Constraints", height=80, value=st.session_state.get('resource_constraints', ''))
        
        if st.button("📈 Generate Goal Cascading System", type="primary"):
            if organization_goal and target_level:
                prompt = f"""Create a comprehensive goal cascading system for:

CASCADING LEVEL: {cascade_level}
ORGANIZATIONAL/HIGHER-LEVEL GOAL: {organization_goal}
TARGET LEVEL/RECIPIENTS: {target_level}
CURRENT PERFORMANCE BASELINE: {current_performance}
CASCADING TIMEFRAME: {cascade_timeframe}
RESOURCE CONSTRAINTS: {resource_constraints}

Develop a complete goal cascading framework including:

CASCADING METHODOLOGY
- Strategic alignment principles and best practices
- Goal decomposition and translation methodology
- Accountability and ownership distribution
- Communication and engagement strategy

CASCADED GOAL STRUCTURE
- Primary cascaded objectives with clear ownership
- Supporting sub-goals and specific activities
- SMART criteria application for each cascaded goal
- Priority ranking and resource allocation

ALIGNMENT MATRIX
- Direct linkage from organizational to individual goals
- Contribution mapping and impact assessment
- Dependencies and interdepartmental coordination
- Cross-functional collaboration requirements

PERFORMANCE MEASUREMENT SYSTEM
- Cascaded KPIs with specific targets and timelines
- Leading and lagging indicator identification
- Progress tracking and reporting mechanisms
- Performance dashboard and visualization framework

IMPLEMENTATION PLAN
- Phase 1: Goal translation and communication
- Phase 2: Individual goal setting and alignment
- Phase 3: Performance tracking system deployment
- Phase 4: Regular review and adjustment process

COMMUNICATION STRATEGY
- Goal cascading workshops and training sessions
- Clear communication of expectations and rationale
- Regular feedback and two-way communication channels
- Success stories and best practice sharing

ACCOUNTABILITY FRAMEWORK
- Clear roles and responsibilities at each level
- Performance review and evaluation criteria
- Recognition and incentive alignment
- Corrective action and support mechanisms

MONITORING AND ADJUSTMENT SYSTEM
- Regular progress review meetings and checkpoints
- Performance variance analysis and root cause identification
- Goal adjustment and rebalancing procedures
- Continuous improvement and optimization process

RISK MANAGEMENT
- Identification of potential cascading risks and barriers
- Mitigation strategies for resource constraints
- Contingency planning for performance gaps
- Change management and adaptation protocols

Address the specific resource constraints and ensure practical implementation within the given timeframe."""

                with st.spinner("Generating goal cascading system..."):
                    content = generate_content(prompt, "Goal Cascading System")
                    if content:
                        st.session_state.generated_content['goal_cascading'] = content
            else:
                st.error("Please fill in Organizational Goal and Target Level")
    
    # Display generated content
    if 'goal_cascading' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Goal Cascading System")
        cleaned_content = clean_text(st.session_state.generated_content['goal_cascading'])
        st.text_area("Goal Cascading Content", value=cleaned_content, height=500)
        create_download_button(cleaned_content, f"Goal_Cascading_{cascade_level.replace(' ', '_')}", "📥 Download Cascading System")

# Tab 4: Performance Review Templates
with tab4:
    st.header("📋 Performance Review Templates")
    st.markdown("Create goal-focused performance review templates aligned with BSC methodology")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Review Types")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("📅 Annual BSC Review", type="secondary"):
            st.session_state.update({
                'review_type': 'Annual Performance Review',
                'review_role': 'Department Manager',
                'review_focus': 'BSC goal achievement, Strategic contribution, Leadership development',
                'review_period': 'Full Year (Jan-Dec 2024)',
                'bsc_elements': 'Financial results, Customer impact, Process improvements, Team development',
                'rating_system': '5-point scale with BSC perspective weighting'
            })
    
    with col_sample2:
        if st.button("📊 Quarterly Goal Review", type="secondary"):
            st.session_state.update({
                'review_type': 'Quarterly Goal Check-in',
                'review_role': 'Individual Contributor',
                'review_focus': 'Goal progress, Obstacle identification, Resource needs, Next quarter planning',
                'review_period': 'Q3 2024 (Jul-Sep)',
                'bsc_elements': 'KPI achievement, Process efficiency, Skill development, Customer feedback',
                'rating_system': 'Progress tracking with improvement recommendations'
            })
    
    with col_sample3:
        if st.button("🎯 Mid-Year Strategic Review", type="secondary"):
            st.session_state.update({
                'review_type': 'Mid-Year Strategic Review',
                'review_role': 'Senior Leader',
                'review_focus': 'Strategic goal progress, Market adaptation, Team performance, Future planning',
                'review_period': 'First Half 2024 (Jan-Jun)',
                'bsc_elements': 'Financial performance, Market position, Operational excellence, Capability building',
                'rating_system': 'Strategic impact assessment with action planning'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Review Framework")
        review_type = st.selectbox("Review Type", [
            "Annual Performance Review",
            "Quarterly Goal Check-in",
            "Mid-Year Strategic Review",
            "Project-based Review",
            "Development Review"
        ])
        review_role = st.text_input("Target Role Level", value=st.session_state.get('review_role', ''))
        review_period = st.text_input("Review Period", value=st.session_state.get('review_period', ''))
    
    with col2:
        st.subheader("Review Content")
        review_focus = st.text_area("Review Focus Areas", height=80, value=st.session_state.get('review_focus', ''))
        bsc_elements = st.text_area("BSC Elements to Evaluate", height=80, value=st.session_state.get('bsc_elements', ''))
        rating_system = st.text_input("Rating/Evaluation System", value=st.session_state.get('rating_system', ''))
        
        if st.button("📋 Generate Performance Review Template", type="primary"):
            if review_type and review_role and review_focus:
                prompt = f"""Create a comprehensive performance review template for:

REVIEW TYPE: {review_type}
TARGET ROLE LEVEL: {review_role}
REVIEW PERIOD: {review_period}
REVIEW FOCUS AREAS: {review_focus}
BSC ELEMENTS TO EVALUATE: {bsc_elements}
RATING/EVALUATION SYSTEM: {rating_system}

Develop a complete performance review framework including:

REVIEW TEMPLATE STRUCTURE
- Employee and reviewer information section
- Review period and goal context overview
- Performance evaluation methodology
- Development planning and future goal setting

BSC-ALIGNED PERFORMANCE EVALUATION

FINANCIAL PERSPECTIVE ASSESSMENT
- Revenue generation and cost management contributions
- ROI and productivity improvements achieved
- Budget management and financial stewardship
- Business impact and value creation metrics

CUSTOMER PERSPECTIVE EVALUATION
- Customer satisfaction and relationship management
- Service quality and delivery excellence
- Market reputation and brand contribution
- Customer retention and loyalty building

INTERNAL PROCESS PERSPECTIVE REVIEW
- Operational efficiency and process improvement
- Quality standards and compliance adherence
- Innovation and continuous improvement initiatives
- Cross-functional collaboration and teamwork

LEARNING AND GROWTH PERSPECTIVE ANALYSIS
- Skill development and competency building
- Knowledge sharing and mentoring contributions
- Leadership capabilities and potential
- Adaptability and change management

GOAL ACHIEVEMENT ASSESSMENT
- Specific goal accomplishment with quantified results
- KPI performance against established targets
- Challenge management and problem-solving effectiveness
- Strategic initiative contribution and impact

COMPETENCY EVALUATION FRAMEWORK
- Role-specific technical competencies
- Leadership and management capabilities
- Communication and interpersonal skills
- Strategic thinking and business acumen

DEVELOPMENT PLANNING SECTION
- Strengths identification and leverage opportunities
- Development areas and improvement priorities
- Learning and growth recommendations
- Career progression and advancement planning

FUTURE GOAL SETTING FRAMEWORK
- Strategic objective alignment for next period
- SMART goal development guidelines
- Resource requirements and support needs
- Success metrics and accountability measures

MANAGER ASSESSMENT SECTION
- Overall performance summary and rating
- Specific achievement recognition
- Development recommendations and support commitments
- Career discussion and progression planning

EMPLOYEE SELF-ASSESSMENT SECTION
- Self-reflection on performance and achievements
- Personal development insights and aspirations
- Feedback on support received and needed
- Career goals and interest areas

ACTION PLANNING AND FOLLOW-UP
- Specific development actions with timelines
- Performance improvement commitments
- Resource allocation and support requirements
- Next review period preparation and expectations

Ensure the template promotes constructive dialogue, strategic alignment, and continuous performance improvement."""

                with st.spinner("Generating performance review template..."):
                    content = generate_content(prompt, "Performance Review Template")
                    if content:
                        st.session_state.generated_content['review_template'] = content
            else:
                st.error("Please fill in Review Type, Target Role Level, and Review Focus Areas")
    
    # Display generated content
    if 'review_template' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Performance Review Template")
        cleaned_content = clean_text(st.session_state.generated_content['review_template'])
        st.text_area("Review Template Content", value=cleaned_content, height=500)
        create_download_button(cleaned_content, f"Review_Template_{review_type.replace(' ', '_')}", "📥 Download Review Template")

# Tab 5: Goal Management Communications
with tab5:
    st.header("📧 Goal Management Communications")
    st.markdown("Create strategic communications for goal setting, tracking, and achievement")
    
    # Quick samples
    st.subheader("🎯 Quick Sample Communications")
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("📧 Goal Setting Launch", type="secondary"):
            st.session_state.update({
                'comm_type': 'Goal Setting Season Launch Email',
                'comm_audience': 'All Employees and Managers',
                'comm_purpose': 'Announce annual goal setting process and BSC alignment',
                'comm_timeline': 'Next 4 weeks',
                'key_messages': 'Strategic alignment importance, Process timeline, Manager support, Resources available',
                'call_to_action': 'Complete goal setting by deadline, Schedule manager meetings'
            })
    
    with col_sample2:
        if st.button("📊 Progress Update", type="secondary"):
            st.session_state.update({
                'comm_type': 'Quarterly Progress Update',
                'comm_audience': 'Department Teams',
                'comm_purpose': 'Share progress against BSC objectives and celebrate achievements',
                'comm_timeline': 'End of Q2 2024',
                'key_messages': 'Progress highlights, Areas needing attention, Team achievements, Next quarter focus',
                'call_to_action': 'Review individual progress, Identify support needs, Adjust goals if needed'
            })
    
    with col_sample3:
        if st.button("🏆 Achievement Recognition", type="secondary"):
            st.session_state.update({
                'comm_type': 'Goal Achievement Recognition',
                'comm_audience': 'High Performers and Teams',
                'comm_purpose': 'Recognize exceptional goal achievement and strategic contribution',
                'comm_timeline': 'Monthly recognition cycle',
                'key_messages': 'Specific achievements, Business impact, Team inspiration, Continued excellence',
                'call_to_action': 'Share success stories, Mentor others, Set stretch goals for next period'
            })
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Communication Details")
        comm_type = st.selectbox("Communication Type", [
            "Goal Setting Season Launch Email",
            "Quarterly Progress Update",
            "Goal Achievement Recognition",
            "Performance Review Reminder",
            "Goal Adjustment Notification",
            "BSC Training Announcement",
            "Year-End Goal Summary"
        ])
        comm_audience = st.text_input("Target Audience", value=st.session_state.get('comm_audience', ''))
        comm_purpose = st.text_area("Communication Purpose", height=80, value=st.session_state.get('comm_purpose', ''))
    
    with col2:
        st.subheader("Message Framework")
        comm_timeline = st.text_input("Relevant Timeline/Deadline", value=st.session_state.get('comm_timeline', ''))
        key_messages = st.text_area("Key Messages to Include", height=100, value=st.session_state.get('key_messages', ''))
        call_to_action = st.text_area("Call to Action", height=80, value=st.session_state.get('call_to_action', ''))
        
        if st.button("📧 Generate Communication", type="primary"):
            if comm_type and comm_audience and comm_purpose:
                prompt = f"""Create a strategic goal management communication for:

COMMUNICATION TYPE: {comm_type}
TARGET AUDIENCE: {comm_audience}
COMMUNICATION PURPOSE: {comm_purpose}
RELEVANT TIMELINE/DEADLINE: {comm_timeline}
KEY MESSAGES TO INCLUDE: {key_messages}
CALL TO ACTION: {call_to_action}

Develop a complete communication package including:

EMAIL COMMUNICATION
- Compelling subject line that drives engagement
- Executive summary for busy professionals
- Clear and motivating message body
- Specific action items with deadlines
- Resource links and support information

STRATEGIC MESSAGING FRAMEWORK
- Alignment with organizational strategic priorities
- BSC perspective integration and value proposition
- Performance improvement and business impact focus
- Employee engagement and motivation elements

CONTENT STRUCTURE
- Opening that captures attention and sets context
- Main message with clear rationale and benefits
- Specific instructions and expectations
- Support and resources available
- Timeline and accountability measures
- Positive and encouraging conclusion

SUPPORTING MATERIALS
- FAQ section addressing common questions
- Resource list with tools and templates
- Contact information for support and clarification
- Follow-up communication schedule
- Success metrics and tracking methods

MANAGER TOOLKIT COMPONENTS
- Key talking points for team discussions
- Frequently asked questions and answers
- Escalation procedures for challenges
- Recognition and celebration guidelines
- Progress tracking and reporting methods

AUDIENCE-SPECIFIC CUSTOMIZATION
- Role-based messaging and expectations
- Department-specific context and examples
- Career level appropriate tone and complexity
- Cultural sensitivity and inclusion considerations

ENGAGEMENT STRATEGIES
- Interactive elements and feedback mechanisms
- Peer collaboration and knowledge sharing opportunities
- Recognition and incentive program integration
- Social proof and success story inclusion

FOLLOW-UP FRAMEWORK
- Progress check-in schedule and methods
- Reminder sequence for key deadlines
- Escalation process for non-compliance
- Celebration and recognition timeline
- Continuous improvement feedback collection

Ensure the communication is professional, motivating, and drives the desired behavioral outcomes."""

                with st.spinner("Generating goal management communication..."):
                    content = generate_content(prompt, "Goal Management Communication")
                    if content:
                        st.session_state.generated_content['goal_communication'] = content
            else:
                st.error("Please fill in Communication Type, Target Audience, and Communication Purpose")
    
    # Display generated content
    if 'goal_communication' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Goal Management Communication")
        cleaned_content = clean_text(st.session_state.generated_content['goal_communication'])
        st.text_area("Communication Content", value=cleaned_content, height=500)
        create_download_button(cleaned_content, f"Goal_Communication_{comm_type.replace(' ', '_')}", "📥 Download Communication")

# Tab 6: Custom BSC Tools
with tab6:
    st.header("🎨 Custom BSC & Goal Setting Tools")
    st.markdown("Create any strategic alignment, BSC, or goal management framework")
    
    # Sample prompts
    st.subheader("🎯 Best Practice BSC Prompts")
    col_sample1, col_sample2 = st.columns(2)
    
    with col_sample1:
        if st.button("📊 BSC Implementation Roadmap", type="secondary"):
            st.session_state['custom_prompt'] = """Create a comprehensive 12-month BSC implementation roadmap for a mid-size technology company transitioning from traditional performance management.

Current State:
- Annual performance reviews only
- Department-specific goals with limited alignment
- Basic financial KPIs with minimal operational metrics
- 200 employees across 5 departments
- Growth stage company expanding rapidly

Implementation Requirements:
- Executive leadership buy-in and training
- Manager capability development
- Employee engagement and communication
- Technology platform selection and deployment
- Change management and cultural transformation

Deliverables:
- Phase-by-phase implementation plan with timelines
- Stakeholder engagement and communication strategy
- Training and development curriculum
- Success metrics and progress tracking framework
- Risk mitigation and contingency planning"""
    
    with col_sample2:
        if st.button("🎯 OKR Integration Framework", type="secondary"):
            st.session_state['custom_prompt'] = """Design an integrated framework that combines Balanced Scorecard strategic planning with OKR execution methodology.

Integration Objectives:
- Leverage BSC for strategic direction and long-term planning
- Use OKRs for quarterly execution and agile goal management
- Ensure seamless alignment between strategic and operational levels
- Maintain measurement consistency and avoid metric confusion

Framework Components:
- BSC-OKR alignment methodology and translation process
- Quarterly OKR setting process based on annual BSC objectives
- Integrated performance dashboard and reporting system
- Manager training on dual framework management
- Employee guidance on navigating both systems effectively"""
    
    st.markdown("---")
    
    # Custom prompt input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💭 Your Custom BSC/Goal Setting Request")
        custom_prompt = st.text_area(
            "Enter your BSC, strategic alignment, or goal management request:",
            height=250,
            value=st.session_state.get('custom_prompt', ''),
            placeholder="""Examples:
• Create a BSC cascade methodology for multi-level organizations
• Design a goal calibration process to ensure fairness across teams
• Develop a strategic planning workshop agenda for department heads
• Build a performance dashboard framework for executive leadership
• Create a goal-setting training curriculum for new managers
• Design a strategic review meeting template for quarterly business reviews
• Develop a goal achievement recognition and rewards program
• Create a change management plan for BSC implementation"""
        )
        
        # Context options
        st.subheader("🎯 Context & Customization")
        col_context1, col_context2 = st.columns(2)
        
        with col_context1:
            company_context = st.selectbox(
                "Organization Type",
                ["Technology Company", "Financial Services", "Healthcare", "Manufacturing", "Retail", "Professional Services", "Non-profit", "Government", "Startup", "Enterprise", "Custom"],
                index=0
            )
            
            if company_context == "Custom":
                custom_company = st.text_input("Enter your organization context:")
                company_context = custom_company
            
            tool_type = st.selectbox(
                "Tool Type",
                ["Strategic Framework", "Implementation Plan", "Training Program", "Communication Strategy", "Measurement System", "Process Design", "Other"]
            )
        
        with col_context2:
            detail_level = st.selectbox(
                "Detail Level",
                ["Comprehensive (Executive-ready)", "Standard (Manager-level)", "Overview (High-level)"]
            )
            
            target_users = st.multiselect(
                "Target Users",
                ["Executive Leadership", "Senior Managers", "Middle Managers", "Team Leaders", "HR Team", "Strategy Team", "All Employees"],
                default=["Senior Managers", "HR Team"]
            )
    
    with col2:
        st.subheader("🚀 Generate Content")
        
        if st.button("🎨 Generate Custom BSC Tool", type="primary"):
            if custom_prompt.strip():
                enhanced_prompt = f"""
                Organization Context: {company_context}
                Tool Type: {tool_type}
                Target Users: {', '.join(target_users)}
                Detail Level: {detail_level}
                
                BSC/Strategic Alignment Request: {custom_prompt}
                
                Create world-class strategic performance management content that:
                1. Leverages proven BSC and strategic alignment methodologies
                2. Is specific to the organization context and industry
                3. Addresses the needs of the target user group
                4. Provides the appropriate level of detail for decision-making
                5. Is immediately implementable with clear action steps
                6. Includes relevant frameworks, processes, and best practices
                7. Focuses on measurable business outcomes and strategic impact
                8. Incorporates change management and adoption considerations
                
                If this is a framework, ensure comprehensive coverage of all BSC perspectives.
                If this is an implementation plan, include phases, timelines, and success metrics.
                If this is a training program, ensure practical application and skill development.
                If this is a measurement system, include KPIs, dashboards, and reporting.
                
                Generate executive-quality content that drives strategic alignment and organizational performance.
                """
                
                with st.spinner("Creating your custom BSC tool..."):
                    content = generate_content(enhanced_prompt, "Custom BSC Tool")
                    if content:
                        st.session_state.generated_content['custom_bsc'] = content
            else:
                st.error("Please enter your BSC/goal setting request")
        
        # Additional options
        st.markdown("---")
        st.subheader("📋 Quick Actions")
        
        if st.button("🔄 Clear Form"):
            st.session_state['custom_prompt'] = ''
            if 'custom_bsc' in st.session_state.generated_content:
                del st.session_state.generated_content['custom_bsc']
            st.rerun()
        
        if st.button("💡 Get Ideas"):
            st.session_state['custom_prompt'] = """Suggest 10 innovative BSC and strategic alignment initiatives for modern organizations:

1. AI-powered goal recommendation system based on historical performance and market trends
2. Real-time strategic dashboard with predictive analytics and early warning indicators
3. Cross-functional goal collaboration platform for matrix organizations
4. Dynamic goal adjustment framework for volatile business environments
5. Behavioral economics-based goal setting methodology for improved motivation
6. Integrated ESG (Environmental, Social, Governance) metrics within BSC framework
7. Agile BSC methodology combining strategic planning with quarterly adaptation
8. Peer-to-peer goal calibration and feedback system for fairness and transparency
9. Strategic storytelling framework for communicating BSC vision and goals
10. Gamification and social recognition platform for goal achievement

For each initiative, provide implementation approach, technology requirements, expected benefits, and success metrics."""
    
    # Display generated content
    if 'custom_bsc' in st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 Generated Custom BSC Tool")
        cleaned_content = clean_text(st.session_state.generated_content['custom_bsc'])
        st.text_area("Custom BSC Tool Content", value=cleaned_content, height=500)
        create_download_button(cleaned_content, f"Custom_BSC_Tool_{datetime.now().strftime('%Y%m%d_%H%M')}", "📥 Download BSC Tool")

# Footer
st.markdown("---")
st.markdown("### 🚀 Strategic Performance Excellence")
st.info("Transform your organization's performance through strategic alignment and balanced scorecard methodology. Continue exploring other HR modules for comprehensive talent management.")

# Instructions
with st.expander("📖 How to Use This BSC Alignment & Goal Setting Module"):
    st.markdown("""
    ## 🎯 **Core Features:**
    1. **🎯 SMART Goals Generator** - Create strategically aligned SMART goals with BSC integration
    2. **📊 BSC Performance Framework** - Develop comprehensive Balanced Scorecard systems
    3. **📈 Goal Cascading System** - Design systematic goal alignment from strategy to execution
    4. **📋 Performance Review Templates** - Build goal-focused performance evaluation systems
    5. **📧 Goal Management Communications** - Create strategic communications for goal processes
    6. **🎨 Custom BSC Tools** - Generate any strategic alignment or BSC-related framework
    
    ## 🎨 **Best Practices:**
    - **Strategic Alignment** - Ensure all goals connect to organizational strategy
    - **Balanced Perspectives** - Include financial, customer, process, and learning goals
    - **Cascading Methodology** - Create clear line of sight from corporate to individual
    - **Measurement Focus** - Emphasize quantifiable outcomes and KPIs
    - **Continuous Improvement** - Build in regular review and adjustment processes
    - **Change Management** - Consider adoption and cultural transformation needs
    
    **Tips:**
    - Use sample buttons to explore different BSC applications
    - Focus on measurable business outcomes and strategic impact
    - Ensure clear accountability and ownership at all levels
    - Integrate performance management with strategic planning cycles
    - Leverage technology for real-time tracking and reporting
    """)

# Navigation
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("← Module 4: Performance Management", key="nav_prev_bsc"):
        st.switch_page("pages/04_performance_management.py")

with col_nav2:
    if st.button("🏠 Back to Main Menu"):
        st.switch_page("pages/00_home.py")

with col_nav3:
    if st.button("Module 6: Employee Relations →", key="nav_next_bsc", disabled=True):
        st.info("Coming Soon!")