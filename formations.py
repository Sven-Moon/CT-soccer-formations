import requests as r
import random
import json

class Teams():
    formations = [(1,3,5,2),(1,3,4,3),(1,4,4,2),(1,4,5,1),(1,4,3,3),(1,5,3,2),(1,5,4,1)]
    formation_index = { "Keeper": 0,  "Defender": 1, "Midfielder": 2, "Striker": 3}
    def __init__(self) -> None:
        pass

    def get_data(self, url):
        data = r.get(url)
        if data.status_code == 200:
            return data.json()['Players']
        else:
            print('Problem getting data')

    def get_teams(self, url):
        players = self.get_data(url)
        for p in players:
            team_name = p['team']
            player = Player(p['first_name'], p['last_name'], p['injured'],p['position'], p['suspended'])
            if team_name not in vars(self):
                team = Team(p['team'])
                self.add_team(team)
            getattr(self,team_name).add_player(player)
            getattr(self,team_name).add_player_to_position(player)
    
    def add_team(self, team):
        setattr(self,team.name, team)

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

    def get_formation_results(self):
        results = []
        teams = {}
        # for each team
        for team_name in vars(self):
            team = getattr(self,team_name)
            # compare the position set minus suspended and injured 
            for formation in self.formations: #[(1,3,5,2)...]
                formation_available = True
                for position in team.positions: # position: "Keeper, etc"
                    available_positions = team.positions[position] - team.suspended - team.injured
            # with the formation possibilities saving to available formations
                    if(formation[self.formation_index[position]] > len(team.positions[position])):
                        formation_available = False
                        break
                if formation_available:
                    results.append("-".join([str(x) for x in formation]))
            teams[team_name] = results
        return teams
        
    def post_results(self,url):        
        Teams = {}
        formation_results = self.get_formation_results()
        for fr in formation_results:
            Teams[fr] = random.choice(formation_results[fr])
        # x = r.post(url,data)
        return json.dumps(Teams, indent=4)
 
class Team():
    def __init__(self, name) -> None:
        self.name = name
        self.players = set()
        self.positions = {"Keeper":set(), "Defender":set(),"Midfielder":set(),"Striker":set()}
        self.suspended = set()
        self.injured = set()

    def add_player(self,player):
        self.players.add(player)

    def playable_formations(self):
        pass
    
    def add_player_to_position(self,player):
        self.positions[player.position].add(player)
    
    def add_player_to_injured(self,player):
        self.injured.add(player)
    
    def add_player_to_suspended(self,player):
        self.suspended.add(player)
        
class Player():
    def __init__(self, first_name, last_name, injured, position, suspended) -> None:
        self.name = f'{first_name} {last_name}'.title()
        self.injured = injured
        self.position = position
        self.suspended = suspended


teams = Teams()
teams.get_teams('https://foxes90-prempundit.herokuapp.com/players')
print(teams.post_results("some_url"))


