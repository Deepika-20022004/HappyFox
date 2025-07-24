from django.core.management.base import BaseCommand
from core.models import CompanyDrive, Skill, PreparationTopic, LearningResource, MockInterviewQuestion
from datetime import date

# --- Dummy Data Definitions ---
# (Copy-paste the dummy data lists from my previous response here)

company_drives_data = [
    {
        'company_name': 'Tech Global Inc.',
        'role': 'Software Engineer (Backend)',
        'domain': 'Cloud Computing',
        'salary_range': '18-25 LPA',
        'hiring_timeline': 'Late August 2025',
        'drive_date': date(2025, 8, 28),
        'location': 'Bengaluru',
        'interview_process_description': '2 Coding Rounds, 1 System Design, 1 HR'
    },
    {
        'company_name': 'Innovate Solutions',
        'role': 'Data Scientist',
        'domain': 'AI/ML',
        'salary_range': '20-30 LPA',
        'hiring_timeline': 'Early September 2025',
        'drive_date': date(2025, 9, 5),
        'location': 'Hyderabad',
        'interview_process_description': 'Coding Test (Python/R), Data Science Case Study, ML Concepts Interview, Hiring Manager Round, HR Round'
    },
    {
        'company_name': 'FinPeak Capital',
        'role': 'Associate Quant Analyst',
        'domain': 'FinTech',
        'salary_range': '12-18 LPA',
        'hiring_timeline': 'Mid September 2025',
        'drive_date': date(2025, 9, 18),
        'location': 'Mumbai',
        'interview_process_description': 'Quantitative Aptitude, C++ / Python Coding, Probability & Statistics Interview, HR Round'
    },
    {
        'company_name': 'Global Consulting Group',
        'role': 'Business Analyst Intern',
        'domain': 'Consulting',
        'salary_range': '50k/month stipend',
        'hiring_timeline': 'Late September 2025',
        'drive_date': date(2025, 9, 25),
        'location': 'Gurugram',
        'interview_process_description': 'Guesstimate Round, Case Study Interview, Behavioral Interview, Partner Round'
    },
    {
        'company_name': 'HealthTech Innovations',
        'role': 'Frontend Developer',
        'domain': 'Healthcare IT',
        'salary_range': '14-20 LPA',
        'hiring_timeline': 'Early October 2025',
        'drive_date': date(2025, 10, 2),
        'location': 'Pune',
        'interview_process_description': 'Online Frontend Coding Assessment, Technical Interview (JS, React), System Design (Frontend focus), HR'
    },
    {
        'company_name': 'EduVerse Solutions',
        'role': 'AI/ML Engineer',
        'domain': 'EdTech',
        'salary_range': '16-24 LPA',
        'hiring_timeline': 'Mid October 2025',
        'drive_date': date(2025, 10, 10),
        'location': 'Chennai',
        'interview_process_description': 'Machine Learning Fundamentals Test, Coding Round (Python), ML System Design, Behavioral Round'
    },
    {
        'company_name': 'CyberSecure Corp.',
        'role': 'Cybersecurity Analyst',
        'domain': 'Cybersecurity',
        'salary_range': '10-15 LPA',
        'hiring_timeline': 'Late October 2025',
        'drive_date': date(2025, 10, 25),
        'location': 'Bengaluru',
        'interview_process_description': 'Online Security Aptitude, Network Security Concepts, Incident Response Scenario, HR'
    }
]

skills_data = [
    {'name': 'Data Structures & Algorithms', 'description': 'Fundamental concepts for problem-solving in software engineering.'},
    {'name': 'System Design', 'description': 'Designing scalable and reliable software systems.'},
    {'name': 'Python Programming', 'description': 'Proficiency in Python language and its ecosystem.'},
    {'name': 'Java Programming', 'description': 'Proficiency in Java language and its ecosystem.'},
    {'name': 'C++ Programming', 'description': 'Proficiency in C++ language and competitive programming.'},
    {'name': 'Operating Systems', 'description': 'Understanding of OS concepts like processes, threads, memory management.'},
    {'name': 'Database Management Systems', 'description': 'Knowledge of database concepts, SQL, and database design.'},
    {'name': 'SQL', 'description': 'Structured Query Language for database interaction.'},
    {'name': 'Excel', 'description': 'Data manipulation and analysis using Microsoft Excel.'},
    {'name': 'Statistics', 'description': 'Statistical methods and hypothesis testing for data analysis.'},
    {'name': 'Data Visualization', 'description': 'Creating visual representations of data for insights.'},
    {'name': 'Machine Learning', 'description': 'Algorithms and techniques for building predictive models.'},
    {'name': 'Deep Learning', 'description': 'Advanced neural network concepts and applications.'},
    {'name': 'Natural Language Processing', 'description': 'Working with human language data programmatically.'},
    {'name': 'Aptitude', 'description': 'Quantitative ability, logical reasoning, and verbal ability.'},
    {'name': 'Logical Reasoning', 'description': 'Problem-solving using logical deduction.'},
    {'name': 'Communication Skills', 'description': 'Effective verbal and written communication.'},
    {'name': 'Case Study Analysis', 'description': 'Analyzing business problems and proposing solutions.'},
    {'name': 'Frontend Development', 'description': 'Building user interfaces with technologies like React, HTML, CSS, JavaScript.'},
    {'name': 'Cybersecurity Fundamentals', 'description': 'Basic concepts of network security, cryptography, and vulnerabilities.'},
    {'name': 'Network Security', 'description': 'Principles and practices for securing computer networks.'},
    {'name': 'Incident Response', 'description': 'Processes for responding to and managing cybersecurity incidents.'},
]

preparation_topics_data = [
    {'name': 'Arrays & Strings', 'associated_skills': ['Data Structures & Algorithms']},
    {'name': 'Linked Lists', 'associated_skills': ['Data Structures & Algorithms']},
    {'name': 'Trees & Graphs', 'associated_skills': ['Data Structures & Algorithms']},
    {'name': 'Dynamic Programming', 'associated_skills': ['Data Structures & Algorithms']},
    {'name': 'Concurrency', 'associated_skills': ['Operating Systems', 'Java Programming', 'Python Programming']},
    {'name': 'Memory Management', 'associated_skills': ['Operating Systems']},
    {'name': 'Normalization & Joins', 'associated_skills': ['Database Management Systems', 'SQL']},
    {'name': 'Indexing & Transactions', 'associated_skills': ['Database Management Systems']},
    {'name': 'Web Servers & Databases', 'associated_skills': ['System Design']},
    {'name': 'Scalability & Load Balancing', 'associated_skills': ['System Design']},
    {'name': 'Regression Analysis', 'associated_skills': ['Statistics', 'Machine Learning']},
    {'name': 'Classification Algorithms', 'associated_skills': ['Machine Learning']},
    {'name': 'Probability Basics', 'associated_skills': ['Statistics', 'Aptitude']},
    {'name': 'Time & Work', 'associated_skills': ['Aptitude']},
    {'name': 'Non-Verbal Reasoning', 'associated_skills': ['Logical Reasoning']},
    {'name': 'Resume Writing Best Practices', 'associated_skills': ['Communication Skills']},
    {'name': 'SQL Queries & Joins (Advanced)', 'associated_skills': ['SQL']},
    {'name': 'Big O Notation', 'associated_skills': ['Data Structures & Algorithms']},
    {'name': 'Object-Oriented Programming (OOP) Concepts', 'associated_skills': ['Python Programming', 'Java Programming', 'C++ Programming']},
    {'name': 'React.js Fundamentals', 'associated_skills': ['Frontend Development']},
    {'name': 'JavaScript ES6+', 'associated_skills': ['Frontend Development']},
    {'name': 'Neural Network Architectures', 'associated_skills': ['Deep Learning', 'Machine Learning']},
    {'name': 'Cryptography Basics', 'associated_skills': ['Cybersecurity Fundamentals', 'Network Security']},
    {'name': 'Threat Modeling', 'associated_skills': ['Cybersecurity Fundamentals', 'Incident Response']},
]

learning_resources_data = [
    {'title': 'LeetCode Top Interview 150', 'url': 'https://leetcode.com/problemset/top-interview-questions/', 'resource_type': 'problem', 'associated_topics': ['Arrays & Strings', 'Linked Lists', 'Trees & Graphs', 'Dynamic Programming']},
    {'title': 'System Design Interview (YouTube Playlist)', 'url': 'https://www.youtube.com/playlist?list=PLMC9KNkIncK_bzgx_gBpmFgkO-xWAyQNM', 'resource_type': 'video', 'associated_topics': ['Web Servers & Databases', 'Scalability & Load Balancing']},
    {'title': 'GeeksforGeeks DSA Section', 'url': 'https://www.geeksforgeeks.org/data-structures/', 'resource_type': 'article', 'associated_topics': ['Arrays & Strings', 'Linked Lists', 'Trees & Graphs', 'Big O Notation']},
    {'title': 'Abdul Bari - OS Lectures', 'url': 'https://www.youtube.com/playlist?list=PLdo5W4Nhv31a8Uc_b_Sy-fdOQp_uA1G8N', 'resource_type': 'video', 'associated_topics': ['Operating Systems', 'Concurrency', 'Memory Management']},
    {'title': 'SQLZoo Interactive SQL Tutorial', 'url': 'https://sqlzoo.net/', 'resource_type': 'course', 'associated_topics': ['SQL', 'Normalization & Joins', 'SQL Queries & Joins (Advanced)']},
    {'title': 'Kaggle Learn - Machine Learning Course', 'url': 'https://www.kaggle.com/learn/intro-to-machine-learning', 'resource_type': 'course', 'associated_topics': ['Machine Learning', 'Regression Analysis', 'Classification Algorithms']},
    {'title': 'HackerRank Aptitude Prep', 'url': 'https://www.hackerrank.com/domains/tutorials/10-days-of-javascript', 'resource_type': 'problem', 'associated_topics': ['Aptitude', 'Logical Reasoning', 'Time & Work']},
    {'title': 'React Official Documentation', 'url': 'https://react.dev/learn', 'resource_type': 'article', 'associated_topics': ['Frontend Development', 'React.js Fundamentals']},
    {'title': 'MDN Web Docs - JavaScript', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'resource_type': 'article', 'associated_topics': ['Frontend Development', 'JavaScript ES6+']},
    {'title': 'Towards Data Science - ML Articles', 'url': 'https://towardsdatascience.com/machine-learning/home', 'resource_type': 'article', 'associated_topics': ['Machine Learning', 'Deep Learning', 'Natural Language Processing']},
    {'title': 'Cybrary - Cybersecurity Courses', 'url': 'https://www.cybrary.it/catalog/', 'resource_type': 'course', 'associated_topics': ['Cybersecurity Fundamentals', 'Network Security', 'Incident Response']},
]

mock_interview_questions_data = [
    # --- Tech Global Inc. (Software Engineer) ---
    {
        'company_name_str': 'Tech Global Inc.',
        'role': 'Software Engineer',
        'question_text': 'Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.',
        'difficulty_level': 'easy',
        'question_type': 'technical',
        'expected_answer_keywords': 'hash map, two-pass, time complexity, space complexity',
        'sample_answer': 'This can be solved using a hash map (dictionary in Python). Iterate through the array, for each number, check if `target - current_number` exists in the hash map. If yes, return the indices. Otherwise, add the current number and its index to the hash map. Time complexity O(N), Space complexity O(N).'
    },
    {
        'company_name_str': 'Tech Global Inc.',
        'role': 'Software Engineer',
        'question_text': 'Design a URL shortening service like TinyURL.',
        'difficulty_level': 'medium',
        'question_type': 'system_design',
        'expected_answer_keywords': 'hash function, collision, database, scalability, unique ID, Base62',
        'sample_answer': 'Key components include a hash function to generate short codes, a database to store mapping between long and short URLs, handling collisions, and scaling considerations for high read/write loads. Use Base62 encoding for short URLs. Discuss database choices (NoSQL for writes, SQL for consistency), load balancers, caching, etc.'
    },
    {
        'company_name_str': 'Tech Global Inc.',
        'role': 'Software Engineer',
        'question_text': 'Tell me about a time you faced a difficult technical challenge and how you overcame it.',
        'difficulty_level': 'easy',
        'question_type': 'behavioral',
        'expected_answer_keywords': 'STAR method, problem, action, result, learning, teamwork',
        'sample_answer': 'Use the STAR method: Situation, Task, Action, Result. Describe a specific technical problem, your role in solving it, the steps you took (research, collaboration, debugging), and the positive outcome/what you learned.'
    },

    # --- Innovate Solutions (Data Scientist) ---
    {
        'company_name_str': 'Innovate Solutions',
        'role': 'Data Scientist',
        'question_text': 'Explain the difference between overfitting and underfitting in machine learning. How can you mitigate them?',
        'difficulty_level': 'medium',
        'question_type': 'technical',
        'expected_answer_keywords': 'bias, variance, training data, test data, cross-validation, regularization, feature engineering, early stopping',
        'sample_answer': 'Overfitting occurs when a model learns the training data too well, including noise, leading to poor performance on unseen data (high variance). Underfitting occurs when a model is too simple to capture the underlying patterns, performing poorly on both training and test data (high bias). Mitigation for overfitting: regularization (L1/L2), more data, cross-validation, feature selection, early stopping. Mitigation for underfitting: more complex model, more features, reducing regularization.'
    },
    {
        'company_name_str': 'Innovate Solutions',
        'role': 'Data Scientist',
        'question_text': 'Write an SQL query to find the top 5 customers who have spent the most in the last quarter.',
        'difficulty_level': 'easy',
        'question_type': 'technical',
        'expected_answer_keywords': 'SUM, GROUP BY, ORDER BY, LIMIT, WHERE, DATE_TRUNC, JOIN',
        'sample_answer': "```sql\nSELECT c.customer_id, c.customer_name, SUM(o.amount) AS total_spent\nFROM customers c\nJOIN orders o ON c.customer_id = o.customer_id\nWHERE o.order_date >= DATE_TRUNC('quarter', CURRENT_DATE - INTERVAL '3 months')\nGROUP BY c.customer_id, c.customer_name\nORDER BY total_spent DESC\nLIMIT 5;\n```"
    },

    # --- Global Consulting Group (Business Analyst) ---
    {
        'company_name_str': 'Global Consulting Group',
        'role': 'Business Analyst',
        'question_text': 'Estimate the number of cars in Delhi.',
        'difficulty_level': 'hard',
        'question_type': 'aptitude',
        'expected_answer_keywords': 'guesstimate, population, households, car ownership rate, avg cars per household, data sources',
        'sample_answer': 'Breakdown: Population of Delhi (~20M). Assume average household size (~4 people) -> ~5M households. Estimate car ownership rate per household (e.g., 50% own at least one car). Account for commercial vehicles, taxis, etc. State assumptions clearly (e.g., population data source, ownership rate estimation). Calculate ~2.5M to 3M private cars.'
    },
    {
        'company_name_str': 'Global Consulting Group',
        'role': 'Business Analyst',
        'question_text': 'Describe a time you had to persuade someone who initially disagreed with your idea.',
        'difficulty_level': 'medium',
        'question_type': 'behavioral',
        'expected_answer_keywords': 'STAR method, active listening, empathy, data-driven, compromise, influence',
        'sample_answer': 'Use STAR. Focus on how you listened to their concerns, presented your data/logic calmly, addressed their objections, and possibly found a middle ground or a solution that incorporated their valid points, leading to a successful outcome.'
    },

    # --- General/Unassigned Questions (no specific company) ---
    {
        'company_name_str': None, # Explicitly None for general questions
        'role': 'Software Engineer',
        'question_text': 'What is the difference between a process and a thread?',
        'difficulty_level': 'easy',
        'question_type': 'technical',
        'expected_answer_keywords': 'process: independent, own memory space, heavyweight; thread: lightweight, shares memory, within a process',
        'sample_answer': 'A process is an independent execution unit with its own memory space, resources, and context. A thread is a lightweight execution unit within a process, sharing the process\'s memory space and resources. Processes are heavy to switch between, while threads are lighter.'
    },
    {
        'company_name_str': None,
        'role': 'Data Scientist',
        'question_text': 'How do you handle missing data in a dataset?',
        'difficulty_level': 'medium',
        'question_type': 'technical',
        'expected_answer_keywords': 'imputation, mean, median, mode, deletion, listwise, pairwise, advanced methods, domain knowledge',
        'sample_answer': 'Methods include deletion (listwise or pairwise), imputation (mean, median, mode, regression imputation, KNN imputation), using models that can handle missing values, or creating missing indicator variables, or creating missing indicator variables, or creating missing indicator variables, or creating missing indicator variables, or creating missing indicator variables. The choice depends on the type of data, amount of missingness, and domain knowledge.'
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with all dummy data for CompanyDrive, Skills, PreparationTopics, LearningResources, and MockInterviewQuestions.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding.',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('Starting data seeding...'))

        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            MockInterviewQuestion.objects.all().delete()
            LearningResource.objects.all().delete()
            PreparationTopic.objects.all().delete()
            Skill.objects.all().delete()
            CompanyDrive.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))
        
        # Check if data already exists to prevent duplicates on accidental runs
        if CompanyDrive.objects.exists() or Skill.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists. Use --clear option to re-seed.'))
            return

        self.stdout.write(self.style.HTTP_INFO('Seeding Company Drives...'))
        companies_created = {} # To store created CompanyDrive objects for linking
        for data in company_drives_data:
            company = CompanyDrive.objects.create(**data)
            companies_created[company.company_name] = company
            self.stdout.write(self.style.SUCCESS(f'Created CompanyDrive: {company.company_name}'))

        self.stdout.write(self.style.HTTP_INFO('Seeding Skills...'))
        skills_created = {} # To store created Skill objects for linking
        for data in skills_data:
            skill = Skill.objects.create(**data)
            skills_created[skill.name] = skill
            self.stdout.write(self.style.SUCCESS(f'Created Skill: {skill.name}'))

        self.stdout.write(self.style.HTTP_INFO('Seeding Preparation Topics...'))
        topics_created = {} # To store created PreparationTopic objects for linking
        for data in preparation_topics_data:
            associated_skill_names = data.pop('associated_skills', []) # Get skill names, remove from dict
            topic = PreparationTopic.objects.create(**data)
            for skill_name in associated_skill_names:
                if skill_name in skills_created:
                    topic.associated_skills.add(skills_created[skill_name])
                else:
                    self.stdout.write(self.style.WARNING(f'Skill "{skill_name}" not found for topic "{topic.name}".'))
            topics_created[topic.name] = topic
            self.stdout.write(self.style.SUCCESS(f'Created PreparationTopic: {topic.name}'))

        self.stdout.write(self.style.HTTP_INFO('Seeding Learning Resources...'))
        for data in learning_resources_data:
            associated_topic_names = data.pop('associated_topics', []) # Get topic names, remove from dict
            resource = LearningResource.objects.create(**data)
            for topic_name in associated_topic_names:
                if topic_name in topics_created:
                    resource.associated_topics.add(topics_created[topic_name])
                else:
                    self.stdout.write(self.style.WARNING(f'Topic "{topic_name}" not found for resource "{resource.title}".'))
            self.stdout.write(self.style.SUCCESS(f'Created LearningResource: {resource.title}'))

        self.stdout.write(self.style.HTTP_INFO('Seeding Mock Interview Questions...'))
        for data in mock_interview_questions_data:
            company_name = data.pop('company_name_str', None) # Get company name string, remove from dict
            company_obj = companies_created.get(company_name) if company_name else None
            
            question = MockInterviewQuestion.objects.create(company=company_obj, **data)
            self.stdout.write(self.style.SUCCESS(f'Created MockQuestion: {question.question_text[:50]}...'))

        self.stdout.write(self.style.SUCCESS('All dummy data seeded successfully!'))