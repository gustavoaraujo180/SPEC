import { CameraService } from './services/camera.js';
import { QrCodeService } from './services/qrcode.js';
import { ToleranceService } from './services/tolerance.js';
import { TicketComponent } from './components/ticket.js';
import { initIcons } from './components/icons.js';
import {
  buscarFuncionarioPorQrCode,
  buscarJanelaHorario,
  registrarPonto,
  registrarOcorrencia,
  salvarImagem
} from './services/supabase.js';

// Seletores DOM
const videoElement = document.getElementById('webcam-video');
const canvasElement = document.getElementById('snapshot-canvas');
const liveClockElement = document.getElementById('live-clock');

const modalOverlay = document.getElementById('feedback-modal');
const modalIconBox = document.getElementById('modal-icon-box');
const modalIcon = document.getElementById('modal-icon');
const modalTitle = document.getElementById('modal-title');
const modalMessage = document.getElementById('modal-message');
const modalDetails = document.getElementById('modal-details');
const detailNome = document.getElementById('detail-nome');
const detailMatricula = document.getElementById('detail-matricula');
const detailHorario = document.getElementById('detail-horario');
const btnCloseModal = document.getElementById('btn-close-modal');

// Estado da Aplicação
let cameraService = null;
let isScanning = true;
let isProcessing = false;
let modalTimeout = null;

/**
 * Atualiza o relógio em tempo real no cabeçalho
 */
function updateClock() {
  const now = new Date();
  if (liveClockElement) {
    liveClockElement.textContent = now.toLocaleTimeString('pt-BR');
  }
}

/**
 * Exibe modal de feedback na tela
 * @param {boolean} success - Se foi aprovado ou bloqueado/erro
 * @param {string} title
 * @param {string} message
 * @param {Object|null} details
 */
function showModal(success, title, message, details = null) {
  modalTitle.textContent = title;
  modalMessage.textContent = message;

  if (success) {
    modalIconBox.className = 'modal-icon-container success';
    modalIconBox.innerHTML = '<i data-lucide="check-circle-2" style="width: 36px; height: 36px;"></i>';
  } else {
    modalIconBox.className = 'modal-icon-container danger';
    modalIconBox.innerHTML = '<i data-lucide="alert-triangle" style="width: 36px; height: 36px;"></i>';
  }

  if (details) {
    modalDetails.style.display = 'block';
    detailNome.textContent = details.nome || '-';
    detailMatricula.textContent = details.matricula || '-';
    detailHorario.textContent = details.horario || new Date().toLocaleTimeString('pt-BR');
  } else {
    modalDetails.style.display = 'none';
  }

  initIcons();
  modalOverlay.classList.add('active');

  // Fecha o modal automaticamente após 5 segundos se não for fechado manualmente
  if (modalTimeout) clearTimeout(modalTimeout);
  modalTimeout = setTimeout(() => {
    closeModal();
  }, 5000);
}

/**
 * Fecha o modal e retoma o escaneamento
 */
function closeModal() {
  modalOverlay.classList.remove('active');
  if (modalTimeout) clearTimeout(modalTimeout);
  isProcessing = false;
  isScanning = true;
}

/**
 * Loop principal de escaneamento de quadros da câmera
 */
async function scanLoop() {
  if (isScanning && !isProcessing && cameraService) {
    const imageData = cameraService.captureFrame();
    if (imageData) {
      const qrCode = QrCodeService.decodeFrame(imageData);
      if (qrCode) {
        await processQrCodeScan(qrCode);
      }
    }
  }
  requestAnimationFrame(scanLoop);
}

/**
 * Processa a leitura de um QR Code detectado
 * @param {string} qrcodeData
 */
async function processQrCodeScan(qrcodeData) {
  isProcessing = true;
  isScanning = false;

  const snapshotBase64 = cameraService.getSnapshotDataUrl();
  const timestamp = new Date();

  try {
    // 1. Busca funcionário no banco
    const funcionario = await buscarFuncionarioPorQrCode(qrcodeData);

    if (!funcionario) {
      // QR Code Inválido ou funcionário não encontrado / inativo
      const fotoUrl = await salvarImagem(snapshotBase64, `ocorrencias/qrcode_invalido_${Date.now()}.jpg`);
      await registrarOcorrencia({
        funcionario_id: null,
        qrcode_lido: qrcodeData,
        tipo_ocorrencia: 'QRCODE_INVALIDO',
        foto_tentativa_url: fotoUrl
      });

      showModal(false, 'Acesso Negado', 'QR Code do crachá é inválido ou funcionário está inativo.');
      return;
    }

    // 2. Busca Janela de Horário
    const janela = await buscarJanelaHorario(funcionario.id);
    const resultadoValidacao = ToleranceService.validarJanelaPonto(janela, timestamp);

    if (resultadoValidacao.aprovado) {
      // BATIDA APROVADA
      const hashComprovante = TicketComponent.gerarHashComprovante();
      const fotoUrl = await salvarImagem(snapshotBase64, `registros/${funcionario.matricula}_${Date.now()}.jpg`);

      await registrarPonto({
        funcionario_id: funcionario.id,
        tipo_registro: resultadoValidacao.tipoRegistro,
        foto_registro_url: fotoUrl,
        hash_comprovante: hashComprovante
      });

      const dadosTicket = {
        nome: funcionario.nome,
        matricula: funcionario.matricula,
        tipoRegistro: resultadoValidacao.tipoRegistro,
        dataHora: timestamp,
        hashComprovante: hashComprovante
      };

      // Emite Ticket
      TicketComponent.imprimirTicket(dadosTicket);

      showModal(
        true,
        'Ponto Registrado!',
        `${resultadoValidacao.mensagem} Comprovante gerado com sucesso.`,
        {
          nome: funcionario.nome,
          matricula: funcionario.matricula,
          horario: timestamp.toLocaleTimeString('pt-BR')
        }
      );
    } else {
      // BATIDA BLOQUEADA (FORA DA JANELA)
      const fotoUrl = await salvarImagem(snapshotBase64, `ocorrencias/fora_janela_${funcionario.matricula}_${Date.now()}.jpg`);

      await registrarOcorrencia({
        funcionario_id: funcionario.id,
        qrcode_lido: qrcodeData,
        tipo_ocorrencia: resultadoValidacao.motivoOcorrencia,
        foto_tentativa_url: fotoUrl
      });

      showModal(
        false,
        'Batida Bloqueada!',
        resultadoValidacao.mensagem,
        {
          nome: funcionario.nome,
          matricula: funcionario.matricula,
          horario: timestamp.toLocaleTimeString('pt-BR')
        }
      );
    }
  } catch (error) {
    console.error('Erro no processamento da batida:', error);
    showModal(false, 'Erro no Sistema', 'Ocorreu uma falha ao comunicar com o servidor. Tente novamente.');
  }
}

/**
 * Inicialização do app
 */
async function initApp() {
  initIcons();
  setInterval(updateClock, 1000);
  updateClock();

  if (btnCloseModal) {
    btnCloseModal.addEventListener('click', closeModal);
  }

  cameraService = new CameraService(videoElement, canvasElement);

  try {
    await cameraService.startCamera();
    requestAnimationFrame(scanLoop);
  } catch (err) {
    console.error('Falha ao inicializar a câmera:', err);
    showModal(false, 'Erro de Câmera', 'Não foi possível acessar a câmera do dispositivo. Verifique as permissões.');
  }
}

document.addEventListener('DOMContentLoaded', initApp);
