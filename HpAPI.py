import requests

class HpAPI:

    url_api = 'https://hp-api.onrender.com/api/characters'

    cores = {
        '': {
            'bg': '#000000',
            'fg': '#FFD700'
        },
        'gryffindor': {
            'bg': '#C20C0C',
            'fg': '#FFFFFF'
        },
        'slytherin': {
            'bg': '#1A5703',
            'fg': '#FFFFFF'
        },
        'hufflepuff': {
            'bg': '#C2A20C',
            'fg':  '#FFFFFF'
        },
        'ravenclaw': {
            'bg': '#062099',
            'fg': '#FFFFFF'
        }
    }

    casas_disponiveis = [ #label/valor
        ('Todas (padrão)', ''), 
        ("Grinfinória", "gryffindor"), 
        ("Sonserina", "slytherin"), 
        ("Lufa-lufa", "hufflepuff"), 
        ("Corvinal", "ravenclaw")
    ]

    def __init__(self, casa_hogwarts = ''):

        self.casa_hogwarts = casa_hogwarts
        url_api = self.url_api

        if casa_hogwarts:
            url_api += f'/house/{casa_hogwarts}'

        response = requests.get(url_api)
        if response.status_code != 200:
            self.resposta_api = None
        else:
            self.resposta_api = response.json()

    def getPersonagens(self):

        if not self.resposta_api:
            return []

        return self.resposta_api
    
    def quantidadePersonagens(self):

        if not self.resposta_api:
            return 0
        
        return len(self.resposta_api)

    def getCoresCasa(self):
        return self.cores[self.casa_hogwarts]
    
    def getCasasDisponiveis(self):
        return self.casas_disponiveis

        