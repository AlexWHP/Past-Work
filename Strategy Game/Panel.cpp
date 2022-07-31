#include "Panel.h"

Panel::Panel(std::string n, float v[4]) : UI(n, v) {}

std::string Panel::pressed(float x, float y)
{
	// Fixing x and y for coordinates
	if (Panel::clicked(x, y))
	{
		// Conversion from width of panel in frame to within panel
		x = (x - vertices[0]) / vertices[2];
		y = (y - vertices[1]) / vertices[3];
		/*
		for (int i = 0; i < sub_panels.size(); i++)
		{
			sub_panels[i].pressed(x, y, width_pan, height_pan);
		}
		*/
		for (int i = 0; i < buttons.size(); i++)
		{
			if (buttons[i].pressed(x, y))
			{
				return buttons[i].name;
			}
			buttons[i].pressed(x, y);
		}
		return name;
	}
	return "";
}