# TODO WIP
def main(args):
    teams = bd.build_teams(pd.read_csv(r"test_league_draft.csv"))
    teams.get_breakdown()
    # teams.print_team(1)
    # print()
    # teams.print_team(2)
    """player1 = input("Enter a players name: ")
    player2 = input("Enter a players name: ")
    teams.trade(player1, player2)"""


if __name__ == "__main__":
    main(None)
