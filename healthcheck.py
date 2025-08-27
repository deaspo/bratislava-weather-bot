#!/usr/bin/env python3
"""
Health check endpoint for Caprover deployment
Simple HTTP server to provide health status
"""

import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time
from datetime import datetime, timedelta
import subprocess

# Add the app directory to Python path
sys.path.insert(0, '/app')

try:
    from logger import logger
    from weather_service import WeatherService
    from twitter_service import TwitterService
except ImportError:
    # Fallback if modules aren't available
    import logging
    logger = logging.getLogger(__name__)

class HealthCheckHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/health':
            self.handle_health_check()
        elif self.path == '/status':
            self.handle_status_check()
        elif self.path == '/logs':
            self.handle_logs()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def handle_health_check(self):
        """Basic health check endpoint"""
        try:
            health_status = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'service': 'bratislava-weather-bot',
                'version': '1.0.0'
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(health_status, indent=2).encode())
            
        except Exception as e:
            logger.error("Health check failed: %s", e)
            self.send_error_response(500, str(e))
    
    def handle_status_check(self):
        """Detailed status check"""
        try:
            status = {
                'service': 'bratislava-weather-bot',
                'timestamp': datetime.now().isoformat(),
                'status': 'running',
                'components': {}
            }
            
            # Check if log files exist and are recent
            log_dir = '/app/logs'
            if os.path.exists(log_dir):
                log_files = os.listdir(log_dir)
                status['components']['logs'] = {
                    'status': 'healthy' if log_files else 'warning',
                    'count': len(log_files)
                }
            
            # Check if cron is running
            try:
                result = subprocess.run(['pgrep', 'cron'], capture_output=True)
                status['components']['cron'] = {
                    'status': 'healthy' if result.returncode == 0 else 'unhealthy',
                    'running': result.returncode == 0
                }
            except:
                status['components']['cron'] = {'status': 'unknown'}
            
            # Check last successful run
            cron_log = '/app/logs/cron.log'
            if os.path.exists(cron_log):
                try:
                    # Get last few lines to check for recent activity
                    with open(cron_log, 'r') as f:
                        lines = f.readlines()
                        if lines:
                            last_line = lines[-1].strip()
                            status['components']['last_activity'] = {
                                'status': 'info',
                                'last_entry': last_line
                            }
                except:
                    pass
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status, indent=2).encode())
            
        except Exception as e:
            logger.error("Status check failed: %s", e)
            self.send_error_response(500, str(e))
    
    def handle_logs(self):
        """Return recent log entries"""
        try:
            logs = {'logs': []}
            
            # Get cron logs
            cron_log = '/app/logs/cron.log'
            if os.path.exists(cron_log):
                try:
                    with open(cron_log, 'r') as f:
                        lines = f.readlines()
                        # Get last 50 lines
                        recent_lines = lines[-50:] if len(lines) > 50 else lines
                        logs['cron_logs'] = [line.strip() for line in recent_lines]
                except Exception as e:
                    logs['cron_logs_error'] = str(e)
            
            # Get application logs (most recent log file)
            log_dir = '/app/logs'
            if os.path.exists(log_dir):
                try:
                    log_files = [f for f in os.listdir(log_dir) if f.startswith('weather_bot_') and f.endswith('.log')]
                    if log_files:
                        # Get most recent log file
                        latest_log = sorted(log_files)[-1]
                        with open(os.path.join(log_dir, latest_log), 'r') as f:
                            lines = f.readlines()
                            recent_lines = lines[-30:] if len(lines) > 30 else lines
                            logs['app_logs'] = [line.strip() for line in recent_lines]
                except Exception as e:
                    logs['app_logs_error'] = str(e)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(logs, indent=2).encode())
            
        except Exception as e:
            logger.error("Logs retrieval failed: %s", e)
            self.send_error_response(500, str(e))
    
    def send_error_response(self, code, message):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        error_response = {
            'error': message,
            'timestamp': datetime.now().isoformat()
        }
        self.wfile.write(json.dumps(error_response).encode())
    
    def log_message(self, format, *args):
        """Override to suppress default logging"""
        pass

def run_health_server(port=8080):
    """Run the health check server"""
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info("Health check server starting on port %d", port)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Health check server stopped")
        server.shutdown()

if __name__ == "__main__":
    # Run health server in a separate thread if this is the main process
    port = int(os.environ.get('PORT', 8080))
    
    # Start health server in background
    health_thread = threading.Thread(target=run_health_server, args=(port,), daemon=True)
    health_thread.start()
    
    logger.info("Health check server started on port %d", port)
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Application stopped")
