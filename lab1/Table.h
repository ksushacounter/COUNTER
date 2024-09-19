#include <iostream>

template <typename KEY, typename value>
class table
{
    struct line
    {
        KEY key;
        value val;
    };

private:
    line *array;
    std::size_t count;
    std::size_t capacity;

public:
    table()
        : array(new line[10]), count(0), capacity(10) {}

    table(const table &other)
        : count(other.count), capacity(other.capacity)
    {
        array = new line[capacity];
        for (std::size_t i = 0; i < count; ++i)
        {
            array[i] = other.array[i];
        }
    }

    ~table()
    {
        this->clear();
    }

    table &operator=(const table &other)
    {
        if (this == &other)
        {
            return *this;
        }

        delete[] array;
        count = other.count;
        capacity = other.capacity;
        array = new line[capacity];
        for (std::size_t i = 0; i < count; ++i)
        {
            array[i] = other.array[i];
        }
        return *this;
    }

    std::size_t current_size(void)
    {
        return count;
    }

    value &operator[](const KEY &key)
    {
        std::size_t index = search(key);
        if (index != -1)
        {
            return array[index].val;
        }
        memory();
        
        array[count].key = key; 
        array[count].val = value(); 
        return array[count++].val;
    }

    bool contains(const KEY &key) const
    {
        return search(key) != -1;
    }

    std::size_t erase(const KEY &key)
    {
        std::size_t i = search(key);
        if (i == -1)
        {
            return 0; // не нашли
        }
        --count;
        line *del = array + i;
        line *last = array + count;
        for (; del < last; ++del)
        { // сдвиг
            *del = *(del + 1);
        }
        if (!count)
        {
            this->clear();
        }
        return 1;
    }

    void clear()
    {
        delete[] array;
        array = new line[capacity];
        count = 0;
    }

private:
    bool memory()
    {
        if (count + 1 > capacity)
        {
            capacity = count + (capacity / 2);
            line *new_array = new line[capacity];

            for (std::size_t i = 0; i < count; ++i)
            {
                new_array[i] = array[i];
            }
            delete[] array;
            array = new_array;
        }
        return true;
    }

    std::size_t search(const KEY &key) const
    {
        std::size_t f = 0, l = count;
        while (f < l)
        {
            std::size_t m = (f + l) >> 1;
            if (key < array[m].key)
            {
                l = m;
            }
            else if (key > array[m].key)
            {
                f = m + 1;
            }
            else
            {
                return m;
            }
        }
        return static_cast<std::size_t>(-1);
    }
};
