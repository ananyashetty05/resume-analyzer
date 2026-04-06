import streamlit as st

from parser import extract_text_from_pdf, extract_text_from_txt
from scorer import generate_detailed_feedback, generate_suggestions, score_resume

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI-Powered Resume Analyzer")
st.markdown("Get richer ATS, skills, impact, and AI-backed resume feedback in one place.")

try:
    from ai_analyzer import AIResumeAnalyzer

    analyzer = AIResumeAnalyzer()
    if analyzer.use_ai:
        st.success(f"🤖 Hugging Face AI Analysis: Enabled ({analyzer.model})")
    else:
        st.warning("🤖 Hugging Face AI Analysis: Disabled (add HUGGINGFACE_API_TOKEN to .env for enhanced analysis)")
except Exception:
    st.info("🤖 AI Analysis: Using fallback mode")

col1, col2 = st.columns(2)

with col1:
    st.header("📋 Resume")
    resume_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])

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
            if resume_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(resume_file)
            else:
                resume_text = extract_text_from_txt(resume_file)

            score_data = score_resume(resume_text, job_text)
            suggestions = generate_suggestions(score_data)
            detailed_feedback = generate_detailed_feedback(score_data)
            ai_analysis = score_data.get("ai_analysis", {})

            st.success("✅ Analysis Complete!")

            if ai_analysis.get("overall_assessment"):
                st.info(f"🤖 **AI Assessment:** {ai_analysis['overall_assessment']}")

            st.subheader("📊 Overall Assessment")
            row1 = st.columns(5)
            metrics_row1 = [
                ("Overall Score", f"{score_data['overall_score']}%"),
                ("Content Match", f"{score_data['similarity_score']}%"),
                ("Skill Match", f"{score_data['skill_match_score']}%"),
                ("Experience Match", f"{score_data['experience_match']}%"),
                ("ATS Score", f"{score_data['ats_score']}%"),
            ]
            for column, (label, value) in zip(row1, metrics_row1):
                with column:
                    st.metric(label, value)

            row2 = st.columns(5)
            metrics_row2 = [
                ("Keyword Coverage", f"{score_data['keyword_coverage_score']}%"),
                ("Contact Completeness", f"{score_data['contact_score']}%"),
                ("Interview Readiness", f"{score_data['interview_readiness']}%"),
                ("Leadership Signal", f"{score_data['leadership_score']}%"),
                ("Quantified Wins", score_data["quantified_achievement_count"]),
            ]
            for column, (label, value) in zip(row2, metrics_row2):
                with column:
                    st.metric(label, value)

            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                "🎯 Skills Analysis",
                "🔑 Keywords",
                "📝 Sections",
                "📈 Impact Signals",
                "🤖 AI Insights",
                "💡 Suggestions",
                "📋 Action Plan",
            ])

            with tab1:
                st.subheader("Comprehensive Skills Analysis")
                total_skills = len(score_data["matching_skills"]) + len(score_data["missing_skills"])
                skill_match_pct = len(score_data["matching_skills"]) / max(total_skills, 1) * 100
                st.progress(skill_match_pct / 100)
                st.write(f"**Skills Match: {skill_match_pct:.1f}%** ({len(score_data['matching_skills'])} of {max(total_skills, 1)} required skills)")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("**✅ Matching Skills**")
                    if score_data["matching_skills"]:
                        for skill in score_data["matching_skills"]:
                            st.success(f"✓ {skill.title()}")
                    else:
                        st.info("No matching skills found")

                with col2:
                    st.write("**❌ Critical Missing Skills**")
                    critical_missing = ai_analysis.get("missing_critical_skills", [])
                    if critical_missing:
                        for skill in critical_missing[:6]:
                            st.error(f"✗ {skill.title()} (Critical)")
                    other_missing = [skill for skill in score_data["missing_skills"] if skill not in critical_missing][:4]
                    for skill in other_missing:
                        st.warning(f"✗ {skill.title()}")
                    if not critical_missing and not other_missing:
                        st.success("All required skills present")

                with col3:
                    st.write("**📊 Your Current Skills**")
                    if score_data["resume_skills"]:
                        for skill in score_data["resume_skills"][:8]:
                            if skill in score_data["matching_skills"]:
                                st.success(f"✓ {skill.title()} (Matches job)")
                            else:
                                st.info(f"• {skill.title()}")
                    else:
                        st.warning("No skills detected")

                nice_to_have = ai_analysis.get("missing_nice_to_have_skills", [])
                if nice_to_have:
                    st.write("**💡 Nice-to-Have Skills**")
                    for skill in nice_to_have[:6]:
                        st.info(f"+ {skill.title()}")

            with tab2:
                st.subheader("Keyword Analysis")
                col1, col2 = st.columns(2)

                with col1:
                    st.write("**🎯 Job Keywords**")
                    for keyword in score_data["job_keywords"][:10]:
                        if keyword in score_data["matching_keywords"]:
                            st.success(f"✓ {keyword}")
                        else:
                            st.error(f"✗ {keyword}")

                with col2:
                    st.write("**📝 Missing Keywords to Add**")
                    if score_data["missing_keywords"]:
                        for keyword in score_data["missing_keywords"][:8]:
                            st.warning(f"+ {keyword}")
                    else:
                        st.success("Great keyword coverage")

            with tab3:
                st.subheader("Resume Structure Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**✅ Present Sections**")
                    for section in score_data["found_sections"]:
                        st.success(f"✓ {section.title()}")

                with col2:
                    st.write("**❌ Missing Sections**")
                    if score_data["missing_sections"]:
                        for section in score_data["missing_sections"]:
                            st.error(f"✗ {section.title()}")
                    else:
                        st.success("All key sections present")

                if score_data["weak_words"]:
                    st.write("**🔄 Words to Strengthen**")
                    for weak, strong in score_data["weak_words"][:5]:
                        st.warning(f"Replace '{weak}' -> '{strong}'")

            with tab4:
                st.subheader("Impact and Readiness Signals")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("**📊 Achievement Strength**")
                    st.info(f"Quantified achievements found: {score_data['quantified_achievement_count']}")
                    st.info(f"Estimated experience referenced: {score_data['estimated_experience_years']} years")
                with col2:
                    st.write("**🤝 Professional Signals**")
                    st.success(f"Leadership: {score_data['leadership_score']}%")
                    st.success(f"Collaboration: {score_data['collaboration_score']}%")
                    st.success(f"Project Depth: {score_data['project_score']}%")
                with col3:
                    st.write("**📇 Contact Completeness**")
                    for label, present in score_data["contact_details"].items():
                        if present:
                            st.success(f"✓ {label.title()}")
                        else:
                            st.error(f"✗ {label.title()}")

            with tab5:
                st.subheader("🤖 AI-Powered Insights")
                col1, col2 = st.columns(2)

                with col1:
                    st.write("**💪 AI-Detected Strengths**")
                    for strength in ai_analysis.get("strengths", []):
                        st.success(f"✓ {strength}")

                    st.write("**🎯 Specific Improvements**")
                    for improvement in ai_analysis.get("specific_improvements", []):
                        st.warning(f"🔧 {improvement}")

                with col2:
                    st.write("**⚠️ AI-Detected Weaknesses**")
                    for weakness in ai_analysis.get("weaknesses", []):
                        st.error(f"✗ {weakness}")

                    st.write("**📝 ATS Recommendations**")
                    for rec in ai_analysis.get("ats_recommendations", []):
                        st.info(f"📝 {rec}")

                st.write("**💪 Recommended Action Verbs**")
                action_verbs = ai_analysis.get("action_verbs_to_use", [])
                if action_verbs:
                    for verb in action_verbs[:8]:
                        st.success(f"• {verb}")

                quantifiable = ai_analysis.get("quantifiable_achievements", "")
                if quantifiable:
                    st.info(f"📊 **Quantifiable Achievements:** {quantifiable}")

                if ai_analysis.get("role_fit_summary"):
                    st.write("**🎯 Role Fit Summary**")
                    st.info(ai_analysis["role_fit_summary"])

                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Seniority Alignment:** {ai_analysis.get('seniority_alignment', 'mixed')}")
                with col2:
                    st.write(f"**Industry Alignment:** {ai_analysis.get('industry_alignment', 'General')}")

                top_highlights = ai_analysis.get("top_resume_highlights", [])
                if top_highlights:
                    st.write("**🌟 Top Resume Highlights**")
                    for item in top_highlights:
                        st.success(f"• {item}")

            with tab6:
                st.subheader("Prioritized Suggestions")
                for suggestion in suggestions["critical"]:
                    st.error(f"🚨 {suggestion}")
                for suggestion in suggestions["important"]:
                    st.warning(f"⚠️ {suggestion}")
                for suggestion in suggestions["optional"]:
                    st.info(f"💡 {suggestion}")

            with tab7:
                st.subheader("Action Plan")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**➕ Content to Add**")
                    for addition in ai_analysis.get("content_to_add", detailed_feedback["additions"]):
                        st.success(f"+ {addition}")
                    st.write("**💪 Strengths to Highlight**")
                    for strength in detailed_feedback["strengths"]:
                        st.info(f"✓ {strength}")
                with col2:
                    st.write("**➖ Content to Remove or Improve**")
                    for removal in ai_analysis.get("content_to_remove", detailed_feedback["removals"]):
                        st.warning(f"- {removal}")
                    st.write("**🔧 Areas for Improvement**")
                    for improvement in detailed_feedback["improvements"]:
                        st.error(f"🔧 {improvement}")
    else:
        st.error("⚠️ Please upload a resume and enter a job description to begin analysis!")

st.markdown("---")
st.markdown("**💡 Pro Tips:**")
st.markdown("• Use keywords from the job description naturally in your resume")
st.markdown("• Quantify achievements with numbers and percentages")
st.markdown("• Tailor your resume for each specific job application")
st.markdown("• Add a Hugging Face token in `.env` to enable AI analysis")

with st.expander("🔧 Setup AI Analysis"):
    st.markdown("""
**To enable AI-powered analysis:**
1. Create a `.env` file in the project root
2. Add: `HUGGINGFACE_API_TOKEN=your-token-here`
3. Optionally add: `HF_MODEL=mistralai/Mistral-7B-Instruct-v0.3`
4. Restart the application

Without AI, the app still provides NLP-based analysis and scoring.
""")

st.markdown("---")
st.markdown("Built with Streamlit, NLP, and Hugging Face AI")
