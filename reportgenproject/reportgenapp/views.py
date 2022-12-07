from django.shortcuts import render,redirect
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from matplotlib import pyplot as plt
import numpy as np
import textwrap
from django.http import HttpResponseRedirect,FileResponse

# Create your views here.
def index(request):
    data = []
    if request.method == "POST":
        title=request.POST["title"]
        fileName=request.POST["fileName"]
        names=request.POST["names"]
        userData=request.POST["data"]
        if len(userData.split(",")) != len(names.split(",")):
            return HttpResponseRedirect("/")
        names = names.split(",")
        userData = userData.split(",")
        for num in userData:
            data.append(int(num))
        textLines=request.POST["textLines"]
        if len(textLines.split()) > 1200:
            return HttpResponseRedirect("/")
        chart=request.POST["chart"]
        #print(chart)
        if chart.upper() == "PIE" or chart.upper() == "BAR":
            pass
        else:
            return HttpResponseRedirect("/")
        textLines = textWrapper(textLines)
        documentTitle="report"
        pdfcreator(fileName,documentTitle,title,textLines,names,data,chart)

        return FileResponse(open(f"static/reportPdfs/{fileName}","rb"),as_attachment=True,content_type="application/pdf")



    
    return render(request, "index.html")
    



def pdfcreator(fileName,documentTitle,title,textLines,names,data,chart):
  pdf = canvas.Canvas(f"static/reportPdfs/{fileName}")
  pdf.setTitle(documentTitle)
  pdf.setFont('Courier', 36)
  pdf.drawCentredString(300, 770, title)
  pdf.line(30, 710, 550, 710)
  text = pdf.beginText(30, 680)
  text.setFont("Courier", 13)
  text.setFillColor(colors.black)
  for line in textLines:
    text.textLine(line)
  pdf.drawText(text)

  #chart = "pie"
  chartGenerator(names,data,chart,title)
  
  pdf.drawInlineImage(f"static/reportImages/report{chart}.JPEG", 2, 5)

  pdf.showPage()
# saving the pdf
  pdf.save()


def chartGenerator(names,data,chart,title):
# Creating plot
  fig = plt.figure(figsize =(5, 3))
  if chart.upper() == "PIE":
    plt.pie(data, labels = names,shadow=True)

  elif chart.upper() == "BAR":
    plt.bar(names,data,color ='maroon',width = 0.4)
    plt.xlabel("")
    plt.ylabel("")
    plt.title(title)
  else:
    raise Exception("Either Pie or Bar chart only!")
    exit()
  
# show plot
  plt.savefig(f"static/reportImages/report{chart}.JPEG")



def textWrapper(textLines):
    wrapper = textwrap.TextWrapper(width=70)
    textLines = wrapper.wrap(text=textLines)
    return textLines
  