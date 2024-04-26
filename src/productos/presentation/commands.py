from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required


from seedwork.application.commands import execute_command
import seedwork.presentation.api as api

from productos.application.mappers import ProductoDTODictMapper
from productos.application.commands.create_producto import CreateProducto

bp_prefix: str = "/productos/commands"
bp: Blueprint = api.create_blueprint("commands", bp_prefix)


@bp.route("/", methods=("POST",))
@jwt_required()
def crear_producto():
    mapper = ProductoDTODictMapper()
    data = request.json
    payload = data.get("payload")
    producto_dto = mapper.external_to_dto(payload)

    command = CreateProducto(producto_dto=producto_dto)

    execute_command(command)
    return {}, 202
