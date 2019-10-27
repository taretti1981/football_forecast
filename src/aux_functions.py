import numpy as np
import yaml
import pandas as pd

def readConfig():
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    return config

def getData(db,current_team):

    sql_query = "select * from football_germany where (home='" + current_team + "' or visitor='" + current_team + "') order by season asc, matchday asc"

    print("Getting " + current_team + " data...")
    data = db.query(sql_query)

    data_goal_diff = pd.DataFrame(
        columns=['season', 'matchday', 'cum_won', 'cum_draw', 'cum_lose', 'cum_goals_scored', 'cum_goals_received',
                 'diff_goals'])

    cum_won = 0
    cum_draw = 0
    cum_lose = 0
    cum_goals_scored = 0
    cum_goals_received = 0
    diff_goals = 0

    for ii, row in data.iterrows():
        data_goal_diff.loc[ii, 'season'] = data.loc[ii, 'season']
        data_goal_diff.loc[ii, 'matchday'] = row['matchday']
        if data.loc[ii, 'home'] == current_team:

            cum_goals_scored = cum_goals_scored + row['goals_home']
            cum_goals_received = cum_goals_received + row['goals_visitor']
            diff_goals = diff_goals + row['goals_home'] - row['goals_visitor']

            if row['goals_home'] > row['goals_visitor']:
                cum_won = cum_won + 1
            if row['goals_home'] < row['goals_visitor']:
                cum_lose = cum_lose + 1
            if row['goals_home'] == row['goals_visitor']:
                cum_draw = cum_draw + 1
        else:
            cum_goals_scored = cum_goals_scored + row['goals_visitor']
            cum_goals_received = cum_goals_received + row['goals_home']
            diff_goals = diff_goals + row['goals_visitor'] - row['goals_home']

            if row['goals_visitor'] > row['goals_home']:
                cum_won = cum_won + 1
            if row['goals_visitor'] < row['goals_home']:
                cum_lose = cum_lose + 1
            if row['goals_home'] == row['goals_visitor']:
                cum_draw = cum_draw + 1

        data_goal_diff.loc[ii, 'cum_won'] = cum_won
        data_goal_diff.loc[ii, 'cum_draw'] = cum_draw
        data_goal_diff.loc[ii, 'cum_lose'] = cum_lose
        data_goal_diff.loc[ii, 'cum_goals_scored'] = cum_goals_scored
        data_goal_diff.loc[ii, 'cum_goals_received'] = cum_goals_received
        data_goal_diff.loc[ii, 'diff_goals'] = diff_goals

    print("Getting " + current_team + " data [Done]")
    return data_goal_diff


def getDataBetween(db,team_home,team_visitor):

    sql_query = "select * from football_germany where (home='" + team_home + "' and visitor='" + team_visitor + "') OR (home='" + team_visitor + "' and visitor='" + team_home + "') order by season asc, matchday asc"

    print("Getting " + team_home + " vs " + team_visitor + " data...")
    data = db.query(sql_query)

    data_goal_diff = pd.DataFrame(
        columns=['season', 'matchday', 'cum_won_home', 'cum_draw', 'cum_visitor', 'cum_goals_home', 'cum_goals_visitor'])

    cum_won_home = 0
    cum_draw = 0
    cum_visitor = 0
    cum_goals_home = 0
    cum_goals_visitor = 0

    for ii, row in data.iterrows():
        data_goal_diff.loc[ii, 'season'] = data.loc[ii, 'season']
        data_goal_diff.loc[ii, 'matchday'] = row['matchday']
        if data.loc[ii, 'home'] == team_home:

            cum_goals_home = cum_goals_home + row['goals_home']
            cum_goals_visitor = cum_goals_visitor + row['goals_visitor']

            if row['goals_home'] > row['goals_visitor']:
                cum_won_home = cum_won_home + 1
            if row['goals_home'] < row['goals_visitor']:
                cum_visitor = cum_visitor + 1
            if row['goals_home'] == row['goals_visitor']:
                cum_draw = cum_draw + 1

        else:
            cum_goals_home = cum_goals_home + row['goals_visitor']
            cum_goals_visitor = cum_goals_visitor + row['goals_home']

            if row['goals_visitor'] > row['goals_home']:
                cum_won_home = cum_won_home + 1
            if row['goals_visitor'] < row['goals_home']:
                cum_visitor = cum_visitor + 1
            if row['goals_home'] == row['goals_visitor']:
                cum_draw = cum_draw + 1

        data_goal_diff.loc[ii, 'cum_won_home'] = cum_won_home
        data_goal_diff.loc[ii, 'cum_draw'] = cum_draw
        data_goal_diff.loc[ii, 'cum_visitor'] = cum_visitor
        data_goal_diff.loc[ii, 'cum_goals_home'] = cum_goals_home
        data_goal_diff.loc[ii, 'cum_goals_visitor'] = cum_goals_visitor

    print("Getting " + team_home + " vs " + team_visitor + " data [Done]")
    return data_goal_diff