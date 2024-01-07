# cuatro
A game of falling blocks where the number four is key. In case you ask, yes, it is a clone of Tetr!s, but due to copyright law, this tribute to one of the great classics of computer gaming had to be renamed. With this project I seek no commercial value and I think it won't affect the profits of the big owner corporation even by half a bees.. hair.

## TL;DR - How to run this game?

* Make sure you're using a modern version of Python (Python3.11.6 at the time of publication)
* Install pygame - this will depend on how your system (different flavours of Linux, MacOS) deals with Python packages [Will update with specific instructions].
* From the root folder of the repo, run 
```
python cuatro
```


## Preface (before you criticise my code)

This is the third rewrite this game has had since I've started it. As my programming skills grow, I realise it can be re-structured in better ways. I'm sure there are lots of improvements this game can receive, and I know there will always be something to "criticise" about its code or its design. I welcome all constructive feedback I can get. Besides, this is something I chose to do to kill time; something I think may be more fun than playing Solitaire while teaching me something in the process.

"Better code" is relative to who reads this. I've learned to code away from the software industry, and I started about 25 years ago. Back then I was always seeking to learn the most __efficient__ forms of code, thinking it would be so cool for developing games, which lead me to learning C and x86 Assembly.

Although I've abandoned low level programming in favour of web development, I've been always a minimalist, seeking to solve my problems with as little dependencies as possible. By dependencies, I mean libraries and frameworks.

The only dependency besides the modules that come with Python is Pygame (https://www.pygame.org/) and its inevitable sub-dependencies.

## Overview

Logically, the code has been divided in two main modules: a __front end__ and a __back end__.

The front end takes care of displaying graphics and managing events like keyboard, screen resize, timers, etc.

The back end is the __engine__ of the game. For each step (triggered by a timer), the engine recalculates its state, updating the existing blocks, updating the position of the falling shape, updating its score, like a big state machine.

The front end and back end are connected through an __event_bus__. This event bus it's an instance of a class that follows the __Pub-Sub__ model, where any part of the code can publish some data to a named event. Publishing this data does nothing at all. If other parts of the code require this published data they can subscribe a callback function that receives this data for a particular event.

By both the front end and back end having access to the same event bus and knowing what data format to expect from each subscription, these two logical parts of the game don't have to know anything about the other part.

## Future improvements and changes

I intend to create a completely different front end that follows the same data communication, just to prove it can be done without modifying anything on the back end side.

With less priority, I may create a more elaborate system of levels to make the game more challenging, and who knows, turn it into a multi player game (a 2 player game).

## Resources used

As mentioned in my preface, I try to use as little external code or assets as practicable.

The design and drawing of the frames and blocks were all done by myself using GIMP (https://www.gimp.org).

The fonts were downloaded from Fonts101 (https://fonts101.com). I tried to get more information about the licensing of these fonts and all I can read is that they're good for non-commercial use.

As for the sounds, I have no information to where these came from.

As an exercise of independence, there are tools to create all of the above. Don't think I will? - Stay tuned.

That's all - Enjoy
