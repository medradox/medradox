# Manutenção do perfil

Execute `python scripts/build_profile.py` para atualizar o calendário (sem dependências externas).
Para recriar retrato e cartão: instale `pillow==12.3.0` e execute `python scripts/build_profile.py --identity`.
Edite a lista `rows` no script para mudar o cartão. A foto aprovada fica em `data/professional-portrait.png`; ela gera o retrato ASCII do README. O avatar da conta é configurado separadamente no GitHub.
O workflow executa diariamente por volta das 06h17 de Brasília; pode haver atraso do GitHub.
O texto anterior está preservado no README e em `data/original-readme.md`.
Os SVGs respeitam a preferência de movimento reduzido.
Implementação própria inspirada em https://www.avivashishta.com/blog/build-animated-github-profile-readme.html
O fundo claro é removido por conectividade; contraste e tons são ajustados antes da conversão em 100 × 53 caracteres. A animação revela as linhas da esquerda para a direita uma vez. Use `STATIC=1` para gerar quadros finais sem animação.
