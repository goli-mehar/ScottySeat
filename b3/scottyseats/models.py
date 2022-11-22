from django.db import models

class RoomModel(models.Model):
    roomname     = models.CharField(max_length=15)
    tablecount = models.IntegerField()
    seatscount = models.IntegerField()
    seatsposition = models.TextField()
    tablesposition = models.TextField()
    peoplecount = models.IntegerField()
    peopleposition = models.TextField()
    occupancy = models.TextField()
    person_or_chair = models.TextField()
    occupied = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()
    available = models.IntegerField()


    def __str__(self):
        return 'Entry(id=' + str(self.id) + ')'