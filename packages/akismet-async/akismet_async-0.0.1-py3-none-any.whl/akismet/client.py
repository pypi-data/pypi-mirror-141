from typing import Union, Optional

import httpx

from akismet.entities import Comment, SpamStatus, SubmissionType
from akismet.exceptions import (
    AkismetError,
    AkismetServerError,
    MissingApiKeyError,
    ParameterError,
)

USER_AGENT = "Akismet-Async/1.0"

AKISMET_CHECK_URL = "https://{api_key}.rest.akismet.com/1.1/comment-check"
AKISMET_SUBMIT_SPAM_URL = "https://{api_key}.rest.akismet.com/1.1/submit-spam"
AKISMET_SUBMIT_HAM_URL = "https://{api_key}.rest.akismet.com/1.1/submit-ham"
AKISMET_KEY_VERIFICATION_URL = "https://rest.akismet.com/1.1/verify-key"

AKISMET_VALID_PARAMETERS = {
    "blog",
    "user_ip",
    "user_agent",
    "referrer",
    "permalink",
    "content_type",
    "comment_author",
    "comment_author_email",
    "comment_author_url",
    "comment_content",
    "comment_date_gmt",
    "comment_post_modified_gmt",
    "blog_lang",
    "blog_charset",
    "is_test",
}


class Akismet:
    def __init__(self, api_key=None, blog=None, user_agent=None):
        self._http_client = httpx.AsyncClient()
        self._api_key = api_key
        self._blog = blog
        self._user_agent = f"{user_agent} | {USER_AGENT}" if user_agent else USER_AGENT

    async def check(self, comment: Union[Comment, dict]) -> SpamStatus:
        parameters = self._check_api_key_and_params(comment)
        resp = await self._http_client.post(
            AKISMET_CHECK_URL.format(api_key=self._api_key),
            data=parameters,
            headers={"User-Agent": self._user_agent},
        )
        result = resp.json()
        if result is False:
            return SpamStatus.HAM
        elif result is True:
            if resp.headers.get("X-Akismet-Pro-Tip") == "discard":
                return SpamStatus.DEFINITE_SPAM
            else:
                return SpamStatus.PROBABLE_SPAM
        else:
            return SpamStatus.UNKNOWN

    async def verify_key(self, blog: Optional[str] = None) -> bool:
        blog_url = blog or self._blog
        resp = await self._http_client.post(
            AKISMET_KEY_VERIFICATION_URL,
            data={"key": self._api_key, "blog": blog_url},
        )
        if resp.text == "valid":
            return True
        elif resp.text == "invalid":
            return False
        else:
            raise AkismetServerError(
                f"Akismet server returned an unexpected response: {resp.text}"
            )

    async def submit_spam(self, comment: Comment) -> None:
        parameters = self._check_api_key_and_params(comment)
        await self._submit(SubmissionType.SPAM, parameters)

    async def submit_ham(self, comment: Comment) -> None:
        parameters = self._check_api_key_and_params(comment)
        await self._submit(SubmissionType.HAM, parameters)

    async def _submit(self, submission_type: SubmissionType, params: dict) -> None:
        if submission_type == SubmissionType.SPAM:
            url = AKISMET_SUBMIT_SPAM_URL.format(api_key=self._api_key)
        else:
            url = AKISMET_SUBMIT_HAM_URL.format(api_key=self._api_key)

        resp = await self._http_client.post(
            url.format(api_key=self._api_key),
            data=params,
            headers={"User-Agent": self._user_agent},
        )

        if resp.text == "Thanks for making the web a better place.":
            return
        else:
            raise AkismetServerError(
                f"Akismet server returned an unexpected response: {resp.text}"
            )

    def _check_api_key_and_params(self, comment):
        if isinstance(comment, Comment):
            parameters = comment.to_dict()
        elif isinstance(comment, dict):
            parameters = comment
        else:
            raise AkismetError(
                "Must supply either Comment entity or parameters dictionary"
            )

        if self._api_key is None:
            raise MissingApiKeyError(
                "api_key must be set on the akismet object before calling any API methods."
            )
        if not parameters.get("blog"):
            if self._blog is None:
                raise ParameterError(
                    "blog is a required parameter if blog_url is not set on the akismet object"
                )
            parameters["blog"] = self._blog
        if not parameters.get("user_ip"):
            raise ParameterError("user_ip is a required parameter")
        if not parameters.get("user_agent"):
            raise ParameterError("user_agent is a required parameter")
        if not parameters.get("referrer"):
            raise ParameterError("referrer is a required parameter")
        for key in parameters.keys():
            if key not in AKISMET_VALID_PARAMETERS:
                raise ParameterError(f"{key} is not a recognised parameter")
        return parameters
