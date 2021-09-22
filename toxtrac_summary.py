import os
import pandas as pd

toxtrac_results_folder = os.getcwd()

def center_counter(file, info):
    center = 0
    arena = 0
    for index,row in file.iterrows():
        if row['Pos. X (mm)'] > (arena_info[2] + 15*arena_info[6]) and row['Pos. X (mm)'] < (arena_info[2] + arena_info[4] - 15*arena_info[6]):
            if row['Pos. Y (mm)'] > (arena_info[3] + 15*arena_info[6]) and row['Pos. Y (mm)'] < (arena_info[3] + arena_info[5] - 15*arena_info[6]):
                center = center + 1
        if row['Pos. X (mm)'] > (arena_info[2]) and row['Pos. X (mm)'] < (arena_info[2] + arena_info[4]):
            if row['Pos. Y (mm)'] > (arena_info[3]) and row['Pos. Y (mm)'] < (arena_info[3] + arena_info[5]):
                arena = arena + 1
    return (center/arena),arena

def speed_filter(file, info):
    speed = []
    for index,row in file.iterrows():
        mm_speed = row['Current Speed (mm/sec)']/arena_info[6]
        mm_limit = 5*arena_info[6] # this is 5 mm/s
        if mm_speed >= mm_limit:
            speed.append(mm_speed)
    speed_average = sum(speed)/len(speed)
    frames = len(speed)
    return speed_average,frames

def exploration(file,info):
    exp_matrix = [[0]*10 for _ in range(10)]
    for index,row in file.iterrows():
        for y in range(10):
            if row['Pos. Y (mm)'] > (arena_info[3] + y*arena_info[5]/10) and row['Pos. Y (mm)'] < (arena_info[3] + (y+1)*arena_info[5]/10):
                for x in range(10):
                    if row['Pos. X (mm)'] > (arena_info[2] + x*arena_info[4]/10) and row['Pos. X (mm)'] < (arena_info[2] + (x+1)*arena_info[4]/10):
                        exp_matrix[y][x] = exp_matrix[y][x] + 1
    exp_rate = 0
    for i in range(len(exp_matrix)):
        for j in range(len(exp_matrix[i])):
            if exp_matrix[i][j] > 0:
                exp_rate = exp_rate + 1    
    return exp_matrix,exp_rate


result_file = ['\t'.join(['video', 'date', 'individual', 'visible', 'center_freq',
            'exp_rate', 'mob_speed', 'mob_rate'])]
print(result_file)

subfolders = [ f.path for f in os.scandir(toxtrac_results_folder) if f.is_dir() ]
for s in subfolders:
    print(s)
    name = os.path.basename(s)
    individuals = ''.join(s + '\\' + name + '_ArenaNames.txt')
    individuals = open(individuals, 'r')
    individuals = individuals.readlines()[1:]
    arena = ''.join(s + '\\' + name + '_Arena.txt')
    arena = open(arena, 'r')
    arena = arena.readlines()[1:]
    for i,a,t in zip(individuals,arena,range(len(individuals))):
        arena_info = [name,i[:-1]]
        a = a[:-1].split('\t')
        a = [float(x) for x in a]
        px_mm = (a[2] + a[3])/(2*100)
        a.append(px_mm)
        arena_info.extend(a)
        track_file = ''.join(s + '\\' + name + '\\' + 'Tracking_RealSpace_' + str(t+1) + '.txt')
        track_file = pd.read_csv(track_file, delimiter = "\t")
        [center,visible_frames] = center_counter(track_file, arena_info)
        visible_frames = visible_frames/track_file.shape[0]
        [exploration_matrix,exploration_rate] = exploration(track_file, arena_info)
        speed_file = ''.join(s + '\\' + name + '\\' + 'Instant_Speed_' + str(t+1) + '.txt')
        speed_file = pd.read_csv(speed_file, delimiter = "\t")
        speed_frames = speed_file.shape[0] 
        [mob_speed,mob_frames] = speed_filter(speed_file, arena_info)
        result_line = [name, name[:name.index('_')], i[:-1], str(visible_frames), str(center),
                       str(exploration_rate), str(mob_speed), str(mob_frames/speed_frames)]
        result_line = ['\t'.join(result_line)]
        result_file.append(result_line)
        print(result_line)

with open('toxtrac_summary_results.txt', 'w') as f:
    f.write('\n'.join(result_file))
f.close()

