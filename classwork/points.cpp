#include<iostream>
#include<math.h>

class point{
public:
    point(float x, float y) : _x(x), _y(y){
    }
    float distance(){
        return sqrt(pow(_x,2) + pow(_y,2));
    }
private:
    float _x;
    float _y;
};

int main(void){
    float x,y;
    std:: cout << "Enter x & y:";
    std:: cin >> x >> y;

    point p(x, y);
    std:: cout << "Distance:" << p.distance() << p.distance() << "\n";
    return 0;
}
