"""Web Resolver."""

import json
from typing import Sequence

import aiohttp
from aries_cloudagent.core.profile import Profile
from aries_cloudagent.resolver.base import (
    BaseDIDResolver,
    DIDNotFound,
    ResolverError,
    ResolverType,
)
from pydid import DID


class WebResolver(BaseDIDResolver):
    """Web Resolver."""

    def __init__(self):
        super().__init__(ResolverType.NATIVE)

    def __transform_to_url(self, did):
        """
        Transform did to url according to
        https://w3c-ccg.github.io/did-method-web/#read-resolve
        """

        as_did = DID(did)
        method_specific_id = as_did.method_specific_id
        if ":" in method_specific_id:
            # contains path
            url = method_specific_id.replace(":", "/")
        else:
            # bare domain needs /.well-known path
            url = method_specific_id + "/.well-known"

        return "https://" + url + "/did.json"

    @property
    def supported_methods(self) -> Sequence[str]:
        """Return list of supported methods."""
        return ["web"]

    async def setup(self, context):
        """Setup the did:web resolver (none required)."""

    async def _resolve(self, profile: Profile, did: str) -> dict:
        """Resolve did:web DIDs."""

        url = self.__transform_to_url(did)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    try:
                        return json.loads(await response.text())
                    except Exception as err:
                        raise ResolverError(
                            "Response was incorrectly formatted"
                        ) from err
                if response.status == 404:
                    raise DIDNotFound(f"No document found for {did}")
                raise ResolverError(
                    "Could not find doc for {}: {}".format(did, await response.text())
                )
