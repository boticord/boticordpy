from datetime import datetime


class CommentData:
    """Model that represents edited comment text data.

    Attributes
    -----------
        old : :class:`str` or :class:`None`
            Old comment text.
        new : :class:`str` or :class:`None`
            New comment text.
    """

    __slots__ = "old", "new"

    old: str or None
    new: str or None

    def __init__(self, raw_data):
        self.old = raw_data.get("old")
        self.new = raw_data.get("new")


class Comment:
    """Model that represents information about a comment.

    Attributes
    -----------
        raw_data : :class:`dict`
            Raw data from the Boticord API.
        user_id : :class:`int`
            ID of comment author.
        comment : :class:`str`
            Comment.
        at : :class:`datetime.datetime`
            The comment creation time.
    """

    __slots__ = "raw_data", "user_id", "comment", "at"

    raw_data: dict
    user_id: int
    comment: str
    at: datetime

    def __init__(self, raw_data):
        self.raw_data = raw_data["data"]
        self.user_id = int(self.raw_data["user"])
        self.comment = self.raw_data["comment"]
        self.at = datetime.fromtimestamp(self.raw_data["at"] / 1000)

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return (
            f'<{name} user_id={self.user_id} comment={self.comment}>'
        )


class EditedComment(Comment):
    """Model that represents information about edited comment.
    It is inherited from :class:`Comment`

    Attributes
    -----------
        comment : :class:`CommentData`
            Comment.
    """

    __slots__ = "raw_data", "user_id", "comment", "at"

    comment: CommentData

    def __init__(self, raw_data):
        super().__init__(raw_data)
        self.comment = CommentData(self.raw_data["comment"])

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return (
            f'<{name} user_id={self.user_id} comment={self.comment.new}>'
        )


class BotVote:
    """Model that represents information about bot's vote.

    Attributes
    -----------
        raw_data : :class:`dict`
            Raw data from the Boticord API.
        user_id : :class:`int`
            ID of user, who voted.
        at : :class:`datetime.datetime`
            Voting date.
    """

    __slots__ = "raw_data", "user_id", "at"

    raw_data: dict
    user_id: int
    at: datetime

    def __init__(self, raw_data):
        self.raw_data = raw_data["data"]
        self.user_id = int(self.raw_data["user"])
        self.at = datetime.fromtimestamp(self.raw_data["at"] / 1000)

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f'<{name} user_id={self.user_id}'
