:- discontiguous padre/2.
:- discontiguous madre/2.

% Hechos

% Nivel 1
padre(bregor, beor).

% Nivel 2
padre(beor, barahir).
padre(beor, bregolas).

% Nivel 3
padre(barahir, beren).
madre(emeldir, beren).

padre(bregolas, belegund).
padre(bregolas, baragund).

% Nivel 4
padre(beren, dior).
madre(luthien, dior).

padre(belegund, rian).

padre(baragund, morwen).

% Nivel 5
padre(dior, elwing).
madre(nimloth, elwing).

padre(huor, tuor).
madre(rian, tuor).

padre(hurin, turin).
madre(morwen, turin).

padre(hurin, nienor).
madre(morwen, nienor).

% Nivel 6
padre(tuor, earendil).
madre(idril, earendil).

% Nivel 7
padre(earendil, elrond).
madre(elwing, elrond).

padre(earendil, elros).
madre(elwing, elros).

% Reglas

hijo(X, Y) :- padre(Y, X).
hijo(X, Y) :- madre(Y, X).

hermano(X, Y) :-
    (padre(P, X), padre(P, Y);
     madre(M, X), madre(M, Y)),
    X \= Y.

tio(X, Y) :- padre(P, Y), hermano(X, P).
tio(X, Y) :- madre(M, Y), hermano(X, M).

tia(X, Y) :- padre(P, Y), hermano(X, P).
tia(X, Y) :- madre(M, Y), hermano(X, M).

ancestro(X, Y) :- padre(X, Y).
ancestro(X, Y) :- madre(X, Y).
ancestro(X, Y) :- padre(X, Z), ancestro(Z, Y).
ancestro(X, Y) :- madre(X, Z), ancestro(Z, Y).

descendiente(X, Y) :- ancestro(Y, X).

