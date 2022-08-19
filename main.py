import discord
import re
import datetime
import os
from discord.ext import commands
from replit import db

client = commands.Bot(command_prefix='$')

#del db["votes"]

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.command()
async def role(ctx, *args):
  print(ctx.message.author.roles[0].id)
  #await ctx.send(f"Your role is: {ctx.message.author.roles}")
  
#
# createvote
#
# Takes in 3 arguments in which it validates the arguments
# to formulate a valid vote
#
# Outputs to the user whether or not the vote was casted
# succesfully.
#
# Example usage:
# createvote(ctx, args, 0/1)
#
async def createvote(ctx, args, negotiable):
  vote_message = " ".join(args)
  vote_message_list = vote_message.split()

  if len(vote_message_list) >= 2:
    # Getting the attributes of the vote
    vote_type = vote_message_list[0]
    user_id = vote_message_list[1]
    vote_duration = vote_message_list[2]
    vote_id = " ".join(vote_message_list[3:])

    # Checking if the vote_type that was passed in is valid
    if check_vote_type_existance(vote_type) >= 0:

      # Checking if the vote_duration that was pssed in is valid
      if check_duration(vote_duration) == True:
        
        # Getting the id of the user that got @'ed
        user_id = user_id.replace('<', '')
        user_id = user_id.replace('>', '')
        user_id = user_id.replace('@', '')
      
        vote_information = [vote_id, user_id, vote_type, vote_duration, negotiable, 0, 0]
      
        added_vote = add_vote(vote_information)
  
        # Checking if the vote was added succesfully
        if added_vote:

          # Add vote to "uservotes"
          
          await ctx.send("```Added vote \"" + vote_id + "\"```")
        else:
          await ctx.send("```The vote \"" + vote_id + "\" is already being casted.\n\nTo see all ongoing votes, use the command $listvotes```")
      
      else:
        await ctx.send("```Invalid duration, please try again. The format for a duration is [HourNumberHere]hr[MinuteNumberHere]m[SecondNumberHere]s.\n\nExample: 1hr26min2s or Indefinite```")
      
    else:
      await ctx.send("```Invalid vote type, please try again. To see a list of available vote types use the command $listvotetypes```")
      
  else:
    await ctx.send("```Invalid command, please try again. The format is $nonnegotiabledurationvote / lowernegotiabledurationvote VoteTypehere @UsernameHere VoteDurationHere VoteTitleHere\n\nTo see a full list of vote types, use the command $listvotetypes```")

#
# nonnegotiabledurationvote
#
# Takes in a tuple of arguments which are then passed
# to the createvote function to attempt to create a valid vote
# that its duration is non negotiable.
#
# Outputs to the user whether or not the vote was casted
# succesfully.
#
# Example Usage:
# $nonnegotiabledurationvote VoteTypehere @UsernameHere VoteDurationHere VoteTitleHere
#
@client.command()
async def nonnegotiabledurationvote(ctx, *args):
  await createvote(ctx, args, 0)

#
# lowernegotiabledurationvote
#
# Takes in a tuple of arguments which are then passed
# to the createvote function to attempt to create a valid vote
# that its duration is negotiable to be lower.
#
# Outputs to the user whether or not the vote was casted
# succesfully.
#
# Example Usage:
# $lowernegotiabledurationvote VoteTypehere @UsernameHere VoteDurationHere VoteTitleHere
#
@client.command()
async def lowernegotiabledurationvote(ctx, *args):
  await createvote(ctx, args, 1)

#
# removevote
#
# Takes in 1 string argument which represent a vote id.
# Using that vote id it will determine if it is able
# to remove the vote.
#
# Outputs to the user if the vote was removed successfully
# or not.
#
# Example usage:
# $removevote Being annoying
#
@client.command()
async def removevote(ctx, *args):
  remove_message = " ".join(args)

  # Checking if the command was used correctly
  if len(remove_message) >= 1:
    
    removed_vote = remove_vote(remove_message)

    # Checking if the vote was removed successfully
    if removed_vote:
      await ctx.send("```Removed vote \"" + remove_message + "\" from the voting poll.```")
    else:
      await ctx.send("```The vote \"" + remove_message + "\" does not exist.```")

  else:
    await ctx.send("```Invalid command, please try again. The format is $removevote VoteNameHere```")


@client.command()
async def yesvote(ctx, *args):
  vote_id = " ".join(args)

  # Checking if the passed in vote_id exists in the database
  if check_vote_existance == True:

    # Checking if the person has already voted

    
  else:
    await ctx.send("```The vote \"" + remove_message + "\" does not exist.```")
#
# addvotetype
#
# Takes in 1 argument which represents a vote type.
# Using that vote type  it will determine if it is able
# to add the vote type to the database.
#
# Outputs to the user if the vote type was successfully
# added or not.
#
# Example usage:
# $addvotetype mute
#
@client.command()
async def addvotetype(ctx, *args):
  message_list = [" ".join(args)]

  # Checking if the command was used correctly
  if len(message_list) == 1:

    # Checking if the "votetypes" key exists in the database
    if "votetypes" in db.keys():
      vote_types = db["votetypes"]
      vote_type = message_list[0]

      # Checking if the vote type already exists in the database
      if check_vote_type_existance(vote_type) == -1:
        vote_types.append(vote_type)
        db["votetypes"] = vote_types
        await ctx.send("```Added vote type \"" + vote_type + "\"```")
      else:
        await ctx.send("```Vote type \"" + vote_type + "\" has already been added.```")
        
    else:
      db["votetypes"] = [message_list[0]]
      await ctx.send("```Added vote type \"" + message_list[0] + "\"```")

  else:
    await ctx.send("```Invalid command, please try again. The format is $addvotetype VoteTypeHere```")

#
# removevotetype
#
# Takes in 1 argument which represents a vote type
# Using that vote type it will look through the database
# to remove it.
#
# Outputs to the user if the vote type was removed
# successfully or not.
#
# Example usage:
# $removevotetype mute
#
@client.command()
async def removevotetype(ctx, *args):
  message_list = [" ".join(args)]

  # Checking if the command was used correctly
  if len(message_list) == 1:

    # Checking if the "votetypes" key exists in the database
    if "votetypes" in db.keys():
      vote_types = db["votetypes"]
      vote_type = message_list[0]
      
      found_type = check_vote_type_existance(vote_type)

      # Checking if the votetype was found in the database
      if found_type >= 0:
        del vote_types[found_type]
        db["votetypes"] = vote_types
        await ctx.send("```Removed vote type \"" + vote_type + "\"```")
      else:
        await ctx.send("```The vote type \"" + vote_type + "\" does not exist.```")
      
    else:
      await ctx.send("```There are currently no vote types to remove. Add some using the command $addvotetype VoteTypeHere```")

  else:
    await ctx.send("```Invalid command, please try again. The format is $removevotetype VoteTypeHere```")

#
# listvotes
#
# Takes in zero arguments, which it will then
# look in the "votes" key in the database
# and retrieve all votes.
#
# Outputs all votes to the user if any were found.
#
# Example usage:
# $listvotes
#
@client.command()
async def listvotes(ctx, *args):
  input_string = " ".join(args)

  # Checking if the command was used correctly
  if len(input_string) == 0:
    votes_list = []

    # Checking if the "votes" key exists in the database
    if "votes" in db.keys():
      votes_list = db["votes"]
      votes = ""

      # Checking if there are any vote types
      if len(votes_list) > 0:
        
        # Adding all vote types into one string
        for i in range(len(votes_list)):
          vote_title = votes_list[i][0]
          user_id = votes_list[i][1]
          vote_type = votes_list[i][2]
          vote_duration = votes_list[i][3]
          negotiable = votes_list[i][4]
          num_vote_yes = votes_list[i][5]
          num_vote_no = votes_list[i][6]

          # Retrieving the user object from the vote and the username
          vote_user_object = await ctx.message.guild.fetch_member(user_id)
          vote_username = vote_user_object.display_name
          
          # Formulating the final string
          votes += "Vote Title: "
          votes += vote_title

          votes += " | Vote Type: "
          votes += vote_type
          
          votes += " | Recipient: "
          votes += vote_username

          votes += " | Duration: "
          votes += vote_duration

          votes += " | Negotiable: "
          if negotiable == 1:
            votes += "Yes"
          else:
            votes += "No"

          votes += " | Yes Votes: "
          votes += str(num_vote_yes)

          votes += " | No Votes: "
          votes += str(num_vote_no)

          if i < len(votes_list) - 1:
            votes += "\n"
  
        await ctx.send("```Votes:\n\n" + votes + "```")
      else:
        await ctx.send("```There are currently no votes. Add Add some using the command $createvote VoteTypehere @UsernameHere VoteTitleHere```")

    else:
      await ctx.send("```There are currently no votes. Add Add some using the command $createvote VoteTypehere @UsernameHere VoteTitleHere```")
    
  else:
    await ctx.send("```Invalid command, please try again. The format is $listvotes```")
    
#
# listvotetypes
#
# Takes in zero arguments, which it will then
# look in the "votetypes" key in the database
# and retrieve all vote types.
#
# Outputs all votetypes to the user if any were found.
#
# Example usage:
# $listvotetypes
#
@client.command()
async def listvotetypes(ctx, *args):
  input_string = " ".join(args)

  # Checking if the command was used correctly
  if len(input_string) == 0:
    vote_types_list = []

    # Checking if the "votetypes" key exists in the database
    if "votetypes" in db.keys():
      vote_types_list = db["votetypes"]
      vote_types = ""

      # Checking if there are any vote types
      if len(vote_types_list) > 0:
        
        # Adding all vote types into one string
        for i in range(len(vote_types_list)):
          vote_types += vote_types_list[i]
          if i < len(vote_types_list) - 1:
            vote_types += "\n"
  
        await ctx.send("```Vote Types:\n\n" + vote_types + "```")
      else:
        await ctx.send("```There are currently no vote types. Add Add some using the command $addvotetype VoteTypeHere```")

    else:
      await ctx.send("```There are currently no vote types. Add some using the command $addvotetype VoteTypeHere```")
    
  else:
    await ctx.send("```Invalid command, please try again. The format is $listvotetypes```")

#
#
#
@client.command()
async def listvotedurations(ctx, *args):
  input_string = " ".join(args)

  if len(input_string) == 0:
    
    # Checking if the "votedurations" key exists in the database
    if "votedurations" in db.keys():
      vote_durations_list = db["votedurations"]
      vote_durations = ""

      # Checking if there are any vote types
      if len(vote_durations_list) > 0:
        
        # Adding all vote types into one string
        for i in range(len(vote_durations_list)):

          vote_durations += "Vote Title: "
          vote_durations += vote_durations_list[i][0]
          vote_durations += " | "

          vote_durations += "Vote effect lasting date: "
          vote_durations += vote_durations_list[i][1]
          
          if i < len(vote_durations_list) - 1:
            vote_durations += "\n"
  
        await ctx.send("```Vote Durations:\n\n" + vote_durations + "```")
      else:
        await ctx.send("```There are currently no vote effect lasting dates.\n\nCreate some votes and get them passed to see effect lasting dates!```")
    
    else:
      await ctx.send("```There are currently no vote effect lasting dates.\n\nCreate some votes and get them passed to see effect lasting dates!```")
  
  else:
    await ctx.send("```Invalid command, please try again. The format is $listvotedurations```")
#
# check_vote_existance
#
# Takes in a vote_id, which will then be used to check
# if it exists in the database.
#
# Returns true if it exists, false otherwise.
#
# Exaple usage:
# check_vote_existance("Being annoying")
#
def check_vote_existance(vote_id):
  votes = []

  # Checking if the key "votes" exists in the database
  if "votes" in db.keys():
    votes = db["votes"]
    for i in range(len(votes)):
      if votes[i][0] == vote_id:
        return True

    return False
  else:
    db["votes"] = votes
    return False

#
# check_vote_type_existance
#
# Takes in a vote_type, which will then be used to check
# if it exists in the database.
#
# Returns the index if it was found, -1 otherwise.
#
# Exaple usage:
# check_vote_type_existance("mute")
#
def check_vote_type_existance(vote_type):
  vote_types = []

  # Checking if the key "votetypes" exists in the database
  if "votetypes" in db.keys():
    vote_types = db["votetypes"]
    for i in range(len(vote_types)):
      if vote_types[i] == vote_type:
        return i

    return -1
  else:
    db["votetypes"] = vote_types
    return -1

#
# check_vote_duration_existance
#
# Takes in a vote_id, which will then be used to check
# if it exists along with the its duration.
#
# Returns the index if it was found, -1 otherwise.
#
# Exaple usage:
# check_vote_duration_existance("Being annoying")
#
def check_vote_duration_existance(vote_id):
  vote_durations = []

  # Checking if the key "votedurations" exists in the database
  if "votedurations" in db.keys():
    vote_durations = db["votedurations"]
    for i in range(len(vote_durations)):
      if vote_durations[i][0] == vote_id:
        return i

    return -1
  else:
    db["votedurations"] = vote_durations
    return -1

#
# check_user_vote_status
#
# Given a user_id and a vote_id, it will check if the user
# has already voted for the vote or not.
#
# Returns true if the user has voted for the given vote_id,
# otherwise it returns false.
#
def check_user_vote_status(vote_id):
  user_votes = []

  # Checking if the key "uservotes" exists in the database
  if "uservotes" in db.keys():
    user_votes = db["uservotes"]

def check_uservotes_existance(vote_id)

#
# add_vote
#
# Takes in a list, which contains information regarding a vote
# that needs to be added.
#
# Returns true if the vote was added to the database succesfully,
# false otherwise.
#
# Exaple usage:
# add_vote(["Being annoying", 123456789, "mute", 0, 0])
#
def add_vote(vote_information):
  if "votes" in db.keys():
    votes = db["votes"]

    # Checking if there is already a vote in the database
    # with the same vote_id
    if check_vote_existance(vote_information[0]) == False:
      votes.append(vote_information)
      db["votes"] = votes
      return True
    else:
      return False
  else:
    
    # Creating a new "votes" key in the database
    db["votes"] = [vote_information]
    return True

#
# remove_vote
#
# Takes in one string argument which represent a vote id.
# Using that vote id it will determine if it is able
# to remove the vote from the database.
#
# Returns true or false depending if the vote was
# successfully removed or not.
#
# Example usage:
# remove_vote("Being annoying")
#
def remove_vote(vote_id):
  votes = []

  # Checking if the key "votes" exists in the database
  if "votes" in db.keys():
    votes = db["votes"]

    # Checking the existance of the vote id in the database
    if check_vote_existance(vote_id):
      for i in range(len(votes)):
        if votes[i][0] == vote_id:
          del votes[i]
          db["votes"] = votes
          return True
    else:
      return False

#
# add_vote_duration
#
# Takes in a list, which contains information regarding a vote
# duration that needs to be added.
#
# Returns true if the vote was added to the database succesfully,
# false otherwise.
#
# Exaple usage:
# add_vote_duration(["Being annoying", datetime_obj)
#
def add_vote_duration(duration_information):
  if "votedurations" in db.keys():
    vote_durations = db["votedurations"]

    # Checking if there is already a vote duration in the database
    # with the same vote_id
    if check_vote_duration_existance(duration_information[0]) == -1:
      vote_durations.append(duration_information)
      db["votedurations"] = vote_durations
      return True
    else:
      return False
  else:
    
    # Creating a new "votedurations" key in the database
    db["votedurations"] = [duration_information]
    return True

def add_vote_to_uservotes(vote_id):
  # Checking if the uservotes key exists in the database
  if "uservotes" in db.keys():

    # Checking if there is already
  
  else:
    db["uservotes"] = [[vote_id, []]]
    return True
    

#
#  check_duration
#
# Takes in one string argument that represents a duration.
# It checks to see if the duration is valid on a certain pattern.
#
# Returns true if the duration is valid, otherwise it returns false.
#
# Example usage:
# check_duration("1hr26m2s")
def check_duration(duration):
  duration_pattern = re.compile("([0-9][0-9]*hr([0-5][0-9]|[0-9])m([0-9]|[0-5][0-9])s)|((i|I)(n|N)(d|D)(e|E)(f|F)(i|I)(n|N)(i|I)(t|T)(e|E))")

  if re.fullmatch(duration_pattern, duration):
    return True
  else:
    return False

#
# calculate_duration
#
# Given a duration string in the form of
# [Hours]hr[Minutes]min[Seconds]s such as 1hr26min6s
# it will calculate the date and time of the current date and time
# plus the duration.
#
# Returns a datetime object representing the addition of
# current date and time and the duration that was given.
#
# Example Usage:
# calculate_duration("1hr26min2s")
#
def calculate_duration(duration):
  # Getting the hours, minutes, and seconds from the duration.
  duration_split = re.split("[hr+m+s]", duration)
  duration_split = list(filter(None, duration_split)) # This was done due to some empty string appearing in the list

  hour = int(duration_split[0])
  minute = int(duration_split[1])
  second = int(duration_split[2])

  # Initiating a new time delta with the retrieved times
  set_time = datetime.timedelta(hours=hour, minutes=minute, seconds=second)
  current_time = datetime.datetime.now()

  added_time = set_time + current_time
  return added_time

client.run(os.environ['TOKEN'])