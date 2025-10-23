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
\
Update : finally worked it out ! I couldn't use Kahn's algorithm as is on the set of all rules,
as there would be inconstencies that way.
Instead, I had to use it for each update, every time restricting the set of rules to the ones relevant to the current udpate.
It also seems the rules have been made such that, for every update, and using only the rules pertaining to that update,
the ordering would be total (I'm assuming, anyway, since I got the right answer).\
I'll clean up the code and move on to Day 6.
### 2025/08/13
Currently thinking about part. 2 of Day 6. I already have an algorithm that could work in theory,
but it just takes too much time to compute, so I'm trying to think of a more efficient one.\
\
Update : found one that actually finished in less than like 30 seconds, but it still feels slow.
Will try finding a more efficient way.\
\
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
\
Update : turns out the iterator class I had constructed for iterating over tables wasn't properly coded, and missed the very first
cell of the table, which made me miss the correct solution by 2. I found a way to make it work, but for the sake of simplicity,
the current version of the code doesn't use it anymore.
Part 2 was pretty easy once I was done with part 1. \
Finished Day 10 ! \
\
Update : finished Day 11 too ! Turns out part 2 was pretty simple. I just changed the mechanics a bit and replaced the use of lists
with the use of sets, and the program ran much - much - faster.
### 2025/08/20
Currently stuck on day 12 part 2. My algorithm works by counting corners, but I realized it doesn't account for 
"inwards" corners, and I can't figure out a simple way to account for them.\
\
Update : figured it out, and it took 7 additional lines of code, which accounted for close to half of the corresponding function,
but was still less than I feared it would be. Moving on to Day 13.\
\
Update : just read the instructions for part 1 of Day 13. At first glance, this feels somewhat simple but also like it could take\
quite a bit of code to achieve it. First step is parsing the input, which is I don't like thinking about too much.\
\
Update : realized halfway through part 2 of day 13 that there's not such thing as a "mininmum cost" unless the coefficients for A
and B happen to be exactly proportional. Just did a quick test, and this doesn't happen for any machine in the input. Don't know if
I should incorporate this assumption in my code, or make it generic/agnostic to input.\
\
Update : made the code agnostic (in theory, anyway), and finally managed to solve Day 13. Won't look at Day 14's instructions
for now, because if I do, I might not be able to move on to something else until I've solved it. I had other things to do today
which I didn't do because I got too busy with this.\
### 2025/08/21
Finished Day 14, which turned out easier than I expected - especially part 2, although the approach was a bit unorthodox.
Even had to change the font size for my shell.\
\
Update : after some discussions with friends who have already attempted AoC, I've confirmed what I was starting to suspect : unlike
what I initially thought, AoC exercises aren't gonna be the type I can solve in just one hour. In fact, I've spent several hours on
each of them almost every time, for the past several days. Considering this was kind of meant as a side quest, I might decide to
slow down a little for the coming days, so I can free some time for other stuff I have to do.
### 2025/08/23
Finished Day 15 one or two days ago.
Currently wrote some code based the A-star algorithm to find the shortest path for part 1, but I haven't tested it yet.
Unless, by a miracle, it works on the first try - I haven't done a single test until now -
, I might just take another break - again, I've got things to do - and finish later.\
Update : couldn't resist, and spent some time trying to correct my - unsurprisingly - not working code.\
New update : I actually got it to work ?? I'd never even tried to implement A-star before, I actually expected it would take longer
to get it to work. The fix I fould should not have changed the result, though, so I'll try to investigate where I've made a mistake
before moving on to part 2.\
Update : turns out I misimplemented the A-star algorithm. Not sure why it still worked in specific conditions, but anyway.\
\
Update : got the solution to part 2 of Day 16 after a lot of trial-and-error, but the resulting code is really messy. Might
try to clean it up. (or just move on straight to Day 17 ?)
### 2025/08/24
Cleaned up Day 16, finished part 1 of Day 17, which felt pretty simple.\
Tried brute-force approach for part 2, but it doesn't seem to work (still running as I write this, currently at
iteration n°14600000).\
While it's still running I'll try to disassemble the program and understand what it does. This is actually my favorite type of problems -
open problem, simple description -, so I'm not complaining - not yet, anyway, though that might change if it turns out too complex.\
\
Update : figured out the disassembled code and put it in a function. Now I need to figure the function that can reverse that process, i.e.
take some "out" as input, and give me the corresponding initial value for register A .
### 2025/08/25
Finally figured out Day 17. I was on the right track, but I needed to tweak a few things, and correct some small - though impactful - mistakes.
While the final "core" code is less than 20 lines long, it required very precise handling of the variables,
and the different steps of the algorithms, along with awareness of a few subtle technicalities. The main idea's always been the same, but
it took me a lot of time to get it exactly right.\
Anyway, moving on.
### 2025/08/26
Finished Day 18. Part 1 was pretty straightforward, it just took me some time to snuff out some small mistakes I made -
e.g. a "<" instead of a ">" -, and then it worked pretty quickly. Same for part 2; I tried a brute appraoch, and when I saw it was too slow,
I just changed it to a dichotomic approach, which didn't take much to implement.\
Started looking at Day 19; I already have some idea for part 1, but depending on the data size I don't know if the program can finish
quickly enough. We'll see when I try.\
Part 1 of Day 19 was pretty straightforward, and part 2 seemed so too, but it turns out my initial recursive approach is too costly/complex.
Will have to figure out a better way to do this.\
Update : got some very rough idea centered around the use of a dictionary for each design. Will think some more about it, and try to implement.
Maybe later though, I've gotta go to sleep now.\
Update : figured out a new approach while I was riding the subway. I had some time + my laptop on me so I tried it, and it worked.\
Finished Day 19 !
### 2025/08/28
Kinda stuck on Day 20. First time this has happened on part 1 of any day, I think.\
\
Update : found a few approaches which are somewhat efficient (i.e. could run in one to a few hours, which is a pretty low bar). Both rely on a first
regular exploration, then try a cheat on each tile on that "regular" path. The second one uses the orginial path as a "hint", so it doesn't have to
re-do that part of the exploration if it stumbles on the original path.
While they are running, thinking about the 2nd approach made me realize there is a much better approach I didn't think of : explore the whole map from
the end to determine the minimum distance from each cell to the end, and then from each tile in that "cheatless" path, try each possible cheat, and
because you already know the distance to the end, you don't have to re-explore anything.\
I'll try to implement that now.\
Update : yup, that was it, that was the right appraoch, if only I'd thought of it earlier.\
Just read part. 2, and with the approach I found for part 1, I feel like part 2 should be pretty easy, and shouldn't require too much change in the code
from part 1. Will try later.\
Update : tried it while I was on the train; it was pretty straightforward, and it worked on the 1st try.\
\
Update : read Day 21's instructions, and thought about it a little, I'm not seeing a clear approach to follow here. I mean, there's a something I could
try, but I can't tell if it's the solution in theory. Plus I've been a little busy lately, so I haven't really put that much time into it. I'll try to
think about it more, but if I can't find anything better, maybe I'll just try that approach and see what results it yields.
### 2025/09/01
Needed some tweaking to find the right approach, and then it took me a lot of time to realize I'd made a small mistake by
lack of attention (a "<" replaced with a ">"). Once I'd found that out, I got the solution for part 1.
I tried to solve part 2 with a similar approach, only changing the number of "steps" taken, but it's not efficient enough, and takes too long.
Currently thinking of another approach with better complexity.\
Update : got an idea, will try to implement it and see if it works.\
### 2025/09/03
Idea didn't seem that good after doing a bit of digging. Thought about it for the past few days, and thought of another approach,
which I'll try to implement now. Well it's actually two approaches, but based on the same idea, but I'm not sure which one to pick exactly.
### 2025/09/05
Might be taking a break/slowing down for some time, I've got a few other things to take care of right now.
<br/>

### 2025/10/11 [back from the break !]
Been considering resuming this in the past few days, and today I decided to try to reason a little on paper while I was
on my way back from sport practice. This helped me get a clearer picture for Day 21, which I was stuck on, and giving
it a little more thought, I think I might have a hint. Will try to test/explore it and report back.\
Update : made a small test on some very small word, and it looks like I'm on the right track (:-O).

### 2025/10/13
After another smaller break cause I was a little busy, I came back to test my theory. It took me some time
to find how to implement the idea, then I realized it was still too inefficient, so I had to combine
it with some earlier idea I had for efficiency, and spent some time trying to implement that too.\
Then I tried, tried submitting the result, but it was "too low".\
I applied some changes to the code, until I - supposedly - got a result that seemed more correct, but it was
still too low.\
Btw, at some point during, I started tearing up at the thought I might be close to the solution after all the days
\- weeks ? - spent trying to find it.\
Anyway, it still wasn't the right result, so I still had to do some more digging.\
Turns out I forgot to "mutliply" the moves in my code (e.g. turn `"<^"` into `"<<^"`).\
Fixed that, ran my code again, got a new result, went to submit it online, and....\
YES ! A NEW GOLD STAR ! DAY 21 FINALLY FINISHED !\
I collapsed from sheer emotion, and had to take some time to recollect, but I can finally move on to something else !\
Honeslty at this point I'm not sure I have the wish or the will to even look at Day 22. Maybe I've endured enough
for today.\
Update : I was going to clean up my code, to remove all the useless code left over from my unsuccessful attempts,
but I feel like maybe I should just leave it there, as a sort of monument to the journey I went through (
which btw isn't even entirely in there, as I already removed some of the code I wrote during previous attempts
).\
Update : opened up page for Day 22 but I don't think I'll read it right before going to bed actually,
otherwise I might not be able to sleep.\
<br>
Update : I've just read Part 1 of Day 22, and it was pretty straightforward to solve. I even took time to make
a C++ version, which made it much faster. Currently reading Part 2.\
Update : just finished reading, and I feel like finishing this one in C++. First approach I'll try is the brute
approach, with the hope it's fast enough.

### 2025/10/14
It seems slow, but I feel like I could wait it out. The issue is, my code finds a price of 0 for every monkey,
so there's somethings wrong, but I haven't figured out what.\
Update : decided to write code that should be more efficient, even though I still haven't figured out what was
wrong previously. If I'm lucky, the - allegedly - more efficient code might also be correct.\
Update : realized my code wasn't correct, and now it's too slow (it's running as I write this, and might take
like an hour to finish)\
Update : tried submitting an intermediary result I had before the code finished running, and it was the right value !
Now I'll try to find that same value again, but in a more efficient/faster manner (I realized I could easily save a lot
of time by computing prices changes once at the beginning, whereas I'm doing the equivalent as many times as there are
negotiation arrays)\
Update : found slightly more efficient code (still very slow, it takes a few minutes to finish).\
Update : got some rough idea for an even more efficient code.\
Update : code runs a lot - a looot - faster, but result is now incorrect.\
Update : figured it out. Moving on to Day 23.

### 2025/10/15
Took my first look at Part 1 of Day 23, and seemed pretty straightforward, so I went straight to
implementing some ideas, but I didn't get it right right away, so I've gotta dig a little more.
Assuming I chose the right approach, it shouldn't take much longer, though.\
Update : I actually misread/misunderstood the instructions, so it's not as straightforward as I
thought.\

### 2025/10/16
Corrected my code for Part 1 of Day 23. Now trying to figure out Part 2.

### 2025/10/21
Been a little busy lately. I try to go back to Day 23 every now and then to think abouta potential
solution, but I can't find something that seems good, apart from the naive recursive approach, which
I feel would probably be too slow. But at this point, I think I'll just give it a try anyway.

### 2025/10/22
Update on previous entry : I'm currently running some "naive" code, and it is indeed taking too long.
As I initially felt, I'll probably need to be smart about the approach I take, if I want my code
to run in a timely manner.\
Update : nevermind, I took inspiration from some earlier Day, and by turning a `list` into a `set`,
the whole thing was a lot faster. Still somewhat slow, but fast enough for me to get a result, and
get my next gold star. I had to create a `HashableGroup` class for that, so I could create a
custom hash for my groups (i.e. sets of `string`'s).\
Update : tried running it all at once, which really highlighted how slow it still was. I could
probably try to figure out a better way to do this, but I've already found the solution,
and I'd rather just move on to the next Day.

### 2025/10/23
After putting it off for about a day, I read instructions for Part 1 of Day 24, and it actually looks
pretty straightforward, so I might just try it straight away.\
Update : yeah I got it. Moving on to Part 2, and praying this one doesn't just torture my mind for
several days.\
Update : just read the instructions for Part 2 of Day 24. Sounds really interesting, on a first read.
Hopefully, I can find some simple and elegant solution to this, and it doesn't take me too long.