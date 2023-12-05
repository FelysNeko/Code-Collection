#include <iostream>


double search(double *array, std::size_t cap, double x) {
    std::size_t left{0};
    std::size_t mid{0};
    std::size_t right{cap-1};
    
    while (left<=right && right<cap) {
        mid = left + (right-left)/2;

        if (array[mid] == x) {
            return mid;
        } else if (array[mid] > x) {
            right = mid - 1;
        } else if (array[mid] < x) {
            left = mid + 1;
        }
    }

    return cap;
}


int main(void)
{
    double array[]{0.3, 1.2, 1.5, 2.7, 4.6, 5};
    std::size_t cap = sizeof(array) / sizeof(double);

    std::cout << search(array, cap, 10) << std::endl;

    return 0;
}
