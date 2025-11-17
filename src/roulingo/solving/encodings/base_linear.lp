#include "base_core.lp".

% Total loads cannot exceed quantity available.
&sum {
    occurs(load(V,I),S) :
        open(I,S),
        available(V,S)
} <= Q :-
    quantity(I,Q).

% Loaded quantities cannot exceed vehicle capacity.
&sum {
    holds(has(V,I),S) :
        open(I,S)
} <= C :-
    capacity(V,C),
    available(V,S).

% Nothing loaded unless action executed.
&sum {
    occurs(load(V,I),S)
} = 0 :-
    open(I,S),
    available(V,S),
    not occurs(load(V,I),S).

% Load positive quantity.
&sum {
    occurs(load(V,I),S)
} > 0 :-
    occurs(load(V,I),S).

% Have previous step quantity plus current step load quantity until delivered.
&sum {
    occurs(load(V,I),S) :
        open(I,S);
    holds(has(V,I),S-1) :  % Not necessarily this index.
        open(I,S-1),
        available(V,S-1)
} = holds(has(V,I),S) :-
    available(V,S),
    opens(I,O),
    closes(I,C),
    transit(I,T),
    O <= S <= C+T,
    not occurs(drop(V,I),S).

% Deliver everything.
&sum {
    holds(has(V,I),S)
} = 0 :-
    occurs(drop(V,I),S).

% Revenue for quantity delivered.
&sum {
    R*occurs(load(V,I),S) :
        open(I,S),
        available(V,S),
        revenue(I,R)
} = revenue.

&minimize{
    -R*occurs(load(V,I),S) :
        open(I,S),
        available(V,S),
        revenue(I,R)
}.

#program cost.

% No traversal cost outside action step.
&sum {
    occurs(go(V),S)
} = 0 :-
    available(V,S),
    not occurs(go(V,_,_),S).

% Record traversal cost for objective.
&sum {
    occurs(go(V),S)
} = C :-
    occurs(go(V,X,Y),S),
    cost(V,X,Y,C).

% Total expenses.
&sum {
    occurs(go(V),S) :
        available(V,S)
} = expense.

&minimize {
    occurs(go(V),S) :
        available(V,S)
}.
