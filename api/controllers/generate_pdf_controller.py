from flask import Request, Response, jsonify, make_response

from api.entities import GeneratePDFDocumentDTO
from api.exceptions import BadRequestException

from das_emitter.emitter import DASEmitter
from das_emitter.exceptions import InvalidCNPJException, MonthNotAvailableException, YearNotAvailableException

def validate_request(request: Request) -> GeneratePDFDocumentDTO:
    data = request.get_json()
    for param in ['cnpj', 'month', 'year']:
        if(data.get(param) is None):
            raise BadRequestException(f'Missing param {param}')
        
    return GeneratePDFDocumentDTO(
        cnpj=str(data['cnpj']),
        month=str(data['month']),
        year=int(data['year'])
    )

class GeneratePDFController:
    def __init__(self) -> None:
        pass
    
    def __make_pdf_response(self, model: GeneratePDFDocumentDTO) -> tuple[Response, int]:
        emitter = DASEmitter()
        pdf_data = emitter.get_pdf(model.cnpj, model.month, model.year) # type: ignore
        response = make_response(pdf_data)
        response.headers['Content-Type'] = 'application/pdf'
        #response.headers['Content-Disposition'] = 'attachment'
        response.headers['Content-Disposition'] = 'inline'
        return response, 200

    def handle(self, request: Request) -> tuple[Response, int]:
        try:
            dto = validate_request(request)
            return self.__make_pdf_response(dto)

        except BadRequestException as ex:
            return jsonify({'message': f'{ex}'}), 400
        except InvalidCNPJException as ex:
            return jsonify({'message': f'{ex}'}), 401
        except (MonthNotAvailableException, YearNotAvailableException) as ex:
            return jsonify({'message': f'{ex}'}), 404
        except Exception as ex:
            return jsonify({'message': f'{ex}'}), 500