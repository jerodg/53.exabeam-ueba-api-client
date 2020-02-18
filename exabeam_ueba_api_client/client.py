#!/usr/bin/env python3.8
"""Exabeam UEBA API Client
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

import asyncio
import logging
from typing import NoReturn, Optional, Union
from uuid import uuid4

from base_api_client import BaseApiClient
from base_api_client.models import Results

from exabeam_ueba_api_client.models import NotableUsersQuery, WatchlistUsersQuery

logger = logging.getLogger(__name__)


class ExabeamApiClient(BaseApiClient):
    """Exabeam UEBA API Client"""
    SEM: int = 15  # This defines the number of parallel async requests to make.

    def __init__(self, cfg: Union[str, dict]):
        """Initializes Class

        Args:
            cfg (Union[str, dict]): As a str it should contain a full path
                pointing to a configuration file (json/toml). See
                config.* in the examples folder for reference.
            sem (Optional[int]): An integer that defines the number of parallel
                requests to make."""
        BaseApiClient.__init__(self, cfg=cfg)

        self.logged_in: bool = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type: None, exc_val: None, exc_tb: None) -> NoReturn:
        await BaseApiClient.__aexit__(self, exc_type, exc_val, exc_tb)

    async def login(self) -> Results:
        """

        Returns:
            results (Results):
        """
        payload = {'username': self.cfg['Auth']['Username'], 'password': self.cfg['Auth']['Password']}

        logger.debug('Logging in to Exabeam...')

        tasks = [asyncio.create_task(self.request(method='post',
                                                  end_point='/api/auth/login',
                                                  request_id=uuid4().hex,
                                                  json=payload))]
        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        self.logged_in = True

        return await self.process_results(results)

    async def get_notable_users(self, query: Optional[NotableUsersQuery] = NotableUsersQuery()) -> Results:
        """

        Args:
            query (OptionL[NotableUsersQuery]):

        Returns:
            results (Results):

        """
        if not self.logged_in:
            await self.login()

        logger.debug('Getting notable users from Exabeam...')

        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point='/uba/api/users/notable',
                                                  request_id=uuid4().hex,
                                                  params=query.dict()))]
        results = Results(data=await asyncio.gather(*tasks))

        logger.debug(f'-> Complete; Retrieved {len(results.data)}, notable users.')

        return await self.process_results(results, 'users')

    async def get_watchlist_users(self, watchlists: dict, query: Optional[WatchlistUsersQuery] = WatchlistUsersQuery()) -> Results:
        """

        Args:
            watchlists (dict): {<watchlist_id>: <watchlist_name>}
            query (OptionL[Query]):

        Returns:
            results (Results):

        """
        if not self.logged_in:
            await self.login()

        results = Results(data=[])

        for k, v in watchlists.items():
            logger.debug(f'Getting watchlist {k}: {v}, users from Exabeam...')
            tasks = [asyncio.create_task(self.request(method='get',
                                                      end_point=f'/uba/api/watchlist/assets/{k}/',
                                                      request_id=uuid4().hex,
                                                      params=query.dict()))]
            res = await self.process_results(Results(data=await asyncio.gather(*tasks)), 'items')
            for r in res.success:
                r['watchlist'] = v

            results.data.extend(res.data)
            results.success.extend(res.success)
            results.failure.extend(res.failure)

        logger.debug(f'-> Complete; Retrieved {len(results.data)}, watchlist users.')

        return results


if __name__ == '__main__':
    print(__doc__)
