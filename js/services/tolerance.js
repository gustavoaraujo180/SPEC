/**
 * Serviço de Validação de Tolerância e Janelas de Horário
 */

export class ToleranceService {
  /**
   * Converte uma string de hora 'HH:MM' ou 'HH:MM:SS' em minutos do dia
   * @param {string} timeStr
   * @returns {number}
   */
  static timeToMinutes(timeStr) {
    if (!timeStr) return 0;
    const parts = timeStr.split(':').map(Number);
    return parts[0] * 60 + parts[1] + (parts[2] ? parts[2] / 60 : 0);
  }

  /**
   * Retorna os minutos decorridos no dia para a data fornecida (ou agora)
   * @param {Date} date
   * @returns {number}
   */
  static getCurrentMinutes(date = new Date()) {
    return date.getHours() * 60 + date.getMinutes() + date.getSeconds() / 60;
  }

  /**
   * Avalia se a hora atual está dentro da janela de entrada ou de saída do funcionário
   * @param {Object} janela - Registro de janelas_horario com janela_entrada_inicio, etc.
   * @param {Date} [now=new Date()]
   * @returns {Object} Resultado com { aprovado, tipoRegistro, motivoOcorrencia }
   */
  static validarJanelaPonto(janela, now = new Date()) {
    if (!janela) {
      return {
        aprovado: false,
        tipoRegistro: null,
        motivoOcorrencia: 'JANELA_NAO_CONFIGURADA',
        mensagem: 'Janela de horário não encontrada para o funcionário.'
      };
    }

    const currentMin = this.getCurrentMinutes(now);

    const entradaInicio = this.timeToMinutes(janela.janela_entrada_inicio);
    const entradaFim = this.timeToMinutes(janela.janela_entrada_fim);
    const salidaInicio = this.timeToMinutes(janela.janela_saida_inicio);
    const salidaFim = this.timeToMinutes(janela.janela_saida_fim);

    // Validação da Janela de Entrada
    if (currentMin >= entradaInicio && currentMin <= entradaFim) {
      return {
        aprovado: true,
        tipoRegistro: 'ENTRADA',
        motivoOcorrencia: null,
        mensagem: 'Ponto de Entrada Aprovado!'
      };
    }

    // Validação da Janela de Saída
    if (currentMin >= salidaInicio && currentMin <= salidaFim) {
      return {
        aprovado: true,
        tipoRegistro: 'SAIDA',
        motivoOcorrencia: null,
        mensagem: 'Ponto de Saída Aprovado!'
      };
    }

    // Se estiver fora, determinar se o horário está mais próximo da entrada ou da saída
    // Se a hora atual for anterior à metade do dia / janela de saída, considera tentativa fora da janela de entrada
    const meioDoDia = (entradaFim + salidaInicio) / 2;
    const tipoOcorrencia = currentMin < meioDoDia
      ? 'TENTATIVA_FORA_JANELA_ENTRADA'
      : 'TENTATIVA_FORA_JANELA_SAIDA';

    return {
      aprovado: false,
      tipoRegistro: currentMin < meioDoDia ? 'ENTRADA' : 'SAIDA',
      motivoOcorrencia: tipoOcorrencia,
      mensagem: `Horário fora da janela permitida. (${currentMin < meioDoDia ? 'Entrada: ' + janela.janela_entrada_inicio + ' - ' + janela.janela_entrada_fim : 'Saída: ' + janela.janela_saida_inicio + ' - ' + janela.janela_saida_fim})`
    };
  }
}
