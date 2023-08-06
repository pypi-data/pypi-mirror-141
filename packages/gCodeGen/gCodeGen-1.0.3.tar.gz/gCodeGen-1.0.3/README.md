# gCodeGen

## Description
This package provides a super simple domain language, which can be used for the generation of G-Code. The main occasion for such a language was that the supported G-Code syntax greatly differs between implementations. Some do not even allow the use of variables or control flow constructs such as loops and if statements. gCodeGen introduces a simple language, which syntactically is pretty similar to python code with a few distinct differences, and of course, a very limited feature set.
It's important to understand that gCodeGen is only a convenient way to write a more extensive G-code file. Thus compilation must resolve all variables to concrete numbers. By restricting on a basic subset of common G-code commands gCodeGen strives to support any kind of G-code implementation.

## Installation
> pip install -m gCodeGen

## Import and usage
For generation of G-Code from an input file use:
```
from gCodeGen import gCodeGen
gCodeGen.generate("inputFileName")
```
To test gCodeGen interactively use:
```
gCodeGen.shell()
```

## Basics of gCodeGen
Comments, like in python, start with a '#' symbol and go until the end of the line:
```
# This is a comment
```

A standard line of G-code will unchangedly be copied into the output file:
```
G0 X100 Y200 Z0
```
Variables must be declared with the 'var' keyword and variable names must be all lower case! Underscores are allowed.
```
var cycle_counter = 0
```
The initialization of the variable is optional. An assignment to a variable can happen any time after its declaration.
```
var my_x
my_x = 2.5
```
Numbers are either intergers without decimal point, or floats. A float can begin, but must not end with a decimal point:
```
var my_y
my_y = .5  # is okay
my_y = 5.  # not allowed!
```
Calculations can be done as expected:
```
var mean = (my_x + my_y) / 2
```
After intialization variables can be used within G-code by simply putting them right behind the corresponding coordinate. Mixing with static values is okay.
```
G0 Xmy_x Ymy_y Z0 F5000
```
So the above will evaluate to 'G0 X2.5 Y0.5 Z0 F5000' in the output file.


## Control Flow
There are only two control flow statements. The first is a 'if' statement which is similar to python syntax. However gCodeGen does not care about indentation, but uses the keyword 'end' to mark the end of a block. So indentation is merely a matter of structuring your code but doesn't alter its meaning. Bool values behave the same way they do in python.
```
var start = True

if start:
    G0 Z0
end
```

Bools can be negated using '!':
```
var not_true = !True
```

Else statements work in a similar fashion. Note that the colon at the end of if and else is mandatory.
```
var speed = 5

if speed > 0:
    G0 X0 Y0 Z0 Fspeed
else:
    speed = speed + 1
end
```
The other control mechanism is the 'repeat' statement. Its similar to a for loop without the index variable. It starts with the keyword 'repeat' followed by a number. If the number is a float it will be rounded to the closest integer. The statements within the body of repeat statement will then be looped over this many times:
```
var times = 10
var my_z = 100

repeat times:
    G0 Zmy_z
    my_z = my_z - 10
end
```
This will output the G-code line 10 times into the output file. Of course you can mix control flow statements. To structure your output code, you can also use 'print' statements. If you are familiar with Rust thats how print statements work. To print variables we simply put some placeholders '{}' into the text and after on specify the variables in the order they should be injected.
```
var one = 1
var two = 2
print("{} wrongs don't make {} right!", two, one)
```
For more example code and its respective output have a look at the companion [github repo](https://github.com/WebiusD/gCodeGenerator).
