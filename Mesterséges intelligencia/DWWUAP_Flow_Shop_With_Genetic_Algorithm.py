import math
import time
import random
import numpy as np                              #needed for matplotlib
import matplotlib.pyplot as plt                 #needed for graphical display
plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()                        #plt.subplots() make the new plots for graphical display


def startmainprogram(int_machines,int_jobs,int_maxiterations,int_generations,int_arrayjobs):        #start the tests

    global ax                                   #needed for the graphical display

    int_arraybest = []                          #store the best found solution for the problem

    int_bestfoundtime = float('inf')            #store the best found time for the problem
    
    int_base_of_the_array = []                          #the base array
    
    int_base_of_the_temporall_array = []                  #a temporal version of the base array(needed for copy)
    
    
    for i in range(int_jobs):
        int_base_of_the_array+=[i]                      #generate the base array
    int_arraybest = int_base_of_the_array.copy()

    file_output = open("logging.txt", "a")
    file_output.write("Base: "+str(int_base_of_the_array)+"\n")
    print("The genetic algorithm:")
    
    for i in range(int_maxiterations):          #repeat the simulation for every iteration
        int_base_of_the_temporall_array,time=getnewgenetic(int_machines,int_jobs,int_arrayjobs,int_base_of_the_array,int_generations,file_output)
        if int_bestfoundtime > time:            #check the new found time
            int_bestfoundtime = time            #if the time is better, we overwrite the best found time, best array, and we set a new base for further generations
            int_arraybest = int_base_of_the_temporall_array.copy()
            int_base_of_the_array=int_base_of_the_temporall_array.copy()

    
    file_output.write("Best found solution: "+str(int_arraybest)+"time: "+str(int_bestfoundtime))
    print("Best found solution: ",str(int_arraybest), "\nTime: ",int_bestfoundtime)
    file_output.close()
    time=fitness(int_machines,int_jobs,int_arrayjobs,int_arraybest,1)       #get the time of the best found solution and generate the graphical display
    ax.set(xlim=(0, time), xticks=np.arange(0, time),                       #ax.set will configurate our plot. Xlim and Ylim will configurate where our display begins, xticks and yticks configurate the lines in our plot
       ylim=(0, int_machines), yticks=np.arange(0, int_machines+1))
    plt.show()                                                              #display the plot


def randomizejobs(int_machines,int_jobs):       #generate random jobs for the program

    file_output = open("logging.txt", "w")          #open file to write logs
    
    int_arrayjobs = [[0 for x in range(int_machines)] for y in range(int_jobs)]     #array to store the jobs
    
    for i in range(int_machines):               #generate random numbers to the array of jobs
        for k in range(int_jobs):
            int_arrayjobs[k][i]=random.randint(1,25)
            file_output.write(str(int_arrayjobs[k][i])+"\t")
        file_output.write("\n")
    file_output.close()
    return int_arrayjobs                        #return the array


def getnewgenetic(int_machines,int_jobs,int_arrayjobs,int_base_of_the_array,int_generations,file_output):       #generate a new solution
    
    actual_data = [[0 for x in range(int_jobs)] for y in range(int_generations)]   #array to store the new generations
    time = []
    order_of_arrays = []                        #array to store the order of the generations.. will be used later

    for i in range(int_generations):
        for k in range(int_jobs):
            actual_data[i][k]=int_base_of_the_array[k]         #copy the base array to our actual_data array
        time+=[0]
        order_of_arrays+=[i]
    int_base_of_the_temporall_array = int_base_of_the_array.copy()

    for i in range(int_generations):            #start mutations on every single array and store it
        actual_data[i]=mutation(actual_data[i],int_jobs)
    for i in range(int_generations-1):          #start recombinations on every single array and store it
        actual_data[i]=recombination(actual_data[i],actual_data[i+1],int_jobs)       #parent 1 always the current array, parent 2 is always the next array
    actual_data[int_generations-1]=recombination(actual_data[int_generations-1],actual_data[0],int_jobs)         #in the lest recombination the parent 1 is the last array, parent 2 is the first array
    
    for i in range(int_generations):            #calculate every single fitness value and store it
        time[i]=fitness(int_machines,int_jobs,int_arrayjobs,actual_data[i],0)

    
    time,order_of_arrays=sort_array(time,order_of_arrays,int_generations)       #sort the time array

    the_probability = 0.64
    
    random_number = random.random()
    
    for i in range(int_generations):            #check the survived genetic
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
    file_output.write("New survived WORST generation: " + str(actual_data[order_of_arrays[int_generations-1]])+ " time: " +str(time[int_generations-1])+ "\n")
    return actual_data[order_of_arrays[int_generations-1]],time[int_generations-1]



def recombination(actual_data1,actual_data2,int_jobs):
    
    first_section = random.randint(0,int(int_jobs/2)-1)                 #get the first point of the recombination
    
    second_section = random.randint(int(int_jobs/2)+1,int_jobs-1)       #get the second point of the recombination
    
    intersection = actual_data1[first_section:second_section]                  #get the intersection of array1
    
    recombinated_array = []
    
    index = 0
    
    for i in range(int_jobs):
        if index >=first_section and index < second_section:            #if we are in the correct section, we put the intersection into the array
            for k in intersection:
                recombinated_array.append(k)
            index = second_section
        if actual_data2[i] not in intersection:                                #if the number in array2 is not in the intersection area, we put that number into the array
            recombinated_array.append(actual_data2[i])
            index+=1
    return recombinated_array


def mutation(actual_data,int_jobs):                    #mutation. we pick 2 random number and switch these numbers in our array

    x = random.randint(0,int_jobs-1)
    
    y = random.randint(0,int_jobs-1)
    
    temp=actual_data[y]
    
    actual_data[y]=actual_data[x]
    
    actual_data[x]=temp
    
    return actual_data


def fitness(int_machines,int_jobs,int_arrayjobs,order_of_jobs,mode):    #calculate fitness. this is the solution for the flow-shop

    if mode==1:
        global ax
    int_arraycurrentworkingleft = [-1 for x in range(int_machines)]     #array to store the remaining work pet machine
    int_arrayalreadydonejobs = [0 for x in range(int_machines)]         #array to store the jobs already done
    for i in range(int_machines):
        int_arraycurrentworkingleft[i]=int_arrayjobs[order_of_jobs[0]][i]

    
    time = -1
    
    while int_arrayalreadydonejobs[int_machines-1]!=int_jobs:
        time+=1
        for i in range(int_machines):
            if int_arraycurrentworkingleft[i]!=0:                       #if the current machine still have job to do, then we decrease the current work
                if i!=0:                                                #we need to separate the first machine and the other machines
                    if int_arrayalreadydonejobs[i]<int_arrayalreadydonejobs[i-1]:
                        int_arraycurrentworkingleft[i]-=1               #if the machine above the current machine is done with the current work, we decrease the value
                else:
                    int_arraycurrentworkingleft[i]-=1                   #if it's the first machine, we don't need to check anything
            else:
                int_arrayalreadydonejobs[i]+=1                          #if the work is done, we increase the already done array's value
                if int_jobs<=int_arrayalreadydonejobs[i]:               #just in case we have too much jobs, we can't go into infinity
                    int_arraycurrentworkingleft[i]=-1
                    int_arrayalreadydonejobs[i]=int_jobs
                else:
                    int_arraycurrentworkingleft[i]=int_arrayjobs[order_of_jobs[int_arrayalreadydonejobs[i]]][i]         #set the next job
                    if i!=0:
                        if int_arrayalreadydonejobs[i-1]>int_arrayalreadydonejobs[i]:                                   #if the machine above the current machine is done with the current work, we decrease the value
                            int_arraycurrentworkingleft[i]-=1
                    else:
                        int_arraycurrentworkingleft[i]-=1                                                               #if it's the first machine, we don't need to check anything
                if mode==1:                                             #just for graphical display
                    ax.bar(time-int_arrayjobs[order_of_jobs[int_arrayalreadydonejobs[i]-1]][i], 1, width=int_arrayjobs[order_of_jobs[int_arrayalreadydonejobs[i]-1]][i],bottom=int_machines-i-1, edgecolor="white", linewidth=2,align='edge',color="red")
    
    return time

def sort_array(time_base,array_base,int_generations):                   #just a simple array sorting

    time=time_base.copy()
    array=array_base.copy()
    for i in range(int_generations-1):
        for k in range(i+1,int_generations):
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
    int_machines = int(file_input.readline())
    
    int_maxiterations = int(file_input.readline())
    
    int_jobs = int(file_input.readline())
    
    int_generations = int(file_input.readline())
                      
    int_seed_of_the_generation=int(file_input.readline())      
    
    return int_seed_of_the_generation,int_machines,int_jobs,int_maxiterations,int_generations          #return the base_data_to_start to the main function


def main():
    
    int_seed_of_the_generation,int_machines,int_jobs,int_maxiterations,int_generations=filereader()
    
    random.seed(int_seed_of_the_generation)        #configurate the seed of the generation

    int_arrayjobs = [[0 for x in range(int_machines)] for y in range(int_jobs)]     #array to store the jobs
    int_arrayjobs = randomizejobs(int_machines,int_jobs)
    
    startmainprogram(int_machines,int_jobs,int_maxiterations,int_generations,int_arrayjobs)


if __name__ == "__main__":
    main()
