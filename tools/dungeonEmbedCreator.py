from turtle import title
from discord import Embed, Colour

class DungeonEmbedCreator():

    def createEmbed(self, state, response, ctx):
        if (state == 'NORMAL'):
            return self.normalEmbed(response, ctx)
        elif (state == 'DEATH'):
            return self.deathEmbed(response, ctx)
        elif (state == 'ITEM'):
            return self.itemEmbed(response, ctx)
        elif (state == 'WIN'):
            return self.winEmbed(response, ctx)
        elif (state == 'FINISH'):
            return self.finishEmbed(response, ctx)
        else:
            return self.leaveEmbed(response, ctx)

    def normalEmbed(self, response, ctx):
        embed = Embed(title="Dungeon Crawler", colour=Colour(0x00FFFF))

        embed.set_author(name=f"{ctx.author.name}'s dungeon", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Dungeon Crawler Beta")

        content = ""
        for str in response['logs']:
            content = content + str + '\n'
        content = content + '---------------------------------------------------------\n'
        content = content + f"{response['enemyType']}-:heart: {response['enemyHealth']} :dagger: {response['enemyAttack']}\n"
        content = content + f"{ctx.author.name}-:heart: {response['heroHealth']} :test_tube: {response['heroMana']} :dagger: {response['heroAttack']} :shield: {response['heroDefense']}\n"
        content = content + '---------------------------------------------------------\n'
        content = content + f"What will you do {ctx.author.name}?\n"
        content = content + "`ATTACK | ITEM | SKILL`"

        embed.add_field(name=f"It's {ctx.author.name}'s turn!", value=content)

        return embed

    def deathEmbed(self, response, ctx):
        embed = Embed(title="Dungeon Crawler", colour=Colour(0x00FFFF))

        embed.set_author(name=f"{ctx.author.name}'s dungeon", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Dungeon Crawler Beta")

        content = ""
        for str in response['logs']:
            content = content + str + '\n'

        embed.add_field(name="You Lose!", value=content)

        return embed

    def itemEmbed(self, response, ctx):
        embed = Embed(title="Dungeon Crawler", colour=Colour(0x00FFFF))

        embed.set_author(name=f"{ctx.author.name}'s dungeon", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Dungeon Crawler Beta")

        content = ""
        for str in response['logs']:
            content = content + str + '\n'

        content = content + "`Choose item with number (from 1)`"

        embed.add_field(name=f"{ctx.author.name}'s items", value=content)

        return embed

    def winEmbed(self, response, ctx):
        embed = Embed(title="Dungeon Crawler", colour=Colour(0x00FFFF))

        embed.set_author(name=f"{ctx.author.name}'s dungeon", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Dungeon Crawler Beta")

        content = ""
        for str in response['logs']:
            content = content + str + '\n'

        content = content + "`CONTINUE | LEAVE`"

        embed.add_field(name=f"You've defeated an enemy", value=content)

        return embed

    def finishEmbed(self, response, ctx):
        embed = Embed(title="Dungeon Crawler", colour=Colour(0x00FFFF))

        embed.set_author(name=f"{ctx.author.name}'s dungeon", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Dungeon Crawler Beta")

        content = ""
        for str in response['logs']:
            content = content + str + '\n'

        embed.add_field(name=f"Congratulation", value=content)

        return embed

    def leaveEmbed(self, response, ctx):
        embed = Embed(title="Dungeon Crawler", colour=Colour(0x00FFFF))

        embed.set_author(name=f"{ctx.author.name}'s dungeon", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Dungeon Crawler Beta")

        content = ""
        for str in response['logs']:
            content = content + str + '\n'

        embed.add_field(name=f"{ctx.author.name} flee", value=content)

        return embed