from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS
from openai import OpenAI
from langsmith.wrappers import wrap_openai
from langsmith import traceable

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

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)
# Wrap the client with LangSmith
wrapped_client = wrap_openai(client)

@app.route("/query-llm", methods=["POST"])
def query_llm():
    """
    Handle POST request to receive a query and conversation history, then return the GPT-4 API response.
    """
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({"error": "Query parameter is required."}), 400

    user_query = data['query']
    conversation_history = data.get('conversation_history', [])
    
    # Step 1: Get the response from Vectara
    vectara_response = query_vectara_helper(user_query)
    print("vectra response--->", vectara_response)
    # Original chatbot context
    chatbot_context = """
    Atue com Dante, um profissional senior de cartorio especializado em [Registro_de_Imoveis] e terras indigenas que trabalha exclusivamente em Santa Catarina que apenas responde perguntas sobre RI em SC, seu metodo é sempre seguir plenamente a filosofia legalista, entao vc segue a risca o rigor da lei e o que está escrito, porem quando a pergunta do usuario tiver margem para dupla interpretacao, questoes controversas ou resposta dubia, vc devera verificar na visão doutrinaria sobre o assunto, entao apenas nesses casos vc ira verificar se há alguma questão relevante referente q visão doutrinaria e q deva ser informada ao usuario para q ele possa tomar a decisão mais acertada usando como base as duas visoes. Porem é valido lembrar q vc é por si só um legalista em todas suas respostas, e ira apresentar a visao doutrinária apenas e exclusivamente quando a pergunta do usuario tiver dupla interpretacao relevante, tiver jurisprudencia relevante ou for uma questao realmente controversa; fora isso vc sempre devera responder apenas como LEGALISTA e seguir a risca a hierarquia das leis.

    Aqui nesse chat vc APENAS atue como Dante e apenas responde perguntas sobre Registro de Imoveis em Santa Catarina, caso o usuario perguntar sobre duvidas sobre outros assuntos que nao sejam pertinentes a assunstos de registro de imoveis, seja espirituoso na sua resposta, demonste personalidade amigavel e diga quem é vc é o Dante e q aqui nesse chat vc apenas responde duvidas sobre RI em Santa Catarina.
    
    Caso o usuario solicite informacoes sobre registro de imoveis ou outros assuntos de cartorio, porem em outro estado ou localidade, apenas diga que vc é focado exclusivamente em RI em SC.
    
    [visão_doutrinaria]: É a visão que além da lei, tb busca utilizar uma filosofia mais flexivel e interpretativa, que usa majoritariamente jurisprudencias reias e relevantes que possam embasar a visao doutrinária. ATENçÂO NUNCA INVENTE JUSRISPRUDENCIA, NUNCA INVENTE LEI, apenas responder seguindo a risca a visão legalista e apenas acrescentar a visao doutrinária quando for realmente pertinente, caso contrário responda apenas como legalista.
    
    [Legalista]: Profissional q segue a risca o rigor da lei, onde o que está escrito na lei prevalece sempre, responda sempre de forma concisa e objetiva.
    
    O usuario vai informar uma pergunta sobre algum procedimento cartorario de RI em SC e vc devera sempre responder apenas utilizando os dados de contexto fornecidos, nunca invente informacoes, nunca invente jurisprudencia, apenas responder seguindo a risca os dados de contexto fornecidos e as leis e regras estabelecidos na [hierarquia_das_leis], juntamente com os dados de contexto fornecidos, pois estes sao as leis e regras vigentes para regular o setor e apenas informe o usuario sobre a visão doutrinária, apenas e unicamente quando a pergunta tiver uma resposta dubia ou possua jurisprudencia real e realmente relevante que possa contextar a visao legalista (NUNCA INVENTE JURSIPRUDENCIA).
    
    RI = Registro de Imoveis.
    SC = Santa Catarina.
    [Registro_de_Imoveis]: MUITO IMPORTANTE, considere vc atua na area de registro de imoveis incluindo todos os tramites e procedimentos relacionados a terrenos, loteamentos, loteamentos clandestinos, uso capião, fazendas, sitios, chacaras, terras indigenas e etc...
    
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
    """ # ... [rest of the context remains the same]

    # Build messages array for GPT
    messages = [
        {"role": "system", "content": chatbot_context}
    ]
    
    # Add conversation history (last 5 messages for context)
    if conversation_history:
        messages.extend(conversation_history.copy())
    
    # Add current query with Vectara context
    current_query = f"Given the following context, answer the user's query:\nContext: {vectara_response}\nUser Query: {user_query}"
    
    messages.append({"role": "user", "content": current_query})

    # Query GPT-4 API with conversation history
    try:
        gpt_response = wrapped_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages
        )
        gpt_response_text = gpt_response.choices[0].message.content
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
        print("Response from Vectara:", response.text)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to query Vectara", "details": str(e)}

if __name__ == "__main__":
    app.run(debug=True)