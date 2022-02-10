import comedian
import demographic
import ReaderWriter
import timetable
import random
import math

class Scheduler:

	def __init__(self,comedian_List, demographic_List):
		self.comedian_List = comedian_List
		self.demographic_List = demographic_List
		self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

	#Using the comedian_List and demographic_List, create a timetable of 5 slots for each of the 5 work days of the week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, comedian_Obj, demographic_Obj, "main")
	#This line will set the session slot '1' on Monday to a main show with comedian_obj, which is being marketed to demographic_obj. 
	#Note here that the comedian and demographic are represented by objects, not strings. 
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in tasks 2 and 3. 
	#Comedian (3rd argument) and Demographic (4th argument) can be assigned any value, but if the comedian or demographic are not in the original lists, 
	#	your solution will be marked incorrectly. 
	#The final, 5th argument, is the show type. For task 1, all shows should be "main". For task 2 and 3, you should assign either "main" or "test" as the show type.
	#In tasks 2 and 3, all shows will either be a 'main' show or a 'test' show
	
	#demographic_List is a list of Demographic objects. A Demographic object, 'd' has the following attributes:
	# d.reference  - the reference code of the demographic
	# d.topics - a list of strings, describing the topics that the demographic like to see in their comedy shows e.g. ["Politics", "Family"]

	#comedian_List is a list of Comedian objects. A Comedian object, 'c', has the following attributes:
	# c.name - the name of the Comedian
	# c.themes - a list of strings, describing the themes that the comedian uses in their comedy shows e.g. ["Politics", "Family"]

	#For Task 1:
	#Keep in mind that a comedian can only have their show marketed to a demographic 
		#if the comedian's themes contain every topic the demographic likes to see in their comedy shows.
	#Furthermore, a comedian can only perform one main show a day, and a maximum of two main shows over the course of the week.
	#There will always be 25 demographics, one for each slot in the week, but the number of comedians will vary.
	#In some problems, demographics will have 2 topics and in others, 3.
	#A comedian will have between 3-8 different themes. 

	#For Task 2 and 3:
	#A comedian can only have their test show marketed to a demographic if the comedian's themes contain at least one topic
		#that the demographic likes to see in their comedy shows.
	#Comedians can only manage a 4 hours of stage time, where main shows 2 hours and test shows are 1 hour.
	#A Comedian can not be on stage for more than 2 hours a day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need. 
	#Furthermore, you should not import anything else beyond what has been imported above. 
	#To reiterate, the five calls are timetableObj.addSession, d.name, d.genres, c.name, c.talents

	#This method should return a timetable object with a schedule that is legal according to all constraints of task 1.

	#TASK 1
	#We use a backtracking algorithm to find a valid schedule for comedians
	#First use arc consistency algorithm to remove comedians we know can't be part of solution as they violate unary constraints
	#Then take valid comedians for demographics and we try adding the pair to an assignment as long as no constraints are broken. As there are so many possibilties at each call for valid comedians
	#we use MRV or fail-first to ensure if there is no solution we take the path that most likely to show there isn't a solution 
	#then when choosing which comedian to choose for a demographics we use LCV heuristic which chooses the comedian that appears least in other demographics which haven't been put in assignment
	#If the assignment fails constraints we backtrack to where there isn't an error and try a new combination
	#We then use a greedy algorithm to assign assignment into a valid schedule following constraints on num of hours(2) comedian can perform in one day
	def createSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(1)
		
		#Here is where you schedule your timetable
		#unary constraint checked first

		domains = self.arcConsistency(1)#This will give domain of only valid comedians for the demographics
		
		assignment= self.backtrackingSearch(domains, 1)#Calls backtracking algorithm choice 1

		#all we gotta do now is another csp where we assign to correct days of schedule
		schedule= self.mainShowSchedule(assignment, timetableObj)#Places assignment into a valid schedule
		
		#Do not change this line
		return timetableObj

	#Now, we have introduced test shows. Each day now has ten sessions, and we want to market one main show and one test show to each demographic. 
	#All slots must be either a main or a test show, and each show requires a comedian and a demographic. 
	#A comedian can have their test show marketed to a demographic if the comedian's themes include at least one topic the demographic likes.
	#We are now concerned with stage hours. A comedian can be on stage for a maximum of four hours a week.
	#Main shows are 2 hours, test shows are 1 hour.
	#A comedian can not be on stage for more than 2 hours a day.
	
	#TASK 2
	#First use arc consistency algorithm to remove comedians we know can't be part of solution as they violate unary constraints
	#Then take valid comedians for demographics and we try adding the pair to an assignment as long as no constraints are broken. As there are so many possibilties at each call for valid comedians
	#we use MRV/fail-first to ensure if there is no solution we take the path that most likely to show there isn't a solution one where domain length 0
	#then when choosing which comedian to choose for a demographics we use LCV heuristic which chooses the comedian that appears least in other demographics which haven't been put in assignment
	#If the assignment fails constraints we backtrack to where there isn't an error and try a new combination
	#We then use a greedy algorithm to assign assignment into a valid schedule following constraints on num of hours(2) comedian can perform in one day
	def createTestShowSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)

		#Here is where you schedule your timetable
		domains = self.arcConsistency(2)#This will give domain of only valid comedians for the demographics(both test and main)
				
		assignment=self.backtrackingSearch(domains, 2)#Calls backtracking algorithm choice 2
		self.mainAndTestShowSchedule(assignment, timetableObj)#Places assignment into a valid schedule

		#Do not change this line
		return timetableObj

	#It costs £500 to hire a comedian for a single main show.
	#If we hire a comedian for a second show, it only costs £300. (meaning 2 shows cost £800 compared to £1000)
	#If those two shows are run on consecutive days, the second show only costs £100. (meaning 2 shows cost £600 compared to £1000)

	#It costs £250 to hire a comedian for a test show, and then £50 less for each extra test show (£200, £150 and £100)
	#If a test shows occur on the same day as anything else a comedian is in, then its cost is halved. 

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible. 
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here. 
	#TASK 3
	#I have chosen to use a genetic algorithm to get a solution with lowest possible cost as well as sorting the solution after to lower costs if possible
	#Done this as a GA will be able to perform well in general for any set of comedians and demographics while backtracking i can only tell how well it performs on 8 problems given
	#Sorting algorithm will not lower cost too much in case where cost is already very optimal. More useful for when cost is above average and will lower cost by a lot more to help lower the average cost
	#Could have used sorting algorithm with my backtracking algorithm using a new heuristic instead of LCV to try and get maximum amount of comedians appearing more than once such as MCV so comedians likely to have 4 shows
	#First we generate numOfParents individuals which randomly assigns a (comedian,demographic,showtype) to a random slot but we use arc consistency algorithm to make sure comedian chosen for demographic is valid
	#Evaluate fitness for all individuals and sort according to fittest individual and select top numBestSelected
	#Then begin crossover of individuals to get the best parts of both schedules and hopefully get children with higher fitness than their parents
	#We then mutate each individual where we randomly choose a slot and rechoose a valid comedian for that demo and show
	#After doing this for 500 generations we then sort the best schedule
	#We find the indexes of comedians that have more than one show as these affect costs
	#We then sort schedules test shows to lower cost and after the main shows
	#Then we add this new best schedule to the timetable
	#Problem x- MinCostDiscoveredSoFar    AverageCost   HighestCost  (8 trials)
	#1          10500                     10950         11550
	#2          10750                     12400         14200
	#3          10250                     10700         11450
	#4          10350                     10650         11250
	#5          10275                     10600         11050
	#6          10300                     10625         10950
	#7          10150                     10450         10900
	#8          10200                     10500         10950
	def createMinCostSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(3)
		#alter to tune for best delivery of results      
		numOfParents=5000
		numBestSelected=200
		numOffspring=300
		numMutations=1
		#From testing found increasing numMutations to be anything more than 1 increases cost by 2k but unlikely to find good solution at 0
		#Found reducing numBestSelected does not increase cost by that much as those at top more likely to get better solution anyway
		#Really depends on random generation of parents if it is close to a valid schedule at beginning way more likely to get lower cost as more time to optimise cost
		typesOfShow=["main","test"]

		#Here is where you schedule your timetable
		domains = self.arcConsistency(3)
		#so randomly choose number of com and dem in slots number of individual determined by numOffParents
		parentGen= self.createParentGen(numOfParents, domains)
		print("Processing: \t Will take approximately 30 seconds")
		genNum=500
		#Run genetic algorithm for 500 generations
		for i in range(genNum):
			parentGen=self.selectBest(parentGen, numBestSelected=200)#Sort and select the first numBestSelected individuals as these have lowest cost
			parentGen=self.crossover(parentGen, numOffspring) #Takes generation and creates offspring by trying to get best bits from parents and combining them to get better solution
			parentGen=self.mutation(parentGen, numMutations, domains)#Randomly mutate element for each individual
		bestChild=self.selectBest(parentGen, numBestSelected=1)[0]#Select the best individual after all generations
		comedians=[]
		for dayNumber, day in enumerate(self.days):
		 	for timeslot in range(1, 11):
				 comedians.append(bestChild[day][timeslot][0])
		duplicates=self.findDuplicatesIndex(comedians)#take comedians with size 2,3,4 of duplicates
		newChild=self.selectBest([bestChild,self.testSort(duplicates, bestChild)], numBestSelected=1)[0]#We then sort the test shows and see if this reduces cost if it does we choose this timetable
		newChild=self.selectBest([newChild,self.mainSort(duplicates, newChild)], numBestSelected=1)[0]#We then sort the main shows and see if this reduces cost if it does we choose this timetable
		#Add this to timetableObj
		for dayNumber, day in enumerate(self.days):
				for timeslot in range(1, 11):
					timetableObj.addSession(day, timeslot, self.comedian_List[newChild[day][timeslot][0]], self.demographic_List[newChild[day][timeslot][1]], typesOfShow[newChild[day][timeslot][2]])
		#Do not change this line
		return timetableObj
	#We just go through blocks and find one that meets conditions in func and we add numAdded items from step to the block in the None slots
	def insertToBlocks(self, testBlocks, step, func, numAdded):
		for block in testBlocks:
			try:
				firstNone=block.index(None)
			except:
				firstNone=len(block)
			if func(step, firstNone, block):
				for i in range(numAdded):
					block[firstNone+i]=step.pop(0)
		return testBlocks
	# We go through block given in blocks and we check if func condition met and if this is true we then swap from toBeSwapped block and and block where condition met
	# We swap numSwapped elements E.g. say blocks=[12,14,20,23] and toBeSwapped=[30,31,None,None] we know we're trying to place pair of step 3(37,35) as it cant be placed in toBeSwapped
	# Say condition is met and numSwapped=2 we then set blocks=[12,14,37,35] and toBeSwapped=[30,31,20,23] which are now valid
	def swapBlocks(self, blocks, step, toBeSwapped, loc, func, numSwapped):
		for block in blocks:
			try:
				firstNone=block.index(None)
			except:
				firstNone=len(block)
			if func(step, firstNone, block, toBeSwapped):
				for i in range(numSwapped):
					toBeSwapped[loc+i]=block[len(block)-1-i]
					block[len(block)-1-i]=step.pop(0)
		return blocks
	# This takes oldBlocks and newBlocks which contain index relating to slot e.g. index=19 means day 1(tuesday) slot 10 
	# We take an empty schedule and we get the slots that are unchanged i.e the ones not contained in the blocks and we place them in same slot
	# Now we take index from oldBlock and get what is contained in that slot and place in newIndex of new schedule do this for all indexes in oldBlock
	def newTimetable(self, oldTimetable, oldBlocks, newBlocks):
		unchanged=[i for i in range(50)]
		oldBlocks1D=[j for sub in oldBlocks for j in sub]
		unchanged=list(set(unchanged)-set(oldBlocks1D))
		newTim={"Monday" : {}, "Tuesday" : {}, "Wednesday" : {}, "Thursday" : {}, "Friday" : {}}
		for slot in unchanged:
			digits=self.getDigits(slot)
			newTim[self.days[digits[0]]][digits[1]+1]=oldTimetable[self.days[digits[0]]][digits[1]+1]
		for i, block in enumerate(oldBlocks):
			for j, slot in enumerate(block):
				newIndex=newBlocks[i][j]
				newTim[self.days[self.getDigits(newIndex)[0]]][self.getDigits(newIndex)[1]+1]=oldTimetable[self.days[self.getDigits(slot)[0]]][self.getDigits(slot)[1]+1]			
		return newTim
	# Similiar to testSort where we place them in blocks using their steps to get closer to optimal cost
	# Next we get indexes of comedians(individuals) that only do one show and blocks where the block isn't ideal I.e. the difference in step isn't 1 which means less discount
	# If we can use index from individuals and swap with something in blocks to get block with step difference of 1 we do this as index of individuals can't violate any constraints
	# Then just replace oldChild schedule with new sorted timetable for main shows and return this
	def mainSort(self, duplicates, oldChild):
		worklist=[[] for i in range(len(self.days))]
		mainSteps=[[] for i in range(len(self.days))]
		duplicatesOneList=[]
		mainDups=[]
		for dup in duplicates:
			if len(dup)==2 and all(oldChild[self.days[self.getDigits(ind)[0]]][self.getDigits(ind)[1]+1][2]==0 for ind in dup) and abs(math.floor(dup[0]/10)-math.floor(dup[1]/10))!=1:
				mainDups.append(dup)
				for comInd in dup:
					mainSteps[math.floor(comInd/10)].append(comInd)
			duplicatesOneList.extend(dup)
		newMainBlocks=[[None for i in range(len(mainDups[j]))] for j in range(len(mainDups))]
		getMainBlock= lambda step, firstNone, block: len(step)>0 and block[len(block)-1]==None and not any(step[0]//10==ind//10 for ind in block[:firstNone])
		for step in mainSteps:
			newMainBlocks=self.insertToBlocks(newMainBlocks, step, getMainBlock, 1)
		for step in mainSteps:
			if len(step)!=0:
				for block in newMainBlocks:
					try:
						firstNone=block.index(None)
					except:
						firstNone=len(block)
					if firstNone==len(block)-1:
						getValidBlock=lambda step, firstNone, block, toBeSwapped:len(step)>0 and not any(toBeSwapped[0]//10==ind//10 for ind in block[:firstNone])
						newMainBlocks=self.swapBlocks(newMainBlocks, step, block, firstNone, getValidBlock, 1)
		for block in newMainBlocks:
			worklist[math.floor(block[0]/10)].append(block)
			worklist[math.floor(block[1]/10)].append(block)
		individuals=[i for i in range(len(self.demographic_List)*2)]
		individuals=list(set(individuals)-set(duplicatesOneList))
		mainDups.extend([[x] for x in individuals])
		temp=[]
		newmainDups=[]
		while temp!=individuals:#if individuals doesn't change
			temp=individuals.copy()
			for individual in individuals:
				x=math.floor(individual/10)-1
				if x==-1:
					x=1
					y=1
				elif x==3:
					y=3
				else:
					y=x+2
				if len(worklist[x])>0 or len(worklist[y])>0:
					swapped=False
					individuals.remove(individual)
					for dups in worklist[x]:
						for dup in dups:
							if dup//10!=x:#the one thats not 1 away from individual swap and append new individual and break from loop cause ur done
								individuals.append(dup)
								z=dups.index(dup)
								newmainDups.append([individual,dups[z-1]])
								newMainBlocks[newMainBlocks.index(dups)]=[individual,dups[z-1]]
								worklist[x].remove(dups)
								worklist[dup//10].remove(dups)
								swapped=True
								break
						if swapped:
							break
					if not swapped:
						for dups in worklist[y]:
							for dup in dups:
								if dup//10!=y:#the one thats not 1 away from individual swap and append new individual and break from loop cause ur done
									individuals.append(dup)
									z=dups.index(dup)
									newmainDups.append([individual,dups[z-1]])
									newMainBlocks[newMainBlocks.index(dups)]=[individual,dups[z-1]]
									worklist[y].remove(dups)
									worklist[dup//10].remove(dups)
									swapped=True
									break
							if swapped:
								break
		newMainBlocks.extend([[x] for x in individuals])
		newChild=self.newTimetable(oldChild, mainDups, newMainBlocks)
		return newChild
	# Get blocks which are just list of list of indexes with same comedians only doing test shows
	# Sort them by length of lists and create an empty clone of it
	# Do this as most important to get cheapest blocks of size 4 first then 3 then 2 as we can get extra discount for 4 blocks
	# Steps get indexes and place them in their step according to 0-9 go to step[0] and 10-19 step[1] ...
	# We then get all possible pairs that reduce costs when placed in same block(goodStepsPairs) and find number of pairs(numPairs) possible for each pair
	# Now we must get 2 pairs that don't share a step and add numPairs of them together andwe choose the 2 pairs with highest number as this most likely to give best cost
	# So we place in order from above into blocks where we place pair from step chosen in block iff there isn't already 2 from same step in there otherwise place in next empty block
	# Next is case where pair1 can't be placed in blocks due to conditions so we must swap pair2 in other block with it which is valid and pair1 valid in oldblock
	# Ideal swap for pair1(say step=2) is a block with pair2,pair3(pair2 step=1 pair3 step=3) as we can swap pair2 with it so we would have block [pair1,pair3] which is ideal block and [pair that blocked pair1,pair2] also ideal
	# Otherwise just swap with somethig valid from a block of len 2 as this easiest
	# Now must place leftover in steps which will all be of len 1 as we have placed all pairs in blocks
	# Add in same way as pairs and do swapping if necessary
	# Then we get oldChild and use the old blocks we got and compare to new sorted blocks and swap them for that schedule to get new sorted timetable for testshows
	def testSort(self, duplicates, oldChild):
		blocks=[]
		steps=[[] for i in range(5)]
		for dup in duplicates:
			if all(oldChild[self.days[self.getDigits(ind)[0]]][self.getDigits(ind)[1]+1][2]==1 for ind in dup):#if a block is only test shows
				blocks.append(dup)
				for comInd in dup:
					steps[math.floor(comInd/10)].append(comInd)
		blocks.sort(key=len, reverse=True)
		newTestBlocks=[[None for i in range(len(blocks[j]))] for j in range(len(blocks))]
		goodStepsPairs=[[0,1],[1,2],[2,3],[3,4]]
		numPairs=[]
		for stepPair in goodStepsPairs:
			numIndividuals=min(steps[stepPair[0]:stepPair[1]+1],key=len)
			numPairs.append(len(numIndividuals)//2)
		totalPairsPossible=[]
		bestPair=[]
		for ind,stepPair in enumerate(goodStepsPairs):
			temp=numPairs.copy()
			tempStep=goodStepsPairs.copy()
			indexes=[]
			if ind!=0:
				indexes.append(ind-1)
			indexes.extend((ind,ind+1))
			temp=[i for j, i in enumerate(temp) if j not in indexes]
			tempStep=[i for j, i in enumerate(tempStep) if j not in indexes]
			maxNumPairs=max(temp)
			totalPairsPossible.append(numPairs[ind]+maxNumPairs)
			bestPair.append(tempStep[temp.index(maxNumPairs)])
		goodStepsPairs=[i for _,i in sorted(zip(totalPairsPossible,goodStepsPairs), key=lambda x: x[0], reverse=True)]
		bestPair=[i for _,i in sorted(zip(totalPairsPossible,bestPair), key=lambda x: x[0], reverse=True)]
		stepPair=goodStepsPairs[0]
		stepPair.extend(bestPair[0])
		stepPair.extend(list(set([i for i in range(len(goodStepsPairs)+1)])-set(stepPair)))
		getFreeBlocks =lambda step, firstNone, block:len(step)>1 and block[len(block)-2]==None and not any(step[0]//10==ind//10 for ind in block[:firstNone])
		for step in stepPair:
			step=steps[step]
			newTestBlocks=self.insertToBlocks(newTestBlocks, step, getFreeBlocks, 2)
		for step in steps:
			if len(step)==2:
				for block in newTestBlocks:
					try:
						firstNone=block.index(None)
					except:
						firstNone=len(block)
					if firstNone==len(block)-2:#there is pair none in block
						#look for block that contains step-1,step+1
						#if not just swap with something valid in 2 block
						getGoodBlock=lambda step, firstNone, block, toBeSwapped: len(step)>1 and len(block)==4 and (toBeSwapped[0]//10)-1==block[0]//10 and (toBeSwapped[0]//10)+1==block[2]//10
						newTestBlocks =self.swapBlocks(newTestBlocks, step, block, firstNone, getGoodBlock, 2)
						get2Block=lambda step, firstNone, block, toBeSwapped:len(step)>1 and len(block)==2 and not any(toBeSwapped[0]//10==ind//10 for ind in block[:firstNone])
						newTestBlocks = self.swapBlocks(newTestBlocks, step, block, firstNone, get2Block, 2)
		getBlockOneStep = lambda step, firstNone, block: len(step)!=0 and firstNone!=len(block) and not any(step[0]//10==ind//10 for ind in block[:firstNone]) and any((step[0]//10)-1==ind//10 for ind in block[:firstNone])
		getAvaBlock = lambda step, firstNone, block: len(step)!=0 and firstNone!=len(block) and not any(step[0]//10==ind//10 for ind in block[:firstNone])
		for step in steps:
			if len(step)&1:
				newTestBlocks=self.insertToBlocks(newTestBlocks, step, getBlockOneStep, 1)
		for step in steps:
			if len(step)&1:
				newTestBlocks=self.insertToBlocks(newTestBlocks, step, getAvaBlock, 1)
		for step in steps:
			if len(step)&1:
				for block in newTestBlocks:
					try:
						firstNone=block.index(None)
					except:
						firstNone=len(block)
					if firstNone!=len(block):
						getBlock=lambda step, firstNone, block, toBeSwapped: len(step)!=0 and len(block)==2 and not any(toBeSwapped[0]//10==ind//10 for ind in block[:firstNone])
						newTestBlocks=self.swapBlocks(newTestBlocks, step, block, firstNone, getBlock, 1)
		return self.newTimetable(oldChild, blocks, newTestBlocks)

	# Creates a domain for all demographics
	# For choice 1 domains[0] corresponds to list of comedians valid for demographic[0]
	# For choice 2 domains[0][0] corresponds to list of comedians valid for demo[0] main show domains[0][1] is test shows for demo[0]
	# Comedian valid for demographic(main show) if topics of demograhic is a subset of all comedian themes
	# Comedian valid for demographic(test show) if topics of demographic contains at least one of comedian themes
	def arcConsistency(self, choice):
		if choice==1:
			domains = [[] for i in range(len(self.demographic_List))]
			for demographicCounter, demographic in enumerate(self.demographic_List):
				for comedianCounter, comedian in enumerate(self.comedian_List):
					if (set(demographic.topics).issubset(comedian.themes)):
						domains[demographicCounter].append(comedianCounter)
		else:
			domains = [[[],[]] for i in range(len(self.demographic_List))]
			for demographicCounter, demographic in enumerate(self.demographic_List):
				for comedianCounter, comedian in enumerate(self.comedian_List):
					if (set(demographic.topics).issubset(comedian.themes)):
						domains[demographicCounter][0].append(comedianCounter)
					if(not (set(demographic.topics).isdisjoint(comedian.themes))):
						domains[demographicCounter][1].append(comedianCounter)
		return domains
					
	# Switch case for which backtracking we choose depending on choice
	def backtrackingSearch(self, domains, choice):
		choices={1: self.recursiveBacktrackingOp1,
				 2: self.recursiveBacktrackingOp2,}
		return choices[choice]([],domains, choice)
	# Backtracking algorithm with stopping condition of the assignment being full(I.e length of assignment same as num of demographics*2 as this accounts for each demo having one main and one test show)
	# First we choose variable(demographic with smallest number of comedians that are valid for it) -fail first
	# Then we choose comedian from this set that is least constraining I.e. comedian with least appearances in other demographics valid comedians as least liekly to cause failure
	# Add this to assignment and call backtrack only if by adding we don't break constraint
	# If the assignment is invalid we just remove what we previously added
	def recursiveBacktrackingOp1(self, assignment, domains, choice):
		if len(assignment)==len(self.demographic_List):
			return assignment
		selectedVariable=self.selectUnassignedVariable(assignment, domains, choice)
		var=domains[selectedVariable]
		for value in self.orderDomainValues(var, assignment, domains, choice):
			comedians=[]
			for demCom in assignment:
				comedians.append(demCom[1])
			if comedians.count(value)<2:#check value consistent with those already in assignment(check that comedian has appeared max once assignment)
				#add demographic and comedian to assignment
				assignment.append([selectedVariable, value])
				result=self.recursiveBacktrackingOp1(assignment, domains, choice)
				if result!=None:#result not failure
					return result
				assignment.remove([selectedVariable, value])#remove demographic and comedian from assignment
		return None #it failed
	# Backtracking algorithm with stopping condition of the assignment being full(I.e length of assignment same as num of demographics*2 as this accounts for each demo having one main and one test show)
	# First we choose variable(demographic with smallest number of comedians that are valid for it) -fail first
	# Then we choose comedian from this set that is least constraining I.e. comedian with least appearances in other demographics valid comedians as least liekly to cause failure
	# Add this to assignment and call backtrack only if by adding we don't break constraint
	# If the assignment is invalid we just remove what we previously added
	def recursiveBacktrackingOp2(self, assignment, domains, choice):#assignment will append with (demoIndex, comIndex, typeShow)
		if len(assignment)==len(self.demographic_List)*2:
			return assignment
		selectedVariable=self.selectUnassignedVariable(assignment, domains, choice)#gives the variable with lowest num variables in either test or main and which one it from
		var=domains[selectedVariable[0]][selectedVariable[1]]
		for value in self.orderDomainValues(var, assignment, domains, choice):
			if self.checkConstraintHolds(value, selectedVariable[1], assignment):#constraints valid function that adds up hours to check
				assignment.append([selectedVariable[0], value, selectedVariable[1]])#add to assignment when adding just add test or main not main then test or test then main
				result=self.recursiveBacktrackingOp2(assignment, domains, choice)
				if result!=None:
					return result
				assignment.remove([selectedVariable[0], value, selectedVariable[1]])#remove from assignment
		return None

	# This will first go through all demographics and find one not already in assignment then it will loop through again and will choose the demographic with the least number of available comdians
	def selectUnassignedVariable(self, assignment, domains, choice):
		#choose it
		if choice==1:
			nextDemographic=0
			for demographic in range(len(domains)):
				if self.checkNotInAssignment(assignment, demographic, choice):
					nextDemographic=demographic
					break
			for demographic in range(nextDemographic, len(domains)):
				if self.checkNotInAssignment(assignment, demographic, choice) and (len(domains[demographic])<len(domains[nextDemographic])):
					nextDemographic=demographic
		else:
			nextDemographic=[0,0]
			for demographic in range(len(domains)*2):#depending on odd or even we look at main or test
				divMod=divmod(demographic,2)
				if self.checkNotInAssignment(assignment, demographic, choice):
					nextDemographic=[divMod[0],divMod[1]]  #this assigns (demoIndex, showType) 
					break
			for demographic in range(len(domains)*2):
				divMod=divmod(demographic,2)
				if self.checkNotInAssignment(assignment, demographic, choice) and (len(domains[divMod[0]][divMod[1]])<len(domains[nextDemographic[0]][nextDemographic[1]])):
					nextDemographic=[divMod[0],divMod[1]] #SAME HERE
			
		return nextDemographic
	# Checks given demographic is not already in assignment if is returns false if not true
	def checkNotInAssignment(self, assignment, demographic, choice):
		if choice==1:
			for value in assignment:
				if value[0]==demographic:
					return False
			return True
		else:
			divMod=divmod(demographic,2)
			for value in assignment:
				if value[0]==divMod[0] and value[2]==divMod[1]:
					return False
			return True
	# Sorts var(list of comedians) by number times comedian appears in remaining variable lists	so we pick the least constraining value first and therefore least likely to fail	
	def orderDomainValues(self, var, assignment, domains, choice):
		numComedian=[]
		for comedian in var:
			numComedian.append([comedian,self.numberComedians(comedian, assignment, domains, choice)])
		#sort list by this new list using the pair
		numComedian.sort(key=lambda x:x[1])
		comedians, num=zip(*numComedian)
		return comedians
		#remove 2nd part return normal list
	# Goes through all possible choices for every demographic and counts number of times the given comedian appears in it	
	def numberComedians(self, comedian, assignment, domains, choice):
		count=0
		if choice==1:
			temp=domains.copy()
			indices=[]
			for demCom in assignment:
				indices.append(demCom[0])
			temp= [i for j, i in enumerate(temp) if j not in indices]
			comedian={comedian}
			for selectedComedians in temp:
				if(comedian.issubset(selectedComedians)): #contains comedian then we up counter
					count+=1
			return count
		else:
			comedian={comedian}
			for demographic in range(len(domains)*2):
				divMod=divmod(demographic,2)
				if(self.checkNotInAssignment(assignment, demographic, choice) and comedian.issubset(domains[divMod[0]][divMod[1]])):
					count+=1
			return count
	# Goes through assignment finding all shows with that comedian and adding total hours worked to make sure constraint holds that comedian can't work more than 4 hours
	def checkConstraintHolds(self, value, showType, assignment):
		hoursCount=0
		for demComShow in assignment:
			if(demComShow[1]==value):
				hoursCount+=2-demComShow[2]#if show type is main(0) so hours increased by 2 otherwise test(1) so increased by 1
		hoursCount+=2-showType
		return hoursCount<=4

	# First we add shows where comedian perform more than once in week as these are only ones that can violate constraints
	# After we just add remaining shows in available slots as comedian only performs 1 show that week and so can't violate anything
	# For choosing which day to place duplicate comedians we go through and find valid day for it using function then we place it in that slot update the pointer pointing to next available slot on that day
	def mainShowSchedule(self, assignment, timetableObj):
		schedule = [[[None, None, None] for i in range(5)]for j in range(5)] #okay heres how we do this we take all assignments with same comedian and assigns to different days
		demographics, comedians = zip(*assignment)
		duplicates=self.findDuplicatesIndex(comedians)
		pointers=[0,0,0,0,0]
		for dupComediansIndex in duplicates:
			for dupComedian in dupComediansIndex:
				toBeAssigned= assignment[dupComedian]+[0]
				dayChoice= self.chooseValidDay(pointers, schedule, toBeAssigned, 2)#chooses day based on smallest pointer and meeting requirement for max hours
				schedule[dayChoice][pointers[dayChoice]]= toBeAssigned
				pointers[dayChoice]+= 1
				timetableObj.addSession(self.days[dayChoice], pointers[dayChoice], self.comedian_List[toBeAssigned[1]], self.demographic_List[toBeAssigned[0]], "main")
		assignment= self.removeDupsFromAssignment(assignment, duplicates)
		dayChoice=0
		for demComShow in assignment:
			while True:
				if pointers[dayChoice]<5:
					schedule[dayChoice][pointers[dayChoice]]=demComShow
					pointers[dayChoice]+=1
					timetableObj.addSession(self.days[dayChoice], pointers[dayChoice], self.comedian_List[demComShow[1]], self.demographic_List[demComShow[0]], "main")
					break
				else:
					dayChoice+=1
		
	# First we add shows where comedian perform more than once in week as these are only ones that can violate constraints
	# After we just add remaining shows in available slots as comedian only performs 1 show that week and so can't violate anything
	# For choosing which day to place duplicate comedians we go through and find valid day for it using function then we place it in that slot update the pointer pointing to next available slot on that day
	def mainAndTestShowSchedule(self, assignment, timetableObj):
		schedule = [[[None, None, None] for i in range(10)]for j in range(5)]
		showTypes = ["main", "test"]
		demographics, comedians, shows = zip(*assignment)
		duplicates=self.findDuplicatesIndex(comedians)

		#pointers for each day points to next available slot in day
		pointers=[0,0,0,0,0]
		for dupComediansIndex in duplicates:
			for dupComedian in dupComediansIndex:
				toBeAssigned= assignment[dupComedian]
				dayChoice= self.chooseValidDay(pointers, schedule, toBeAssigned, 2)#chooses day based on smallest pointer and meeting requirement for max hours
				schedule[dayChoice][pointers[dayChoice]]= toBeAssigned
				pointers[dayChoice]+= 1
				timetableObj.addSession(self.days[dayChoice], pointers[dayChoice], self.comedian_List[toBeAssigned[1]], self.demographic_List[toBeAssigned[0]], showTypes[toBeAssigned[2]])
		assignment= self.removeDupsFromAssignment(assignment, duplicates)
		dayChoice=0
		for demComShow in assignment:
			while True:
				if pointers[dayChoice]<10:
					schedule[dayChoice][pointers[dayChoice]]=demComShow
					pointers[dayChoice]+=1
					timetableObj.addSession(self.days[dayChoice], pointers[dayChoice], self.comedian_List[demComShow[1]], self.demographic_List[demComShow[0]], showTypes[demComShow[2]])
					break
				else:
					dayChoice+=1
	# First finds index of minimum pointer in temp(pointers) checks numHours comedian already worked in that day if hoursWorked plus this toBeAssigned show doesnt exceed max 2 hours then we return that pointer as valid
	# Otherwise we set this pointer to the max+1 so when we loop through to find next smallest pointer to check the old smallest can't be chosen 
	#So this will go through pointers in order of smallest to largest until one is valid day to place comedian show on
	def chooseValidDay(self, pointers, schedule, toBeAssigned, choice):
		
		temp=pointers.copy()

		if choice==2:
			while True:
				pointer = temp.index(min(temp))
				hoursWorked=0
				for demComShow in schedule[pointer]:
					if(demComShow[1]==toBeAssigned[1]):
						hoursWorked+=2-demComShow[2]#if show type is main(0) so hours increased by 2 otherwise test(1) so increased by 1
				if (hoursWorked+2-toBeAssigned[2])<=2:
					break
				temp[pointer]=max(temp)+1
		return pointer
	# Goes through assignment and only keeps element in it if its not in dupicates
	def removeDupsFromAssignment(self, assignment, duplicates):
		indices=[j for sub in duplicates for j in sub]
		assignment = [i for j, i in enumerate(assignment) if j not in indices]
		return assignment
	#For each item(x) in seq we find number of duplicates and if length of this num duplicates above 1 it added to list of items with a duplicate
	def findDuplicatesIndex(self, seq):
		duplicates=[]
		for x in seq:
			dups=self.listDuplicatesOf(seq, x)
			if(len(dups)>1):#if there is duplicate
				duplicates.append(dups)#this is indexes of dups
		return [list(element) for element in set(tuple(index) for index in duplicates)]#removes dups by switching to dict and back must turn to tuple to be able to hash
	#Goes through sequence and appends index of item in seq
	def listDuplicatesOf(self, seq, item):
		start=-1
		indexes = []
		while True:
			try:
				ind= seq.index(item, start+1)
			except ValueError:
				break
			else:
				indexes.append(ind)
				start= ind
		return indexes
	# Randomly creates first generation of size numParents
	# Shuffles list of integers 0-49 where 1 refers to demo 1 showType 1 and 2 refers to demo 2 showType 0 etc
	# Then for each slot we choose corresponding (demo,showType) and we choose a random comedian from those valid for the demo,showType
	def createParentGen(self, numParents, domains):
		
		parentGen =[{"Monday" : {}, "Tuesday" : {}, "Wednesday" : {}, "Thursday" : {}, "Friday" : {}} for i in range(numParents)]
		refToDomain = list(range(len(self.demographic_List)*2))
		for individual in parentGen:
			random.shuffle(refToDomain)
			for dayNumber, day in enumerate(self.days):
				for timeslot in range(1,11):
					demoRefChosen=refToDomain[dayNumber*10+timeslot-1]
					div=demoRefChosen//2
					mod=demoRefChosen & 1
					individual[day][timeslot]=[random.choice(domains[div][mod]),div,mod]
		return parentGen
	# Gets individual and checks its validity if totally valid we return its cost otherwise we return the number of errors of the individual
    # Got most of this from other files provided	
	def fitness(self, individual):
		errors=0

		comedian_Count = dict()
		main_demographics_Assigned = list()
		test_demographics_Assigned = list()
		schedule_Cost = 0
		comedians_Yesterday = list()
		main_show_Count = dict()
		test_show_Count = dict()

		for comedian in range(len(self.comedian_List)):
			main_show_Count[comedian] = 0
			test_show_Count[comedian] = 0
			comedian_Count[comedian] = 0


		for day in individual:
			day_List = individual[day]

			#Again, we check each day has all of its slots assigned
			if len(day_List) != 10:
				print(len(day_List))
				print(str(day) + " does not have every slot assigned.")
				errors += 1

			comedians_Today = dict()
			possible_Discount = dict()

			#process the validity of each entry
			for entry in individual[day]:
				[comedian, demographic, show_type] = day_List[entry]

				if show_type == 0:
					if demographic in main_demographics_Assigned:
						#print(str(demographic) + " is being marketed more than one main show a week.")
						errors+=1
					else:
						main_demographics_Assigned.append(demographic)

				else:
					if demographic in test_demographics_Assigned:
						#print(str(demographic) + " is being marketed more than one test show a week.")
						errors+=1
					else:
						test_demographics_Assigned.append(demographic)

				#We now go through every comedian to make sure they are not on stage for too long in a week	
				if comedian in comedians_Today:
					#This branch means the comedian is already on stage today.
					if comedians_Today[comedian] >= 2:
						#print(str(comedian) + " is already on stage for two hours on " + str(day))
						errors += 1
					
					#We calculate the cost for the show, if it is a main show.
					if show_type == 0:
						comedians_Today[comedian] = comedians_Today[comedian] + 2
						main_show_Count[comedian] = main_show_Count[comedian] + 1
						if main_show_Count[comedian] == 1:
							schedule_Cost = schedule_Cost + 500
						elif comedian in comedians_Yesterday:
							schedule_Cost = schedule_Cost + 100
						else:
							schedule_Cost = schedule_Cost + 300
					else:
						#We calculate the cost of a test show
						comedians_Today[comedian] = comedians_Today[comedian] + 1
						test_show_Count[comedian] = test_show_Count[comedian] + 1
						initial_test_show_Cost = (300 - (50 * test_show_Count[comedian])) / 2
						schedule_Cost = schedule_Cost + initial_test_show_Cost

						if comedian in possible_Discount:
							schedule_Cost = schedule_Cost - possible_Discount.pop(comedian)
				else:
					#This branch means the comedian has not yet been on stage today
					#We calculate the costs correspondingly
					if show_type == 0:
						comedians_Today[comedian] = 2
						main_show_Count[comedian] = main_show_Count[comedian] + 1
						if main_show_Count[comedian] == 1:
							schedule_Cost = schedule_Cost + 500
						elif comedian in comedians_Yesterday:
							schedule_Cost = schedule_Cost + 100
						else:
							schedule_Cost = schedule_Cost + 300
					else:
						comedians_Today[comedian] = 1

						test_show_Count[comedian] = test_show_Count[comedian] + 1
						initial_test_show_Cost = (300 - (50 * test_show_Count[comedian]))
						schedule_Cost = schedule_Cost + initial_test_show_Cost
						possible_Discount[comedian] = initial_test_show_Cost / 2

				#We update the hours the comedian is on stage for the week
				if show_type == 0:
					comedian_Count[comedian] = comedian_Count[comedian] + 2
				else:
					comedian_Count[comedian] = comedian_Count[comedian] + 1

				#Make sure a comedian is not on stage for more than four hours a week
				if comedian_Count[comedian] > 4:
						#print(str(comedian) + " is already on stage for 4 hours")
						errors += 1			

			#One last check to make sure daily stage hours haven't been exceeded
			for name in comedians_Today:
				if comedians_Today[name] > 2:
					#print(str(name) + " is on stage for more than two hours in a day.")
					errors += 1

			comedians_Yesterday = comedians_Today

		#One final check to make sure total hours haven't been exceeded
		for name in comedian_Count:
			if comedian_Count[name] > 4:
				#print(str(name) + " is on stage for more than four hours a week")
				errors += 1

		#If we get here, schedule is legal, so we assign the cost and return True
		if errors!=0:
			schedule_Cost=None
		return [errors, schedule_Cost]
	# Evaluates cost for each individual adds it to list
	# Then we sort generation by lowest cost and select number of individuals for next generation by numBestSelected
	# Sorting will first look at actual cost and go from lowest to highest but if cost is Null which occurs when not valid solution it sorts by lowest number of errors 
	def selectBest(self, parentGen, numBestSelected):
		costs=[self.fitness(individual) for individual in parentGen]
		sortedparentGen=[individual for cost, individual in sorted(zip(costs ,parentGen), key=lambda x: (x[0][1] is None, x[0][1], x[0][0] ))]
		return sortedparentGen[:numBestSelected]
	# We go through pairs in the generation next to each other. If we go past length of generation we loop around
	# Then we run crossover on pair to get its children which is then added to the offspring as well as the original parent in case both children worse than parents we keep parent
	# in next generation so if parent better it will be used for next generation instead of worse children. Ensures genetic algorithm closes in on more optimal solution and doesn't go in wrong direction
	def crossover(self, parentGen, numOffspring):
		offspring=[]
		
		for ind in range(numOffspring):#Instead of using pythons [-1] index to make sure we don't exceed length of list we do this way as would rather crossover individuals at the start again as more likely to give better solution
			parent1=parentGen[ind%len(parentGen)]#select parent1
			parent2=parentGen[(ind+1)%len(parentGen)]#select parent2
			children=self.crossoverPair(parent1,parent2)
			offspring.extend(children)
		offspring.extend(parentGen)
		return offspring
	# For the 2 parents we go through the parents and we have a half chance of adding this to the child in the same slot
	# Otherwise we add the demographic and showType to dict(demoToBeAdded) for use later as well as store the slot we haven't used
	# Now we go through all the timeslots again and if in a slot we find demo and show in demoToBeAdded we then add it to the child in an available slot from emptySlots
	# This creates 2 children where child1 uses parent1 slots and then fills the rest with available from parent2 and vice versa for child2
	def crossoverPair(self,parent1, parent2):
		child1={"Monday" : {}, "Tuesday" : {}, "Wednesday" : {}, "Thursday" : {}, "Friday" : {}}
		child2={"Monday" : {}, "Tuesday" : {}, "Wednesday" : {}, "Thursday" : {}, "Friday" : {}}
		demoToBeAdded1=dict()
		demoToBeAdded2=dict()
		emptySlots=[]

		for dayNumber, day in enumerate(self.days):
			for timeslot in range(1, 11):
				if random.random()<0.5:
					child1[day][timeslot]=parent1[day][timeslot]
					child2[day][timeslot]=parent2[day][timeslot]
				else:
					temp1=parent1[day][timeslot]
					temp2=parent2[day][timeslot]
					demoToBeAdded1[str(temp1[1])+str(temp1[2])]=True
					demoToBeAdded2[str(temp2[1])+str(temp2[2])]=True
					emptySlots.append([day,timeslot])
		i,j =0, 0
		for dayNumber, day in enumerate(self.days):
			for timeslot in range(1, 11):
				temp1=parent2[day][timeslot]
				temp2=parent1[day][timeslot]
				if str(temp1[1])+str(temp1[2]) in demoToBeAdded1:
					child1[emptySlots[i][0]][emptySlots[i][1]]=temp1
					i+=1
				if str(temp2[1])+str(temp2[2]) in demoToBeAdded2:
					child2[emptySlots[j][0]][emptySlots[j][1]]=temp2
					j+=1
		return (child1,child2)
	# Goes through every individual in the generation and mutates each individual 
	def mutation(self, parentGen, numMutations, domains):
		mutatedParentGen=[]
		for individual in parentGen:
			mutatedParentGen.append(self.mutateIndividual(individual, numMutations, domains))
		return mutatedParentGen
	# Gets an individual and randomly replaces a slot with another comedian that is valid for that demographic. Does this numMutations times
	def mutateIndividual(self, individual, numMutations, domains):
		for num in range(numMutations):
			toBeMutated=random.choice(range(50))
			digits=self.getDigits(toBeMutated)
			digits[1]+=1
			old=individual[self.days[digits[0]]][digits[1]]
			individual[self.days[digits[0]]][digits[1]]=[random.choice(domains[old[1]][old[2]]),old[1],old[2]]
		
		return individual
	# Gets integer and splits it into its digits E.g.14=[1,4]
	def getDigits(self, number):
		digits=[int(digit) for digit in str(number)]
		if number<10:
			digits=[0,digits[0]]
		return digits