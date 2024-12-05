
# portfolio/views.py
# Add these imports at the top
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from django.contrib.staticfiles import finders

def export_portfolio_pdf(request):
    # Gather all necessary data
    projects = Project.objects.all()
    skills = Skill.objects.all().order_by('category', 'name')
    
    # Render the HTML content
    html_string = render_to_string('portfolio/portfolio_pdf.html', {
        'projects': projects,
        'skills': skills,
    })
    
    # Create the HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="portfolio.pdf"'
    
    # Generate PDF
    pdf = weasyprint.HTML(string=html_string).write_pdf()
    response.write(pdf)
    
    return response