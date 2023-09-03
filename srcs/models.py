from typing import Any, Optional

from pydantic import BaseModel


class Update(BaseModel):
    update_id: int
    message: Any
    edited_message: Optional[Any]
    channel_post: Optional[Any]
    edited_channel_post: Optional[Any]
    inline_query: Optional[Any]
    chosen_inline_result: Optional[Any]
    callback_query: Optional[Any]
    shipping_query: Optional[Any]
    pre_checkout_query: Optional[Any]
    poll: Optional[Any]