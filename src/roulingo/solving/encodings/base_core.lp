#include "base_aux.lp".

% Optionally start first step each availability.
{
    occurs(start(V,X),S) :
        accessible(X,V),
        origin(I,X),
        open(I,S)
} 1 :-
    available(V,S,_).

% Choose next destination until availability elapses.
{
    occurs(go(V,X,Y),S) :
        duration(V,X,Y,D),
        available(V,B,E),
        B <= S,
        E >= S+D+1
} = 1 :-
    holds(at(V,X),S),
    1 {
        duration(V,X,_,D) :
            available(V,B,E),
            B <= S,
            E >= S+D+1
    }.

% Deliver to destination.
occurs(drop(V,I),S) :-
    destination(I,X),
    holds(at(V,X),S),
    holds(has(V,I,_),S-1).

% Derive start position.
holds(at(V,X),S) :-
    occurs(start(V,X),S).

% Arrive at destination.
holds(at(V,Y),S+D+1) :-
    occurs(go(V,X,Y),S),
    duration(V,X,Y,D).

% Initial steps until transit elapses.
holds(has(V,I,T+1),S) :-
    transit(I,T),
    occurs(load(V,I),S).

% Transit steps decrease if not delivered.
holds(has(V,I,T-1),S) :-
    holds(has(V,I,T),S-1),
    not occurs(drop(V,I),S),
    step(S),
    T > 0.

% Opening expiry steps.
holds(due(I,F),S) :-
    opens(I,S),
    frequency(I,F).

% Loading resets expiry steps.
holds(due(I,F),S) :-
    frequency(I,F),
    open(I,S),
    holds(due(I,_),S-1),
    occurs(load(_,I),S).

% Expiry steps decrease if not loaded.
holds(due(I,F-1),S) :-
    open(I,S),
    holds(due(I,F),S-1),
    not occurs(load(_,I),S),
    F > 0.

% Expiry persists until unavailable.
holds(due(I,0),S) :-
    open(I,S),
    holds(due(I,0),S-1).

% One vehicle per node each step.
 :- holds(at(A,X),S),
    holds(at(B,X),S),
    A != B.

% Traversal cannot violate transit constraints.
 :- holds(has(V,_,T),S),
    occurs(go(V,X,Y),S),
    duration(V,X,Y,D),
    T-1 < D.

% No loading after frequency expires.
 :- occurs(load(_,I),S),
    holds(due(I,0),S).

% Nothing in transit at horizon.
 :- holds(has(_,_,_),horizon).

% Cargo transit steps never elapse.
 :- holds(has(_,_,0),_).

#show occurs/2.

#program opt.

% Optionally load at origin.
{
    occurs(load(V,I),S) :
        origin(I,X),
        open(I,S)
} :-
    holds(at(V,X),S).

#program req.

% Load if not delivering.
1 {
    occurs(load(V,I),S) :
        origin(I,X),
        open(I,S)
} :-
    holds(at(V,X),S),
    not occurs(drop(V,_),S).

% Optionally load if delivering.
{
    occurs(load(V,I),S) :
        origin(I,X),
        open(I,S)
} :-
    holds(at(V,X),S),
    occurs(drop(V,_),S).
