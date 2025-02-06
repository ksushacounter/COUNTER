#include <iostream>
#include <cmath>

class Point {
private:
    size_t size;   
    double* array; 

public:
    Point(size_t size) : size(size) {
        array = new double[size];
        for (size_t i = 0; i < size; ++i) {
            array[i] = 0.0;
        }
    }

    Point(const Point &other)
    {
        array = new double[size];
        for (std::size_t i = 0; i < size; ++i)
        {
            array[i] = other.array[i];
        }
    }

    ~Point() {
        delete[] array;
    }

    Point &operator = (const Point &other){
        delete[] array;
        size = other.size;
        array = new double[size];
        for (int i = 0; i < size; i++){
            array[i] = other.array[i];
        }
        return *this;
    }

    double distance() const {
        double sum = 0.0;
        for (size_t i = 0; i < size; ++i) {
            sum += std::pow(array[i], 2);
        }
        return std::sqrt(sum);
    }


    void set(size_t index, double value) {
        array[index] = value;
    }

    double get(size_t index) const {
        return array[index];
    }
};

int main() {
    size_t my_size;
    std::cin >> my_size;

    Point p(my_size);

    for (size_t i = 0; i < my_size; ++i) {
        double value;
        std::cin >> value;
        p.set(i, value);
    }

    std::cout << p.distance() << "\n";

    return 0;
}
