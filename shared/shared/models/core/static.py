from django.db import models

class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'regions'
        managed = False

class Country(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    phonecode = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    currency_name = models.CharField(max_length=255, blank=True, null=True)
    currency_symbol = models.CharField(max_length=255, blank=True, null=True)
    emoji = models.CharField(max_length=191, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)

    class Meta:
        db_table = 'countries'
        managed = False

    def __str__(self):
        return self.name

class State(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, db_column='country_id')

    class Meta:
        db_table = 'states'
        managed = False

    def __str__(self):
        return self.name  

class City(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, db_column='state_id')
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, db_column='country_id')

    class Meta:
        db_table = 'cities'
        managed = False
        
    def __str__(self):
        return self.name 

class Currency(models.Model):
    id = models.BigIntegerField(primary_key=True)
