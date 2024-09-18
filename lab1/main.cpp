
#include <iostream>
#include <string>
#include "Table.h" 

int main() {
    table<std::string, int> myTable;

    myTable["apple"] = 10;
    myTable["banana"] = 20;
    myTable["cherry"] = 30;

    std::cout << "Size: " << myTable.current_size() << std::endl;

    if (myTable.contains("banana")) {
        std::cout << "Table contains 'banana'" << std::endl;
    } else {
        std::cout << "Table does not contain 'banana'" << std::endl;
    }

    std::cout << "Value for 'apple': " << myTable["apple"] << std::endl;

    myTable.erase("banana");
    std::cout << "Size after erase: " << myTable.current_size() << std::endl;

    if (!myTable.contains("banana")) {
        std::cout << "Table does not contain 'banana' anymore" << std::endl;
    }

    myTable.clear();
    std::cout << "Size after clear: " << myTable.current_size() << std::endl;

    return 0;
}
