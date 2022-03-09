from operator import index
import os
from django.conf import settings
from django.apps import apps
from unidecode import unidecode
conf = {
    'INSTALLED_APPS': [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.sitemaps',
        'django.contrib.sites',
        'django.contrib.staticfiles',
        'kifwat_scrapy.demo.app',
    ],
    'DATABASES': {
         'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'demodatabase',
        'USER': 'root', 
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306'
     },
    },
    'TIME_ZONE': 'UTC',
    'SECRET_KEY' : 'django-insecure-r+r$dw1%v9t!y@#jp^th2wm9=h7k_nkgbl!fj%l3!t)p52s1d%'
}

settings.configure(**conf)
apps.populate(settings.INSTALLED_APPS)

# from demo.app.models import root,subroot
# newdata = root(name='ramehs')
# newdata.save()
# sdata = subroot(root=newdata)
# sdata.save()
# data = root.objects.all()
# print(data)
from kifwat_scrapy.demo.app.models import scrapData
def fixField(field):
    field = unidecode(field)
    startwith = [
        ('- ',''),
        ('+ ','plus_'),
        # ("Répartition selon l'âge'",'Repartition_selon_lage'),
        # ("Répartition selon l'activité (Hommes)",'Repartition_selon_lactivite_Hommes'),
        # ("Répartition selon l'activité (Femmes)",'Repartition_selon_lactivite_Femmes'),
        ]
    for data in startwith:
        if field.startswith(data):
            field = field.replace(data[0],data[1],1)
        else:
            if " - " in field:
                field = field.replace(" - ",'_')
                field = f'key_{field}' 
        if field[:1].isnumeric():
            field = field.replace(field[:1],"key_"+field[:1])
    replace = [
        ("'",''),
        (" ",'_'),
        ("(",''),
        (")",''),
        ("dept",'department'),
    ]
    for d in replace:
        field = field.replace(d[0],d[1])
    return field

def uploaddata(data):
    print(data)
    fdata = {}
    fields = [f.name for f in scrapData._meta.fields]
    for key,value in data.items():
        nkey = fixField(key)
        lowerfield = [field.lower() for field in fields]
        if nkey.lower() in lowerfield:
            index = lowerfield.index(nkey.lower())
            fdata[fields[index]] = value
    # newda,created = scrapData.objects.get_or_create(**fdata)
    # print(created)
    try:
        newda = scrapData.objects.get(**fdata)
    except:
        newda = scrapData(**fdata) 
        newda.clean()
        newda.save()
    # input('press any key')
