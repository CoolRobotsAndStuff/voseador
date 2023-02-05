from voseador import Voseador

voseador = Voseador()

vos_verb = voseador.vos_from_vosotros(mood="indicativo", tense="presente", infinitivo="comer", vosotros_verb="coméis")

print(vos_verb)