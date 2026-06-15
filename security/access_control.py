from security.roles import ROLE_PERMISSIONS


def has_access(role: str, document_name: str) -> bool:
    """Strictly evaluates permission and returns a boolean."""
    if not document_name:
        return False
        
    permissions = ROLE_PERMISSIONS.get(role, [])

    if "all" in permissions:
        return True

    return document_name in permissions