from celery import shared_task
from .services import prune_stale_users_from_room as _prune_stale_users_from_room


@shared_task(name="dots_connect_deta.board.prune_stale_users_from_room")
def prune_stale_users_from_room():
    _prune_stale_users_from_room()
