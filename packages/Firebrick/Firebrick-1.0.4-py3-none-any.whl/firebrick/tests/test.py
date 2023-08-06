from django.urls import resolve, reverse
from django.test import Client


def get_reverse_url(name):
    if '/' not in name:
        return reverse(name)
    else:
        return name


class ResolveUrlTest:
    def test_url_is_resolved(self):   
        url = get_reverse_url(self.name)
        
        if '__func__' in dir(self.view):
            self.assertEquals(resolve(url).func, self.view.__func__)
        else:
            self.assertEquals(resolve(url).func.view_class, self.view)


class GetViewTest:
    def test_GET(self):
        client = Client()
        
        url = get_reverse_url(self.name)
        
        response = client.get(url)
        
        self.assertEquals(response.status_code, self.status)
        self.assertTemplateUsed(response, self.template)
