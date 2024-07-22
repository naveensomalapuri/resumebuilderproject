from sqlalchemy import Column, Integer, String
from database import Base

class Resumebuildertable(Base):
    __tablename__ = "resumedatatable"


    id = Column(Integer, primary_key=True, index=True)

    # personal data
    name = Column(String, index=True)
    email = Column(String, index=True)
    phonenumber = Column(String, index=True)
    location = Column(String, index=True)
    linkedinlink = Column(String, index=True)
    githublink = Column(String, index=True)
    careerobjective = Column(String, index=True)

    # college data
    college_qualification = Column(String, index=True)
    college_name = Column(String, index=True)
    college_year_of_pass = Column(String, index=True)
    college_gpa = Column(String, index=True)

    # school data
    school_qualification = Column(String, index=True)
    school_name = Column(String, index=True)
    school_year_of_pass = Column(String, index=True)
    school_gpa = Column(String, index=True)

    # skills
    skill1 = Column(String, index=True)
    skill2 = Column(String, index=True)
    skill3 = Column(String, index=True)
    skill4 = Column(String, index=True)
    skill5 = Column(String, index=True)
    skill6 = Column(String, index=True)
    skill7 = Column(String, index=True, default="")
    skill8 = Column(String, index=True, default="")
    skill9 = Column(String, index=True, default="")
    skill10 = Column(String, index=True, default="")
    
    # Experiance
    project1_name = Column(String, index=True)
    project1_description = Column(String, index=True)
    project1_duration = Column(String, index=True)
    
    project2_name = Column(String, index=True)
    project2_description = Column(String, index=True)
    project2_duration = Column(String, index=True)
    
    # communication skills
    language1 = Column(String, index=True)
    language2 = Column(String, index=True)
    language3 = Column(String, index=True, default="")