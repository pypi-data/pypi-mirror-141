#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import date
from typing import List, Dict, Optional

import aiohttp
import ujson

__all__ = ["EwbLoadShapeInfoProvider"]

from zepben.auth.client import create_token_fetcher

from zepben.opendss import LoadShapeInfoProvider, LoadShapeInfo


class EwbLoadShapeInfoProvider(LoadShapeInfoProvider):
    _load_api_date_format = "%Y-%m-%d"

    def __init__(
            self,
            host: str,
            port: int,
            secure: bool = False,
            username: Optional[str] = None,
            password: Optional[str] = None,
            client_id: Optional[str] = None
    ):
        self.host = host
        self.port = port
        if secure:
            authenticator = create_token_fetcher(f"https://{host}/ewb/auth")
            authenticator.token_request_data.update(
                {
                    "grant_type": "password",
                    "username": username,
                    "password": password,
                    "scope": "offline_access openid profile email",
                    "client_id": client_id
                }
            )
            authenticator.refresh_request_data.update({
                "grant_type": "refresh_token",
                "scope": "offline_access openid profile email",
                "client_id": client_id
            })

            self.token = authenticator.fetch_token()
        else:
            self.token = ''

    async def get_load_shape_info(
            self,
            conducting_equipment_mrid: str,
            from_date: date,
            to_date: date
    ) -> LoadShapeInfo:
        load_result = await self._get_load_profile(conducting_equipment_mrid, from_date, to_date)

        max_abs_val = 0
        values = []
        for result in load_result:
            for series in result["series"]:
                for series_item in series:
                    for reading in series_item['energy']["readings"]:
                        val = reading["values"]["kwNet"]
                        abs_val = abs(val)
                        if abs_val > max_abs_val:
                            max_abs_val = abs_val
                        values.append(val)

        return LoadShapeInfo(
            max_abs_val,
            1.0,
            [v if max_abs_val == 0 else v / max_abs_val for v in values],
            0.5
        )

    async def _get_load_profile(self, from_asset_mrid: str, from_date: date, to_date: date) -> List[Dict]:
        async with aiohttp.ClientSession(headers={'Authorization': self.token} if self.token else None, json_serialize=ujson.dumps) as session:
            async with session.get(url=f'{"https" if self.token else "http"}://{self.host}:{self.port}/ewb/energy/profiles/api/v1/range/{from_asset_mrid}'
                                       f'/from-date/{from_date.strftime(EwbLoadShapeInfoProvider._load_api_date_format)}'
                                       f'/to-date/{to_date.strftime(EwbLoadShapeInfoProvider._load_api_date_format)}'
                                   ) as response:
                return (await response.json())["results"] if response.status == 200 else []
