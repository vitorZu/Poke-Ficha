"""import"""
import io
import json
import urllib.request
from django.shortcuts import render
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
# import requests

# from docx import Document
# from docx.shared import Inches

# Create your views here.
def index(request):
    '''Função para gerar o arquivo PDF com base na PokeAPI'''
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
            "foto-shiny": str(list_of_data['sprites']['other']['official-artwork']['front_shiny']),
            "moves": {}
        }

        for i in range(len(list_of_data['moves'])):
            data["moves"][i] = str(list_of_data['moves'][i]['move']['name']).capitalize

        # criando BIOstream and fotos
        buf = io.BytesIO()

        # Criando Canvas
        page = canvas.Canvas(buf, pagesize = A4)
        #Texto
        page.setTitle(data['nome'] + "-" + data['id'])
        page.drawImage(data['foto'],x=20*mm,y=263*mm, width=100, height=100, mask = 'auto')
        page.drawImage(data['foto-shiny'],x=155*mm,y=263*mm, width=100, height=100,mask = 'auto')
        page.setFont("Helvetica", 35)
        page.drawString(75*mm,263*mm,data['nome'])
        page.line(30*mm,258*mm,182*mm,258*mm)
        page.setFont("Helvetica", 14)
        page.drawString(100*mm,252*mm,data['id'])

        # for i in range(len(list_of_data['moves'])):
        #     page.drawString(200, 100 ,data['moves'][i])

        page.showPage()
        page.save()
        buf.seek(0)

        #return
        return FileResponse(buf, as_attachment = True, filename = 'orçamento.pdf')

    else:
        data = {}

    return render(request, 'index.html' ,data)
