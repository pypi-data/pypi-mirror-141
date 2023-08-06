from dataclasses import asdict, dataclass
from typing import Optional

from strenum import StrEnum


@dataclass(frozen=True)
class Comment:
    comment_content: str
    user_ip: str
    user_agent: str
    referrer: str
    permalink: Optional[str] = None
    content_type: Optional[str] = None
    comment_author: Optional[str] = None
    comment_author_email: Optional[str] = None
    comment_author_url: Optional[str] = None
    comment_date_gmt: Optional[str] = None
    comment_post_modified_gmt: Optional[str] = None
    blog: Optional[str] = None
    blog_lang: Optional[str] = None
    blog_charset: Optional[str] = None
    is_test: Optional[bool] = False

    def to_dict(self):
        return asdict(self)


class SpamStatus(StrEnum):
    HAM = "ham"
    UNKNOWN = "unknown"
    PROBABLE_SPAM = "probable_spam"
    DEFINITE_SPAM = "definite_spam"


class SubmissionType(StrEnum):
    HAM = "ham"
    SPAM = "spam"
