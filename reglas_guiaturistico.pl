%1. Regla para encontrar destinos por tipo de inter�s:
recomendar_por_interes(Interes, Nombre, Canton, Provincia) :-destino(Nombre, Canton, Provincia, Interes, _, _).
%2. Regla para encontrar destinos por presupuesto:
recomendar_por_presupuesto(TipoVisitante, PresupuestoMax, Nombre, Canton, Provincia) :-
    destino(Nombre, Canton, Provincia, _, ListaPrecios, _),
    member(TipoVisitante-Presupuesto, ListaPrecios),
    Presupuesto =< PresupuestoMax.
%3. Regla para encontrar destinos por tiempo disponible:
recomendar_por_tiempo(TiempoMax, Nombre, Canton, Provincia) :-
    destino(Nombre, Canton, Provincia, _, _, TiempoRequerido),
    TiempoRequerido =< TiempoMax.
%4. Regla combinada: Destino ideal:
recomendar_destino_ideal(Interes, TipoVisitante, PresupuestoMax, TiempoMax, Nombre, Canton, Provincia) :-
    destino(Nombre, Canton, Provincia, Interes, ListaPrecios, TiempoRequerido),
    member(TipoVisitante-Presupuesto, ListaPrecios),
    Presupuesto =< PresupuestoMax,
    TiempoRequerido =< TiempoMax.
%5. Regla para listar destinos por provincia:
listar_destinos_provincia(Provincia, Nombre, Canton, Interes) :- destino(Nombre, Canton, Provincia, Interes, _, _).

