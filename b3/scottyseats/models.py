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
    def __str__(self):
        return 'Entry(id=' + str(self.id) + ')'
