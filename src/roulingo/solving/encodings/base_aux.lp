step(0..horizon).

% Steps categorised into periods.
step(S,P) :-
    step(S),
    P = #max {
        N :
            month(N,B,E),
            B <= S <= E
    }.

% Vehicle.
vehicle(V) :-
    vehicle(V,_).

% Vehicle capacity.
capacity(V,C) :-
    vehicle(V,C).

% Nodes accessible to vehicle.
accessible(X,V) :-
    arc(_,X,V,_,_),
    arc(X,_,V,_,_).

% Vehicle availability steps.
available(V,B..E) :-
    available(V,B,E).

% Directed arc for vehicle.
arc(V,X,Y) :-
    arc(X,Y,V,_,_).

% Vehicle arc traversal cost.
cost(V,X,Y,C) :-
    arc(X,Y,V,C,_).

% Vehicle arc traversal duration steps.
duration(V,X,Y,D) :-
    arc(X,Y,V,_,D).

% Opening step.
opens(I,B) :-
    demand(I,_,_,M,_,_,_,_),
    month(M,B,_).

% Closing step.
closes(I,E) :-
    demand(I,_,_,M,_,_,_,_),
    month(M,_,E).

% Every step available for loading.
open(I,B..E) :-
    opens(I,B),
    closes(I,E).

% Origin node.
origin(I,X) :-
    demand(I,X,_,_,_,_,_,_).

% Destination node.
destination(I,Y) :-
    demand(I,_,Y,_,_,_,_,_).

% Required load frequency.
frequency(I,F) :-
    demand(I,_,_,_,_,_,F,_).

% Transit step bound.
transit(I,T) :-
    demand(I,_,_,_,_,_,_,T).

% Total units available.
quantity(I,Q) :-
    demand(I,_,_,_,Q,_,_,_).

% Revenue per unit delivered.
revenue(I,R) :-
    demand(I,_,_,_,_,R,_,_).
