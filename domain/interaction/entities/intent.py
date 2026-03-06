from enum import Enum


class UserIntent(Enum):
    ATTEND = "ATTEND"
    CANCEL = "CANCEL"
    QUERY_STAT = "QUERY_STAT"
    NOTIFY_AGAIN = "NOTIFY_AGAIN"
    GET_HELP = "GET_HELP"
    REGISTER = "REGISTER"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def from_text(cls, text: str) -> "UserIntent":
        if not text:
            return cls.UNKNOWN

        t = text.strip()

        # 使用對照表（Mapping），增加可讀性
        keywords = {
            cls.ATTEND: ["要", "參加", "+1", "yes", "好"],
            cls.CANCEL: ["不要", "取消", "-1", "no"],
            cls.QUERY_STAT: ["統計", "名單", "誰要來"],
            cls.NOTIFY_AGAIN: ["發出召集令", "通知"],
            cls.GET_HELP: ["指令", "幫助", "help"],
            cls.REGISTER: ["註冊", "註冊Admin"],
        }

        matches = [intent for intent, kws in keywords.items() if t in kws]

        # 核心邏輯：必須「剛好只有一個」吻合才回傳該 Intent，否則一律 UNKNOWN
        if len(matches) == 1:
            return matches[0]

        return cls.UNKNOWN
