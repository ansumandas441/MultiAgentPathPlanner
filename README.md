	
Problem:

![Screenshot from 2021-03-31 21-26-54](https://user-images.githubusercontent.com/42487965/113177563-4a431b80-926b-11eb-971a-dc69f61aa3b5.png)


	

Robot sources are:
	
	source	Destination
	(0,0)	(0,8)
	(0,0)	(5,5)
	(5,9)	(5,5)

Tasks are:
	
	Task	Pickup	Delivery
	1	(5,0)	(3,12)
	2	(4,6)	(0,5)
	3	(5,0)	(0,5)	

Blockage:
	
	(2,1), (5,3) (4,10) (0,13) (2,15)

 
For Optimal Distance between two points Iterretive Deepening is used for storage requirement.
The schedule is made using hamiltonian cycles.



Usage:

	python search_heuristic.py task
