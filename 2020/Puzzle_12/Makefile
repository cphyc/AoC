all: test

solve: solve.cpp
	g++ -Wall -std=c++20 -O3 solve.cpp -o solve

test: solve
	./solve

clean:
	rm solve
