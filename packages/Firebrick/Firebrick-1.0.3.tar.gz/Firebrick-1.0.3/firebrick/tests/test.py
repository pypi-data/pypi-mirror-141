from django.urls import resolve, reverse


def get_reverse_url(name):
    if '/' not in name:
        return reverse(name)
    else:
        return name


class ResolveUrlTest:
    def test_url_is_resolved(self):
        self.client = Client()
        
        url = get_reverse_url(self.name)
        
        if '__func__' in dir(self.view):
            self.assertEquals(resolve(url).func, self.view.__func__)
        else:
            self.assertEquals(resolve(url).func.view_class, self.view)


class GetViewTest:
    def test_GET(self):
        self.client = Client()
        
        url = get_reverse_url(self.name)
        
        response = self.client.get(url)
        
        self.assertEquals(response.status_code, self.status)
        self.assertTemplateUsed(response, self.template)
