import streamlit as st
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1 {
        color: #4F46E5;
        font-weight: 800;
    }

    h2, h3 {
        font-weight: 700;
    }

    div[data-testid="stMetric"] {
        background-color: rgba(79, 70, 229, 0.08);
        border: 1px solid rgba(79, 70, 229, 0.25);
        padding: 18px;
        border-radius: 12px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }
</style>
""", unsafe_allow_html=True)
import pandas as pd 

from resume_parser import extract_resume_text
from analyzer import analyze_resume


# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Application title
st.title("📄 AI Resume Analyzer")

st.markdown(
    "### Smart Resume Screening & Job Description Matching"
)

st.caption(
    "Upload your resume, compare your skills with a job description, "
    "and discover opportunities to improve."
)

st.divider()
st.write(
    "Upload your resume and compare your skills "
    "with a job description."
)

st.divider()

# Sidebar
with st.sidebar:
    st.header("About")
    st.write(
        "This tool extracts resume text, identifies skills, "
        "and estimates similarity to a job description."
    )
    st.caption("The match score is an estimate, not an official ATS score.")

with st.sidebar:
    st.header("📋 Resume Inputs")

    # Resume upload
    st.subheader("1. Upload Your Resume")

    uploaded_file = st.file_uploader(
        "Choose your resume (PDF format)",
        type=["pdf"]
    )

    # Job description
    st.subheader("2. Enter the Job Description")

    job_description = st.text_area(
        "Paste the complete job description here",
        height=220,
        placeholder=(
            "Example: We are looking for a Data Analyst "
            "with Python, SQL, Excel, and Power BI skills..."
        )
    )

# Analyze button
if st.button("Analyze Resume", type="primary"):

    if uploaded_file is None:
        st.error("Please upload a PDF resume first.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        with st.spinner("Analyzing your resume..."):

            resume_text = extract_resume_text(uploaded_file)

            if not resume_text:
                st.error(
                    "No text was extracted. Try a text-based PDF "
                    "rather than a scanned image PDF."
                )

            elif resume_text.startswith("Error reading PDF:"):
                st.error(resume_text)

            else:
                results = analyze_resume(
                    resume_text,
                    job_description
                )

                st.success("Resume analysis completed!")

                st.divider()
                st.header("3. Analysis Results")

                # Match score
                st.metric(
                    "Text Similarity Score",
                    f"{results['match_score']}%"
                )

                st.progress(
                    min(results["match_score"] / 100, 1.0)
                )

                st.caption(
                    "This score measures text similarity only. "
                    "It does not predict hiring decisions."
                )

                # Skills summary
                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Resume Skills",
                    len(results["resume_skills"])
                )

                col2.metric(
                    "Matched Skills",
                    len(results["matched_skills"])
                )

                col3.metric(
                    "Missing Skills",
                    len(results["missing_skills"])
                )

                st.divider()

                # Skills comparison chart
                st.subheader("📊 Skills Match Overview")

                chart_data = pd.DataFrame({
                    "Category": ["Matched Skills", "Missing Skills"],
                    "Count": [
                        len(results["matched_skills"]),
                        len(results["missing_skills"])
                    ]
                })

                st.bar_chart(
                    chart_data.set_index("Category")
                )
                # Matched skills
                st.subheader("✅ Matched Skills")

                if results["matched_skills"]:
                    st.write(
                        ", ".join(results["matched_skills"])
                    )
                else:
                    st.info("No matching skills were detected.")

                # Missing skills
                st.subheader("📌 Skills to Consider Developing")
                st.subheader("💡 Resume Improvement Suggestions")

                if results["suggestions"]:
                    for suggestion in results["suggestions"]:
                        st.write("- " + suggestion)
                else:
                    st.success(
                        "All detected job-description skills "
                        "are present in your resume!"
                    )

                if results["missing_skills"]:
                    st.write(
                        ", ".join(results["missing_skills"])
                    )
                else:
                    st.write(
                        "All detected job-description skills "
                        "were found in the resume."
                    )

                # All resume skills
                st.subheader("🧠 Skills Found in Your Resume")

                if results["resume_skills"]:
                    st.write(
                        ", ".join(results["resume_skills"])
                    )
                else:
                    st.info(
                        "No skills from the current skill list "
                        "were detected."
                    )

                # Extracted text preview
                with st.expander("View Extracted Resume Text"):
                    st.text(resume_text)

                # Downloadable report
                report = f"""
AI RESUME ANALYZER REPORT

Text Similarity Score: {results['match_score']}%

Resume Skills:
{', '.join(results['resume_skills'])}

Matched Skills:
{', '.join(results['matched_skills'])}

Missing Skills:
{', '.join(results['missing_skills'])}
"""

                st.download_button(
                    label="Download Analysis Report",
                    data=report,
                    file_name="resume_analysis.txt",
                    mime="text/plain"
                )