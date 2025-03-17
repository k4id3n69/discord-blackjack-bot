import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


games = {}

def calculate_hand(hand):
    aces = hand.count(11)
    total = sum(hand)

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total

@bot.command(name='start-blackjack', help='Starts a new game of blackjack.')
async def start_blackjack(ctx):
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    random.shuffle(deck)

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    if calculate_hand(player_hand) == 21:
        await ctx.send(f"Blackjack! You win with {player_hand}!")
        return

    games[ctx.author.id] = (deck, player_hand, dealer_hand)

    await ctx.send(f"Game started!\nYour hand: {player_hand}\nDealer's hand: {dealer_hand[0]}")

@bot.command(name='hit', help='Draw another card.')
async def hit(ctx):
    deck, player_hand, dealer_hand = games[ctx.author.id]

    player_hand.append(deck.pop())

    player_total = calculate_hand(player_hand)
    if player_total > 21:
        del games[ctx.author.id]
        await ctx.send(f"You busted with {player_hand}! Game Over.")
    elif player_total == 21:
        del games[ctx.author.id]
        await ctx.send(f"You hit blackjack with {player_hand}! You Win!")
    else:
        games[ctx.author.id] = (deck, player_hand, dealer_hand)
        await ctx.send(f"Your hand is now {player_hand}")

@bot.command(name = 'stand', help='End your turn without drawing any more cards.')
async def stand(ctx):
    deck, player_hand, dealer_hand = games[ctx.author.id]

    player_total = calculate_hand(player_hand)
    dealer_total = calculate_hand(dealer_hand)

    while dealer_total < 17:
        dealer_hand.append(deck.pop())
        dealer_total = calculate_hand(dealer_hand)

    del games[ctx.author.id]

    if dealer_total > 21:
        await ctx.send(f"The dealer busted with {dealer_hand}! You Win!")
    elif dealer_total > player_total:
        await ctx.send(f"The dealer wins with {dealer_hand}!")
    elif dealer_total < player_total:
        await ctx.send(f"You win with {player_hand}!")
    else:
        await ctx.send("It's a tie!")

bot.run('MTM1MTA0MjQzNzk1ODg2MDgwMA.Gwf4Gk.El6jJST2F_wVF22hktjXLfaIkCQ8WICqGxbf5o')
