
#include <iostream>
#include <string>
#include "Table.h" 

int main() {
    table<std::string, int> myTable;

    myTable["a"] = 1;
    myTable["b"] = 2;
    myTable["c"] = 3;

    std::cout << myTable["a"] << " " << myTable["b"] << "\n";

    myTable.clear();
    std::cout << "Size after clear: " << myTable.current_size() << std::endl;

    return 0;
}
