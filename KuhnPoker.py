# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 10:27:45 2022

@author: Furtherun
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from typing import List


BET = "BET"                         #加注
CALL = "CALL"                       #跟注
CHECK = "CHECK"                     #验牌
FOLD = "FOLD"                       #认输

CARD12, CARD21 = "12", "21"
CARD13, CARD31 = "13", "31"
CARD23, CARD32 = "23", "32"
CARD1, CARD2, CARD3 = "1", "2", "3"

CARDS_LIST = [CARD12, CARD21, CARD13, CARD31, CARD23, CARD32]

INITIAL_GAME_COIN = 3000
TOTAL_NUMBER_OF_GAMES = 1000

RANDOM = "RANDOM"
STABLE = "STABLE"
GREEDY = "GREEDY"

STRATEGY_FOR_PLAYER1 = GREEDY
STRATEGY_FOR_PLAYER2 = GREEDY


class GameTreeNode:
    def __init__(self):
        self.history: List[str] = []
        self.cards: str = CARD12
    
    def print_cards(self) -> None:
        """
        Print cards of player one and player two in game tree node.
        """
        print("Player one gets poker {}, player two gets poker {}.".
              format(self.cards[0], self.cards[1]))
    
    def print_history(self) -> None:
        """
        Print players' actions so far.
        """
        for idx, action in enumerate(self.history):
            print("Player {} takes {}.".
                  format("one" if idx%2==0 else "two", action))
    
class PlayerNode(GameTreeNode):
    def __init__(self, cards: str, history: List[str]):
        self.cards = cards
        self.history = history
        
        self.player_id = len(self.history) % 2
        
        self.action_list: List[str] = []
        
        self.strategy_dict = {RANDOM: self.take_random_strategy(), 
                              STABLE: self.take_stable_strategy(),
                              GREEDY: self.take_greedy_strategy()}
        
    def evaluate(self) -> int:
        """
        Return the coin(s) of player wins(loses) in this game.
        """
        self.take_acton()
        
        # print(self.action_list)
        
        if self.is_leaf_node():
            return self.judge_score()
        
        opponent = PlayerNode(self.cards, self.history)
        
        return -opponent.evaluate()
    
    def judge_score(self) -> int:
        """
        Return the results at the end of this round of games.
        """
        if self.is_double_check():
            return 1 if self.is_player_higher() else -1
        elif self.is_fold():
            return -1
        else:
            return 2 if self.is_player_higher() else -2
    
    def is_player_higher(self) -> bool:
        """
        Return if player's card is higher than opponent's.
        """
        return self.cards[self.player_id] > self.cards[1 - self.player_id]
    
    def is_fold(self) -> bool:
        """
        Return if player takes FOLD action in this round.
        """
        return self.history[-1] == FOLD
    
    def is_call(self) -> bool:
        """
        Return if player takes CALL action in this round.
        """
        return self.history[-1] == CALL
    
    def is_double_check(self) -> bool:
        """
        Return if two players both take CHECK actions.

        """
        return self.history.count(CHECK) == 2
    
    def is_leaf_node(self) -> bool:
        """
        Return if this round of the game is end.
        """
        return self.is_fold() or self.is_call() or self.is_double_check()
    
    def take_acton(self) -> None:
        """
        Update actions player maybe takes by player's strategy.
        """
        if self.player_id == 0:
            self.action_list = self.strategy_dict[STRATEGY_FOR_PLAYER1]
        else:
            self.action_list = self.strategy_dict[STRATEGY_FOR_PLAYER2]
        
        self.history.append(self.sample_one())
    
    def sample_one(self) -> str:
        """
        Return one action player actually takes.
        """
        return random.choice(self.action_list)
    
    def take_random_strategy(self) -> []:
        """
        Returns actions player maybe takes in random startegy.
        """
        if len(self.history) == 0:
            return [CHECK, BET]
        elif len(self.history) == 2:
            return [FOLD, CALL]
        else:
            if self.history[-1] == CHECK:
                return [CHECK, BET]
            else:
                return [FOLD, CALL]
    
    def take_stable_strategy(self) -> []:
        """
        Returns actions player maybe takes in stable startegy
        """
        if self.cards[self.player_id] == CARD1:
            if len(self.history) == 0:
                return [CHECK]
            else:
                return [FOLD] if self.history[-1] == BET else [CHECK]
        elif self.cards[self.player_id] == CARD2:
            if len(self.history) == 0:
                return [CHECK]
            elif len(self.history) == 2:
                return [CALL]
            else:
                return [CHECK] if self.history[-1] == CHECK else [FOLD]
        else:
            if len(self.history) == 0:
                return [BET]
            elif len(self.history) == 1:
                return [BET] if self.history[-1] == CHECK else [CALL]
            else:
                return [CALL]
      
    def take_greedy_strategy(self) -> []:
        """
        Returns actions player maybe takes in greedy(my) startegy.
        
        Players will try best to BET in the game,
        if they get poker 1, they would BET(or CALL) with a 
        probaility of 0.3, for poker 2 is 0.6,
        and for poker 3 is 1. 
        """
        if self.cards[self.player_id] == CARD1:
            if len(self.history) == 0:
                return [CHECK]*7 + [BET]*3
            else:
                return [FOLD] if self.history[-1] == BET \
                    else [CHECK]*9 + [BET]
        elif self.cards[self.player_id] == CARD2:
            if len(self.history) == 0:
                return [CHECK]*4 + [BET]*6
            else:
                return [FOLD]*4 + [CALL]*6 if self.history[-1] == BET \
                    else [CHECK]*4 + [BET]*6
        else:
            if len(self.history) == 0:
                return [BET]
            else:
                return [CALL] if self.history[-1] == BET \
                    else [BET]

class InitNode(GameTreeNode):
    def __init__(self):
        super().__init__()
        self.player1_coin_list = [INITIAL_GAME_COIN]
        self.player2_coin_list = [INITIAL_GAME_COIN]
        
    def start_one_new_game(self, cards: str,
                           display_cards = False,
                           display_history = False,
                           display_result = False) -> int:
        """
        Return the result of one game.
        """
        
        self.cards = cards
        self.history = []
        
        player = PlayerNode(self.cards, self.history)
        
        player_win = player.evaluate()
        
        if display_cards:
            super().print_cards()
        
        if display_history:
            super().print_history()
        
        if display_result:
            self.show_result(player_win)
            
        return player_win
    
    def run_ngames(self, coins = 3000, n = 1000,
                   show_one_game_datails = False,
                   show_step_result = False,
                   show_coin_list = True) -> None:
        """
        Run the game n times, deal with details.
        """
        player1_coin = player2_coin = coins
        t = 0
        while player1_coin >= 2 and player2_coin >= 2 and t < n:
            t += 1
            
            if show_step_result:
                print("This is game {}.".format(t))
            
            random.shuffle(CARDS_LIST)
            cards = random.choice(CARDS_LIST)
            if show_one_game_datails:
                player1_coin += self.start_one_new_game(cards,
                    display_cards = True,
                    display_history = True,
                    display_result = True)
            else:
                player1_coin += self.start_one_new_game(cards)
            
            player2_coin = 2 * coins - player1_coin
            
            self.player1_coin_list.append(player1_coin)
            self.player2_coin_list.append(player2_coin)
            
            if show_step_result:
                self.print_coin_result()
        
        if show_coin_list:
            self.draw_coin_list()
            
            self.print_num_of_win_game()
            self.print_num_of_final_coin()
    
    def print_coin_result(self) -> None:
        """
        Print players' coins by now
        """
        print("Player one has {} coin(s), player two has {} coin(s).".
              format(self.player1_coin_list[-1],
                     self.player2_coin_list[-1]))
    
    def print_num_of_final_coin(self) -> None:
        print("Player one finally has {} coin(s).".
              format(self.player1_coin_list[-1]))
        
        print("Player two finally has {} coin(s).".
              format(self.player2_coin_list[-1]))
    
    def print_num_of_win_game(self) -> None:
        player1_win_num = 0
        for idx, coin in enumerate(self.player1_coin_list):
            if idx > 0 and self.player1_coin_list[idx] > \
                self.player1_coin_list[idx-1]:
                    player1_win_num += 1
        
        print("Player one wins {}({:.1%}) time(s).".
              format(player1_win_num,
                     player1_win_num/TOTAL_NUMBER_OF_GAMES))
        print("Player two wins {}({:.1%}) time(s).".
              format(TOTAL_NUMBER_OF_GAMES-player1_win_num,
                     1 - player1_win_num/TOTAL_NUMBER_OF_GAMES))
    
    def draw_coin_list(self) -> None:
        """
        dwaw coins winned/lossed in process of one game.
        """
        x = np.arange(len(self.player1_coin_list))
        plt.plot(x, self.player1_coin_list,
                           self.player2_coin_list)
        plt.legend(["Player one: " + STRATEGY_FOR_PLAYER1, 
                    "Player two: " + STRATEGY_FOR_PLAYER2],
                   loc="upper left")
        plt.xlabel("number of games")
        plt.ylabel("number of coins")
        plt.show()
        
    def show_result(self, result: int) -> None:
        """
        Print coin(s) winned/losed in one game.
        """
        if result == 0:
            print("The game is draw!")
        elif abs(result) == 1:
            print("Player {} wins {} coin from player {}.".
                  format("one" if result > 0 else "two",
                     abs(result), "two" if result > 0 else "one"))
        else:
            print("Player {} wins {} coins from player {}.".
                  format("one" if result > 0 else "two",
                     abs(result), "two" if result > 0 else "one"))
            
def run_game() -> None:
    """
    entry program
    """
    game = InitNode()
    
    game.run_ngames(INITIAL_GAME_COIN, TOTAL_NUMBER_OF_GAMES,
                    show_one_game_datails=True,
                    show_step_result=True,
                    show_coin_list = True)
    
if __name__ == '__main__':
    
    # one run case
    run_game()
    
    # for _ in range(10):
    #     print(_)
    #     run_game()
        
    