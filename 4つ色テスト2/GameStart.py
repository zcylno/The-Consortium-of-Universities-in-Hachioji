import ColorGame as Game
import DQN as T

action_dim = 4

def run():
    count = 0
    Game.game_init()
    farmer = Game.farmer



    
    train = T.Train(action_dim)
    train.load_nets(12000000)
    state = Game.get_image()

    while True:
        Game.close_win()
        Game.draw_and_update()
        Game.update_score()
        #farmer.move()

        action = train.get_action(state)
        #farmer.move_(action)
        state_next= Game.get_image()
        train.memory.memory_push(state, action, farmer.score, state_next)
        state = state_next

        if farmer.score > 0:
            Game.reset_score()

        if count > 0 and count % 1000 == 0:
            Game.set_cash(count)
        if count > 0 and count % 20000 == 0:
            Game.plt_cash()
        #if count >= 1000 and count % 1000 == 0:
        #    Game.set_cash(count)
        #if count > 0 and count % 20000 == 0:
        #    Game.plt_cash()
        Game.plt_img(state_next)

        #if count >= 10000 and count % 2000 == 0:
        #    for i in range(50):
        #        train.optimize()

        #if count >= 2000000 and count % 2000000 == 0:
        #   train.save_nets(count)


        count += 1
        #print(count)

        
run()