from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

import seedwork.presentation.api as api
from seedwork.application.commands import execute_command
from indicadores.application.commands.add_form import CreateFormula
from indicadores.application.commands.recalculate_index import CalculateIndicador
#from sesiones.application.commands.end_sesion import EndSesionDeportiva
from indicadores.application.mappers import FormulaDTODictMapper, IndicadoresDTODictMapper

bp_prefix: str = "/indicadores/commands"
bp: Blueprint = api.create_blueprint("commands", bp_prefix)


@bp.route("/", methods=("POST",))
@jwt_required()
def create_form():
    identificacion: dict = get_jwt_identity()
    data: dict = request.json
    data["tipo_identificacion"] = identificacion.get("tipo")
    data["identificacion"] = identificacion.get("valor")
    mapper = FormulaDTODictMapper()
    formula_dto = mapper.external_to_dto(data)

    command = CreateFormula(formula_dto=formula_dto)
    execute_command(command)
    return {}, 201

@bp.route("/recalculate", methods=("PUT",))
@jwt_required()
def recalculate_index():
    identificacion: dict = get_jwt_identity()
    data: dict = request.json
    data["tipo_identificacion"] = identificacion.get("tipo")
    data["identificacion"] = identificacion.get("valor")
    mapper = IndicadoresDTODictMapper()
    indicador_dto = mapper.external_to_dto(data)
    command = CalculateIndicador(indicador_dto=indicador_dto)
    commandresult = execute_command(command)
    return jsonify([mapper.dto_to_external(e) for e in commandresult.result])
