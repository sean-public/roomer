from django.db import models


class DPU(models.Model):
    '''The DPU model stores information about a specific
       Depth Processing Unit, which is a hardware device
       stored above doorways.

       The hardware ID number is used as primary key (required,
       unique, and not auto-incrementing).

       If the device is not assigned to a location yet the
       doorway field can be set to NULL. Same goes if a doorway
       is deleted; the cascading delete will set it to NULL
       but keep the DPU otherwise intact.

       A "nickname" is optional, we fall back to using its
       hardware ID in string representations.

       NB: they can be added/removed/relocated physically
       at any time
    '''

    id = models.PositiveIntegerField(primary_key=True)
    active = models.BooleanField(default=True)
    doorway = models.ForeignKey(
        to='Doorway',
        on_delete=models.SET_NULL,
        null=True,
        help_text='[optional] location where the device is installed')

    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='[optional] nickname for the device')

    def __str__(self):
        return self.name if self.name else f'DPU {self.id}'

class Space(models.Model):
    ''' Spaces are areas that we want to track occupancy in
        and are connected by doorways. The "name" field is
        required.
        A space cannot be deleted while it still has doorways
        assigned to it. The client UI should enforce that
        design consideration on hard deletes.
    '''

    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Doorway(models.Model):
    ''' A Doorway model is used to specify a location that
        an DPU can be positioned at. It has a "direction" such
        that people approaching the doorway, you are said to be
        "leaving from" one space and "entering into" another.
        See the README for details on how this works.

        Since this is essentially a join table that helps describe
        a graph of connected spaces, some thought about enforcing
        reasonable constraints on the client side is advised. Without
        any checks, it would be possible to make some really bizarre
        layouts (i.e. a Klein bottle room that enters into itself).

        Both exiting_to and entering_to are required.
    '''

    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='[optional] nickname for the device')

    entering_to = models.ForeignKey(
        to='Space',
        on_delete=models.PROTECT,
        related_name='doorway_entering_to',
        help_text='the space that this doorway enters into (and the sensor points into)')

    exiting_to = models.ForeignKey(
        to='Space',
        on_delete=models.PROTECT,
        related_name='doorway_exiting_to',
        help_text='the space that this doorway exits to (and is not visible to the sensor)')

    def __str__(self):
        return self.name

class Occupancy(models.Model):
    ''' A history of occupancy counts for spaces. Allows
        for fast lookups at any given time (or the current
        state) and pulling ranges for charts & stats.
    '''

    space = models.ForeignKey('Space', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('space', 'timestamp')
        indexes = [
            models.Index(fields=['space']),
            models.Index(fields=['timestamp']),
        ]
