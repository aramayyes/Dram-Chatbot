from enum import Enum
from typing import Union


class BankId(Enum):
    """Contains ids of all supported bank."""
    acba = 'acba'
    ameria = 'ameria'
    ararat = 'ararat'
    ardshin = 'ardshin'
    arm_business = 'arm_business'
    arm_swiss = 'arm_swiss'
    armeconom = 'armeconom'
    artsakh = 'artsakh'
    byblos = 'byblos'
    converse_bank = 'converse_bank'
    evoca = 'evoca'
    hsbc = 'hsbc'
    id_ = 'id_'
    ineco = 'ineco'
    mellat = 'mellat'
    uni = 'uni'
    vtb = 'vtb'


class Bank:
    """Represents a bank used in this app."""

    def __init__(self, id_: BankId, rate_am_id: str, hy_name, en_name, ru_name) -> None:
        self.id_ = id_
        self.rate_am_id = rate_am_id
        self.hy_name = hy_name
        self.en_name = en_name
        self.ru_name = ru_name


# Holds all available banks
BANKS = [
    Bank(BankId.acba, 'f3ffb6cf-dbb6-4d43-b49c-f6d71350d7fb', 'ԱԿԲԱ-ԿՐԵԴԻՏ ԱԳՐԻԿՈԼ ԲԱՆԿ', 'ACBA-Credit Agricole Bank',
         'АКБА Кредит Агриколь Банк'),
    Bank(BankId.ameria, '989ba942-a5cf-4fc2-b62e-3248c4edfbbc', 'Ամերիաբանկ', 'Ameriabank', 'Америабанк'),
    Bank(BankId.ararat, '5ee70183-87fe-4799-802e-ef7f5e7323db', 'ԱՐԱՐԱՏԲԱՆԿ', 'ARARATBANK', 'АРАРАТБАНК'),
    Bank(BankId.ardshin, '466fe84c-197f-4174-bc97-e1dc7960edc7', 'Արդշինբանկ', 'Ardshinbank', 'Ардшинбанк'),
    Bank(BankId.arm_business, 'db08ff22-add9-45ea-a450-1fe5b1993704', 'ՀԱՅԲԻԶՆԵՍԲԱՆԿ', 'ArmBusinessBank',
         'Армбизнесбанк'),
    Bank(BankId.arm_swiss, '95b795f4-073d-4670-993d-dfb781375a94', 'Արմսվիսբանկ', 'ArmSwissBank', 'Армсвисбанк'),
    Bank(BankId.armeconom, 'b5bb13d2-8a79-43a8-a538-ffd1e2e21009', 'ՀԱՅԷԿՈՆՈՄԲԱՆԿ', 'ARMECONOMBANK', 'АРМЭКОНОМБАНК'),
    Bank(BankId.artsakh, 'e1a68c2e-bc47-4f58-afd2-3b80a8465b14', 'Արցախբանկ', 'Artsakhbank', 'Арцахбанк'),
    Bank(BankId.byblos, 'ebd241ce-4a38-45a4-9bcd-c6e607079706', 'Բիբլոս Բանկ Արմենիա', 'Byblos Bank Armenia',
         'Библос Банк Армения'),
    Bank(BankId.converse_bank, '2119a3f1-b233-4254-a450-304a2a5bff19', 'Կոնվերս Բանկ', 'Converse Bank', 'Конверс Банк'),
    Bank(BankId.evoca, '0fffdcc4-8e36-49f3-9863-93ad02ce6541', 'Էվոկաբանկ', 'Evocabank', 'Эвокабанк'),
    Bank(BankId.hsbc, '332c7078-97ad-4bf7-b8ee-44d85a9c88d1', 'Էյչ-Էս-Բի-Սի Բանկ', 'HSBC Bank Armenia',
         'Эйч-Эс-Би-Си Банк Армения'),
    Bank(BankId.id_, '8e9bd4c8-6f4a-4663-ae86-b8fbaf295030', 'ԱյԴի Բանկ', 'IDBank', 'АйДи Банк'),
    Bank(BankId.ineco, '65351947-217c-4593-9011-941b88ee7baf', 'Ինեկոբանկ', 'Inecobank', 'Инекобанк'),
    Bank(BankId.mellat, 'f288c3fc-f524-468c-bff7-fbd9bbc6b8d7', 'Մելլաթ բանկ', 'Mellat Bank', 'Меллат Банк'),
    Bank(BankId.uni, '133240fd-5910-421d-b417-5a9cedd5f5f7', 'Յունիբանկ', 'Unibank', 'Юнибанк/Армения'),
    Bank(BankId.vtb, '69460818-02ec-456e-8d09-8eeff6494bce', 'ՎՏԲ-Հայաստան Բանկ', 'VTB Bank (Armenia)', 'ВТБ Армения'),
]


def get_by_name(name: str) -> Bank:
    """Returns a bank with given name.

    :param str name: name of the wanted bank. Can be in any supported language
    :return Bank:
    """
    return next(
        (bank for bank in BANKS if bank.hy_name == name or bank.en_name == name or bank.ru_name == name), None)


def get_by_id(id_: Union[BankId, str]) -> Bank:
    """Returns a bank with given id.

    :param id_: id of the wanted bank
    :return Bank:
    """
    if isinstance(id_, BankId):
        id_ = id_.value
    return next(
        (bank for bank in BANKS if bank.id_.value == id_), None)
