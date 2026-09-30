CC = g++
CFLAGS = -g
DEPS = Value.h Operator.h Value.cpp Operator.cpp Sub.h Sub.cpp Plus.h Plus.cpp Multiply.h Multiply.cpp Constant.h Constant.cpp
OBJ = main.o Operator.o
%.o: %.cpp $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main: $(OBJ)
	g++ -o $@ $^ $(CFLAGS)

clean:
	rm *.o
