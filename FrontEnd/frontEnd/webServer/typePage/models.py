# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Dlltable(models.Model):
    malware_dll_id = models.SmallIntegerField(primary_key=True)
    dll_name = models.CharField(max_length=80)

    def __str__(self):
        return self.dll_name

    class Meta:
        managed = False
        db_table = 'dlltable'


class Element(models.Model):
    severity = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(db_column='OS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.CharField(db_column='CategoryID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rollupstatus = models.CharField(db_column='Rollupstatus', max_length=255, blank=True, null=True)  # Field name made lowercase.
    schemaversion = models.CharField(db_column='Schemaversion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=255, blank=True, null=True)  # Field name made lowercase.
    threatid = models.BigIntegerField(db_column='threatID', blank=True, null=True)  # Field name made lowercase.
    hash = models.CharField(db_column='HASH', primary_key=True, max_length=32)  # Field name made lowercase.
    unpackedmd5 = models.CharField(db_column='unpackedMD5', max_length=32, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.
    subtype = models.CharField(db_column='subType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'element'


class Malware(models.Model):
    severity = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(db_column='OS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.CharField(db_column='CategoryID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rollupstatus = models.CharField(db_column='Rollupstatus', max_length=255, blank=True, null=True)  # Field name made lowercase.
    schemaversion = models.CharField(db_column='Schemaversion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=255, blank=True, null=True)  # Field name made lowercase.
    threatid = models.BigIntegerField(db_column='threatID', blank=True, null=True)  # Field name made lowercase.
    hash = models.CharField(db_column='Hash', primary_key=True, max_length=32)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.
    subtype = models.CharField(db_column='subType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.hash

    class Meta:
        managed = False
        db_table = 'malware'
        # ordering = ("type",)


class Malware2Dll(models.Model):
    hash = models.CharField(db_column='Hash', primary_key=True, max_length=32)  # Field name made lowercase.
    malware_dll_id = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'malware2dll'
        unique_together = (('hash', 'malware_dll_id'),)
    
    def __str__(self):
        return self.unique_together
