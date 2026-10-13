#!/usr/bin/env python3
"""Gera as páginas de texto (privacidade, termos, suporte, exclusão de dados e 404)
a partir da moldura do index.html (português) e do en/index.html (inglês).

Uso: python3 gerar-paginas.py   (rodar na raiz do site, depois de mexer na navegação ou no rodapé da home)
"""
import os
import re

D = "https://multgestaoesistemas.com.br"
M = "contato@multgestaoesistemas.com.br"
MAIL = f'<a href="mailto:{M}">{M}</a>'
RAZAO = "MULT GESTAO E SISTEMAS LTDA"
CNPJ = "68.916.372/0001-04"


def peca(html, ini, fim):
    i = html.index(ini)
    return html[i: html.index(fim, i) + len(fim)]


def pagina(base, lang, home, titulo, desc, canon, alt_pt, alt_en, corpo, extra_head=""):
    head = peca(base, "<head>", "</head>")
    head = re.sub(r"<title>.*?</title>", f"<title>{titulo}</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'{extra_head}<link rel="canonical" href="{canon}">', head)
    head = re.sub(r'<link rel="alternate" hreflang="pt-BR" href="[^"]*">', f'<link rel="alternate" hreflang="pt-BR" href="{alt_pt}">', head)
    head = re.sub(r'<link rel="alternate" hreflang="en" href="[^"]*">', f'<link rel="alternate" hreflang="en" href="{alt_en}">', head)
    head = re.sub(r'<meta property="og:[^>]*>\n', "", head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", head, flags=re.S)
    simbolos = peca(base, '<svg width="0"', "</svg>")
    # âncoras da home passam a apontar para a home; os <use href="#i-..."> ficam como estão
    ancora = lambda bloco: re.sub(r'(<a [^>]*?href=")#', rf"\g<1>{home}#", bloco)
    nav = ancora(peca(base, '<nav class="nav"', "</nav>"))
    foot = ancora(peca(base, "<footer>", "</footer>"))
    # o seletor de idioma leva para a mesma página no outro idioma
    if lang == "pt-BR":
        troca = ('href="/en/" hreflang="en" lang="en"', f'href="{alt_en.replace(D, "")}" hreflang="en" lang="en"')
        pular = "Pular para o conteúdo"
    else:
        troca = ('href="/" hreflang="pt-BR" lang="pt-BR"', f'href="{alt_pt.replace(D, "")}" hreflang="pt-BR" lang="pt-BR"')
        pular = "Skip to content"
    nav, foot = nav.replace(*troca), foot.replace(*troca)
    return (f'<!doctype html>\n<html lang="{lang}">\n{head}\n<body>\n{simbolos}\n\n<a class="skip" href="#conteudo">{pular}</a>\n\n{nav}\n\n'
            f'<main id="conteudo" class="page">\n<section class="palco">\n  <div class="wrap">\n{corpo}\n  </div>\n</section>\n</main>\n\n{foot}\n\n'
            '<script src="/assets/site.js" defer></script>\n</body>\n</html>\n')


def corpo(rotulo, titulo, vigencia, secoes):
    linhas = [f'    <span class="eyebrow">{rotulo}</span>', f"    <h1>{titulo}</h1>"]
    if vigencia:
        linhas.append(f'    <p class="meta">{vigencia}</p>')
    for t, blocos in secoes:
        linhas.append(f"\n    <h2>{t}</h2>")
        for b in blocos:
            if isinstance(b, list):
                linhas.append("    <ul>\n" + "\n".join(f"      <li>{i}</li>" for i in b) + "\n    </ul>")
            else:
                linhas.append(f"    <p>{b}</p>")
    return "\n".join(linhas)


BUSKAR = '<a href="https://buskarveiculos.com/" rel="noopener">BUSKAR</a>'
CONSULTA = '<a href="https://appconsultaai.com/institucional" rel="noopener">Consulta.ai</a>'

PAGINAS = [
    # ───────────── privacidade ─────────────
    dict(
        pt=dict(slug="privacidade", titulo="Política de privacidade — Mult Gestão e Sistemas",
                desc="Política de privacidade da Mult Gestão e Sistemas: que dados o site trata, para quê, com quem compartilha, por quanto tempo guarda e como pedir a exclusão.",
                corpo=corpo("Privacidade · site institucional", 'Política de <em class="grifo">privacidade</em>', "Em vigor desde 13 de outubro de 2026", [
                    ("1. Quem responde por esta política", [
                        f"Este site pertence à <strong>{RAZAO}</strong>, CNPJ {CNPJ}, com sede em Uberlândia, Minas Gerais, Brasil. A Mult é a controladora dos dados pessoais tratados neste site.",
                        f"Contato para assuntos de privacidade e proteção de dados: {MAIL}."]),
                    ("2. A que esta política se aplica", [
                        "Esta política vale para o site multgestaoesistemas.com.br.",
                        f"Cada produto e cada aplicativo publicado pela Mult tem a própria política de privacidade, que descreve os dados tratados no uso daquele produto. O endereço da política aparece no próprio produto e na página dele na loja de aplicativos. Políticas atuais: <a href=\"https://buskarveiculos.com/privacidade\" rel=\"noopener\">BUSKAR</a> e <a href=\"https://appconsultaai.com/privacidade\" rel=\"noopener\">Consulta.ai</a>."]),
                    ("3. Que dados este site trata", [
                        "Este site é informativo. Não tem cadastro, não tem formulário, não usa cookies de publicidade e não usa ferramenta de análise de audiência. Os dados tratados são só estes:",
                        ["<strong>Registro técnico de acesso.</strong> Endereço IP, data, hora e navegador, recebidos pelo provedor de hospedagem para o site funcionar e para segurança.",
                         "<strong>Fontes tipográficas.</strong> As letras do site são entregues pelo Google Fonts. Para isso, o seu navegador informa o endereço IP ao Google.",
                         "<strong>Mensagens que você nos envia.</strong> Se você escrever para o nosso e-mail, tratamos o seu nome, o seu e-mail e o conteúdo da mensagem."]]),
                    ("4. Para que usamos e com que base", [
                        ["<strong>Manter o site no ar e seguro.</strong> Base: legítimo interesse.",
                         "<strong>Responder a quem entra em contato.</strong> Base: atendimento ao pedido de quem escreveu.",
                         "<strong>Cumprir a lei.</strong> Base: obrigação legal ou regulatória."],
                        "Não vendemos dados pessoais, não usamos os dados deste site para publicidade e não tomamos decisões automatizadas com eles."]),
                    ("5. Com quem compartilhamos", [
                        "Só com os provedores que fazem o site funcionar, e com autoridades quando a lei exigir:",
                        ["<strong>GitHub</strong>, que hospeda o site.", "<strong>Google</strong>, que entrega as fontes tipográficas.", "<strong>Hostinger</strong>, que hospeda o e-mail."],
                        "Esses provedores tratam os dados em nosso nome e seguem padrões de proteção equivalentes aos desta política. Eles podem tratar os dados fora do Brasil."]),
                    ("6. Por quanto tempo guardamos", [
                        "A Mult não mantém banco de dados de visitantes deste site. Os registros técnicos ficam com o provedor de hospedagem, pelo prazo da política dele. As mensagens de e-mail ficam guardadas enquanto forem necessárias para atender o pedido e, depois, pelo prazo que a lei exigir."]),
                    ("7. Como protegemos", [
                        "O site é servido por conexão cifrada (HTTPS). O acesso às caixas de e-mail é restrito a pessoas autorizadas."]),
                    ("8. Seus direitos", [
                        f"A Lei Geral de Proteção de Dados (Lei 13.709/2018) garante a você confirmar se tratamos seus dados, acessar, corrigir, pedir a eliminação, pedir a portabilidade, saber com quem compartilhamos e revogar o consentimento, quando ele for a base do tratamento. Para exercer qualquer um deles, escreva para {MAIL}. Respondemos em até 15 dias.",
                        "Você também pode apresentar reclamação à Autoridade Nacional de Proteção de Dados (ANPD)."]),
                    ("9. Exclusão de conta e de dados", [
                        'O caminho para pedir a exclusão de uma conta ou dos seus dados em um produto operado pela Mult está em <a href="/exclusao-de-dados/">Exclusão de dados</a>.']),
                    ("10. Crianças e adolescentes", [
                        "Este site e os produtos da Mult não são direcionados a menores de 18 anos, e não coletamos dados deles de forma intencional."]),
                    ("11. Mudanças nesta política", [
                        "Se esta política mudar, a nova versão será publicada nesta página com a data de vigência atualizada."]),
                ])),
        en=dict(slug="en/privacy", titulo="Privacy policy — Mult Gestão e Sistemas",
                desc="Privacy policy of Mult Gestão e Sistemas: what data the website processes, why, who it is shared with, how long it is kept and how to request deletion.",
                corpo=corpo("Privacy · corporate website", 'Privacy <em class="grifo">policy</em>', "Effective from 13 October 2026", [
                    ("1. Who is responsible for this policy", [
                        f"This website belongs to <strong>{RAZAO}</strong>, CNPJ (Brazilian tax ID) {CNPJ}, headquartered in Uberlândia, Minas Gerais, Brazil. Mult is the controller of the personal data processed on this website.",
                        f"Privacy and data protection contact: {MAIL}."]),
                    ("2. What this policy covers", [
                        "This policy covers the website multgestaoesistemas.com.br.",
                        "Each product and each app published by Mult has its own privacy policy, describing the data processed when that product is used. The address of that policy is shown in the product itself and on its store listing. Current policies, in Portuguese: <a href=\"https://buskarveiculos.com/privacidade\" rel=\"noopener\">BUSKAR</a> and <a href=\"https://appconsultaai.com/privacidade\" rel=\"noopener\">Consulta.ai</a>."]),
                    ("3. What data this website processes", [
                        "This is an informational website. It has no sign-up, no forms, no advertising cookies and no audience analytics. The only data processed are:",
                        ["<strong>Technical access logs.</strong> IP address, date, time and browser, received by the hosting provider so the website works and stays secure.",
                         "<strong>Web fonts.</strong> The typefaces are delivered by Google Fonts. To do that, your browser shares your IP address with Google.",
                         "<strong>Messages you send us.</strong> If you write to our e-mail address, we process your name, your e-mail address and the content of the message."]]),
                    ("4. Why we use it and on what basis", [
                        ["<strong>Keeping the website online and secure.</strong> Basis: legitimate interest.",
                         "<strong>Replying to people who contact us.</strong> Basis: handling the request of the person who wrote.",
                         "<strong>Complying with the law.</strong> Basis: legal or regulatory obligation."],
                        "We do not sell personal data, we do not use data from this website for advertising and we do not make automated decisions with it."]),
                    ("5. Who we share it with", [
                        "Only with the providers that make the website work, and with authorities when required by law:",
                        ["<strong>GitHub</strong>, which hosts the website.", "<strong>Google</strong>, which delivers the web fonts.", "<strong>Hostinger</strong>, which hosts the e-mail service."],
                        "These providers process data on our behalf and follow protection standards equivalent to those in this policy. They may process data outside Brazil."]),
                    ("6. How long we keep it", [
                        "Mult does not keep a database of visitors to this website. Technical logs stay with the hosting provider, for the period set in its own policy. E-mail messages are kept for as long as needed to handle the request and, after that, for the period required by law."]),
                    ("7. How we protect it", [
                        "The website is served over an encrypted connection (HTTPS). Access to the mailboxes is restricted to authorised people."]),
                    ("8. Your rights", [
                        f"The Brazilian General Data Protection Law (LGPD, Law 13,709/2018) gives you the right to confirm whether we process your data, to access it, correct it, request its deletion, request portability, know who we share it with and withdraw consent, when consent is the basis for processing. To exercise any of these rights, write to {MAIL}. We reply within 15 days.",
                        "You may also lodge a complaint with the Brazilian data protection authority (ANPD)."]),
                    ("9. Account and data deletion", [
                        'How to request the deletion of an account or of your data in a product operated by Mult is explained in <a href="/en/data-deletion/">Data deletion</a>.']),
                    ("10. Children and teenagers", [
                        "This website and Mult's products are not directed at people under 18, and we do not knowingly collect their data."]),
                    ("11. Changes to this policy", [
                        "If this policy changes, the new version will be published on this page with an updated effective date."]),
                ]))),
    # ───────────── termos ─────────────
    dict(
        pt=dict(slug="termos", titulo="Termos de uso — Mult Gestão e Sistemas",
                desc="Termos de uso do site institucional da Mult Gestão e Sistemas.",
                corpo=corpo("Termos · site institucional", 'Termos de <em class="grifo">uso</em>', "Em vigor desde 13 de outubro de 2026", [
                    ("1. Quem somos", [
                        f"Este site é mantido pela <strong>{RAZAO}</strong>, CNPJ {CNPJ}, com sede em Uberlândia, Minas Gerais, Brasil. Ao navegar por ele, você concorda com estes termos."]),
                    ("2. Para que serve este site", [
                        "O site apresenta a Mult e as marcas para as quais ela desenvolve tecnologia. O conteúdo é informativo e pode ser alterado a qualquer momento."]),
                    ("3. Produtos e aplicativos", [
                        "Estes termos valem só para este site. O uso de cada produto ou aplicativo segue os termos e a política de privacidade do próprio produto, publicados no site dele.",
                        "No BUSKAR e no Consulta.ai, a Mult desenvolve e opera o produto. Nas demais marcas do Grupo Avante apresentadas aqui, a Mult responde pela tecnologia, e o serviço é prestado pela empresa responsável pela marca."]),
                    ("4. Marcas e conteúdo", [
                        "A marca Mult e o conteúdo deste site pertencem à Mult. As marcas do Grupo Avante exibidas aqui pertencem aos respectivos titulares e aparecem para identificar os projetos. Não é permitido copiar, modificar ou usar marcas e conteúdo sem autorização por escrito."]),
                    ("5. Uso permitido", [
                        "Você pode navegar pelo site e compartilhar os endereços das páginas. Não é permitido:",
                        ["tentar acessar áreas ou sistemas sem autorização;", "prejudicar o funcionamento do site;", "usar o site para atividade ilícita ou para se passar pela Mult."]]),
                    ("6. Links para outros sites", [
                        "O site tem links para os produtos e para as marcas do Grupo Avante. Cada um desses sites tem os próprios termos e a própria política de privacidade."]),
                    ("7. Responsabilidade", [
                        "A Mult cuida para manter as informações deste site corretas e atualizadas, mas elas são gerais e não substituem os termos de cada produto. Nos limites permitidos pela lei, a Mult não responde por indisponibilidade temporária do site nem por decisões tomadas só com base no conteúdo desta página."]),
                    ("8. Privacidade", [
                        'O tratamento de dados pessoais neste site está descrito na <a href="/privacidade/">Política de privacidade</a>.']),
                    ("9. Lei aplicável e foro", [
                        "Estes termos seguem as leis brasileiras. Fica eleito o foro da comarca de Uberlândia, Minas Gerais, ressalvado o direito do consumidor de escolher o foro do seu domicílio."]),
                    ("10. Contato e mudanças", [
                        f"Dúvidas sobre estes termos: {MAIL}. Se os termos mudarem, a nova versão será publicada nesta página com a data de vigência atualizada."]),
                ])),
        en=dict(slug="en/terms", titulo="Terms of use — Mult Gestão e Sistemas",
                desc="Terms of use of the Mult Gestão e Sistemas corporate website.",
                corpo=corpo("Terms · corporate website", 'Terms of <em class="grifo">use</em>', "Effective from 13 October 2026", [
                    ("1. Who we are", [
                        f"This website is maintained by <strong>{RAZAO}</strong>, CNPJ (Brazilian tax ID) {CNPJ}, headquartered in Uberlândia, Minas Gerais, Brazil. By browsing it, you agree to these terms."]),
                    ("2. What this website is for", [
                        "The website presents Mult and the brands it builds technology for. The content is informational and may change at any time."]),
                    ("3. Products and apps", [
                        "These terms cover this website only. The use of each product or app is governed by that product's own terms and privacy policy, published on its website.",
                        "For BUSKAR and Consulta.ai, Mult develops and operates the product. For the other Grupo Avante brands shown here, Mult is responsible for the technology, and the service is provided by the company behind the brand."]),
                    ("4. Trademarks and content", [
                        "The Mult brand and the content of this website belong to Mult. The Grupo Avante brands shown here belong to their respective owners and appear to identify the projects. Copying, modifying or using trademarks and content without written permission is not allowed."]),
                    ("5. Permitted use", [
                        "You may browse the website and share the addresses of its pages. You may not:",
                        ["try to access areas or systems without authorisation;", "disrupt the operation of the website;", "use the website for unlawful activity or to impersonate Mult."]]),
                    ("6. Links to other websites", [
                        "The website links to the products and to the Grupo Avante brands. Each of those websites has its own terms and privacy policy."]),
                    ("7. Liability", [
                        "Mult takes care to keep the information on this website correct and up to date, but it is general and does not replace the terms of each product. To the extent permitted by law, Mult is not liable for temporary unavailability of the website or for decisions made solely on the basis of the content of this page."]),
                    ("8. Privacy", [
                        'How personal data is processed on this website is described in the <a href="/en/privacy/">Privacy policy</a>.']),
                    ("9. Governing law and venue", [
                        "These terms are governed by Brazilian law. The courts of Uberlândia, Minas Gerais, Brazil, have jurisdiction, without prejudice to a consumer's right to choose the courts of their own place of residence."]),
                    ("10. Contact and changes", [
                        f"Questions about these terms: {MAIL}. If the terms change, the new version will be published on this page with an updated effective date."]),
                ]))),
    # ───────────── suporte ─────────────
    dict(
        pt=dict(slug="suporte", titulo="Suporte — Mult Gestão e Sistemas",
                desc="Como falar com a Mult Gestão e Sistemas e onde encontrar o suporte de cada produto.",
                corpo=corpo("Suporte", 'Como falar <em class="grifo">com a gente</em>', "", [
                    ("Contato da Mult", [
                        f"Escreva para {MAIL}. Respondemos em dias úteis.",
                        "Para agilizar, informe na mensagem:",
                        ["o produto (por exemplo, BUSKAR ou Consulta.ai);", "o e-mail da sua conta no produto;", "o que aconteceu, em que tela e, se puder, com uma captura de tela."],
                        "Nunca envie senha, código de verificação ou dados de cartão por e-mail. A Mult não pede essas informações."]),
                    ("Suporte de cada produto", [
                        "Quem já é cliente encontra o atendimento dentro do próprio produto:",
                        [f"<strong>{BUSKAR}:</strong> canais de atendimento no site e no Portal do Parceiro.",
                         f"<strong>{CONSULTA}:</strong> canais de atendimento no site e no painel."],
                        "Para as demais marcas do Grupo Avante, use os canais de atendimento do site de cada marca."]),
                    ("Conta, privacidade e exclusão de dados", [
                        'Pedidos sobre dados pessoais estão explicados na <a href="/privacidade/">Política de privacidade</a>. Para excluir a conta ou os dados em um produto operado pela Mult, veja <a href="/exclusao-de-dados/">Exclusão de dados</a>.']),
                    ("Quem é a Mult", [
                        f"{RAZAO}, CNPJ {CNPJ}, Uberlândia, Minas Gerais, Brasil."]),
                ])),
        en=dict(slug="en/support", titulo="Support — Mult Gestão e Sistemas",
                desc="How to contact Mult Gestão e Sistemas and where to find support for each product.",
                corpo=corpo("Support", 'How to <em class="grifo">reach us</em>', "", [
                    ("Contacting Mult", [
                        f"Write to {MAIL}. We reply on business days, in Portuguese or English.",
                        "To speed things up, please include:",
                        ["the product (for example, BUSKAR or Consulta.ai);", "the e-mail address of your account in the product;", "what happened, on which screen and, if possible, a screenshot."],
                        "Never send a password, a verification code or card details by e-mail. Mult does not ask for this information."]),
                    ("Support for each product", [
                        "Existing customers find help inside the product itself:",
                        [f"<strong>{BUSKAR}:</strong> help channels on the website and in the dealer portal.",
                         f"<strong>{CONSULTA}:</strong> help channels on the website and in the dashboard."],
                        "For the other Grupo Avante brands, use the help channels on each brand's website."]),
                    ("Account, privacy and data deletion", [
                        'Requests about personal data are explained in the <a href="/en/privacy/">Privacy policy</a>. To delete your account or your data in a product operated by Mult, see <a href="/en/data-deletion/">Data deletion</a>.']),
                    ("Who Mult is", [
                        f"{RAZAO}, CNPJ (Brazilian tax ID) {CNPJ}, Uberlândia, Minas Gerais, Brazil."]),
                ]))),
    # ───────────── exclusão de dados ─────────────
    dict(
        pt=dict(slug="exclusao-de-dados", titulo="Exclusão de conta e de dados — Mult Gestão e Sistemas",
                desc="Como pedir a exclusão da sua conta e dos seus dados no BUSKAR e no Consulta.ai, produtos operados pela Mult Gestão e Sistemas.",
                corpo=corpo("Exclusão de conta e de dados", 'Como excluir sua conta <em class="grifo">e seus dados</em>', "Em vigor desde 13 de outubro de 2026", [
                    ("A quais produtos esta página se aplica", [
                        f"Aos produtos e aplicativos operados pela {RAZAO}: <strong>BUSKAR</strong> e <strong>Consulta.ai</strong>."]),
                    ("Como pedir", [
                        ["<strong>Dentro do produto.</strong> Quando a sua conta mostrar a opção de excluir, use-a: é o caminho mais rápido.",
                         f"<strong>Por e-mail.</strong> Escreva para {MAIL} com o assunto “Exclusão de conta” e informe o produto e o e-mail da conta. Envie a mensagem, de preferência, do próprio e-mail cadastrado."],
                        "Antes de excluir, confirmamos que o pedido veio do dono da conta. Respondemos em até 15 dias."]),
                    ("O que é excluído", [
                        "A conta e os dados ligados a ela: dados de cadastro e de contato, dados de uso e o conteúdo que você criou no produto. A exclusão é definitiva. Desativar ou bloquear a conta não conta como exclusão."]),
                    ("O que a lei obriga a guardar", [
                        "Alguns registros não podem ser apagados na hora, porque a lei exige que sejam guardados:",
                        ["<strong>Registros financeiros e fiscais</strong> (pagamentos, faturas e notas fiscais, com a identificação de quem pagou): guardados por 5 anos.",
                         "<strong>Registros de segurança e de acesso:</strong> guardados pelo prazo que a lei exigir."],
                        "Esses registros ficam com acesso restrito, não são usados para outro fim e são apagados ao fim do prazo. A política de privacidade de cada produto traz os detalhes."]),
                    ("Excluir só parte dos dados", [
                        f"Você também pode pedir a exclusão de dados específicos sem encerrar a conta. Escreva para {MAIL} dizendo quais dados e em qual produto."]),
                    ("Dúvidas", [
                        f'Fale com a Mult em {MAIL} ou veja a página de <a href="/suporte/">Suporte</a>.']),
                ])),
        en=dict(slug="en/data-deletion", titulo="Account and data deletion — Mult Gestão e Sistemas",
                desc="How to request the deletion of your account and data in BUSKAR and Consulta.ai, products operated by Mult Gestão e Sistemas.",
                corpo=corpo("Account and data deletion", 'How to delete your account <em class="grifo">and your data</em>', "Effective from 13 October 2026", [
                    ("Which products this page covers", [
                        f"The products and apps operated by {RAZAO}: <strong>BUSKAR</strong> and <strong>Consulta.ai</strong>."]),
                    ("How to request it", [
                        ["<strong>Inside the product.</strong> When your account shows a delete option, use it: it is the fastest way.",
                         f"<strong>By e-mail.</strong> Write to {MAIL} with the subject “Account deletion” and tell us the product and the e-mail address of the account. Preferably, send the message from the registered e-mail address."],
                        "Before deleting, we confirm that the request came from the account owner. We reply within 15 days."]),
                    ("What is deleted", [
                        "The account and the data linked to it: registration and contact data, usage data and the content you created in the product. Deletion is permanent. Deactivating or blocking an account does not count as deletion."]),
                    ("What the law requires us to keep", [
                        "Some records cannot be erased right away, because the law requires them to be kept:",
                        ["<strong>Financial and tax records</strong> (payments, invoices and tax documents, with the identification of the payer): kept for 5 years.",
                         "<strong>Security and access records:</strong> kept for the period required by law."],
                        "These records are kept under restricted access, are not used for any other purpose and are erased at the end of the period. Each product's privacy policy gives the details."]),
                    ("Deleting only part of the data", [
                        f"You can also ask for specific data to be deleted without closing the account. Write to {MAIL} telling us which data and which product."]),
                    ("Questions", [
                        f'Contact Mult at {MAIL} or see the <a href="/en/support/">Support</a> page.']),
                ]))),
]


def main():
    pt = open("index.html", encoding="utf-8").read()
    en = open("en/index.html", encoding="utf-8").read()
    urls = [f"{D}/", f"{D}/en/"]
    for par in PAGINAS:
        alt_pt, alt_en = f"{D}/{par['pt']['slug']}/", f"{D}/{par['en']['slug']}/"
        for lang, base, home in (("pt", pt, "/"), ("en", en, "/en/")):
            p = par[lang]
            os.makedirs(p["slug"], exist_ok=True)
            html = pagina(base, "pt-BR" if lang == "pt" else "en", home, p["titulo"], p["desc"], f"{D}/{p['slug']}/", alt_pt, alt_en, p["corpo"])
            open(f"{p['slug']}/index.html", "w", encoding="utf-8").write(html)
            urls.append(f"{D}/{p['slug']}/")
    erro = corpo("Erro 404", 'Este endereço <em class="grifo">não existe.</em>', "", [])
    erro += ('\n    <p>O link pode estar errado ou a página pode ter mudado de lugar.</p>\n'
             '    <p style="margin-top:30px"><a class="btn btn-dark" href="/">Voltar ao início <i><svg class="ico"><use href="#i-arrow"/></svg></i></a></p>')
    open("404.html", "w", encoding="utf-8").write(
        pagina(pt, "pt-BR", "/", "Página não encontrada — Mult Gestão e Sistemas", "Página não encontrada.", f"{D}/", f"{D}/", f"{D}/en/", erro,
               extra_head='<meta name="robots" content="noindex">\n'))
    mapa = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    open("sitemap.xml", "w", encoding="utf-8").write(mapa)
    print(f"{len(urls) - 2} páginas de texto geradas + 404 + sitemap ({len(urls)} endereços)")


if __name__ == "__main__":
    main()
