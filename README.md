KonamiCode: A BrainF-like esoteric programming language that can be written with a game controller

Commands:
*	^: Get the value at the current address [i.e. <<(^))]
*	v[value]: Save the passed value to the current address
*	\>[address]: Set the current address pointer
*	<: Gets the current address pointer [i.e. <<(<))]
*	<<: Output the current address’s value to the console (as ASCII)
*	\>\>: Gets a value from the console and saves it to the current address
*	L: A marker for A and B 
*	A: If the current address is equal to the value in the comparison buffer, skip ahead until the next L symbol and continue from there
*	B: If the current address is not equal to the value in the comparison buffer, back up until the next L symbol and continue from there
*	S[value]: Sets the comparison buffer
*	( and ): Start and end a number (see below)
*	[ and ]: The text inside them is a comment
*	Spaces and linebreaks are both ignored. Other characters are not allowed.

Numbers:
*	Start with a (
*	Repeat the ^ symbol as many times as needed for that base
*	Use the > symbol to go to the next base
*	Special numbers:
o	((>)) and ((<)) are special numbers that essentially mean increment and decrement. Note the double parenthesis. When passed to v, S, or >, they will increase/decrease their values by 1
o	For example, >((>)) will increase the current address pointer by 1
o	You can also change how much they increment/decrement. For example, >((>)^^>^) will increase the current address pointer by 21.
o	Do not confuse these with 0 (>)
o	((S)) represents the value of the comparison buffer
Examples: 
100 would be (^>>)
0 would be (>)
123 would be (^>^^>^^^)
5 would be (^^^^^)
12 would be (^>^^)

Hello world (with linebreaks and comments added for brevity):
```
v(^^^^^^^>^^) [writes 72 (or H) to address 0 in memory]
>((>)) [prints it]
v(^>>^) [writes 101 (or e) to address 1 in memory]
>((>)) [prints it]
v(^>>^^^^^^^^) [etc]
>((>))
v(^>>^^^^^^^^)
>((>))
v(^>^>^)
>((>))
v(^^^>^^)
>((>))
v(^>^>^^^^^^^^^)
>((>))
v(^>^>^)
>((>))
v(^>^>^^^^)
>((>))
v(^>>^^^^^^^^)
>((>))
v(^>>)
```
Without comments/linebreaks (142 characters):
```
v(^^^^^^^>^^)<<v(^>>^)<<v(^>>^^^^^^^^)<<v(^>>^^^^^^^^)<<v(^>^>^)<<v(^^^>^^)<<v(^>^>^^^^^^^^^)<<v(^>^>^)<<v(^>^>^^^^)<<v(^>>^^^^^^^^)<<v(^>>)<<
```