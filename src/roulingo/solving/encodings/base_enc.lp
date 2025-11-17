#include "base_core.lp".

% Avoid load frequency expirations.
 :~ holds(due(I,0),S). [1@1,I,S]

#program cost.

% Mitigate costs.
 :~ occurs(go(V,X,Y),S),
    cost(V,X,Y,C). [C,V,S]
