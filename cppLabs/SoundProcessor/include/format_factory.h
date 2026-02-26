#include <memory>
#include <stdexcept>
#include "music.h"

class format_factory
{
public:
    static bool ends_with(std::string input_path, const std::string suffix);
    static std::unique_ptr<FORMAT> create_format(const std::string file_path);
};