from typing import List
from typing import Optional
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class League(Base):

    __tablename__ = 'League'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    matchup_periods: Mapped[str] = mapped_column(String(200))
    espn_s2: Mapped[str] = mapped_column(String(200))
    swid: Mapped[str] = mapped_column(String(200))

    def __repr__(self) -> str:
        return f"League(id={self.id!r}, name={self.name!r})"


class Matchups(Base):

    __tablename__ = 'Matchups'

    week: Mapped[int] = mapped_column()
    is_playoff:  Mapped[bool] = mapped_column()
    type: Mapped[str] = mapped_column(String(50))
    home_team_id: Mapped[int] = mapped_column()
    away_team_id: Mapped[int] = mapped_column()
    home_team_roster: Mapped[str] = mapped_column(String(200))
    away_team_roster: Mapped[str] = mapped_column(String(200))
    home_score: Mapped[float] = mapped_column()
    away_score: Mapped[float] = mapped_column()
    matchup_id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"League(matchup_id={self.matchup_id!r}, week={self.week!r})"


class Teams(Base):

    __tablename__ = 'Teams'

    team_id: Mapped[int] = mapped_column(primary_key=True)
    team_abbrev: Mapped[str] = mapped_column(String(5))
    team_name: Mapped[str] = mapped_column(String(50))
    owner: Mapped[str] = mapped_column(String(50))
    wins: Mapped[int] = mapped_column()
    losses: Mapped[int] = mapped_column()
    ties: Mapped[int] = mapped_column()
    points_for: Mapped[float] = mapped_column()
    points_against: Mapped[float] = mapped_column()
    draft_projected_rank: Mapped[int] = mapped_column()
    standing: Mapped[int] = mapped_column()
    final_standing: Mapped[int] = mapped_column()
    playoff_pct: Mapped[float] = mapped_column()

    def __repr__(self) -> str:
        return f"League(team_id={self.team_id!r}, team_name={self.team_name!r})"


class Players(Base):

    __tablename__ = 'Players'

    id: Mapped[int] = mapped_column(primary_key=True)
    player_name: Mapped[str] = mapped_column(String(40))
    position: Mapped[str] = mapped_column(String(40))
    player_stats = relationship("Player_stats", back_populates="player", cascade="all, delete-orphan")
    eligible_slots: Mapped[str] = mapped_column()
    acquisition_type: Mapped[str] = mapped_column()
    pro_team: Mapped[str] = mapped_column()
    percent_owned: Mapped[int] = mapped_column()
    percent_started: Mapped[int] = mapped_column()

    player_stats = relationship("Player_stats", back_populates="player")


class Player_stats(Base):

    __tablename__ = 'Player_stats'

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("Players.id"))
    played_for_team_id: Mapped[int] = mapped_column(String(40))
    week: Mapped[int] = mapped_column()
    slot_position: Mapped[str] = mapped_column(String(10))
    points: Mapped[float] = mapped_column()
    projected_points: Mapped[float] = mapped_column()
    game_played: Mapped[int] = mapped_column()
    game_date: Mapped[datetime.datetime] = mapped_column()
    on_bye_week: Mapped[bool] = mapped_column()
    pro_opponent: Mapped[str] = mapped_column()
    pro_pos_rank: Mapped[int] = mapped_column()

    player = relationship("Players", back_populates="player_stats")