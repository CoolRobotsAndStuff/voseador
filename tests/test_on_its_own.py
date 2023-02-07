import copy
import pytest

import voseador

vs = voseador.Voseador()

# -er tests

def test_indicativo_presente_comer():
    assert vs.vos_from_vosotros("indicativo", 
                                "presente", 
                                "comer", 
                                "coméis") == "comés"

assert vs.vos_from_vosotros("imperativo", 
                            "afirmativo", 
                            "comer", 
                            "comed") == "comé"

assert vs.vos_from_vosotros("imperativo", 
                            "negativo", 
                            "comer", 
                            "no comáis") == "no comás"

assert vs.vos_from_vosotros("subjuntivo", 
                            "pretérito_perfecto", 
                            "comer", 
                            "hayáis comido") == "hayás comido"

assert vs.vos_from_vosotros("subjuntivo", 
                            "presente", 
                            "comer", 
                            "comáis") == "comás"


assert vs.vos_from_vosotros("subjuntivo", 
                            "PRETERITO_perfectó", 
                            "comer", 
                            "hayais comido") == "hayás comido"

# -ar tests

assert vs.vos_from_vosotros("indicativo", 
                            "presente", 
                            "amar", 
                            "amáis") == "amás"

assert vs.vos_from_vosotros("imperativo", 
                            "afirmativo", 
                            "amar", 
                            "amad") == "amá"

assert vs.vos_from_vosotros("imperativo", 
                            "negativo", 
                            "amar", 
                            "no améis") == "no amés"

assert vs.vos_from_vosotros("subjuntivo", 
                            "pretérito_perfecto", 
                            "amar", 
                            "hayáis amado") == "hayás amado"

assert vs.vos_from_vosotros("subjuntivo", 
                            "presente", 
                            "amar", 
                            "améis") == "amés"


assert vs.vos_from_vosotros("subjuntivo", 
                            "PRETERITO_perfectó", 
                            "amar", 
                            "hayais amado") == "hayás amado"

# -ir tests

assert vs.vos_from_vosotros("indicativo", 
                            "presente", 
                            "morir", 
                            "morís") == "morís"

assert vs.vos_from_vosotros("imperativo", 
                            "afirmativo", 
                            "morir", 
                            "morid") == "morí"

assert vs.vos_from_vosotros("imperativo", 
                            "negativo", 
                            "morir", 
                            "no muráis") == "no murás"

assert vs.vos_from_vosotros("subjuntivo", 
                            "pretérito_perfecto", 
                            "morir", 
                            "hayáis muerto") == "hayás muerto"

assert vs.vos_from_vosotros("subjuntivo", 
                            "presente", 
                            "morir", 
                            "muraís") == "murás"


assert vs.vos_from_vosotros("subjuntivo", 
                            "PRETERITO_perfectó", 
                            "morir", 
                            "hayais muerto") == "hayás muerto"



my_moods = {

    "Infinitivo":"comer",

    "Indicativo":{
        "prEsenté":{
            "yo":"como",
            "tú":"comes",
            "vosotros":"coméis"
        },
        "pretérito perfecto simple":{
            "yo":"comí",
            "tú":"comiste",
            "vosotros":"comisteis"
        }
    },
    "Condicional":{
        "presente":{
            "yo" : "comería",
            "tú": "comerías",
            "vosotros": "comeríais"
        },
    }

}

my_moods_with_vos = copy.deepcopy(my_moods)

inf = my_moods["Infinitivo"]
for mood in my_moods.keys():
    if mood == "Infinitivo":
        continue
    for tense in my_moods[mood]:
        vosotros = my_moods[mood][tense]["vosotros"]
        if vs.needs_derivation_from_vosotros(mood, tense):
            my_moods_with_vos[mood][tense]["vos"] = vs.vos_from_vosotros(mood, tense, inf, vosotros)
        else:
            my_moods_with_vos[mood][tense]["vos"] = my_moods_with_vos[mood][tense]["tú"]

assert my_moods_with_vos == {
    "Infinitivo": "comer",
    "Indicativo": {
        "prEsenté": {
            "yo": "como",
            "tú": "comes",
            "vosotros": "coméis",
            "vos": "comés"
        },
        "pretérito perfecto simple": {
            "yo": "comí",
            "tú": "comiste",
            "vosotros": "comisteis",
            "vos": "comiste"
        }
    },
    "Condicional": {
        "presente": {
            "yo": "comería",
            "tú": "comerías",
            "vosotros": "comeríais",
            "vos": "comerías"
        }
    }
}

print("Everything looks great!")
