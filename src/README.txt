
📦 ESTRUTURA DE IMPORTAÇÃO OTIMIZADA - MIX TELEMATICS

Você deve incluir os seguintes arquivos no diretório principal do seu projeto (ex: `src/` ou raiz do backend):

1. ✅ Arquivos para INCLUIR:
--------------------------------------------------
- importador_lote.py
- main_lote.py

Esses dois arquivos substituem o modelo antigo com múltiplas chamadas. Eles executam uma única chamada à API, filtram em memória e inserem nas tabelas separadas normalmente.

2. 🚫 Arquivos que você pode aposentar (se quiser):
--------------------------------------------------
- main.py
- todos os arquivos tr_*.py (se não forem usados mais)

3. ✅ Execução recomendada:
--------------------------------------------------
Dentro da pasta onde estão `main_lote.py` e `.env`, rode:

    python main_lote.py

4. 🛡️ O que o novo sistema faz:
--------------------------------------------------
- 1 chamada para buscar até 1000 eventos
- Filtra em memória por EventTypeId
- Insere nas tabelas `tr_*` correspondentes
- Ignora duplicações com `ON DUPLICATE KEY`
- Respeita os limites da API (20/min e 500/hora)

5. 🔁 Próximos passos (opcional):
--------------------------------------------------
- Agendar com cron ou agendador da nuvem
- Salvar backup dos dados brutos em JSON
- Gerar um log por execução

Dúvidas? É só me chamar aqui 😄

..