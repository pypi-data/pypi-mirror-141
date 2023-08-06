from __future__ import (
    annotations,
)

import logging
from asyncio import (
    gather,
)
from typing import (
    TYPE_CHECKING,
)
from uuid import (
    UUID,
)

from cached_property import (
    cached_property,
)
from dependency_injector.wiring import (
    Provide,
    inject,
)

from minos.common import (
    MinosConfig,
    ModelType,
    import_module,
)
from minos.networks import (
    EnrouteDecorator,
    Request,
    Response,
    ResponseException,
    enroute,
)

from .abc import (
    SnapshotRepository,
)

if TYPE_CHECKING:
    from ..entities import (
        RootEntity,
    )

logger = logging.getLogger(__name__)


class SnapshotService:
    """Snapshot Service class."""

    # noinspection PyUnusedLocal
    @inject
    def __init__(
        self,
        *args,
        config: MinosConfig = Provide["config"],
        snapshot_repository: SnapshotRepository = Provide["snapshot_repository"],
        **kwargs,
    ):
        self.config = config
        self.snapshot_repository = snapshot_repository

    @classmethod
    def __get_enroute__(cls, config: MinosConfig) -> dict[str, set[EnrouteDecorator]]:
        simplified_name = config.service.aggregate.rsplit(".", 1)[-1]
        return {
            cls.__get_one__.__name__: {enroute.broker.command(f"_Get{simplified_name}Snapshot")},
            cls.__get_many__.__name__: {enroute.broker.command(f"_Get{simplified_name}Snapshots")},
            cls.__synchronize__.__name__: {enroute.periodic.event("* * * * *")},
        }

    async def __get_one__(self, request: Request) -> Response:
        """Get one ``RootEntity`` instance.

        :param request: The ``Request`` instance that contains the instance identifier.
        :return: A ``Response`` instance containing the requested instances.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuid": UUID}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            instance = await self.type_.get(content["uuid"])
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting the instance: {exc!r}")

        return Response(instance)

    async def __get_many__(self, request: Request) -> Response:
        """Get many ``RootEntity`` instances.

        :param request: The ``Request`` instance that contains the instance identifiers.
        :return: A ``Response`` instance containing the requested instances.
        """
        try:
            content = await request.content(model_type=ModelType.build("Query", {"uuids": list[UUID]}))
        except Exception as exc:
            raise ResponseException(f"There was a problem while parsing the given request: {exc!r}")

        try:
            instances = await gather(*(self.type_.get(uuid) for uuid in content["uuids"]))
        except Exception as exc:
            raise ResponseException(f"There was a problem while getting the instances: {exc!r}")

        return Response(instances)

    @cached_property
    def type_(self) -> type[RootEntity]:
        """Load the concrete ``RootEntity`` class.

        :return: A ``Type`` object.
        """
        # noinspection PyTypeChecker
        return import_module(self.config.service.aggregate)

    # noinspection PyUnusedLocal
    async def __synchronize__(self, request: Request) -> None:
        """Performs a Snapshot synchronization every minute.

        :param request: A request containing information related with scheduling.
        :return: This method does not return anything.
        """
        logger.info("Performing periodic Snapshot synchronization...")
        await self.snapshot_repository.synchronize()
