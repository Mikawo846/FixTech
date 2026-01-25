from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import re
from pathlib import Path

app = FastAPI(title="FixTech - Repair Instructions")

# Mount static files
app.mount("/static", StaticFiles(directory="."), name="static")

# Set up templates
templates = Jinja2Templates(directory=".")

def extract_title_from_h1(content: str) -> str:
    """Extract text from first <h1> tag"""
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    if h1_match:
        h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1))
        return h1_text.strip()
    return ""

def extract_first_paragraph(content: str) -> str:
    """Extract first paragraph after h1"""
    h1_pos = content.lower().find('<h1')
    if h1_pos == -1:
        return ""
    
    h1_end = content.lower().find('</h1>', h1_pos)
    if h1_end == -1:
        return ""
    
    after_h1 = content[h1_end + 5:]
    p_match = re.search(r'<p[^>]*>(.*?)</p>', after_h1, re.DOTALL | re.IGNORECASE)
    if p_match:
        p_text = re.sub(r'<[^>]+>', '', p_match.group(1))
        return p_text.strip()
    return ""

def generate_description(h1_text: str, first_paragraph: str) -> str:
    """Generate meta description"""
    if not h1_text:
        return "Пошаговые инструкции по ремонту техники. Советы экспертов, таблицы, FAQ."
    
    if first_paragraph:
        paragraph_snippet = first_paragraph[:80]
        if len(first_paragraph) > 80:
            paragraph_snippet = paragraph_snippet.rstrip() + "..."
    else:
        paragraph_snippet = ""
    
    description = f"Пошаговая инструкция: {h1_text}"
    if paragraph_snippet:
        description += f". {paragraph_snippet}"
    description += ". Советы экспертов, таблицы, FAQ."
    
    if len(description) > 160:
        description = description[:157].rstrip() + "..."
    elif len(description) < 140 and paragraph_snippet:
        if len(first_paragraph) > 80:
            extended_snippet = first_paragraph[:120]
            if len(first_paragraph) > 120:
                extended_snippet = extended_snippet.rstrip() + "..."
            description = f"Пошаговая инструкция: {h1_text}. {extended_snippet}. Советы экспертов, таблицы, FAQ."
    
    return description

def get_page_description(html_file: str) -> str:
    """Generate description for a specific HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        h1_text = extract_title_from_h1(content)
        first_paragraph = extract_first_paragraph(content)
        return generate_description(h1_text, first_paragraph)
    except Exception:
        return "Пошаговые инструкции по ремонту техники. Советы экспертов, таблицы, FAQ."

@app.get("/")
async def home(request: Request):
    description = get_page_description("index.html")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "description": description
    })

@app.get("/{page_name}")
async def page(request: Request, page_name: str):
    # Add .html extension if not present
    if not page_name.endswith('.html'):
        page_name += '.html'
    
    # Check if file exists
    file_path = Path(page_name)
    if not file_path.exists():
        return templates.TemplateResponse("404.html", {
            "request": request,
            "description": "Страница не найдена - FixTech"
        }, status_code=404)
    
    description = get_page_description(page_name)
    return templates.TemplateResponse(page_name, {
        "request": request,
        "description": description
    })

# Category pages
@app.get("/articles")
async def articles(request: Request):
    description = get_page_description("articles.html")
    return templates.TemplateResponse("articles.html", {
        "request": request,
        "description": description
    })

@app.get("/smartphones")
async def smartphones(request: Request):
    description = get_page_description("smartphones.html")
    return templates.TemplateResponse("smartphones.html", {
        "request": request,
        "description": description
    })

@app.get("/laptops")
async def laptops(request: Request):
    description = get_page_description("laptops.html")
    return templates.TemplateResponse("laptops.html", {
        "request": request,
        "description": description
    })

@app.get("/tv")
async def tv(request: Request):
    description = get_page_description("tv.html")
    return templates.TemplateResponse("tv.html", {
        "request": request,
        "description": description
    })

@app.get("/cameras")
async def cameras(request: Request):
    description = get_page_description("cameras.html")
    return templates.TemplateResponse("cameras.html", {
        "request": request,
        "description": description
    })

@app.get("/consoles")
async def consoles(request: Request):
    description = get_page_description("consoles.html")
    return templates.TemplateResponse("consoles.html", {
        "request": request,
        "description": description
    })

@app.get("/auto-electronics")
async def auto_electronics(request: Request):
    description = get_page_description("auto-electronics.html")
    return templates.TemplateResponse("auto-electronics.html", {
        "request": request,
        "description": description
    })

@app.get("/small-appliances")
async def small_appliances(request: Request):
    description = get_page_description("small-appliances.html")
    return templates.TemplateResponse("small-appliances.html", {
        "request": request,
        "description": description
    })

@app.get("/large-appliances")
async def large_appliances(request: Request):
    description = get_page_description("large-appliances.html")
    return templates.TemplateResponse("large-appliances.html", {
        "request": request,
        "description": description
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
