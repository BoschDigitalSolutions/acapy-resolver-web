"""ACA-Py Resolver for did:web."""

from aries_cloudagent.config.injection_context import InjectionContext
from aries_cloudagent.resolver.did_resolver_registry import DIDResolverRegistry

from .resolver import WebResolver


async def setup(context: InjectionContext):
    """Setup the plugin."""
    registry = context.inject(DIDResolverRegistry)
    assert isinstance(registry, DIDResolverRegistry)
    registry.register(WebResolver())
