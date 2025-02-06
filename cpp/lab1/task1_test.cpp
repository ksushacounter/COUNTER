#include <gtest/gtest.h>
#include "Table.h" 


TEST(TableTest, fall) {
    table<int, std::string> myTable;

    myTable[3] = "Three"; 
    myTable[1] = "One";   
    myTable[2] = "Two";   
    
    EXPECT_EQ(myTable[1], "One"); 
    EXPECT_EQ(myTable[2], "Two"); 
    EXPECT_EQ(myTable[3], "Three"); 
    
    
}

TEST(TableTest, 100_el) {
    table<int, std::string> myTable;
    for(std::size_t i = 0; i < 100; ++i){
        myTable[i] = "something" + i;
    }
    for(std::size_t i = 0; i < 100; ++i){
        EXPECT_EQ(myTable[i], "something"+i);
    }
}
int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
