# -*- coding: utf-8 -*-
from django.db import models


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.docfile.name.rsplit('/', 1)[1]


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


# The Malware table is emptier and destroyable
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
    filetype = models.CharField(db_column='filetype', max_length=255, blank=True, null=True)
    def __str__(self):
        return self.hash

    class Meta:
        managed = False
        db_table = 'malware'
        # ordering = ("type",)


class Dlltable(models.Model):
    malware_dll_id = models.SmallIntegerField()
    dll_name = models.CharField(max_length=80, primary_key=True)

    def __str__(self):
        return self.dll_name

    class Meta:
        managed = False
        db_table = 'dlltable'


class Malware2Dll(models.Model):
    id = models.AutoField(unique=True)
    hash = models.CharField(db_column='Hash', max_length=32)  # Field name made lowercase.
    malware_dll_id = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'malware2dll'
        unique_together = (('hash', 'malware_dll_id'),)

    def __str__(self):
        return self.unique_together
