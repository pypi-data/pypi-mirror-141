import asyncio
import contextvars
from dataclasses import dataclass
from typing import Any, AsyncContextManager, Awaitable, Callable, Dict, List

from pydantic import BaseModel
from arkitekt.api.schema import TemplateFragment, WidgetInput
from arkitekt.arkitekt import Arkitekt
from arkitekt.messages import Provision
from arkitekt.structures.registry import StructureRegistry
from arkitekt.definition.registry import DefinitionRegistry
from arkitekt.agents.base import BaseAgent
from arkitekt.postmans.base import BasePostman
from koil import Koil, unkoil
import koil


class BaseApp(BaseModel):
    arkitekt: Arkitekt
    structure_registry: StructureRegistry
    definition_registry: DefinitionRegistry
    agent: BaseAgent
    postman: BasePostman
    additional_contexts: List[AsyncContextManager] = []
    koil = Koil()

    def register(
        self,
        widgets: Dict[str, WidgetInput] = {},
        interfaces: List[str] = [],
        on_provide: Callable[[Provision, TemplateFragment], Awaitable[Any]] = None,
        on_unprovide: Callable[[], Awaitable[Any]] = None,
        structure_registry: StructureRegistry = None,
        **actorparams,
    ) -> None:
        """
        Register a new function
        """

        def real_decorator(function):
            # Simple bypass for now
            def wrapped_function(*args, **kwargs):
                return function(*args, **kwargs)

            self.definition_registry.register(
                function,
                widgets=widgets,
                interfaces=interfaces,
                structure_registry=structure_registry,
                on_provide=on_provide,
                on_unprovide=on_unprovide,
                **actorparams,
            )

        return real_decorator

    def run(self, *args, **kwargs) -> None:
        """
        Run the application.
        """
        unkoil(self.arun, *args, **kwargs)

    async def arun(self) -> None:
        """
        Run the application.
        """
        async with self:
            await asyncio.sleep(0.01)
            print("Running")

    async def __aenter__(self):
        for context in self.additional_contexts:
            await context.__aenter__()  # ATTENTION: GATHER DOES NOT COPY THE CONTEXT VARIABLES

        await self.agent.__aenter__()
        await self.postman.__aenter__()
        await self.arkitekt.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)
        await self.agent.__aexit__(exc_type, exc_val, exc_tb)
        await self.postman.__aexit__(exc_type, exc_val, exc_tb)
        await self.arkitekt.__aexit__(exc_type, exc_val, exc_tb)
        print("nananan")
        for context in self.additional_contexts:
            await context.__aexit__(exc_type, exc_val, exc_tb)
            print("sss")

        print("ENtering here?")

    def __enter__(self):
        self.koil.__enter__()
        unkoil(self.__aenter__)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        unkoil(self.__aexit__, exc_type, exc_val, exc_tb)

    class Config:
        arbitrary_types_allowed = True
