CXX = g++
CXXFLAGS = -std=c++11
TARGET = explore_system
OBJS = ExploreSystem.o main.o

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $(TARGET)

ExploreSystem.o: ExploreSystem.cpp ExploreSystem.h
	$(CXX) $(CXXFLAGS) -c ExploreSystem.cpp

main.o: main.cpp ExploreSystem.h
	$(CXX) $(CXXFLAGS) -c main.cpp

.PHONY: clean
clean:
	rm -f $(OBJS) $(TARGET)
