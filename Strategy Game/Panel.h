#pragma once
#include "Button.h"
#include "UI.h"
#include <vector>

class Panel : public UI
{
public:
	Panel(std::string n, float v[4]);
public:
	//std::vector<Panel> sub_panels;
	std::vector<Button> buttons;
public:
	std::string pressed(float x, float y);
};

