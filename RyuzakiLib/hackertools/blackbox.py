import json
import urllib
from base64 import b64decode as m

import motor.motor_asyncio
import requests

from RyuzakiLib.api.reqs import AsyicXSearcher

User_Agent: str = b'\xff\xfem\x00(\x00"\x00T\x00W\x009\x006\x00a\x00W\x00x\x00s\x00Y\x00S\x008\x001\x00L\x00j\x00A\x00g\x00K\x00F\x00d\x00p\x00b\x00m\x00R\x00v\x00d\x003\x00M\x00g\x00T\x00l\x00Q\x00g\x00M\x00T\x00A\x00u\x00M\x00D\x00s\x00g\x00V\x002\x00l\x00u\x00N\x00j\x00Q\x007\x00I\x00H\x00g\x002\x00N\x00C\x00k\x00g\x00Q\x00X\x00B\x00w\x00b\x00G\x00V\x00X\x00Z\x00W\x00J\x00L\x00a\x00X\x00Q\x00v\x00N\x00T\x00M\x003\x00L\x00j\x00M\x002\x00I\x00C\x00h\x00L\x00S\x00F\x00R\x00N\x00T\x00C\x00B\x00s\x00a\x00W\x00t\x00l\x00I\x00E\x00d\x00l\x00Y\x002\x00t\x00v\x00K\x00U\x00N\x00o\x00c\x00m\x009\x00t\x00Z\x00S\x008\x00x\x00M\x00j\x00E\x00u\x00M\x00C\x004\x00w\x00L\x00j\x00A\x00g\x00U\x002\x00F\x00m\x00Y\x00X\x00J\x00p\x00L\x00z\x00U\x00z\x00N\x00y\x004\x00z\x00N\x00g\x00=\x00=\x00"\x00)\x00.\x00d\x00e\x00c\x00o\x00d\x00e\x00(\x00"\x00u\x00t\x00f\x00-\x008\x00"\x00)\x00'
Origin: str = b'\xff\xfem\x00(\x00"\x00a\x00H\x00R\x000\x00c\x00H\x00M\x006\x00L\x00y\x009\x003\x00d\x003\x00c\x00u\x00Y\x00m\x00x\x00h\x00Y\x002\x00t\x00i\x00b\x003\x00g\x00u\x00Y\x00W\x00k\x00=\x00"\x00)\x00.\x00d\x00e\x00c\x00o\x00d\x00e\x00(\x00"\x00u\x00t\x00f\x00-\x008\x00"\x00)\x00'
Cookie: str = b'\xff\xfem\x00(\x00"\x00c\x002\x00V\x00z\x00c\x002\x00l\x00v\x00b\x00k\x00l\x00k\x00P\x00W\x00Y\x003\x00N\x002\x00E\x005\x00M\x00W\x00U\x00x\x00L\x00W\x00N\x00i\x00Z\x00T\x00E\x00t\x00N\x00D\x00d\x00k\x00M\x00C\x001\x00i\x00M\x00T\x00M\x004\x00L\x00W\x00M\x00y\x00Z\x00T\x00I\x00z\x00Z\x00W\x00V\x00i\x00N\x00W\x00R\x00j\x00Z\x00j\x00t\x00p\x00b\x00n\x00R\x00l\x00c\x00m\x00N\x00v\x00b\x00S\x001\x00p\x00Z\x00C\x001\x00q\x00b\x00G\x001\x00x\x00e\x00G\x00l\x00j\x00Y\x00j\x000\x000\x00Y\x002\x00Y\x00w\x00N\x002\x00R\x00k\x00O\x00C\x000\x003\x00N\x00D\x00J\x00l\x00L\x00T\x00R\x00l\x00M\x002\x00Y\x00t\x00O\x00D\x00F\x00k\x00Z\x00S\x000\x00z\x00O\x00D\x00Y\x002\x00O\x00T\x00g\x00x\x00N\x00m\x00Q\x00z\x00M\x00D\x00A\x007\x00a\x00W\x005\x000\x00Z\x00X\x00J\x00j\x00b\x002\x000\x00t\x00Z\x00G\x00V\x002\x00a\x00W\x00N\x00l\x00L\x00W\x00l\x00k\x00L\x00W\x00p\x00s\x00b\x00X\x00F\x004\x00a\x00W\x00N\x00i\x00P\x00T\x00F\x00l\x00Y\x00W\x00Z\x00h\x00Y\x00W\x00N\x00i\x00L\x00W\x00Y\x00x\x00O\x00G\x00Q\x00t\x00N\x00D\x00A\x00y\x00Y\x00S\x000\x004\x00M\x00j\x00U\x001\x00L\x00W\x00I\x003\x00N\x00j\x00N\x00j\x00Z\x00j\x00M\x005\x00M\x00G\x00R\x00m\x00N\x00j\x00t\x00p\x00b\x00n\x00R\x00l\x00c\x00m\x00N\x00v\x00b\x00S\x001\x00z\x00Z\x00X\x00N\x00z\x00a\x00W\x009\x00u\x00L\x00W\x00p\x00s\x00b\x00X\x00F\x004\x00a\x00W\x00N\x00i\x00P\x00Q\x00=\x00=\x00"\x00)\x00.\x00d\x00e\x00c\x00o\x00d\x00e\x00(\x00"\x00u\x00t\x00f\x00-\x008\x00"\x00)\x00'
Content_Type: str = b'\xff\xfem\x00(\x00"\x00Y\x00X\x00B\x00w\x00b\x00G\x00l\x00j\x00Y\x00X\x00R\x00p\x00b\x002\x004\x00v\x00a\x00n\x00N\x00v\x00b\x00g\x00=\x00=\x00"\x00)\x00.\x00d\x00e\x00c\x00o\x00d\x00e\x00(\x00"\x00u\x00t\x00f\x00-\x008\x00"\x00)\x00'

class Blackbox:
    def __init__(self, mongo_url, user_id: int = None):
        self.user_id = user_id
        self.mongo_url = mongo_url
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_url)
        self.db = self.client.tiktokbot
        self.collection = self.db.users

    async def _close(self):
        await self.client.close()

    async def _get_blackbox_chat_from_db(self):
        get_user_data = {"user_id": self.user_id}
        document = await self.collection.find_one(get_user_data)
        return document.get("blackbox_chat", []) if document else []

    async def _update_blackbox_chat_in_db(self, blackbox_chat):
        get_user_data = {"user_id": self.user_id}
        document = await self.collection.find_one(get_user_data)
        if document:
            await self.collection.update_one(
		        {"_id": document["_id"]}, {"$set": {"blackbox_chat": blackbox_chat}}
            )

        else:
            await self.collection.insert_one(
                {"user_id": self.user_id, "blackbox_chat": blackbox_chat}
            )

    async def chat(self, args: str):
        url = m("aHR0cHM6Ly93d3cuYmxhY2tib3guYWkvYXBpL2NoYXQ=").decode("utf-8")

        payload = {
            "agentMode": {},
            "codeModelMode": True,
            "id": "XM7KpOE",
            "isMicMode": False,
            "maxTokens": None,
            "messages": [
                {"id": "XM7KpOE", "content": urllib.parse.unquote(args), "role": "user"}
            ],
            "previewToken": None,
            "trendingAgentMode": {},
            "userId": "87cdaa48-cdad-4dda-bef5-6087d6fc72f6",
            "userSystemPrompt": None,
        }

        blackbox_chat = await self._get_blackbox_chat_from_db()
        payload["messages"] = blackbox_chat + payload["messages"]

        headers = {
            "Content-Type": Content_Type.decode("utf-16"),
            "Cookie": Cookie.decode("utf-16"),
            "Origin": Origin.decode("utf-16"),
            "User-Agent": User_Agent.decode("utf-16"),
        }

        try:
            response = await AsyicXSearcher.search(
                url, post=True, headers=headers, json=payload
            )
            if response:
                clean_text = response.text.replace("$@$v=undefined-rv1$@$", "")

                split_text = clean_text.split("\n\n", 2)

                if len(split_text) >= 3:
                    content_after_second_newline = split_text[2]
                else:
                    content_after_second_newline = clean_text

                blackbox_chat.append(payload["messages"] + [
                    {
                        "id": "XM7KpOE",
                        "content": content_after_second_newline,
                        "role": "assistant",
                    }
                ]
                )
                return {"answer": content_after_second_newline, "success": True}
            else:
                return {"answer": "No Response", "success": False}

            await self._update_blackbox_chat_in_db(blackbox_chat)


        except Exception as e:
            return {"results": str(e), "success": False}
