# return a dictionary containing team information for each team
# Valid lineups must contain 11 players and are limited to the following, shown as Keeper-Defenders-Midfielders-Strikers:
# 1-3-5-2
# 1-3-4-3
# 1-4-4-2
# 1-4-5-1
# 1-4-3-3
# 1-5-3-2
# 1-5-4-1 
import requests as r

class Teams():
    formations = [(1,3,5,2),(1,3,4,3),(1,4,4,2),(1,4,5,1),(1,4,3,3),(1,5,3,2),(1,5,4,1)]
    def __init__(self) -> None:
        self.teams = {}
        self.suspended = set()
        self.injured = set()

    def get_data(self, url):
        data = r.get(url)
        if data.status_code == 200:
            return data.json()['Players']
        else:
            print('Problem getting data')

    def get_teams(self, url):
        players = self.get_data(url)
        # players = the list "Players" from the API 
        for p in players:
            # p = the object with the attributes {first_name...}
            player = Player(p['first_name'], p['last_name'], p['injured'],p['position'], p['suspended'])
            team = Team(p['team'])
            if p['team'] not in self.teams.keys():
                self.add_team(team)
            self.teams[p['team']].add_player(player)
            self.teams[p['team']].add_player_to_position(player)
    
    def add_team(self, team):
        self.teams[team.name] = team

    def display_teams(self):
        for team_name in self.teams:
            team = self.teams[team_name]
            print(team.name)
            for position in team.positions:
                print(position)
                for player in team.positions[position]:
                    print(player.name, end=", ")
                print()

    def display_positions(self):
        for team_name in self.teams:
            team = self.teams[team_name]
            print(team.name)
            for position in team.positions:
                print(position)
                for player in team.positions[position]:
                    print(player.name, end=", ")
                print()

class Team():
    def __init__(self, name) -> None:
        self.name = name
        self.players = set()
        self.positions = {"Keeper":set(), "Defender":set(),"Midfielder":set(),"Striker":set()}

    def add_player(self,player):
        self.players.add(player)

    def check_formation(self):
        pass
    
    def add_player_to_position(self,player):
        self.positions[player.position].add(player)
    
    def add_player_to_injured(self,player):
        self.positions[player.position].add(player)
    
    def add_player_to_suspended(self,player):
        self.positions[player.position].add(player)
        
class Player():
    def __init__(self, first_name, last_name, injured, position, suspended) -> None:
        self.name = f'{first_name} {last_name}'.title()
        self.injured = injured
        self.position = position
        self.suspended = suspended



teams = Teams()
teams.get_teams('https://foxes90-prempundit.herokuapp.com/players')
teams.display_teams()

