
def object_to_list(roster):
    roster_list = []
    for player in roster:
        roster_list.append(player.playerId)
    return roster_list
