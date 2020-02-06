import requests
from bs4 import BeautifulSoup
import time
from itertools import tee

def get_games(my_team, week_num):


    print(my_team)
    URL = 'https://www.espn.co.uk/nfl/fixtures/_/week/' + str(week_num) + '/seasontype/2'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'lxml')

    x = 0
    y = 0
    game_date = []

    for date in soup.find_all('h2', class_='table-caption'):
        game_date.append(str(date.text))

    for main_body in soup.find_all(('tbody')):
        print(game_date[y])
        for main_tr in main_body.find_all('tr'):
            first_team = main_tr.td.span.text
            first_team_abrv = main_tr.td.abbr.text
            second_team_class = main_tr.find('td', class_='home')
            second_team = second_team_class.div.span.text
            second_team_abrv = second_team_class.div.abbr.text

            with open('games.txt', 'a') as file:
                file.write(first_team + "\n")
                file.write(second_team + "\n")
                file.write("\n")

            is_derby = derby_games(first_team_abrv, second_team_abrv, my_team)

            print(first_team + " (" + first_team_abrv + ")")
            print(second_team + " (" + second_team_abrv + ")")

            team_ranking(first_team_abrv, second_team_abrv, is_derby)
            print()
            x += 1
        y += 1
    print("There are " + str(x) + " games played this week.\n")

    bye_week_func(soup)


def team_ranking(first_team_abrv, second_team_abrv, is_derby):


    teams_dict = {"KC": 5, "LAR": 5, "NO": 5, "NE": 5, "GB": 4, "HOU": 4, "IND": 4,
     "SEA": 4, "LAC": 4, "DAL": 4, "CHI": 4, "PIT": 3, "SF": 3, "WSH": 3,
     "PHI": 3, "BAL": 3, "CLE": 3, "ATL": 3, "MIN": 3, "TEN": 2, "CAR": 2,
     "DET": 2, "JAX": 2, "MIA": 2, "DEN": 2, "CIN": 2, "NYJ": 1, "NYG": 2,
     "OAK": 1, "BUF": 1, "TB": 1, "ARI": 1}

    game_rating = int(teams_dict[first_team_abrv]) + int(teams_dict[second_team_abrv])
    if(is_derby == "yes"):
        game_rating + 1
        print("This game is rated " + str(game_rating) + "/10 (+1 for derby)")
    else:
        print("This game is rated " + str(game_rating) + "/10")


def bye_week_func(soup):


    bye_week_temp = []
    bye_week_abrv_temp = []
    v = 0
    for bye_week in soup.find_all('tr', class_='odd byeweek'):
        print("These teams are on a bye week.")
        for bye_team in bye_week.find_all("span"):
            bye_week_temp.append(bye_team.text)

        for bye_team_abrv in bye_week.find_all("abbr"):
            bye_week_abrv_temp.append(bye_team_abrv.text)

    while (v <= (len(bye_week_temp) - 1)):
        print(bye_week_temp[v] + " " + bye_week_abrv_temp[v])
        v += 1


def derby_games(first_team_abrv, second_team_abrv, my_team):

    #NFC (East = 5, West = 6, North = 7, South = 8
    #AFC (East = 1, North = 2, South = 3, West = 4

    division_dict = {"KC": 2, "LAR": 6, "NO": 8, "NE": 1, "GB": 7, "HOU": 4, "IND": 4,
                      "SEA": 6, "LAC": 2, "DAL": 5, "CHI": 7, "PIT": 3, "SF": 6, "WSH": 5,
                      "PHI": 5, "BAL": 3, "CLE": 3, "ATL": 8, "MIN": 7, "TEN": 4, "CAR": 8,
                      "DET": 7, "JAX": 4, "MIA": 1, "DEN": 2, "CIN": 3, "NYJ": 1, "NYG": 5,
                      "OAK": 2, "BUF": 1, "TB": 8, "ARI": 2}

    if(first_team_abrv == my_team or second_team_abrv == my_team):
        print("This is the game your team is playing!")
    else:
        None

    if (int(division_dict[first_team_abrv]) == int(division_dict[second_team_abrv])):
        print("Derby Game!")
        is_derby = "yes"
        return is_derby
    else:
        None


def main():


    team_abrvs = ["NYJ", "NYG", "OAK", "BUF", "TB", "CAR", "TEN", "DET", "JAX", "MIA", "DEN", "CIN",
                  "PIT", "SF", "WSH", "PHI", "BAL", "CLE", "ATL", "MIN", "GB", "HOU", "IND", "SEA", "LAC", "DAL", "CHI",
                   "KC", "LAR", "NO", "NE", "ARI"]

    team_input = input("Enter team abrv: ")
    if team_input.upper() in team_abrvs:
        week_num = int(input("Enter week you want: "))

        try:
            if week_num >= 1:
                if week_num <= 16:

                    get_games(team_input.upper(), week_num)
            else:
                print("Error invalid week choice!")
        except ValueError as error:
            print(error)
    else:
        print("Error invalid team!")

if __name__ == "__main__":
    main()
