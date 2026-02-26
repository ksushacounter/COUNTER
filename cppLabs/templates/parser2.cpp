#include <iostream>
#include <fstream>
#include <sstream>
#include <tuple>
#include <vector>
#include <string>
#include <iterator>
#include <stdexcept>

template <int index, typename... types>
typename std::enable_if<index == sizeof...(types)>::type
print_tuple(std::ostream &os, const std::tuple<types...> &)
{
}

template <int index, typename... types>
typename std::enable_if<index < sizeof...(types)>::type
print_tuple(std::ostream &os, const std::tuple<types...> &t)
{
    if (index > 0)
    {
        os << ", ";
    }
    os << std::get<index>(t);
    print_tuple<index + 1>(os, t);
}

template <typename... types>
std::ostream &operator<<(std::ostream &os, const std::tuple<types...> &t)
{
    os << "(";
    print_tuple<0>(os, t);
    os << ")";
    return os;
}

template <typename... types>
class csv_parser
{
public:
    class iterator;
    csv_parser(std::istream &input, int skip_lines) : input_stream(input), skip_lines(skip_lines)
    {
        std::string line;
        for (size_t i = 0; i < skip_lines; ++i)
        {
            if (!std::getline(input_stream, line))
            {
                break;
            }
        }
    }

    iterator begin()
    {
        return iterator(input_stream);
    }

    iterator end()
    {
        return iterator();
    }

    class iterator
    {
    public:
        iterator() : input_stream(nullptr), end_of_stream(true) {}

        iterator(std::istream &stream) : input_stream(&stream), end_of_stream(false)
        {
            ++(*this);
        }

        std::tuple<types...> operator*() const
        {
            return current_row;
        }

        iterator &operator++()
        {
            if (!input_stream || !std::getline(*input_stream, current_line))
            {
                end_of_stream = true;
                return *this;
            }

            std::istringstream line_stream(current_line);
            parse_line(line_stream, current_row, std::index_sequence_for<types...>{});
            return *this;
        }

        bool operator!=(const iterator &other) const
        {
            return  (number_line != other.number_line);
        }

    private:
        std::istream *input_stream;
        bool end_of_stream;
        std::string current_line;
        std::tuple<types...> current_row;
        int number_line = -1;

        template <std::size_t... indexes>
        void parse_line(std::istream &line_stream, std::tuple<types...> &row, std::index_sequence<indexes...>)
        {
            int index = 0;
            number_line++;
            std::string cell;
            ((parse_cell<indexes>(line_stream, std::get<indexes>(row), index)), ...);

            if (line_stream >> cell)
            {
                throw std::runtime_error("Too many columns in line: " + current_line);
            }
        }

        template <std::size_t Index, typename t>
        void parse_cell(std::istream &line_stream, t &field, int &index)
        {
            std::string cell;
            if (!std::getline(line_stream, cell, ','))
            {
                throw std::runtime_error("Too few columns in line: " + current_line);
            }
            try
            {
                field = convert_to<t>(cell);
            }
            catch (const std::exception &e)
            {
                throw std::runtime_error("Failed to parse column " + std::to_string(index) + ": " + e.what());
            }
            ++index;
        }

        template <typename t>
        t convert_to(const std::string &str)
        {
            if constexpr (std::is_same<t, std::string>::value)
            {
                return str;
            }
            else
            {
                std::istringstream ss(str);
                t value;
                if (!(ss >> value))
                {
                    throw std::invalid_argument("Invalid conversion");
                }
                return value;
            }
        }
    };

private:
    std::istream &input_stream;
    int skip_lines;
};

int main()
{
    try
    {
        std::ifstream file("example.csv");
        // csv_parser<int, std::string, double> parser(file, 1);
        // for (const auto &row : parser)
        // {
        //     std::cout << row << "\n";
        // }
        csv_parser<int, std::string, double>::iterator iterator(file);
        csv_parser<int, std::string, double>::iterator iterator2(file);

        // if (iterator != iterator2)
        // {
        // std::cout << *iterator << std::endl;
        // ++iterator;
        // }

        std::cout << *iterator << std::endl;
        std::cout << *iterator2 << std::endl;
        ++iterator;
        std::cout << (iterator != iterator2) << std::endl;



        // if (iterator != iterator2)
        // {
        //     std::cout << *iterator << std::endl;
        //     ++iterator;
        // }

        // if (iterator != iterator2)
        // {
        //     std::cout << *iterator << std::endl;
        //     ++iterator;
        // }

            

        // std::cout << "Enter CSV data:\n";
        // csv_parser<int, std::string, double> stdin_parser(std::cin, 0);
        // for (const auto &row : stdin_parser)
        // {
        //     std::cout << row << "\n";
        // }
    }
    catch (const std::exception &e)
    {
        std::cerr << "Error: " << e.what() << "\n";
    }
    return 0;
}
