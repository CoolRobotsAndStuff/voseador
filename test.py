from verbecc import Conjugator
import pprint
from voseador import Voseador


voseador = Voseador()

pp = pprint.PrettyPrinter()

cg = Conjugator(lang='es')
conjugation = cg.conjugate("callar")

conjugation = voseador.add_vos_to_verbecc_conjugation(conjugation)

pp.pprint(conjugation["moods"])