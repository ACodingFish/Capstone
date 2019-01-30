#include <cstdlib>
#include <iostream>
#include <string>
#include <cmath>
#include "ConfigCommands.h"

#define NUMBER_OF_ARGUMENTS (1+1)

using namespace std;

int main(int argc, char *argv[])
{
    if (argc < NUMBER_OF_ARGUMENTS){
		cout << "Too few arguments.";
		return -1;
	} else if (argc > NUMBER_OF_ARGUMENTS){
		cout << "Too Many arguments.";
		return -1;
	}

	return 0;
}
