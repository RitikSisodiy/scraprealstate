from operator import mod
from pyexpat import model
from django.db import models

# Create your models here.


class scrapData(models.Model):
    name = models.CharField(max_length=100,default=None,null=True)
    prix_bas_maison = models.BigIntegerField(default=0)
    prix_moyen_maison = models.BigIntegerField(default=0)
    prix_haut_maison = models.BigIntegerField(default=0)
    prix_bas_apparetement = models.BigIntegerField(default=0)
    prix_moyen_apparetement = models.BigIntegerField(default=0)
    prix_haut_apparetement = models.BigIntegerField(default=0)
    depuis_2_ans_maisons = models.CharField(max_length=100,default=None,null=True)
    depuis_2_ans_appartements= models.CharField(max_length=100,default=None,null=True)
    depuis_1_an_maisons = models.CharField(max_length=100,default=None,null=True)
    depuis_1_an_appartements = models.CharField(max_length=100,default=None,null=True)
    depuis_6_mois_maisons = models.CharField(max_length=100,default=None,null=True)
    depuis_6_mois_appartements = models.CharField(max_length=100,default=None,null=True)
    depuis_3_mois_maisons = models.CharField(max_length=100,default=None,null=True)
    depuis_3_mois_appartements = models.CharField(max_length=100,default=None,null=True)
    Maisons= models.CharField(max_length=100,default=None,null=True)
    Appartements= models.CharField(max_length=100,default=None,null=True)
    de_35m2 = models.TextField(null=True,blank=True)
    key_35m2_80m2= models.TextField(null=True,blank=True)
    key_80m2_110m2= models.TextField(null=True,blank=True)
    plus_de_150m2= models.TextField(null=True,blank=True)
    key_1_piece= models.TextField(null=True,blank=True)
    key_2_pieces= models.TextField(null=True,blank=True)
    key_3_pieces= models.TextField(null=True,blank=True)
    plus_4_pieces= models.TextField(null=True,blank=True)
    volume= models.TextField(null=True,blank=True)
    evolution= models.TextField(null=True,blank=True)
    Repartition_selon_lage= models.TextField(null=True,blank=True)
    Repartition_selon_lactivite_Hommes= models.TextField(null=True,blank=True)
    Repartition_selon_lactivite_Femmes= models.TextField(null=True,blank=True)
    Habitants= models.CharField(max_length=100,default=None,null=True)
    Population= models.CharField(max_length=100,default=None,null=True)
    Superficie= models.CharField(max_length=100,default=None,null=True)
    Marie= models.CharField(max_length=100,default=None,null=True)
    Logements= models.CharField(max_length=100,default=None,null=True)
    price_table= models.TextField(null=True,blank=True)
    region= models.CharField(max_length=100,default=None,null=True)
    department= models.CharField(max_length=100,default=None,null=True)
    city= models.CharField(max_length=100,default=None,null=True)
    quarter= models.CharField(max_length=100,default=None,null=True)
    street= models.CharField(max_length=100,default=None,null=True)
    top_city= models.IntegerField(max_length=100,default=0)
    zip_code= models.CharField(max_length=10,blank=True,null=True)
    updated_at= models.DateTimeField(auto_now=True)
    price_chart= models.TextField(null=True,blank=True)
    class Meta:
        db_table = "barometer_regions"
    def clean(self):
        print('inclean')
        for f in scrapData._meta.fields:
            if "BigIntegerField" in str(type(f)) or "IntegerField"  in str(type(f)):
                if isinstance(getattr(self,f.name),str) and not getattr(self,f.name).isnumeric():
                    # print("not string")
                    setattr(self,f.name,0)
   
