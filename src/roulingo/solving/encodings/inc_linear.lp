#include "inc_core.lp".

#program inc(index).

% Todo: externals?

% Total loads cannot exceed quantity available.
&sum{
   occurs(load(V,I,R),S) :
      open(I,S),
      available(V,S),
      step(S,index)
} <= Q
:- quantity(I,Q),
   revenue(I,R).

% Loaded quantities cannot exceed vehicle capacity.
&sum{holds(has(V,I),S) : open(I,S)} <= C :-
   capacity(V,C),
   available(V,S),
   step(S,index).

% Nothing loaded unless action executed.
&sum{occurs(load(V,I,R),S)} = 0 :-
   open(I,S),
   revenue(I,R),
   available(V,S),
   step(S,index),
   not occurs(load(V,I),S).

% Load positive quantity.
&sum{occurs(load(V,I,R),S)} > 0 :-
   occurs(load(V,I),S),
   revenue(I,R),
   step(S,index).

% Have previous step quantity plus current step load quantity until delivered.
&sum{
   occurs(load(V,I,R),S) :
      open(I,S);
   holds(has(V,I),S-1) : % Not necessarily this index.
      open(I,S-1),
      available(V,S-1)
} = holds(has(V,I),S)
:- available(V,S),
   opens(I,O),
   closes(I,C),
   transit(I,T),
   revenue(I,R),
   O <= S <= C+T,
   step(S,index),
   not occurs(drop(V,I),S).

% Deliver everything.
&sum{holds(has(V,I),S)} = 0 :-
   occurs(drop(V,I),S),
   step(S,index).

% Revenue for quantity delivered.
&minimize{
   -R*occurs(load(V,I,R),S) :
      open(I,S),
      available(V,S),
      revenue(I,R),
      step(S,index)
}.

&show{
   occurs(load(V,I,R),S) :
      open(I,S),
      available(V,S),
      revenue(I,R),
      step(S,index)
}.

#program cost(index).

% No traversal cost outside action step.
&sum{occurs(go(V),S)} = 0 :-
   available(V,S),
   step(S,index),
   not occurs(go(V,_,_),S).

% Record traversal cost for objective.
&sum{occurs(go(V),S)} = C :-
   occurs(go(V,X,Y),S),
   cost(V,X,Y,C),
   step(S,index).

% Traversal costs.
&minimize{
   occurs(go(V),S) :
      available(V,S),
      step(S,index)
}.

&show{
   occurs(go(V),S) :
      available(V,S),
      step(S,index)
}.