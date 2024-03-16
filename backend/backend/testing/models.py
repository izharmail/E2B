# from django.db import models
# from django.db.models import Q
# from django.core import validators
# from enum import Enum
#
# from api.enums import Choice
# from extensions.fields import ArbitraryDecimalField
#
#
# class BaseDbModel(models.Model):
#     class Meta:
#         abstract = True
#
#
# class ContainerDbModel(BaseDbModel):
#     pass
#
#
# class ElementDbModel(BaseDbModel):
#     container = models.ForeignKey(ContainerDbModel, on_delete=models.CASCADE, related_name='elements')
#     text = models.CharField(null=True)
#     num = models.IntegerField(null=True)
#     choice = models.CharField(null=True, choices=Choice.choices(Choice.FIRST, Choice.SECOND))
#
# class Choice2(Enum):
#     ONE = 1
#     TWO = 2
#     THREE = 3
#
# class Choice3(Enum):
#     ONE = 's1'
#     TWO = 's2'
#     THREE = 's3'
#
#
# class Test(models.Model):
#     class Meta:
#         constraints = []
#
#     num = models.IntegerField(null=True)
#     Meta.constraints.append(models.CheckConstraint(check=Q(num__in=[x.value for x in Choice2]), name='test_num'))
#
#     text = models.CharField(null=True)
#     Meta.constraints.append(models.CheckConstraint(check=Q(text__in=[x.value for x in Choice3]), name='test_text'))
#
#     dec = ArbitraryDecimalField(null=True)


# class Base(models.Model):
#     class Meta:
#         abstract = True
#
#
# class Office(Base):
#     pass
#
#
# class Company(Base):
#     office = models.OneToOneField(Office, on_delete=models.CASCADE, related_name='company', null=True)
#
#
# class Plane(Base):
#     pass
#
#
# class Flight(Base):
#     companies = models.ManyToManyField(Company, related_name='flights')
#     plane = models.ForeignKey(Plane, on_delete=models.CASCADE, related_name='flights', null=True)