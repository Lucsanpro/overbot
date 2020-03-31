import discord
from discord.ext import commands
import asyncio
import os

PREFIX = '&'

client = commands.Bot( command_prefix = PREFIX )


@client.event

async def on_ready():
	print( 'Бот в сети' )

	await client.change_presence( status = discord.Status.online, activity = discord.Game( 'Over Tournament' ) )

@client.event

async def on_member_join( member ):
	channel = client.get_channel( 663885558686416923 )

	role = discord.utils.get( member.guild.roles, id = 649309182662541353 )	

	await member.add_roles( role )
	await channel.send( embed = discord.Embed( description = f'**Добро пожаловать на наш сервер ``{ member.name }`` ! Наш бот дал вам роль Community. Притного общения.**', 
							color = 0x3bf30e ) )

#clear
@client.command( pass_context = True )
@commands.has_any_role('Administrator', 'General Administrator', 'Developer' )

async def clear(ctx, amount = 100 ):

    await ctx.channel.purge( limit = amount )
    await ctx.send(embed = discord.Embed(description = f'**:heavy_check_mark: Удалено {amount} сообщений.**', color=0x0c0c0c))

#kick

@client.command()
@commands.has_any_role('Administrator', 'General Administrator', 'Developer' )

async def kick(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        channel_log = client.get_channel(693822990198243328) #Айди канала логов

        await member.kick( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0xfd0004))
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен от рук {ctx.author.mention}\n:book: по причине: {reason}**', color=0xfd0004)) 

# Работа с ошибками кика

@kick.error 
async def kick_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))



#ban
@client.command()
@commands.has_any_role('Administrator', 'General Administrator', 'Developer' )

async def ban(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:
        
        channel_log = client.get_channel(693822990198243328) #Айди канала логов

        await member.ban( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0xfd0004)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован от рук {ctx.author.mention}\n:book: по причине: {reason}**', color=0xfd0004)) 

# Работа с ошибками бана

@ban.error 
async def ban_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))  

#unban

@client.command( pass_context = True )
@commands.has_any_role('Administrator', 'General Administrator', 'Developer' )

async def unban( ctx, *, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user

		await ctx.guild.unban( user )
		await ctx.send(embed = discord.Embed(description = f'Участник {member.mention} был разблокирован администратором {ctx.author.mention}!', color=0x64fd00 ))

		return



#mute

@client.command()
@commands.has_any_role('Administrator', 'General Administrator', 'Developer' )

async def mute(ctx,member: discord.Member, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        mute_role = discord.utils.get( ctx.message.guild.roles, name = 'mute' ) #Айди роли

        await member.add_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам руками {ctx.author.mention}\n:book: по причине: {reason}**', color=0xfd0004)) 

# Работа с ошибками мута


# мут на время
# &tempmute 10 user reason
@client.command()
@commands.has_any_role('Support', 'Moderator','Administrator', 'General Administrator', 'Developer')

async def tempmute(ctx,amount : int,member: discord.Member = None, reason = None):
	await ctx.channel.purge( limit = 1 )

	mute_role = discord.utils.get(member.guild.roles, id = 693560149071233165) #Айди роли
	channel_log = client.get_channel(693822990198243328) #Айди канала логов

	await member.add_roles( mute_role )
	await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} временно ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0xfd0004)) 
	await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был временно ограничен доступ к чатам руками {ctx.author.mention}\n:book: по причине: {reason}**', color=0xfd0004))
	await asyncio.sleep(amount)
	await member.remove_roles( mute_role )   

# Работа с ошибками мута на время

@tempmute.error 
async def tempmute_error(ctx, error):

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))
# bot
# Размут

@client.command()
@commands.has_any_role('Support', 'Moderator','Administrator', 'General Administrator', 'Developer') 

async def unmute(ctx,member: discord.Member = None): 


	if member is None:

		await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

	else:

		mute_role = discord.utils.get(member.guild.roles, id = 693560149071233165 ) #Айди роли

		await member.remove_roles( mute_role )
	await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был вернут доступ к чатам от {ctx.author.mention}.**', color=0x64fd00)) 


# Работа с ошибками размута

@unmute.error 

async def unmute_error(ctx, error):

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))


#help

@client.command()

async def ahelp( ctx ):
	await ctx.send(embed = discord.Embed(description = f'** &kick - исключить участника\n&ban - забанить участника\n&mute - перм мут\n&tempmute временный мут, пишется так &tempmute (время в секундах) user причина\n&clear (число сообщ, которые хочешь удалить)\n&unmute user\nunban user\nНа пока что всё, мб потом чёто ещё добавлю))) **', color = 0x8b09ff ) )

@client.command()

async def u( ctx ):
	await ctx.send('**Привет, как дела?**')
#news

@client.command()
async def news(ctx,url,*,args=None):
    channel = client.get_channel(693544294749044817)
    embed=discord.Embed(description=args, colour = 0xffed00)
    embed.set_image(url=url)
    await channel.send(embed=embed)


#повторялка

@client.command()
async def p(ctx,url,*,args=None):
	await ctx.channel.purge( limit = 1 )

	channel = client.get_channel(693557965512507392)
	embed=discord.Embed(description=args, colour = 0xffed00)
	await channel.send(embed=embed)   

@client.event

async def on_message_delete(message):
    if message.channel.id == 694492887609507920:
        await message.author.send(embed = discord.Embed(description = f"Приветствую, я представитель турнирной организации **Over Tournament**.\nВаша заявка была удалена по причине - __нарушение формы подачи заявок__ .", color = 0xfd0004 ))


#токен



token = os.environ.ger('BOT_TOKEN')
client.run( token )