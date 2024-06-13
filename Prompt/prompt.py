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
    "End Date": "<end_date>",
    "Grade Type": "<grade_type>",
    "Grades": "<grade>",
  },
  "Experience": [
    {
      "Your Designation": "<job_title>",
      "Company Name": "<company_name>",
      "Company Location": "<location>",
      "Industry Type": "<industry_type>",
      "Start Date": "<start_date>",
      "End Date": "<end_date>",
      "Description": "<brief_description_of_responsibilities>"
    },
    // Include additional entries as needed
  ],
  "Projects": [
    {
      "Project Name": "<project_name>",
      "Technologies": ["<technology_1>", "<technology_2>", "<technology_3>"],
      "Project Url": "<project_link>",
      "Description": "<brief_description_of_the_project>"
    },
    // Include additional entries as needed
  ],
  "Skills": ["<skill_1>", "<skill_2>", "<skill_3>", ...],
  "Certifications": [
    {
      "Name": "<certification_name>",
      "Credential URL": "<certificate_link>",
      "Issue date": "<date_of_completion>"
    },
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

We are looking for a seasoned Data Scientist to join our team. The ideal candidate will have experience working with large datasets and developing machine learning models. You will be responsible for analyzing data, identifying trends, and developing predictive models to drive business decisions. The candidate should have a strong background in statistics, mathematics, and programming. Experience with Python, Tensorflow or Pytorch, LLMS, GenerativeAI, MLOps is required. Knowledge of cloud platforms like AWS, Azure, or GCP is a plus. The candidate should have excellent communication skills and be able to present complex data in a clear and concise manner. A degree in Computer Science, Mathematics, or a related field is required. Certifications in Data Science or Machine Learning are a plus. Also the candidate should have experience in working with large datasets and developing machine learning models.
"""


ParsingCheckPrompt = """
You will be provided with a sample output of how a parsing should look like and you need to check if the parsing is correct or not. If the parsing is correct, you can approve it. If the parsing is incorrect, you can reject it. Output with a YES OR NO ONLY.

This is how the parsing should look like:
{
    "Name": "SHIV PRATAP SINGH",
    "Contact": {
        "Email": "shiv33852@gmail.com",
        "Phone": "+91-6386273931",
        "LinkedIn": "",
        "Github": ""
    },
    "Education": {
        "Degree": "Bachelor of Technology",
        "University Name": "ABES Engineering College",
        "Specialization": "Computer Science and Engineering",
        "Start Date": "2019-08-01",
        "End Date": "2023-07-31",
        "GradeType": "CGPA",
        "Grades": "8.0/10.0"
    },
    "Experience": [
        {
            "Your Designation": "Development Support Engineering Intern",
            "Company Name": "Amazon India",
            "Company Location": "Bangalore, Karnataka",
            "Industry Type": "",
            "Start Date": "2023-01-01",
            "EndDate": "2023-06-30",
            "Description": "- I designed and implemented a user-friendly and visually appealing dashboard that provided an overview of the code quality and health of all the team packages.\n- The dashboard included key metrics, such as code coverage, code duplication, and code smells, allowing for quick identification of areas that required improvement.\n- Tech Stack: Java, AWS: RDS, IAM, EC2, VPC, Amazon Route 53, AWS CloudFormation, Elastic Container Registry, Amazon Federate.\n\n- Removed unused dependencies and resolved major version conflicts to enhance project efficiency.\n- Implemented integration tests to identify and handle exceptions at the server end, ensuring robust error handling.\n- Invalid input is validated at server end. Developed validation filters to intercept incoming requests, enhancing data validation before processing. Utilized Java-based validation libraries and custom validation logic to validate input data comprehensively.\n- Tech Stack: Java, Testing.\n\n- Diligently identified critical bugs within the project's pipeline that were causing deployment failures.\n- Applied targeted code modifications to address these issues, ensuring that the project could progress smoothly through CI/CD pipeline.\n- Introduced automation scripts and processes to facilitate a seamless transition from manual deployments to full Continuous Delivery (CD).\n\n- Actively engaged in addressing Shepherd tickets, demonstrating a proactive approach to resolving critical issues that impacted the team's workflow and project progress.\n- Leveraged technical expertise in AWS services to develop and implement effective solutions for Shepherd ticket issues."
        },
        ...
    ],
    "Projects": [
        {
            "Project Name": "OBJECT DETECTION THROUGH LIVE WEB CAM | Deep Learning",
            "Technologies": [
                "Python",
                "OpenCV",
                "TensorFlow"
            ],
            "Project Url": "",
            "Description": "A Deep learning application for detecting common objects. Developed a computer vision project utilizing deep learning techniques to detect and track objects in real-time using a web camera. Implemented the project using Python, OpenCV, and TensorFlow. To make user friendly, users can also capture the image and detect all the objects present in that frame."
        },
        {
            "Project Name": "COVID-19 Data Analysis | Data Science",
            "Technologies": [
                "NumPy",
                "Pandas",
                "Matplotlib"
            ],
            "Project Url": "",
            "Description": "Conducted an in-depth analysis of COVID-19 data, focusing on state-wise, gender-wise, and age group-wise comparisons of cases. Leveraged NumPy and Pandas libraries for data manipulation and performed data visualization using matplotlib. Extracted valuable insights and trends from the data, helping to understand the impact of the pandemic at different levels."
        },
        ...
    ],
    "Skills": [
        "C",
        "C++",
        "Python",
        "HTML",
        "CSS",
        "JavaScript",
        "Data Science",
        "Machine Learning",
        "MySQL",
        "Postman",
        "Git",
        "Linux",
        "IntelliJ",
        "VS Code",
        "PyCharm",
        "React JS",
        "Redux",
        "Tailwind CSS",
        ...
    ],
    "Certifications": [
        {
            "Name": "Basics of Amazon CloudWatch",
            "Credential URL": "",
            "Issue date": ""
        },
        {
            "Name": "Amazon CloudWatch Dashboard",
            "Credential URL": "",
            "Issue date": ""
        },
        {
            "Name": "Open Source policy training",
            "Credential URL": "",
            "Issue date": ""
        }
        ...
    ]
}

NOTE THAT THIS IS JUST A SAMPLE EXAMPLE AND THE OUTPUT MAY VARY. BUT THE KEYS FOR THIS JSON SHOULD REMAIN THE SAME. SO YOU NEED TO SPOT FOR KEY ERRORS MAJORlY. AMOUNT OF CERTIFICATES, WORK EXPERIENCE, PROJECTS, SKILLS, ETC MAY VARY FROM RESUME TO RESUME.

If you get anything except for an output following this structure, you can reject it and output NO, else YES.

"""