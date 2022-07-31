#pragma once
#include <string>
// User interface (Parent of all UI displayed items)
class UI
{
public:
	UI(std::string n, float v[4]);
	std::string name;
	float vertices[4];
	unsigned int buffers[3];
	// v[0] left, v[1] bottom, v[2] width, v[3] height
private:
	bool active = true;
public:
	bool clicked(float x, float y);
	void setBuffers(unsigned int b[3]);
};

