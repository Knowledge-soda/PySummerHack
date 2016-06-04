def text_dict(text, counter):
    res = {}
    res["hacked from PyWeek"] = text[counter].startswith("hacked")
    while text[counter]:
        n = text[counter].find(":")
        res[text[counter][:n]] = text[counter][n+1:]
        counter += 1
    return (res, counter)


class Game_list:
    rounds = ["1st round hack", "2nd round hack", "3rd round hack",
              "4th round hack"]
    game_attr = ["game", "author", "link"]
    hack_attr = ["hacked from", "original game link", "author", "link"]
    def __init__(self, path="game_list.txt"):
        self.path = path
        self.games = []
        self.names = set()
        with open(path) as file:
            text = file.read()
        text = text.splitlines()
        count = 0
        lenght = len(text) - 1
        while count < lenght:
            game, count = text_dict(text, count)
            count += 1
            self.games.append(game)
            if game["hacked from PyWeek"]:
                self.names.add(game["hacked from"])
            else:
                self.names.add(game["game"])

    def save(self):
        with open(self.path, "w") as file:
            for game in self.games:
                if game["hacked from PyWeek"]:
                    attr = self.hack_attr
                else:
                    attr = self.game_attr
                for key in attr:
                    print(key, game[key], sep=":", file=file)
                for key in self.rounds:
                    if key in game:
                        print(key, game[key], sep=":", file=file)
                print(file=file)

    def add_game(self, name, author, link):
        if name in self.names:
            return 1  # same name can't be used twice
        self.names.add(name)
        self.games.append({
            "hacked from PyWeek": False,
            "game": name,
            "author": author,
            "link": link
            })

    def add_hacked_game(self, name, orig_link, author, link):
        if name in self.names:
            return 1  # same name can't be used twice
        self.names.add(name)
        self.games.append({
            "hacked from PyWeek": True,
            "hacked from": name,
            "original game link": orig_link,
            "author": author,
            "link": link
            })

    def add_hack(self, game_name, author, round_):
        for game in self.games:
            if game["hacked from PyWeek"]:
                if game["hacked from"] == game_name:
                    break
            elif game["game"] == game_name:
                break
        else:
            return 1  # you can't hack game which doesn't exist
        game[self.rounds[round_ - 1]] = author

    def list_games(self):
        for game in self.games:
            if game["hacked from PyWeek"]:
                print(game["hacked from"])
            else:
                print(game["game"])

    def list_available(self, round_):
        round_ = self.rounds[round_ - 1]
        for game in self.games:
            if round_ in game:
                if game["hacked from PyWeek"]:
                    print(game["hacked from"])
                else:
                    print(game["game"])                

    def describe(self, game_name):
        for game in self.games:
            if game["hacked from PyWeek"]:
                if game["hacked from"] == game_name:
                    break
            elif game["game"] == game_name:
                break
        else:
            return "Game with name {} doesn't exist!".format(game_name)
        hackers = ", ".join(game[r] for r in self.rounds if r in game)
        if game["hacked from PyWeek"]:
            if hackers:
                return "Game {} is on {}, original game hack by {} is on"\
                       " {} and was later hacked by {}.".format(
                           game["hacked from"], game["original game link"],
                           game["author"], game["link"], hackers)
            else:
                return "Game {} is on {}, original game hack by {} is on "\
                       "{}.".format(game["hacked from"],
                                    game["original game link"],
                                    game["author"],
                                    game["link"])
        else:
            if hackers:
                return "Game {} is made by {}, is on {} and was hacked by"\
                       " {}.".format(game["game"], game["author"],
                                     game["link"], hackers)
            else:
                return "Game {} is made by {} and is on {}.".format(
                    game["game"], game["author"], game["link"])


def shell(path="game_list.txt"):
    game_list = Game_list(path)
    print("Welcome to PySummerHack shell!")
    while True:
        command = input().split()
        if command[0].lower() in ("quit", "q"):
            break
        if command[0].lower() in ("help", "h"):
            print("quit/q - quits the shell")
            print("help/h - prints this message")
            print("save/s - save all changes")
            print("list/ls - list all games")
            print("list/ls available/av n - list all games not hacked on nth round")
            print("add/a game/g - adds game")
            print("add/a hacked/hacked_game/hg - adds hacked game")
            print("add/a hack/h - adds hack to some game")
        if command[0].lower() in ("list", "ls"):
            if len(command) > 1 and command[1].lower() in ("available",
                                                          "av"):
                game_list.list_available(int(command[2]))
            else:
                game_list.list_games()
        if command[0].lower() in ("save", "s"):
            game_list.save()
        if command[0].lower() in ("add", "a"):
            if command[1].lower() in ("g", "game"):
                name = input("name:")
                author = input("author:")
                link = input("link:")
                if game_list.add_game(name, author, link):
                    print("Name already used!")
            if command[1].lower() in ("hacked", "hacked_game", "hg"):
                name = input("original game name:")
                orig_link = input("original link:")
                author = input("author:")
                link = input("link:")
                if game_list.add_game(name, orig_link, author, link):
                    print("Name already used!")
            if command[1].lower() in ("hack", "h"):
                name = input("game name:")
                author = input("author:")
                round_ = int(input("round:"))
                if game_list.add_hack(name, author, round_):
                    print("Game with name {} doesn't exist!".format(name))

if __name__ == "__main__":
    shell()
