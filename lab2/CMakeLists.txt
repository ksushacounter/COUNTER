cmake_minimum_required(VERSION 3.10) 
set(CMAKE_CXX_STANDARD 17)

project(lab2)

set(exe_name ${PROJECT_NAME})  

include_directories(include)

set(SOURCES
    src/main.cpp
    src/music.cpp
    src/factory.cpp
    src/converter.cpp
)


add_executable(${exe_name} ${SOURCES})

# Зависимости для основного приложения
# Если corelib - это библиотека, то ее нужно либо создать, либо указать правильный путь к ней
# target_link_libraries(${exe_name} corelib)  # Убедитесь, что corelib правильно создана

# Загружаем GoogleTest через FetchContent
include(FetchContent)
FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/58d77fa8070e8cec2dc1ed015d66b454c8d78850.zip
)


set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)


