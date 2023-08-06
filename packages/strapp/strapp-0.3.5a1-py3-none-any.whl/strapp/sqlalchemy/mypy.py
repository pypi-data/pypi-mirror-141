from typing import Type
from mypy.plugin import DynamicClassDefContext, Plugin


class StrappSqlalchemyPlugin(Plugin):
    def get_dynamic_class_hook(self, fullname: str):
        if fullname == "strapp.sqlalchemy.model_base.declarative_base":
            return _dynamic_class_hook
        return None


def _dynamic_class_hook(ctx: DynamicClassDefContext) -> None:
    """Generate a TypedBase class when the declarative_base() is called."""
    try:
        from sqlalchemy.ext.mypy.plugin import _dynamic_class_hook as sqlalchemy_dynamic_class_hook
    except ImportError:
        pass
    else:
        sqlalchemy_dynamic_class_hook(ctx)


def plugin(_: str) -> Type[StrappSqlalchemyPlugin]:
    return StrappSqlalchemyPlugin
