% o python só precisa chamar o prolog e rodar verificar_adequacao(Projeto, Time, R)
% o Time é uma lista tipo [ana, bruno]
% o prolog devolve adequado ou nao_adequado
% pode chamar usando subprocess ou pyswip
% no subprocess dá pra usar algo tipo:
% swipl -q -s kb.pl -g "verificar_adequacao(sistema_web,[ana,bruno],R), format('~w',[R]), halt."
% e ler o resultado no python pra mostrar pro usuário

% kb.pl
% Teste: verificar_adequacao(sistema_web, [ana, bruno], R).

% alunos
aluno(ana). aluno(bruno). aluno(carla). aluno(diego).
aluno(edu). aluno(flora). aluno(gabriel). aluno(helo).
aluno(igor). aluno(julia). aluno(kauan). aluno(lana).

% skills dos alunos
aluno_skill(ana, frontend).
aluno_skill(ana, javascript).
aluno_skill(bruno, backend).
aluno_skill(bruno, python).
aluno_skill(carla, frontend).
aluno_skill(carla, css).
aluno_skill(diego, backend).
aluno_skill(diego, prolog).
aluno_skill(edu, database).
aluno_skill(edu, backend).
aluno_skill(flora, design).
aluno_skill(flora, html).
aluno_skill(gabriel, javascript).
aluno_skill(gabriel, frontend).
aluno_skill(helo, prolog).
aluno_skill(helo, logic).
aluno_skill(igor, devops).
aluno_skill(igor, backend).
aluno_skill(julia, mobile).
aluno_skill(julia, frontend).
aluno_skill(kauan, python).
aluno_skill(kauan, data).
aluno_skill(lana, css).
aluno_skill(lana, html).

% projeto e requisitos
projeto(sistema_web, [frontend, backend, prolog]).

% junta skills do time
team_skills([], []).
team_skills([P|Ps], Skills) :-
    team_skills(Ps, Rest),
    findall(S, aluno_skill(P, S), A),
    append(A, Rest, All),
    sort(All, Skills).

% checa cobertura
covers_all(Skills, Req) :-
    forall(member(R, Req), member(R, Skills)).

% regra principal
verificar_adequacao(Proj, Team, adequado) :-
    projeto(Proj, Req),
    team_skills(Team, Skills),
    covers_all(Skills, Req).

verificar_adequacao(Proj, Team, nao_adequado) :-
    projeto(Proj, Req),
    team_skills(Team, Skills),
    \+ covers_all(Skills, Req).
