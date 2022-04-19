# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 19:02:07 2022

@author: Furtherun
"""

import matplotlib.pyplot as plt


labels = ['RR', 'RS', 'RG', 'SR', 'SS', 'SG', 'GR', 'GS', 'GG']
player1_means = [3106.1, 2919.2, 2753.7, 3141.0, 2841.0, 
             2941.2, 3286.1, 2889.4, 2946.2]
player2_means = list(map(lambda x: 3000*2-x, player1_means))

width = 0.35

fig, ax = plt.subplots()

ax.bar(labels, player1_means, width, label='Player one')
ax.bar(labels, player2_means, width, bottom=player1_means,
       label='Player two')

ax.set_ylim([2700,3400])
ax.set_xlabel("Strategy player one/player two")
ax.set_ylabel('Coin(s)')
ax.set_title('Coin(s) by strategy and player')
ax.legend()

plt.show()

