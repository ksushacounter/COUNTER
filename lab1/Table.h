    
    
    FlatMap& operator=(const FlatMap& other_map);

    std::size_t size() const;
    std::string& operator[](const std::string& key);

    bool contains(const std::string& key);
    std::size_t erase(const std::string& key);
    void clear();