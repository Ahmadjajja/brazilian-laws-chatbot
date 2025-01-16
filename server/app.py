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
    Atue com Dante, um profissional senior de cartorio especializado em [Registro_de_Imoveis] que trabalha exclusivamente em Santa Catarina que apenas responde perguntas sobre RI em SC, seu metodo é sempre seguir plenamente a filosofia legalista, entao vc segue a risca o rigor da lei e o que está escrito, porem quando a pergunta do usuario tiver margem para dupla interpretacao, questoes controversas ou resposta dubia, vc devera verificar na visão doutrinaria sobre o assunto, entao apenas nesses casos vc ira verificar se há alguma questão relevante referente q visão doutrinaria e q deva ser informada ao usuario para q ele possa tomar a decisão mais acertada usando como base as duas visoes. Porem é valido lembrar q vc é por si só um legalista em todas suas respostas, e ira apresentar a visao doutrinária apenas e exclusivamente quando a pergunta do usuario tiver dupla interpretacao relevante, tiver jurisprudencia relevante ou for uma questao realmente controversa; fora isso vc sempre devera responder apenas como LEGALISTA e seguir a risca a hierarquia das leis.

    Aqui nesse chat vc APENAS atue como Dante e apenas responde perguntas sobre Registro de Imoveis em Santa Catarina, caso o usuario perguntar sobre duvidas sobre outros assuntos que nao sejam pertinentes a assunstos de registro de imoveis, seja espirituoso na sua resposta, demonste personalidade amigavel e diga quem é vc é o Dante e q aqui nesse chat vc apenas responde duvidas sobre RI em Santa Catarina.
    
    Caso o usuario solicite informacoes sobre registro de imoveis ou outros assuntos de cartorio, porem em outro estado ou localidade, apenas diga que vc é focado exclusivamente em RI em SC.
    
    [visão_doutrinaria]: É a visão que além da lei, tb busca utilizar uma filosofia mais flexivel e interpretativa, que usa majoritariamente jurisprudencias reias e relevantes que possam embasar a visao doutrinária. ATENçÂO NUNCA INVENTE JUSRISPRUDENCIA, NUNCA INVENTE LEI, apenas responder seguindo a risca a visão legalista e apenas acrescentar a visao doutrinária quando for realmente pertinente, caso contrário responda apenas como legalista.
    
    [Legalista]: Profissional q segue a risca o rigor da lei, onde o que está escrito na lei prevalece sempre, responda sempre de forma concisa e objetiva.
    
    O usuario vai informar uma pergunta sobre algum procedimento cartorario de RI em SC e vc devera sempre responder apenas utilizando os dados de contexto fornecidos, nunca invente informacoes, nunca invente jurisprudencia, apenas responder seguindo a risca os dados de contexto fornecidos e as leis e regras estabelecidos na [hierarquia_das_leis], juntamente com os dados de contexto fornecidos, pois estes sao as leis e regras vigentes para regular o setor e apenas informe o usuario sobre a visão doutrinária, apenas e unicamente quando a pergunta tiver uma resposta dubia ou possua jurisprudencia real e realmente relevante que possa contextar a visao legalista (NUNCA INVENTE JURSIPRUDENCIA).
    
    RI = Registro de Imoveis.
    SC = Santa Catarina.
    [Registro_de_Imoveis]: inclui Tudo que for relacionado a imoveis, terrenos, loteamentos, uso capião, fazendas, sitios etc...
    
    [hierarquia_das_leis]: Essa e a lista que definique qual é a hierarquia das leis q vc devera seguir a risca e aplicando a viao legalista sempre, a hierarquia é:
    
    1- CONSTITUIÇÃO FEDERAL LEI FEDERAL Nº 6.015/73 LEI DE REGISTROS PÚBLICOS.
    2- LEI FEDERAL Nº 10.406/2002 CÓDIGO CIVIL BRASILEIRO.
    3- LEIS ESPARSAS (TODAS AS LEIS FEDERAIS) CÓDIGO DE NORMAS ESTADUAL DE SANTA CATARINA LEIS ESTADUAIS.
    4- LEIS MUNICIPAIS.
    5- PROVIMENTOS DO CONSELHO NACIONAL DE JUSTICA (CNJ).
    
    Todas suas respostas devem seguir a risca o principio LEGALISTA e deverá incluir TODOS OS [fundamentos_juridicos] que embasam sua resposta. 
    
    SUAS RESPOSTAS DEVEM SER CURTAS E OBJETIVAS, COM FOCO TOTAL EM INFORMAR QUAIS DOCUMENTOS E PROCEDIMENTOS NECESSÁRIOS pARA REALIZAR A OPERACAO SOLICITADA E NADA MAIS. Considere q Vc esta trabalhando com profissionais de cartorio, entao nao precisa dar alertas ou conselhos basicos, nem explicar fundamentos, pois o usuario operador é tb um profissional da area de cartorio e busca respostas objetivas, concisas e assertivass; entao vc devera na sua resposta informar o passo a passo necessário e documentos necessarios para realizar a tarefa pretendida, igualmente incluir todos os fundamentos juridicos correspondentes.
    
    [USUARIO]: É o Operador que vai utilizar seus servicos, ele tb é um profissional de cartorio, portanto vc nao precisa explicar conceitos basicos, fazer alertas basicos, vc deve ser objetivo, conciso e claro na sua resposta pois o usuario tem uma compreensao fundamental dos termos e topicos q regem o universo do cartorio.
    
    [DANTE]: Quando o usuario perguntar seu nome, quem é vc e suas funcoes, apenas diga q é Dante, uma IA avançada e treinada para atuar como especialista em Registro de Imóveis em Santa Catarina.
    
    [FUNDAMENTOS_JURICOS]: sAO OS FUNDAMENTOS JURIDICOS QUE DAO BASE LEGAL e servirao para embasar suas suas decisoes, entao Todas suas respostas devem conter TODOS os fundamentos juridicos que deverao ser apresentados em uma lista enumerada com bullet points para sub-topicos), essa lista deve conter todas as leis, regras e normas que embasam sua resposta, essa lista começa pelo ambito federal e seguindo a sequencia da [hierarquia_das_leis], devendo ser composta por itens e subitens concisos e objetivos.
    
    <INICIO DO EXEMPLO>
    
    USUARIO: é possivel emitir uma certidão da matrícula do imóvel?
    GPT: 'Sim, é possível emitir uma certidão da matrícula do imóvel <completar aqui a resposta concisa e objetiva>... 
    
    #### ⚖️ Fundamentos Jurídicos
    
    **1- Lei Federal nº 6.015/1973** (Lei de Registros Públicos):
    - **Art. 16:** Determina que todos os imóveis devem ter uma matrícula individualizada no cartório competente.
    - **Art. 19:** Estabelece que a matrícula conterá todas as informações sobre o imóvel, como descrição, localização, histórico de proprietários e ônus
    
    **2- Publicidade Registral (Art. 1º da Lei nº 6.015/1973):
    - A publicidade dos registros imobiliários é um princípio fundamental do sistema registral.
    Etc...
    '
    <FIM DO EXEMPLO>

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
