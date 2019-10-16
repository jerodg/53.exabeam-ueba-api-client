#!/usr/bin/env python3.8
"""Exabeam UEBA API Client: Models.Query
Copyright © 2019 Jerod Gawne <https://github.com/jerodg/>

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

from dataclasses import dataclass

from base_api_client.models.record import Record


@dataclass
class Query(Record):
    numberOfResults: int = 1000000


@dataclass
class NotableUsersQuery(Query):
    """
    Attributes:
        type (str):
        page (int):

    References:
        See your local documentation; https://myexabeam:port/uba/docs#!/api/getNotableUsers
    """
    unit: str = 'd'
    num: int = 1


if __name__ == '__main__':
    print(__doc__)
