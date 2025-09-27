import streamlit as st
from parser import extract_text_from_pdf, extract_text_from_txt
from scorer import score_resume, generate_suggestions

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 Resume Analyzer")
st.markdown("Upload your resume and job description to get a compatibility score and suggestions!")

col1, col2 = st.columns(2)

with col1:
    st.header("📋 Resume")
    resume_file = st.file_uploader("Upload Resume", type=['pdf', 'txt'])
    
    if resume_file:
        if resume_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = extract_text_from_txt(resume_file)
        
        st.text_area("Resume Content", resume_text[:500] + "...", height=200)

with col2:
    st.header("💼 Job Description")
    job_text = st.text_area("Paste Job Description", height=200, placeholder="Paste the job description here...")

if st.button("🔍 Analyze Resume", type="primary"):
    if resume_file and job_text:
        with st.spinner("Analyzing..."):
            # Get resume text
            if resume_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(resume_file)
            else:
                resume_text = extract_text_from_txt(resume_file)
            
            # Score the resume
            score_data = score_resume(resume_text, job_text)
            suggestions = generate_suggestions(score_data)
            
            st.success("Analysis Complete!")
            
            # Display results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Overall Score", f"{score_data['overall_score']}%")
            with col2:
                st.metric("Content Similarity", f"{score_data['similarity_score']}%")
            with col3:
                st.metric("Skill Match", f"{score_data['skill_match_score']}%")
            
            # Skills analysis
            st.subheader("🎯 Skills Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Your Skills:**")
                if score_data['resume_skills']:
                    for skill in score_data['resume_skills']:
                        st.write(f"✅ {skill}")
                else:
                    st.write("No skills detected")
            
            with col2:
                st.write("**Required Skills:**")
                if score_data['job_skills']:
                    for skill in score_data['job_skills']:
                        if skill in score_data['matching_skills']:
                            st.write(f"✅ {skill}")
                        else:
                            st.write(f"❌ {skill}")
                else:
                    st.write("No skills detected in job description")
            
            # Suggestions
            st.subheader("💡 Suggestions")
            for suggestion in suggestions:
                st.write(f"• {suggestion}")
    
    else:
        st.error("Please upload a resume and enter a job description!")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")