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

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
