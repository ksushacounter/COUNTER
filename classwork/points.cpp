#include<iostream>
#include<math.h>

class point{
private:
    float size;
    double array;
public:
    point() : array(nullptr), size(10) {
        double array = new point[size];
    }

    ~point() {
        delete[] array;
    }

    float distance(){
        float sum = 0;
        for (int i = 0; i < size; i++){
            float a = array[i];
            sum += pow(a,2);
        }
        return sqrt(sum);
    }

    void setx(){
        
        } 

    void getx(){
        
    }

};

int main(void){
    float x,y;
    std:: cout << "Enter x & y:";
    std:: cin >> x >> y;

    point p(x, y);
    std:: cout << "Distance:" << p.distance() << p.distance() << "\n";
    return 0;
}
