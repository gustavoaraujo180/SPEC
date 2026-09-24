/**
 * Serviço de Gerenciamento da Câmera usando Web MediaDevices API
 */

export class CameraService {
  constructor(videoElement, canvasElement) {
    this.videoElement = videoElement;
    this.canvasElement = canvasElement;
    this.stream = null;
    this.canvasContext = canvasElement ? canvasElement.getContext('2d') : null;
  }

  /**
   * Inicia o fluxo de vídeo da câmera do dispositivo
   */
  async startCamera() {
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user', width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false
      });
      this.videoElement.srcObject = this.stream;
      await this.videoElement.play();
      return true;
    } catch (error) {
      console.error('Erro ao acessar a câmera:', error);
      throw error;
    }
  }

  /**
   * Encerra o fluxo de vídeo da câmera
   */
  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
  }

  /**
   * Captura o frame atual do vídeo no canvas
   * @returns {ImageData|null}
   */
  captureFrame() {
    if (!this.videoElement || this.videoElement.readyState !== this.videoElement.HAVE_ENOUGH_DATA) {
      return null;
    }

    this.canvasElement.width = this.videoElement.videoWidth;
    this.canvasElement.height = this.videoElement.videoHeight;
    this.canvasContext.drawImage(
      this.videoElement,
      0,
      0,
      this.canvasElement.width,
      this.canvasElement.height
    );

    return this.canvasContext.getImageData(
      0,
      0,
      this.canvasElement.width,
      this.canvasElement.height
    );
  }

  /**
   * Captura uma imagem em formato Data URL (base64 JPEG)
   * @returns {string}
   */
  getSnapshotDataUrl() {
    if (!this.canvasElement) return '';
    return this.canvasElement.toDataURL('image/jpeg', 0.85);
  }
}
