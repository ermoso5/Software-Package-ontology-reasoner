%===================================
% INITIALIZATION
%===================================
:- use_module(library(semweb/rdf_db)).
:- use_module(library(semweb/rdfs)).
:- use_module(library(semweb/rdf_portray)).
loadprefix :- rdf_register_prefix(ontology, 'http://www.semanticweb.org/ontologies/2014/2/Ontology1395738954259.owl#').
:- loadprefix.
:- rdf_meta
	find_dependencies(r), find_recommends_atomic(r), find_suggestions_atomic(r), find_conflicts_atomic(r), transform(r).

%===================================
% HELPER FUNCTIONS
%===================================
transform(P, R) :- rdf_global_object(ontology:P, R).
flattener(D, LR, F) :- flatten(LR, R), subtract(R, D, S), append(D, S, F).
listAll(X) :- findall(Z,rdf(Z, rdf:type, owl:'NamedIndividual'), X).

%===================================
% FIND PACKAGE DEPENDENCIES
%===================================
find_dependencies(P,D) :- findall(Z,rdf_reachable(P,ontology:depends, Z), D).

%===================================
% FIND PACKAGE RECOMMENDATIONS
%===================================
find_recommends_atomic(P, R) :- findall(Z,rdf_reachable(P,ontology:recommends, Z), R).
find_recommends([], R, R).
find_recommends([D|T], Acc, LR) :- find_recommends_atomic(D,Temp), length(Temp,X),
				   X > 1 -> append(Acc,[Temp],R), find_recommends(T, R, LR);
					    find_recommends(T, Acc, LR).

%===================================
% FIND PACKAGE SUGGESTIONS
%===================================
find_suggestions_atomic(P, S) :- findall(Z,rdf(P, ontology:suggests, Z), S).
find_suggestions([], S, S).
find_suggestions([D|T], Acc, LS) :- find_suggestions_atomic(D,Temp), length(Temp, X),
				    X >= 1 ->  append([D],Temp,R1), append(Acc,[R1],R), find_suggestions(T, R, LS);
				               find_suggestions(T, Acc, LS).

%===================================
% FIND PACKAGE CONFLICTS
%===================================
find_conflicts_atomic(P, C) :- findall(Z,rdf(P, ontology:conflicts, Z), C).
find_conflicts([], C, C).
find_conflicts([D|T], Acc, LC) :- find_conflicts_atomic(D,Temp), length(Temp, X),
				  X >= 1 ->  append([D],Temp,R1), append(Acc,[R1],R), find_conflicts(T, R, LC);
					     find_conflicts(T, Acc, LC).

%===================================
% PRINTING
%===================================
printWarningList([]).
printWarningList([T]) :- transform(X, T), write(X), printWarningList([]).
printWarningList([H|T]) :- transform(X, H), write(X), write(', '), printWarningList(T).

sublist_check(_, [], S, S).
sublist_check(F, [H|T], Acc, R) :- member(H,F) -> append(Acc, H, NA), sublist_check(F, T, NA, R);
						  sublist_check(F, T, Acc, R).
checkWarning(_, [], W, W).
checkWarning(F, [[_|C2]|CT], Acc, W) :- sublist_check(F, C2, [], Temp), append(Acc, [Temp], R), checkWarning(F, CT, R, W).
issueWarning(D, LR, LS, LC) :- flattener(D, LR, F1), flattener(F1, LS, F2),  checkWarning(F2, LC, [], WT), flatten(WT, W),
	                       length(W, WL), WL >= 1 -> write('Warning: Relationship structure has an inconsistency. Packages '), printWarningList(W),
			                                 write(' are suggested/recommended by the package\n or any of the package dependencies, but they are also in conflict'),
							 write(' with the package or any of its dependencies.');
							 true.

printDependencies([]) :- write('.\n').
printDependencies([T]) :- transform(X, T), write(X), printDependencies([]).
printDependencies([H|T]) :- transform(X, H), write(X), write(', '), printDependencies(T).

printRecommendations([]).
printRecommendations([T]) :- transform(X, T), write(X), printRecommendations([]).
printRecommendations([[HH|TT]|T]) :- transform(X, HH), write('Package '), write(X), write(' recommends: '),
				     printDependencies(TT), printRecommendations(T).

printSuggestions([]).
printSuggestions([T]) :- transform(X, T), write(X), printSuggestions([]).
printSuggestions([[HH|TT]|T]) :- transform(X, HH), write('Package '), write(X), write(' suggests: '),
				     printDependencies(TT), printSuggestions(T).

printConflicts([]).
printConflicts([T]) :- transform(X, T), write(X), printConflicts([]).
printConflicts([[HH|TT]|T]) :- transform(X, HH), write('Package '), write(X), write(' conflicts: '),
				     printDependencies(TT), printConflicts(T).


print(P, [DH|DT], LR, LS, LC) :- write('===Information about package \''), write(P), write('\'===:\n'),
			     length([DH|DT], LD), length(LR, LRL), length(LS, LSL), length(LC, LCL), (LD =:= 1, LRL =:= 0, LSL =:= 0, LCL =:= 0) -> write('Package has no relationship information.\n');
			     length([DH|DT], X), X > 1 -> write('Depends on: '), printDependencies(DT), printRecommendations(LR), printSuggestions(LS), printConflicts(LC);
							  printRecommendations(LR), printSuggestions(LS), printConflicts(LC).

%===================================
% LIST AND PRINT ALL PACKAGES
%===================================
startPrintAll([]).
startPrintAll([H|T]) :- transform(X, H), info(X), write('\n'), startPrintAll(T).

%===================================
% CALLABLE FUNCTIONS
%===================================
load(F) :- rdf_load(F).
viewRaw(P, D, LR, F, LS, LC) :- transform(P, T), find_dependencies(T, D), find_recommends(D, [], LR), flattener(D, LR, F), find_suggestions(F, [], LS), find_conflicts(F, [], LC).
info(P) :- transform(P, T), find_dependencies(T, D), find_recommends(D, [], LR), flattener(D, LR, F), find_suggestions(F, [], LS), find_conflicts(F, [], LC), print(P, D, LR, LS, LC), issueWarning(D, LR, LS, LC).
printall :- listAll(X), startPrintAll(X).
