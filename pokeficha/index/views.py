from django.shortcuts import render
import urllib.request
import json
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import requests

# from docx import Document
# from docx.shared import Inches

# Create your views here.
def index(request):
    if request.method == "POST":
        pokemon = request.POST['pokemon'].lower()
        pokemon = pokemon.replace(' ', '%20')
        url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon/{pokemon}/')
        url_pokeapi.add_header('User-Agent', 'blastoise')

        source = urllib.request.urlopen(url_pokeapi).read()

        list_of_data = json.loads(source)

        altura = list_of_data['height']/10
        peso = list_of_data['weight']/10

        data = {
            "id": str(list_of_data['id']),
            "nome": str(list_of_data['species']['name']).capitalize(),
            "altura": str(altura),
            "peso": str(peso),
            "foto": str(list_of_data['sprites']['other']['official-artwork']['front_default']),
            "foto-shiny": str(list_of_data['sprites']['other']['official-artwork']['front_shiny'])
        }

        # criando BIOstream and fotos
        buf = io.BytesIO()
        response1 = requests.get(data['foto'], stream=True)
        foto = io.BytesIO(response1.content)
        response2 = requests.get(data['foto-shiny'], stream=True)
        foto_shiny = io.BytesIO(response2.content)

        # Criando Canvas
        c = canvas.Canvas(buf, pagesize = letter, bottomup = 0)

        # Configurando Pagina PDF
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)

        #linha do Texto
        lines = [
            data['id'],
            data['nome'],
            data['altura'] + " M",
            data['peso'] + " kg",
            f"{foto}",
            f"{foto_shiny}",
            "=============",
        ]

        #looping
        for line in lines:
            textob.textLine(line)


        #finalizando
        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        #return
        return FileResponse(buf, as_attachment = True, filename = 'orçamento.pdf')


        

        # document = Document()
        # document.add_heading(f"{data['nome']} - {data['id']}", 0)
        # document.add_picture(foto, width=Inches(1.25))
        # document.add_picture(foto_shiny, width=Inches(1.25))
        

        # document.save('demo.docx')

    else:
        data = {}

    return render(request, 'index.html' ,data)