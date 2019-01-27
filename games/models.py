from django.db import models
import uuid as uuid_lib
from django.utils import timezone


class Team(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=64, blank=False)
    is_basketball_team = models.BooleanField()


class Player(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=64, blank=False)
    team = models.ForeignKey(Team, related_name="team_players", on_delete=models.SET_NULL)


