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

import asyncio
import base64

import motor.motor_asyncio

from .APIsicX import async_searcher


class GeminiLatest:
    def init(
        self,
        api_key: str = None,
        mongo_url: str=None,
        api_base="https://generativelanguage.googleapis.com",
        version: str="v1beta",
        model: str="models/gemini-1.0-pro",
        content: str="generateContent",
        user_id: int=None,
        oracle_base: str = None,
    ):
        self.api_key = api_key
        self.api_base = api_base
        self.version = version
        self.model = model
        self.content = content
        self.user_id = user_id
        self.oracle_base = oracle_base
        self.mongo_url = mongo_url
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_url)
        self.db = self.client.tiktokbot
        self.collection = self.db.users

    def _close(self):
        self.client.close()

    async def __get_response_gemini(self, query: str = None):
        try:
            gemini_chat = await self._get_gemini_chat_from_db()
            gemini_chat.append({"role": "user", "parts": [{"text": query}]})
            api_method = f"{self.api_base}/{self.version}/{self.model}:{self.content}?key={self.api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {"contents": gemini_chat}

            response = await async_searcher.search(
                api_method, post=True, headers=headers, json=payload, re_json=True
            )
            # response = requests.post(api_method, headers=headers, json=payload)

            if "error" in response:
                return "Error responding", gemini_chat

            answer = (
                response.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )

            gemini_chat.append({"role": "model", "parts": [{"text": answer}]})
            await self._update_gemini_chat_in_db(gemini_chat)
            return answer, gemini_chat
        except Exception as e:
            error_msg = f"Error response: {e}"
            return error_msg, gemini_chat

    async def _get_gemini_chat_from_db(self):
        get_data_user = {"user_id": self.user_id}
        document = await self.collection.find_one(get_data_user)
        return document.get("gemini_chat", []) if document else []

    async def _update_gemini_chat_in_db(self, gemini_chat):
        get_data_user = {"user_id": self.user_id}
        document = await self.collection.find_one(get_data_user)
        if document:
            await self.collection.update_one(
                {"_id": document["_id"]}, {"$set": {"gemini_chat": gemini_chat}}
            )
        else:
            await self.collection.insert_one(
                {"user_id": 6000000 + self.user_id, "gemini_chat": gemini_chat}
            )

    async def _clear_history_in_db(self):
        unset_clear = {"gemini_chat": None}
        return await self.collection.update_one(
            {"user_id": self.user_id}, {"$unset": unset_clear}
        )
#############################----Oracle----##################################

    async def __get_response_oracle(self, query: str = None):
        try:
            oracle_chat = await self._get_oracle_chat_from_db()

            if await self._check_oracle_chat__db():
                oracle_chat.append({"role": "user", "parts": [{"text": query}]})
            else:
                await self._set_oracle_chat_in_db(oracle_chat)
                oracle_chat.append(
                    {
                        "role": "user",
                        "parts": [{"text": self.oracle_base + f"\n\n" + query}],
                    }
                )

            api_method = f"{self.api_base}/{self.version}/{self.model}:{self.content}?key={self.api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {"contents": oracle_chat}

            response = await async_searcher.search(
                api_method, post=True, headers=headers, json=payload, re_json=True
            )

            if "error" in response:
                return "Error responding", oracle_chat

            answer = (
                response.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )

            if "I am a large language model, trained by Google." in answer:
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [
                        {"role": "user", "parts": [{"text": self.oracle_base}]}
                    ]
                }
                response = await async_searcher.search(
                    api_method, post=True, headers=headers, json=payload, re_json=True
                )

                if "error" in response:
                    return "Error responding", oracle_chat

                try:
                    answer = (
                        response_data.get("candidates", [{}])[0]
                        .get("content", {})
                        .get("parts", [{}])[0]
                        .get("text", "")
                    )
                    oracle_chat.append({"role": "model", "parts": [{"text": answer}]})
                    await self._update_oracle_chat_in_db(oracle_chat)
                    return answer, oracle_chat
                except Exception as e:
                    await self._clear_oracle_history_in_db()
                    error_msg = f"Error response: {e}"
                    return error_msg, oracle_chat
            else:
                oracle_chat.append({"role": "model", "parts": [{"text": answer}]})
                await self._update_oracle_chat_in_db(oracle_chat)
                return answer, oracle_chat
        except Exception as e:
            await self._clear_oracle_history_in_db()
            error_msg = f"Error response: {e}"
            return error_msg, oracle_chat

    async def _get_oracle_chat_from_db(self):
        get_data_user = {"user_id": 6000000 + self.user_id}
        document = await self.collection.find_one(get_data_user)
        return document.get("oracle_chat", []) if document else []

    async def _check_oracle_chat__db(self):
        get_data_user = {"user_id": 6000000 + self.user_id}
        document = await self.collection.find_one(get_data_user)
        return bool(document)

    async def _set_oracle_chat_in_db(self, oracle_chat):
        get_data_user = {"user_id": 6000000 + self.user_id}
        document = await self.collection.find_one(get_data_user)
        if not document:
            try:
                await self.collection.insert_one(
                    {"user_id": 6000000 + self.user_id, "oracle_chat": self.oracle_base}
                )
            except Exception as e:
                error_msg = f"Error response: {e}"
                return error_msg, oracle_chat
            return None, oracle_chat
        else:
            return oracle_chat

    async def _update_oracle_chat_in_db(self, oracle_chat):
        get_data_user = {"user_id": 6000000 + self.user_id}
        document = await self.collection.find_one(get_data_user)
        if document:
            try:
                await self.collection.update_one(
                    {"_id": document["_id"]}, {"$set": {"oracle_chat": oracle_chat}}
                )
            except Exception as e:
                error_msg = f"Error response: {e}"
                return error_msg, oracle_chat
        else:
            await self.collection.insert_one(
                {"user_id": 6000000 + self.user_id, "oracle_chat": self.oracle_base}
            )

    async def _clear_oracle_history_in_db(self):
        unset_clear = {"oracle_chat": None}
        return await self.collection.update_one(
            {"user_id": 6000000 + self.user_id}, {"$unset": unset_clear}
        )
