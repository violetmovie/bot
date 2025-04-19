from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMember

from dispatcher import TOKEN
from bot.models import ChannelsToSubscribe


bot = Bot(token=TOKEN)




async def check_user_subscription(user_id: int) -> bool:
    results = {"342":True}
    chat_ids = list(ChannelsToSubscribe.objects.values_list("link", flat=True))
    for chat_id in chat_ids:
        try:
            chat_member: ChatMember = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            subscribed_statuses = {ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}
            results[chat_id] = chat_member.status in subscribed_statuses
        except Exception as e:
            print(f"❌ Error checking {chat_id}: {e}")
            results[chat_id] = False

    return all(results.values())

