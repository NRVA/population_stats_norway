from django.shortcuts import render

def home(request):
    import json
    import requests
    from . import sp
    from . import backend
    from pyjstat import pyjstat


    if request.method == "POST":
        input = [request.POST['komunenummer']]
        url = "https://data.ssb.no/api/v0/no/table/07459/"
        sp = json.loads(str(sp.historikk).replace("\'", "\""))
        try:
            InputFormater = backend.InputFormater(input)
            navn = InputFormater.navn
            sp["query"][0]["selection"]["values"] = InputFormater.idnr_K #"K-1804"
            res = requests.post(url, json=sp)
            content = pyjstat.Dataset.read(res.text)  # json.loads(res.content)
            content = content.write("dataframe")
            content = backend.reshaper(content)
            graph = backend.graph(content, "Antall innbyggere", navn)

        except Exception as e:
            navn = "Noe gikk galt..."
            graph = None

        return render(request, 'home.html', {'content': navn, 'graph': graph})
    else:
        url = "https://data.ssb.no/api/v0/no/table/07459/"
        sp = json.loads(str(sp.historikk).replace("\'", "\""))
        sp["query"][0]["selection"]["values"] = ["K-1804"]
        try:
            res = requests.post(url, json=sp)
            content = pyjstat.Dataset.read(res.text) #json.loads(res.content)
            content = content.write("dataframe")

            content = backend.reshaper(content)
            graph = backend.graph(content, "Antall innbyggere", "Bodø")

        except Exception as e:
            content = "Noe gikk galt..."

        return render(request, 'home.html', {'content': content, 'graph': graph})

def about(request):
    return render(request, 'about.html', {})

# python manage.py runserver