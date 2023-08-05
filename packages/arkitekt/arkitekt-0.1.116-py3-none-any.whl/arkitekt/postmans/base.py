from typing import Any, Dict, List, Optional
from arkitekt.postmans.transport.base import PostmanTransport
from arkitekt.messages import Assignation, Reservation, Unassignation, Unreservation
from arkitekt.api.schema import AssignationStatus, ReservationStatus, ReserveParamsInput


class BasePostman:
    """Postman


    Postmans are the the messengers of the arkitekt platform, they are taking care
    of the communication between your app and the arkitekt-server.

    needs to implement:
        broadcast: On assignation Update or on reservation update (non updated fields are none)


    """

    def __init__(self, transport: PostmanTransport) -> None:
        self.transport = transport
        self.transport.abroadcast = self.abroadcast

    async def aconnect(self):
        await self.transport.aconnect()

    async def abroadcast(self):
        raise NotImplementedError(
            "This needs to be overwritten by your Postman subclass"
        )

    async def adisconnect(self):
        await self.transport.adisconnect()

    async def __aenter__(self):
        await self.aconnect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.adisconnect()
        return self
