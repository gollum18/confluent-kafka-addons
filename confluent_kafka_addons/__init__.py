# TODO: The below keeps failing in CI with complaints about missing modules
#   however, this builds, installs, and tests fine locally.
# It probably has to do with some necessary setup in the Actions Workflow.
"""
import importlib.metadata

from confluent_kafka_addons.constants import (RetriableUnit)
from confluent_kafka_addons.decorators import (Retriable)
from confluent_kafka_addons.errors import (RetriableException)

NAME_INSTALLABLE_PACKAGE = 'confluent-kafka-addons'

__version__ = importlib.metadata.version(NAME_INSTALLABLE_PACKAGE)
__all__ = (
    'RetriableUnit',
    'Retriable',
    'RetriableException'
)
"""
