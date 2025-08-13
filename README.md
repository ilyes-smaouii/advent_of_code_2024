# advent_of_code_2024

## Intro/context
Decided to have a crack at the 2024 edition of Advent of Code, albeit a little late. \
Also a good opportunity for me to add some stuff to my GitHub profile, as I haven't used it much since its creation.

## Journal/Misc
- 2025/08/09 : Was going to do it in C++, but I figured it'd be quicker to code in Python.
Might switch back to C++ later, if I feel like it. 
- 2025/08/11 : Currently stuck on part 2 of day 5. This one feels like it might be quite complex.
- 2025/08/12 : Just went for a search online and found out about topological sorting, this might help me with task 05.2\
Kahn's algorithm for topological sorting seems interesting. Doesn't give a unique solution though, so I'm still a little
confused with the way we're supposed to go about this. Unless the people who made this exercise made sure it had
only one solution.\
Update : finally worked it out ! I couldn't use Kahn's algorithm as is on the set of all rules,
as there would be inconstencies that way.
Instead, I had to use it for each update, every time restricting the set of rules to the ones relevant to the current udpate.
It also seems the rules have been made such that, for every update, and using only the rules pertaining to that update,
the ordering would be total (I'm assuming, anyway, since I got the right answer).\
I'll clean up the code and move on to Day 6.
- 2025/08/13 - Currently thinking about part. 2 of Day 6. I already have an algorithm that could work in theory,
but it just takes too much time to compute, so I'm trying to think of a more efficient one.\
Update : found one that actually finished in less than like 30 seconds, but it still feels slow.
Will try finding a more efficient way.\
Update : leaving it like this for now, I'm spending too much time on this
