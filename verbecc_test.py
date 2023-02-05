from verbecc import Conjugator
from voseador import Voseador

conjugator = Conjugator(lang='es')
voseador = Voseador()

conjugation = conjugator.conjugate("haber")

conjugation = voseador.add_vos_to_verbecc_conjugation(conjugation)

print(conjugation["moods"])