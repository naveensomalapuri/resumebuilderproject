from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from sqlalchemy.orm import Session
from models import Resumebuildertable
import pdfkit
import os
import io
from xhtml2pdf import pisa

import models
import database

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=database.engine)

@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request, db: Session = Depends(database.get_db)):
    resumebuildertable = db.query(models.Resumebuildertable).all()
    return templates.TemplateResponse("index.html", {"request": request, "resumebuildertable": resumebuildertable})


# resume view
def get_resume_by_id(db: Session, resume_id: int):
    return db.query(Resumebuildertable).filter(Resumebuildertable.id == resume_id).first()


@app.get("/resumeview/{resumebuildertable_id}", response_class=HTMLResponse)
async def read_items(request: Request, resumebuildertable_id: int, db: Session = Depends(database.get_db)):
    resume = get_resume_by_id(db, resumebuildertable_id)
    if resume is None:
        return HTMLResponse(content="Resume not found", status_code=404)
    return templates.TemplateResponse("resumeview.html", {"request": request, "resume": resume})


@app.get("/create", response_class=HTMLResponse)
async def create_item_form(request: Request):
    return templates.TemplateResponse("create_item.html", {"request": request})

@app.post("/create", response_class=HTMLResponse)
async def create_item(
    name: str = Form(...),
    email: str = Form(...),
    phonenumber: str = Form(...),
    location: str = Form(...),
    linkedinlink: str = Form(...),
    githublink: str = Form(...),
    careerobjective: str = Form(...),
    college_qualification: str = Form(...),
    college_name: str = Form(...),
    college_year_of_pass: str = Form(...),
    college_gpa: str = Form(...),
    school_qualification: str = Form(...),
    school_name: str = Form(...),
    school_year_of_pass: str = Form(...),
    school_gpa: str = Form(...),
    skill1: str = Form(...),
    skill2: str = Form(...),
    skill3: str = Form(...),
    skill4: str = Form(...),
    skill5: str = Form(...),
    skill6: str = Form(...),
    skill7: str = Form(...),
    skill8: str = Form(...),
    skill9: str = Form(...),
    skill10: str = Form(...),
    project1_name: str = Form(...),
    project1_description: str = Form(...),
    project1_duration: str = Form(...),
    project2_name: str = Form(...),
    project2_description: str = Form(...),
    project2_duration: str = Form(...),
    language1: str = Form(...),
    language2: str = Form(...),
    language3: str = Form(...),
    db: Session = Depends(database.get_db)
):
    db_resumebuilder = models.Resumebuildertable(
        name=name, email=email, phonenumber=phonenumber,
        location=location, linkedinlink=linkedinlink, githublink=githublink,
        careerobjective=careerobjective, college_qualification=college_qualification,
        college_name=college_name, college_year_of_pass=college_year_of_pass, college_gpa=college_gpa,
        school_qualification=school_qualification, school_name=school_name,
        school_year_of_pass=school_year_of_pass, school_gpa=school_gpa,
        skill1=skill1, skill2=skill2, skill3=skill3, skill4=skill4, skill5=skill5,
        skill6=skill6, skill7=skill7, skill8=skill8, skill9=skill9, skill10=skill10,
        project1_name=project1_name, project1_description=project1_description,
        project1_duration=project1_duration, project2_name=project2_name, project2_description=project2_description,
        project2_duration=project2_duration, language1=language1, language2=language2,
        language3=language3
    )
    db.add(db_resumebuilder)
    db.commit()
    db.refresh(db_resumebuilder)
    return RedirectResponse("/", status_code=303)

@app.get("/update/{resumebuildertable_id}", response_class=HTMLResponse)
async def update_item_form(resumebuildertable_id: int, request: Request, db: Session = Depends(database.get_db)):
    resumebuildertable = db.query(models.Resumebuildertable).filter(models.Resumebuildertable.id == resumebuildertable_id).first()
    if not resumebuildertable:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse("update_item.html", {"request": request, "resumebuildertable": resumebuildertable})

@app.post("/update/{resumebuildertable_id}", response_class=HTMLResponse)
async def update_item(
    resumebuildertable_id: int, 
    name: str = Form(...),
    email: str = Form(...),
    phonenumber: str = Form(...),
    location: str = Form(...),
    linkedinlink: str = Form(...),
    githublink: str = Form(...),
    careerobjective: str = Form(...),
    college_qualification: str = Form(...),
    college_name: str = Form(...),
    college_year_of_pass: str = Form(...),
    college_gpa: str = Form(...),
    school_qualification: str = Form(...),
    school_name: str = Form(...),
    school_year_of_pass: str = Form(...),
    school_gpa: str = Form(...),
    skill1: str = Form(...),
    skill2: str = Form(...),
    skill3: str = Form(...),
    skill4: str = Form(...),
    skill5: str = Form(...),
    skill6: str = Form(...),
    skill7: str = Form(...),
    skill8: str = Form(...),
    skill9: str = Form(...),
    skill10: str = Form(...),
    project1_name: str = Form(...),
    project1_description: str = Form(...),
    project1_duration: str = Form(...),
    project2_name: str = Form(...),
    project2_description: str = Form(...),
    project2_duration: str = Form(...),
    language1: str = Form(...),
    language2: str = Form(...),
    language3: str = Form(...),
    db: Session = Depends(database.get_db)
):
    resumebuildertable = db.query(models.Resumebuildertable).filter(models.Resumebuildertable.id == resumebuildertable_id).first()
    if not resumebuildertable:
        raise HTTPException(status_code=404, detail="Item not found")
    
    resumebuildertable.name = name
    resumebuildertable.email = email
    resumebuildertable.phonenumber = phonenumber
    resumebuildertable.location = location
    resumebuildertable.linkedinlink = linkedinlink
    resumebuildertable.githublink = githublink
    resumebuildertable.careerobjective = careerobjective
    resumebuildertable.college_qualification = college_qualification
    resumebuildertable.college_name = college_name
    resumebuildertable.college_year_of_pass = college_year_of_pass
    resumebuildertable.college_gpa = college_gpa
    resumebuildertable.school_qualification = school_qualification
    resumebuildertable.school_name = school_name
    resumebuildertable.school_year_of_pass = school_year_of_pass
    resumebuildertable.school_gpa = school_gpa
    resumebuildertable.skill1 = skill1
    resumebuildertable.skill2 = skill2
    resumebuildertable.skill3 = skill3
    resumebuildertable.skill4 = skill4
    resumebuildertable.skill5 = skill5
    resumebuildertable.skill6 = skill6
    resumebuildertable.skill7 = skill7
    resumebuildertable.skill8 = skill8
    resumebuildertable.skill9 = skill9
    resumebuildertable.skill10 = skill10
    resumebuildertable.project1_name = project1_name
    resumebuildertable.project1_description = project1_description
    resumebuildertable.project1_duration = project1_duration
    resumebuildertable.project2_name = project2_name
    resumebuildertable.project2_description = project2_description
    resumebuildertable.project2_duration = project2_duration
    resumebuildertable.language1 = language1
    resumebuildertable.language2 = language2
    resumebuildertable.language3 = language3

    db.commit()
    return RedirectResponse("/", status_code=303)

# convert html as pdf
from pdfcrowd import HtmlToPdfClient

@app.get("/download_pdf", response_class=FileResponse)
async def download_pdf(request: Request, db: Session = Depends(database.get_db)):
    resumebuildertable = db.query(models.Resumebuildertable).all()
    html_content = templates.TemplateResponse("resumeview.html", {"request": request, "resumebuildertable": resumebuildertable}).body.decode("utf-8")
    
    pdf_file_path = "items.pdf"
    client = HtmlToPdfClient("somalapurinaveen999","e9c2eb9b110f3e6036b876e3fd36d679") # ("your_api_key")
    client.setUseHttp(True)
    client.convertStringToFile(html_content, pdf_file_path)
    return FileResponse(path=pdf_file_path, filename="items.pdf", media_type="application/pdf")


"""@app.get("/download_pdf", response_class=FileResponse)
async def download_pdf(request: Request, db: Session = Depends(database.get_db)):
    resumebuildertable = db.query(models.Resumebuildertable).all()
    html_content = templates.TemplateResponse("index.html", {"request": request, "resumebuildertable": resumebuildertable}).body.decode("utf-8")
    
    # Update paths to absolute URLs
    html_content = html_content.replace('href="/static/', f'href="{request.url_for("static", path="")}')
    html_content = html_content.replace('src="/static/', f'src="{request.url_for("static", path="")}')
    
    pdf_file_path = "items.pdf"
    pdfkit.from_string(html_content, pdf_file_path)
    return FileResponse(path=pdf_file_path, filename="items.pdf", media_type="application/pdf")

"""



"""
@app.get("/download_pdf")
async def download_pdf(request: Request, db: Session = Depends(database.get_db)):
    resumebuildertable = db.query(models.Resumebuildertable).all()
    
    # Render HTML content using a template
    html_content = templates.TemplateResponse("update_item.html", {"request": request, "resumebuildertable": resumebuildertable}).body.decode("utf-8")
    
    # Convert HTML to PDF
    pdf_file_path = "NewResume.pdf"
    pdf = io.BytesIO()
    
    pisa_status = pisa.CreatePDF(io.StringIO(html_content), dest=pdf)
    
    if pisa_status.err:
        return {"detail": "Error generating PDF: {}".format(pisa_status.err)}

    pdf.seek(0)
    
    # Save PDF to a file
    with open(pdf_file_path, "wb") as f:
        f.write(pdf.read())

    return FileResponse(path=pdf_file_path, filename="NewResume.pdf", media_type="application/pdf")"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
