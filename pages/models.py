from django.db import models

#Asisiy sayt malumotlari<<<
class Site(models.Model):
    sites_name = models.CharField(max_length=25, null=True, blank=True)
    description = models.CharField(max_length=60, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    url1 = models.CharField(max_length=100, null=True, blank=True)
    url2 = models.CharField(max_length=100, null=True, blank=True)
    url3 = models.CharField(max_length=100, null=True, blank=True)
    tel = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    yt = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.sites_name
