# Backlog do Projeto - Sistema de Controle de Ponto com QR Code

## Visão Geral
Sistema Kiosk autônomo para leitura de QR Code em crachás de funcionários, validação de janelas de horário de ponto e integração com o Supabase.

---

## Tarefas & Status

### 1. Estrutura e Configuração Inicial
- [x] Criação da estrutura de diretórios (`css/`, `js/`, `js/services/`, `js/components/`) - *Data: 2025-05-10*
- [x] Inicialização do documento `backlog.md` - *Data: 2025-05-10*
- [x] Configuração de credenciais do Supabase em `js/config.js` - *Data: 2025-05-10*
- [x] Implementação de serviço da API Supabase em `js/services/supabase.js` - *Data: 2025-05-10*

### 2. Módulos do Sistema (Services & Components)
- [x] Implementação do controle de câmera e canvas (`js/services/camera.js`) - *Data: 2025-05-10*
- [x] Implementação da decodificação de QR Code (`js/services/qrcode.js`) - *Data: 2025-05-10*
- [x] Implementação do validador de janelas e tolerância de horário (`js/services/tolerance.js`) - *Data: 2025-05-10*
- [x] Implementação da renderização e impressão de tickets (`js/components/ticket.js`) - *Data: 2025-05-10*
- [x] Inicialização da biblioteca Lucide Icons (`js/components/icons.js`) - *Data: 2025-05-10*

### 3. Interface e Estilização (UI/UX)
- [x] Construção do layout semântico Kiosk em `index.html` (otimizado para Tablets e Desktops) - *Data: 2025-05-10*
- [x] Implementação do CSS global e utilitários em `css/main.css` (fundo `#ffffff`, bordas `#e2e8f0`) - *Data: 2025-05-10*
- [x] Implementação dos componentes de UI e modais em `css/components.css` - *Data: 2025-05-10*

### 4. Integração do Fluxo da Aplicação
- [x] Conexão dos eventos de leitura de QR Code, verificação de funcionário e janelas em `js/app.js` - *Data: 2025-05-10*
- [x] Gravação de batida aprovada na tabela `registros_ponto` e emissão de ticket - *Data: 2025-05-10*
- [x] Captura de foto e gravação de ocorrência na tabela `ocorrencias_ponto` (`TENTATIVA_FORA_JANELA_ENTRADA`, `TENTATIVA_FORA_JANELA_SAIDA`, `QRCODE_INVALIDO`) - *Data: 2025-05-10*
- [x] Alertas visuais e bloqueios na interface sem emojis (apenas Lucide Icons) - *Data: 2025-05-10*

---

## Histórico de Alterações

| Data | Responsável | Descrição da Alteração | Status |
| :--- | :--- | :--- | :--- |
| 2025-05-10 | Google Jules | Criação da estrutura base do projeto e inicialização do backlog.md | Concluído |
| 2025-05-10 | Google Jules | Configuração de credenciais e cliente do Supabase | Concluído |
| 2025-05-10 | Google Jules | Implementação dos serviços de Câmera, QR Code, Tolerância, Ticket e Ícones | Concluído |
| 2025-05-10 | Google Jules | Construção do layout Kiosk em HTML5/CSS3 sem emojis | Concluído |
| 2025-05-10 | Google Jules | Integração completa do fluxo da aplicação em app.js com gravações no Supabase | Concluído |
