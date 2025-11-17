#const dup = 1.

#defined data/1.
#defined drop/1.

% Ignore redundant data point.
data(node(X)) :-
    data(node(X,_)).

% Keep available vehicles.
keep(vehicle(V,C)) :-
    data(vehicle(V,C)),
    keep(available(V,_,_)).

% Adjacent kept nodes for given vehicle.
next(X,Y,V) :-
    data(vehicle(V,_)),
    data(arc(Y,X,V,_,_)),
    data(node(X)),
    data(node(Y)),
    not drop(node(X)),
    not drop(node(Y)).

% Vehicle can close cycle containing this edge.
cyclable(X,Y,V) :- next(X,Y,V).
cyclable(X,Y,V) :- next(Z,Y,V), cyclable(X,Z,V).

% Keep arcs that can be cycled through.
keep(arc(X,Y,V,C,D)) :-
    data(arc(X,Y,V,C,D)),
    cyclable(X,Y,V).

% Keep nodes if outgoing arcs are retained.
keep(node(X)) :-
    data(node(X)),
    keep(arc(X,_,_,_,_)).

% First non-dropped step.
start(S) :-
    S = #min {
        B :
            data(month(M,B,_)),
            not drop(month(M,_,_))
    }.

% Months retained and steps start counting at zero.
keep(month(N,B-S,E-S)) :-
    data(month(M,B,E)),
    not drop(month(M,B,E)),
    start(S),
    N = #count {
        X :
            data(month(_,X,_)),
            not drop(month(_,X,_)),
            X-S < B-S
    }.

% Derive available steps and subtract dropped steps.
available(V,N-S) :-
    start(S),
    data(available(V,B,E)),
    keep(month(_,I,_)),
    keep(month(_,_,J)),
    N-S >= I,
    N-S <= J,
    N = B..E.

% Retain relevant availabilities.
keep(available(V,B,E)) :-
    available(V,B),
    available(V,E),
    not available(V,B-1),
    not available(V,E+1),
    available(V,N) :
        N = B..E;
    B <= E.

% Retain demand if nodes kept and month not dropped.
keep(demand(I,X,Y,N,Q,R,F,T)) :-
    data(demand(I,X,Y,M,Q,R,F,T)),
    keep(node(X)),
    keep(node(Y)),
    start(S),
    keep(month(N,B-S,E-S)),
    data(month(M,B,E)),
    not drop(month(M,B,E)),
    not drop(demand(I,X,Y,M,Q,R,F,T)).

% Enforce disjoint availabilities.
 :- data(available(V,S,E)),
    data(available(V,X,_)),
    S < X,
    E > X.

% Contiguous months share their last and first steps.
 :- keep(month(M,_,E)),
    not keep(month(_,E,_)),
    1 {
        keep(month(N,_,_)) :
            N > M
    }.

% Steps ascend.
 :- keep(month(_,S,E)),
    S > E.

% Duplicate nodes.
copy(node(@append_letter(X,1..dup,dup))) :-
    keep(node(X)).

% Duplicate vehicles.
copy(vehicle(@append_letter(V,1..dup,dup),C)) :-
    keep(vehicle(V,C)).

% Duplicate vehicle availabilities.
copy(available(@append_letter(V,1..dup,dup),B,E)) :-
    keep(available(V,B,E)).

% Months never duplicated.
copy(month(M,B,E)) :-
    keep(month(M,B,E)).

% Duplicate arcs.
copy(arc(@append_letter(X,I,dup),@append_letter(Y,I,dup),@append_letter(V,I,dup),C,D)) :-
    keep(arc(X,Y,V,C,D)),
    I = 1..dup.

copy(demand(@append_letter(I,J,dup),@append_letter(X,J,dup),@append_letter(Y,J,dup),N,Q,R,F,T)) :-
    keep(demand(I,X,Y,N,Q,R,F,T)),
    J = 1..dup.

#show copy/1.
