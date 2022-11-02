// file main.cpp
#include <stdio.h>
#include "filter.h"

int main(void) {
   Filter_lowpass_2x_type filter;
   // initialization
   Filter_lowpass_2x_init(filter);

   // inputs to the function
   float x = 10.0f;
   float w = 2.0f;
   float q = 4.0f;

   // calling the function
   float result = Filter_lowpass_2x(filter,x,w,q);
   printf("result = %4.2f\n", result);
   return 0;
}
