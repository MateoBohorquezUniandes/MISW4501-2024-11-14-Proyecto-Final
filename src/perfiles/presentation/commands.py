from uuid import UUID

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from perfiles.application.commands.associate_alimento import AssociateAlimento
from perfiles.application.commands.associate_reporte_sanguineo import (
    AssociateReporteSanguineo,
)
from perfiles.application.commands.create_alimento import CreateAlimento
from perfiles.application.commands.update_clasificacion_riesgo import (
    ActualizarClasificacionRiesgo,
)
from perfiles.application.commands.update_fisiologia import ActualizarPerfilDemografico
from perfiles.application.commands.update_tipo_alimentacion import (
    ActualizarTipoAlimentacion,
)
import seedwork.presentation.api as api
from perfiles.application.commands.crear_habito_deportivo import CrearHabitoDeportivo
from perfiles.application.commands.crear_molestia import CrearMolestia
from perfiles.application.commands.create_perfil_inicial import PerfilamientoInicial
from perfiles.application.mappers import (
    AlimentoDTODictMapper,
    HabitoDTODictMapper,
    MolestiaDTODictMapper,
    PerfilAlimenticioDTODictMapper,
    PerfilDemograficoDTODictMapper,
    PerfilamientoInicialDTODictMapper,
    ReporteSanguineoDTODictMapper,
)
from perfiles.application.queries.get_perfil_demografico import ObtenerPerfilDemografico
from seedwork.application.commands import execute_command
from seedwork.application.queries import execute_query

bp_prefix: str = "/perfiles/commands"
bp: Blueprint = api.create_blueprint("commands", bp_prefix)


@bp.route("/demografico/init", methods=("POST",))
def create():
    mapper = PerfilamientoInicialDTODictMapper()
    data = request.json
    pefil_demografico_dto = mapper.external_to_dto(data.get("payload"))

    command = PerfilamientoInicial(
        correlation_id=UUID(data.get("correlation_id")),
        perfil_dto=pefil_demografico_dto,
    )
    execute_command(command)
    return {}, 202


@bp.route("/demografico/riesgo", methods=("PATCH",))
def actualizar_riesgo_perfil():
    mapper = PerfilDemograficoDTODictMapper()

    payload = request.json
    correlation_id = (
        UUID(payload["correlation_id"]) if "correlation_id" in payload else None
    )

    query_result = execute_query(
        ObtenerPerfilDemografico(
            tipo_identificacion=payload["payload"].get("tipo_identificacion"),
            identificacion=payload["payload"].get("identificacion"),
        )
    )
    vo_max_perfil = query_result.result.clasificacion_riesgo.vo_max.valor
    perfil_dict = mapper.dto_to_external(query_result.result)

    vo_max = payload.get("payload", {}).get("vo_max", vo_max_perfil)
    perfil_dict["clasificacion_riesgo"]["vo_max"]["valor"] = vo_max
    perfil_dto = mapper.external_to_dto(perfil_dict)

    command = ActualizarClasificacionRiesgo(
        correlation_id=correlation_id,
        perfil_dto=perfil_dto,
    )
    execute_command(command)
    return {}, 202


@bp.route("/demografico/reporte-sanguineo", methods=("POST",))
@jwt_required()
def asociar_reporte_sanguineo():
    identificacion: dict = get_jwt_identity()
    reporte_sanguineo_dto = ReporteSanguineoDTODictMapper().external_to_dto(
        request.json
    )

    command = AssociateReporteSanguineo(
        reporte_sanguineo_dto=reporte_sanguineo_dto,
        tipo_identificacion=identificacion.get("tipo"),
        identificacion=identificacion.get("valor"),
    )

    execute_command(command)

    return {}, 202


@bp.route("/demografico", methods=("PUT",))
@jwt_required()
def actualizar_datos_perfil():
    identificacion: dict = get_jwt_identity()
    mapper = PerfilDemograficoDTODictMapper()
    data = request.json

    query_result = execute_query(
        ObtenerPerfilDemografico(
            tipo_identificacion=identificacion.get("tipo"),
            identificacion=identificacion.get("valor"),
        )
    )

    perfil_dict = mapper.dto_to_external(query_result.result)
    edad = query_result.result.fisiologia.edad
    genero = query_result.result.fisiologia.genero
    peso_perfil = query_result.result.fisiologia.peso
    altura_perfil = query_result.result.fisiologia.altura
    pais = query_result.result.demografia.pais
    ciudad = query_result.result.demografia.ciudad
    peso = data.get("payload", {}).get("fisiologia", {}).get("peso", peso_perfil)
    altura = data.get("payload", {}).get("fisiologia", {}).get("altura", altura_perfil)
    edad = data.get("payload", {}).get("fisiologia", {}).get("edad", edad)
    genero = data.get("payload", {}).get("fisiologia", {}).get("genero", genero)
    pais = data.get("payload", {}).get("demografia", {}).get("pais_residencia", pais)
    ciudad = (
        data.get("payload", {}).get("demografia", {}).get("ciudad_residencia", ciudad)
    )
    perfil_dict["fisiologia"]["altura"] = altura
    perfil_dict["fisiologia"]["peso"] = peso
    perfil_dict["fisiologia"]["edad"] = edad
    perfil_dict["fisiologia"]["genero"] = genero
    perfil_dict["demografia"]["pais"] = pais
    perfil_dict["demografia"]["ciudad"] = ciudad

    perfil_dto = mapper.external_to_dto(perfil_dict)

    print(perfil_dict)
    command = ActualizarPerfilDemografico(
        perfil_dto=perfil_dto,
    )

    execute_command(command)

    return {}, 202


@bp.route("/deportivo/habitos", methods=("POST",))
@jwt_required()
def crear_habito_deportivo():
    mapper = HabitoDTODictMapper()
    data = request.json
    identificacion: dict = get_jwt_identity()
    payload = data.get("payload")
    payload["identificacion"] = identificacion.get("valor")
    payload["tipo_identificacion"] = identificacion.get("tipo")
    habito_dto = mapper.external_to_dto(payload)

    command = CrearHabitoDeportivo(habito_dto=habito_dto)

    execute_command(command)
    return {}, 202


@bp.route("/deportivo/molestias", methods=("POST",))
@jwt_required()
def crear_molestias():
    mapper = MolestiaDTODictMapper()
    data = request.json
    identificacion: dict = get_jwt_identity()
    payload = data.get("payload")
    payload["identificacion"] = identificacion.get("valor")
    payload["tipo_identificacion"] = identificacion.get("tipo")
    molestia_dto = mapper.external_to_dto(payload)

    command = CrearMolestia(molestia_dto=molestia_dto)

    execute_command(command)
    return {}, 202


@bp.route("/alimentos", methods=("POST",))
def crear_alimento():
    alimento_dto = AlimentoDTODictMapper().external_to_dto(request.json)
    command = CreateAlimento(alimento_dto=alimento_dto)

    execute_command(command)
    return {}, 202


@bp.route("/alimenticio/alimentos", methods=("POST",))
@jwt_required()
def asociar_alimento():
    identificacion: dict = get_jwt_identity()
    alimento_dto = AlimentoDTODictMapper().external_to_dto(request.json)

    command = AssociateAlimento(
        alimento_dto=alimento_dto,
        tipo_identificacion=identificacion.get("tipo"),
        identificacion=identificacion.get("valor"),
    )

    execute_command(command)
    return {}, 202


@bp.route("/alimenticio/tipo", methods=("PATCH",))
@jwt_required()
def actualizar_tipo_alimentacion():
    identificacion: dict = get_jwt_identity()
    payload = request.json

    payload["identificacion"] = identificacion.get("valor")
    payload["tipo_identificacion"] = identificacion.get("tipo")
    perfil_dto = PerfilAlimenticioDTODictMapper().external_to_dto(payload)

    command = ActualizarTipoAlimentacion(perfil_dto=perfil_dto)
    execute_command(command)
    return {}, 202
