import streamlit as st
import pdfplumber
import re

st.title("AI Resume Analyzer")
st.caption("Upload your resume and get instant feedback")
role = st.selectbox("Select Role", [
    "Developer", "Data Analyst", "Web Developer",
    "ML Engineer", "CyberSecurity", "Android Developer", "Testing Engineer"
])

file = st.file_uploader("Upload your resume", type="pdf")
if file is not None:
    st.success("File uploaded successfully")

    # Extract text
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

    words = text.lower()

    # Role skills
    role_skills = {
        "Developer": ['python','java','c','sql'],
        "Data Analyst": ['python','sql','excel','powerbi'],
        "Web Developer": ['html','css','javascript','react'],
        "ML Engineer": ['python','machine learning','pandas'],
        "CyberSecurity": ["network security","cryptography","linux"],
        "Android Developer": ["java","kotlin","firebase"],
        "Testing Engineer": ["testing","selenium","automation testing"]
    }

    skills = role_skills.get(role, [])

    found = []
    missing = []
    attributes = ["skills", "projects", "education","internships"]

    for skill in skills:
        if skill in words:
            found.append(skill)
        else:
            missing.append(skill)
    role_score={}
    for r,skill_list in role_skills.items():
       match_count=0
       for skill in skill_list:
          if skill in words or skill in text.lower():
             match_count+=1
       role_score[r]=match_count
    if max(role_score.values())==0:
       st.warning("No matching skills found")
       best_role=None
    else:
       best_role=max(role_score,key=role_score.get)

    score = (len(found) / len(skills)) * 100

    # Display results
    st.subheader("Results")
    if len(found)==0:
       st.warning("No relevant skills found in resume")
    else:
       st.success(f"Detected Skills: {', '.join(found)}")
    st.error(f"Missing Skills: {', '.join(missing)}")
    st.metric("Resume Score" ,f"{score:.2f}%")
    st.progress(int(score))
    if score > 80:
      st.success("Excellent Resume 🎉")
    elif score > 60:
      st.info("Good Resume 👍")
    else:
      st.warning("Needs Improvement ⚠️")

    # Suggestions
    if missing:
        st.subheader("Suggestions")
        for skill in missing:
            st.write(f"- Add **{skill}** to strengthen your Resume better")

    for attr in attributes:
       if attr not in words:
          st.warning(f"Consider Adding **{attr}** section to your Resume")
    st.subheader("Recommended Role")
    if best_role and role_score[best_role]>0:
       st.success(f"Based on your resume ,you are best suited for: {best_role}")
    else:
       st.warning("Not enough skills detected to recommend a role")
    sorted_roles=sorted(role_score.items(),key=lambda x:x[1],reverse=True)
    st.subheader("Top Matching Roles:")
    for r,score_val in sorted_roles[:2]:
       st.write(f"{r} ({score_val} skills matched)")