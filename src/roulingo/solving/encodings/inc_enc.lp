#include "inc_core.lp".

#program inc(index).

% Avoid load frequency expiration.
 :~ holds(due(I,0),S),
    step(S,index). [1@1,I,S]

#program cost(index).

% Mitigate traversal costs.
 :~ occurs(go(V,X,Y),S),
    cost(V,X,Y,C),
    step(S,index). [C,V,S]
