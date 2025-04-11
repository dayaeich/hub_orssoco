from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

# Notion
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# OpenRouter (análises de transcrição)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# AssemblyAI (transcrição de áudios)
ASSEMBLY_API_KEY = os.getenv("ASSEMBLY_API_KEY")

# OpenAI (Assistente para responder no Telegram)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Mapeamento dos prompts para análise automática
PROMPTS = {
    "Transcrição - Qualificação": (
        "Analise a transcrição de qualificação a seguir.\n"
        "Responda e dê insights nos seguintes tópicos:\n"
        "1. Budget (quanto o cliente pode investir)\n"
        "2. Authority (quem toma a decisão)\n"
        "3. Need (o que o cliente realmente precisa)\n"
        "4. Timing (prazo para a solução)\n\n"
        "Se não encontrar alguma informação, escreva exatamente 'Informação não fornecida'.\n"
        "Além disso, analise o perfil do cliente, possíveis objeções, pontos relevantes da reunião "
        "e a melhor estratégia para o closer criar vínculo com o cliente.\n"
        "Não invente informações. Seja objetivo e siga a ordem dos tópicos."
    ),
    "Transcrição - Vendas": (
        "Analise a transcrição de reunião de vendas e preencha rigorosamente os seguintes campos:\n\n"
        "Resumo da Reunião\n"
        "Participantes:\n"
        "Contexto do Cliente:\n\n"
        "Visão Geral do Negócio:\n\n"
        "Dores Identificadas\n"
        "1.\n"
        "2.\n"
        "3.\n\n"
        "Desejos e Objetivos do Cliente\n"
        "Objetivo Principal com a V4:\n"
        "Metas de Faturamento / ROI Esperado:\n"
        "KPI’s desejados:\n\n"
        "Necessidades Percebidas\n"
        "-\n"
        "-\n"
        "-\n\n"
        "Estrutura Comercial e de Marketing\n"
        "Time de Vendas:\n"
        "Time de Marketing:\n"
        "CRM utilizado:\n"
        "Investimento atual em marketing:\n"
        "Principais Canais Atuais:\n"
        "Stakeholders (Nome, Cargo, Contato):\n\n"
        "Estratégia Proposta pela V4\n"
        "Canais recomendados:\n"
        "Proposta de estruturação comercial e marketing:\n"
        "Ponto de atenção / limitações do cliente:\n"
        "Métricas de validação:\n\n"
        "Insights (intuição do vendedor)\n"
        "Tom de decisão do cliente:\n"
        "Preocupações implícitas percebidas:\n"
        "O que o cliente valorizou na conversa:\n"
        "Objeções levantadas e como foram tratadas:\n"
        "Observações adicionais relevantes para operação:\n"
        "Oportunidades de upsell:\n\n"
        "Se alguma informação não for dita, escreva exatamente: 'Informação não fornecida'.\n"
        "Não invente dados. Respeite a ordem dos tópicos."
    ),
    "Transcrição - GrowthClass": (
        "Analise a transcrição da Growth Class seguindo:\n"
        "1. Insights sobre o comportamento do cliente.\n"
        "2. Adesão a soluções propostas.\n"
        "3. Oportunidades de cross-sell.\n"
        "4. Validação do commitment ao processo.\n"
        "5. Entendimento dos prazos.\n\n"
        "Siga exatamente a ordem dos tópicos. Não invente informações."
    ),
    "Transcrição - kickoff": (
    "Analise a transcrição do Kickoff e responda cuidadosamente às perguntas abaixo:\n\n"
    "1. Conte sobre a empresa.\n"
    "2. Liste os principais envolvidos no projeto (nome, cargo e e-mail).\n"
    "3. Motivos para escolha da empresa em relação a outros fornecedores.\n"
    "4. Faturamento mensal atual da empresa.\n"
    "5. Margem de lucro atual.\n"
    "6. Margem de contribuição.\n"
    "7. Ticket médio atual.\n"
    "8. Tempo médio entre prospecção e fechamento de venda.\n"
    "9. Existe recorrência de compra? Se sim, qual o intervalo?\n"
    "10. Descrição dos principais produtos ou serviços (funcionalidades, atributos e percepção do cliente).\n"
    "11. Três maiores obstáculos de marketing e vendas.\n"
    "12. Principais concorrentes.\n"
    "13. Momento atual da empresa (queda, crescimento, estagnação).\n"
    "14. Metas de performance em marketing e vendas (se houver).\n"
    "15. Análise SWOT:\n"
    "    - Strengths/Forças\n"
    "    - Weaknesses/Fraquezas\n"
    "    - Opportunities/Oportunidades\n"
    "    - Threats/Ameaças\n"
    "16. Possui contas de anúncio? (Listar acessos se informado).\n"
    "17. Classe social predominante do público (A, B, C ou D).\n"
    "18. Faixa etária predominante do público.\n"
    "19. Gênero predominante do público.\n"
    "20. Três principais objeções de compra.\n"
    "21. Existe manual da marca/brandbook? (Inserir link, se houver).\n"
    "22. Existe pasta de fotos? (Inserir link, se houver).\n"
    "23. Cores que devem ser usadas.\n"
    "24. Cores que não devem ser usadas.\n"
    "25. Referências e inspirações (links, se informados).\n"
    "26. Descrição do processo de vendas atual (jornada do cliente, estrutura do time, ferramentas usadas).\n"
    "27. Três critérios para lead bem qualificado.\n"
    "28. Peculiaridades sazonais do negócio (momentos positivos e negativos).\n\n"
    "⚡ Importante:\n"
    "- Caso alguma informação não seja mencionada na transcrição, responda exatamente: 'Informação não fornecida'.\n"
    "- Não invente dados.\n"
    "- Responda de forma clara, objetiva e fiel ao que foi falado na gravação.\n"
    ),
    "Transcrição - Benchmark": (
        "A partir da gravação de Benchmark, gere insights estratégicos e comparativos reais.\n"
        "Seja objetivo. Baseie-se apenas no que foi falado. Sem invenções."
    ),
    "Transcrição - Growth Storm": (
        "Analise todos os pontos abordados na reunião e documente de forma objetiva.\n"
        "Elimine a necessidade de apresentações em PPT, siga apenas fatos ditos na gravação."
    ),
    "Transcrição - aprovação do planejamento": (
        "Analise a reunião de aprovação do planejamento:\n"
        "1. Identifique momentos de entendimento, confusão, distração, concordância, discordância, "
        "insegurança e insatisfação.\n"
        "2. Gere insights específicos para reforço em futuras reuniões.\n\n"
        "Baseie-se apenas no que foi falado. Não invente informações."
    ),
    "Transcrição - Checkin": (
        "Analise o Check-in:\n"
        "1. Complete o perfil pessoal e profissional (hobbies, família, novos projetos).\n"
        "2. Atualize o Health Score com base na participação, entrega e percepção de ROI.\n\n"
        "Seja objetivo e baseado somente na gravação."
    ),
    "Sentimento - padrão": (
    "Com base na transcrição da reunião, execute as seguintes tarefas:\n\n"
    "1. Atribua uma nota de 1 a 5 para o sentimento geral do cliente em relação ao projeto, seguindo as diretrizes abaixo:\n"
    "   - 5: Cliente muito entusiasmado e positivo. Demonstra grande interesse, concordância e envolvimento.\n"
    "   - 4: Cliente majoritariamente positivo, mas com pequenas dúvidas ou hesitações.\n"
    "   - 3: Cliente neutro. Mostra interesse moderado, ou demonstra dúvidas e hesitações relevantes.\n"
    "   - 2: Cliente com sentimento negativo moderado. Demonstra ceticismo, preocupação ou desconforto.\n"
    "   - 1: Cliente claramente insatisfeito, desinteressado ou resistente.\n\n"
    "2. Justifique a nota do cliente citando comportamentos, falas e atitudes específicas observadas na transcrição.\n"
    "   - Use exemplos reais, como: 'O cliente disse frases como \"sim\", \"entendi\", \"faz sentido\" indicando aprovação.'\n"
    "   - Ou: 'O cliente demonstrou dúvidas frequentes, interrompeu diversas vezes, indicando ceticismo.'\n\n"
    "3. Avalie a performance da pessoa que conduziu a reunião, considerando:\n"
    "   - Clareza e objetividade na comunicação.\n"
    "   - Organização da reunião e controle do tempo.\n"
    "   - Capacidade de gerar conexão e conforto para o cliente.\n"
    "   - Presença de interrupções, confusões ou falhas de comunicação.\n\n"
    "4. Gere um insight final sobre a reunião:\n"
    "   - Baseado em toda a conversa, identifique oportunidades de melhoria, riscos ou boas práticas.\n"
    "   - Apresente a opinião de forma construtiva e objetiva.\n"
    "   - Não invente informações.\n\n"
    "Formato de resposta esperado:\n\n"
    "Sentimento do Cliente:\n"
    "Nota X - [Justificativa baseada em trechos reais da transcrição]\n\n"
    "Avaliação do Condutor:\n"
    "- [Comentário objetivo sobre a condução da reunião]\n\n"
    "Insight Final da IA:\n"
    "- [Opinião construtiva baseada no que foi observado]\n\n"
    "⚡ Importante:\n"
    "- Seja extremamente objetivo.\n"
    "- Baseie-se exclusivamente no conteúdo da transcrição.\n"
    "- Mantenha a resposta concisa e útil para o time de vendas e operação.\n"
    )
}

