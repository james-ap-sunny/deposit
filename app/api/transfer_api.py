"""
Transfer API endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from decimal import Decimal

from app.services.transfer_service import TransferService
from app.config.settings import Config
from app.utils.exceptions import BankingException
from app.utils.logger import log_audit

logger = logging.getLogger(__name__)

transfer_bp = Blueprint('transfer', __name__)


@transfer_bp.route('/transfers', methods=['POST'])
@jwt_required(optional=True)
def create_transfer():
    """Create a new transfer"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': {
                    'code': 'INVALID_REQUEST',
                    'message': 'Request body is required'
                }
            }), 400
        
        # Validate required fields
        required_fields = ['from_account', 'to_account', 'amount']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'error': {
                    'code': 'MISSING_FIELDS',
                    'message': f'Missing required fields: {", ".join(missing_fields)}'
                }
            }), 400
        
        # Prepare transfer request
        transfer_request = {
            'from_account': data['from_account'],
            'to_account': data['to_account'],
            'amount': data['amount'],
            'currency': data.get('currency', 'CNY'),
            'description': data.get('description', 'Transfer'),
            'reference': data.get('reference', '')
        }
        
        # Initialize transfer service
        config = Config()
        transfer_service = TransferService(config)
        
        # Process transfer
        result = transfer_service.process_transfer(transfer_request)
        
        # Log audit event
        user_id = get_jwt_identity() or 'anonymous'
        log_audit(user_id, 'CREATE_TRANSFER', result['transfer_id'], {
            'from_account': transfer_request['from_account'],
            'to_account': transfer_request['to_account'],
            'amount': transfer_request['amount']
        })
        
        return jsonify({
            'success': True,
            'data': result
        }), 201
        
    except BankingException as e:
        logger.warning(f"Transfer failed: {str(e)}")
        return jsonify(e.to_dict()), 400
        
    except Exception as e:
        logger.error(f"Unexpected error in transfer: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error'
            }
        }), 500


@transfer_bp.route('/transfers/<transfer_id>', methods=['GET'])
@jwt_required(optional=True)
def get_transfer_status(transfer_id):
    """Get transfer status by ID"""
    try:
        # Initialize transfer service
        config = Config()
        transfer_service = TransferService(config)
        
        # Get transfer status
        transfer_info = transfer_service.get_transfer_status(transfer_id)
        
        if not transfer_info:
            return jsonify({
                'error': {
                    'code': 'TRANSFER_NOT_FOUND',
                    'message': f'Transfer {transfer_id} not found'
                }
            }), 404
        
        # Log audit event
        user_id = get_jwt_identity() or 'anonymous'
        log_audit(user_id, 'VIEW_TRANSFER', transfer_id)
        
        return jsonify({
            'success': True,
            'data': transfer_info
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting transfer status: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error'
            }
        }), 500


@transfer_bp.route('/transfers/history/<account_no>', methods=['GET'])
@jwt_required(optional=True)
def get_transfer_history(account_no):
    """Get transfer history for an account"""
    try:
        # Get query parameters
        limit = min(int(request.args.get('limit', 10)), 100)  # Max 100 records
        offset = int(request.args.get('offset', 0))
        
        # Initialize transfer service
        config = Config()
        transfer_service = TransferService(config)
        
        # Get transfer history
        transfers = transfer_service.get_transfer_history(account_no, limit, offset)
        
        # Log audit event
        user_id = get_jwt_identity() or 'anonymous'
        log_audit(user_id, 'VIEW_TRANSFER_HISTORY', account_no, {'count': len(transfers)})
        
        return jsonify({
            'success': True,
            'data': {
                'account_no': account_no,
                'transfers': transfers,
                'count': len(transfers),
                'limit': limit,
                'offset': offset
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting transfer history: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error'
            }
        }), 500


@transfer_bp.route('/transfers/validate', methods=['POST'])
@jwt_required(optional=True)
def validate_transfer():
    """Validate transfer request without executing it"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': {
                    'code': 'INVALID_REQUEST',
                    'message': 'Request body is required'
                }
            }), 400
        
        # Validate required fields
        required_fields = ['from_account', 'to_account', 'amount']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'error': {
                    'code': 'MISSING_FIELDS',
                    'message': f'Missing required fields: {", ".join(missing_fields)}'
                }
            }), 400
        
        # Prepare transfer request
        transfer_request = {
            'from_account': data['from_account'],
            'to_account': data['to_account'],
            'amount': data['amount'],
            'currency': data.get('currency', 'CNY')
        }
        
        # Initialize transfer service
        config = Config()
        transfer_service = TransferService(config)
        
        # Validate transfer request (this will raise exceptions if invalid)
        transfer_service._validate_transfer_request(transfer_request)
        
        # If we get here, the transfer is valid
        return jsonify({
            'success': True,
            'data': {
                'valid': True,
                'message': 'Transfer request is valid',
                'from_account': transfer_request['from_account'],
                'to_account': transfer_request['to_account'],
                'amount': float(transfer_request['amount']),
                'currency': transfer_request['currency']
            }
        }), 200
        
    except BankingException as e:
        logger.warning(f"Transfer validation failed: {str(e)}")
        return jsonify({
            'success': False,
            'data': {
                'valid': False,
                'error': e.to_dict()
            }
        }), 200  # Return 200 but with valid=false
        
    except Exception as e:
        logger.error(f"Unexpected error in transfer validation: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error'
            }
        }), 500


@transfer_bp.route('/transfers/limits', methods=['GET'])
@jwt_required(optional=True)
def get_transfer_limits():
    """Get current transfer limits"""
    try:
        config = Config()
        
        limits = {
            'max_transfer_amount': float(config.MAX_TRANSFER_AMOUNT),
            'min_transfer_amount': float(config.MIN_TRANSFER_AMOUNT),
            'daily_transfer_limit': float(config.DAILY_TRANSFER_LIMIT),
            'supported_currencies': ['CNY'],
            'transaction_timeout': config.TRANSACTION_TIMEOUT
        }
        
        return jsonify({
            'success': True,
            'data': limits
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting transfer limits: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error'
            }
        }), 500


@transfer_bp.errorhandler(400)
def handle_bad_request(error):
    """Handle bad request errors"""
    return jsonify({
        'error': {
            'code': 'BAD_REQUEST',
            'message': 'Bad request'
        }
    }), 400


@transfer_bp.errorhandler(404)
def handle_not_found(error):
    """Handle not found errors"""
    return jsonify({
        'error': {
            'code': 'NOT_FOUND',
            'message': 'Resource not found'
        }
    }), 404