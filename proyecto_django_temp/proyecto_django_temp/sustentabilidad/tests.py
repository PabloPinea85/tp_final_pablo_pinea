from django.test import TestCase
from django.urls import reverse


class PanelSustentabilidadTest(TestCase):
    """Pruebas basicas del panel web de sustentabilidad."""

    def test_el_panel_carga(self):
        """La pagina tiene que responder sin errores."""
        respuesta = self.client.get(reverse("panel_sustentabilidad"))
        self.assertEqual(respuesta.status_code, 200)

    def test_el_panel_muestra_las_plantas(self):
        """Tiene que aparecer cada planta y el total de emisiones."""
        respuesta = self.client.get(reverse("panel_sustentabilidad"))
        self.assertContains(respuesta, "Planta Norte")
        self.assertContains(respuesta, "Planta Este")
        self.assertContains(respuesta, "206.9")
