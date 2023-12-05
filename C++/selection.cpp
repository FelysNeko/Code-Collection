#include <iostream>


void selection(double *array, std::size_t cap)
{
    std::size_t index{};
    double temp{};

    for (std::size_t i{cap-1}; i>0; --i) {
        index = 0;
        for (std::size_t x{0}; x<=i; ++x) {
            if (array[x] > array[index]) {
                index = x;
            }
        }

        temp = array[i];
        array[i] = array[index];
        array[index] = temp;
    }
}


int main(void) 
{
    double array[]{7,4,4,2,1,5,4,2,9};
    std::size_t cap = sizeof(array) / sizeof(double);

    selection(array, cap);
    
    for (std::size_t i{0}; i<cap; ++i) {
        std::cout << array[i];
    }
    std::cout << std::endl;
    
    return 0;
}

