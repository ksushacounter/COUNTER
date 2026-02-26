#include <iostream>

template<typename T>
class array 
{
public:
    array(int size): list(new T[size]), size(size){};
    void add_element(int index, T value)
    {
        list[index] = value;
    }
    void print_array()
    {
        for(int i = 0; i < size; i++)
        std::cout << list[i] << std::endl;
    }
    ~array() 
    {
        delete[] list;
    }
private:
    T* list;
    int size;
};

main()
{
    int a = 5, b = 4, c = 3;
    int size = 3;
    array<int> array1{size};
    array1.add_element(0, a);
    array1.add_element(1, b);
    array1.add_element(2, c);
    array1.print_array();
}