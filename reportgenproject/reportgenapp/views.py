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
from django.http import HttpResponseRedirect,FileResponse,HttpResponse
from django.contrib import messages

# Create your views here.
def index(request):
    data = []

    #check if method is post
    if request.method == "POST":

      """
      Get all data from forms and do error checking
      return  user back to homepage if form isnt valid
      """
      title=request.POST["title"]
      fileName=request.POST["fileName"]
      if "pdf" not in fileName.split("."):
        messages.error(request, "'.pdf' extension required in filename section")
        return HttpResponseRedirect("/")

      names=request.POST["names"]
      userData=request.POST["data"]
      if len(userData.split(",")) != len(names.split(",")):
        messages.error(request, "length of data and values should be equal Please")
        return HttpResponseRedirect("/")
      names = names.split(",")


      userData = userData.split(",")
      for num in userData:
        try:
          data.append(int(num))
        except:
          messages.error(request, "Enter only numbers in the data frequency section please")
          return HttpResponseRedirect("/")


      textLines=request.POST["textLines"]
      if len(textLines.split()) > 350:
        messages.error(request, "Your Information can't be more than 350 words please")
        return HttpResponseRedirect("/")


      chart=request.POST["chart"]
      if chart.upper() == "PIE" or chart.upper() == "BAR":
        pass
      else:
        messages.error(request, "Please Type Either 'pie or bar' ")
        return HttpResponseRedirect("/")
      textLines = textWrapper(textLines)
      documentTitle="report"

      #call the pdfcreator function
      pdfcreator(fileName,documentTitle,title,textLines,names,data,chart)

      #return the generated pdf for user
      return FileResponse(open(f"static/reportPdfs/{fileName}","rb"),as_attachment=True,content_type="application/pdf")
       


    #if a get request, return the homepage
    return render(request, "index.html")
    

"""
Function that generates the pdf template with reportlab canvas
PDF is stored to the directory provided

"""

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

  """calls the chart generator function which returns 
  an image of the chart,pie or bar
  this is then used by the pdfgenerator to render the pdf with the graph
  """
  chartGenerator(names,data,chart,title)
  
  pdf.drawInlineImage(f"static/reportImages/report{chart}.JPEG", 2, 5)

  #create a page
  pdf.showPage()
# saving the pdf
  pdf.save()

"""
Function that creates a chart, pie or bar 
it takes the parameters of the name of the data, the type of chart
the title of the chart
and the data values
"""

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
  
# save plot
  plt.savefig(f"static/reportImages/report{chart}.JPEG")


"""
function that wraps the text the user inputs 
This makes the lines start on new lines without going beyond 
the page width
"""
def textWrapper(textLines):
    wrapper = textwrap.TextWrapper(width=70)
    textLines = wrapper.wrap(text=textLines)
    return textLines
  