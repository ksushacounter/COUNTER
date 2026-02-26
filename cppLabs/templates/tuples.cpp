#include <iostream>
#include <tuple>
#include <string>

template <int Index, typename... Types>
typename std::enable_if<Index == sizeof...(Types)>::type
printTuple(std::ostream &os, const std::tuple<Types...> &)
{
}

template <int Index, typename... Types>
typename std::enable_if <Index < sizeof...(Types)>::type
printTuple(std::ostream &os, const std::tuple<Types...> &t)
{
    if (Index > 0)
    {
        os << ", ";  
    }
    os << std::get<Index>(t);  
    printTuple<Index + 1>(os, t);  
}

template <typename... Types>
std::ostream &operator<<(std::ostream &os, const std::tuple<Types...> &t)
{
    os << "(";  
    printTuple<0>(os, t);  
    os << ")";  
    return os;
}

int main()
{
    std::tuple<int, std::string, double> t = {5, "abcd", 3.14};
    std::cout << t << std::endl;  
    return 0;
}
