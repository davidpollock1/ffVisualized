from models import *
from utils import *
from sqlalchemy import exists, update, exc
from db import session
import json
from espn_api.football import League as EspnLeague
from dotenv import load_dotenv
import os

load_dotenv('.env')


# class to build league and load in DB.
class league_loader:
    def __init__(self, league_id, year, espn_s2, swid):
        self.league_id = league_id
        self.year = year
        self.espn_s2 = espn_s2
        self.swid = swid
        self.league = EspnLeague(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)

    def initial_load(self):
        self.load_league_data()

    def load_league_data(self):

        league = League(
            id=self.league.league_id,
            name=self.league.settings.name,
            matchup_periods=json.dumps(self.league.settings.matchup_periods),
            espn_s2=self.espn_s2,
            swid=self.swid
        )

        ret = session.query(exists().where(League.id == league.id))

        try:

            if ret is False:
                session.add(league)
                session.commit()
            else:
                session.merge(league)
                session.commit()

        except exc.SQLAlchemyError:
            print("SQLAlchemy Error")

        # calling load_teams function and passing league object.
        # load_teams()

        # calling load_matchups function and passing league object.
        # load_matchups()

    def load_teams(self):

        num_teams = self.league.settings.team_count

        for i in range(num_teams):
            team_obj = self.league.teams[i]
            team = Teams(
                team_id=team_obj.team_id,
                team_abbrev=team_obj.team_abbrev,
                team_name=team_obj.team_name,
                owner=team_obj.owner,
                wins=team_obj.wins,
                losses=team_obj.losses,
                ties=team_obj.ties,
                points_for=team_obj.points_for,
                points_against=team_obj.points_against,
                draft_projected_rank=team_obj.draft_projected_rank,
                standing=team_obj.standing,
                final_standing=team_obj.final_standing,
                playoff_pct=team_obj.playoff_pct
            )
            ret = session.query(exists().where(Teams.team_id == team.team_id))

            if ret is False:
                session.add(team)
                session.commit()
            else:
                session.merge(team)
                session.commit()

    def load_matchups(self):

        num_matchups = int(self.league.settings.team_count / 2)
        current_week = self.league.current_week

        for k in range(current_week):
            week = k + 1
            box_scores = self.league.box_scores(week)

            self.add_player_stats(box_scores, week, num_matchups)

            for i in range(num_matchups):
                current_box_score = box_scores[i]
                home_roster = current_box_score.home_lineup
                away_roster = current_box_score.away_lineup

                matchup = Matchups(
                    week=week,
                    is_playoff=current_box_score.is_playoff,
                    type=current_box_score.matchup_type,

                    home_team_id=current_box_score.home_team.team_id,
                    home_team_roster=json.dumps(object_to_list(home_roster)),
                    home_score=current_box_score.home_score,

                    away_team_id=current_box_score.away_team.team_id,
                    away_team_roster=json.dumps(object_to_list(away_roster)),
                    away_score=current_box_score.away_score,

                    matchup_id=int(str(current_box_score.home_team.team_id) + str(current_box_score.away_team.team_id) + str(week))
                )

                self.add_player(home_roster)
                self.add_player(away_roster)

                ret = session.query(exists().where(Matchups.matchup_id == matchup.matchup_id))

                if ret is False:
                    session.add(matchup)
                    session.commit()
                else:
                    session.merge(matchup)
                    session.commit()

    @staticmethod
    def add_player(roster):
        for spot in roster:

            player = Players(
                id=spot.playerId,
                player_name=spot.name,
                position=spot.position,
                eligible_slots=str(json.dumps(spot.eligibleSlots)),
                acquisition_type=str(spot.acquisitionType),
                pro_team=spot.proTeam,
                percent_owned=spot.percent_owned,
                percent_started=spot.percent_started
            )

            ret = session.query(exists().where(Players.id == player.id))

            if ret is False:
                session.add(player)
                session.commit()
            else:
                session.merge(player)
                session.commit()

    @staticmethod
    def add_player_stats(boxscores, week, num_matchups):

        for k in range(num_matchups):

            team_home = boxscores[k].home_team
            roster_home = boxscores[k].home_lineup

            for home_player in roster_home:
                if hasattr(home_player, 'game_date'):
                    game_date = home_player.game_date
                else:
                    game_date = datetime.datetime(9999, 12, 31)

                player_stats = Player_stats(
                    id=int(str(home_player.playerId) + str(week)),
                    player_id=home_player.playerId,
                    played_for_team_id=team_home.team_id,
                    week=week,
                    slot_position=home_player.slot_position,
                    points=home_player.points,
                    projected_points=home_player.projected_points,
                    game_played=home_player.game_played,
                    game_date=game_date,
                    on_bye_week=home_player.on_bye_week,
                    pro_opponent=home_player.pro_opponent,
                    pro_pos_rank=home_player.pro_pos_rank
                )

                ret = session.query(exists().where(Player_stats.id == player_stats.id))

                try:

                    if ret is False:
                        session.add(player_stats)
                        session.commit()
                    else:
                        session.merge(player_stats)
                        session.commit()

                except exc.SQLAlchemyError:
                    print("SQLAlchemy Error")

            team_away = boxscores[k].away_team
            roster_away = boxscores[k].away_lineup

            for away_player in roster_away:

                if hasattr(away_player, 'game_date'):
                    game_date = away_player.game_date
                else:
                    game_date = datetime.datetime(9999, 12, 31)

                away_player_stats = Player_stats(
                    id=int(str(away_player.playerId) + str(week)),
                    player_id=away_player.playerId,
                    played_for_team_id=team_away.team_id,
                    week=week,
                    slot_position=away_player.slot_position,
                    points=away_player.points,
                    projected_points=away_player.projected_points,
                    game_played=away_player.game_played,
                    game_date=game_date,
                    on_bye_week=away_player.on_bye_week,
                    pro_opponent=away_player.pro_opponent,
                    pro_pos_rank=away_player.pro_pos_rank
                )

                ret = session.query(exists().where(Player_stats.id == away_player_stats.id))

                try:

                    if ret is False:
                        session.add(away_player_stats)
                        session.commit()
                    else:
                        session.merge(away_player_stats)
                        session.commit()

                except exc.SQLAlchemyError:
                    print("SQLAlchemy Error")


if __name__ == '__main__':
    _espn_s2 = os.getenv('ESPN_S2')
    _swid = os.getenv('SWID')
    _league_id = os.getenv('LEAGUE_ID')
    _year = os.getenv('2022')

    new_league = league_loader(_league_id, _year, _espn_s2, _swid)
    # new_league.load_league_data()
    # new_league.load_teams()
    new_league.load_matchups()
