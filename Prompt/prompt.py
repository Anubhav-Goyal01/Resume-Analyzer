prompt = """
You have been tasked with building a resume parser that can extract information from resumes and convert it into a structured format.
Given the text of a resume, extract and format the information into a structured JSON object. The JSON should include details such as name, contact information, education, work experience, projects, and skills.

Review the resume carefully and spot for dates carefully. The dates should be in the format of YYYY-MM-DD. If the date is not available, you can leave it as an empty string in the output JSON. In case where the date is not in this format, you can convert it to the required format.

Here is the required format for the output:

Degree
University Name
Specialization
Start date
End date (or expected)
Grade type
Grades


{
  "Name": "<name>",
  "Contact": {
    "Email": "<email>",
    "Phone": "<number>",
    "LinkedIn": "<linkedin_url>",
    "Github": "<github_url>"
},
  "Education": {
    "Degree": "<degree>",
    "University Name": "<university_name>",
    "Specialization": "<specialization>",
    "Start Date": "<start_date>",
    "End Date": "<end_date>"
    "GradeType": "<grade_type>",
    "Grades": "<grade>",
  },
  "Experience": [
    {
      "Your Designation": "<job_title>",
      "Company Name": "<company_name>",
      "Company Location": "<location>",
      "Industry Type": "<industry_type>",
      "Start Date": "<start_date>",
      "EndDate": "<end_date>",
      "Description": "<brief_description_of_responsibilities>"
    }
    // Include additional entries as needed
  ],
  "Projects": [
    {
      "Project Name": "<project_name>",
      "Technologies": ["<technology_1>", "<technology_2>", "<technology_3>"],
      "Project Url": "<project_link>",
      "Description": "<brief_description_of_the_project>"
    }
    // Include additional entries as needed
  ],
  "Skills": ["<skill_1>", "<skill_2>", "<skill_3>", ...],
  "Certifications": [
    {
      "Name": "<certification_name>",
      "Credential URL": "<certificate_link>",
      "Issue date": "<date_of_completion>"
    }
    // Include additional entries as needed
  ]
}


In case you are not able to identify a particular key, you can leave it as an empty string. For example, if the resume does not contain a LinkedIn URL, you can leave it as an empty string in the output JSON.

"""


rankingPrompt = """
You will be provided with JSON of resumes as well as the Job description. You need to rank the resumes based on the following criteria: 
1. Relevance to the job description
2. Quality of the resume
3. Experience and skills
4. Education and certifications
5. Overall presentation

You need to assign a score to each resume based on the above criteria. The score should be between 1 and 10, with 10 being the highest and 1 being the lowest. You can assign decimal values to the score as well.

Submit the scores for each resume in the following format:

{
  "scores": [
    {
      "resume_id": "<resume_id>",
      "score": <score>
    },
    {
      "resume_id": "<resume_id>",
      "score": <score>
    },
    Include additional entries as needed
  ]

The Scores should be in the range of 1 to 10. You can assign decimal values to the score as well.
Make Sure you dont assign the same score to multiple resumes. And do Relative marking.
"""

jobDescriptionPrompt = """
Job Description:

We are looking for a Backend Software Developer with experience in building web applications using modern technologies like React & NextJS as well as Python. The ideal candidate should have a strong background in computer science and software engineering principles. He should be proficient with Databases and Deployment. The candidate should be able to work independently and as part of a team to deliver high-quality software solutions.
"""