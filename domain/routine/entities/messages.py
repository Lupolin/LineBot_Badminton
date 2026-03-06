from dataclasses import dataclass


@dataclass
class BadmintonMessages:
    ASK_DEFAULT: str = (
        "嗨各位~\n這週五({date})\n"
        "我們照常在{location}打球，\n"
        "回復一下你會不會來吧，讓我們好抓人數喔~\n\n"
        "請回覆「要」或「不要」喔！"
    )

    ASK_TUESDAY: str = (
        "嗨嗨～再提醒一次！\n"
        "禮拜五({date} {time}) {location})\n"
        "目前還有些人沒回覆會不會來，幫個忙回覆一下 🙏\n"
        "人數掌握一下比較好排場次～\n\n"
        "請回覆「要」或「不要」喔！"
    )

    ASK_WEDNESDAY: str = (
        "後天就要打球啦～\n"
        "禮拜五({date} {time}) {location})！\n"
        "還沒回覆的，今天務必講一下要不要來，\n"
        "我們要安排場次、人數，不能再靠猜的了～\n"
        "再不說，真的會派人面對面來問你喔（不是開玩笑）👀\n\n"
        "請回覆「要」或「不要」喔！"
    )

    SUMMARY_TEMPLATE: str = (
        "羽球出席統計（{date}）\n\n"
        "✅ 參加：\n{attending_members}\n\n"
        "❌ 不參加：\n{not_attending_members}\n\n"
        "❓ 未回覆：\n{pending_members}"
    )
