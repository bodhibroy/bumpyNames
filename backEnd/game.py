game_messages = {}
game_messages["user move"] = 1
game_messages["collide"] = 2
game_messages["collided into"] = 3
game_messages["collected coin"] = 4
game_messages["randomly sound"] = 5

game_messages["db init"] = 100
game_messages["add user"] = 101
game_messages["update user"] = 102
game_messages["placed coin"] = 103
game_messages["player collision"] = 104

game_messages["misc"] = 200
game_messages["player kicked"] = 201

game_messages_inv = {game_messages[k]: k for k in game_messages}

coin_icon = "coins_stack.png"