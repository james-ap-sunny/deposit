"""
Health check API endpoints
"""

from flask import Blueprint, jsonify
from datetime import datetime
import logging

from app.database.connection import get_database_info, test_connections

logger = logging.getLogger(__name__)

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    try:
        # Test database connections
        db_status = test_connections()
        
        health_status = {
            'status': 'healthy' if db_status else 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'core-banking-transfer-system',
            'version': '1.0.0',
            'database_status': 'connected' if db_status else 'disconnected'
        }
        
        status_code = 200 if db_status else 503
        return jsonify(health_status), status_code
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 503


@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """Detailed health check with database information"""
    try:
        # Get database connection info
        db_info = get_database_info()
        
        # Determine overall health
        source_healthy = db_info.get('source', {}).get('status') == 'connected'
        dest_healthy = db_info.get('dest', {}).get('status') == 'connected'
        overall_healthy = source_healthy and dest_healthy
        
        health_status = {
            'status': 'healthy' if overall_healthy else 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'core-banking-transfer-system',
            'version': '1.0.0',
            'components': {
                'source_database': {
                    'status': 'healthy' if source_healthy else 'unhealthy',
                    'details': db_info.get('source', {})
                },
                'destination_database': {
                    'status': 'healthy' if dest_healthy else 'unhealthy',
                    'details': db_info.get('dest', {})
                }
            }
        }
        
        status_code = 200 if overall_healthy else 503
        return jsonify(health_status), status_code
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 503


@health_bp.route('/health/ready', methods=['GET'])
def readiness_check():
    """Readiness check for Kubernetes"""
    try:
        # Test if the application is ready to serve requests
        db_status = test_connections()
        
        if db_status:
            return jsonify({
                'status': 'ready',
                'timestamp': datetime.utcnow().isoformat()
            }), 200
        else:
            return jsonify({
                'status': 'not_ready',
                'timestamp': datetime.utcnow().isoformat(),
                'reason': 'database_not_connected'
            }), 503
            
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return jsonify({
            'status': 'not_ready',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 503


@health_bp.route('/health/live', methods=['GET'])
def liveness_check():
    """Liveness check for Kubernetes"""
    try:
        # Basic liveness check - just return that the service is running
        return jsonify({
            'status': 'alive',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Liveness check failed: {str(e)}")
        return jsonify({
            'status': 'dead',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 503