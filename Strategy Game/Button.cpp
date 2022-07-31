#include "Button.h"

Button::Button(std::string n, float v[4]) : UI(n, v) {}

bool Button::pressed(float x, float y)
{
    if (Button::clicked(x, y))
    {
        return true;
    }
    return false;
}