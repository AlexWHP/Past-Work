#include "UI.h"

UI::UI(std::string n, float v[4])
{
	name = n;
	// Needs to be initialised as this as the original object is destroyed
	vertices[0] = v[0];
	vertices[1] = v[1];
	vertices[2] = v[2];
	vertices[3] = v[3];
}
bool UI::clicked(float x, float y)
{
	// Designed for square UI objects
	if (active)
	{
		// Evaluates if within vertices
		if ((x >= vertices[0] && x <= vertices[0] + vertices[2]) && (y >= vertices[1] && y <= vertices[1] + vertices[3]))
		{
			return true;
		}
	}
	return false;
}
void UI::setBuffers(unsigned int b[3])
{
	buffers[0] = b[0];
	buffers[1] = b[1];
	buffers[2] = b[2];
}