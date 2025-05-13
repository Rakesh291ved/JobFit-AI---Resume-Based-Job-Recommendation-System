import sqlite3
import os

db_path = 'jobs.db'

# Delete if corrupted or empty
if os.path.exists(db_path) and os.path.getsize(db_path) < 100:
    os.remove(db_path)
    print("🧹 Removed invalid jobs.db")

# Create fresh DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS job_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    skills TEXT NOT NULL
);
''')

job_data = [
    # Data & AI
    ("Data Analyst", "python,sql,data analysis,excel,tableau"),
    ("Data Scientist", "python,sql,machine learning,statistics,pandas,numpy,scikit-learn,matplotlib"),
    ("ML Engineer", "python,machine learning,tensorflow,pytorch,flask,sql,data pipelines"),
    ("AI Researcher", "python,tensorflow,pytorch,nlp,deep learning,reinforcement learning"),
    ("BI Developer", "power bi,sql,data warehousing,etl,ssrs,excel"),

    # Web Development
    ("Frontend Developer", "html,css,javascript,react,vue,redux,typescript"),
    ("Backend Developer", "python,flask,django,node.js,express,sql,mongodb"),
    ("Full Stack Developer", "html,css,javascript,react,node.js,express,mongodb,sql"),
    ("Web Developer", "html,css,javascript,bootstrap,jquery,php"),

    # Mobile Development
    ("Android Developer", "java,kotlin,android sdk,xml,retrofit,sqlite"),
    ("iOS Developer", "swift,objective-c,xcode,core data,swiftui"),
    ("Flutter Developer", "flutter,dart,firebase,android sdk,ios sdk"),

    # DevOps & Cloud
    ("DevOps Engineer", "docker,kubernetes,jenkins,git,aws,azure,ci/cd,linux,bash"),
    ("Cloud Engineer", "aws,azure,gcp,terraform,cloudformation,linux,networking"),
    ("Site Reliability Engineer", "python,golang,docker,kubernetes,monitoring,prometheus,grafana"),

    # Cybersecurity
    ("Security Analyst", "network security,vulnerability scanning,wireshark,linux,firewalls,siem"),
    ("Penetration Tester", "kali linux,metasploit,nmap,burp suite,ethical hacking,owasp"),

    # UI/UX & Product
    ("UI Designer", "figma,adobe xd,sketch,html,css,design systems"),
    ("UX Researcher", "user research,wireframes,personas,journey mapping,interviews,prototyping"),
    ("Product Manager", "agile,scrum,jira,roadmaps,stakeholder communication,wireframes"),

    # Testing & QA
    ("QA Engineer", "manual testing,automation testing,selenium,postman,bug tracking,api testing"),
    ("Test Automation Engineer", "selenium,java,python,testng,junit,jenkins,cypress"),

    # Others / Bonus Roles
    ("Database Administrator", "sql,mysql,oracle,performance tuning,backups,pl/sql"),
    ("Technical Support Engineer", "troubleshooting,networking,windows,linux,customer service"),
    ("Systems Administrator", "linux,windows server,networking,shell scripting,backup tools"),
    ("Game Developer", "unity,c#,game physics,3d modeling,animation"),

    # Emerging Tech
    ("Blockchain Developer", "solidity,ethereum,web3.js,smart contracts,ganache,truffle"),
    ("AR/VR Developer", "unity,c#,vr sdk,arcore,arkit,3d modeling"),

    # Entry-level Roles
    ("Junior Web Developer", "html,css,javascript,bootstrap,git"),
    ("IT Intern", "ms office,troubleshooting,teamwork,documentation"),
    
    # Finance & Accounting
    ("Financial Analyst", "excel,financial modeling,accounting,forecasting,sql,python"),
    ("Accountant", "accounting,tally,excel,bookkeeping,erp,quickbooks"),
    ("Investment Analyst", "equity research,valuation,excel,financial modeling,python,macroeconomics"),

    # Marketing & Sales
    ("Digital Marketing Specialist", "seo,sem,google ads,social media,analytics,content marketing"),
    ("Content Writer", "writing,seo,wordpress,editing,copywriting,content strategy"),
    ("Sales Executive", "negotiation,crm,communication,lead generation,salesforce"),

    # HR & Administration
    ("HR Executive", "recruitment,interviews,hrms,payroll,onboarding,employee engagement"),
    ("Talent Acquisition Specialist", "sourcing,interviewing,job portals,linkedin,recruitment strategies"),
    ("Office Administrator", "ms office,scheduling,inventory management,filing,customer service"),

    # Operations & Logistics
    ("Operations Manager", "supply chain,inventory management,erp,logistics,forecasting"),
    ("Logistics Coordinator", "scheduling,tracking,warehouse,shipping,inventory software"),

    # Mechanical / Civil / Core Engineering
    ("Mechanical Engineer", "autocad,solidworks,catia,thermodynamics,manufacturing"),
    ("Civil Engineer", "autocad,staad pro,site supervision,construction management,estimation"),
    ("Electrical Engineer", "pcb design,electrical circuits,matlab,autocad,electrical safety"),

    # Education & Training
    ("Teacher", "lesson planning,classroom management,subject expertise,grading,ms office"),
    ("Corporate Trainer", "training design,presentation,communication,learning management systems"),

    # Legal & Compliance
    ("Legal Associate", "contract drafting,legal research,compliance,litigation,ms word"),
    ("Compliance Officer", "audit,regulatory knowledge,policies,risk management,reporting"),

    # Media & Entertainment
    ("Video Editor", "adobe premiere,final cut pro,after effects,storyboarding,sound editing"),
    ("Graphic Designer", "photoshop,illustrator,creativity,branding,figma,canva"),

    # Hospitality & Tourism
    ("Hotel Manager", "hospitality,guest handling,inventory,housekeeping,operations management"),
    ("Travel Consultant", "itinerary planning,gds,customer service,booking systems,travel knowledge")
]


cursor.executemany('INSERT INTO job_roles (title, skills) VALUES (?, ?)', job_data)

conn.commit()
conn.close()

print("✅ jobs.db created and populated.")
