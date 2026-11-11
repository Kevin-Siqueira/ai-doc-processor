import os
import httpx

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

def gerar_resumo_ia(texto: str) -> dict:
    """
    Processa o texto enviando para a API da OpenAI (se houver chave configurada)
    ou executa uma análise heurística/NLP como fallback.
    """
    # Se houver chave da OpenAI configurada nas variáveis de ambiente
    if OPENAI_API_KEY:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system", 
                        "content": "Você é um assistente especializado em resumir documentos e extrair pontos-chave em português."
                    },
                    {
                        "role": "user", 
                        "content": f"Resuma o seguinte texto e extraia 3 pontos principais:\n\n{texto}"
                    }
                ],
                "temperature": 0.5
            }
            
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                conteudo = data["choices"][0]["message"]["content"]
                
                return {
                    "provedor": "OpenAI (GPT)",
                    "resultado": conteudo
                }
        except Exception as e:
            print(f"Erro ao chamar OpenAI: {e}. Alternando para fallback de NLP.")

    # --- SIMULADOR DE PROCESSAMENTO DE IA (FALLBACK) ---
    # Usado para testes locais sem gastar créditos de API
    palavras = texto.split()
    total_palavras = len(palavras)
    
    # Pega as primeiras frases para compor o resumo
    frases = [f.strip() for f in texto.replace("\n", " ").split(".") if f.strip()]
    resumo_previa = ". ".join(frases[:2]) + "." if frases else texto[:150]
    
    resultado_simulado = (
        f"[Resumo Automático de IA]\n"
        f"O documento contém um total de {total_palavras} palavras.\n\n"
        f"**Prévia do Conteúdo:** {resumo_previa}\n\n"
        f"**Pontos Extraídos:**\n"
        f"1. Documento processado via pipeline assíncrono.\n"
        f"2. Extensão do texto: {len(texto)} caracteres.\n"
        f"3. Análise de densidade textual concluída com sucesso."
    )

    return {
        "provedor": "Simulador NLP / Modelo Local",
        "resultado": resultado_simulado
    }