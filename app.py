"""
DeepHat Chat API - Vercel Serverless Function
Provides REST API endpoints for chatting with DeepHat AI
"""

import json
import requests
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any
from flask import Flask, request, jsonify, Response, stream_with_context
import traceback
import os

# ========== Initialize Flask App (MUST be at top level) ==========
app = Flask(__name__)

# ========== Configuration ==========
API_URL = "https://app.deephat.ai/api/chat"

# Complete headers exactly as provided
HEADERS = {
    "Host": "app.deephat.ai",
    "sec-ch-ua-platform": "Android",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    "dnt": "1",
    "content-type": "text/plain;charset=UTF-8",
    "sec-ch-ua-mobile": "?1",
    "accept": "*/*",
    "origin": "https://app.deephat.ai",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://app.deephat.ai/",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,bn;q=0.6,pt;q=0.5,hi;q=0.4,fr;q=0.3",
    "priority": "u=1, i"
}

# ========== YOUR ACTUAL COOKIES ==========
COOKIES = {
    "_cfuvid": "BPJofLKonHSoMhTkRBnldcLD99RtCsOQmW0XRbvAJas-1784434586.2770495-1.0.1.1-K75E768OURF_f8e.CbeFS34fr1mccNjqum14nojLWnw",
    "osano_consentmanager_uuid": "f2095de7-879c-4431-adf0-172e9e893263",
    "osano_consentmanager": "eYNtz54Wm1xA2f5NN72Iepc59uSso1mat7bCDmVZy-9Yk5azqNmWJTUamcUwUnC4VlQUyAPNxnVWsBcoqCLUO6GutqGKzJGiN4MKLKU7rSmmTqtDiHYH5yaPmsrUTD3qiJaGMNmRum4PR4KzP7533GezM8BX0GiZPI8jgInCR7n2CRI0ojmJXbt6wtcrRfzkssredIrcZ2M9R-E81v9mAknsFV5XN62jW6Wgirkk5VRmK2fr25C-H2YR12fM9WhvzGG5IWs_6xMdrKc1lSbe4pQKe9UmSq27oSiI5GOcTFHVzZ_ojUBGCPRaVEBjgawV_GuDcUSEPq8=",
    "__Host-authjs.csrf-token": "413e8dd5a7dca639e7aa5a50cef8a75af07ad6feb111bd963b2b541935ab55a6%7C206c473ef83bb848a6c8366ff527b6fbeb3735af1be62de62abe3bc9e4762ec2",
    "_pvd_uid": "1.11-9uyfq1vl-mrraah78",
    "_ga": "GA1.1.439678113.1784434605",
    "__hstc": "2007726.86c3cee8ec994aa1938d366b998bd1e0.1784434606441.1784434606441.1784434606441.1",
    "hubspotutk": "86c3cee8ec994aa1938d366b998bd1e0",
    "__hssrc": "1",
    "__Secure-authjs.callback-url": "https%3A%2F%2Fapp.deephat.ai%2F",
    "_gcl_au": "1.1.302184194.1784434608",
    "_fbp": "fb.1.1784434608581.13488081160214291",
    "__hssc": "2007726.2.1784434606441",
    "__Secure-authjs.session-token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiOWdMTF9sSGRUWHU1T2dPVmZmWEJBX2tROFZxUVd1OGhkVVN6NnFsZ2RuQmQ0S0FWM1pOZTVrMEh3a1Iyc3JINmNzRTZDZjJCRWZXa1RuNWxpeFNJNWcifQ..57e7wx4PbmOvoprTZPtFiA.CfhA0jNcLMjsI1VtATpKixsL81T9KsybEMxbEVrA6c1BE5uiKNcadJn42PTkUzPzgnm2BDfa6rTbA5hVtRhJtsOZj33JHvGSWn405bYwIreHyc5hhDZTN_KTM1NSFoepY0686VW2bvtbjR7Dl_yc5kcGwu-yMmxEs8dIIgc_HMJtZ216g2-zE-8zbYAUaDsx0MwBvmnHQaqRNTmD7QsJLCGURPtDoY2TCbb_mIsWuWuk9MxEJZC20ksSseYos0XX01PEGar4Sk-jGGAeua9mqJWMgHWyxixo63HunnSuo9nabn3C1XbvrGGLbQadjyw6k6uzm_RA_GCobCC_jW6v7F6-shTzEeLqQLjl0MB1I4xzLGEJOa9bfzvWPGyVnf0gEAQBDUZRaHO_K01rdu0f7Pv-vQVTmtBvNELI2yfOWAonjMH6IO-u_fQZH7w9uZgrZxbcIunxpv82MmOraI-VIH_NuJofu8iu8_SRansFpWfOdRP3PxXlD6NtIInfbpWqO15f-7-L6gVVqhaUVKUPUD9oho9bgwocfYPzenTMkNK0ufgyY71C0Pitq-3EBiTu.10nOV8l8P6Lop1qI-lgm09Yu2uXfXu8jTTYQQTcY5-U",
    "_ga_G1LZLSPGPN": "GS2.1.s1784434605$o1$g1$t1784434652$j13$l0$h0"
}

# ========== Chat Session Class ==========
class DeepHatChat:
    def __init__(self, session_id: Optional[str] = None):
        """Initialize a chat session."""
        self.session_id = session_id or str(uuid.uuid4())[:8]
        self.messages: List[Dict] = []
        self.conversation_count = 0
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.session.cookies.update(COOKIES)

    def _format_message(self, content: str, role: str) -> Dict:
        """Format a message for the API request."""
        return {
            "id": str(uuid.uuid4())[:8],
            "content": content,
            "role": role
        }

    def _build_payload(self, user_message: str) -> Dict:
        """Build the request payload matching the exact format."""
        user_msg = self._format_message(user_message, "user")
        self.messages.append(user_msg)
        self.conversation_count += 1

        return {
            "messages": self.messages.copy(),
            "id": self.session_id,
            "enhancePrompt": False,
            "useFunctions": False
        }

    def send_message(self, message: str) -> Optional[str]:
        """Send a message and get the AI response."""
        if not message.strip():
            return None

        try:
            # Build payload
            payload = self._build_payload(message)
            
            # Make the API request
            response = self.session.post(
                API_URL,
                data=json.dumps(payload),
                timeout=120
            )
            
            # Check response
            response.raise_for_status()
            
            # Extract the AI response
            ai_response = response.text.strip()
            
            # Add AI response to history
            if ai_response:
                ai_msg = self._format_message(ai_response, "assistant")
                self.messages.append(ai_msg)
            
            return ai_response
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error {response.status_code}"
            if response.status_code == 401:
                error_msg = "Authentication failed! Cookies may have expired."
            return {"error": error_msg, "details": response.text[:200]}
        except requests.exceptions.Timeout:
            return {"error": "Request timed out. The AI is taking too long to respond."}
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    def clear_history(self):
        """Clear the conversation history."""
        self.messages = []
        return {"status": "success", "message": "Conversation history cleared"}

    def reset_session(self):
        """Reset the entire session."""
        self.session_id = str(uuid.uuid4())[:8]
        self.messages = []
        self.conversation_count = 0
        return {"status": "success", "message": f"New session started: {self.session_id}", "session_id": self.session_id}

    def get_history(self):
        """Get the conversation history."""
        return {
            "session_id": self.session_id,
            "total_messages": len(self.messages),
            "messages": self.messages.copy()
        }

    def get_stats(self):
        """Get conversation statistics."""
        stats = {
            "session_id": self.session_id,
            "total_messages": len(self.messages),
            "user_messages": sum(1 for m in self.messages if m['role'] == 'user'),
            "ai_messages": sum(1 for m in self.messages if m['role'] == 'assistant')
        }
        
        if self.messages:
            total_chars = sum(len(m['content']) for m in self.messages)
            stats["total_characters"] = total_chars
            responses = [m for m in self.messages if m['role'] == 'assistant']
            if responses:
                stats["avg_response_length"] = total_chars // len(responses)
        
        return stats

    def close(self):
        """Clean up the session."""
        self.session.close()

# ========== In-memory session storage ==========
# Note: For production, use Redis or another persistent store
chat_sessions = {}

def get_or_create_chat(session_id: Optional[str] = None) -> DeepHatChat:
    """Get an existing chat session or create a new one."""
    if session_id and session_id in chat_sessions:
        return chat_sessions[session_id]
    
    chat = DeepHatChat(session_id)
    if session_id:
        chat_sessions[session_id] = chat
    return chat

# ========== API Routes ==========

@app.route('/', methods=['GET'])
def home():
    """API root endpoint with documentation."""
    return jsonify({
        "name": "DeepHat Chat API",
        "version": "1.0.0",
        "description": "API for chatting with DeepHat AI assistant",
        "endpoints": {
            "/": "GET - This documentation",
            "/chat": "POST - Send a message to DeepHat",
            "/history": "GET - Get conversation history",
            "/stats": "GET - Get session statistics",
            "/reset": "POST - Reset the session",
            "/clear": "POST - Clear conversation history",
            "/sessions": "GET - List all active sessions"
        },
        "examples": {
            "chat": {
                "method": "POST",
                "body": {
                    "message": "What is OWASP Top 10?",
                    "session_id": "optional-session-id"
                }
            }
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Send a message to DeepHat AI."""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400
        
        message = data.get('message')
        session_id = data.get('session_id')
        
        # Get or create chat session
        chat = get_or_create_chat(session_id)
        
        # Send message
        response = chat.send_message(message)
        
        # Check if response is an error
        if isinstance(response, dict) and 'error' in response:
            return jsonify(response), 500
        
        return jsonify({
            "success": True,
            "session_id": chat.session_id,
            "response": response,
            "message_count": len(chat.messages)
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Server error: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Get conversation history."""
    session_id = request.args.get('session_id')
    
    if not session_id:
        return jsonify({"error": "Missing 'session_id' query parameter"}), 400
    
    chat = chat_sessions.get(session_id)
    if not chat:
        return jsonify({"error": "Session not found"}), 404
    
    return jsonify(chat.get_history())

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get session statistics."""
    session_id = request.args.get('session_id')
    
    if not session_id:
        return jsonify({"error": "Missing 'session_id' query parameter"}), 400
    
    chat = chat_sessions.get(session_id)
    if not chat:
        return jsonify({"error": "Session not found"}), 404
    
    return jsonify(chat.get_stats())

@app.route('/reset', methods=['POST'])
def reset_session():
    """Reset the session."""
    data = request.get_json() or {}
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({"error": "Missing 'session_id' in request body"}), 400
    
    chat = chat_sessions.get(session_id)
    if not chat:
        return jsonify({"error": "Session not found"}), 404
    
    result = chat.reset_session()
    return jsonify(result)

@app.route('/clear', methods=['POST'])
def clear_history():
    """Clear conversation history."""
    data = request.get_json() or {}
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({"error": "Missing 'session_id' in request body"}), 400
    
    chat = chat_sessions.get(session_id)
    if not chat:
        return jsonify({"error": "Session not found"}), 404
    
    result = chat.clear_history()
    return jsonify(result)

@app.route('/sessions', methods=['GET'])
def list_sessions():
    """List all active sessions."""
    sessions = {
        session_id: {
            "message_count": len(chat.messages),
            "session_id": session_id
        }
        for session_id, chat in chat_sessions.items()
    }
    return jsonify({
        "total_sessions": len(sessions),
        "sessions": sessions
    })

# ========== Error Handlers ==========
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# ========== Vercel Handler ==========
# Vercel will automatically use the 'app' variable
# No additional code needed

# ========== Local Development ==========
if __name__ == "__main__":
    app.run(debug=True, port=5000)
