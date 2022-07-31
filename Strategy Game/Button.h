#pragma once
#include <string>
#include "UI.h"

class Button : public UI
{
public:
    Button(std::string n, float v[4]);
public:
    bool pressed(float x, float y);
};

