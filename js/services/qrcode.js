// Importa jsQR via CDN ESM
import jsQR from 'https://cdn.jsdelivr.net/npm/jsqr@1.4.0/+esm';

/**
 * Serviço para decodificação de QR Code a partir de ImageData
 */
export class QrCodeService {
  /**
   * Tenta decodificar o código QR no frame de imagem fornecido
   * @param {ImageData} imageData
   * @returns {string|null} Código decodificado ou null se não for encontrado
   */
  static decodeFrame(imageData) {
    if (!imageData) return null;

    const code = jsQR(imageData.data, imageData.width, imageData.height, {
      inversionAttempts: 'dontInvert'
    });

    if (code && code.data && code.data.trim() !== '') {
      return code.data.trim();
    }

    return null;
  }
}
