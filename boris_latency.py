import os


### DEFINITIONS

def evaluated_time(arena_file):
    food_list = []
    for line in arena_file[16:]:
        line = line.split('\t')
        #print(line)
        time = line[0]
        file_total = float(line[2])
        behavior = line[5]
        if behavior == 'food':
            food_list.append(time)
    start = float(food_list[0])
    end = round((start + (30*60)), 3)
    if end > file_total:
        delta = round((end - file_total)/60)+1
        end = round((start + (30*60) - (delta*60)),3)
    total_evaluated = round((end - start)/60)
    return [arena,start,end,total_evaluated]

def latency_to_behavior(behavior, arena_file, start):
    behavior_list = []
    for line in arena_file[16:]:
        line = line.split('\t')
        time = line[0]
        behav = line[5]
        if behav == behavior:
            behavior_list.append(time)
    if len(behavior_list) == 0:
        latency = 'NA'
    elif len(behavior_list) > 0:
        latency = round((float(behavior_list[0]) - start),3)
    return latency


### START HERE

events_dir = os.getcwd()

latency_file = open("latency05.csv", 'w')

latency_file.write('arena\tindividual\ttreatment\tweek\tgroup\tstart\tend\ttotal\tsmelling\tnear\ttesting\teating\tbreathing\tmoving\tturning\n')

for filename in os.listdir(events_dir):
    if filename.endswith(".tsv"): 
        arena = filename[:6]
        print(arena)
        if arena[0] == 'C':
            treatment = "control"
        elif arena[0] == 'D':
            treatment = "dhq"
        week = arena[4:]
        group = arena[1:4]
        individual = arena[:4]
        arena_file = open(os.path.join(events_dir, filename), 'r')
        arena_file = arena_file.readlines()
        total_list = evaluated_time(arena_file)
        start = total_list[1]
        end = str(total_list[2])
        total = str(total_list[3])
        latencies = []
        for b in ['smelling', 'near', 'testing', 'eating', 'breathing', 'moving', 'turning']:
            latencies.append(str(latency_to_behavior(b, arena_file, start)))
#        print(latencies)
        latencies = '\t'.join(latencies)
        latency_file.write(arena+'\t'+individual+'\t'+treatment+'\t'+week+'\t'+group+'\t'+str(start)+'\t'+end+'\t'+total+'\t'+latencies+'\n')
latency_file.close()
