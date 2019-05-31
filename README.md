## Scrapper de feriados

Scrapper de feriados para Python 3 que funciona en base a información extraída desde el sitio www.feriadoschilenos.cl. No estoy afiliado con el sitio y el uso de esta herramienta es responsabilidad de quien la usa.

## Ejemplo Uso

    python parse_holidays.py 1990 2000
    {
        "2010": [
            {
                "date": "2010-01-01",
                "name": "A\u00f1o Nuevo",
                "irrenunciable": true,
                "recurrente": true,
                "religioso": false,
                "singular": false,
                "escolar": false,
                "local": false,
                "locality": null
            },
            ...
        ],
        "2011": [
            {
                "date": "2011-01-01",
                "name": "A\u00f1o Nuevo",
                "irrenunciable": true,
                "recurrente": true,
                "religioso": false,
                "singular": false,
                "escolar": false,
                "local": false,
                "locality": null
            },
            ...
        ]
    }
