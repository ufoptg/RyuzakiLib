#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2020-2023 (c) Randy W @xtdevs, @xtsea
#
# from : https://github.com/TeamKillerX
# Channel : @RendyProjects
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from io import BytesIO
from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message

# Lazy session - created only when first needed and inside an event loop
_aiosession = None


async def get_session():
    global _aiosession
    if _aiosession is None or _aiosession.closed:
        _aiosession = ClientSession()
    return _aiosession


class CarbonSuper:
    def __init__(self, code: str, color: str = None):
        self.code = code
        self.color = color

    async def make_carbon(self, ryuzaki: bool = None):
        url = "https://carbonara.solopov.dev/api/cook"
        session = await get_session()

        if ryuzaki and self.color:
            payload = {"code": self.code, "backgroundColor": self.color}
        else:
            payload = {"code": self.code}

        async with session.post(url, json=payload) as resp:
            if resp.status != 200:
                raise Exception(f"Carbon API error: {resp.status}")
            image = BytesIO(await resp.read())
            image.name = "carbon.png"
            return image

    async def close(self):
        """Optional: call this on bot shutdown"""
        global _aiosession
        if _aiosession and not _aiosession.closed:
            await _aiosession.close()
            _aiosession = None
