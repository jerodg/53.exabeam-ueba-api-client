#!/usr/bin/env python3.8
"""Exabeam UEBA API Client: Test Auth
Copyright © 2019-2020 Jerod Gawne <https://github.com/jerodg/>

This program is free software: you can redistribute it and/or modify
it under the terms of the Server Side Public License (SSPL) as
published by MongoDB, Inc., either version 1 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
SSPL for more details.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

You should have received a copy of the SSPL along with this program.
If not, see <https://www.mongodb.com/licensing/server-side-public-license>."""
import time
from os import getenv

import pytest
from base_api_client.models import Results
from base_api_client.utils import bprint, tprint

from exabeam_ueba_api_client import ExabeamApiClient


@pytest.mark.asyncio
async def test_login():
    ts = time.perf_counter()

    bprint('Test: Login')
    async with ExabeamApiClient(cfg=f'{getenv("CFG_HOME")}/exabeam_api_client.toml') as eac:
        results = await eac.login()

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
