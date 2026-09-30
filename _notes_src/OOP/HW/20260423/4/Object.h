#pragma once

class Splash;


#include <iostream>
#include <string>

using namespace std;

enum Direction {NONE, LEFT, RIGHT, UP, DOWN};
enum Actor {PLAYER, WATER, TOXIC};

struct Dir{
	int x,y;
	Direction dir;
};
extern Dir DIRE[4];

class Object {
protected:
	Splash* splash;
	int x, y;
public:
	virtual int act(Direction fromwhere, Actor fromwho) = 0;
	virtual ~Object() {}
};

class Water : public Object {
	int value;
	public:
		Water(int,int,int,Splash *);
		int act(Direction fromwhere, Actor fromwho);
};

class Void : public Object {
	// TODO
	public:
	Void(int,int,Splash *);
	int act(Direction fromwhere, Actor fromwho);
};

class Barrier : public Object {
	// TODO
	public:
	Barrier(int,int,Splash *);
	int act(Direction fromwhere, Actor fromwho);
};

class Toxic : public Object {
	int value;
	// TODO
	public:
	Toxic(int,int,int,Splash *);
	int act(Direction fromwhere, Actor fromwho);
};
