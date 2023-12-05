#include <iostream>


void insertion(double *array, std::size_t cap)
{
    std::size_t index{};
    double value{};

    for (std::size_t i{1}; i<cap; ++i) {
        value = array[i];
    
        for (index=i; index>0 && value<array[index-1]; --index) {
            array[index] = array[index-1];
        }

        array[index] = value;
    }
}


int main(void) 
{
    double array[]{7,4,4,2,1,5,4,2,9};
    std::size_t cap = sizeof(array) / sizeof(double);

    insertion(array, cap);
    
    for (std::size_t i{0}; i<cap; ++i) {
        std::cout << array[i];
    }
    std::cout << std::endl;
    
    return 0;
}

