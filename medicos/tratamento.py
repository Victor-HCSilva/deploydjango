import re

def formatar_cpf(cpf):
    """Remove a formatação do CPF (pontos e traço)."""
    if cpf:
        return re.sub(r'\D', '', cpf)  # Remove tudo que não é dígito
    return ''

def formatar(cpf:str):
    return cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:]

def rerirar_formatacao(cpf:str):
    return cpf.replace('.','').replace('-','')