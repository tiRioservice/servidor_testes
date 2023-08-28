from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, registry, declarative_base
from sqlalchemy.sql import func
from sqlalchemy import String, Integer, Float, Column, DateTime, BigInteger
from .connection import engine
from modules.cryptopass import generate_pass
from .via_cep import Via_cep
import datetime

DBase = declarative_base()
reg = registry()

class Base(DBase):
     __tablename__ = 'tb_bases'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     base_id: Mapped[int] = mapped_column(primary_key=True)
     base_nome: Mapped[str] = mapped_column(String(30), nullable=False)
     base_desc: Mapped[str] = mapped_column(String(300))
     end_id: Mapped[Optional[int]]

     def __repr__(self) -> str:
          return f"Base -> (base_id={self.base_id!r}, base_nome={self.base_nome!r}, base_desc={self.base_desc!r})"

class Cargo(DBase):
     __tablename__ = 'tb_cargos'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     cargo_id: Mapped[int] = mapped_column(primary_key=True)
     cargo_nome: Mapped[str] = mapped_column(String(30), nullable=False)
     cargo_desc: Mapped[str] = mapped_column(String(300))

     def __repr__(self) -> str:
          return f"Cargo -> (cargo_id={self.cago_id!r}, cargo_nome={self.cargo_nome!r}, cargo_desc={self.cargo_desc!r})"
     
class Cargo_config(DBase):
     __tablename__ = 'tb_cargo_configs'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     cargo_config_id: Mapped[int] = mapped_column(primary_key=True)
     cargo_id: Mapped[Optional[int]]
     perm_id: Mapped[Optional[int]]
     nvl_acesso: Mapped[bool]

     def __repr__(self) -> str:
          return f"Cargo_config -> (cargo_config_id={self.cago_config_id!r}, cargo_id={self.cargo_id!r}, perm_id={self.perm_id!r}, nvl_acesso={self.nvl_acesso!r})"

class Permissao(DBase):
     __tablename__ = 'tb_permissoes'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     perm_id: Mapped[int] = mapped_column(primary_key=True)
     perm_cod: Mapped[int]
     perm_nome: Mapped[str] = mapped_column(String(50), nullable=False)
     perm_desc: Mapped[str] = mapped_column(String(300), nullable=False)

     def __repr__(self) -> str:
          return f"Permissao -> (perm_id={self.perm_id!r}, perm_cod={self.perm_cod!r}, perm_nome={self.perm_nome!r}, perm_desc={self.perm_desc!r})"

class Categoria(DBase):
     __tablename__ = 'tb_categorias'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     categ_id: Mapped[int] = mapped_column(primary_key=True)
     categ_nome: Mapped[str] = mapped_column(String(15), nullable=False)
     categ_desc: Mapped[str] = mapped_column(String(200))

     def __repr__(self) -> str:
          return f"Categoria -> (categ_id={self.categ_id!r}, categ_nome={self.categ_nome!r}, categ_desc={self.categ_desc!r})"
     
class Rel_item_forn(DBase):
     __tablename__ = 'tb_rel_item_forn'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     rel_item_forn_id: Mapped[int] = mapped_column(primary_key=True)
     item_id: Mapped[int] = mapped_column(Integer, nullable=False)
     forn_id: Mapped[int] = mapped_column(Integer, nullable=False)

     def __repr__(self) -> str:
          return f"Rel_item_forn -> (rel_item_forn_id={self.rel_item_forn_id!r}, item_id={self.item_id!r}, forn_id={self.forn_id!r})"
     
class Lista_itens(DBase):
     __tablename__ = 'tb_lista_itens'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     lista_itens_id: Mapped[int] = mapped_column(primary_key=True)
     item_id: Mapped[int] = mapped_column(Integer, nullable=False)
     lista_itens_nome: Mapped[str] = mapped_column(String(100), nullable=True)
     lista_itens_qnt_necessaria: Mapped[int] = mapped_column(Integer, nullable=True)
     lista_itens_val_un: Mapped[float] = mapped_column(Float, nullable=True)
     lista_itens_sub_total: Mapped[float] = mapped_column(Float, nullable=True)
     cot_id: Mapped[int] = mapped_column(Integer, nullable=False)

     def __repr__(self) -> str:
          return f"Lista_itens -> (lista_itens_id={self.lista_itens_id!r}, item_id={self.item_id!r}, forn_id={self.forn_id!r})"
     
class Lista_forn(DBase):
     __tablename__ = 'tb_lista_forn'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     lista_forn_id: Mapped[int] = mapped_column(primary_key=True)
     forn_id: Mapped[int] = mapped_column(Integer, nullable=False)
     lista_forn_prazo_pag: Mapped[int] = mapped_column(Integer, nullable=True)
     lista_forn_prazo_entrega: Mapped[int] = mapped_column(Integer, nullable=True)
     cot_id: Mapped[int] = mapped_column(Integer, nullable=False)

     def __repr__(self) -> str:
          return f"Lista_forn -> (lista_forn_id={self.lista_forn_id!r}, item_id={self.item_id!r}, forn_id={self.forn_id!r})"
     
class Cotacao(DBase):
     __tablename__ = 'tb_cotacoes'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     cot_id: Mapped[int] = mapped_column(primary_key=True)
     colab_id: Mapped[int] = mapped_column(Integer, nullable=False)
     cot_valid: Mapped[str] = mapped_column(String(12), nullable=True)
     cot_status: Mapped[int] = mapped_column(Integer, nullable=True)
     cot_val_total: Mapped[float] = mapped_column(Float, nullable=True)

     def __repr__(self) -> str:
          return f"Cotacao -> (cot_id={self.cot_id!r}, colab_id={self.colab_id!r}, cot_status={self.cot_status!r})"
     
class Nota_fiscal(DBase):
     __tablename__ = 'tb_notas_fiscais'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     nota_id: Mapped[int] = mapped_column(primary_key=True)
     colab_id: Mapped[int] = mapped_column(Integer, nullable=False)
     forn_id: Mapped[int] = mapped_column(Integer, nullable=False)
     nota_centro_custo: Mapped[str] = mapped_column(String(100), nullable=True)
     nota_forma_pag: Mapped[str] = mapped_column(String(50), nullable=True)
     nota_cond_pag: Mapped[str] = mapped_column(String(100), nullable=True)
     nota_valor_total: Mapped[float] = mapped_column(Float, nullable=True)

     def __repr__(self) -> str:
          return f"Nota_fiscal -> (nota_id={self.nota_id!r}, colab_id={self.colab_id!r}, forn_id={self.forn_id!r})"
     
class Rel_item_nota(DBase):
     __tablename__ = 'tb_rel_item_nota'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     rel_item_nota_id: Mapped[int] = mapped_column(primary_key=True)
     nota_id: Mapped[int] = mapped_column(Integer, nullable=False)
     item_id: Mapped[int] = mapped_column(Integer, nullable=False)

     def __repr__(self) -> str:
          return f"Rel_item_nota -> (rel_item_nota_id={self.rel_item_nota_id!r}, nota_id={self.nota_id!r}, item_id={self.item_id!r})"
     
class Estoque(DBase):
     __tablename__ = 'tb_estoque'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     estoque_id: Mapped[int] = mapped_column(primary_key=True)
     item_id: Mapped[int] = mapped_column(Integer, nullable=False)
     base_id: Mapped[int] = mapped_column(Integer, nullable=False)
     estoque_qnt: Mapped[int] = mapped_column(Integer, nullable=False)
     estoque_min: Mapped[int] = mapped_column(Integer, nullable=False)

     def __repr__(self) -> str:
          return f"Estoque -> (estoque_id={self.estoque_id!r}, item_id={self.item_id!r}, base_id={self.base_id!r}, estoque_qnt={self.estoque_qnt!r}, estoque_min={self.estoque_min!r})"
     
class Item(DBase):
     __tablename__ = 'tb_itens'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     item_id: Mapped[int] = mapped_column(primary_key=True)
     categ_id: Mapped[int]
     item_nome: Mapped[str] = mapped_column(String(30), nullable=False)
     item_tamanho: Mapped[str] = mapped_column(String(3), nullable=False)
     item_preco: Mapped[float] = mapped_column(Float, nullable=False)
     item_qualidade: Mapped[Optional[int]]
     item_desc: Mapped[str] = mapped_column(String(200))

     def __repr__(self) -> str:
          return f"Item -> (item_id={self.item_id!r}, categ_id={self.categ_id!r}, item_nome={self.item_nome!r}, item_tamanho={self.item_tamanho!r}, item_preco={self.item_preco!r}, item_quantidade={self.item_quantidade!r}, item_desc={self.item_desc!r})"
     
class Fornecedor(DBase):
     __tablename__ = 'tb_fornecedores'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     forn_id: Mapped[int] = mapped_column(primary_key=True)
     forn_cnpj = Column(BigInteger, nullable=False)
     forn_razao_social: Mapped[str] = mapped_column(String(50), nullable=True)
     forn_nome_fantasia: Mapped[str] = mapped_column(String(50), nullable=True)
     forn_insc_estadual = Column(BigInteger, nullable=False)
     forn_insc_municipal = Column(BigInteger, nullable=False)
     forn_tel_cod: Mapped[Optional[int]]
     forn_tel_num: Mapped[Optional[int]]
     forn_email: Mapped[Optional[str]] = mapped_column(String(70))
     forn_nome_contato: Mapped[Optional[str]] = mapped_column(String(50))
     forn_banco: Mapped[Optional[str]] = mapped_column(String(20))
     forn_titular: Mapped[Optional[str]] = mapped_column(String(50))
     forn_cnpj_cpf_titular: Mapped[Optional[int]]
     forn_agencia: Mapped[Optional[str]] = mapped_column(String(6))
     forn_conta: Mapped[Optional[str]] = mapped_column(String(8))
     forn_tp_operacao: Mapped[Optional[str]] = mapped_column(String(20))
     forn_pix: Mapped[Optional[str]] = mapped_column(String(200))
     end_id: Mapped[Optional[int]]

     def __repr__(self) -> str:
          return f"Fornecedor -> (forn_id={self.forn_id!r})"
     
class Colaborador(DBase):
     __tablename__ = 'tb_colaboradores'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     colab_id: Mapped[int] = mapped_column(Integer, primary_key=True)
     colab_matricula: Mapped[Optional[int]]
     colab_nome: Mapped[str] = mapped_column(String(50), nullable=False)
     colab_nascimento: Mapped[Optional[datetime.date]]
     colab_cpf: Mapped[str] = mapped_column(String(11), nullable=False)
     colab_rg: Mapped[str] = mapped_column(String(9), nullable=True)
     colab_est_civil: Mapped[str] = mapped_column(String(15), nullable=True)
     colab_naturalidade: Mapped[str] = mapped_column(String(30), nullable=True)
     colab_fone: Mapped[str] = mapped_column(String(13), nullable=True)
     colab_celular: Mapped[str] = mapped_column(String(14), nullable=True)
     colab_escolaridade: Mapped[str] = mapped_column(String(50), nullable=True)
     colab_admissao: Mapped[Optional[datetime.date]]
     colab_email: Mapped[str] = mapped_column(String(100), nullable=True)
     colab_centro_custo: Mapped[str] = mapped_column(String(100), nullable=True)
     colab_salario: Mapped[Optional[float]]
     colab_status: Mapped[bool]
     colab_login: Mapped[str] = mapped_column(String(50), nullable=False)
     colab_password: Mapped[str] = mapped_column(String(100), nullable=True)
     end_id: Mapped[Optional[int]]
     cargo_id: Mapped[Optional[int]]
     base_id: Mapped[Optional[int]]

     def __init__(self, colab_matricula:int, colab_nome:str, colab_cpf:str, colab_login:str, colab_password:str, end_id:int):
          self.colab_matricula = colab_matricula
          self.colab_nome = colab_nome
          self.colab_cpf = colab_cpf
          self.colab_login = colab_login
          self.colab_password = self.__generate_hash(colab_password)
          self.end_id = end_id
          self.colab_status = False

     def __repr__(self) -> str:
          return f"Colaborador -> (colab_id={self.colab_id!r}, colab_nome={self.colab_nome!r})"

     def __generate_hash(self, password):
          return generate_pass(password)

class Endereco(DBase):
     __tablename__ = 'tb_enderecos'

     registro = Column(DateTime(timezone=True), server_default=func.now())
     end_id: Mapped[int] = mapped_column(primary_key=True)
     end_tipo: Mapped[str] = mapped_column(String(1), nullable=False)
     end_cep: Mapped[Optional[int]]
     end_logradouro: Mapped[Optional[str]] = mapped_column(String(100))
     end_numero: Mapped[Optional[int]]
     end_bairro: Mapped[Optional[str]] = mapped_column(String(100))
     end_cidade: Mapped[Optional[str]] = mapped_column(String(100))
     end_uf: Mapped[Optional[str]] = mapped_column(String(2))
     end_referencia: Mapped[Optional[str]] = mapped_column(String(300))

     def __init__(self, end_tipo:str, end_cep:int, end_numero:int, end_referencia:str):
          self.end_cep = end_cep
          self.end_tipo = end_tipo
          self.end_numero = end_numero
          self.end_referencia = end_referencia

     def __repr__(self) -> str:
          return f"Endereco -> (end_id={self.end_id!r}, end_cep={self.end_cep!r}, end_logradouro={self.end_logradouro!r}, end_numero={self.end_numero!r}, end_bairro={self.end_bairro!r}, end_cidade={self.end_cidade!r}, end_uf={self.end_uf!r}, end_referencia={self.end_referencia!r})"
     
     def get_end_from_viacep(self) -> dict:
          via_cep = Via_cep(self.end_cep)
          end = via_cep.get_end()
          self.set_end_from_viacep(end)
          return end
     
     def set_end_from_viacep(self, data:dict) -> None:
          self.end_logradouro = data['logradouro']
          self.end_bairro = data['bairro']
          self.end_cidade = data['localidade']
          self.end_uf = data['uf']
     
DBase.metadata.create_all(engine)