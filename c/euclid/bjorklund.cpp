#include <iostream>
#include <string>

/**
Bjorklund's Algorithm

from: https://bitbucket.org/sjcastroe/bjorklunds-algorithm/src/master/

bjorklund evenly distributes a number of beats within a set number of total steps (thereby creating a rhythm)
Ex. if beats = 4 and steps = 8, "11110000" ==> "10101010"
@param beats is the number of "active" steps (a single beat is represented by a "1")
@param steps is the total number of units (total number of "1"s and "0"s)
*/

std::string bjorklund(int beats, int steps);


std::string bjorklund(int beats, int steps)
{
	//We can only have as many beats as we have steps (0 <= beats <= steps)
	if (beats > steps)
		beats = steps;

	//Each iteration is a process of pairing strings X and Y and the remainder from the pairings
	//X will hold the "dominant" pair (the pair that there are more of)
	std::string x = "1";
	int x_amount = beats;

	std::string y = "0";
	int y_amount = steps - beats;

	do
	{
		//Placeholder variables
		int x_temp = x_amount;
		int y_temp = y_amount;
		std::string y_copy = y;

		//Check which is the dominant pair 
		if (x_temp >= y_temp)
		{
			//Set the new number of pairs for X and Y
			x_amount = y_temp;
			y_amount = x_temp - y_temp;

			//The previous dominant pair becomes the new non dominant pair
			y = x;
		}
		else
		{
			x_amount = x_temp;
			y_amount = y_temp - x_temp;
		}

		//Create the new dominant pair by combining the previous pairs
		x = x + y_copy;
	} while (x_amount > 1 && y_amount > 1);//iterate as long as the non dominant pair can be paired (if there is 1 Y left, all we can do is pair it with however many Xs are left, so we're done)

	//By this point, we have strings X and Y formed through a series of pairings of the initial strings "1" and "0"
	//X is the final dominant pair and Y is the second to last dominant pair
	std::string rhythm;
	for (int i = 1; i <= x_amount; i++)
		rhythm += x;
	for (int i = 1; i <= y_amount; i++)
		rhythm += y;
	return rhythm;
}



int main(int argc, char *argv[])
{
	if (argc == 3) {
		int beats = atoi(argv[1]);
		int steps = atoi(argv[2]);

		std::cout << bjorklund(beats, steps) << std::endl;
		return 0;		
	} else {
		printf("usage: bjorkland <n_beats> <n_steps>");
	}

}
