from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent, JoinEvent, LikeEvent, ShareEvent, FollowEvent
from colorama import Fore, Style, init
import asyncio
import playtext
import time
import os

init(autoreset=True)  # Tự động reset màu terminal

id = input("Nhập ID phòng TikTok: ")
client: TikTokLiveClient = TikTokLiveClient(unique_id=id)

# =======================
# 📌 Ghi log vào file
# =======================
log_file = "history.log"

def log_event(event_type, message):
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {event_type}: {message}\n")

# =======================
# 📌 Xử lý sự kiện
# =======================

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    message = f"Kết nối thành công! @{event.unique_id} (Room ID: {client.room_id})"
    print(Fore.GREEN + "✅ " + message)
    log_event("Kết nối", message)

@client.on(FollowEvent)
async def on_follow(event: FollowEvent):
    message = f"{event.user.nickname} đã theo dõi 🎉"
    print(Fore.YELLOW + f"[{event.user.nickname}]: " + Fore.CYAN + "Đã theo dõi 🎉")
    log_event("Follow", message)

@client.on(ShareEvent)
async def on_share(event: ShareEvent):
    message = f"{event.user.nickname} đã chia sẻ livestream 🎉"
    print(Fore.YELLOW + f"[{event.user.nickname}]: " + Fore.CYAN + "Đã chia sẻ 🎉")
    log_event("Share", message)

@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    message = f"{event.user.nickname} đã like ❤️ x {event.count}"
    print(Fore.YELLOW + f"[{event.user.nickname}]: " + Fore.RED + f"Đã like ❤️ x {event.count}")
    log_event("Like", message)

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    count = event.repeat_count if event.gift.streakable and not event.streaking else 1
    message = f"{event.user.nickname} gửi quà 🎁 {event.gift.name} x {count}"
    print(Fore.YELLOW + f"[{event.user.nickname}]: " + Fore.MAGENTA + f"Gửi quà 🎁 {event.gift.name} x {count}")
    log_event("Gift", message)

@client.on(JoinEvent)
async def on_join(event: JoinEvent):
    nickname = event.user.nickname or "Người dùng ẩn danh"
    message = f"{nickname} đã tham gia phòng!"
    print(Fore.MAGENTA + f"[{nickname}]: " + Fore.CYAN + "Tham gia phòng!")
    log_event("Join", message)

# =======================
# 📌 Xử lý bình luận và đọc bình luận
# =======================

# Danh sách phản hồi tự động
auto_reply = {
    "xin chào": "Chào bạn! Chúc bạn xem livestream vui vẻ!",
    "bot đâu": "Mình đây! Hãy chat với mình nhé!",
    "mấy giờ rồi": f"Bây giờ là {time.strftime('%H:%M:%S')}"
}

async def on_comment(event: CommentEvent):
    user = event.user.nickname
    comment = event.comment.lower()

    print(Fore.BLUE + f"[{user}]: " + Fore.GREEN + comment)
    log_event("Comment", f"{user}: {comment}")

    # Tự động phản hồi nếu có từ khóa
    for keyword, response in auto_reply.items():
        if keyword in comment:
            await play(response)
            print(Fore.YELLOW + f"🤖 Bot: {response}")
            return

    # Phát âm thanh bình luận
    await play(comment)

client.add_listener(CommentEvent, on_comment)

# =======================
# 📌 Phát giọng nói bình luận
# =======================

async def play(text: str):
    if playtext.runing:
        playtext.runing = False
        asyncio.create_task(playtext.play(text, speed=1.2))  # Tăng tốc độ giọng đọc

# =======================
# 📌 Chạy bot
# =======================

if __name__ == '__main__':
    print(Fore.GREEN + "🚀 Đang kết nối tới TikTok Live...")
    client.run()
