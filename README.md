# advent_of_code_2024

## Intro/context
Decided to have a crack at the 2024 edition of Advent of Code, albeit a little late. \
Also a good opportunity for me to add some stuff to my GitHub profile, as I haven't used it much since its creation.

## Journal/Misc
### 2025/08/09
Was going to do it in C++, but I figured it'd be quicker to code in Python.
Might switch back to C++ later, if I feel like it. 
### 2025/08/11
Currently stuck on part 2 of day 5. This one feels like it might be quite complex.
### 2025/08/12
Just went for a search online and found out about topological sorting, this might help me with task 05.2\
Kahn's algorithm for topological sorting seems interesting. Doesn't give a unique solution though, so I'm still a little
confused with the way we're supposed to go about this. Unless the people who made this exercise made sure it had
only one solution.\
Update : finally worked it out ! I couldn't use Kahn's algorithm as is on the set of all rules,
as there would be inconstencies that way.
Instead, I had to use it for each update, every time restricting the set of rules to the ones relevant to the current udpate.
It also seems the rules have been made such that, for every update, and using only the rules pertaining to that update,
the ordering would be total (I'm assuming, anyway, since I got the right answer).\
I'll clean up the code and move on to Day 6.
### 2025/08/13
Currently thinking about part. 2 of Day 6. I already have an algorithm that could work in theory,
but it just takes too much time to compute, so I'm trying to think of a more efficient one.\
Update : found one that actually finished in less than like 30 seconds, but it still feels slow.
Will try finding a more efficient way.\
Update : leaving it like this for now, I'm spending too much time on this. Plus I gotta sleep.
### 2025/08/15
Got a little busy these days with other stuff, so I haven't done much, might have more time this weekend
### 2025/08/17
Finished day 9.\
Added some stuff in helpers.py, cause why not.
### 2025/08/18
Spent a lot of time on day 10 part 1 using a lot of wrapper and helper stuff I've added to helpers.py, but
I ended up with some pretty unnecessarilty complex code, and the answer was wrong. I tried to ditch the object-oriented, elegant
approach and rewriting my code to be much simpler, with a more direct approach, but I just ended up with the exact same result.
At this point, I wonder if I haven't just misread the instructions.\
Update : turns out the iterator class I had constructed for iterating over tables wasn't properly coded, and missed the very first
cell of the table, which made me miss the correct solution by 2. I found a way to make it work, but for the sake of simplicity,
the current version of the code doesn't use it anymore.
Part 2 was pretty easy once I was done with part 1. \
Finished Day 10 ! \
Update : finished Day 11 too ! Turns out part 2 was pretty simple. I just changed the mechanics a bit and replaced the use of lists
with the use of sets, and the program ran much - much - faster.
### 2025/08/20
Currently stuck on day 12 part 2. My algorithm works by counting corners, but I realized it doesn't account for 
"inwards" corners, and I can't figure out a simple way to account for them.\
Update : figured it out, and it took 7 additional lines of code, which accounted for close to half of the corresponding function,
but was still less than I feared it would be. Moving on to Day 13.\
Update : just read the instructions for part 1 of Day 13. At first glance, this feels somewhat simple but also like it could take\
quite a bit of code to achieve it. First step is parsing the input, which is I don't like thinking about too much.\
Update : realized halfway through part 2 of day 13 that there's not such thing as a "mininmum cost" unless the coefficients for A\
and B happen to be exactly proportional. Just did a quick test, and this doesn't happen for any machine in the input. Don't know if
I should incorporate this assumption in my code, or make it as agnostic to input.\
Update : made the code agnostic (in theory, anyway), and finally managed to solve Day 13. Won't look at Day 14's instructions
for now, because if I do, I might not be able to move on to something else until I've solved it. I had other things to do today
which I didn't do because I got too busy with this.\
### 2025/08/21
Finished Day 14, which turned out easier than I expected - especially part 2, although the approach was a bit unorthodox.
Even had to change the font size for my shell.\
Update : after some discussions with friends who have already attempted AoC, I've confirmed what I was starting to suspect : unlike
what I initially thought, AoC exercises aren't gonna be the type I can solve in just one hour. In fact, I've spend several hours on
each of them almost every time, for the past several days. Considering this was kind of meant as a side quest, I might decide to
slow down a little for the coming days, so I can free some time for other stuff I have to do.