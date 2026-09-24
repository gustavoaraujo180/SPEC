import { SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY } from '../config.js';

// Importa o cliente Supabase via CDN ESM
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm';

export const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY);

/**
 * Busca funcionário ativo pelo hash do QR Code
 * @param {string} qrcodeHash
 * @returns {Promise<Object|null>}
 */
export async function buscarFuncionarioPorQrCode(qrcodeHash) {
  const { data, error } = await supabase
    .from('funcionarios')
    .select('*')
    .eq('qrcode_hash', qrcodeHash)
    .eq('ativo', true)
    .single();

  if (error || !data) {
    return null;
  }
  return data;
}

/**
 * Busca a janela de horário configurada no sistema
 * @param {string} [funcionarioId] - ID opcional do funcionário se a tabela tiver relacionamento
 * @returns {Promise<Object|null>}
 */
export async function buscarJanelaHorario(funcionarioId) {
  let query = supabase.from('janelas_horario').select('*');

  if (funcionarioId) {
    const { data: funcJanela } = await query.eq('funcionario_id', funcionarioId).maybeSingle();
    if (funcJanela) return funcJanela;
  }

  const { data, error } = await supabase
    .from('janelas_horario')
    .select('*')
    .limit(1)
    .maybeSingle();

  if (error || !data) {
    return null;
  }
  return data;
}

/**
 * Registra uma batida de ponto aprovada
 * @param {Object} dadosPonto
 * @returns {Promise<Object>}
 */
export async function registrarPonto(dadosPonto) {
  const { funcionario_id, tipo_registro, foto_registro_url, hash_comprovante } = dadosPonto;

  const { data, error } = await supabase
    .from('registros_ponto')
    .insert([
      {
        funcionario_id,
        tipo_registro,
        foto_registro_url: foto_registro_url || '',
        hash_comprovante
      }
    ])
    .select()
    .single();

  if (error) {
    throw error;
  }
  return data;
}

/**
 * Registra uma ocorrência de erro ou tentativa fora da janela
 * @param {Object} dadosOcorrencia
 * @returns {Promise<Object>}
 */
export async function registrarOcorrencia(dadosOcorrencia) {
  const { funcionario_id, qrcode_lido, tipo_ocorrencia, foto_tentativa_url } = dadosOcorrencia;

  const { data, error } = await supabase
    .from('ocorrencias_ponto')
    .insert([
      {
        funcionario_id: funcionario_id || null,
        qrcode_lido: qrcode_lido || null,
        tipo_ocorrencia,
        foto_tentativa_url: foto_tentativa_url || null
      }
    ])
    .select()
    .single();

  if (error) {
    throw error;
  }
  return data;
}

/**
 * Faz upload de imagem base64/blob para o Supabase Storage ou retorna a string base64
 * @param {string} base64Data
 * @param {string} fileName
 * @returns {Promise<string>} URL da imagem ou data URL
 */
export async function salvarImagem(base64Data, fileName) {
  try {
    const byteCharacters = atob(base64Data.split(',')[1]);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'image/jpeg' });

    const { data, error } = await supabase.storage
      .from('fotos_ponto')
      .upload(fileName, blob, { contentType: 'image/jpeg', upsert: true });

    if (error) {
      return base64Data;
    }

    const { data: publicUrlData } = supabase.storage
      .from('fotos_ponto')
      .getPublicUrl(fileName);

    return publicUrlData.publicUrl || base64Data;
  } catch (err) {
    return base64Data;
  }
}
