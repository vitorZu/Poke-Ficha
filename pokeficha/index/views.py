"""import"""
import io
import json
import urllib.request
from django.shortcuts import render
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
# import requests

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
            "moves": {},
            "types": {},
            "types-icon": {
                "normal": str("./staticos/Mezastar_Normal_type.png"),
                "fire": str("./staticos/Mezastar_Fire_type.png"),
                "water": str("./staticos/Mezastar_Water_type.png"),
                "grass": str("./staticos/Mezastar_Grass_type.png"),
                "electric": str("./staticos/Mezastar_Electric_type.png"),
                "ice": str("./staticos/Mezastar_Ice_type.png"),
                "fighting": str("./staticos/Mezastar_Fighting_type.png"),
                "poison": str("./staticos/Mezastar_Poison_type.png"),
                "ground": str("./staticos/Mezastar_Ground_type.png"),
                "flying": str("./staticos/Mezastar_Flying_type.png"),
                "psychic": str("./staticos/Mezastar_Psychic_type.png"),
                "bug": str("./staticos/Mezastar_Bug_type.png"),
                "rock": str("./staticos/Mezastar_Rock_type.png"),
                "ghost": str("./staticos/Mezastar_Ghost_type.png"),
                "dark": str("./staticos/Mezastar_Dark_type.png"),
                "dragon": str("./staticos/Mezastar_Dragon_type.png"),
                "steel": str("./staticos/Mezastar_Steel_type.png"),
                "fairy": str("./staticos/Mezastar_Fairy_type.png"),
            },
            "stats-hp": str(list_of_data['stats'][0]['base_stat']),
            "stats-atk": str(list_of_data['stats'][1]['base_stat']),
            "stats-def": str(list_of_data['stats'][2]['base_stat']),
            "stats-spAtk": str(list_of_data['stats'][3]['base_stat']),
            "stats-spDef": str(list_of_data['stats'][4]['base_stat']),
            "stats-speed": str(list_of_data['stats'][5]['base_stat']),
        }

        for i in range(len(list_of_data['moves'])):
            data["moves"][i] = str(list_of_data['moves'][i]['move']['name']).capitalize
        for i in range(len(list_of_data['types'])):
            data["types"][i] = str(list_of_data['types'][i]['type']['name'])

        # criando BIOstream and fotos
        buf = io.BytesIO()

        # Criando Canvas
        pdf = canvas.Canvas(buf, pagesize = A4)

        stats_dados = [
            ["","Base Stats"],
            ["HP", data['stats-hp']],
            ["ATK", data['stats-atk']],
            ["DEF", data['stats-def']],
            ["Sp.ATK", data['stats-spAtk']],
            ["Sp.DEF", data['stats-spDef']],
            ["Speed", data['stats-speed']],
        ]
        stats = Table(stats_dados,2*[3*cm],7*[.57*cm])
        stats.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,6), colors.grey),
            ('TEXTCOLOR',(0,0),(0,6), colors.white),
            ('BACKGROUND',(0,0),(1,0), colors.grey),
            ('TEXTCOLOR',(0,0),(1,0), colors.white),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ]))

        #Texto
        pdf.setTitle(data['nome'] + "-" + data['id'])
        pdf.setFont("Helvetica", 35)
        pdf.drawCentredString(10.5*cm,28.3*cm,data['nome'])
        pdf.line(3*cm,28*cm,18.2*cm,28*cm)
        pdf.setFont("Helvetica", 14)
        pdf.drawCentredString(10.5*cm,27.3*cm,data['id'])
        pdf.drawImage(
            data['foto'],
            x=2*cm,
            y=23.4*cm,
            width=4.25*cm,
            height=4.25*cm,
            mask='auto'
            )
        pdf.drawImage(
            data['foto-shiny'],
            x=6.27*cm,
            y=23.4*cm,
            width=4.25*cm,
            height=4.25*cm,
            mask='auto'
            )

        stats.wrapOn(pdf,7*cm,3.5*cm)
        stats.drawOn(pdf,11.5*cm,23.6*cm)

        
        codx = 3
        for i in data['types']:
            pdf.drawImage(
                data["types-icon"][f"{data['types'][i]}"],
                x=codx*cm,
                y=22.5*cm,
                height=.5*cm,
                width=.6*cm,
                mask='auto',
            )

            pdf.drawString((codx + .7)*cm,22.6*cm,f"{data['types'][i]}".upper())

            codx += (.5 + (len(data["types"][i])/2.2))

        pdf.showPage()
        pdf.save()
        buf.seek(0)

        #return
        return FileResponse(buf, as_attachment = True, filename = f"FichaPokemon-{data['nome']}.pdf")

    else:
        data = {}

    return render(request, 'index.html' ,data)
