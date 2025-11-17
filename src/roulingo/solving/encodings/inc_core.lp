#include "base_aux.lp".

#program inc(index).

% Respect actions during previous periods.
occurs(X,S) :-
    occurred(X,S),
    step(S,index).

% Input vehicle starting positions.
#external occurred(start(V,X),S) :
    accessible(X,V),
    available(V,S,_),
    step(S,index).

% Optionally start first step each availability.
{
    occurs(start(V,X),S) :
        accessible(X,V),
        origin(I,X),
        open(I,S)
} 1 :-
    available(V,S,_),
    step(S,index).

% Input traversals.
#external occurred(go(V,X,Y),S) :
    available(V,S),
    duration(V,X,Y,D),
    step(S,index).

% Choose next destination until availability elapses.
{
    occurs(go(V,X,Y),S) :
        duration(V,X,Y,D),
        available(V,B,E),
        B <= S,
        E >= S+D+1
} = 1 :-
    holds(at(V,X,_),S),
    step(S,index),
    1 {
        duration(V,X,_,D) :
            available(V,B,E),
            B <= S,
            E >= S+D+1
    }.

% Deliver to destination.
occurs(drop(V,I,index),S) :-
    holds(at(V,X,index),S),
    holds(has(V,I,_,index),S-1),
    destination(I,X).

% Derive start position.
holds(at(V,X,index),S) :-
    occurs(start(V,X),S),
    step(S,index).

% Arrive at destination.
holds(at(V,Y,index),S+D+1) :-
    occurs(go(V,X,Y),S),
    duration(V,X,Y,D),
    step(S,index).

% Initial steps until transit elapses.
holds(has(V,I,T+1,index),S) :-
    occurs(load(V,I),S),
    transit(I,T),
    step(S,index).

% Transit steps decrease if not delivered.
holds(has(V,I,T-1,index),S) :-
    holds(has(V,I,T,index),S-1),
    not occurs(drop(V,I,index),S),
    T > 0.

% Opening expiry steps.
holds(due(I,F),S) :-
    opens(I,S),
    frequency(I,F),
    step(S,index).

% Loading resets expiry steps.
holds(due(I,F),S) :-
    frequency(I,F),
    open(I,S),
    holds(due(I,_),S-1),
    occurs(load(_,I),S),
    step(S,index).

% Expiry steps decrease if not loaded.
holds(due(I,F-1),S) :-
    open(I,S),
    holds(due(I,F),S-1),
    not occurs(load(_,I),S),
    step(S,index),
    F > 0.

% Expiry persists until unavailable.
holds(due(I,0),S) :-
    open(I,S),
    holds(due(I,0),S-1),
    step(S,index).

% Input loads.
#external occurred(load(V,I),S) :
    open(I,S),
    available(V,S),
    step(S,index).

#program opt(index).

% Load at origin.
{
    occurs(load(V,I),S) :
        origin(I,X),
        open(I,S)
} :-
    holds(at(V,X,_),S),
    step(S,index).

#program req(index).

% Load if not delivering.
1 {
    occurs(load(V,I),S) :
        origin(I,X),
        open(I,S)
} :-
    holds(at(V,X,_),S),
    not occurs(drop(V,_,_),S),
    step(S,index).

% Optionally load if also delivering.
{
    occurs(load(V,I),S) :
        origin(I,X),
        open(I,S)
} :-
    holds(at(V,X,_),S),
    occurs(drop(V,_,_),S),
    step(S,index).

% Only cross boundary to deliver.
 :- holds(at(V,_,index),S),
    not step(S,index),
    not occurs(drop(V,_,index),S).

#program base.

% One vehicle per node each step.
 :- holds(at(A,X,_),S),
    holds(at(B,X,_),S),
    A != B.

% Traversal cannot violate transit constraints.
 :- holds(has(V,_,T,_),S),
    occurs(go(V,X,Y),S),
    duration(V,X,Y,D),
    T-1 < D,
    step(S).

% Nothing in transit at horizon.
 :- holds(has(_,_,_,_),horizon).

% Transit steps never elapse.
 :- holds(has(_,_,0,_),_).

% No loading after frequency expires.
 :- occurs(load(_,I),S),
    holds(due(I,0),S),
    step(S).

#show occurs/2.
