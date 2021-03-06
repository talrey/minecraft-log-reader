import re
import gzip
import glob
import os
import time

logsPath = './sample-logs/*.log.gz'
files = sorted(glob.glob(logsPath))

# this dict is for storing the number of players that joined each hour
popular_time = {'00': 0, '01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0, '07': 0, '08': 0, '09': 0, '10': 0,
                '11': 0, '12': 0, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0,
                '22': 0, '23': 0}

# stores all players that have logged on
players = []

start_time = time.time()

zombie_kills = 0
skel_kills = 0

# For storing each line in a file in a list
lines = []

def scan_file(lines,file):

    for line in lines:

        file_name = os.path.basename(file)
        date_stamp = file_name[:-7]

        # regex to look for lines where player joins server
        if re.search(r'^\[\d\d:\d\d:\d\d\] \[User Authenticator #\d{1,10}/INFO\]: UUID of player.*$', line):

            time_stamp = line[:10]

            # probably a better way to do this, but it scans through the line to find the location of the player name
            player = line[line.find('UUID') + 15:line.find(' is ')]
            if player not in players:  # if player isn't already in list
                    players.append(player)
                    hour_joined = time_stamp[1:3]
                    popular_time[hour_joined] += 1
                    # print(player.ljust(20), date_joined, time_joined)

        if re.search(' Zombie', line):
            if '<' not in line and 'true' not in line and 'Pigman' not in line:
                print(line)
                # I'm sure this is bad practice, as global vars are bad, I'll fix it later maybe
                global zombie_kills
                zombie_kills += 1
        if re.search(' Skeleton', line):
            if '<' not in line and 'Wither' not in line:
                print(line)
                global skel_kills
                skel_kills += 1

        # For writing all chat messages to a file

        # if re.search(r'^\[\d\d:\d\d:\d\d\] \[Server thread/INFO\]:.*<.*>.*$', line):
        #     time_stamp = line[:10]
        #     player_name = line[line.find('INFO]: <') + 8 : line.find('>')]
        #     message_content = line[line.find('>') + 2:]
        #     output_file = open('chat-history.txt',mode='a',encoding='utf-8')
        #     output_file.write(time_stamp)
        #     output_file.write('\t')
        #     output_file.write(player_name)
        #     output_file.write(':')
        #     output_file.write(message_content)
        #     output_file.write('\n')
        #     output_file.close()

def read_files(files):

    for file in files:
        file_size = os.path.getsize(file)
        # For storing each line in a file in a list
        lines = []
        if file_size < 500000:  # TODO change this to be less lazy, purpose is to ignore the huge files full of errors
            with gzip.open(file, 'rt', encoding='utf-8') as log_file:
                lines = list(log_file)

        scan_file(lines,file)

read_files(files)

end_time = time.time()
print('Zombie Kill Count: ', zombie_kills)
print('Skeleton Kill Count: ', skel_kills)
print('Players: ', len(players), '\nTotal time: ', end_time-start_time)
