from schema import User, Dish, GameInProgress, Reaction, Result
import random


def add_user(chat_id, name, surname):
    """
    Add user to a User database if not already in it
    """
    # check if user exists
    if type(chat_id) == str:
        chat_id = int(chat_id)
    query = User.select().where(User.chat_id == chat_id)
    if len(query) > 0:
        pass
    else:  # user doesn't exist
        User.create(chat_id=chat_id, name=name, surname=surname, isPlaying=False).save()


def is_in_game(user_id):
    return User.select().where(User.user_id == user_id)[0].isPlaying


def random_meal():
    query = Dish.select()
    dishes = query.count()
    id = random.randint(1, dishes)
    types = query.where(Dish.dish_id == id)[0].types.split('_')
    type = int(random.choice(types))
    return id, type


def random_type(meal_id):
    query = Dish.select().where(Dish.dish_id == meal_id)
    types = query[0].types.split('_')
    type = int(random.choice(types))
    return type


def start_game(user_id):
    """
    Starts a new game
    """
    user = User.select().where(User.user_id == user_id).get()
    user.isPlaying = True
    user.save()
    # check if game exists for this user
    query = GameInProgress.select().where(GameInProgress.user_id == user_id)
    if len(query) == 1:  # game already exists - meaning that a player lost and restarts
        game = query.get()
        game.current_dish = 1
        game.dish1_type = random_type(game.dish1)
        game.dish2_type = random_type(game.dish2)
        game.dish3_type = random_type(game.dish3)
        game.dish4_type = random_type(game.dish4)
        game.dish5_type = random_type(game.dish5)
        game.dish6_type = random_type(game.dish6)
        game.score += 1
        game.save()
    elif len(query) == 0:  # no such game
        dishes = [random_meal() for i in range(1, 7)]
        GameInProgress.create(user_id=user_id, dish1=dishes[0][0], dish2=dishes[1][0],
                              dish3=dishes[2][0], dish4=dishes[3][0], dish5=dishes[4][0],
                              dish6=dishes[5][0], current_dish=1,
                              dish1_type=dishes[0][1], dish2_type=dishes[1][1], dish3_type=dishes[2][1],
                              dish4_type=dishes[3][1], dish5_type=dishes[4][1], dish6_type=dishes[5][1], score=0)
    else:
        print(f"There is a wrong number of games: {len(query)}")


def get_user_id(chat_id):
    """
    Returns user id based on chat id
    """
    query = User.select().where(User.chat_id == chat_id)
    if len(query) == 1:
        return query[0].user_id
    else:
        print(f"Expected one result in 'get user id', but got {len(query)}")


def current_meal(user_id):
    """
    Returns a string with a description of the current meal for the user
    """
    query = User.select().where(User.user_id == user_id)
    if query[0].isPlaying:
        query = GameInProgress.select().where(GameInProgress.user_id == user_id)
        dish_num = query[0].current_dish
        if dish_num == 1:
            dish_id = query[0].dish1
            dish_type = query[0].dish1_type
        elif dish_num == 2:
            dish_id = query[0].dish2
            dish_type = query[0].dish2_type
        elif dish_num == 3:
            dish_id = query[0].dish3
            dish_type = query[0].dish3_type
        elif dish_num == 4:
            dish_id = query[0].dish4
            dish_type = query[0].dish4_type
        elif dish_num == 5:
            dish_id = query[0].dish5
            dish_type = query[0].dish5_type
        elif dish_num == 6:
            dish_id = query[0].dish6
            dish_type = query[0].dish6_type
        else:
            print(f"Passed unacessible dish num: {dish_num}")

        query = Dish.select().where(Dish.dish_id == dish_id)
        dish_name = query[0].name
        dish_descriptions = query[0].descriptions
        dish_description = dish_descriptions.split('_')[dish_type]

        return f"Название: {dish_name}\nОписание:\n{dish_description}"
    else:
        print("Cannot get a meal as player is not playing a game at the moment")
        return "Not accessible!"


def apply(user_id, ingredient):
    """
    Applies a passed ingredient and returns the result
    """
    query = User.select().where(User.user_id == user_id)
    if query[0].isPlaying:
        query = GameInProgress.select().where(GameInProgress.user_id == user_id)
        dish_num = query[0].current_dish
        if dish_num == 1:
            dish_id = query[0].dish1
            dish_type = query[0].dish1_type
        elif dish_num == 2:
            dish_id = query[0].dish2
            dish_type = query[0].dish2_type
        elif dish_num == 3:
            dish_id = query[0].dish3
            dish_type = query[0].dish3_type
        elif dish_num == 4:
            dish_id = query[0].dish4
            dish_type = query[0].dish4_type
        elif dish_num == 5:
            dish_id = query[0].dish5
            dish_type = query[0].dish5_type
        elif dish_num == 6:
            dish_id = query[0].dish6
            dish_type = query[0].dish6_type
        else:
            print(f"Passed unacessible dish num: {dish_num}")

        query = Reaction.select().where(Reaction.dish_type == f"{dish_id}_{dish_type}")
        res = getattr(query[0], ingredient)

        return f"Эффект: {res}"
    else:
        print("Cannot apply ingredient as player is not playing a game at the moment")
        return "Not accessible!"


def highscore(user_id):
    query = Result.select().where(Result.user_id == user_id)
    if len(query) == 0:
        return "No highscore registered"
    else:
        score = query[0].highscore
        place = 1
        for s in Result.select().order_by(Result.highscore):
            if s.highscore < score:
                place += 1
            else:
                break
        return f"You are on the position #{place} with a score of {score}!"


def game_over(user_id):
    score = GameInProgress.select().where(GameInProgress.user_id == user_id)[0].score
    query = Result.select().where(Result.user_id == user_id)
    if len(query) > 0:
        if score < query[0].highscore:
            record = query.get()
            record.highscore = score
            record.save()
    else:
        Result.create(user_id=user_id, highscore=score)
    GameInProgress.select().where(GameInProgress.user_id == user_id)[0].delete_instance()
    user = User.select().where(User.user_id == user_id).get()
    user.isPlaying = False
    user.save()
    return f"You gave successfully fed 6 meals to the king! Your score is {score}"


def end_game(user_id):
    query = User.select().where(User.user_id == user_id)
    if query[0].isPlaying:
        GameInProgress.select().where(GameInProgress.user_id == user_id)[0].delete_instance()
        user = User.select().where(User.user_id == user_id).get()
        user.isPlaying = False
        user.save()
    else:
        print("There is no game to end!")


def lose(user_id, source):
    start_game(user_id)
    if source == "dog":
        return f"You gave a good food for a dog. You are beheaded\nIt is time to try again!\nCurrent score: \
{GameInProgress.select().where(GameInProgress.user_id == user_id)[0].score}"
    elif source == "king":
        return f"You gave a poisoned food for a king. You are beheaded\nIt is time to try again!\nCurrent score: \
{GameInProgress.select().where(GameInProgress.user_id == user_id)[0].score}"


def win(user_id):
    query = GameInProgress.select().where(GameInProgress.user_id == user_id).get()
    query.current_dish += 1
    query.save()
    if query.current_dish > 6:
        return game_over(user_id)
    else:
        return f"Congratulations, it's time for meal #{query.current_dish}"


def give_to_dog(user_id):
    query = User.select().where(User.user_id == user_id)
    if query[0].isPlaying:
        query = GameInProgress.select().where(GameInProgress.user_id == user_id)
        d_num = query[0].current_dish
        if d_num == 1:
            type = query[0].dish1_type
        elif d_num == 2:
            type = query[0].dish2_type
        elif d_num == 3:
            type = query[0].dish3_type
        elif d_num == 4:
            type = query[0].dish4_type
        elif d_num == 5:
            type = query[0].dish5_type
        elif d_num == 6:
            type = query[0].dish6_type
        else:
            print(f"Wrong current dish num given in dog: {d_num}")
        if type == 0:
            return lose(user_id, "dog")
        else:
            return win(user_id)
    else:
        print("Unable to give a meal to a dog while not in game!")
        return "Not accessible!"


def give_to_king(user_id):
    query = User.select().where(User.user_id == user_id)
    if query[0].isPlaying:
        query = GameInProgress.select().where(GameInProgress.user_id == user_id)
        d_num = query[0].current_dish
        if d_num == 1:
            type = query[0].dish1_type
        elif d_num == 2:
            type = query[0].dish2_type
        elif d_num == 3:
            type = query[0].dish3_type
        elif d_num == 4:
            type = query[0].dish4_type
        elif d_num == 5:
            type = query[0].dish5_type
        elif d_num == 6:
            type = query[0].dish6_type
        else:
            print(f"Wrong current dish num given in king: {d_num}")
        if type != 0:
            return lose(user_id, "king")
        else:
            return win(user_id)
    else:
        print("Unable to give a meal to a dog while not in game!")
        return "Not accessible!"
