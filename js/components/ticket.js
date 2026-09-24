/**
 * Módulo para formatação e impressão de comprovantes/tickets de ponto
 */

export class TicketComponent {
  /**
   * Gera um hash aleatório simplificado para o comprovante
   * @returns {string}
   */
  static gerarHashComprovante() {
    const randomArray = new Uint8Array(16);
    crypto.getRandomValues(randomArray);
    return Array.from(randomArray, byte => byte.toString(16).padStart(2, '0')).join('');
  }

  /**
   * Imprime o ticket criando uma janela de impressão rápida
   * @param {Object} dadosTicket
   */
  static imprimirTicket(dadosTicket) {
    const { nome, matricula, tipoRegistro, dataHora, hashComprovante } = dadosTicket;

    const dataFormatada = new Date(dataHora).toLocaleString('pt-BR', {
      dateStyle: 'short',
      timeStyle: 'medium'
    });

    const ticketWindow = window.open('', '_blank', 'width=400,height=600');
    if (!ticketWindow) {
      console.warn('Pop-up de impressão bloqueado pelo navegador.');
      return;
    }

    const htmlContent = `
      <!DOCTYPE html>
      <html lang="pt-BR">
      <head>
        <meta charset="UTF-8">
        <title>Comprovante de Ponto</title>
        <style>
          body {
            font-family: 'Courier New', Courier, monospace;
            width: 280px;
            margin: 0 auto;
            padding: 10px;
            color: #000;
          }
          .header {
            text-align: center;
            border-bottom: 1px dashed #000;
            padding-bottom: 8px;
            margin-bottom: 8px;
          }
          .title {
            font-weight: bold;
            font-size: 14px;
          }
          .item {
            margin: 4px 0;
            font-size: 12px;
          }
          .footer {
            border-top: 1px dashed #000;
            margin-top: 10px;
            padding-top: 8px;
            text-align: center;
            font-size: 10px;
            word-break: break-all;
          }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="title">COMPROVANTE DE PONTO</div>
          <div>SISTEMA AUTÔNOMO</div>
        </div>
        <div class="item"><strong>NOME:</strong> ${nome}</div>
        <div class="item"><strong>MATRÍCULA:</strong> ${matricula}</div>
        <div class="item"><strong>TIPO:</strong> ${tipoRegistro}</div>
        <div class="item"><strong>DATA/HORA:</strong> ${dataFormatada}</div>
        <div class="footer">
          <div>HASH COMPROVANTE:</div>
          <div>${hashComprovante}</div>
        </div>
        <script>
          window.onload = function() {
            window.print();
            setTimeout(function() { window.close(); }, 500);
          };
        </script>
      </body>
      </html>
    `;

    ticketWindow.document.write(htmlContent);
    ticketWindow.document.close();
  }
}
