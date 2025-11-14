import streamlit as st
from parser import extract_text_from_pdf, extract_text_from_txt
from scorer import score_resume, generate_suggestions, generate_detailed_feedback

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI-Powered Resume Analyzer")
st.markdown("Get comprehensive feedback on your resume with AI-powered analysis!")

col1, col2 = st.columns(2)

with col1:
    st.header("📋 Resume")
    resume_file = st.file_uploader("Upload Resume", type=['pdf', 'txt'])
    
    if resume_file:
        if resume_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = extract_text_from_txt(resume_file)
        
        st.text_area("Resume Content Preview", resume_text[:500] + "...", height=200)

with col2:
    st.header("💼 Job Description")
    job_text = st.text_area("Paste Job Description", height=200, placeholder="Paste the complete job description here...")

if st.button("🔍 Analyze Resume", type="primary"):
    if resume_file and job_text:
        with st.spinner("Performing comprehensive analysis..."):
            # Get resume text
            if resume_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(resume_file)
            else:
                resume_text = extract_text_from_txt(resume_file)
            
            # Score the resume
            score_data = score_resume(resume_text, job_text)
            suggestions = generate_suggestions(score_data)
            detailed_feedback = generate_detailed_feedback(score_data)
            
            st.success("✅ Analysis Complete!")
            
            # Display AI Assessment
            ai_analysis = score_data.get('ai_analysis', {})
            if ai_analysis.get('overall_assessment'):
                st.info(f"🤖 **AI Assessment:** {ai_analysis['overall_assessment']}")
            
            # Display main scores
            st.subheader("📊 Overall Assessment")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                score_color = "green" if score_data['overall_score'] >= 70 else "orange" if score_data['overall_score'] >= 50 else "red"
                st.metric("Overall Score", f"{score_data['overall_score']}%")
            with col2:
                st.metric("Content Match", f"{score_data['similarity_score']}%")
            with col3:
                st.metric("Skill Match", f"{score_data['skill_match_score']}%")
            with col4:
                st.metric("Experience Match", f"{score_data['experience_match']}%")
            with col5:
                st.metric("ATS Score", f"{score_data['ats_score']}%")
            
            # Detailed Analysis Tabs
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🎯 Skills Analysis", "🔑 Keywords", "📝 Sections", "🤖 AI Insights", "💡 Suggestions", "📋 Action Plan"])
            
            with tab1:
                st.subheader("Comprehensive Skills Analysis")
                
                # Skills match percentage
                skill_match_pct = len(score_data['matching_skills']) / max(len(score_data['matching_skills']) + len(score_data['missing_skills']), 1) * 100
                st.progress(skill_match_pct / 100)
                st.write(f"**Skills Match: {skill_match_pct:.1f}%** ({len(score_data['matching_skills'])} of {len(score_data['matching_skills']) + len(score_data['missing_skills'])} required skills)")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**✅ Matching Skills**")
                    if score_data['matching_skills']:
                        for skill in score_data['matching_skills']:
                            st.success(f"✓ {skill.title()}")
                        st.write(f"**Total: {len(score_data['matching_skills'])} skills**")
                    else:
                        st.info("No matching skills found")
                
                with col2:
                    st.write("**❌ Critical Missing Skills**")
                    critical_missing = ai_analysis.get('missing_critical_skills', [])
                    if critical_missing:
                        for skill in critical_missing[:6]:
                            st.error(f"✗ {skill.title()} (Critical)")
                    
                    other_missing = [s for s in score_data['missing_skills'] if s not in critical_missing][:4]
                    if other_missing:
                        st.write("**Other Missing:**")
                        for skill in other_missing:
                            st.warning(f"✗ {skill.title()}")
                    
                    if not critical_missing and not other_missing:
                        st.success("All required skills present!")
                
                with col3:
                    st.write("**📊 Your Current Skills**")
                    if score_data['resume_skills']:
                        for skill in score_data['resume_skills'][:8]:
                            if skill in score_data['matching_skills']:
                                st.success(f"✓ {skill.title()} (Matches job)")
                            else:
                                st.info(f"• {skill.title()}")
                        if len(score_data['resume_skills']) > 8:
                            st.write(f"... and {len(score_data['resume_skills']) - 8} more")
                    else:
                        st.warning("No skills detected")
                
                # Nice to have skills
                nice_to_have = ai_analysis.get('missing_nice_to_have_skills', [])
                if nice_to_have:
                    st.write("**💡 Nice-to-Have Skills (Bonus Points)**")
                    cols = st.columns(3)
                    for i, skill in enumerate(nice_to_have[:6]):
                        with cols[i % 3]:
                            st.info(f"+ {skill.title()}")
            
            with tab2:
                st.subheader("Keyword Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🎯 Job Keywords (Top Priority)**")
                    for keyword in score_data['job_keywords'][:10]:
                        if keyword in score_data['matching_keywords']:
                            st.success(f"✓ {keyword}")
                        else:
                            st.error(f"✗ {keyword}")
                
                with col2:
                    st.write("**📝 Missing Keywords to Add**")
                    if score_data['missing_keywords']:
                        for keyword in score_data['missing_keywords'][:8]:
                            st.warning(f"+ {keyword}")
                    else:
                        st.success("Great keyword coverage!")
            
            with tab3:
                st.subheader("Resume Structure Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**✅ Present Sections**")
                    for section in score_data['found_sections']:
                        st.success(f"✓ {section.title()}")
                
                with col2:
                    st.write("**❌ Missing Sections**")
                    if score_data['missing_sections']:
                        for section in score_data['missing_sections']:
                            st.error(f"✗ {section.title()}")
                    else:
                        st.success("All key sections present!")
                
                if score_data['weak_words']:
                    st.write("**🔄 Words to Strengthen**")
                    for weak, strong in score_data['weak_words'][:5]:
                        st.warning(f"Replace '{weak}' → '{strong}'")
            
            with tab4:
                st.subheader("🤖 AI-Powered Insights")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**💪 AI-Detected Strengths**")
                    ai_strengths = ai_analysis.get('strengths', [])
                    if ai_strengths:
                        for strength in ai_strengths:
                            st.success(f"✓ {strength}")
                    else:
                        st.info("Enable AI analysis for detailed insights")
                    
                    st.write("**🎯 Specific Improvements**")
                    specific_improvements = ai_analysis.get('specific_improvements', [])
                    for improvement in specific_improvements:
                        st.warning(f"🔧 {improvement}")
                
                with col2:
                    st.write("**⚠️ AI-Detected Weaknesses**")
                    ai_weaknesses = ai_analysis.get('weaknesses', [])
                    for weakness in ai_weaknesses:
                        st.error(f"✗ {weakness}")
                    
                    st.write("**📝 ATS Recommendations**")
                    ats_recommendations = ai_analysis.get('ats_recommendations', [])
                    for rec in ats_recommendations:
                        st.info(f"📝 {rec}")
                
                # Action verbs and achievements
                st.write("**💪 Recommended Action Verbs**")
                action_verbs = ai_analysis.get('action_verbs_to_use', [])
                if action_verbs:
                    verb_cols = st.columns(4)
                    for i, verb in enumerate(action_verbs[:8]):
                        with verb_cols[i % 4]:
                            st.success(f"• {verb}")
                
                quantifiable = ai_analysis.get('quantifiable_achievements', '')
                if quantifiable:
                    st.info(f"📊 **Quantifiable Achievements:** {quantifiable}")
            
            with tab5:
                st.subheader("Prioritized Suggestions")
                
                if suggestions['critical']:
                    st.write("**🚨 Critical (Fix Immediately)**")
                    for suggestion in suggestions['critical']:
                        st.error(f"🚨 {suggestion}")
                
                if suggestions['important']:
                    st.write("**⚠️ Important (High Impact)**")
                    for suggestion in suggestions['important']:
                        st.warning(f"⚠️ {suggestion}")
                
                if suggestions['optional']:
                    st.write("**💡 Optional (Nice to Have)**")
                    for suggestion in suggestions['optional']:
                        st.info(f"💡 {suggestion}")
            
            with tab6:
                st.subheader("📋 Action Plan")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**➕ Content to Add**")
                    content_to_add = ai_analysis.get('content_to_add', detailed_feedback['additions'])
                    for addition in content_to_add:
                        st.success(f"+ {addition}")
                    
                    st.write("**💪 Strengths to Highlight**")
                    for strength in detailed_feedback['strengths']:
                        st.info(f"✓ {strength}")
                
                with col2:
                    st.write("**➖ Content to Remove/Improve**")
                    content_to_remove = ai_analysis.get('content_to_remove', detailed_feedback['removals'])
                    for removal in content_to_remove:
                        st.warning(f"- {removal}")
                    
                    st.write("**🔧 Areas for Improvement**")
                    for improvement in detailed_feedback['improvements']:
                        st.error(f"🔧 {improvement}")
    
    else:
        st.error("⚠️ Please upload a resume and enter a job description to begin analysis!")

st.markdown("---")
st.markdown("**💡 Pro Tips:**")
st.markdown("• Use keywords from the job description naturally in your resume")
st.markdown("• Quantify achievements with numbers and percentages")
st.markdown("• Tailor your resume for each specific job application")
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & AI")