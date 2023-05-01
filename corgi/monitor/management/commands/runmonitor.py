from django.conf import settings
from django.core.management.base import BaseCommand

from corgi.monitor.consumer import BrewUMBListener


class Command(BaseCommand):
    """Run Brew UMB monitor to listen on events on configured virtual topics."""

    help = __doc__

    def handle(self, *args: str, **options: dict[str, str]) -> None:
        if settings.UMB_BREW_MONITOR_ENABLED:
            try:
                BrewUMBListener.consume()
            except KeyboardInterrupt:
                pass
