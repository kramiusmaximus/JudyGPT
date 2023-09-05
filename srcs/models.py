import datetime
from enum import Enum
from typing import Any, Optional, List

from pydantic import BaseModel, Field


class ChatPhoto(BaseModel):
    """
    This object represents a chat photo.
    https://core.telegram.org/bots/api#chatphoto
    """
    small_file_id: str = None
    big_file_id: str = None


class ChatPermissions(BaseModel):
    can_send_messages: Optional[bool] = None
    can_send_media_messages: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_views: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None


class Chat(BaseModel):  # Checked
    id: int
    type: str
    title: str = None
    username: str = None
    first_name: str = None
    last_name: str = None
    all_members_are_administrators: bool = None
    photo: ChatPhoto = None
    description: str = None
    invite_link: str = None
    pinned_message: Any = None  # TODO make this type Message
    permissions: ChatPermissions = None
    sticker_set_name: str = None
    can_set_sticker_set: bool = None


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str = None
    username: str = None
    language_code: str = None


class MessageEntityType(str, Enum):
    MENTION = 'mention'
    HASHTAG = 'hashtag'
    CASHTAG = 'cashtag'
    BOT_COMMAND = 'bot_command'
    URL = 'url'
    EMAIL = 'email'
    PHONE_NUMBER = 'phone_number'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    PRE = 'pre'
    TEXT_LINK = 'text_link'
    TEXT_MENTION = 'text_mention'


class MessageEntity(BaseModel):
    """
    This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.
    https://core.telegram.org/bots/api#messageentity
    """
    type: MessageEntityType = None
    offset: int = None
    length: int = None
    url: str = None
    user: 'User' = None


class Audio(BaseModel):
    """
    This object represents an audio file to be treated as music by the Telegram clients.
    https://core.telegram.org/bots/api#audio
    """
    file_id: str = None
    duration: int = None
    performer: str = None
    title: str = None
    mime_type: str = None
    file_size: int = None
    thumb: 'PhotoSize' = None


class Document(BaseModel):
    """
    This object represents a general file (as opposed to photos, voice messages and audio files).
    https://core.telegram.org/bots/api#document
    """
    file_id: str = None
    thumb: 'PhotoSize' = None
    file_name: str = None
    mime_type: str = None
    file_size: int = None


class Animation(BaseModel):
    """
    You can provide an animation for your game so that it looks stylish in chats
    (check out Lumberjack for an example).
    This object represents an animation file to be displayed in the message containing a game.
    https://core.telegram.org/bots/api#animation
    """

    file_id: str = None
    thumb: 'PhotoSize' = None
    file_name: str = None
    mime_type: str = None
    file_size: int = None


class Game(BaseModel):
    """
    This object represents a game.
    Use BotFather to create and edit games, their short names will act as unique identifiers.
    https://core.telegram.org/bots/api#game
    """
    title: str = None
    description: str = None
    photo: List['PhotoSize'] = []
    text: str = None
    text_entities: List['MessageEntity'] = []
    animation: 'Animation' = None


class PhotoSize(BaseModel):
    """
    This object represents one size of a photo or a file / sticker thumbnail.
    https://core.telegram.org/bots/api#photosize
    """
    file_id: str = None
    width: int = None
    height: int = None
    file_size: int = None


class MaskPosition(BaseModel):
    """
    This object describes the position on faces where a mask should be placed by default.
    https://core.telegram.org/bots/api#maskposition
    """
    point: str = None
    x_shift: float = None
    y_shift: float = None
    scale: float = None


class Sticker(BaseModel):
    """
    This object represents a sticker.
    https://core.telegram.org/bots/api#sticker
    """
    file_id: str = None
    width: int = None
    height: int = None
    thumb: 'PhotoSize' = None
    emoji: str = None
    set_name: str = None
    mask_position: MaskPosition = None
    file_size: int = None


class Invoice(BaseModel):
    """
    This object contains basic information about an invoice.
    https://core.telegram.org/bots/api#invoice
    """
    title: str = None
    description: str = None
    start_parameter: str = None
    currency: str = None
    total_amount: int = None


class Video(BaseModel):
    """
    This object represents a video file.
    https://core.telegram.org/bots/api#video
    """
    file_id: str = None
    width: int = None
    height: int = None
    duration: int = None
    thumb: 'PhotoSize' = None
    mime_type: str = None
    file_size: int = None


class Voice(BaseModel):
    """
    This object represents a voice note.
    https://core.telegram.org/bots/api#voice
    """
    file_id: str = None
    duration: int = None
    mime_type: str = None
    file_size: int = None


class VideoNote(BaseModel):
    """
    This object represents a video message (available in Telegram apps as of v.4.0).
    https://core.telegram.org/bots/api#videonote
    """
    file_id: str = None
    length: int = None
    duration: int = None
    thumb: 'PhotoSize' = None
    file_size: int = None


class Contact(BaseModel):
    """
    This object represents a phone contact.
    https://core.telegram.org/bots/api#contact
    """
    phone_number: str = None
    first_name: str = None
    last_name: str = None
    user_id: int = None
    vcard: str = None

    @property
    def full_name(self):
        name = self.first_name
        if self.last_name is not None:
            name += ' ' + self.last_name
        return name


class Location(BaseModel):
    """
    This object represents a point on the map.
    https://core.telegram.org/bots/api#location
    """
    longitude: float = None
    latitude: float = None


class Venue(BaseModel):
    """
    This object represents a venue.
    https://core.telegram.org/bots/api#venue
    """
    location: 'Location' = None
    title: str = None
    address: str = None
    foursquare_id: str = None
    foursquare_type: str = None


class PollOption(BaseModel):
    text: str = None
    voter_count: int = None


class Poll(BaseModel):
    id: str = None
    question: str = None
    options: List[PollOption] = []
    is_closed: bool = None


class ShippingAddress(BaseModel):
    """
    This object represents a shipping address.
    https://core.telegram.org/bots/api#shippingaddress
    """
    country_code: str = None
    state: str = None
    city: str = None
    street_line1: str = None
    street_line2: str = None
    post_code: str = None


class OrderInfo(BaseModel):
    """
    This object represents information about an order.
    https://core.telegram.org/bots/api#orderinfo
    """
    name: str = None
    phone_number: str = None
    email: str = None
    shipping_address: ShippingAddress = None


class SuccessfulPayment(BaseModel):
    """
    This object contains basic information about a successful payment.
    https://core.telegram.org/bots/api#successfulpayment
    """
    currency: str = None
    total_amount: int = None
    invoice_payload: str = None
    shipping_option_id: str = None
    order_info: OrderInfo = None
    telegram_payment_charge_id: str = None
    provider_payment_charge_id: str = None


class PassportFile(BaseModel):
    """
    This object represents a file uploaded to Telegram Passport.
    Currently all Telegram Passport files are in JPEG format when decrypted and don't exceed 10MB.
    https://core.telegram.org/bots/api#passportfile
    """

    file_id: str = None
    file_size: int = None
    file_date: int = None


class EncryptedPassportElement(BaseModel):
    """
    Contains information about documents or other Telegram Passport elements shared with the bot by the user.
    https://core.telegram.org/bots/api#encryptedpassportelement
    """

    type: str = None
    data: str = None
    phone_number: str = None
    email: str = None
    files: List[PassportFile] = []
    front_side: PassportFile = None
    reverse_side: PassportFile = None
    selfie: PassportFile = None


class EncryptedCredentials(BaseModel):
    """
    Contains data required for decrypting and authenticating EncryptedPassportElement.
    See the Telegram Passport Documentation for a complete description of the data decryption
    and authentication processes.
    https://core.telegram.org/bots/api#encryptedcredentials
    """

    data: str = None
    hash: str = None
    secret: str = None


class PassportData(BaseModel):
    """
    Contains information about Telegram Passport data shared with the bot by the user.
    https://core.telegram.org/bots/api#passportdata
    """

    data: List[EncryptedPassportElement] = None
    credentials: EncryptedCredentials = None


class LoginUrl(BaseModel):
    """
    This object represents a parameter of the inline keyboard button used to automatically authorize a user.
    Serves as a great replacement for the Telegram Login Widget when the user is coming from Telegram.
    All the user needs to do is tap/click a button and confirm that they want to log in.
    https://core.telegram.org/bots/api#loginurl
    """
    url: str = None
    forward_text: str = None
    bot_username: str = None
    request_write_access: bool = None


class CallbackGame(BaseModel):
    """
    A placeholder, currently holds no information. Use BotFather to set up your game.
    https://core.telegram.org/bots/api#callbackgame
    """
    pass


class InlineKeyboardButton(BaseModel):
    """
    This object represents one button of an inline keyboard. You must use exactly one of the optional fields.
    https://core.telegram.org/bots/api#inlinekeyboardbutton
    """
    text: str
    url: str = None
    login_url: LoginUrl = None
    callback_data: str = None
    switch_inline_query: str = None
    switch_inline_query_current_chat: str = None
    callback_game: CallbackGame = None
    pay: bool = None

    def __init__(self, text: str,
                 url: str = None,
                 login_url: 'LoginUrl' = None,
                 callback_data: str = None,
                 switch_inline_query: str = None,
                 switch_inline_query_current_chat: str = None,
                 callback_game: 'CallbackGame' = None,
                 pay: bool = None, **kwargs):
        super(InlineKeyboardButton, self).__init__(text=text,
                                                   url=url,
                                                   login_url=login_url,
                                                   callback_data=callback_data,
                                                   switch_inline_query=switch_inline_query,
                                                   switch_inline_query_current_chat=switch_inline_query_current_chat,
                                                   callback_game=callback_game,
                                                   pay=pay, **kwargs)


class InlineKeyboardMarkup(BaseModel):
    """
    This object represents an inline keyboard that appears right next to the message it belongs to.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016.
    Older clients will display unsupported message.
    https://core.telegram.org/bots/api#inlinekeyboardmarkup
    """
    inline_keyboard: List[List[InlineKeyboardButton]] = []

    def __init__(self, row_width=3, inline_keyboard=None, **kwargs):
        if inline_keyboard is None:
            inline_keyboard = []

        self.conf = kwargs.pop('conf', {}) or {}
        self.conf['row_width'] = row_width

        super(InlineKeyboardMarkup, self).__init__(**kwargs,
                                                   conf=self.conf,
                                                   inline_keyboard=inline_keyboard)

    @property
    def row_width(self):
        return self.conf.get('row_width', 3)

    @row_width.setter
    def row_width(self, value):
        self.conf['row_width'] = value

    def add(self, *args):
        """
        Add buttons
        :param args:
        :return: 'self'
        :rtype: ':'obj:`types.InlineKeyboardMarkup`
        """
        row = []
        for index, button in enumerate(args, start=1):
            row.append(button)
            if index % self.row_width == 0:
                self.inline_keyboard.append(row)
                row = []
        if len(row) > 0:
            self.inline_keyboard.append(row)
        return self

    def row(self, *args):
        """
        Add row
        :param args:
        :return: 'self'
        :rtype: ':'obj:`types.InlineKeyboardMarkup`
        """
        btn_array = []
        for button in args:
            btn_array.append(button)
        self.inline_keyboard.append(btn_array)
        return self

    def insert(self, button):
        """
        Insert button to last row
        :param button:
        :return: 'self'
        :rtype: ':'obj:`types.InlineKeyboardMarkup`
        """
        if self.inline_keyboard and len(self.inline_keyboard[-1]) < self.row_width:
            self.inline_keyboard[-1].append(button)
        else:
            self.add(button)
        return self


class Message(BaseModel):  # Checked
    message_id: int
    from_user: User = Field(None, alias='from')
    date: datetime.datetime
    chat: Chat
    forward_from: User = None
    forward_from_chat: Chat = None
    forward_from_message_id: int = None
    forward_signature: str = None
    forward_sender_name: str = None
    forward_date: datetime.datetime = None
    reply_to_message: 'Message' = None
    edit_date: datetime.datetime = None
    media_group_id: str = None
    author_signature: str = None
    text: str = None
    entities: List[MessageEntity] = None
    caption_entities: List[MessageEntity] = None
    audio: Audio = None
    document: Document = None
    animation: Animation = None
    game: Game = None
    photo: List[PhotoSize] = None
    sticker: Sticker = None
    video: Video = None
    voice: Voice = None
    video_note: VideoNote = None
    caption: str = None
    contact: Contact = None
    location: Location = None
    venue: Venue = None
    poll: Poll = None
    new_chat_members: List[User] = []
    left_chat_member: User = None
    new_chat_title: str = None
    new_chat_photo: List[PhotoSize] = []
    delete_chat_photo: bool = None
    group_chat_created: bool = None
    supergroup_chat_created: bool = None
    channel_chat_created: bool = None
    migrate_to_chat_id: int = None
    migrate_from_chat_id: int = None
    pinned_message: 'Message' = None  # TODO Make this Message
    invoice: Invoice = None
    successful_payment: SuccessfulPayment = None
    connected_website: str = None
    passport_data: PassportData = None
    reply_markup: InlineKeyboardMarkup = None


Message.update_forward_refs()


class Update(BaseModel):
    update_id: int
    message: Message
    edited_message: Optional[Any]
    channel_post: Optional[Any]
    edited_channel_post: Optional[Any]
    inline_query: Optional[Any]
    chosen_inline_result: Optional[Any]
    callback_query: Optional[Any]
    shipping_query: Optional[Any]
    pre_checkout_query: Optional[Any]
    poll: Optional[Any]
