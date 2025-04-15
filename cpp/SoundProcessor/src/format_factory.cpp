#include <memory>
#include <stdexcept>
#include "music.h"
#include "format_factory.h"

bool format_factory::ends_with(const std::string file_path, const std::string suffix)
{
    if (suffix.size() > file_path.size())
        return false;
    return std::equal(suffix.rbegin(), suffix.rend(), file_path.rbegin());
}
std::unique_ptr<FORMAT> format_factory::create_format(const std::string file_path)
{
    if (ends_with(file_path, ".wav"))
    {
        return std::make_unique<WAV>(file_path);
    }

    throw std::runtime_error("Unsupported file format: " + file_path);
}
