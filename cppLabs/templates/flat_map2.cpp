#include <iostream>
#include <iterator>

template <typename KEY, typename VALUE>
class table {
    struct line {
        KEY key;
        VALUE val;
    };

private:
    line* array;
    std::size_t count;
    std::size_t capacity;

public:
    table()
        : array(new line[10]), count(0), capacity(10) {}

    table(const table& other)
        : count(other.count), capacity(other.capacity) {
        array = new line[capacity];
        for (std::size_t i = 0; i < count; ++i) {
            array[i] = other.array[i];
        }
    }

    ~table() {
        this->clear();
    }

    table& operator=(const table& other) {
        if (this == &other) {
            return *this;
        }

        delete[] array;
        count = other.count;
        capacity = other.capacity;
        array = new line[capacity];
        for (std::size_t i = 0; i < count; ++i) {
            array[i] = other.array[i];
        }
        return *this;
    }

    std::size_t current_size() const {
        return count;
    }

    VALUE& operator[](const KEY& key) {
        std::size_t index = search(key);
        if (index != static_cast<std::size_t>(-1)) {
            return array[index].val;
        }
        memory();
        array[count].key = key;
        array[count].val = VALUE();
        return array[count++].val;
    }

    bool contains(const KEY& key) const {
        return search(key) != static_cast<std::size_t>(-1);
    }

    std::size_t erase(const KEY& key) {
        std::size_t i = search(key);
        if (i == static_cast<std::size_t>(-1)) {
            return 0;
        }
        --count;
        line* del = array + i;
        line* last = array + count;
        for (; del < last; ++del) {
            *del = *(del + 1);
        }
        if (!count) {
            this->clear();
        }
        return 1;
    }

    void clear() {
        delete[] array;
        array = new line[capacity];
        count = 0;
    }

private:
    bool memory() {
        if (count + 1 > capacity) {
            capacity = count + (capacity / 2);
            line* new_array = new line[capacity];
            for (std::size_t i = 0; i < count; ++i) {
                new_array[i] = array[i];
            }
            delete[] array;
            array = new_array;
        }
        return true;
    }

    std::size_t search(const KEY& key) const {
        std::size_t f = 0, l = count;
        while (f < l) {
            std::size_t m = (f + l) >> 1;
            if (key < array[m].key) {
                l = m;
            } else if (key > array[m].key) {
                f = m + 1;
            } else {
                return m;
            }
        }
        return static_cast<std::size_t>(-1);
    }

public:
    class iterator {
        line* ptr;

    public:
        iterator(line* p = nullptr) : ptr(p) {}

        iterator& operator++() {
            ++ptr;
            return *this;
        }

        iterator operator++(int) {
            iterator temp = *this;
            ++ptr;
            return temp;
        }

        line& operator*() {
            return *ptr;
        }

        line* operator->() {
            return ptr;
        }

        bool operator==(const iterator& other) const {
            return ptr == other.ptr;
        }

        bool operator!=(const iterator& other) const {
            return ptr != other.ptr;
        }
    };

    iterator begin() {
        return iterator(array);
    }

    iterator end() {
        return iterator(array + count);
    }
};

int main() {
    table<std::string, int> myTable;

    myTable["a"] = 1;
    myTable["b"] = 2;
    myTable["c"] = 3;

    std::cout << myTable["a"] << " " << myTable["b"] << "\n";

    for (auto it = myTable.begin(); it != myTable.end(); ++it) {
        std::cout << it->key << " " << it->val << std::endl;
    }

    myTable["d"] = 4;
    for (auto& elem : myTable) {
        std::cout << elem.key << " " << elem.val << std::endl;
    }

    myTable.clear();
    std::cout << "Size after clear: " << myTable.current_size() << std::endl;

    return 0;
}

