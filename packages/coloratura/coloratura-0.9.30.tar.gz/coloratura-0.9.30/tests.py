from coloratura import cprint, Pantone

Portfel = {
    'Iwona': {
        'imie': 'Iwona',
        'nazwisko': 'Langner',
        'data_utworzenia_portfela': '04.03.2022',
        'waluty': {
            'pln': 10000,
            'usd': 3000,
            'chf': 1000,
            'eur': 5000},
        'metale': {
            'au': 5}
    },
    'Dawid': {
        'imie': 'Dawid',
        'nazwisko': 'Szatkowski',
        'data_utworzenia_portfela': '05.03.2022',
        'waluty': {
            'pln': 0,
            'usd': 5000},
        'metale': {
            'au': 20}
    }
}

cprint('Dawid', 'Oksana', 'Aron', color=Pantone.ROSE_QUARTZ)

cprint(Portfel['Dawid']['waluty']['usd'], color=Pantone.ROSE_QUARTZ)
