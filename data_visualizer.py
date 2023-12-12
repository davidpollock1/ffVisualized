import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import select
from db.db import session
from models import *
import pandas as pd
import numpy as np
from scipy import stats
import logging

# Set the SQLAlchemy logging level to WARNING to reduce output
logging.getLogger('sqlalchemy.engine').setLevel(logging.CRITICAL)

sns.set_theme(style="darkgrid", palette="pastel")


def plot_player_year(player_id):

    stmt = select(Player_stats.__table__).where(Player_stats.on_bye_week != 1, Player_stats.player_id == f"{player_id}")

    player_stmt = select(Players.__table__).where(Players.id == f"{player_id}")

    with session:
        data = session.execute(stmt).fetchall()
        player = session.execute(player_stmt).fetchone()
        df = pd.DataFrame(data)

    avg_points_by_rank = df.groupby('pro_pos_rank')['points'].mean().reset_index()
    sns.lineplot(data=avg_points_by_rank, x='pro_pos_rank', y='points')
    plt.title("Average Player Performance vs. Opponent Rank\n"
              f"{player.player_name}")
    plt.xlabel("Opponent Position Rank")
    plt.ylabel("Average Points Scored")
    plt.show()


def plot_position_vs_opp_rank(position):

    stmt = select(Player_stats.__table__).where(Player_stats.on_bye_week != 1, Player_stats.slot_position == f"{position}")

    with session:
        data = session.execute(stmt).fetchall()
        df = pd.DataFrame(data)

    # Calculate Z-scores for the 'points' field
    z_scores = np.abs(stats.zscore(df['points']))

    # Find the indices of outliers
    threshold = 3

    # Find the indices of outliers
    outlier_indices = np.where(z_scores > threshold)

    # Replace outliers with the average of preceding records
    for idx in outlier_indices[0]:
        if idx > 0:
            avg_value = df.loc[:idx - 1, 'points'].mean()
            df.at[idx, 'points'] = avg_value

    avg_points_by_rank = df.groupby('pro_pos_rank')['points'].mean().reset_index()
    sns.lineplot(data=avg_points_by_rank, x='pro_pos_rank', y='points')
    plt.title(f"Average {position} Performance vs. Opponent Rank")
    plt.xlabel("Opponent Position Rank")
    plt.ylabel("Average Points Scored")
    plt.show()


def top_player_plotted_vs_opp_rank(position):

    id_points = get_position_rank_one_id(position)

    stmt = select(Player_stats.__table__).where(Player_stats.on_bye_week != 1, Player_stats.player_id == f"{id_points[0]}")

    player_stmt = select(Players.__table__).where(Players.id == f"{id_points[0]}")

    with session:
        data = session.execute(stmt).fetchall()
        player = session.execute(player_stmt).fetchone()
        df = pd.DataFrame(data)

    sns.lineplot(data=df, x='pro_pos_rank', y='points')
    plt.title(f"{player.player_name} \nPerformance vs. Opponent Rank\n"
              f"Total points {id_points[1]}")
    plt.xlabel("Opponent Position Rank")
    plt.ylabel("Average Points Scored")
    plt.show()


def get_position_rank_one_id(position):

    stmt = select(Player_stats.__table__).where(Player_stats.on_bye_week != 1, Player_stats.slot_position == f"{position}")

    try:
        with session:
            data = session.execute(stmt).fetchall()
            df = pd.DataFrame(data)

        # Group by player and sum their points
        total_points = df.groupby('player_id').agg({'points': 'sum'}).reset_index()

        # Find the player with the most combined points
        max_points_player = total_points.loc[total_points['points'].idxmax()]

        return str(max_points_player['player_id']), max_points_player['points']

    except Exception as e:
        print(f"Exception occurred: {e}")


if __name__ == '__main__':
    # plot_player_year(4262921)
    # plot_position_vs_opp_rank("QB")
    # get_position_rank_one_id("QB")
    top_player_plotted_vs_opp_rank("QB")
