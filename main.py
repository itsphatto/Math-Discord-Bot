import discord
from discord.ext import commands
from discord import app_commands
import re
from itertools import chain, combinations
import matplotlib.pyplot as plt
import numpy as np
import os
import math

#PUT YOUR OWN BOT TOKEN HERE
TOKEN = 
#PUT YOUR OWN BOT TOKEN HERE

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="dm", description="Send a direct message to a user")
async def dm(interaction: discord.Interaction, user_id: str, message: str):
    try:
        user = await bot.fetch_user(user_id)
        if user is not None: 
            await user.send(message)
            await interaction.response.send_message(f"Message sent to {user.name}")
        else:
            await interaction.response.send_message("User not found.")
    except discord.Forbidden:
        await interaction.response.send_message("I do not have permission to send a message to this user.")
    except discord.HTTPException:
        await interaction.response.send_message("Failed to send the message.")
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}")


@bot.tree.command(name="union", description="A ∪ B")
async def union(interaction: discord.Interaction, set1: str, set2: str):
    try:
        numbers1 = set(map(int, re.findall(r'\d+', set1)))
        numbers2 = set(map(int, re.findall(r'\d+', set2)))
        result = numbers1 | numbers2
        response = "{" + ", ".join(map(str, sorted(result))) + "}"
        await interaction.response.send_message(response)
    except ValueError:
        await interaction.response.send_message("error try using brain ex: `/union {1,2,3} {4,5,6}`")


@bot.tree.command(name="different", description="A-B")
async def different(interaction: discord.Interaction, set1: str, set2: str):
    try:
        set1 = set(map(int, set1.strip('{}').split(',')))
        set2 = set(map(int, set2.strip('{}').split(',')))
        difference = set1 - set2
        await interaction.response.send_message(f"Difference between sets is: {difference}")
    except Exception as e:
        await interaction.response.send_message(f"@itsphatto Error: {str(e)}")


@bot.tree.command(name="subset", description="⊆ A")
async def subset(interaction: discord.Interaction, set_str: str):
    try:
        elements = set(map(str, set_str.strip('{}').split(',')))
        def all_subsets(s):
            return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))
        subsets = all_subsets(elements)
        formatted_subsets = ["{" + ", ".join(map(str, subset)) + "}" if subset else "∅" for subset in subsets]
        await interaction.response.send_message("Subsets: " + ", ".join(formatted_subsets))
    except Exception as e:
        await interaction.response.send_message(f"Error: {str(e)}")

@bot.tree.command(name='solve_quadratic', description='Solves a quadratic equation of the form ax^2 + bx + c = 0')
async def solve_quadratic(interaction: discord.Interaction, a: float, b: float, c: float):

    try:

        discriminant = b ** 2 - 4 * a * c
        print(f'Discriminant: {discriminant}')

        if discriminant < 0:
            # Complex roots
            real_part = -b / (2 * a)
            imaginary_part = math.sqrt(-discriminant) / (2 * a)
            await interaction.response.send_message(
                f"x ∉ R\n"
                f"Complex roots: x₁ = {real_part:.2f} + {imaginary_part:.2f}i, "
                f"x₂ = {real_part:.2f} - {imaginary_part:.2f}i"
            )
        elif discriminant == 0:
            # One real root
            x = -b / (2 * a)
            await interaction.response.send_message(f"one real root: x = {x:.2f}")
        else:
            # Two real roots
            root1 = (-b + math.sqrt(discriminant)) / (2 * a)
            root2 = (-b - math.sqrt(discriminant)) / (2 * a)
            await interaction.response.send_message(
                f"two real roots: x₁ = {root1:.2f}, x₂ = {root2:.2f}"
            )

    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')

@bot.tree.command(name='logic', description='logic boolean calculation')
async def logic_operation(interaction: discord.Interaction, a: bool, b: bool, operation: str):
    if operation == 'AND':
        result = a and b
        await interaction.response.send_message(f"{a} ^ {b} = {result}")
    elif operation == 'OR':
        result = a or b
        await interaction.response.send_message(f"{a} ∨ {b} = {result}")
    elif operation == 'NOT':
        result_a = not a
        result_b = not b
        await interaction.response.send_message(f"¬ {a} = {result_a}, ¬ {b} = {result_b}")
    else:
        await interaction.response.send_message(" use ^(and), ∨(or), or ¬ (not) dumb ass")


@bot.tree.command(name="collatz", description="Compute and visualize the Collatz sequence")
async def collatz(interaction: discord.Interaction, num: int):
    if num <= 0:
        await interaction.response.send_message("Please enter a positive integer.", ephemeral=True)
        return

    sequence = []
    n = num
    while n != 1:
        sequence.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    sequence.append(1)  # Final step

    plt.figure(figsize=(10, 5))
    plt.plot(range(len(sequence)), sequence, marker="o", linestyle="-", color="b", markersize=3)
    plt.axhline(y=1, color='r', linestyle='dashed', label="Reaches 1")
    plt.yscale("log")  # Log scale for large numbers
    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.title(f"Collatz Sequence for {num}")
    plt.legend()
    plt.grid(True)

    file_path = "collatz.png"
    plt.savefig(file_path)
    plt.close()



    await interaction.response.send_message(file=discord.File(file_path))


bot.run(TOKEN)
