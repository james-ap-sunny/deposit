"""
Account management API endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from app.database.connection import get_source_session, get_dest_session
from app.services.account_service import AccountService
from app.utils.exceptions import BankingException
from app.utils.logger import log_audit

logger = logging.getLogger(__name__)

account_bp = Blueprint('account', __name__)


@account_bp.route('/accounts/<account_no>', methods=['GET'])
@jwt_required(optional=True)
def get_account_info(account_no):
    """Get account information"""
    try:
        # Try source database first
        try:
            with get_source_session() as session:
                account_service = AccountService(session)
                account_info = account_service.get_account_info(account_no)
                account_info['database'] = 'source'
                
                # Log audit event
                user_id = get_jwt_identity() or 'anonymous'
                log_audit(user_id, 'VIEW_ACCOUNT', account_no)
                
                return jsonify({
                    'success': True,
                    'data': account_info
                }), 200
                
        except Exception:
            # Try destination database
            with get_dest_session() as session:
                account_service = AccountService(session)
                account_info = account_service.get_account_info(account_no)
                account_info['database'] = 'destination'
                
                # Log audit event
                user_id = get_jwt_identity() or 'anonymous'
                log_audit(user_id, 'VIEW_ACCOUNT', account_no)
                
                return jsonify({
                    'success': True,
                    'data': account_info
                }), 200
                
    except BankingException as e:
        logger.warning(f"Account lookup failed: {str(e)}")
        return jsonify(e.to_dict()), 400
        
    except Exception as e:
        logger.error(f"Unexpected error in account lookup: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error'
            }
        }), 500


@account_bp.route('/accounts/<account_no>/balance', methods=['GET'])
@jwt_required(optional=True)
def get_account_balance(account_no):
    """Get account balance"""
    try:
        # Try source database first
        try:
            with get_source_session() as session:
                account_service = AccountService(session)
                account, balance = account_service.get_account_balance(account_no)
                
                # Log audit event
                user_id = get_jwt_identity() or 'anonymous'
                log_audit(user_id, 'VIEW_BALANCE', account_no)
                
                return jsonify({
                    'success': True,
                    'data': {
                        'account_no': account_no,
                        'balance': float(balance.TOTAL_AMOUNT),
                        'currency': account.ACCT_CCY,
                        'last_updated': balance.TRAN_TIMESTAMP.isoformat(),
                        'database': 'source'
                    }
                }), 200
                
        except Exception:
            # Try destination database
            with get_dest_session() as session:
                account_service = AccountService(session)
                account, balance = account_service.get_account_balance(account_no)
                
                # Log audit event
                user_id = get_jwt_identity() or 'anonymous'
                log_audit(user_id, 'VIEW_BALANCE', account_no)
                
                return jsonify({
                    'success': True,
                    'data': {
                        'account_no': account_no,
                        'balance': float(balance.TOTAL_AMOUNT),
                        'currency': account.ACCT_CCY,
                        'last_updated': balance.TRAN_TIMESTAMP.isoformat(),
                        'database': 'destination'
                    }
                }), 200
                
    except BankingException as e:
        logger.warning(f"Balance lookup failed: {str(e)}")
        return jsonify(e.to_dict()), 400
        
    except Exception as e:
        logger.error(f"Unexpected error in balance lookup: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error'
            }
        }), 500


@account_bp.route('/accounts/<account_no>/transactions', methods=['GET'])
@jwt_required(optional=True)
def get_account_transactions(account_no):
    """Get account transaction history"""
    try:
        # Get query parameters
        limit = min(int(request.args.get('limit', 10)), 100)  # Max 100 records
        offset = int(request.args.get('offset', 0))
        
        transactions = []
        
        # Try source database first
        try:
            with get_source_session() as session:
                account_service = AccountService(session)
                source_transactions = account_service.get_account_transaction_history(
                    account_no, limit, offset
                )
                for tx in source_transactions:
                    tx['database'] = 'source'
                transactions.extend(source_transactions)
                
        except Exception as e:
            logger.debug(f"No transactions found in source database: {str(e)}")
        
        # Try destination database
        try:
            with get_dest_session() as session:
                account_service = AccountService(session)
                dest_transactions = account_service.get_account_transaction_history(
                    account_no, limit, offset
                )
                for tx in dest_transactions:
                    tx['database'] = 'destination'
                transactions.extend(dest_transactions)
                
        except Exception as e:
            logger.debug(f"No transactions found in destination database: {str(e)}")
        
        # Sort by transaction date (most recent first)
        transactions.sort(key=lambda x: x.get('transaction_date', ''), reverse=True)
        
        # Apply limit after merging
        transactions = transactions[offset:offset+limit]
        
        # Log audit event
        user_id = get_jwt_identity() or 'anonymous'
        log_audit(user_id, 'VIEW_TRANSACTIONS', account_no, {'count': len(transactions)})
        
        return jsonify({
            'success': True,
            'data': {
                'account_no': account_no,
                'transactions': transactions,
                'count': len(transactions),
                'limit': limit,
                'offset': offset
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting transaction history: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error'
            }
        }), 500


@account_bp.route('/accounts/<account_no>/validate', methods=['POST'])
@jwt_required(optional=True)
def validate_account(account_no):
    """Validate account for transfer operations"""
    try:
        data = request.get_json() or {}
        is_source = data.get('is_source', True)
        
        # Try source database first
        try:
            with get_source_session() as session:
                account_service = AccountService(session)
                account, balance = account_service.validate_account_for_transfer(
                    account_no, is_source
                )
                
                return jsonify({
                    'success': True,
                    'data': {
                        'account_no': account_no,
                        'valid': True,
                        'account_name': account.ACCT_NAME,
                        'currency': account.ACCT_CCY,
                        'status': account.ACCT_STATUS,
                        'balance': float(balance.TOTAL_AMOUNT),
                        'database': 'source'
                    }
                }), 200
                
        except Exception:
            # Try destination database
            with get_dest_session() as session:
                account_service = AccountService(session)
                account, balance = account_service.validate_account_for_transfer(
                    account_no, is_source
                )
                
                return jsonify({
                    'success': True,
                    'data': {
                        'account_no': account_no,
                        'valid': True,
                        'account_name': account.ACCT_NAME,
                        'currency': account.ACCT_CCY,
                        'status': account.ACCT_STATUS,
                        'balance': float(balance.TOTAL_AMOUNT),
                        'database': 'destination'
                    }
                }), 200
                
    except BankingException as e:
        logger.warning(f"Account validation failed: {str(e)}")
        return jsonify({
            'success': False,
            'data': {
                'account_no': account_no,
                'valid': False,
                'error': e.to_dict()
            }
        }), 200  # Return 200 but with valid=false
        
    except Exception as e:
        logger.error(f"Unexpected error in account validation: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error'
            }
        }), 500


@account_bp.errorhandler(400)
def handle_bad_request(error):
    """Handle bad request errors"""
    return jsonify({
        'error': {
            'code': 'BAD_REQUEST',
            'message': 'Bad request'
        }
    }), 400


@account_bp.errorhandler(404)
def handle_not_found(error):
    """Handle not found errors"""
    return jsonify({
        'error': {
            'code': 'NOT_FOUND',
            'message': 'Resource not found'
        }
    }), 404