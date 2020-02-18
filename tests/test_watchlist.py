#!/usr/bin/env python3.8
"""Exabeam UEBA API Client: Test Watchlist
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
from base_api_client import bprint, tprint
from base_api_client.models import Results

from exabeam_ueba_api_client import ExabeamApiClient


@pytest.mark.asyncio
async def test_get_watchlist_users():
    ts = time.perf_counter()

    bprint('Test: Get Notable Users')
    async with ExabeamApiClient(cfg=f'{getenv("CFG_HOME")}/exabeam_api_client.toml') as eac:
        watchlists = {'5accc39070e07300079d256c': 'High Risk Roles',
                      '5ab2bf4770e0730008a04fc2': 'Last Working Day',
                      '5b0d4d1c70e0730007bbd984': 'Last Working Day Contractor',
                      '59caa27d37f20cdfe9af07c2': 'Executive Users',
                      '5ab2be0770e0730008a04fc1': 'Work Status Change'}
        results = await eac.get_watchlist_users(watchlists=watchlists)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
