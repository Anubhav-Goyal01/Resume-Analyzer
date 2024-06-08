prompt = """
You have been tasked with building a resume parser that can extract information from resumes and convert it into a structured format.
Given the text of a resume, extract and format the information into a structured JSON object. The JSON should include details such as name, contact information, education, work experience, projects, and skills.

Review the resume carefully and spot for dates carefully. The dates should be in the format of YYYY-MM-DD. If the date is not available, you can leave it as an empty string in the output JSON. In case where the date is not in this format, you can convert it to the required format.

Here is the required format for the output:
{
  "Name": "<name>",
  "Contact": {
    "Email": "<email>",
    "Phone": "<number>",
    "LinkedIn": "<linkedin_url>",
    "Github": "<github_url>"
},
  "Education": {
    "Field": "<field_of_study>",
    "Institution": "<institution_name>",
    "CGPA": "<cgpa>",
    "StartDate": "<start_date>",
    "EndDate": "<end_date>"
  },
  "Experience": [
    {
      "Role": "<job_title>",
      "Company": "<company_name>",
      "Location": "<location>",
      "StartDate": "<start_date>",
      "EndDate": "<end_date>",
      "Description": "<brief_description_of_responsibilities>"
    }
    // Include additional entries as needed
  ],
  "Projects": [
    {
      "Name": "<project_name>",
      "Technologies": ["<technology_1>", "<technology_2>", "<technology_3>"],
      "Link": "<project_link>",
      "Description": "<brief_description_of_the_project>"
    }
    // Include additional entries as needed
  ],
  "Skills": ["<skill_1>", "<skill_2>", "<skill_3>", ...],
  "Certifications": [
    {
      "Name": "<certification_name>",
      "Link": "<certificate_link>",
      "Date": "<date_of_completion>"
    }
    // Include additional entries as needed
  ]
}


In case you are not able to identify a particular key, you can leave it as an empty string. For example, if the resume does not contain a LinkedIn URL, you can leave it as an empty string in the output JSON.

"""