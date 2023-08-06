import click
from meu_contracheque.mg_last_period import scraping_mg_last_period_cli
from meu_contracheque.mg_all_periods import scraping_mg_all_periods_cli
from meu_contracheque.mg_initial_period import scraping_mg_initial_period_cli

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
  """
    Conjunto de comandos criados para extração de informações de contracheques.
  """
  pass


@cli.group()
@click.option('--masp', '-m', envvar='MASP', required=True,
              help="Masp do servidor do Estado de Minas Gerais")
@click.option('--senha', '-s', envvar='PORTAL_PWD', required=True,
              help="Senha de acesso ao Portal do servidor do Estado de Minas Gerais")
@click.option('--headless/--no-headless', default=True,
              help='''
              Determina se Chrome será mostrada para usuário ou não durante execução.
              Por padrão --headless = True.
              A utilização da flag --no-headless mostrará o navegador durante execução.''')
@click.option('--pdf/--no-pdf', default=True,
              help='''
              Determina se a cópia pdf do documento será baixada.
              Por padrão --pdf = True.
              A utilização da flag --no-pdf Não baixará o arquivo.''')
@click.pass_context
def mg(ctx, masp, senha, headless, pdf):
  """
    Funções responsáveis pela extração de informações de contracheques dos servidores do Estado de Minas Gerais.
  """
  ctx.ensure_object(dict)
  ctx.obj['masp'] = masp
  ctx.obj['senha'] = senha
  ctx.obj['headless'] = headless
  ctx.obj['pdf'] = pdf

mg.add_command(scraping_mg_last_period_cli)
mg.add_command(scraping_mg_all_periods_cli)
mg.add_command(scraping_mg_initial_period_cli)

