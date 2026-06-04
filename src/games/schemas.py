from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator, model_validator


class CreateGameRequest(BaseModel):
    game_name: str = Field(...)
    game_type: str = Field(...)
    cash_in: float = Field(...)
    cash_out: Optional[float] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    notes: Optional[str] = None
    entry_mode: Optional[str] = None
    freeplay_used: Optional[float] = None

    @field_validator("cash_in")
    @classmethod
    def cash_in_validator(cls, cash_in):
        if cash_in < 0:
            raise ValueError("cash_in cannot be negative")
        return cash_in

    @field_validator("cash_out")
    @classmethod
    def cash_out_validator(cls, cash_out):
        if cash_out is not None and cash_out < 0:
            raise ValueError("cash_out cannot be negative")
        return cash_out

    @field_validator("freeplay_used")
    @classmethod
    def free_play_validator(cls, freeplay_used):
        if freeplay_used is not None and freeplay_used < 0:
            raise ValueError("freeplay_used cannot be negative")
        return freeplay_used

    @model_validator(mode="after")
    def validate_dates(self):
        if self.ended_at is not None and self.started_at is not None:
            if self.ended_at < self.started_at:
                raise ValueError("ended_at cannot be before started_at")
        return self

    @model_validator(mode="after")
    def validate_freeplay_used(self):
        if self.cash_in == 0:
            if self.freeplay_used is None or self.freeplay_used <= 0:
                raise ValueError("freeplay_used must be greater than 0 if cash_in is 0")
        return self

    @model_validator(mode="after")
    def validate_cash_out_when_ended(self):
        if self.ended_at is not None:
            if self.cash_out is None:
                raise ValueError("cash_out is required for a completed game")
        return self


class GameResponse(BaseModel):
    game_id: str
    session_id: str
    trip_id: str
    user_id: str
    game_name: str
    game_type: str
    cash_in: float
    cash_out: Optional[float]
    status: str
    started_at: Optional[str]
    ended_at: Optional[str]
    created_at: str
    notes: Optional[str]
    entry_mode: Optional[str]
    freeplay_used: Optional[float]

class GameListResponse(BaseModel):
    games: List[GameResponse]

class UpdateGameRequest(BaseModel):
    game_name: Optional[str] = None
    game_type: Optional[str] = None
    cash_in: Optional[float] = None
    cash_out: Optional[float] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    notes: Optional[str] = None
    entry_mode: Optional[str] = None
    freeplay_used: Optional[float] = None

    @field_validator("cash_in")
    @classmethod
    def cash_in_validator(cls, cash_in):
        if cash_in < 0:
            raise ValueError("cash_in cannot be negative")
        return cash_in

    @field_validator("cash_out")
    @classmethod
    def cash_out_validator(cls, cash_out):
        if cash_out is not None and cash_out < 0:
            raise ValueError("cash_out cannot be negative")
        return cash_out

    @field_validator("freeplay_used")
    @classmethod
    def free_play_validator(cls, freeplay_used):
        if freeplay_used is not None and freeplay_used < 0:
            raise ValueError("freeplay_used cannot be negative")
        return freeplay_used

    @model_validator(mode="after")
    def validate_dates(self):
        if self.ended_at is not None and self.started_at is not None:
            if self.ended_at < self.started_at:
                raise ValueError("ended_at cannot be before started_at")
        return self