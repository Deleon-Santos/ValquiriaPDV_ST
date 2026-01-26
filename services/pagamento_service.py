from controllers.pagamento import buscar_venda_aberta, efetuar_pagamento


def processar_pagamento(
    id_venda: int,
    total_venda: float,
    forma_pagamento: str,
    valor_pago: float
) -> dict:
    return efetuar_pagamento(
        id_venda=id_venda,
        total_venda=total_venda,
        forma_pagamento=forma_pagamento,
        valor_pago=valor_pago
    )

def obter_venda_aberta(usuario: dict):
    return buscar_venda_aberta(usuario["id"])