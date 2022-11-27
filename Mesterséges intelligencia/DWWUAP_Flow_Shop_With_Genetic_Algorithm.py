import math
import time
import random
import numpy as np                              #needed for matplotlib
import matplotlib.pyplot as plt                 #needed for graphical display


def startmainprogram(machines,jobs,maxiterations,generations,arrayjobs,file_output):        #start the tests

    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()                        #plt.subplots() make the new plots for graphical display

    int_arraybest = []                          #store the best found solution for the problem

    int_bestfoundtime = float('inf')            #store the best found time for the problem
    
    int_base_of_the_array = []                          #the base array
    
    int_base_of_the_temporall_array = []                  #a temporal version of the base array(needed for copy)
    
    
    for i in range(jobs):
        int_base_of_the_array+=[i]                      #generate the base array
    int_arraybest = int_base_of_the_array.copy()

    file_output.write("Base: "+str(int_base_of_the_array)+"\n")
    print("The genetic algorithm:")
    
    for i in range(maxiterations):          #repeat the simulation for every iteration
        int_base_of_the_temporall_array,time=getnewgenetic(machines,jobs,arrayjobs,int_base_of_the_array,generations,file_output,ax)
        if int_bestfoundtime > time:            #check the new found time
            int_bestfoundtime = time            #if the time is better, we overwrite the best found time, best array, and we set a new base for further generations
            int_arraybest = int_base_of_the_temporall_array.copy()
            int_base_of_the_array=int_base_of_the_temporall_array.copy()

    
    file_output.write("Best found solution: "+str(int_arraybest)+"time: "+str(int_bestfoundtime))
    print("Best found solution: ",str(int_arraybest), "\nTime: ",int_bestfoundtime)
    time=fitness(machines,jobs,arrayjobs,int_arraybest,1,ax)       #get the time of the best found solution and generate the graphical display
    ax.set(xlim=(0, time), xticks=np.arange(0, time),                       #ax.set will configurate our plot. Xlim and Ylim will configurate where our display begins, xticks and yticks configurate the lines in our plot
       ylim=(0, machines), yticks=np.arange(0, machines+1))
    plt.show()                                                              #display the plot


def randomizejobs(machines,jobs,file_output):       #generate random jobs for the program

              #open file to write logs
    arrayjobs = [[0 for x in range(machines)] for y in range(jobs)]     #array to store the jobs
    
    for i in range(machines):               #generate random numbers to the array of jobs
        for k in range(jobs):
            arrayjobs[k][i]=random.randint(1,25)
            file_output.write(str(arrayjobs[k][i])+"\t")
        file_output.write("\n")
    return arrayjobs                        #return the array


def getnewgenetic(machines,jobs,arrayjobs,int_base_of_the_array,generations,file_output,ax):       #generate a new solution
    
    actual_data = [[0 for x in range(jobs)] for y in range(generations)]   #array to store the new generations
    time = []
    order_of_arrays = []                        #array to store the order of the generations.. will be used later

    for i in range(generations):
        for k in range(jobs):
            actual_data[i][k]=int_base_of_the_array[k]         #copy the base array to our actual_data array
        time+=[0]
        order_of_arrays+=[i]
    int_base_of_the_temporall_array = int_base_of_the_array.copy()

    for i in range(generations):            #start mutations on every single array and store it
        actual_data[i]=mutation(actual_data[i],jobs)
    for i in range(generations-1):          #start recombinations on every single array and store it
        actual_data[i]=recombination(actual_data[i],actual_data[i+1],jobs)       #parent 1 always the current array, parent 2 is always the next array
    actual_data[generations-1]=recombination(actual_data[generations-1],actual_data[0],jobs)         #in the lest recombination the parent 1 is the last array, parent 2 is the first array
    
    for i in range(generations):            #calculate every single fitness value and store it
        time[i]=fitness(machines,jobs,arrayjobs,actual_data[i],0,ax)

    
    time,order_of_arrays=sort_array(time,order_of_arrays,generations)       #sort the time array

    the_probability = 0.64
    
    random_number = random.random()
    
    for i in range(generations):            #check the survived genetic
        if i==0:
            if random_number < the_probability:     #the survived genetic is the BEST solution we can find
                file_output.write("New survived BEST generation: " + str(actual_data[order_of_arrays[i]])+ " time: " +str(time[i])+ "\n")
                return actual_data[order_of_arrays[i]],time[i]
            else:
                random_number-=the_probability
        else:
            if random_number < (pow(1-the_probability,i)*the_probability):       #the survived genetic is not the BEST souliton, but not the WORST solution
                file_output.write("New survived medium generation: " + str(actual_data[order_of_arrays[i]])+ " time: " +str(time[i])+ "\n")
                return actual_data[order_of_arrays[i]],time[i]
            else:
                random_number-=(pow(1-the_probability,i)*the_probability)


                                                #the survived genetic is the WORST solution we can find... this is very rare to happen
    file_output.write("New survived WORST generation: " + str(actual_data[order_of_arrays[generations-1]])+ " time: " +str(time[generations-1])+ "\n")
    return actual_data[order_of_arrays[generations-1]],time[generations-1]



def recombination(actual_data1,actual_data2,jobs):
    
    first_section = random.randint(0,int(jobs/2)-1)                 #get the first point of the recombination
    
    second_section = random.randint(int(jobs/2)+1,jobs-1)       #get the second point of the recombination
    
    intersection = actual_data1[first_section:second_section]                  #get the intersection of array1
    
    recombinated_array = []
    
    index = 0
    
    for i in range(jobs):
        if index >=first_section and index < second_section:            #if we are in the correct section, we put the intersection into the array
            for k in intersection:
                recombinated_array.append(k)
            index = second_section
        if actual_data2[i] not in intersection:                                #if the number in array2 is not in the intersection area, we put that number into the array
            recombinated_array.append(actual_data2[i])
            index+=1
    return recombinated_array


def mutation(actual_data,jobs):                    #mutation. we pick 2 random number and switch these numbers in our array

    x = random.randint(0,jobs-1)
    
    y = random.randint(0,jobs-1)
    
    temp=actual_data[y]
    
    actual_data[y]=actual_data[x]
    
    actual_data[x]=temp
    
    return actual_data


def fitness(machines,jobs,arrayjobs,order_of_jobs,mode,ax):    #calculate fitness. this is the solution for the flow-shop

    machine_start = [[0 for x in range(int(machines))] for y in range(int(jobs))]
    machine_end = [[0 for x in range(int(machines))] for y in range(int(jobs))]
    for i in range(jobs):
        for r in range(machines):
            if i==0:
                if r==0:
                    machine_start[order_of_jobs[i]][r]=0
                else:
                    machine_start[order_of_jobs[i]][r]=machine_end[order_of_jobs[i]][r-1]
            else:
                if r==0:
                    machine_start[order_of_jobs[i]][r]=machine_end[order_of_jobs[i-1]][r]
                else:
                    if machine_end[order_of_jobs[i]][r-1] > machine_end[order_of_jobs[i-1]][r]:
                        machine_start[order_of_jobs[i]][r]=machine_end[order_of_jobs[i]][r-1]
                    else:
                        machine_start[order_of_jobs[i]][r]=machine_end[order_of_jobs[i-1]][r]
            machine_end[order_of_jobs[i]][r]=int(machine_start[order_of_jobs[i]][r])+int(arrayjobs[order_of_jobs[i]][r])
            if mode:
                ax.bar(machine_start[order_of_jobs[i]][r], 1, width=arrayjobs[order_of_jobs[i]][r],bottom=machines-r-1, edgecolor="white", linewidth=0.7,align='edge')

    return machine_end[order_of_jobs[jobs-1]][machines-1]

def sort_array(time_base,array_base,generations):                   #just a simple array sorting

    time=time_base.copy()
    array=array_base.copy()
    for i in range(generations-1):
        for k in range(i+1,generations):
            if time[i]>time[k]:
                temp=time[i]
                time[i]=time[k]
                time[k]=temp
                temp=array[i]
                array[i]=array[k]
                array[k]=temp
    return time,array


def filereader():                               #a file reader function to read base_data_to_start

    file_input=open("base_data_to_start.txt", "r")
    
    file_input.readline()                       #read unused line from the file(to make more readable)

    machines = []
    maxiterations = []
    jobs = []
    generations = []
    seed_of_the_generation = []

    input_data=file_input.readline().split("\t")
    machines+=input_data
    
    input_data=file_input.readline().split("\t")
    maxiterations+=input_data

    input_data=file_input.readline().split("\t")
    jobs+=input_data
    
    input_data=file_input.readline().split("\t")
    generations+=input_data

    input_data=file_input.readline().split("\t")
    seed_of_the_generation+=input_data
    
    return seed_of_the_generation,machines,jobs,maxiterations,generations          #return the base_data_to_start to the main function


def main():
    
    seed_of_the_generation,machines,jobs,maxiterations,generations=filereader()

    file_output = open("logging.txt", "w")
    for i in range(len(seed_of_the_generation)):
        random.seed(int(seed_of_the_generation[i]))        #configurate the seed of the generation

        arrayjobs = [[0 for x in range(int(machines[i]))] for y in range(int(jobs[i]))]     #array to store the jobs
        arrayjobs = randomizejobs(int(machines[i]),int(jobs[i]),file_output)
    
        startmainprogram(int(machines[i]),int(jobs[i]),int(maxiterations[i]),int(generations[i]),arrayjobs,file_output)
        file_output.write("\n\n\n\n")
    file_output.close()

if __name__ == "__main__":
    main()
