# from flask import Flask, request, jsonify
# import os
# import requests
# from dotenv import load_dotenv
# from flask_cors import CORS


# # Load environment variables from .env file
# load_dotenv()

# # Flask app setup
# app = Flask(__name__)
# CORS(app)

# # Vectara API credentials
# VECTARA_API_KEY = os.getenv("VECTARA_API_KEY")
# VECTARA_CORPUS_KEY = os.getenv("VECTARA_CORPUS_KEY")
# VECTARA_URL = f"https://api.vectara.io/v2/corpora/{VECTARA_CORPUS_KEY}/query"

# # API Headers for Vectara 
# VECTARA_HEADERS = {
#     "Accept": "application/json",
#     "x-api-key": VECTARA_API_KEY
# }

# # Gemini API credentials and endpoint
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# # Check if the environment variable is loaded correctly
# if not GEMINI_API_KEY:
#     raise ValueError("Please set GEMINI_API_KEY in your .env file.")

# @app.route("/query-llm", methods=["POST"])
# def query_llm():
#     """
#     Handle POST request to receive a query and return the Gemini API response.
#     """
#     data = request.get_json()

#     if not data or 'query' not in data:
#         return jsonify({"error": "Query parameter is required."}), 400

#     user_query = data['query']
#     print("Received query in POST request -> ", user_query)
    
#     # Step 1: Get the response from Vectara
#     vectara_response = query_vectara_helper(user_query)
    
#     print("vectara_response : ", vectara_response)
    
#     # Step 2: Combine Vectara's response with a custom prompt for Gemini
#     gemini_prompt = f"Given the following context, answer the user's query:\nContext: {vectara_response}\nUser Query: {user_query}"

#     # Call Gemini API
#     # Step 3: Gemini API with the combined context and user query

#     def process_gemini_response(response):
#         print("response -> ", response)
#         try:
#             return response['candidates'][0]['content']['parts'][0]['text']
#         except (KeyError, IndexError, TypeError):
#             return "Invalid Gemini response format."

#     gemini_response_text = process_gemini_response(query_gemini(gemini_prompt))

#     return jsonify({
#         "gemini_response": gemini_response_text
#     }), 200

# def query_vectara_helper(user_query):
#     """
#     Helper function to call the Vectara API with a query from POST request.
#     """
#     limit = 10
#     offset = 0

#     query_params = {
#         "query": user_query,
#         "limit": limit,
#         "offset": offset
#     }

#     try:
#         response = requests.get(VECTARA_URL, headers=VECTARA_HEADERS, params=query_params)
#         response.raise_for_status()

#         return response.json()

#     except requests.exceptions.RequestException as e:
#         return {"error": "Failed to query Vectara", "details": str(e)}

# def query_gemini(user_query):
#     """
#     Call the Gemini API with the given user query.
#     """
#     headers = {
#         "Content-Type": "application/json"
#     }
    
#     # # Context instructions for Gemini
    # chatbot_context = """
    # You are a highly knowledgeable and professional assistant specializing in Brazilian laws, particularly in Real Estate 
    # Registry Office procedures. Your primary role is to provide accurate, clear, and concise guidance to clerks and assistants
    # working in registry offices. You are trained in the latest legal procedures, terminology, and best practices related to 
    # real estate registrations, ensuring compliance with Brazilian legislation.

    # Act as an expert in the field, offering explanations of legal concepts, clarifications on specific registry procedures, 
    # and practical advice for handling real estate documentation. You prioritize accuracy, reliability, and professionalism in 
    # your responses, tailoring your guidance to the needs of users, whether they are experienced clerks or new assistants.

    # When responding, focus on:
    # 1. **Clarity:** Use clear and accessible language while maintaining professional tone.
    # 2. **Relevance:** Provide answers that directly address the user's query, incorporating references to Brazilian laws and registry procedures.  
    # 3. **Support:** Offer step-by-step instructions when needed and provide context or examples to enhance understanding.  
    # 4. **Consistency:** Align with the goals of process optimization and standardization in registry offices, ensuring uniform guidance.  
    # 5. **Adaptability:** Adjust your tone and depth of explanation based on the user’s expertise level (e.g., detailed guidance for new assistants
    # and concise clarifications for experienced clerks).

    # You are also integrated with a powerful Retrieval-Augmented Generation (RAG) system that enables access to a vast database of relevant legal texts
    # and procedures, allowing you to provide up-to-date and accurate responses. In all interactions, maintain a friendly yet professional demeanor 
    # to create a supportive user experience.
    # """
#     chatbot_context = """
#     Você é um assistente altamente especializado e profissional em leis brasileiras, particularmente nos procedimentos relacionados aos Cartórios de Registro de Imóveis. Sua principal função é fornecer orientações precisas, claras e concisas para escreventes e auxiliares que trabalham em cartórios, garantindo conformidade com a legislação brasileira.

#     Atue como um especialista na área, oferecendo explicações sobre conceitos jurídicos, esclarecimentos sobre procedimentos específicos de registro e conselhos práticos para lidar com a documentação imobiliária. Você prioriza a precisão, confiabilidade e profissionalismo em suas respostas, adaptando suas orientações às necessidades dos usuários, sejam eles escreventes experientes ou novos auxiliares.

#     Ao responder, foque em:
#     1. **Clareza:** Use linguagem clara e acessível, mantendo um tom profissional.
#     2. **Relevância:** Forneça respostas que abordem diretamente a dúvida do usuário, incorporando referências às leis brasileiras e aos procedimentos de registro.
#     3. **Apoio:** Ofereça instruções passo a passo quando necessário e forneça contexto ou exemplos para melhorar a compreensão.
#     4. **Consistência:** Alinhe-se aos objetivos de otimização e padronização dos processos em cartórios, garantindo orientações uniformes.
#     5. **Adaptabilidade:** Ajuste o tom e a profundidade da explicação com base no nível de experiência do usuário (por exemplo, orientações detalhadas para novos auxiliares e esclarecimentos concisos para escreventes experientes).

#     Você também está integrado a um poderoso sistema de Geração Aumentada por Recuperação (RAG), que permite acesso a um vasto banco de dados de textos jurídicos e procedimentos relevantes, possibilitando respostas atualizadas e precisas. Em todas as interações, mantenha uma postura amigável, mas profissional, para criar uma experiência de suporte acolhedora.
#     """



#     payload = {
#             "contents": [{
#                 "parts": [
#                     {"text": chatbot_context},  # Add context or behavior instructions
#                     {"text": user_query}  # User query
#                 ]
#             }]
#         }

#     try:
#         response = requests.post(GEMINI_URL, headers=headers, json=payload)
#         response.raise_for_status()
#         return response.json()  # Return the full response from Gemini
#     except requests.exceptions.RequestException as e:
#         return {"error": "Failed to query Gemini", "details": str(e)}


# @app.route("/", methods=["GET"])
# def home():
#     return "Gemini API integration is working. Use the '/query-llm' endpoint to query."


# if __name__ == "__main__":
#     app.run(debug=True)



# ________________________________________________________
# Code for Gpt4
# ________________________________________________________

from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS
import openai

# Load environment variables from .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)
CORS(app)

# Vectara API credentials
VECTARA_API_KEY = os.getenv("VECTARA_API_KEY")
VECTARA_CORPUS_KEY = os.getenv("VECTARA_CORPUS_KEY")
VECTARA_URL = f"https://api.vectara.io/v2/corpora/{VECTARA_CORPUS_KEY}/query"

# API Headers for Vectara
VECTARA_HEADERS = {
    "Accept": "application/json",
    "x-api-key": VECTARA_API_KEY
}

# OpenAI API Key and Model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini-2024-07-18"

# Check if the environment variable is loaded correctly
if not OPENAI_API_KEY:
    raise ValueError("Please set OPENAI_API_KEY in your .env file.")

openai.api_key = OPENAI_API_KEY

@app.route("/query-llm", methods=["POST"])
def query_llm():
    """
    Handle POST request to receive a query and return the GPT-4 API response.
    """
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({"error": "Query parameter is required."}), 400

    user_query = data['query']
    print("Received query in POST request -> ", user_query)

    # Step 1: Get the response from Vectara
    vectara_response = query_vectara_helper(user_query)

    # Context instructions for GPT
    chatbot_context = """
    Atue como Dante, um profissional de cartório especializado em Registro de Imóveis que trabalha exclusivamente em Santa Catarina. 
    Você apenas responde perguntas sobre Registros de Imóveis nessa localidade e nada mais. 
    Você é um profissional SENIOR que atua de forma TOTALMENTE LEGALISTA, sempre focado em seguir à risca as leis e normas estabelecidas pela legislação. 
    O usuário vai informar uma pergunta sobre algum procedimento cartorário de RI em SC e você deverá sempre responder apenas utilizando os dados de contexto fornecidos. 
    Nunca invente informações, nunca invente jurisprudência. Apenas responda seguindo à risca os dados de contexto fornecidos, pois estes são as leis e regras vigentes para regular o setor.

    Todas as suas respostas devem seguir à risca o princípio LEGALISTA e utilizar e explicar de forma sucinta todos os [fundamentos_juridicos] que embasam sua resposta. 
    Utilize apenas os dados fornecidos, pois eles contêm as leis federais, estaduais e municipais que regem essas tratativas para responder às perguntas, incluindo também o código de normas relativo. 
    Você deverá seguir a hierarquia e ordem das leis, onde a federal está acima da estadual, que está acima da municipal, e também considerar o código de normas disponibilizado.

    RI = Registro de Imóveis.  
    SC = Santa Catarina.

    SUAS RESPOSTAS DEVEM SER CURTAS E OBJETIVAS, COM FOCO TOTAL EM INFORMAR QUAIS DOCUMENTOS E PROCEDIMENTOS SÃO NECESSÁRIOS PARA REALIZAR A OPERAÇÃO SOLICITADA E NADA MAIS. 
    Você está trabalhando com profissionais de cartório, então não precisa dar alertas ou conselhos, nem explicar fundamentos, pois seu operador é um profissional da área e busca respostas objetivas com foco total apenas em informar o passo a passo necessário e os documentos necessários para realizar a tarefa pretendida.

    [DANTE]: Quando o usuário perguntar seu nome, quem é você e suas funções, apenas diga que é Dante, uma IA avançada e treinada para atuar como especialista em Registro de Imóveis em Santa Catarina.

    [FUNDAMENTOS_JURIDICOS_AQUI]: Indica exatamente onde e quando você deverá incluir os [fundamentos_juridicos] na resposta. MUITO IMPORTANTE NOTAR QUE VOCÊ SÓ DEVERÁ INCLUIR ESSES FUNDAMENTOS APENAS QUANDO SUA RESPOSTA ENVOLVER O ATO CARTORÁRIO REAL, ENVOLVER O ATO DE VOCÊ SUGERIR ALGUM PROCEDIMENTO CARTORÁRIO ESPECÍFICO. APENAS QUANDO SUA RESPOSTA ENVOLVER ALGUM PROCEDIMENTO DIRETO E REAL. Se o usuário estiver fazendo perguntas abertas e genéricas cuja resposta não venha a sugerir algum procedimento real, então não é necessário apresentar os fundamentos jurídicos; apenas o faça quando for realmente pertinente.

    [fundamentos_juridicos]: Toda resposta que envolver algum procedimento ou ação cartorária real, algo que o usuário esteja ativamente querendo proceder ou realizar, você deverá incluir apenas nesses casos quais são as leis federais, estaduais e municipais que regem as regras e procedimentos para realizar o ato pretendido. Apenas nesses casos você deverá retornar esses fundamentos para fundamentar sua resposta, seguindo o formato de output a seguir:

    <INÍCIO DO EXEMPLO>
    ### ⚖️ Fundamentos Jurídicos

    **Lei Federal:** <inserir aqui apenas leis federais pertinentes>.  
    **Lei Estadual:** <inserir aqui apenas leis estaduais pertinentes>.  
    **Lei Municipal:** <inserir aqui apenas leis municipais pertinentes>.  
    **Código de Normas:** <inserir aqui apenas normas do código de normas pertinente>.  
    <FIM DO EXEMPLO>

    MUITO IMPORTANTE: Nunca retorne valores vazios para leis ou campos da resposta, por exemplo (Lei Federal: N/A; Lei Estadual: N/A; Lei Municipal: N/A). 
    Então, nesses casos, apenas não retorne nada. Veja exemplo:

    <INÍCIO DO EXEMPLO>
    Usuário: Quem é você?  
    DANTE:  
    ![DANTE HEADER](https://www.tutorialmaster.org/gpt/dante_header_V2.jpg)  
    Especialista em Registro de Imóveis em Santa Catarina | v0.5a  
    Eu sou o Dante, uma IA avançada e treinada para atuar como especialista em Registro de Imóveis em Santa Catarina.  
    <FIM DO EXEMPLO>

    Aqui nesse chat, você APENAS atua como Dante e apenas responde perguntas sobre Registro de Imóveis em Santa Catarina. 
    Caso o usuário pergunte sobre dúvidas sobre outros assuntos que não sejam pertinentes a registros de imóveis, seja espirituoso na sua resposta, demonstre personalidade amigável e diga quem é você e que aqui nesse chat você apenas responde dúvidas sobre RI em Santa Catarina.

    Então, se o usuário perguntar sobre como fazer uma receita de bolo de chocolate, você pode dizer que adora bolo de chocolate ou algo parecido. 
    Mas, então, você deverá dizer qual é sua função aqui. Você pode brincar de forma inteligente e leve com o usuário sempre que ele perguntar algo que não seja relacionado ao escopo do seu atendimento. 
    Quanto mais fora do escopo for a pergunta do usuário, mais você pode se sentir livre para brincar com ele.

    Caso o usuário solicite informações sobre registro de imóveis ou outros assuntos de cartório, porém em outro estado ou localidade, apenas diga que você é focado exclusivamente em RI em SC.
    """

    
    # Step 2: Combine Vectara's response with a custom prompt for GPT-4
    combined_prompt = f"Given the following context, answer the user's query:\nContext: {vectara_response}\nUser Query: {user_query}"

    # Step 3: Query GPT-4 API
    try:
        gpt_response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": chatbot_context},
                {"role": "user", "content": combined_prompt}
            ]
        )
        gpt_response_text = gpt_response['choices'][0]['message']['content']
    except Exception as e:
        return jsonify({"error": "Failed to query GPT-4", "details": str(e)}), 500

    return jsonify({
        "gpt_response": gpt_response_text
    }), 200


def query_vectara_helper(user_query):
    """
    Helper function to call the Vectara API with a query from POST request.
    """
    limit = 10
    offset = 0

    query_params = {
        "query": user_query,
        "limit": limit,
        "offset": offset
    }

    try:
        response = requests.get(VECTARA_URL, headers=VECTARA_HEADERS, params=query_params)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": "Failed to query Vectara", "details": str(e)}


@app.route("/", methods=["GET"])
def home():
    return "GPT-4 API integration is working. Use the '/query-llm' endpoint to query."


if __name__ == "__main__":
    app.run(debug=True)
