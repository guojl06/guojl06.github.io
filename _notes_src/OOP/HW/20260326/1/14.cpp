#include <iostream> 
using namespace std;

class Counter {
private:
    int count;

public:
    void reset() {
        count = 0;
    }

    void increment() {
        count++;
    }

    void decrement() {
        count--;
    }

    int getCount() {
        return count;
    }
};

int main() {
    Counter c;

    c.reset();
    c.increment();
    c.increment();
    c.decrement();
    c.increment();

    cout << c.getCount() << endl;

    return 0;
}
