from operator import index
import os
from django.conf import settings
from django.apps import apps
from unidecode import unidecode
import os     
from dotenv import load_dotenv
import subprocess
load_dotenv()
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
        'app',
    ],
    'DATABASES': {
         'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'), 
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
     },
    },
    'TIME_ZONE': 'UTC',
    'SECRET_KEY' : 'django-insecure-r+r$dw1%v9t!y@#jp^th2wm9=h7k_nkgbl!fj%l3!t)p52s1d%'
}
settings.configure(**conf)
apps.populate(settings.INSTALLED_APPS)
process = subprocess.Popen("python manage.py migrate app", shell=True, stdout=subprocess.PIPE)
process.wait()

# from demo.app.models import root,subroot
# newdata = root(name='ramehs')
# newdata.save()
# sdata = subroot(root=newdata)
# sdata.save()
# data = root.objects.all()
# print(data)
from app.models import scrapData
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
