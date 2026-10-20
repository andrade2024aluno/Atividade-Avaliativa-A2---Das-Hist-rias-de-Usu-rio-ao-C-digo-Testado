"""Controle de acesso por tipo de usuário."""


class AcessoNegadoError(Exception):
    """Lançada quando o usuário não tem permissão para a funcionalidade."""


def exigir_tipo(usuario, tipo):
    """Garante que o usuário é do tipo exigido; caso contrário, nega o acesso."""
    if not isinstance(usuario, tipo):
        nome = getattr(usuario, "nome", "Usuário")
        raise AcessoNegadoError(
            f"{nome} ({type(usuario).__name__}) não tem acesso a esta funcionalidade."
        )
