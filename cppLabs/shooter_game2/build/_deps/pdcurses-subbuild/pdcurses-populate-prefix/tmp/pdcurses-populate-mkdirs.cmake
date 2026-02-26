# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

# If CMAKE_DISABLE_SOURCE_CHANGES is set to true and the source directory is an
# existing directory in our source tree, calling file(MAKE_DIRECTORY) on it
# would cause a fatal error, even though it would be a no-op.
if(NOT EXISTS "C:/Users/garku/VSCodeProjects/shooter_game2/build/_deps/pdcurses-src")
  file(MAKE_DIRECTORY "C:/Users/garku/VSCodeProjects/shooter_game2/build/_deps/pdcurses-src")
endif()
file(MAKE_DIRECTORY
  "C:/Users/garku/VSCodeProjects/shooter_game2/build/_deps/pdcurses-build"
  "C:/Users/garku/VSCodeProjects/shooter_game2/build/_deps/pdcurses-subbuild/pdcurses-populate-prefix"
  "C:/Users/garku/VSCodeProjects/shooter_game2/build/_deps/pdcurses-subbuild/pdcurses-populate-prefix/tmp"
  "C:/Users/garku/VSCodeProjects/shooter_game2/build/_deps/pdcurses-subbuild/pdcurses-populate-prefix/src/pdcurses-populate-stamp"
  "C:/Users/garku/VSCodeProjects/shooter_game2/build/_deps/pdcurses-subbuild/pdcurses-populate-prefix/src"
  "C:/Users/garku/VSCodeProjects/shooter_game2/build/_deps/pdcurses-subbuild/pdcurses-populate-prefix/src/pdcurses-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "C:/Users/garku/VSCodeProjects/shooter_game2/build/_deps/pdcurses-subbuild/pdcurses-populate-prefix/src/pdcurses-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "C:/Users/garku/VSCodeProjects/shooter_game2/build/_deps/pdcurses-subbuild/pdcurses-populate-prefix/src/pdcurses-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
