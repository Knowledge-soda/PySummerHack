def text_dict(text, counter):
    res = {}
    res["hacked from PyWeek"] = text[counter].startswith("hacked")
    while text[counter]:
        n = text[counter].find(":")
        res[text[counter][:n]] = text[counter][n+1:]
        counter += 1
    return (res, counter)


class GameList:
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
