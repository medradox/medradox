# Manutenção do perfil

Execute `python scripts/build_profile.py` para atualizar o calendário (sem dependências externas).
Para recriar retrato e cartão: instale `pillow==12.3.0` e execute `python scripts/build_profile.py --identity`.
Edite a lista `rows` no script para mudar o cartão. O avatar fica em `data/avatar.png`.
O workflow executa diariamente por volta das 06h17 de Brasília; pode haver atraso do GitHub.
O texto anterior está preservado no README e em `data/original-readme.md`.
Os SVGs respeitam a preferência de movimento reduzido.
Implementação própria inspirada em https://www.avivashishta.com/blog/build-animated-github-profile-readme.html
Adaptação: retrato com contraste e escala de cinza, sem remoção de fundo por IA.
