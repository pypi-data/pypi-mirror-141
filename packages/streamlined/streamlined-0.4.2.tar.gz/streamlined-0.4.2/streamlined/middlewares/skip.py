from functools import partial
from typing import Any, Awaitable, Dict

from ..common import (
    ACTION,
    AND,
    CONTRADICTION,
    DEFAULT_KEYERROR,
    IDENTITY_FACTORY,
    IS_DICT,
    IS_DICT_MISSING_KEY,
    IS_NONE,
    IS_NOT_CALLABLE,
    IS_NOT_DICT,
    NOOP,
    RETURN_FALSE,
    VALUE,
    WHEN,
)
from ..services import Scoped
from .action import Action
from .middleware import Context, Middleware


def _TRANSFORM_WHEN_NOT_DICT(value: Any) -> Dict[str, Any]:
    return {VALUE: value}


_MISSING_ACTION = partial(IS_DICT_MISSING_KEY, key=ACTION)


def _TRANSFORM_WHEN_MISSING_ACTION(value: Dict[str, Any]) -> Dict[str, Any]:
    value[ACTION] = NOOP
    return value


_MISSING_VALUE = partial(IS_DICT_MISSING_KEY, key=VALUE)


def _TRANSFORM_WHEN_MISSING_VALUE(value: Dict[str, Any]) -> Dict[str, Any]:
    value[VALUE] = RETURN_FALSE
    return value


def _VALUE_NOT_CALLABLE(value: Dict[str, Any]) -> bool:
    return IS_NOT_CALLABLE(value[VALUE])


def _TRANSFORM_WHEN_VALUE_NOT_CALLABLE(value: Dict[str, Any]) -> Dict[str, Any]:
    value[VALUE] = IDENTITY_FACTORY(value[VALUE])
    return value


class Skip(Middleware):
    @classmethod
    def verify(cls, value: Any) -> None:
        super().verify(value)

        if not IS_DICT(value):
            raise TypeError(f"{value} should be dict")

        if _MISSING_ACTION(value):
            raise DEFAULT_KEYERROR(value, ACTION)

        if _MISSING_VALUE(value):
            raise DEFAULT_KEYERROR(value, VALUE)

    def _init_simplifications(self) -> None:
        super()._init_simplifications()

        # `{'skip': None}` -> `{'skip': False}`
        self.simplifications.append((IS_NONE, CONTRADICTION))

        # `{'skip': <bool>}` -> `{'skip': IDENTITY_FACTORY(<bool>)}`
        self.simplifications.append((AND(IS_NOT_DICT, IS_NOT_CALLABLE), IDENTITY_FACTORY))

        # `{'skip': <any>}` -> `{'skip': {VALUE: <any>}}`
        self.simplifications.append((IS_NOT_DICT, _TRANSFORM_WHEN_NOT_DICT))

        # `{'skip': {VALUE: ...}}` -> `{'skip': {VALUE: ..., ACTION: NOOP}}`
        self.simplifications.append(
            (AND(IS_DICT, _MISSING_ACTION), _TRANSFORM_WHEN_MISSING_ACTION)
        )

        # `{'skip': {ACTION: ...}}` -> `{'skip': {VALUE: RETURN_FALSE, ACTION: ...}}`
        self.simplifications.append((AND(IS_DICT, _MISSING_VALUE), _TRANSFORM_WHEN_MISSING_VALUE))

        # `{'skip': {VALUE: <non-callable>, ACTION: ...}}`
        self.simplifications.append(
            (AND(IS_DICT, _VALUE_NOT_CALLABLE), _TRANSFORM_WHEN_VALUE_NOT_CALLABLE)
        )

    def _do_parse(self, value: Dict[str, Any]) -> Dict[str, Middleware]:
        self.verify(value)

        return {WHEN: Action(value[VALUE]), ACTION: Action(value[ACTION])}

    async def should_skip(self, context: Context) -> Awaitable[bool]:
        should_skip_action: Action = getattr(self, WHEN)
        scoped = await should_skip_action.apply_onto(context)
        skipped = scoped.getmagic(VALUE)
        context.scoped.setmagic(SKIP, skipped)
        return skipped

    async def when_skip(self, context: Context) -> Awaitable[Scoped]:
        action_when_skip: Action = getattr(self, ACTION)
        scoped = await action_when_skip.apply_into(context)
        return scoped.getmagic(VALUE)

    async def _do_apply(self, context: Context) -> Scoped:
        if await self.should_skip(context.replace_with_void_next()):
            await self.when_skip(context.replace_with_void_next())
        else:
            await context.next()
        return context.scoped


SKIP = Skip.get_name()
